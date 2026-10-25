<script lang="ts">
  import { stan } from '../lib/stan.svelte';
  import { mon, mnoz } from '../lib/format';
  import { wycenZamowienie, etykietaOsady, etykietaKoniunktury, modyfikatorKoniunktury } from '../silnik.js';
  import Podpowiedz from '../komponenty/Podpowiedz.svelte';
  import WyborCech from '../komponenty/WyborCech.svelte';
  import WyborOsady from '../komponenty/WyborOsady.svelte';
  import WyborRynku from '../komponenty/WyborRynku.svelte';

  const d = $derived(stan.d);
  let k = $state('kowal'), o = $state('miasteczko'), n = $state('normalna'), co = $state(''), jakosc = $state<Record<string, number>>({});
  let wynik = $state<any>(null);
  const towary = $derived(d.cennik.pozycje.filter((c: any) => c.typ === 'towar'));
  let material = $state(false), pora = $state<string | null>(null), wahania = $state<string | null>(null);
  function wycen() { wynik = co.trim() ? wycenZamowienie(d, { kupiec: k, osada: o, koniunktura: n, przedmiot: co, jakosc, material, pora, wahania }) : null; }
  const kon = $derived(d.koniunktura.koniunktury.find((x: any) => x.id === n));
  const lok = $derived(d.osady.osady.find((x: any) => x.id === o));
</script>

<h2>Zamówienie na miarę</h2>
<p class="drugi">Rzecz robiona albo sprowadzana na zamówienie. Zamówienie u zapisanego kupca (z terminem i zaliczką) złożysz w jego karcie.</p>
<div class="panel">
  <div class="pasek">
    <label class="pole"><span>U kogo</span><select bind:value={k} onchange={wycen}>
      {#each d.kupcy.kupcy as x}<option value={x.id}>{x.nazwa} ({mnoz(x.marza)})</option>{/each}</select></label>
    <label class="pole"><span>Gdzie</span><WyborOsady bind:value={o} onchange={wycen} /></label>
    <label class="pole"><span>Sytuacja</span><select bind:value={n} onchange={wycen}>
      {#each d.koniunktura.koniunktury as x}<option value={x.id}>{etykietaKoniunktury(d, x, { krotko: true })}</option>{/each}</select></label>
  </div>
  <div class="pasek"><WyborRynku bind:pora bind:wahania onchange={() => queueMicrotask(wycen)} /></div>
  <div class="pasek">
    <label class="pole"><span>Co</span><input bind:value={co} list="zam-towary" placeholder="np. kolczuga, rapier, teleskop" onkeydown={e => e.key === 'Enter' && wycen()} />
      <datalist id="zam-towary">{#each towary as c}<option value={c.nazwa}></option>{/each}</datalist></label>
    <button class="glowny" onclick={wycen}>Wyceń</button>
  </div>
  <label class="male" style="display:flex;gap:6px;align-items:center;margin-bottom:8px"><input type="checkbox" bind:checked={material} onchange={wycen} />
    Materiał zamawiającego <Podpowiedz tekst={`Zamawiający daje drewno, żelazo, sukno (np. wieś składa się na wóz). Wytwórca bierze ${Math.round(d.rynek.zamowienie.material_wlasny * 100)}% ceny za robotę. Nie dotyczy rzeczy sprowadzanych.`} /></label>
  <p class="male drugi">Jakość <Podpowiedz tekst={`PG s. 292 i HR-024: cena z cennika to wariant podstawowy. Każda Zaleta przedmiotu ×${String(d.rynek.jakosc.za_zalete).replace('.', ',')} (każdy poziom Wyśmienity i Wytrzymały to osobna Zaleta), każda Wada ×${String(d.rynek.jakosc.za_wade).replace('.', ',')}. Wyroby z Zaletami wymagają Testu Rzemiosła wytwórcy.`} /></p>
  <WyborCech bind:cechy={() => jakosc, c => { jakosc = c; wycen(); }} />
</div>

{#if wynik}
  <div class="panel">
    {#if wynik.status === 'brak_w_cenniku'}
      <p class="blad">Tego nie ma w cenniku albo to nie jest towar (usługi, nocleg i czynsze się nie zamawia).</p>
    {:else if wynik.status === 'odmowa'}
      <h3>{wynik.przedmiot.nazwa}: odmowa</h3>
      <p>{wynik.powod ?? `${d.kupcy.kupcy.find((x: any) => x.id === k).nazwa} tego nie robi ani nie sprowadza.`}
        Odsyła do: <b>{wynik.odsyla_do.join(', ') || '—'}</b>.</p>
    {:else}
      {@const s = wynik.skladowe}
      <h3>{wynik.przedmiot.nazwa} — {wynik.jakosc.nazwa.toLowerCase()}
        <span class="znacznik" class:zielony={wynik.status === 'wykonuje'} class:niebieski={wynik.status === 'sprowadza'}>{wynik.status === 'wykonuje' ? 'robi sam' : 'sprowadza'}</span></h3>
      <div class="liczby">
        <div><span>Cena</span><b class="cena">{mon(wynik.cena_p)}</b></div>
        <div><span>Zaliczka</span><b>{mon(wynik.zaliczka_p)}</b></div>
        <div><span>Termin</span><b>{wynik.termin}</b></div>
        <div><span>Targowanie</span><b>najwyżej −{Math.round(wynik.max_targowanie * 100)}%</b></div>
      </div>
      <p class="male drugi" style="margin-top:10px">
        cena bazowa {mon(wynik.przedmiot.cena_p)} × jakość {mnoz(wynik.jakosc.mnoznik)} × marża {mnoz(s.marza)} ×
        {etykietaOsady(lok)} {mnoz(s.osada)} × {kon.nazwa} ({modyfikatorKoniunktury(kon, wynik.przedmiot.kat)}) {mnoz(s.koniunktura)} ×
        narzut {wynik.status === 'wykonuje' ? 'roboty' : 'sprowadzenia'} {mnoz(s.narzut)}{#if wynik.material} × materiał zamawiającego {mnoz(wynik.material)}{/if}
        = {mnoz(wynik.mnoznik * wynik.jakosc.mnoznik * (wynik.material ?? 1))}</p>
      {#if wynik.rzadkosc}<p class="komunikat male">Tu rzadkość ({wynik.rzadkosc.dostepnosc}, w sprzedaży {Math.round(wynik.rzadkosc.szansa * 100)}%):
        termin + {wynik.rzadkosc.termin_tyg} tyg., narzut {mnoz(wynik.rzadkosc.narzut)} (już w cenie).</p>{/if}
      {#if wynik.calosc_z_gory}<p class="komunikat">Rzecz poza skalą sklepu: kupiec żąda całości z góry.</p>{/if}
      {#if wynik.test_rzemiosla}<p class="male">{d.rynek.zamowienie.zalety}</p>{/if}
    {/if}
  </div>
{/if}
