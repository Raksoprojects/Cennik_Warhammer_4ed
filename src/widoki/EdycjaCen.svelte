<script lang="ts">
  // Ustawienia MG na żywo: każda zmiana → zastosujUstawienia → wszystkie zakładki liczą od nowa.
  import { stan, pusteUstawienia } from '../lib/stan.svelte';
  import { daneBazowe } from '../lib/dane';
  import { mon, mnoz, pl, norm, parsujCene, parsujMnoznik, pobierzPlik, wczytajPlik, dzis } from '../lib/format';
  import { zastosujUstawienia, roznicaCen } from '../silnik.js';
  import { sprawdzWszystko } from '../spojnosc.js';
  import Podpowiedz from '../komponenty/Podpowiedz.svelte';

  const d = $derived(stan.d), u = $derived(stan.ust);
  const baza = zastosujUstawienia(daneBazowe, pusteUstawienia());
  const K = $derived(d.klasy), pr = $derived(K.presety[u.preset || K.domyslny]);
  const zmiany = $derived(roznicaCen(baza, d));
  const ileWKlasie = $derived(d.cennik.pozycje.reduce((m: any, c: any) => (m[c.klasa] = (m[c.klasa] || 0) + 1, m), {}));
  const kategorie = $derived(d.koniunktura.kategorie as string[]);
  let msg = $state(''), zly = $state(false), spojnosc = $state<any[] | null>(null), konId = $state('wojna');
  const kon = $derived(d.koniunktura.koniunktury.find((x: any) => x.id === konId));
  const ZR: Record<string, string> = { dane: 'zielony', zasada: 'zloty', 'dane + zasada': 'zloty', brak: 'czerwony', sprzeczne: 'czerwony' };

  function liczba(txt: string, fn: (m: number) => void) {
    const m = parsujMnoznik(txt);
    if (m == null) return;
    if (Number.isNaN(m) || m < 0) { msg = `„${txt}” to nie liczba.`; zly = true; return; }
    fn(m); msg = ''; zly = false;
  }
  const ustaw = (fn: (x: any) => void) => stan.zmienUst(fn);

  // pojedyncza pozycja
  let pozTxt = $state(''), pozCena = $state('');
  function ustawPozycje() {
    const n = norm(pozTxt.trim()), c = d.cennik.pozycje.find((x: any) => norm(x.nazwa) === n);
    if (!c) { msg = 'Nie ma takiej pozycji.'; zly = true; return; }
    const p = parsujCene(pozCena), m = /^[x×]/i.test(pozCena.trim()) ? parsujMnoznik(pozCena.trim().slice(1)) : null;
    if (m != null && !Number.isNaN(m)) ustaw(x => { x.pozycje[c.id] = { mnoznik: m }; });
    else if (p != null && !Number.isNaN(p)) ustaw(x => { x.pozycje[c.id] = { cena_p: p }; });
    else { msg = 'Wpisz cenę („4 ZK”, „15 s 6 p”) albo mnożnik („×1,2”).'; zly = true; return; }
    pozTxt = pozCena = ''; msg = `${c.nazwa}: zmienione.`; zly = false;
  }
  // nowa pozycja MG
  let nNazwa = $state(''), nKat = $state('Wyposażenie różne'), nCena = $state(''), nDost = $state('Powszechna'), nObc = $state(''), nKom = $state('');
  function dodajNowa() {
    const p = parsujCene(nCena);
    if (!nNazwa.trim() || p == null || Number.isNaN(p) || p <= 0) { msg = 'Nowa pozycja: nazwa i cena są wymagane.'; zly = true; return; }
    const id = 'mg-' + nNazwa.trim().toLowerCase().replace(/ł/g, 'l').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
    if (d.cennik.pozycje.some((c: any) => c.id === id)) { msg = 'Taka pozycja już jest.'; zly = true; return; }
    ustaw(x => { x.nowe.push({ id, nazwa: nNazwa.trim(), kat: nKat, cena_p: p, dostepnosc: nDost, obc: nObc ? +nObc : null, komentarz: nKom.trim() }); });
    msg = `Dodano „${nNazwa.trim()}” (${mon(p)}). Jest w cenniku i u kupców tej kategorii.`; zly = false;
    nNazwa = nCena = nObc = nKom = '';
  }
  // JSON
  let json = $state('');
  $effect(() => { json = JSON.stringify($state.snapshot(stan.ust), null, 1); });
  function zastosujJson() {
    try { const j = JSON.parse(json); zastosujUstawienia(daneBazowe, j); stan.ustaw({ ...pusteUstawienia(), ...j }); msg = 'Zastosowano.'; zly = false; }
    catch (e) { msg = 'Błąd JSON: ' + (e as Error).message; zly = true; }
  }
  async function importuj(e: Event) {
    try { const j = await wczytajPlik(e); if (!j) return; const { opis, przyklad, ...r } = j; zastosujUstawienia(daneBazowe, r); stan.ustaw({ ...pusteUstawienia(), ...r }); msg = 'Wczytano ustawienia z pliku.'; zly = false; }
    catch (err) { msg = 'Nie udało się wczytać: ' + (err as Error).message; zly = true; }
  }
  function sprawdz() {
    spojnosc = sprawdzWszystko(d.cennik, { reguly: d.spojnosc.reguly, testy: d.spojnosc_v4, czynsze: d.czynsze, rynek: d.rynek, bronCechy: d.bron_cechy });
  }
