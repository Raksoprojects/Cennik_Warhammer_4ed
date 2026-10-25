<script lang="ts">
  // Zalety i Wady przedmiotu (PG s. 292) z poziomami. Wartość: { Wytrzymały: 2, Tandetny: 1 }.
  // Niezwykłe (bardzo rzadko): Zaleta innej broni albo usunięta Wada broni — liczą się jak Zaleta przedmiotu.
  import { stan } from '../lib/stan.svelte';
  import { mnoz } from '../lib/format';
  import { jakoscZ } from '../silnik.js';
  let { cechy = $bindable({}) }: { cechy?: Record<string, number> } = $props();
  const J = $derived(stan.d.rynek.jakosc);
  const N = $derived(J.niezwykle);
  const jak = $derived(jakoscZ(stan.d, cechy));
  const nazwyCech = (pole: 'zalety' | 'wady') =>
    [...new Set(stan.d.bron_cechy.pozycje.flatMap((p: any) => (p[pole] ?? []).map((x: any) => x.nazwa.replace(/\s*\(.*\)$/, ''))))].sort() as string[];
  const zaletyBroni = $derived(nazwyCech('zalety')), wadyBroni = $derived(nazwyCech('wady'));
  const niezwykle = $derived(Object.keys(cechy).filter(k => N && (k.startsWith(N.prefiks_zalety) || k.startsWith(N.prefiks_bez_wady))));
  let nowaZaleta = $state(''), bezWady = $state('');
  function ustaw(nazwa: string, n: number) {
    const c = { ...cechy }; if (n > 0) c[nazwa] = n; else delete c[nazwa]; cechy = c;
  }
</script>

<div class="cechy">
  {#each [['Zalety', J.zalety], ['Wady', J.wady]] as [tytul, lista]}
    <div class="male"><b>{tytul}:</b>
      {#each lista as z}
        <label class="cecha" title={z.opis}>{z.nazwa}
          <select value={cechy[z.nazwa] ?? 0} onchange={e => ustaw(z.nazwa, +e.currentTarget.value)}>
            {#each z.wielokrotna ? [0, 1, 2, 3, 4] : [0, 1] as n}<option value={n}>{n || '—'}</option>{/each}
          </select></label>
      {/each}
    </div>
  {/each}
  {#if N}
    <details class="male">
      <summary style="cursor:pointer;color:var(--fiolet)">Niezwykłe (bardzo rzadko){niezwykle.length ? ` — ${niezwykle.length}` : ''}</summary>
      <p class="drugi">{N.opis}</p>
      <div class="pasek">
        <select bind:value={nowaZaleta}><option value="">Zaleta innej broni…</option>{#each zaletyBroni as z}<option>{z}</option>{/each}</select>
        <button class="maly" disabled={!nowaZaleta} onclick={() => { ustaw(N.prefiks_zalety + nowaZaleta, 1); nowaZaleta = ''; }}>Dodaj</button>
        <select bind:value={bezWady}><option value="">Usuń Wadę broni…</option>{#each wadyBroni as z}<option>{z}</option>{/each}</select>
        <button class="maly" disabled={!bezWady} onclick={() => { ustaw(N.prefiks_bez_wady + bezWady, 1); bezWady = ''; }}>Dodaj</button>
      </div>
      {#each niezwykle as k}<span class="znacznik fiolet">{k} <button class="maly" aria-label="Usuń" onclick={() => ustaw(k, 0)}>✕</button></span>{/each}
    </details>
  {/if}
  <div class="male">Jakość: <b>{jak.nazwa}</b> → cena <b class="cena">{mnoz(jak.mnoznik)}</b>
    {#if jak.zalety > jak.wady}<span class="drugi">(Dostępność o {jak.zalety - jak.wady} stopień rzadsza)</span>{/if}</div>
</div>

<style>
  .cechy { display: flex; flex-direction: column; gap: 6px; }
  .cecha { display: inline-flex; align-items: center; gap: 4px; margin: 2px 8px 2px 0; }
  .cecha select { min-height: 34px; padding: 2px 6px; }
</style>
