<script lang="ts">
  // Zalety i Wady przedmiotu (PG s. 292) z poziomami. Wartość: { Wytrzymały: 2, Tandetny: 1 }.
  import { stan } from '../lib/stan.svelte';
  import { mnoz } from '../lib/format';
  import { jakoscZ } from '../silnik.js';
  let { cechy = $bindable({}) }: { cechy?: Record<string, number> } = $props();
  const J = $derived(stan.d.rynek.jakosc);
  const jak = $derived(jakoscZ(stan.d, cechy));
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
  <div class="male">Jakość: <b>{jak.nazwa}</b> → cena <b class="cena">{mnoz(jak.mnoznik)}</b>
    {#if jak.zalety > jak.wady}<span class="drugi">(Dostępność o {jak.zalety - jak.wady} stopień rzadsza)</span>{/if}</div>
</div>

<style>
  .cechy { display: flex; flex-direction: column; gap: 6px; }
  .cecha { display: inline-flex; align-items: center; gap: 4px; margin: 2px 8px 2px 0; }
  .cecha select { min-height: 34px; padding: 2px 6px; }
</style>
