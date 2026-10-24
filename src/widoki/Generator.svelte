<script lang="ts">
  // Generator kupca. Stan w adresie: #kupcy?k=zbrojmistrz&o=altdorf&n=wojna&s=48213 — ten sam link = ten sam kupiec.
  import { stan } from '../lib/stan.svelte';
  import { mon, mnoz } from '../lib/format';
  import { generujKupca, etykietaOsady, etykietaKoniunktury } from '../silnik.js';
  import { utworzKupca } from '../kupcy_trwali.js';
  import TabelaTowaru from '../komponenty/TabelaTowaru.svelte';
  import Podpowiedz from '../komponenty/Podpowiedz.svelte';

  const d = $derived(stan.d);
  const p = stan.trasa.param;
  let k = $state(p.get('k') || 'kramarz'), o = $state(p.get('o') || 'miasteczko'), n = $state(p.get('n') || 'normalna');
  let seed = $state(+(p.get('s') || 0) || ((Math.random() * 1e6) | 0)), ps = $state(0);
  let nazwa = $state(''), grupa = $state(''), notatka = $state('');

  const sklep = $derived.by(() => { try { return generujKupca(d, { kupiec: k, osada: o, koniunktura: n, seed }); } catch { return null; } });
  $effect(() => { history.replaceState(null, '', `#kupcy?k=${k}&o=${o}&n=${n}&s=${seed}`); });
  const grupy = $derived([...new Set(stan.kupcy.map(x => x.grupa).filter(Boolean))]);

  function zapisz() {
    if (!sklep) return;
    const K = utworzKupca(d, sklep, { nazwa: nazwa.trim() || undefined, grupa: grupa.trim(), notatka: notatka.trim() });
    stan.zapiszKupca(K);
    stan.idz('#kupcy/' + K.uid);
  }
</script>

<h2>Generator kupca</h2>
<div class="panel nie-drukuj">
  <div class="pasek">
    <label class="pole"><span>Kto handluje</span><select bind:value={k}>
      {#each d.kupcy.kupcy as x}<option value={x.id}>{x.nazwa} ({mnoz(x.marza)})</option>{/each}</select></label>
    <label class="pole"><span>Gdzie</span><select bind:value={o}>
      {#each d.osady.osady as x}<option value={x.id}>{etykietaOsady(x)}</option>{/each}</select></label>
    <label class="pole"><span>Sytuacja</span><select bind:value={n}>
      {#each d.koniunktura.koniunktury as x}<option value={x.id}>{etykietaKoniunktury(d, x, { krotko: true })}</option>{/each}</select></label>
  </div>
  <div class="pasek">
    <label class="pole waskie"><span>Seed <Podpowiedz tekst="Ten sam seed, kupiec, osada i sytuacja dają zawsze tego samego kupca. Link z paska adresu odtwarza sklep." /></span>
      <input type="number" bind:value={seed} /></label>
    <button class="glowny" onclick={() => (seed = (Math.random() * 1e6) | 0)}>Losuj</button>
    <label class="pole waskie"><span>PS z Targowania <Podpowiedz tekst="Poziomy Sukcesu drużyny w Przeciwstawnym Teście Targowania. Każdy PS −10%, najwyżej −30%. Cena nie spada poniżej minimalnej." /></span>
      <input type="number" min="0" max="10" bind:value={ps} /></label>
  </div>
</div>

{#if sklep}
  <div class="panel">
    <h3>{sklep.imie} <span class="drugi male">— {sklep.kupiec.nazwa}, {sklep.kupiec.status}</span></h3>
    <p class="drugi">{sklep.kupiec.opis} <i>{sklep.dziwactwo}</i></p>
    <p class="male">{sklep.etykiety.osada} · {sklep.etykiety.koniunktura}</p>
    <div class="liczby">
      <div><span>Gotówka</span><b class="cena">{mon(sklep.gotowka_p ?? 0)}</b></div>
      <div><span>Wartość towaru</span><b>{mon(sklep.wartosc_towaru_p)}</b></div>
      <div><span>Marża</span><b>{mnoz(sklep.kupiec.marza)}</b></div>
      <div><span>Skup</span><b>{Math.round(sklep.kupiec.skup * 100)}% jego ceny</b></div>
    </div>
  </div>
  <TabelaTowaru towar={sklep.towar} {ps} gotowka={sklep.gotowka_p} />

  <div class="panel nie-drukuj" style="margin-top:14px">
    <h3>Zapisz do bazy kupców</h3>
    <p class="male drugi">Zapisany kupiec trafia do „Moi kupcy”. Tam zmienisz towar, ceny, miasto i sytuację, a czas zrobi resztę.</p>
    <div class="pasek">
      <label class="pole"><span>Nazwa</span><input bind:value={nazwa} placeholder={sklep.imie} /></label>
      <label class="pole"><span>Grupa (np. miasto)</span><input bind:value={grupa} list="grupy-kupcow" placeholder="Altdorf" />
        <datalist id="grupy-kupcow">{#each grupy as g}<option value={g}></option>{/each}</datalist></label>
    </div>
    <label class="pole"><span>Notatka</span><textarea bind:value={notatka} placeholder="Krótki opis, kto to, co wie, jak traktuje drużynę…"></textarea></label>
    <div class="przyciski"><button class="glowny" onclick={zapisz}>Zapisz kupca</button></div>
  </div>
{:else}
  <p class="blad">Nie udało się wygenerować kupca.</p>
{/if}
