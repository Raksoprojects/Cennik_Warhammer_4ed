<script lang="ts">
  // Generator kupca. Stan w adresie: #kupcy?k=zbrojmistrz&o=altdorf&n=wojna&s=48213 — ten sam link = ten sam kupiec.
  import { stan } from '../lib/stan.svelte';
  import { mon, mnoz } from '../lib/format';
  import { generujKupca, etykietaKoniunktury } from '../silnik.js';
  import WyborOsady from '../komponenty/WyborOsady.svelte';
  import WyborRynku from '../komponenty/WyborRynku.svelte';
  import { utworzKupca, dodajPozycje, czyWAsortymencie, wycen } from '../kupcy_trwali.js';
  import { norm } from '../lib/format';
  import TabelaTowaru from '../komponenty/TabelaTowaru.svelte';
  import PostacKupca from '../komponenty/PostacKupca.svelte';
  import Podpowiedz from '../komponenty/Podpowiedz.svelte';

  const d = $derived(stan.d);
  const p = stan.trasa.param;
  let k = $state(p.get('k') || 'kramarz'), o = $state(p.get('o') || 'miasteczko'), n = $state(p.get('n') || 'normalna');
  let seed = $state(+(p.get('s') || 0) || ((Math.random() * 1e6) | 0)), ps = $state(0), talent = $state(0);
  let nazwa = $state(''), grupa = $state(''), notatka = $state('');

  let charaktery = $state<string[]>(['dobry', 'neutralny', 'zly']);
  let pora = $state<string | null>(p.get('p') || null), wahania = $state<string | null>(p.get('w') || null);
  const sklep = $derived.by(() => { try { return generujKupca(d, { kupiec: k, osada: o, koniunktura: n, seed, charaktery, pora, wahania }); } catch { return null; } });
  $effect(() => { history.replaceState(null, '', `#kupcy?k=${k}&o=${o}&n=${n}&s=${seed}${pora ? '&p=' + pora : ''}${wahania ? '&w=' + wahania : ''}`); });
  const grupy = $derived([...new Set(stan.kupcy.map(x => x.grupa).filter(Boolean))]);

  // Dodatkowy towar MG w wygenerowanym sklepie: cena liczona jak u tego kupca, także spoza asortymentu (ze znacznikiem).
  let dodane = $state<string[]>([]), dodajTxt = $state('');
  $effect(() => { k; o; n; seed; charaktery; pora; wahania; dodane = []; });
  const Kdod = $derived.by(() => {
    if (!sklep) return null;
    let K: any = utworzKupca(d, sklep);
    for (const id of dodane) { const r: any = dodajPozycje(d, K, id, { wymus: true }); if (!r.blad) K = r; }
    return K;
  });
  const towar = $derived(dodane.length && Kdod ? wycen(d, Kdod).towar : sklep?.towar ?? []);
  const towary = $derived(d.cennik.pozycje.filter((c: any) => c.typ === 'towar'));
  const wybrany = $derived(dodajTxt.trim() ? towary.find((c: any) => norm(c.nazwa) === norm(dodajTxt.trim())) : null);
  const pasuje = $derived(wybrany && Kdod ? czyWAsortymencie(d, Kdod, wybrany.id) : null);

  function zapisz() {
    if (!sklep || !Kdod) return;
    const K = { ...Kdod, nazwa: nazwa.trim() || sklep.imie, grupa: grupa.trim(), notatka: notatka.trim() };
    stan.zapiszKupca(K);
    stan.idz('#kupcy/' + K.uid);
  }
</script>

