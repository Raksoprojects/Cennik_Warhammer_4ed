<script lang="ts">
  import { stan } from '../lib/stan.svelte';
  import { mon, mnoz, parsujCene, parsujMnoznik, pobierzPlik, norm } from '../lib/format';
  import { etykietaKoniunktury } from '../silnik.js';
  import WyborOsady from '../komponenty/WyborOsady.svelte';
  import WyborRynku from '../komponenty/WyborRynku.svelte';
  import DataKampanii from '../komponenty/DataKampanii.svelte';
  import NaZamowienie from '../komponenty/NaZamowienie.svelte';
  import { cenaTypowa } from '../lib/ceny';
  import * as T from '../kupcy_trwali.js';
  import TabelaTowaru from '../komponenty/TabelaTowaru.svelte';
  import Podpowiedz from '../komponenty/Podpowiedz.svelte';
  import Potwierdz from '../komponenty/Potwierdz.svelte';
  import PostacKupca from '../komponenty/PostacKupca.svelte';
  import WyborCech from '../komponenty/WyborCech.svelte';

  let { uid }: { uid: string } = $props();
  const d = $derived(stan.d);
  const K = $derived(stan.kupiec(uid));
  const W = $derived(T.wycen(d, K));
  let ps = $state(0), talent = $state(0), tygodnie = $state(1), msg = $state(''), zly = $state(false);
  let decyzja = $state<{ tytul: string; tekst: string; tak: () => void } | null>(null);
  const grupy = $derived([...new Set(stan.kupcy.map(x => x.grupa).filter(Boolean))]);
  const towaryCennika = $derived(d.cennik.pozycje.filter((c: any) => c.typ === 'towar'));
  const poNazwie = (txt: string) => { const n = norm(txt.trim()); return towaryCennika.find((c: any) => norm(c.nazwa) === n)
    ?? towaryCennika.filter((c: any) => norm(c.nazwa).includes(n)).sort((a: any, b: any) => a.nazwa.length - b.nazwa.length)[0]; };

  function zapisz(nowy: any, komunikat = '') {
    if (nowy?.blad) { msg = nowy.powod; zly = true; return false; }
    stan.zapiszKupca(nowy); msg = komunikat; zly = false; return true;
  }
  const pole = (klucz: string, v: any) => zapisz({ ...$state.snapshot(K), [klucz]: v });
  // Operacja, która może wymagać decyzji MG: najpierw bez wymuszenia, potem okno „czy chcesz kontynuować?”.
  function zDecyzja(tytul: string, op: (wymus: boolean) => any, komunikat: string) {
    const r = op(false);
    if (r?.blad === 'poza_asortymentem' || r?.blad === 'odmowa' || r?.blad === 'brak_gotowki')
      decyzja = { tytul, tekst: `Niedostępne u tego kupca: ${r.powod}. Czy chcesz kontynuować?`, tak: () => { decyzja = null; zapisz(op(true), komunikat); } };
    else zapisz(r, komunikat);
  }

  // ---- modyfikator MG
  let modTxt = $state('');
  function ustawMod(m: number | null) {
    if (m == null || Number.isNaN(m) || m <= 0) { msg = 'Wpisz mnożnik, np. 0,9 albo −10%.'; zly = true; return; }
    pole('modyfikator', m); modTxt = '';
  }
  // ---- dodawanie i skup spoza sklepu
  let dodajTxt = $state(''), dodajIle = $state(''), dogenKat = $state(''), dogenIle = $state(2);
  function dodaj() {
    const c = poNazwie(dodajTxt); if (!c) { msg = 'Nie ma takiego towaru w cenniku.'; zly = true; return; }
    const sztuk = dodajIle ? Math.max(1, +dodajIle | 0) : undefined;
    zDecyzja('Towar spoza asortymentu', w => T.dodajPozycje(d, $state.snapshot(K), c.id, { sztuk, wymus: w }), `Dodano: ${c.nazwa}.`);
    dodajTxt = ''; dodajIle = '';
  }
  let skupTxt = $state(''), skupIle = $state(1), skupCena = $state('');
  const skupPoz = $derived(skupTxt ? poNazwie(skupTxt) : null);
  const skupSugestia = $derived(skupPoz ? Math.round(cenaTypowa(d, W.kupiec, W.osada, W.koniunktura, skupPoz) * W.kupiec.skup * (K.modyfikator ?? 1)) : 0);
  function skup() {
    if (!skupPoz) { msg = 'Nie ma takiego towaru w cenniku.'; zly = true; return; }
    const cena = parsujCene(skupCena) ?? skupSugestia;
    if (Number.isNaN(cena)) return;
    zDecyzja('Brak gotówki', w => T.transakcja(d, $state.snapshot(K), { id: skupPoz.id, typ: 'sprzedaz', ilosc: Math.max(1, skupIle | 0), cena_p: cena, wymus: w }),
      `Kupiec odkupił: ${skupPoz.nazwa}.`);
    skupTxt = skupCena = ''; skupIle = 1;
  }
  // ---- zamówienia
  let zamMat = $state(false);
  let zamTxt = $state(''), zamJak = $state<Record<string, number>>({}), zamDla = $state(''), zamCena = $state('');
  function zamow() {
    const c = poNazwie(zamTxt); if (!c) { msg = 'Nie ma takiego towaru w cenniku.'; zly = true; return; }
    const cena = parsujCene(zamCena);
    zDecyzja('Kupiec tego nie robi', w => T.zamow(d, $state.snapshot(K), { id: c.id, jakosc: zamJak, dla: zamDla.trim(), wymus: w, material: zamMat, cena_p: Number.isNaN(cena) ? null : cena }),
      `Zamówiono: ${c.nazwa}.`);
    zamTxt = zamDla = zamCena = ''; zamJak = {};
  }
  const STATUS: Record<string, string> = { w_toku: 'w toku', gotowe: 'gotowe do odbioru', odebrane: 'odebrane', anulowane: 'anulowane' };
  let notatkaWpis = $state('');
  function dopiszDziennik() {
    if (!notatkaWpis.trim()) return;
    const k = $state.snapshot(K); k.dziennik.push({ tydzien: k.tydzien, tekst: notatkaWpis.trim() }); zapisz(k); notatkaWpis = '';
  }
  function kopia() {
    const k = { ...$state.snapshot(K), uid: T.nowyUid(), nazwa: K.nazwa + ' (kopia)' };
    stan.zapiszKupca(k); stan.idz('#kupcy/' + k.uid);
  }