</script>

<h2>Edycja cen</h2>
<details class="opis" open>
  <summary>Jak zmieniać ceny</summary>
  <p>Zmiany działają od razu we wszystkich zakładkach i zostają w tej przeglądarce. Kolejność (późniejsze wygrywają):
    preset → mnożnik klasy → mnożnik kategorii → cena albo mnożnik pozycji. Grupę pozycji zmienisz też w Cenniku:
    filtr + „Zmień ceny widocznych”.</p>
  <p><b>Eksport</b> daje plik w formacie <code>data/ustawienia.json</code>. Wgrany do repozytorium staje się domyślnym cennikiem dla wszystkich.</p>
</details>
{#if msg}<div class="komunikat" class:zly>{msg}</div>{/if}

<div class="panel">
  <div class="pasek">
    <label class="pole"><span>Preset cennika</span><select value={u.preset || K.domyslny} onchange={e => ustaw(x => { x.preset = e.currentTarget.value; })}>
      {#each Object.keys(K.presety) as p}<option value={p}>{p}{p === K.domyslny ? ' (domyślny)' : ''}</option>{/each}</select></label>
    <label class="pole waskie"><span>Premia znaku stanu <Podpowiedz tekst="Miecz jest droższy, bo to symbol stanu: mnożnik dla mieczy, szabli, rapierów itd. (zasada domowa)." /></span>
      <input value={pl(u.premia_znak_stanu ?? pr.premia_znak_stanu)} onchange={e => liczba(e.currentTarget.value, m => ustaw(x => { x.premia_znak_stanu = m; }))} /></label>
    <button class="glowny" onclick={sprawdz}>Sprawdź spójność</button>
  </div>
  {#if spojnosc}
    {#each spojnosc as w}
      <details class="opis" open={w.bledy.length > 0 && !w.ostrzezenie}>
        <summary><span class:blad={w.bledy.length && !w.ostrzezenie} class:ok={!w.bledy.length}>{w.bledy.length ? (w.ostrzezenie ? '⚠ ' : '✖ ') : '✔ '}{w.nazwa} — {w.bledy.length ? w.bledy.length + (w.ostrzezenie ? ' do przejrzenia' : ' błędów') : 'w porządku'}</span></summary>
        <ul class="male">{#each w.bledy as b}<li>{b}</li>{/each}</ul>
      </details>
    {/each}
  {/if}
</div>

<details class="sekcja" open>
  <summary><span>Mnożniki klas cenowych</span><span class="szary male">{Object.keys(pr.mnozniki).length}</span></summary>
  <div class="tabela karty"><table class="karty">
    <thead><tr><th>Klasa</th><th class="num">Pozycji</th><th class="num">Mnożnik</th><th>Skąd</th></tr></thead>
    <tbody>{#each Object.keys(pr.mnozniki) as k}
      {@const uz = K.uzasadnienia[k]}
      <tr><td class="tytul">{k}{#if u.mnozniki[k] != null}<span class="znacznik zloty">MG</span>{/if}</td>
        <td class="num" data-l="Pozycji">{ileWKlasie[k] ?? 0}</td>
        <td class="num" data-l="Mnożnik"><input class="w-tabeli" value={pl(u.mnozniki[k] ?? pr.mnozniki[k])}
          onchange={e => liczba(e.currentTarget.value, m => ustaw(x => { if (m === pr.mnozniki[k]) delete x.mnozniki[k]; else x.mnozniki[k] = m; }))} /></td>
        <td class="pelna male">{#if uz}<span class="znacznik {ZR[uz.zrodlo] ?? ''}">{uz.zrodlo}</span> <span class="drugi">{uz.tekst}</span>{/if}</td></tr>
    {/each}</tbody></table></div>
</details>

<details class="sekcja">
  <summary><span>Mnożniki kategorii</span><span class="szary male">{Object.keys(u.kategorie || {}).length} zmienionych</span></summary>
  <div class="tabela karty"><table class="karty">
    <thead><tr><th>Kategoria</th><th class="num">Mnożnik</th></tr></thead>
    <tbody>{#each kategorie as k}
      <tr><td class="tytul">{k}</td><td class="num" data-l="Mnożnik"><input class="w-tabeli" value={pl(u.kategorie?.[k] ?? 1)}
        onchange={e => liczba(e.currentTarget.value, m => ustaw(x => { x.kategorie ??= {}; if (m === 1) delete x.kategorie[k]; else x.kategorie[k] = m; }))} /></td></tr>
    {/each}</tbody></table></div>
</details>

<details class="sekcja" open={Object.keys(u.pozycje).length > 0}>
  <summary><span>Pojedyncze pozycje</span><span class="szary male">{Object.keys(u.pozycje).length} zmienionych</span></summary>
  <div class="panel" style="border-top:0;border-radius:0 0 var(--r) var(--r)">
    <div class="pasek">
      <label class="pole"><span>Pozycja</span><input bind:value={pozTxt} list="edycja-poz" placeholder="np. miecz" />
        <datalist id="edycja-poz">{#each d.cennik.pozycje as c}<option value={c.nazwa}></option>{/each}</datalist></label>
      <label class="pole waskie"><span>Cena albo ×mnożnik</span><input bind:value={pozCena} placeholder="4 ZK albo ×1,2" /></label>
      <button onclick={ustawPozycje}>Ustaw</button>
      {#if Object.keys(u.pozycje).length}<button class="niebezp" onclick={() => ustaw(x => { x.pozycje = {}; })}>Usuń wszystkie</button>{/if}
    </div>
    {#each Object.entries(u.pozycje) as [id, o]}
      {@const c = d.cennik.pozycje.find((x: any) => x.id === id)}
      <div class="male" style="padding:4px 0;border-top:1px solid var(--linia)">{c?.nazwa ?? id}:
        {(o as any).cena_p != null ? mon((o as any).cena_p) : mnoz((o as any).mnoznik)} → <span class="cena">{c ? mon(c.cena_p) : '—'}</span>
        <button class="maly" onclick={() => ustaw(x => { delete x.pozycje[id]; })}>usuń</button></div>
    {/each}
  </div>
</details>

<details class="sekcja" open={(u.nowe || []).length > 0}>
  <summary><span>Nowe pozycje MG</span><span class="szary male">{(u.nowe || []).length}</span></summary>
  <div class="panel" style="border-top:0;border-radius:0 0 var(--r) var(--r)">
    <div class="pasek">
      <label class="pole"><span>Nazwa</span><input bind:value={nNazwa} /></label>
      <label class="pole"><span>Kategoria</span><select bind:value={nKat}>{#each kategorie as k}<option>{k}</option>{/each}</select></label>
      <label class="pole waskie"><span>Cena bazowa</span><input bind:value={nCena} placeholder="2 ZK 5 s" /></label>
      <label class="pole waskie"><span>Dostępność</span><select bind:value={nDost}>{#each ['Powszechna', 'Ograniczona', 'Rzadka', 'Egzotyczna'] as x}<option>{x}</option>{/each}</select></label>
      <label class="pole waskie"><span>Obc.</span><input bind:value={nObc} type="number" min="0" /></label>
    </div>
    <label class="pole"><span>Komentarz</span><input bind:value={nKom} /></label>
    <div class="przyciski"><button class="glowny" onclick={dodajNowa}>Dodaj pozycję</button></div>
    {#each u.nowe || [] as x}
      <div class="male" style="padding:4px 0;border-top:1px solid var(--linia)">{x.nazwa} ({x.kat}): {mon(x.cena_p)}
        <button class="maly" onclick={() => ustaw(y => { y.nowe = y.nowe.filter((z: any) => z.id !== x.id); delete y.pozycje[x.id]; })}>usuń</button></div>
    {/each}
  </div>
</details>

<details class="sekcja">
  <summary><span>Osady i kupcy</span></summary>
  <div class="siatka" style="padding-top:10px">
    <div class="tabela"><table>
      <thead><tr><th>Osada</th><th class="num">Mnożnik</th></tr></thead>
      <tbody>{#each d.osady.osady as o}<tr><td>{o.nazwa}{#if u.osady[o.id]}<span class="znacznik zloty">MG</span>{/if}</td>
        <td class="num"><input class="w-tabeli" value={pl(o.mnoznik)} onchange={e => liczba(e.currentTarget.value, m => ustaw(x => { x.osady[o.id] = { ...(x.osady[o.id] || {}), mnoznik: m }; }))} /></td></tr>{/each}</tbody>
    </table></div>
    <div class="tabela"><table>
      <thead><tr><th>Kupiec</th><th class="num">Marża</th><th class="num">Skup</th></tr></thead>
      <tbody>{#each d.kupcy.kupcy as k}<tr><td>{k.nazwa}{#if u.kupcy[k.id]}<span class="znacznik zloty">MG</span>{/if}</td>
        <td class="num"><input class="w-tabeli" value={pl(k.marza)} onchange={e => liczba(e.currentTarget.value, m => ustaw(x => { x.kupcy[k.id] = { ...(x.kupcy[k.id] || {}), marza: m }; }))} /></td>
        <td class="num"><input class="w-tabeli" value={pl(k.skup)} onchange={e => liczba(e.currentTarget.value, m => ustaw(x => { x.kupcy[k.id] = { ...(x.kupcy[k.id] || {}), skup: m }; }))} /></td></tr>{/each}</tbody>
    </table></div>
  </div>
  <div class="przyciski"><button class="maly" onclick={() => ustaw(x => { x.osady = {}; x.kupcy = {}; })}>Przywróć osady i kupców</button></div>
</details>

<details class="sekcja">
  <summary><span>Sytuacje (koniunktura)</span></summary>
  <div class="panel" style="border-top:0;border-radius:0 0 var(--r) var(--r)">
    <label class="pole"><span>Sytuacja</span><select bind:value={konId}>{#each d.koniunktura.koniunktury as k}<option value={k.id}>{k.nazwa}</option>{/each}</select></label>
    <div class="tabela" style="margin-top:8px"><table>
      <thead><tr><th>Kategoria</th><th class="num">Cena</th><th class="num">Popyt</th></tr></thead>
      <tbody>{#each kategorie as kat}
        {@const v = kon.kategorie[kat] ?? { cena: 1, popyt: 0 }}
        <tr><td>{kat}</td>
          <td class="num"><input class="w-tabeli" value={pl(v.cena)} onchange={e => liczba(e.currentTarget.value, m => ustaw(x => { const k = x.koniunktury[konId] ??= {}; k.kategorie ??= {}; k.kategorie[kat] = { ...(k.kategorie[kat] || {}), cena: m }; }))} /></td>
          <td class="num"><select value={v.popyt} onchange={e => ustaw(x => { const k = x.koniunktury[konId] ??= {}; k.kategorie ??= {}; k.kategorie[kat] = { ...(k.kategorie[kat] || {}), popyt: +e.currentTarget.value }; })}>
            {#each [-1, 0, 1] as p}<option value={p}>{p > 0 ? '+1' : p}</option>{/each}</select></td></tr>
      {/each}
        <tr><td><b>Czynsz</b></td><td class="num"><input class="w-tabeli" value={pl(kon.czynsz?.mnoznik ?? 1)} onchange={e => liczba(e.currentTarget.value, m => ustaw(x => { (x.koniunktury[konId] ??= {}).czynsz = m; }))} /></td><td></td></tr>
      </tbody>
    </table></div>
    <div class="przyciski"><button class="maly" onclick={() => ustaw(x => { delete x.koniunktury[konId]; })}>Przywróć tę sytuację</button></div>
  </div>
</details>

<details class="sekcja">
  <summary><span>Rynek i upływ czasu</span></summary>
  <div class="tabela"><table><tbody>
    {#each [
      ['preferencje', 'rdzen', 'Preferencja: rdzeń asortymentu'], ['preferencje', 'boczne', 'Preferencja: boczny asortyment'],
      ['cena_minimalna', 'narzut_min', 'Cena minimalna: narzut na koszt'], ['cena_minimalna', 'wyprzedaz', 'Cena minimalna przy wyprzedaży'],
      ['cena_minimalna', 'koszt_wlasny', 'Koszt własny wytwórcy'], ['uplyw_czasu', 'dokupienie', 'Szansa dokupienia rdzenia / tydz.'],
      ['uplyw_czasu', 'nowy_towar', 'Szansa nowego towaru / tydz.'], ['uplyw_czasu', 'rynek_co', 'Nowy popyt i kaprys co (tyg.)'],
      ['uplyw_czasu', 'gotowka_max', 'Sufit gotówki kupca (× gotówka startowa)'],
    ] as [sek, pole, nazwa]}
      <tr><td>{nazwa}</td><td class="num"><input class="w-tabeli" value={pl(d.rynek[sek][pole])}
        onchange={e => liczba(e.currentTarget.value, m => ustaw(x => { x.rynek[sek] = { ...(x.rynek[sek] || {}), [pole]: m }; }))} /></td></tr>
    {/each}
    <tr><td>Kaprys: granice (najniżej, najwyżej)</td><td class="num">
      <input class="w-tabeli" value={pl(d.rynek.kaprys.granice[0])} onchange={e => liczba(e.currentTarget.value, m => ustaw(x => { x.rynek.kaprys = { ...(x.rynek.kaprys || {}), granice: [m, d.rynek.kaprys.granice[1]] }; }))} />
      <input class="w-tabeli" value={pl(d.rynek.kaprys.granice[1])} onchange={e => liczba(e.currentTarget.value, m => ustaw(x => { x.rynek.kaprys = { ...(x.rynek.kaprys || {}), granice: [d.rynek.kaprys.granice[0], m] }; }))} /></td></tr>
    <tr><td>Sprzedaż / tydz. przy popycie niskim, normalnym, wysokim</td><td class="num">
      {#each [0, 1, 2] as i}<input class="w-tabeli" value={pl(d.rynek.uplyw_czasu.sprzedaz[i])} onchange={e => liczba(e.currentTarget.value, m => ustaw(x => {
        const s = [...d.rynek.uplyw_czasu.sprzedaz]; s[i] = m; x.rynek.uplyw_czasu = { ...(x.rynek.uplyw_czasu || {}), sprzedaz: s }; }))} />{/each}</td></tr>
  </tbody></table></div>
  <div class="przyciski"><button class="maly" onclick={() => ustaw(x => { x.rynek = {}; })}>Przywróć rynek</button></div>
</details>

<details class="sekcja" open={zmiany.length > 0 && zmiany.length < 40}>
  <summary><span>Zmienione ceny względem cennika domyślnego</span><span class="szary male">{zmiany.length}</span></summary>
  <div class="tabela karty"><table class="karty">
    <thead><tr><th>Pozycja</th><th class="num">Było</th><th class="num">Jest</th><th class="num">Zmiana</th></tr></thead>
    <tbody>{#each zmiany as z}<tr><td class="tytul">{z.nazwa}</td><td class="num" data-l="Było">{mon(z.przed_p)}</td>
      <td class="num" data-l="Jest"><span class="cena">{mon(z.po_p)}</span></td>
      <td class="num" data-l="Zmiana" class:plus={z.po_p > z.przed_p} class:minus={z.po_p < z.przed_p}>{mnoz(z.po_p / z.przed_p)}</td></tr>
    {:else}<tr><td class="pelna szary">Brak zmian.</td></tr>{/each}</tbody></table></div>
</details>

<details class="sekcja">
  <summary><span>Ustawienia jako JSON, eksport, import</span></summary>
  <div class="panel" style="border-top:0;border-radius:0 0 var(--r) var(--r)">
    <textarea bind:value={json} spellcheck="false" style="min-height:220px;font-family:ui-monospace,Consolas,monospace;font-size:.85rem"></textarea>
    <div class="przyciski">
      <button onclick={zastosujJson}>Zastosuj JSON</button>
      <button class="glowny" onclick={() => pobierzPlik('ustawienia.json', { opis: `Ustawienia MG ze Skarbca, ${dzis()}. Format: data/ustawienia.json.`, ...$state.snapshot(stan.ust) })}>Eksportuj plik</button>
      <label class="chip" style="display:inline-flex;align-items:center;min-height:44px">Importuj plik<input type="file" accept=".json,application/json" hidden onchange={importuj} /></label>
      <button class="niebezp" onclick={() => { stan.przywrocUst(); msg = 'Przywrócono cennik domyślny.'; zly = false; }}>Przywróć domyślne</button>
    </div>
  </div>
</details>
