<script lang="ts">
  import { stan } from '../lib/stan.svelte';
  import { mon, mnoz, norm, proc } from '../lib/format';
  import { etykietaKoniunktury, podrozKupiecka } from '../silnik.js';

  const d = $derived(stan.d);
  let pod = $state('modyfikatory'), q = $state(''), filtr = $state('');
  const POD = [['modyfikatory', 'Jak liczona jest cena'], ['zasady', 'Zasady domowe'], ['handel', 'Handel (Poradnik)'], ['podroz', 'Podróż kupiecka'],
    ['audyt', 'Audyt profesji'], ['historia', 'Źródła historyczne']];
  // Podróż kupiecka (Poradnik s. 39–40)
  let km = $state(200), teren = $state<'lad' | 'woda'>('lad'), poraPodr = $state(''), slaby = $state(false), zdarzenia = $state<any[] | null>(null);
  const H = $derived(d.handel);
  const NAZWA_ST = $derived(H.stopnie_nazwy);
  const WERDYKT: Record<string, string> = { ok: 'bez zmian', dochod: 'inny Dochód', ryzyko: 'dochód ryzykowny', zmiana: 'zmiana Statusu' };
  const audyt = $derived(d.audyt.flatMap((p: any) => p.poziomy.map((l: any) => ({ ...l, klasa: p.klasa, profesja: p.profesja })))
    .filter((l: any) => (!filtr || l.w === filtr) && (!q || norm(`${l.klasa} ${l.profesja} ${l.nazwa}`).includes(norm(q)))));
  const historia = $derived(d.historia.filter((h: any) => (!filtr || h.kat === filtr) && (!q || norm(`${h.poz} ${h.zrodlo} ${h.orig}`).includes(norm(q)))));
  const histKat = $derived([...new Set(d.historia.map((h: any) => h.kat))] as string[]);
  function zmien(p: string) { pod = p; q = ''; filtr = ''; }
  const pl1 = (x: number) => String(x).replace('.', ',');
</script>

