<script lang="ts">
  // v6g: osady i sytuacje — podgląd wszystkiego, co wpływa na ceny w osadzie, i edycja MG (ustawienia → ust.osady,
  // ust.nowe_osady, ust.koniunktury, ust.nowe_sytuacje). Zmiany działają od razu we wszystkich zakładkach.
  import { stan } from '../lib/stan.svelte';
  import { mon, mnoz, pl, proc, norm, parsujCene, parsujMnoznik } from '../lib/format';
  import { koniunkturaEfektywna, wyliczOsade, cenyStrefy, etykietaKoniunktury } from '../silnik.js';
  import Podpowiedz from '../komponenty/Podpowiedz.svelte';

  const d = $derived(stan.d), u = $derived(stan.ust);
  const osady = $derived(d.osady.osady as any[]);
  const sytuacje = $derived(d.koniunktura.koniunktury as any[]);
  const kategorie = $derived(d.koniunktura.kategorie as string[]);
  const TYPY = ['wies', 'miasteczko', 'miasto', 'metropolia'];
  const nazwaSyt = (id?: string) => sytuacje.find(k => k.id === (id ?? 'normalna'))?.nazwa ?? '—';
  const tagi = $derived([...new Set(d.cennik.pozycje.flatMap((c: any) => c.branze ?? []))].sort() as string[]);
  const slug = (s: string) => s.trim().toLowerCase().replace(/ł/g, 'l').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  const kopia = (x: any) => { const { wlasna, ...r } = structuredClone($state.snapshot(x)); return r; };

  let msg = $state(''), zly = $state(false);
  const blad = (t: string) => { msg = t; zly = true; };
  const ok = (t = '') => { msg = t; zly = false; };
  function liczba(txt: string, fn: (m: number) => void) {
    const m = parsujMnoznik(txt);
    if (m == null) return;
    if (Number.isNaN(m) || m < 0) return blad(`„${txt}” to nie liczba.`);
    fn(m); ok();
  }
  const ustaw = (fn: (x: any) => void) => stan.zmienUst(fn);

  /* ------------------------------------------------ lista */
  let q = $state(''), fProw = $state(''), fSyt = $state('');
  const prowincje = $derived([...new Set(osady.map(o => o.prowincja).filter(Boolean))].sort() as string[]);
  const lista = $derived(osady.filter(o => (!q || norm(o.nazwa).includes(norm(q)))
    && (!fProw || (fProw === '-' ? !o.prowincja : o.prowincja === fProw))
    && (!fSyt || (o.sytuacja ?? 'normalna') === fSyt)));
  const zmieniona = (id: string) => !!u.osady?.[id];

  /* ------------------------------------------------ jedna osada */
  const o = $derived(osady.find(x => x.id === stan.trasa.sciezka) ?? null);
  const kon = $derived(sytuacje.find(k => k.id === (o?.sytuacja ?? 'normalna')) ?? sytuacje[0]);
  const efekt = $derived(o ? koniunkturaEfektywna(d, kon, { osada: o }) : null);
  const typOs = $derived(o ? d.rynek.typ_osady?.kategorie?.[o.dostepnosc] ?? {} : {});
  const zam = $derived(d.handel.zamoznosc);
  const dost = $derived(o ? d.rynek.dostepnosc.tabela[o.dostepnosc] ?? {} : {});

  function zmien(pola: any) { const id = o.id; ustaw(x => { x.osady ??= {}; x.osady[id] = { ...(x.osady[id] || {}), ...pola }; }); ok(); }
  // Typ, zamożność, strefa → mnożnik, limit, Dostępność i ceny strefy liczone od nowa (jak dane_v6c.py). Mnożnik można potem nadpisać.
  function zmienWyliczane(pola: any) {
    const s = { typ: o.typ, zamoznosc: o.zamoznosc, strefa: o.strefa, ...pola };
    if (!s.typ) {   // osada-wzorzec (Wieś, Miasto…): zamożność rządzi tylko towarem nielegalnym
      zmien({ ...pola, ...(pola.strefa ? { kategorie: cenyStrefy(d, pola.strefa) } : {}) }); return;
    }
    const w: any = wyliczOsade(d, s);
    if (!w.limit_omijaja_podtypy) w.limit_omijaja_podtypy = null;
    const st = d.handel.strefy.find((x: any) => x.id === s.strefa);
    zmien({ ...pola, ...w, ...(st && o.grupa && !o.wlasna ? { grupa: st.nazwa } : {}) });
  }
  function ustawTag(t: string, m: number | null) {
    const n = { ...(o.tagi || {}) };
    if (m == null || m === 1) delete n[t]; else n[t] = m;
    zmien({ tagi: n });
  }
  let nowyTag = $state(''), nowyTagM = $state('0,9');
  function dodajTag() {
    const t = nowyTag.trim(), m = parsujMnoznik(nowyTagM);
    if (!tagi.includes(t)) return blad(`Nie ma branży „${t}” w cenniku.`);
    if (m == null || Number.isNaN(m)) return blad('Mnożnik specjalności, np. 0,9 albo 1,1.');
    ustawTag(t, m); nowyTag = '';
  }
  function przywroc() { const id = o.id; ustaw(x => { delete x.osady[id]; }); ok('Przywrócono dane osady.'); }

  /* ------------------------------------------------ nowa osada */
  let nNazwa = $state(''), nWzor = $state('miasteczko');
  function dodajOsade() {
    const nazwa = nNazwa.trim(), id = 'mg-' + slug(nazwa), w = osady.find(x => x.id === nWzor);
    if (!nazwa) return blad('Podaj nazwę osady.');
    if (osady.some(x => x.id === id)) return blad('Taka osada już jest.');
    const nowa = { ...kopia(w), id, nazwa, grupa: 'Osady MG', typ: w.typ ?? (TYPY.includes(w.id) ? w.id : 'miasteczko'),
      uwaga: `Osada MG na wzór: ${w.nazwa}.`, populacja_poradnik: null, populacja_przed_wojna: null };
    ustaw(x => { x.nowe_osady = [...(x.nowe_osady || []), nowa]; });
    nNazwa = ''; ok(`Dodano „${nazwa}”.`); stan.idz('#osady/' + id);
  }
  function usunOsade() {
    const id = o.id, nazwa = o.nazwa;
    ustaw(x => { x.nowe_osady = (x.nowe_osady || []).filter((y: any) => y.id !== id); delete x.osady?.[id]; });
    ok(`Usunięto „${nazwa}”.`); stan.idz('#osady');
  }

  /* ------------------------------------------------ sytuacje */
  let konId = $state('normalna');
  const k = $derived(sytuacje.find(x => x.id === konId) ?? sytuacje[0]);
  const ileOsad = (id: string) => osady.filter(x => (x.sytuacja ?? 'normalna') === id).length;
  const zmienKon = (fn: (y: any) => void) => { const id = k.id; ustaw(x => { x.koniunktury ??= {}; fn(x.koniunktury[id] ??= {}); }); ok(); };
  let sNazwa = $state(''), sWzor = $state('normalna');
  function dodajSytuacje() {
    const nazwa = sNazwa.trim(), id = 'mg-' + slug(nazwa), w = sytuacje.find(x => x.id === sWzor);
    if (!nazwa) return blad('Podaj nazwę sytuacji.');
    if (sytuacje.some(x => x.id === id)) return blad('Taka sytuacja już jest.');
    const { opis_cen, opis_popytu, ...r } = kopia(w);
    ustaw(x => { x.nowe_sytuacje = [...(x.nowe_sytuacje || []), { ...r, id, nazwa, opis: `Sytuacja MG na wzór: ${w.nazwa}.` }]; });
    sNazwa = ''; konId = id; ok(`Dodano sytuację „${nazwa}”. Ustaw jej mnożniki poniżej.`);
  }
  function usunSytuacje() {
    const id = k.id, nazwa = k.nazwa;
    ustaw(x => { x.nowe_sytuacje = (x.nowe_sytuacje || []).filter((y: any) => y.id !== id); delete x.koniunktury?.[id]; });
    konId = 'normalna'; ok(`Usunięto „${nazwa}”. Osady z tą sytuacją wracają do Normalnej.`);
  }