</script>

{#if decyzja}<Potwierdz tytul={decyzja.tytul} tekst={decyzja.tekst} onTak={decyzja.tak} onNie={() => (decyzja = null)} />{/if}

<p class="nie-drukuj"><a href="#kupcy">← Moi kupcy</a></p>
<div class="panel">
  <div class="pasek">
    <label class="pole"><span>Nazwa</span><input value={K.nazwa} onchange={e => pole('nazwa', e.currentTarget.value.trim() || K.imie)} /></label>
    <label class="pole"><span>Grupa</span><input value={K.grupa} list="grupy-karta" onchange={e => pole('grupa', e.currentTarget.value.trim())} />
      <datalist id="grupy-karta">{#each grupy as g}<option value={g}></option>{/each}</datalist></label>
  </div>
  <p class="drugi">{W.kupiec.nazwa}, {W.kupiec.status}. {W.kupiec.opis} <i>{K.dziwactwo}</i></p>
  {#if K.postac}<PostacKupca postac={K.postac} onPrzelosuj={() => zapisz(T.przelosujPostac(d, $state.snapshot(K)), 'Nowa osobowość.')} />
  {:else}<button class="maly nie-drukuj" onclick={() => zapisz(T.przelosujPostac(d, $state.snapshot(K)), 'Dodano osobowość.')}>Dodaj osobowość</button>{/if}
  <label class="pole"><span>Notatka</span><textarea value={K.notatka} placeholder="Kim jest, co wie, jak traktuje drużynę…"
    onchange={e => pole('notatka', e.currentTarget.value)}></textarea></label>
  <div class="liczby" style="margin-top:10px">
    <div><span>Gotówka</span><b class="cena">{mon(K.gotowka_p)}</b></div>
    <div><span>Wartość towaru</span><b>{mon(W.wartosc_towaru_p)}</b></div>
    <div><span>Tydzień kampanii</span><b>{K.tydzien}</b></div>
    <div><span>Modyfikator MG</span><b>{mnoz(K.modyfikator ?? 1)}</b></div>
  </div>
</div>

{#if msg}<div class="komunikat" class:zly>{msg}</div>{/if}

<div class="siatka nie-drukuj">
  <div class="panel">
    <h3>Gdzie i kiedy</h3>
    <label class="pole"><span>Osada</span><WyborOsady value={K.osada} onchange={v => zapisz(T.przenies(d, $state.snapshot(K), { osada: v }), 'Ceny przeliczone dla nowej osady.')} /></label>
    <div class="pasek" style="margin-top:8px"><WyborRynku pora={K.pora ?? null} wahania={K.wahania ?? null} poraZDaty={!!K.data}
      onchange={z => zapisz(T.przenies(d, $state.snapshot(K), z), 'Ceny przeliczone.')} /></div>
    <DataKampanii data={K.data ?? null} onUstaw={dt => zapisz(T.przenies(d, $state.snapshot(K), { data: dt }), dt ? 'Data ustawiona, pora roku z kalendarza.' : 'Bez daty.')} />
    <label class="pole" style="margin-top:8px"><span>Sytuacja</span><select value={K.koniunktura} onchange={e => zapisz(T.przenies(d, $state.snapshot(K), { koniunktura: e.currentTarget.value }), 'Ceny przeliczone dla nowej sytuacji.')}>
      {#each d.koniunktura.koniunktury as k}<option value={k.id}>{etykietaKoniunktury(d, k, { krotko: true })}</option>{/each}</select></label>
    <p class="male drugi" style="margin-top:6px">{W.etykiety.koniunktura}</p>
    <div class="pasek">
      <label class="pole waskie"><span>Minęło tygodni <Podpowiedz tekst={`Co tydzień kupiec sprzedaje część towaru (popyt niski / normalny / wysoki: ${d.rynek.uplyw_czasu.sprzedaz.map((x: number) => Math.round(x * 100) + '%').join(' / ')}), uzupełnia rdzeń za koszt nabycia, czasem bierze nowy towar. Co ${d.rynek.uplyw_czasu.rynek_co} tygodnie zmienia się popyt i kaprys. Zamówienia z minionym terminem są gotowe. Parametry: Edycja cen → Rynek.`} /></span>
        <input type="number" min="1" max="52" bind:value={tygodnie} /></label>
      <button class="glowny" onclick={() => zapisz(T.uplywCzasu(d, $state.snapshot(K), Math.max(1, tygodnie | 0)))}>Minął czas</button>
    </div>
  </div>

  <div class="panel">
    <h3>Ceny tego kupca</h3>
    <p class="male drugi">Twój mnożnik na wszystkie jego ceny i zamówienia: taniej dla przyjaciół, drożej dla wrogów.</p>
    <div class="chipy">
      {#each [0.8, 0.9, 0.95, 1, 1.05, 1.1, 1.25] as m}
        <button class="chip" aria-pressed={(K.modyfikator ?? 1) === m} onclick={() => ustawMod(m)}>{m === 1 ? 'bez zmian' : (m > 1 ? '+' : '−') + Math.round(Math.abs(m - 1) * 100) + '%'}</button>
      {/each}
    </div>
    <div class="pasek">
      <label class="pole waskie"><span>Własny</span><input bind:value={modTxt} placeholder="0,85 albo +15%" /></label>
      <button onclick={() => ustawMod(parsujMnoznik(modTxt))}>Ustaw</button>
    </div>
    <div class="pasek">
      <label class="pole waskie"><span>Gotówka</span><input placeholder={mon(K.gotowka_p)} onchange={e => { const p = parsujCene(e.currentTarget.value); if (p != null && !Number.isNaN(p)) pole('gotowka_p', p); e.currentTarget.value = ''; }} /></label>
      <label class="pole waskie"><span>PS z Targowania</span><input type="number" min="0" max="10" bind:value={ps} /></label>
      <label class="pole waskie"><span>Talent, −%</span><input type="number" min="0" max="30" bind:value={() => Math.round(talent * 100), v => (talent = Math.max(0, +v || 0) / 100)} /></label>
    </div>
  </div>

  <div class="panel">
    <h3>Towar</h3>
    <datalist id="towary-cennika">{#each towaryCennika as c}<option value={c.nazwa} label={c.dostepnosc ?? ''}></option>{/each}</datalist>
    <div class="pasek">
      <label class="pole"><span>Dodaj z cennika</span><input bind:value={dodajTxt} list="towary-cennika" placeholder="np. kolczuga" /></label>
      <label class="pole waskie"><span>Sztuk</span><input bind:value={dodajIle} type="number" min="1" placeholder="norma" /></label>
      <button onclick={dodaj}>Dodaj</button>
    </div>
    <div class="pasek">
      <label class="pole"><span>Dogeneruj z kategorii</span><select bind:value={dogenKat}>
        <option value="">cały asortyment</option>{#each [...W.kupiec.rdzen, ...W.kupiec.boczne] as k}<option>{k}</option>{/each}</select></label>
      <label class="pole waskie"><span>Ile</span><input type="number" min="1" max="10" bind:value={dogenIle} /></label>
      <button onclick={() => zapisz(T.dogeneruj(d, $state.snapshot(K), { kat: dogenKat || null, ile: Math.max(1, dogenIle | 0) }))}>Dogeneruj</button>
    </div>
    <div class="przyciski">
      <button onclick={() => (decyzja = { tytul: 'Nowy asortyment', tekst: 'Cały towar zostanie wylosowany od nowa. Imię, gotówka, notatki i zamówienia zostają. Kontynuować?', tak: () => { decyzja = null; zapisz(T.przelosujWszystko(d, $state.snapshot(K)), 'Nowy asortyment.'); } })}>Przelosuj wszystko</button>
    </div>
  </div>

  <div class="panel">
    <h3>Drużyna sprzedaje coś, czego kupiec nie ma</h3>
    <div class="pasek">
      <label class="pole"><span>Co</span><input bind:value={skupTxt} list="towary-cennika" placeholder="np. miecz" /></label>
      <label class="pole waskie"><span>Ile</span><input type="number" min="1" bind:value={skupIle} /></label>
      <label class="pole waskie"><span>Za sztukę</span><input bind:value={skupCena} placeholder={skupSugestia ? mon(skupSugestia) : 'cena'} /></label>
      <button onclick={skup}>Sprzedaj</button>
    </div>
    {#if skupPoz}<p class="male drugi">Podpowiedź: typowa cena u niego × skup {Math.round(W.kupiec.skup * 100)}% = {mon(skupSugestia)}.</p>{/if}
  </div>
</div>

<h3 style="margin-top:6px">Na stanie <span class="szary male">{W.towar.length} pozycji</span>
  <button class="maly nie-drukuj" onclick={() => print()}>Drukuj</button></h3>
<p class="male drugi nie-drukuj">Kliknij wiersz: rozbicie ceny, ilość, cena ręczna, przelosowanie, kupno i sprzedaż.</p>
<TabelaTowaru towar={W.towar} {ps} {talent} bezTargu={!!K.postac?.cecha?.efekt?.bez_targu} gotowka={K.gotowka_p} edycja
  onZmien={(id, z) => zapisz(T.zmienPozycje($state.snapshot(K), id, z))}
  onUsun={id => zapisz(T.usunPozycje($state.snapshot(K), id))}
  onPrzelosuj={id => zapisz(T.przelosujPozycje(d, $state.snapshot(K), id))}
  onTransakcja={(id, typ, ilosc, cena_p) => zDecyzja('Brak gotówki', w => T.transakcja(d, $state.snapshot(K), { id, typ, ilosc, cena_p, wymus: w }), typ === 'kupno' ? 'Sprzedane drużynie.' : 'Odkupione od drużyny.')} />
<NaZamowienie kupiec={K.kupiec} osada={K.osada} koniunktura={K.koniunktura} pora={K.pora ?? null} wahania={K.wahania ?? null}
  naStanie={W.towar.filter((t: any) => t.sztuk > 0).map((t: any) => t.id)} />

<div class="siatka" style="margin-top:14px">
  <div class="panel">
    <h3>Zamówienia</h3>
    <div class="pasek nie-drukuj">
      <label class="pole"><span>Co</span><input bind:value={zamTxt} list="towary-cennika" placeholder="np. rapier" /></label>
      <label class="pole waskie"><span>Dla kogo</span><input bind:value={zamDla} placeholder="postać" /></label>
      <label class="pole waskie"><span>Cena <Podpowiedz tekst="Puste = cena z wyliczenia (jak w zakładce Zamówienie, z Twoim modyfikatorem). Wpisz, jeśli umówiliście się inaczej." /></span><input bind:value={zamCena} placeholder="auto" /></label>
      <button onclick={zamow}>Zamów</button>
    </div>
    <label class="male nie-drukuj" style="display:flex;gap:6px;align-items:center"><input type="checkbox" bind:checked={zamMat} />
      Materiał zamawiającego (płaci {Math.round(d.rynek.zamowienie.material_wlasny * 100)}% — tylko gdy kupiec robi sam)</label>
    <details class="opis nie-drukuj"><summary>Jakość zamówienia (Zalety i Wady przedmiotu)</summary><WyborCech bind:cechy={zamJak} /></details>
    {#each [...K.zamowienia].reverse() as z (z.uid)}
      <div style="border-top:1px solid var(--linia);padding:8px 0">
        <b>{z.nazwa}</b> <span class="drugi male">{z.jakosc}{z.dla ? ', dla ' + z.dla : ''}</span>
        <span class="znacznik" class:zielony={z.status === 'gotowe'} class:niebieski={z.status === 'w_toku'}>{STATUS[z.status]}</span>
        {#if z.wymuszone}<span class="znacznik fiolet">decyzja MG</span>{/if}
        <div class="male">{mon(z.cena_p)} · zaliczka {mon(z.zaliczka_p)} · złożone w tyg. {z.tydzien_zlozenia}, gotowe w tyg. {z.tydzien_gotowe}
          ({z.sposob === 'wykonuje' ? 'robi sam' : 'sprowadza'})</div>
        {#if z.status === 'w_toku' || z.status === 'gotowe'}
          <div class="przyciski nie-drukuj" style="margin-top:6px">
            <button class="maly glowny" onclick={() => zapisz(T.odbierzZamowienie($state.snapshot(K), z.uid), 'Odebrane.')}>Odbierz (dopłata {mon(z.cena_p - z.zaliczka_p)})</button>
            <button class="maly" onclick={() => zapisz(T.anulujZamowienie($state.snapshot(K), z.uid), 'Anulowane, zaliczka przepada.')}>Anuluj</button>
            <button class="maly" onclick={() => zapisz(T.anulujZamowienie($state.snapshot(K), z.uid, { zwrotZaliczki: true }), 'Anulowane, zaliczka zwrócona.')}>Anuluj ze zwrotem</button>
          </div>
        {/if}
      </div>
    {:else}<p class="szary male">Brak zamówień.</p>{/each}
  </div>

  <div class="panel">
    <h3>Dziennik</h3>
    <div class="pasek nie-drukuj">
      <label class="pole"><span>Wpis</span><input bind:value={notatkaWpis} placeholder="np. pokłócił się z Ulrykiem" onkeydown={e => e.key === 'Enter' && dopiszDziennik()} /></label>
      <button onclick={dopiszDziennik}>Dopisz</button>
    </div>
    <ul class="dziennik">{#each [...K.dziennik].reverse() as w}<li><span class="szary">tydz. {w.tydzien}:</span> {w.tekst}</li>{/each}</ul>
  </div>
</div>

<div class="przyciski nie-drukuj" style="margin-top:14px">
  <button onclick={() => pobierzPlik(`kupiec-${norm(K.nazwa).replace(/[^a-z0-9]+/g, '-')}.json`, $state.snapshot(K))}>Eksport do pliku</button>
  <button onclick={kopia}>Kopia kupca</button>
  <button class="niebezp" onclick={() => (decyzja = { tytul: 'Usuń kupca', tekst: `Usunąć „${K.nazwa}” z bazy? Tego nie da się cofnąć (chyba że masz eksport).`, tak: () => { decyzja = null; stan.usunKupca(uid); stan.idz('#kupcy'); } })}>Usuń kupca</button>
</div>
<p class="male szary">Zapisany {K.utworzony}, zmieniony {K.zmieniony}. Seed {K.seed}.</p>
