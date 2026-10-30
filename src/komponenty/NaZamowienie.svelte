<script lang="ts">
  // Co ten kupiec zrobi albo sprowadzi na zamówienie (rzeczy, których nie ma na półce). Liczone po rozwinięciu.
  import { stan } from '../lib/stan.svelte';
  import { mon } from '../lib/format';
  import { wycenZamowienie, wTowarze, robiTo } from '../silnik.js';
  import { handlujacy, zrodloNazwa } from '../lib/ceny';
  let { kupiec, osada, koniunktura, pora = null, wahania = null, naStanie = [] }:
    { kupiec: string; osada: string; koniunktura: string; pora?: string | null; wahania?: string | null; naStanie?: string[] } = $props();
  let otwarte = $state(false), q = $state('');
  const d = $derived(stan.d);
  const lista = $derived.by(() => {
    if (!otwarte) return [];
    const kup = d.kupcy.kupcy.find((k: any) => k.id === kupiec), mam = new Set(naStanie);
    return d.cennik.pozycje
      .filter((c: any) => wTowarze(d, c) && !mam.has(c.id) && (robiTo(kup, c) || handlujacy(d, c).includes(kup)))
      .map((c: any) => ({ c, w: wycenZamowienie(d, { kupiec, osada, koniunktura, przedmiot: c, pora, wahania, seed: 1 }) }))
      .filter((x: any) => x.w.status === 'wykonuje' || x.w.status === 'sprowadza');
  });
  const widoczne = $derived(q ? lista.filter((x: any) => x.c.nazwa.toLowerCase().includes(q.toLowerCase())) : lista);
  const kategorie = $derived([...new Set(widoczne.map((x: any) => x.c.kat))] as string[]);
</script>

<details class="opis nie-drukuj" bind:open={otwarte}>
  <summary>Na zamówienie u niego{otwarte ? ` (${lista.length})` : ''}</summary>
  <p class="male drugi">Rzeczy, których nie ma na półce, a kupiec je zrobi albo sprowadzi. Cena zwykłej jakości, z jego marżą,
    osadą i sytuacją. Zamówienie złożysz w karcie zapisanego kupca albo w zakładce Zamówienie.</p>
  <label class="pole"><span>Szukaj</span><input type="search" bind:value={q} /></label>
  {#each kategorie as k}
    <h4 style="margin:10px 0 4px">{k}</h4>
    {#each widoczne.filter((x: any) => x.c.kat === k) as { c, w }}
      <details class="male" style="padding:2px 0">
        <summary style="cursor:pointer">{c.nazwa} <span class="szary">({c.dostepnosc ?? 'Powszechna'})</span> —
          <span class="cena">{mon(w.cena_p)}</span> · {w.termin}{w.rzadkosc ? ` + ${w.rzadkosc.termin_tyg} tyg.` : ''}
          <span class="znacznik" class:zielony={w.status === 'wykonuje'}>{w.status === 'wykonuje' ? 'robi sam' : 'sprowadza'}</span></summary>
        <div class="drugi" style="padding:2px 0 6px 14px">Źródło: {zrodloNazwa(c.zrodlo, c.strona)}. Zaliczka {mon(w.zaliczka_p)}.
          {#if w.rzadkosc}Tu rzadkość ({w.rzadkosc.dostepnosc}): narzut ×{String(w.rzadkosc.narzut).replace('.', ',')} w cenie.{/if}
          {#if c.nielegalny}<span class="blad">Nielegalny.</span>{/if}</div>
      </details>
    {/each}
  {/each}
</details>