</script>

<h2>Osady</h2>
<details class="opis">
  <summary>Co wpływa na ceny w osadzie</summary>
  <p>Cena u kupca = cena bazowa × marża × <b>mnożnik osady</b> × <b>ceny strefy handlowej</b> × <b>typ osady</b> × <b>sytuacja</b>
    × pora roku × wahania × <b>specjalności</b> × zapas i popyt. Mnożnik osady = typ × zamożność. Zmiana typu, zamożności
    albo strefy liczy mnożnik i ceny strefy od nowa; potem każdą liczbę możesz nadpisać ręcznie.</p>
  <p>Zmiany zostają w tej przeglądarce i trafiają do eksportu ustawień (Edycja cen → JSON). Plik wgrany jako
    <code>data/ustawienia.json</code> trafia też do Kompendium (<code>node narzedzia/eksport_kompendium.mjs</code>).</p>
</details>
{#if msg}<div class="komunikat" class:zly>{msg}</div>{/if}

{#if o}
  <div class="pasek nie-drukuj"><a href="#osady">← wszystkie osady</a></div>
  <div class="panel">
    <h3>{o.nazwa}{#if o.wlasna}<span class="znacznik zloty">osada MG</span>{:else if zmieniona(o.id)}<span class="znacznik zloty">MG</span>{/if}</h3>
    <p class="drugi male">{o.grupa ?? 'Typ osady (wzorzec)'}{o.prowincja ? ' · ' + o.prowincja : ''}{o.wolne_miasto ? ' · wolne miasto' : ''}{o.dochody ? ' · dochody: ' + o.dochody : ''}</p>
    <div class="pasek">
      {#if o.wlasna}<label class="pole"><span>Nazwa</span><input value={o.nazwa} onchange={e => e.currentTarget.value.trim() && zmien({ nazwa: e.currentTarget.value.trim() })} /></label>{/if}
      <label class="pole"><span>Prowincja</span><input value={o.prowincja ?? ''} list="osady-prow" onchange={e => zmien({ prowincja: e.currentTarget.value.trim() || null })} />
        <datalist id="osady-prow">{#each prowincje as p}<option value={p}></option>{/each}</datalist></label>
      <label class="pole waskie"><span>Populacja</span><input value={o.populacja ?? ''} inputmode="numeric"
        onchange={e => { const v = e.currentTarget.value.replace(/\D/g, ''); zmien({ populacja: v ? +v : null }); }} /></label>
      <label class="pole"><span>Sytuacja domyślna <Podpowiedz tekst="Podstawia się przy wyborze osady w Generatorze, Cenniku, Czynszach i Zamówieniu. Przy stole zmienisz ją ręcznie." /></span>
        <select value={o.sytuacja ?? 'normalna'} onchange={e => zmien({ sytuacja: e.currentTarget.value === 'normalna' ? null : e.currentTarget.value })}>
          {#each sytuacje as s}<option value={s.id}>{s.nazwa}</option>{/each}</select></label>
    </div>
    <div class="pasek">
      {#if o.typ}<label class="pole waskie"><span>Typ</span><select value={o.typ} onchange={e => zmienWyliczane({ typ: e.currentTarget.value })}>
        {#each TYPY as t}<option value={t}>{osady.find(x => x.id === t)?.nazwa ?? t}</option>{/each}</select></label>{/if}
      <label class="pole waskie"><span>Zamożność <Podpowiedz tekst="Poradnik Staroświatowca: 1–5. Mnoży ceny ośrodka i rządzi towarem nielegalnym (tab. 3-11)." /></span>
        <select value={String(o.zamoznosc ?? 3)} onchange={e => zmienWyliczane({ zamoznosc: +e.currentTarget.value })}>
          {#each Object.entries(zam.mnoznik_cen) as [z, m]}<option value={z}>{z} (×{pl(m as number)})</option>{/each}</select></label>
      <label class="pole"><span>Strefa handlowa</span><select value={o.strefa ?? ''} onchange={e => e.currentTarget.value && zmienWyliczane({ strefa: e.currentTarget.value })}>
        <option value="">— średnia Imperium —</option>{#each d.handel.strefy as s}<option value={s.id}>{s.nazwa}</option>{/each}</select></label>
      <label class="pole waskie"><span>Mnożnik osady</span><input value={pl(o.mnoznik, 3)} onchange={e => liczba(e.currentTarget.value, m => zmien({ mnoznik: m }))} /></label>
      <label class="pole waskie"><span>Limit towaru</span><input value={o.limit_p == null ? '' : mon(o.limit_p)} placeholder="bez limitu"
        onchange={e => { const p = parsujCene(e.currentTarget.value); if (Number.isNaN(p)) blad('Limit: „15 ZK” albo puste.'); else zmien({ limit_p: p }); }} /></label>
    </div>
    <div class="pasek">
      <label class="chip"><input type="checkbox" checked={!!o.rzadkie_latwiej} onchange={e => zmien({ rzadkie_latwiej: e.currentTarget.checked })} /> Rzadkie jak Ograniczone</label>
      <label class="chip"><input type="checkbox" checked={!!o.import} onchange={e => zmien({ import: e.currentTarget.checked })} /> Import (Egzotyczne częściej)</label>
      <label class="chip"><input type="checkbox" checked={!!o.wolne_miasto} onchange={e => zmien({ wolne_miasto: e.currentTarget.checked })} /> Wolne miasto</label>
    </div>
    <label class="pole"><span>Uwagi</span><input value={o.uwaga ?? ''} onchange={e => zmien({ uwaga: e.currentTarget.value.trim() || null })} /></label>
    <div class="przyciski">
      {#if zmieniona(o.id) && !o.wlasna}<button class="maly" onclick={przywroc}>Przywróć dane osady</button>{/if}
      {#if o.wlasna}<button class="maly niebezp" onclick={usunOsade}>Usuń osadę</button>{/if}
    </div>
  </div>

  <div class="siatka" style="margin-top:14px">
    <div class="panel">
      <h3>Ceny kategorii <Podpowiedz tekst="Razem = mnożnik osady × strefa × typ osady × sytuacja domyślna (bez marży kupca, pory roku i wahań)." /></h3>
      <div class="tabela"><table>
        <thead><tr><th>Kategoria</th><th class="num">Strefa</th><th class="num">Typ</th><th class="num">Sytuacja</th><th class="num">Razem</th></tr></thead>
        <tbody>{#each kategorie as kat}
          {@const r = o.mnoznik * (efekt.kategorie[kat]?.cena ?? 1)}
          <tr><td>{kat}</td>
            <td class="num"><input class="w-tabeli" value={pl(o.kategorie?.[kat]?.cena ?? 1, 3)}
              onchange={e => liczba(e.currentTarget.value, m => zmien({ kategorie: { ...(o.kategorie || {}), [kat]: { cena: m } } }))} /></td>
            <td class="num">{mnoz(typOs[kat] ?? 1)}</td>
            <td class="num">{mnoz(kon.kategorie[kat]?.cena ?? 1)}{#if kon.kategorie[kat]?.popyt} <span class="szary">popyt {kon.kategorie[kat].popyt > 0 ? '+' : ''}{kon.kategorie[kat].popyt}</span>{/if}</td>
            <td class="num" class:plus={r > 1.005} class:minus={r < 0.995}><b>{proc(r)}</b></td></tr>
        {/each}</tbody></table></div>
    </div>
    <div>
      <div class="panel">
        <h3>Specjalności <Podpowiedz tekst="Tag branży z cennika × mnożnik ceny, np. futra ×0,8 w Middenheim. Kilka naraz: łącznie ×0,8–×1,2." /></h3>
        {#each Object.entries(o.tagi || {}) as [t, m]}
          <div class="pasek"><span style="min-width:9em">{t}</span>
            <input class="w-tabeli" value={pl(m as number)} onchange={e => liczba(e.currentTarget.value, x => ustawTag(t, x))} />
            <button class="maly" onclick={() => ustawTag(t, null)}>usuń</button></div>
        {:else}<p class="szary male">Brak — ceny jak w strefie.</p>{/each}
        <div class="pasek">
          <label class="pole"><span>Branża</span><input bind:value={nowyTag} list="osady-tagi" placeholder="np. futra" />
            <datalist id="osady-tagi">{#each tagi as t}<option value={t}></option>{/each}</datalist></label>
          <label class="pole waskie"><span>Mnożnik</span><input bind:value={nowyTagM} /></label>
          <button onclick={dodajTag}>Dodaj</button>
        </div>
      </div>
      <div class="panel" style="margin-top:14px">
        <h3>Dostępność i towar nielegalny</h3>
        <p class="male">Szansa, że rzecz jest w sklepie ({o.dostepnosc}):
          {['Powszechna', 'Ograniczona', 'Rzadka', 'Egzotyczna'].map(x => {
            const p = x === 'Rzadka' && o.rzadkie_latwiej ? dost['Ograniczona'] : x === 'Egzotyczna' && o.import ? d.rynek.dostepnosc.import_egzotyczne : dost[x];
            return `${x} ${pl((p ?? 1) * 100, 1)}%`; }).join(', ')}.</p>
        <p class="male">Limit ceny towaru: {o.limit_p == null ? 'bez limitu' : mon(o.limit_p)}{o.limit_omijaja_podtypy ? ' (nie dotyczy żywego inwentarza i podstawowej żywności)' : ''}.</p>
        <p class="male">Nielegalne (zamożność {o.zamoznosc ?? 3}): cena ×{pl(zam.nielegalne[o.zamoznosc ?? 3]?.cena ?? 1)}, Dostępność {zam.nielegalne[o.zamoznosc ?? 3]?.dostepnosc ?? '—'}.</p>
      </div>
    </div>
  </div>
{:else}
  <div class="pasek">
    <label class="pole"><span>Szukaj</span><input bind:value={q} placeholder="nazwa" /></label>
    <label class="pole"><span>Prowincja</span><select bind:value={fProw}><option value="">wszystkie</option><option value="-">typy osad i bez prowincji</option>
      {#each prowincje as p}<option value={p}>{p}</option>{/each}</select></label>
    <label class="pole"><span>Sytuacja</span><select bind:value={fSyt}><option value="">każda</option>
      {#each sytuacje as s}<option value={s.id}>{s.nazwa} ({ileOsad(s.id)})</option>{/each}</select></label>
  </div>
  <div class="tabela karty"><table class="karty">
    <thead><tr><th>Osada</th><th>Prowincja</th><th class="num">Populacja</th><th class="num">Zamożność</th><th class="num">Mnożnik</th><th>Sytuacja</th><th>Specjalności</th></tr></thead>
    <tbody>{#each lista as x}
      <tr><td class="tytul"><a href="#osady/{x.id}">{x.nazwa}</a>{#if x.wlasna}<span class="znacznik zloty">osada MG</span>{:else if zmieniona(x.id)}<span class="znacznik zloty">MG</span>{/if}
          <div class="szary male">{x.grupa ?? 'typ osady'}</div></td>
        <td data-l="Prowincja">{x.prowincja ?? '—'}</td>
        <td class="num" data-l="Populacja">{x.populacja ? x.populacja.toLocaleString('pl') : '—'}</td>
        <td class="num" data-l="Zamożność">{x.zamoznosc ?? '—'}</td>
        <td class="num" data-l="Mnożnik" class:plus={x.mnoznik > 1} class:minus={x.mnoznik < 1}>{proc(x.mnoznik)}</td>
        <td data-l="Sytuacja">{nazwaSyt(x.sytuacja)}</td>
        <td class="male" data-l="Specjalności">{Object.entries(x.tagi || {}).map(([t, m]) => `${t} ×${pl(m as number)}`).join(', ') || '—'}</td></tr>
    {:else}<tr><td class="pelna szary">Nic nie pasuje.</td></tr>{/each}</tbody></table></div>

  <details class="sekcja">
    <summary><span>Nowa osada</span><span class="szary male">{(u.nowe_osady || []).length} dodanych</span></summary>
    <div class="panel" style="border-top:0;border-radius:0 0 var(--r) var(--r)">
      <div class="pasek">
        <label class="pole"><span>Nazwa</span><input bind:value={nNazwa} placeholder="np. Grünburg" /></label>
        <label class="pole"><span>Na wzór</span><select bind:value={nWzor}>{#each osady as x}<option value={x.id}>{x.nazwa}</option>{/each}</select></label>
        <button class="glowny" onclick={dodajOsade}>Dodaj osadę</button>
      </div>
      <p class="szary male">Kopiuje mnożniki, strefę, specjalności i sytuację wzoru. Potem zmienisz je w karcie osady.</p>
    </div>
  </details>
{/if}

<details class="sekcja" style="margin-top:14px" open={!o}>
  <summary><span>Sytuacje</span><span class="szary male">{sytuacje.length}, w tym {(u.nowe_sytuacje || []).length} MG</span></summary>
  <div class="panel" style="border-top:0;border-radius:0 0 var(--r) var(--r)">
    <div class="pasek">
      <label class="pole"><span>Sytuacja</span><select bind:value={konId}>{#each sytuacje as s}<option value={s.id}>{s.nazwa}{s.wlasna ? ' (MG)' : ''} — {ileOsad(s.id)} osad</option>{/each}</select></label>
      {#if k.wlasna}<label class="pole"><span>Nazwa</span><input value={k.nazwa} onchange={e => e.currentTarget.value.trim() && zmienKon(y => { y.nazwa = e.currentTarget.value.trim(); })} /></label>{/if}
    </div>
    <p class="male drugi">{etykietaKoniunktury(d, k)}{k.opis ? ' — ' + k.opis : ''}</p>
    <div class="tabela"><table>
      <thead><tr><th>Kategoria</th><th class="num">Cena</th><th class="num">Popyt</th></tr></thead>
      <tbody>{#each kategorie as kat}
        {@const v = k.kategorie[kat] ?? { cena: 1, popyt: 0 }}
        <tr><td>{kat}</td>
          <td class="num"><input class="w-tabeli" value={pl(v.cena)} onchange={e => liczba(e.currentTarget.value, m => zmienKon(y => { y.kategorie ??= {}; y.kategorie[kat] = { ...(y.kategorie[kat] || {}), cena: m }; }))} /></td>
          <td class="num"><select value={v.popyt ?? 0} onchange={e => zmienKon(y => { y.kategorie ??= {}; y.kategorie[kat] = { ...(y.kategorie[kat] || {}), popyt: +e.currentTarget.value }; })}>
            {#each [-1, 0, 1] as p}<option value={p}>{p > 0 ? '+1' : p}</option>{/each}</select></td></tr>
      {/each}
        <tr><td><b>Czynsz</b></td><td class="num"><input class="w-tabeli" value={pl(k.czynsz?.mnoznik ?? 1)} onchange={e => liczba(e.currentTarget.value, m => zmienKon(y => { y.czynsz = m; }))} /></td><td></td></tr>
      </tbody>
    </table></div>
    <div class="przyciski">
      {#if u.koniunktury?.[k.id] && !k.wlasna}<button class="maly" onclick={() => { const id = k.id; ustaw(x => { delete x.koniunktury[id]; }); ok('Przywrócono sytuację.'); }}>Przywróć tę sytuację</button>{/if}
      {#if k.wlasna}<button class="maly niebezp" onclick={usunSytuacje}>Usuń sytuację</button>{/if}
    </div>
    <div class="pasek" style="margin-top:10px;border-top:1px solid var(--linia);padding-top:10px">
      <label class="pole"><span>Nowa sytuacja</span><input bind:value={sNazwa} placeholder="np. Głód po żniwach" /></label>
      <label class="pole"><span>Na wzór</span><select bind:value={sWzor}>{#each sytuacje as s}<option value={s.id}>{s.nazwa}</option>{/each}</select></label>
      <button class="glowny" onclick={dodajSytuacje}>Dodaj sytuację</button>
    </div>
  </div>
</details>
