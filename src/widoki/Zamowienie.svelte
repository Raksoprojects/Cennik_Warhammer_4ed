<script lang="ts">
  import { stan } from '../lib/stan.svelte';
  import { mon, mnoz } from '../lib/format';
  import { wycenZamowienie, etykietaOsady, etykietaKoniunktury, modyfikatorKoniunktury } from '../silnik.js';
  import Podpowiedz from '../komponenty/Podpowiedz.svelte';

  const d = $derived(stan.d);
  let k = $state('kowal'), o = $state('miasteczko'), n = $state('normalna'), co = $state(''), jakosc = $state('zwykla');
  let wynik = $state<any>(null);
  const towary = $derived(d.cennik.pozycje.filter((c: any) => c.typ === 'towar'));
  function wycen() { wynik = co.trim() ? wycenZamowienie(d, { kupiec: k, osada: o, koniunktura: n, przedmiot: co, jakosc }) : null; }
  const kon = $derived(d.koniunktura.koniunktury.find((x: any) => x.id === n));
  const lok = $derived(d.osady.osady.find((x: any) => x.id === o));
</script>

<h2>Zamówienie na miarę</h2>
<p class="drugi">Rzecz robiona albo sprowadzana na zamówienie. Zamówienie u zapisanego kupca (z terminem i zaliczką) złożysz w jego karcie.</p>
<div class="panel">
  <div class="pasek">
    <label class="pole"><span>U kogo</span><select bind:value={k} onchange={wycen}>
      {#each d.kupcy.kupcy as x}<option value={x.id}>{x.nazwa} ({mnoz(x.marza)})</option>{/each}</select></label>
    <label class="pole"><span>Gdzie</span><select bind:value={o} onchange={wycen}>
      {#each d.osady.osady as x}<option value={x.id}>{etykietaOsady(x)}</option>{/each}</select></label>
    <label class="pole"><span>Sytuacja</span><select bind:value={n} onchange={wycen}>
      {#each d.koniunktura.koniunktury as x}<option value={x.id}>{etykietaKoniunktury(d, x, { krotko: true })}</option>{/each}</select></label>
  </div>
  <div class="pasek">
    <label class="pole"><span>Co</span><input bind:value={co} list="zam-towary" placeholder="np. kolczuga, rapier, teleskop" onkeydown={e => e.key === 'Enter' && wycen()} />
      <datalist id="zam-towary">{#each towary as c}<option value={c.nazwa}></option>{/each}</datalist></label>
    <label class="pole"><span>Jakość <Podpowiedz tekst="HR-024: każda Wada ×½, każda Zaleta ×2. Wyroby z Zaletami wymagają Testu Rzemiosła wytwórcy." /></span>
      <select bind:value={jakosc} onchange={wycen}>{#each d.rynek.jakosc.opcje as j}<option value={j.id}>{j.nazwa} ({mnoz(j.mnoznik)})</option>{/each}</select></label>
    <button class="glowny" onclick={wycen}>Wyceń</button>
  </div>
</div>

{#if wynik}
  <div class="panel">
    {#if wynik.status === 'brak_w_cenniku'}
      <p class="blad">Tego nie ma w cenniku albo to nie jest towar (usługi, nocleg i czynsze się nie zamawia).</p>
    {:else if wynik.status === 'odmowa'}
      <h3>{wynik.przedmiot.nazwa}: odmowa</h3>
      <p>{d.kupcy.kupcy.find((x: any) => x.id === k).nazwa} tego nie robi ani nie sprowadza.
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
        narzut {wynik.status === 'wykonuje' ? 'roboty' : 'sprowadzenia'} {mnoz(s.narzut)} = {mnoz(wynik.mnoznik * wynik.jakosc.mnoznik)}</p>
      {#if wynik.calosc_z_gory}<p class="komunikat">Rzecz poza skalą sklepu: kupiec żąda całości z góry.</p>{/if}
      {#if wynik.test_rzemiosla}<p class="male">{d.rynek.zamowienie.zalety}</p>{/if}
    {/if}
  </div>
{/if}