<h2>Generator kupca</h2>
<div class="panel nie-drukuj">
  <div class="pasek">
    <label class="pole"><span>Kto handluje</span><select bind:value={k}>
      {#each d.kupcy.kupcy as x}<option value={x.id}>{x.nazwa} ({mnoz(x.marza)})</option>{/each}</select></label>
    <label class="pole"><span>Gdzie <Podpowiedz tekst="Typ osady albo konkretny ośrodek handlu z Poradnika Staroświatowca (tab. 3-2): wielkość wg populacji, ceny wg zamożności (1–5) i strefy handlowej (co tam tanie, co drogie)." /></span>
      <WyborOsady bind:value={o} /></label>
    <label class="pole"><span>Sytuacja</span><select bind:value={n}>
      {#each d.koniunktura.koniunktury as x}<option value={x.id}>{etykietaKoniunktury(d, x, { krotko: true })}</option>{/each}</select></label>
  </div>
  <div class="pasek"><WyborRynku bind:pora bind:wahania /></div>
  <div class="pasek">
    <label class="pole waskie"><span>Seed <Podpowiedz tekst="Ten sam seed, kupiec, osada i sytuacja dają zawsze tego samego kupca. Link z paska adresu odtwarza sklep." /></span>
      <input type="number" bind:value={seed} /></label>
    <button class="glowny" onclick={() => (seed = (Math.random() * 1e6) | 0)}>Losuj</button>
    <label class="pole waskie"><span>PS z Targowania <Podpowiedz tekst={`Poziomy Sukcesu drużyny w Przeciwstawnym Teście Targowania. Każdy PS −${Math.round(d.rynek.targowanie.za_ps * 100)}%, najwyżej −${Math.round(d.rynek.targowanie.max * 100)}%. Cena nie spada poniżej minimalnej kupca.`} /></span>
      <input type="number" min="0" max="10" bind:value={ps} /></label>
    <label class="pole waskie"><span>Talent, dodatkowe −% <Podpowiedz tekst="Np. Żyłka Handlowa: dodatkowy upust ponad limit z PS, gdy drużyna wygrała test. Wpisz procent, np. 4." /></span>
      <input type="number" min="0" max="30" bind:value={() => Math.round(talent * 100), v => (talent = Math.max(0, +v || 0) / 100)} /></label>
  </div>
  <div class="chipy"><span class="male drugi" style="align-self:center">Charakter kupca:</span>
    {#each [['dobry', 'dobry'], ['neutralny', 'neutralny'], ['zly', 'zły']] as [id, nazwa]}
      <button class="chip" aria-pressed={charaktery.includes(id)} onclick={() => (charaktery = charaktery.includes(id) ? charaktery.filter(x => x !== id) : [...charaktery, id])}>{nazwa}</button>
    {/each}
    <Podpowiedz tekst="Losuje tylko z zaznaczonych. Motywacja, cecha kupiecka, potrzeba i sekret pasują do charakteru. Nic nie zaznaczone = wszystkie." />
  </div>
</div>

{#if sklep}
  <div class="panel">
    <h3>{sklep.imie} <span class="drugi male">— {sklep.kupiec.nazwa}, {sklep.kupiec.status}</span></h3>
    <p class="drugi">{sklep.kupiec.opis} <i>{sklep.dziwactwo}</i></p>
    <PostacKupca postac={sklep.postac} />
    <p class="male">{sklep.etykiety.osada} · {sklep.etykiety.koniunktura}</p>
    <div class="liczby">
      <div><span>Gotówka</span><b class="cena">{mon(sklep.gotowka_p ?? 0)}</b></div>
      <div><span>Wartość towaru</span><b>{mon(sklep.wartosc_towaru_p)}</b></div>
      <div><span>Marża</span><b>{mnoz(sklep.kupiec.marza)}</b></div>
      <div><span>Skup</span><b>{Math.round(sklep.kupiec.skup * 100)}% jego ceny</b></div>
    </div>
  </div>
  <TabelaTowaru {towar} {ps} {talent} bezTargu={!!sklep.postac?.cecha?.efekt?.bez_targu} gotowka={sklep.gotowka_p} />

  <div class="panel nie-drukuj" style="margin-top:14px">
    <h3>Dodaj towar do tego sklepu <Podpowiedz tekst="Cena liczona jak u tego kupca (marża, osada, sytuacja, kaprys). Rzecz spoza jego asortymentu dostaje znacznik. Dodany towar zapisuje się razem z kupcem." /></h3>
    <div class="pasek">
      <label class="pole"><span>Co</span><input bind:value={dodajTxt} list="gen-towary" placeholder="np. lutnia, kolczuga" />
        <datalist id="gen-towary">{#each towary as c}<option value={c.nazwa}></option>{/each}</datalist></label>
      <button disabled={!wybrany} onclick={() => { if (wybrany && !dodane.includes(wybrany.id)) dodane = [...dodane, wybrany.id]; dodajTxt = ''; }}>Dodaj</button>
      {#if dodane.length}<button class="maly" onclick={() => (dodane = [])}>Usuń dodane ({dodane.length})</button>{/if}
    </div>
    {#if pasuje}<p class="male" class:ok={pasuje.ok} class:blad={!pasuje.ok}>{pasuje.ok ? 'Pasuje do tego kupca.' : `Nie pasuje: ${pasuje.powod}. Możesz dodać mimo to.`}</p>{/if}
  </div>

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
