<script lang="ts">
  import { stan } from '../lib/stan.svelte';
  import { mon, norm, pl, mnoz, parsujCene, parsujMnoznik } from '../lib/format';
  import { mnoznikKlasy, cenaTypowa, handlujacy, robot, POROWNANIE, zrodloNazwa, TYPY } from '../lib/ceny';
  import { etykietaKoniunktury, jakoscZ, szansaDostepnosci } from '../silnik.js';
  import WyborOsady from '../komponenty/WyborOsady.svelte';
  import { daneBazowe } from '../lib/dane';
  // Ceny domyślne (bez ustawień MG) — komentarz i podstawa historyczna opisują właśnie je.
  const DOMYSLNE: Record<string, number> = Object.fromEntries(daneBazowe.cennik.pozycje.map((c: any) => [c.id, c.cena_p]));
  import Podpowiedz from '../komponenty/Podpowiedz.svelte';
  import WyborCech from '../komponenty/WyborCech.svelte';
  let jakosc = $state<Record<string, number>>({});

  const d = $derived(stan.d);
  let q = $state(''), kat = $state(''), otwarte = $state<string | null>(null);
  let flagi = $state<Record<string, boolean>>({});
  let uKupca = $state(false), kupId = $state('zbrojmistrz'), osId = $state('miasteczko'), konId = $state('normalna');
  let grupowy = $state(''), msg = $state('');

  const FLAGI: [string, string, (c: any) => boolean][] = [
    ['raw', 'zmienione wobec podręcznika', c => c.cena_raw_p != null && c.cena_raw_p !== c.cena_p],
    ['zrodlo', 'bez źródła historycznego', c => !c.podstawa_hist],
    ['handel', 'nie w handlu', c => c.typ !== 'towar'],
    ['mg', 'zmienione przez MG', c => !!c.nadpisane || !!c.wlasna],
    ['kampania', 'pozycje kampanii', c => c.cena_raw_p == null],
  ];
  const kategorie = $derived([...new Set(d.cennik.pozycje.map((c: any) => c.kat))] as string[]);
  const widoczne = $derived.by(() => {
    const n = norm(q.trim()), f = FLAGI.filter(([k]) => flagi[k]);
    return d.cennik.pozycje.filter((c: any) => (!kat || c.kat === kat) && (!n || norm(c.nazwa).includes(n) || norm(c.kat).includes(n))
      && f.every(([, , t]) => t(c)));
  });
  const grupy = $derived(kategorie.map(k => [k, widoczne.filter((c: any) => c.kat === k)] as const).filter(([, l]) => l.length));
  const kup = $derived(d.kupcy.kupcy.find((k: any) => k.id === kupId));
  const lok = $derived(d.osady.osady.find((o: any) => o.id === osId));
  const kon = $derived(d.koniunktura.koniunktury.find((k: any) => k.id === konId));
  const handluje = (c: any) => handlujacy(d, c).includes(kup);
  // Szansa, że rzecz jest w sklepie w wybranej osadzie (PG s. 290 + zasady kampanii).
  const DOST_OPIS = (c: any) => {
    const p = szansaDostepnosci(d, { kupiec: kup, osada: lok, pozycja: c });
    return `${lok.nazwa}: ${p >= 1 ? 'zawsze' : p >= 0.01 ? Math.round(p * 100) + '%' : (p * 100).toFixed(1) + '%'}` + (p < 0.5 ? ' (zwykle na zamówienie)' : '');
  };
  const cechy = $derived(Object.fromEntries(d.bron_cechy.pozycje.map((p: any) => [p.id, p])));

  function zastosujGrupowy() {
    const m = parsujMnoznik(grupowy);
    if (m == null || Number.isNaN(m) || m <= 0) { msg = 'Wpisz mnożnik, np. 1,2 albo −10%.'; return; }
    const ids = widoczne.map((c: any) => c.id);
    stan.zmienUst(u => {
      for (const id of ids) {
        const o = u.pozycje[id];
        u.pozycje[id] = o?.cena_p != null ? { cena_p: Math.max(1, Math.round(o.cena_p * m)) } : { mnoznik: +((o?.mnoznik ?? 1) * m).toFixed(4) };
      }
    });
    msg = `${mnoz(m)} dla ${ids.length} pozycji. Cofniesz to w Edycji cen.`; grupowy = '';
  }
  let cenaPoz = $state(''), mnozPoz = $state('');
  function ustawPoz(id: string) {
    const p = parsujCene(cenaPoz), m = parsujMnoznik(mnozPoz);
    if (p != null && !Number.isNaN(p)) stan.zmienUst(u => { u.pozycje[id] = { cena_p: p }; });
    else if (m != null && !Number.isNaN(m)) stan.zmienUst(u => { u.pozycje[id] = { mnoznik: m }; });
    else return;
    cenaPoz = mnozPoz = '';
  }
  const usunNadpisanie = (id: string) => stan.zmienUst(u => { delete u.pozycje[id]; });
  const usunWlasna = (id: string) => stan.zmienUst(u => { u.nowe = u.nowe.filter((x: any) => x.id !== id); delete u.pozycje[id]; });