<h2>Zasady i tabele</h2>
<div class="podzakladki">{#each POD as [id, n]}<button class="chip" aria-pressed={pod === id} onclick={() => zmien(id)}>{n}</button>{/each}</div>

{#if pod === 'modyfikatory'}
  <div class="komunikat mono male">cena u kupca = cena bazowa × marża × preferencja × kaprys × osada × sytuacja[kategoria] × rynek[zapas][popyt] × modyfikator MG kupca<br />
    cena minimalna = koszt nabycia × {pl1(d.rynek.cena_minimalna.narzut_min)} (przy wyprzedaży × {pl1(d.rynek.cena_minimalna.wyprzedaz)}) · koszt nabycia = cena bazowa × osada × sytuacja (wytwórca: × {pl1(d.rynek.cena_minimalna.koszt_wlasny)})</div>
  <details class="sekcja" open><summary><span>1. Marża i asortyment kupców</span></summary>
    <div class="tabela karty"><table class="karty"><thead><tr><th>Kupiec</th><th>Status</th><th class="num">Marża</th><th class="num">Limit</th><th class="num">Skup</th><th>Rdzeń</th><th>Robi sam</th></tr></thead>
      <tbody>{#each d.kupcy.kupcy as k}<tr><td class="tytul">{k.nazwa}</td><td data-l="Status">{k.status}</td><td class="num" data-l="Marża">{mnoz(k.marza)}</td>
        <td class="num" data-l="Limit">{mon(k.limit_p)}</td><td class="num" data-l="Skup">{Math.round(k.skup * 100)}%</td>
        <td class="pelna male">{k.rdzen.join(', ')}<span class="szary"> · boczne: {k.boczne.join(', ')}</span></td><td class="pelna male drugi">{[...k.robota, ...(k.robota_pozycje ?? []).map((i: string) => d.cennik.pozycje.find((c: any) => c.id === i)?.nazwa ?? i)].join(', ') || '—'}
          {#if k.jakosc}<br /><span class="szary">jakość: Zalety {Math.round((k.jakosc.zalety ?? 0) * 100)}%, Wady {Math.round((k.jakosc.wady ?? 0) * 100)}% pozycji</span>{/if}</td></tr>{/each}</tbody></table></div></details>
  <details class="sekcja"><summary><span>2. Osady</span></summary>
    <div class="tabela karty"><table class="karty"><thead><tr><th>Osada</th><th class="num">Mnożnik</th><th class="num">Limit towaru</th><th>Uwagi</th></tr></thead>
      <tbody>{#each d.osady.osady.filter((o: any) => !o.grupa) as o}<tr><td class="tytul">{o.nazwa}</td><td class="num" data-l="Mnożnik">{proc(o.mnoznik)}</td>
        <td class="num" data-l="Limit">{o.limit_p == null ? 'bez limitu' : mon(o.limit_p)}</td><td class="pelna male drugi">{o.uwaga ?? ''}</td></tr>{/each}</tbody></table></div></details>
  <details class="sekcja"><summary><span>3. Sytuacje</span></summary>
    <div class="tabela karty"><table class="karty"><thead><tr><th>Sytuacja</th><th>Ceny i czynsz</th><th>Popyt</th></tr></thead>
      <tbody>{#each d.koniunktura.koniunktury as k}<tr><td class="tytul">{k.nazwa}</td><td class="pelna male">{etykietaKoniunktury(d, k).replace(k.nazwa + ' ', '')}</td>
        <td class="pelna male drugi">{k.opis_popytu ?? ''}</td></tr>{/each}</tbody></table></div></details>
  <details class="sekcja"><summary><span>4. Osobowość kupca: preferencja i kaprys</span></summary>
    <div class="panel"><p>Rdzeń asortymentu {mnoz(d.rynek.preferencje.rdzen)}, boczny {mnoz(d.rynek.preferencje.boczne)}. Kaprys 1k10 na pozycję:</p>
      <ul>{#each d.rynek.kaprys.progi as p, i}<li>{i ? d.rynek.kaprys.progi[i - 1].do + 1 : 1}–{p.do}: {mnoz(p.mnoznik)} — {p.opis}</li>{/each}</ul>
      <p>Preferencja × kaprys mieści się w {mnoz(d.rynek.kaprys.granice[0])} … {mnoz(d.rynek.kaprys.granice[1])}.</p></div></details>
  <details class="sekcja"><summary><span>5. Rynek: zapas × popyt</span></summary>
    <div class="tabela"><table><thead><tr><th>Zapas \ popyt</th>{#each d.rynek.popyt.nazwy as n}<th class="num">{n}</th>{/each}</tr></thead>
      <tbody>{#each d.rynek.macierz_zapas_x_popyt.wartosci as w, i}<tr><td>{d.rynek.zapas.progi[i].nazwa} <span class="szary male">(1k10 ≤ {d.rynek.zapas.progi[i].do})</span></td>
        {#each w as m}<td class="num" class:plus={m > 1} class:minus={m < 1}>{mnoz(m)}</td>{/each}</tr>{/each}</tbody></table></div>
    <p class="male drugi" style="margin-top:8px">Ostatnie sztuki czegoś, czego nikt nie chce, to zaległy towar — kupiec odda go taniej.
      Ostatnie sztuki czegoś, po co stoi kolejka, to jego najlepszy dzień w miesiącu.</p></details>
{:else if pod === 'zasady'}
  <div class="siatka">
    <div class="panel"><h3>1. Pozycja i Dochód to dwie liczby</h3><p>Pozycja rządzi tym, kto z tobą rozmawia i gdzie cię wpuszczą. Dochód rządzi sakiewką.</p>
      <ul class="male">{#each d.pozycja_dochod.przyklady as p}<li>{p.kto}: Pozycja {p.pozycja} / Dochód {p.dochod}{p.uwaga ? ` (${p.uwaga})` : ''}</li>{/each}</ul></div>
    <div class="panel"><h3>2. Utrzymanie płacisz w mieście</h3><p>80% brutto to opłata za bycie kimś w danym miejscu: czynsz, czeladź, strój, składka cechowa.
      Naliczaj je tylko za tygodnie w osadzie. W trasie postać płaci realne ceny z cennika.</p></div>
    <div class="panel"><h3>3. Jakość (PG s. 292, HR-024)</h3><p>Cena w cenniku to wariant podstawowy; cechy broni są w niej wliczone.
      Każda Zaleta przedmiotu ×{d.rynek.jakosc.za_zalete}, każda Wada ×{String(d.rynek.jakosc.za_wade).replace('.', ',')}.
      Wyśmienity i Wytrzymały można brać kilka razy — każdy poziom to osobna Zaleta: miecz Wytrzymały 2, Wyśmienity 2 kosztuje
      ×{String(+(d.rynek.jakosc.za_zalete ** 4).toFixed(2)).replace('.', ',')}.</p>
      <ul class="male">{#each d.rynek.jakosc.zalety as z}<li><b>{z.nazwa}</b>{z.wielokrotna ? ' (wielokrotna)' : ''}: {z.opis}</li>{/each}
        {#each d.rynek.jakosc.wady as z}<li><b>{z.nazwa}</b> (Wada): {z.opis}</li>{/each}</ul></div>
    <div class="panel"><h3>4. Dochód ryzykowny dla Łotrów</h3><p>Rzuć jak za Status o dwa szczeble wyżej (Brąz 5 → Srebro 2), potem Test
      Kradzieży, Zastraszania, Hazardu albo Oszustwa. Porażka — połowa i ktoś cię szuka. Porażka z dubletem — zero i oskarżenie.</p></div>
    <div class="panel"><h3>5. Jałmużna zamiast martwego Brązu 0</h3><p>Test Charyzmy albo Plotkowania: za każde 2 PS 1k10 pensów, podwojone w święto i podczas zarazy.</p></div>
    <div class="panel"><h3>6. Figury państwowe</h3><p>Elektorowie, Wielki Teogonista, Patriarchowie bogatych Kolegiów, Cesarz: dochód ×10 i bez rzutu.</p></div>
    <div class="panel"><h3>7. Targowanie</h3><p>Przeciwstawny Test Targowania. Każdy PS gracza −{Math.round(d.rynek.targowanie.za_ps * 100)}%, najwyżej
      −{Math.round(d.rynek.targowanie.max * 100)}% (zamówienia −{Math.round(d.rynek.targowanie.max_zamowienie * 100)}%). Pełen skład: +10 dla gracza.
      Ostatnie sztuki przy wysokim popycie: −20. Dolna granica to cena minimalna kupca.</p></div>
    <div class="panel"><h3>8. Co nie jest towarem</h3><p>Nocleg, posiłek w gospodzie, stajnia, praca najmitów i czynsze mają ceny już detaliczne.
      Nie ma ich w sklepach, nie da się ich odkupić i nie przechodzą przez marżę. W cenniku: „nie w handlu”.</p></div>
    <div class="panel"><h3>9. Ceny w cenniku to ceny wytwórcy</h3><p>Kupiec dolicza marżę. Gracz nigdy nie płaci ceny z cennika wprost.
      Kotwica: robotnik niewykwalifikowany (Brąz 3) zarabia {mon(d.statusy.robotnik_brutto_p)} brutto tygodniowo.</p></div>
  </div>
{:else if pod === 'handel'}
  <p class="drugi">{H.opis}</p>
  <details class="sekcja" open><summary><span>Pora roku i wahania rynku</span></summary>
    <div class="panel"><p class="male">{H.pory_roku.opis}</p>
      <ul class="male">{#each H.pory_roku.lista as p}<li><b>{p.nazwa}</b>: ceny {mnoz(p.ceny)}{#each Object.entries(p.kategorie) as [k, v]} · {k} {mnoz((v as any).cena)}{(v as any).popyt ? ', popyt +' + (v as any).popyt : ''}{/each} · zagrożenia w podróży +{p.zagrozenia} — {p.uwaga}</li>{/each}</ul>
      <p class="male">{H.wahania.opis}</p>
      <ul class="male">{#each H.wahania.lista as w}<li>1k10 {w.od}–{w.do}: <b>{w.nazwa}</b> — ceny {mnoz(w.ceny)}, popyt {w.popyt > 0 ? '+' : ''}{w.popyt}</li>{/each}</ul></div></details>
  <details class="sekcja"><summary><span>Strefy handlowe: co tanie, co drogie</span></summary>
    <p class="male drugi" style="margin:8px 0">Stopnie z Poradnika (s. 41) uśrednione na kategorie Skarbca. Mnożnik ceny: {Object.entries(H.mnozniki_stopni).map(([s, m]) => `${NAZWA_ST[s]} ${mnoz(m as number)}`).join(' · ')}.</p>
    <div class="tabela"><table><thead><tr><th>Strefa</th>{#each H.towary_poradnika as t}<th title={t} style="writing-mode:vertical-rl;font-size:.7rem">{t}</th>{/each}</tr></thead>
      <tbody>{#each H.strefy as s}<tr><td><b>{s.nazwa}</b><div class="male szary">{s.szlak}{s.zagranica ? ' · import: ' + s.zagranica : ''}</div></td>
        {#each s.siatka.split(' ') as l}<td class="num" title={NAZWA_ST[l]} class:plus={['Z', 'R', 'S'].includes(l)} class:minus={['D', 'Po'].includes(l)}>{l}</td>{/each}</tr>{/each}</tbody></table></div></details>
  <details class="sekcja"><summary><span>Ośrodki handlu Imperium</span><span class="szary male">{H.miasta.length}</span></summary>
    <div class="tabela karty"><table class="karty"><thead><tr><th>Miasto</th><th class="num">Populacja</th><th class="num">Zamożność</th><th>Prowincja</th><th>Strefa</th><th class="num">Ceny</th></tr></thead>
      <tbody>{#each H.miasta as [nazwa, pop, zam, prow, strefa, wolne]}
        {@const o = d.osady.osady.find((x: any) => x.nazwa === nazwa)}
        <tr><td class="tytul">{nazwa}{#if wolne}<span class="znacznik zloty">wolne miasto</span>{/if}</td><td class="num" data-l="Populacja">{pop.toLocaleString('pl')}</td>
          <td class="num" data-l="Zamożność">{zam}</td><td data-l="Prowincja">{prow}</td><td data-l="Strefa">{H.strefy.find((s: any) => s.id === strefa)?.nazwa}</td>
          <td class="num" data-l="Ceny">{o ? proc(o.mnoznik) : '—'}</td></tr>{/each}</tbody></table></div></details>
  <details class="sekcja"><summary><span>Myto, taryfy, opłaty i kary</span></summary>
    <div class="panel"><p class="male drugi">{H.oplaty.opis}</p>
      <ul class="male">{#each H.oplaty.lista as o}<li><span class="szary">{o.grupa}:</span> {o.nazwa} — <b>{o.stawka}</b></li>{/each}</ul>
      <p class="male">{H.oplaty.unikanie}</p></div></details>
  <details class="sekcja"><summary><span>Nielegalne towary i przemyt</span></summary>
    <div class="panel"><p class="male">{H.nielegalne.opis}</p><p class="male">Rodzaje: {H.nielegalne.rodzaje.join(', ')}. {H.nielegalne.uwaga}</p>
      <div class="tabela"><table><thead><tr><th class="num">Zamożność</th><th>Test Plotkowania</th><th class="num">Cena ×</th><th>Dostępność</th></tr></thead>
        <tbody>{#each Object.entries(H.zamoznosc.nielegalne) as [z, v]}<tr><td class="num">{z}</td><td>{(v as any).plotkowanie}</td><td class="num">{mnoz((v as any).cena)}</td><td>{(v as any).dostepnosc}</td></tr>{/each}</tbody></table></div>
      <p class="male drugi" style="margin-top:8px">{H.zamoznosc.nielegalne_opis} W Skarbcu nielegalny towar ma tylko paser i kupiec z cechą „Powiązania przestępcze”.</p></div></details>
  <details class="sekcja"><summary><span>Bogowie kupców</span></summary>
    <div class="siatka" style="padding-top:8px">{#each H.bogowie as b}<div class="panel"><h3>{b.nazwa}</h3><p class="male drugi">{b.domena}. Symbol: {b.symbol}. {b.charakter}.</p>
      <ul class="male">{#each b.przykazania as p}<li>{p}</li>{/each}</ul><p class="male">{b.swiatynie} Kult: {b.kult}. Święto: {b.swieto}.</p></div>{/each}</div></details>
  <details class="sekcja"><summary><span>Zasady dodatkowe: spekulacje, lichwa, gildia…</span></summary>
    <div class="siatka" style="padding-top:8px">{#each H.zasady_dodatkowe as z}<div class="panel"><h3>{z.nazwa}</h3><p class="male">{z.tekst}</p></div>{/each}</div></details>
{:else if pod === 'podroz'}
  <p class="drugi">{H.zagrozenia.opis}</p>
  <div class="panel">
    <div class="pasek">
      <label class="pole waskie"><span>Odległość (km)</span><input type="number" min="50" step="50" bind:value={km} /></label>
      <label class="pole"><span>Droga</span><select bind:value={teren}><option value="lad">lądem (karawana)</option><option value="woda">wodą (łódź, statek)</option></select></label>
      <label class="pole"><span>Pora roku</span><select bind:value={poraPodr}><option value="">—</option>{#each H.pory_roku.lista as p}<option value={p.id}>{p.nazwa} (+{p.zagrozenia})</option>{/each}</select></label>
      <label style="display:flex;gap:6px;align-items:center"><input type="checkbox" bind:checked={slaby} /> mało uczęszczany szlak</label>
      <button class="glowny" onclick={() => (zdarzenia = podrozKupiecka(d, { km, teren, pora: poraPodr || null, slaby_szlak: slaby }))}>Losuj podróż</button>
    </div>
    {#if zdarzenia}
      {#each zdarzenia as z}<div style="border-top:1px solid var(--linia);padding:6px 0"><span class="szary">{z.km} km, 1k100 = {z.rzut}:</span> <b>{z.nazwa}</b> — {z.opis}</div>
      {:else}<p class="ok">Spokojna podróż — bez zdarzeń.</p>{/each}
    {/if}
  </div>
  <details class="sekcja"><summary><span>Tabela zagrożeń</span><span class="szary male">{H.zagrozenia.lista.length}</span></summary>
    <div class="tabela karty"><table class="karty"><thead><tr><th class="num">Ląd</th><th class="num">Woda</th><th>Zagrożenie</th></tr></thead>
      <tbody>{#each H.zagrozenia.lista as z}<tr><td class="num" data-l="Ląd">{z.lad ? z.lad.join('–') : '—'}</td><td class="num" data-l="Woda">{z.woda ? z.woda.join('–') : '—'}</td>
        <td class="pelna"><b>{z.nazwa}.</b> {z.opis}</td></tr>{/each}</tbody></table></div></details>
{:else if pod === 'audyt'}
  <p class="drugi">Status zapisuj jako parę Pozycja / Dochód. U większości profesji obie wartości są równe.</p>
  <div class="pasek"><label class="pole"><span>Szukaj</span><input type="search" bind:value={q} placeholder="profesja, poziom…" /></label></div>
  <div class="chipy"><button class="chip" aria-pressed={!filtr} onclick={() => (filtr = '')}>wszystkie</button>
    {#each Object.entries(WERDYKT) as [k, n]}<button class="chip" aria-pressed={filtr === k} onclick={() => (filtr = k)}>{n}</button>{/each}</div>
  <div class="tabela karty"><table class="karty">
    <thead><tr><th>Poziom</th><th>Profesja</th><th>RAW</th><th>Werdykt</th><th>Pozycja</th><th>Dochód</th><th>Uzasadnienie</th></tr></thead>
    <tbody>{#each audyt as l}<tr><td class="tytul">{l.nazwa}</td><td data-l="Profesja">{l.profesja} <span class="szary male">({l.klasa})</span></td>
      <td data-l="RAW">{l.raw}</td><td data-l="Werdykt"><span class="znacznik" class:zielony={l.w === 'ok'} class:zloty={l.w !== 'ok'}>{WERDYKT[l.w] ?? l.w}</span></td>
      <td data-l="Pozycja">{l.poz || l.raw}</td><td data-l="Dochód">{l.doch || l.poz || l.raw}</td><td class="pelna male drugi">{l.powod}</td></tr>{/each}</tbody></table></div>
{:else}
  <div class="pasek"><label class="pole"><span>Szukaj</span><input type="search" bind:value={q} placeholder="pozycja, miasto, rok…" /></label></div>
  <div class="chipy"><button class="chip" aria-pressed={!filtr} onclick={() => (filtr = '')}>wszystkie</button>
    {#each histKat as k}<button class="chip" aria-pressed={filtr === k} onclick={() => (filtr = k)}>{k}</button>{/each}</div>
  <div class="tabela karty"><table class="karty">
    <thead><tr><th>Pozycja</th><th>Oryginalnie</th><th>Źródło</th><th class="num">Dniówek</th><th class="num">Imperium</th></tr></thead>
    <tbody>{#each historia as h}<tr><td class="tytul">{h.poz}</td><td data-l="Oryginalnie">{h.orig}</td><td data-l="Źródło">{h.zrodlo}</td>
      <td class="num" data-l="Dniówek">{h.dniowki == null ? '—' : String(h.dniowki).replace('.', ',')}</td><td class="num" data-l="Imperium"><span class="cena">{h.wfrp}</span></td></tr>{/each}</tbody></table></div>
  <details class="opis" style="margin-top:12px"><summary>Źródła</summary><ul class="male">
    <li><a href="https://historia.org.pl/2025/08/09/ile-kosztowalo-zycie-w-zlotym-wieku-w-krakowie-ceny-i-zarobki-w-xvi-wieku/">Ceny i zarobki w Krakowie w XVI wieku</a> — za J. Pelcem, <i>Ceny w Krakowie 1369–1600</i></li>
    <li><a href="https://medieval.ucdavis.edu/120D/Money.html">Medieval price list — UC Davis</a> (tabela Dyera, żołd, zbroje, czynsze)</li>
    <li><a href="https://bowvsmusket.com/2015/07/01/16th-century-prices-of-weapons/">16th Century Prices of Weapons</a></li>
    <li><a href="https://de.wikipedia.org/wiki/Preise_im_Mittelalter">Preise im Mittelalter</a> — Frankfurt, Kolonia, Norymberga</li>
    <li><a href="https://freepages.rootsweb.com/~stanier/family/N-Money.html">Phelps Brown &amp; Hopkins</a> — płace w Anglii XVI w.</li>
  </ul></details>
{/if}