</script>

<h2>Cennik <span class="szary male">{widoczne.length} z {d.cennik.pozycje.length}</span></h2>
<details class="opis">
  <summary>Jak czytać ceny</summary>
  <p><b>Podręcznik</b> — cena z podręcznika (RAW), bez zmian kampanii. Przekreślona, gdy nasza jest inna.</p>
  <p><b>×1</b> — poziom przed mnożnikiem klasy cenowej. Od niego liczą się limity osad i ilości w sklepie.</p>
  <p><b>Cena bazowa</b> — cena wytwórcy w obowiązującym cenniku: u źródła, hurtem. Gracz nigdy jej nie płaci wprost —
    kupiec dolicza marżę. Cenę kupca pokazuje przełącznik „Ceny u kupca” i zakładka Kupcy.</p>
  <p><b>Robót</b> — ile Robót (netto, tyle realnie się odkłada) trzeba zebrać: chłop / robotnik (Brąz 3) — mistrz z czeladnikami (Srebro 3).</p>
  <p>Kliknij wiersz, żeby zobaczyć źródło, komentarz, cechy broni, kto to sprzedaje i zmienić cenę.</p>
</details>

<div class="pasek">
  <label class="pole"><span>Szukaj</span><input type="search" bind:value={q} placeholder="np. kaplon, miecz, siodło…" /></label>
  <label class="pole"><span>Kategoria</span>
    <select bind:value={kat}><option value="">wszystkie</option>{#each kategorie as k}<option>{k}</option>{/each}</select></label>
</div>
<div class="chipy">
  {#each FLAGI as [k, nazwa]}
    <button class="chip" aria-pressed={!!flagi[k]} onclick={() => (flagi[k] = !flagi[k])}>{nazwa}</button>
  {/each}
  <button class="chip" aria-pressed={uKupca} onclick={() => (uKupca = !uKupca)}>ceny u kupca</button>
</div>

{#if uKupca}
  <div class="panel">
    <div class="pasek">
      <label class="pole"><span>Kupiec</span><select bind:value={kupId}>
        {#each d.kupcy.kupcy as k}<option value={k.id}>{k.nazwa} ({mnoz(k.marza)})</option>{/each}</select></label>
      <label class="pole"><span>Osada</span><WyborOsady bind:value={osId} /></label>
      <label class="pole"><span>Sytuacja</span><select bind:value={konId}>
        {#each d.koniunktura.koniunktury as k}<option value={k.id}>{etykietaKoniunktury(d, k, { krotko: true })}</option>{/each}</select></label>
    </div>
    <p class="male drugi">„U kupca” = cena bazowa × marża × preferencja × osada × sytuacja.
      <Podpowiedz tekst="To cena typowa. W sklepie dochodzi kaprys kupca (zwykle ±10%) i rynek: zapas × popyt (od ×0,65 przy zaległym towarze do ×1,7 przy ostatnich sztukach w wysokim popycie). Kreska = ten kupiec tym nie handluje." /></p>
  </div>
{/if}

<details class="opis nie-drukuj">
  <summary>Zmień ceny widocznych pozycji ({widoczne.length})</summary>
  <p class="male drugi">Mnożnik działa na to, co teraz widać (filtry i wyszukiwarka). Np. kategoria „Pancerze” i ×1,2.
    Zapisuje się jako mnożnik każdej pozycji — lista i cofanie w zakładce Edycja cen.</p>
  <div class="pasek">
    <label class="pole waskie"><span>Mnożnik</span><input bind:value={grupowy} placeholder="1,2 albo -10%" /></label>
    <button class="glowny" onclick={zastosujGrupowy}>Zastosuj</button>
  </div>
  {#if msg}<p class="male">{msg}</p>{/if}
</details>

{#each grupy as [k, lista] (k)}
  <details class="sekcja" open={!!q || !!kat || grupy.length < 4}>
    <summary><span>{k}</span><span class="szary male">{lista.length}</span></summary>
    <div class="tabela karty">
      <table class="karty">
        <thead><tr>
          <th>Przedmiot</th><th class="num">Podręcznik</th><th class="num">×1</th>
          {#if uKupca}<th class="num">U kupca</th>{:else}<th>Klasa</th>{/if}
          <th class="num">Cena bazowa</th><th class="num">Robót: chłop / Srebro 3</th>
        </tr></thead>
        <tbody>
          {#each lista as c (c.id)}
            {@const mk = mnoznikKlasy(d, stan.ust, c)}
            <tr class="klik" class:otwarty={otwarte === c.id} onclick={() => (otwarte = otwarte === c.id ? null : c.id)}>
              <td class="tytul">{c.nazwa} {#if c.dostepnosc}<span class="szary male">({c.dostepnosc})</span>{/if}
                {#if c.nielegalny}<span class="znacznik czerwony">nielegalny</span>{/if}
                {#if c.typ !== 'towar'}<span class="znacznik niebieski">nie w handlu</span>{/if}
                {#if c.wlasna}<span class="znacznik fiolet">MG: nowa</span>{:else if c.nadpisane}<span class="znacznik zloty">MG</span>{/if}
                {#if !c.podstawa_hist}<span class="znacznik">bez źródła</span>{/if}
              </td>
              <td class="num" data-l="Podręcznik"><span class:przekreslone={c.cena_raw_p != null && c.cena_raw_p !== c.cena_p}>{c.cena_raw_p == null ? '—' : mon(c.cena_raw_p)}</span></td>
              <td class="num szary zwin" data-l="×1">{mon(c.cena_ref_p)}</td>
              {#if uKupca}
                <td class="num" data-l="U kupca">{#if c.typ === 'towar' && handluje(c)}<span class="cena">{mon(cenaTypowa(d, kup, lok, kon, c))}</span>{:else}<span class="szary">—</span>{/if}</td>
              {:else}
                <td class="zwin" data-l="Klasa">{c.klasa} {mnoz(mk.m)}{#if mk.znak !== 1} · znak stanu {mnoz(mk.znak)}{/if}</td>
              {/if}
              <td class="num" data-l="Cena bazowa"><span class="cena">{mon(c.cena_p)}</span></td>
              <td class="num zwin" data-l="Robót: chłop / Srebro 3">{POROWNANIE.map(s => pl(robot(d, c.cena_p, s), 1)).join(' / ')}</td>
            </tr>
            {#if otwarte === c.id}
              {@const bc = cechy[c.id]}
              <tr class="szczegoly"><td class="pelna" colspan="6">
                {#if DOMYSLNE[c.id] != null && DOMYSLNE[c.id] !== c.cena_p}
                  <p class="komunikat male">Cena zmieniona w Edycji cen: {mon(DOMYSLNE[c.id])} → {mon(c.cena_p)} ({mnoz(c.cena_p / DOMYSLNE[c.id])}).
                    Podstawa historyczna, komentarz i uzasadnienie klasy poniżej opisują cenę domyślną {mon(DOMYSLNE[c.id])}.</p>
                {/if}
                <dl class="szczegoly-siatka">
                  <div><dt>Źródło</dt><dd>{zrodloNazwa(c.zrodlo, c.strona)} · {TYPY[c.typ] ?? c.typ}{c.obc != null ? ' · Obc. ' + c.obc : ''}</dd></div>
                  <div><dt>Dostępność</dt><dd>{c.dostepnosc ?? 'nie podana (jak Powszechna)'}
                    <span class="drugi male">— w sklepie: {DOST_OPIS(c)}</span>
                    {#if c.nielegalny}<div class="blad male">Nielegalny: tylko u pasera albo kupca z powiązaniami przestępczymi. {c.nielegalny_uwaga ?? ''}</div>{/if}</dd></div>
                  <div><dt>Podstawa historyczna</dt><dd>{c.podstawa_hist || '— (szacunek)'}</dd></div>
                  {#if c.komentarz}<div><dt>Komentarz</dt><dd>{c.komentarz}</dd></div>{/if}
                  {#if c.uwagi_danych}<div><dt>Uwagi</dt><dd class="drugi">{c.uwagi_danych}</dd></div>{/if}
                  <div><dt>Klasa cenowa</dt><dd>{c.klasa} {mnoz(mk.m)}{#if mk.znak !== 1} × znak stanu {mnoz(mk.znak)}{/if}
                    <span class="drugi male">{d.klasy.uzasadnienia[c.klasa]?.tekst ?? ''}</span>
                    {#if d.klasy.presety[d.klasy.domyslny].mnozniki[c.klasa] != null && d.klasy.presety[d.klasy.domyslny].mnozniki[c.klasa] !== mk.m}
                      <span class="blad male">Uzasadnienie dotyczy mnożnika domyślnego {mnoz(d.klasy.presety[d.klasy.domyslny].mnozniki[c.klasa])}, nie obecnego {mnoz(mk.m)}.</span>{/if}</dd></div>
                  {#if bc?.grupa}<div><dt>Cechy broni (w cenie podstawowej)</dt><dd>{bc.grupa} · {bc.obrazenia}{bc.zasieg ? ' · ' + bc.zasieg : ''}<br />
                    Zalety: {bc.zalety.map((x: any) => x.nazwa).join(', ') || '—'}<br />Wady: {bc.wady.map((x: any) => x.nazwa).join(', ') || '—'}</dd></div>{/if}
                  {#if c.typ === 'towar'}<div><dt>Egzemplarz lepszy albo gorszy</dt><dd>
                    <WyborCech bind:cechy={jakosc} />
                    <span class="male">Cena bazowa egzemplarza: <b class="cena">{mon(Math.round(c.cena_p * jakoscZ(d, jakosc).mnoznik))}</b></span></dd></div>{/if}
                  {#if c.typ === 'towar'}
                    {@const mj = jakoscZ(d, jakosc).mnoznik}
                    <div><dt>U kupców (typowo, {lok.nazwa}, {kon.nazwa}{mj !== 1 ? `, jakość ${mnoz(mj)}` : ''})</dt><dd>
                      {#each handlujacy(d, c) as k}<div class="male">{k.nazwa}: <span class="cena">{mon(Math.round(cenaTypowa(d, k, lok, kon, c) * mj))}</span></div>{:else}—{/each}
                    </dd></div>
                  {:else}
                    <div><dt>Na miejscu ({lok.nazwa}) wg gospody <Podpowiedz tekst={d.rynek.gospoda.opis} /></dt><dd>
                      {#each d.rynek.gospoda.standardy as s}<div class="male">{s.nazwa}: <span class="cena">{mon(Math.round(c.cena_p * lok.mnoznik * s.mnoznik))}</span></div>{/each}
                      <span class="szary male">Osadę zmienisz w „ceny u kupca”.</span></dd></div>
                  {/if}
                </dl>
                <div class="pasek nie-drukuj" style="margin-top:10px">
                  <label class="pole waskie"><span>Nowa cena</span><input bind:value={cenaPoz} placeholder="4 ZK, 15 s 6 p" /></label>
                  <label class="pole waskie"><span>albo mnożnik</span><input bind:value={mnozPoz} placeholder="1,2" /></label>
                  <button onclick={() => ustawPoz(c.id)}>Ustaw</button>
                  {#if stan.ust.pozycje?.[c.id]}<button onclick={() => usunNadpisanie(c.id)}>Przywróć cenę z cennika</button>{/if}
                  {#if c.wlasna}<button class="niebezp" onclick={() => usunWlasna(c.id)}>Usuń pozycję</button>{/if}
                </div>
              </td></tr>
            {/if}
          {/each}
        </tbody>
      </table>
    </div>
  </details>
{:else}
  <p class="szary">Nic nie pasuje.</p>
{/each}
