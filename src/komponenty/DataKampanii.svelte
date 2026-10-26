<script lang="ts">
  // Data kampanii w kalendarzu Imperium (data/kalendarz.json). Tydzień = 8 dni; pora roku wynika z daty.
  import { stan } from '../lib/stan.svelte';
  import { dataImperialna, dzienRoku } from '../silnik.js';
  import Podpowiedz from './Podpowiedz.svelte';
  let { data = null, onUstaw }: { data?: { dzien: number; rok: number | null } | null; onUstaw: (d: { dzien: number; rok: number | null } | null) => void } = $props();
  const K = $derived(stan.d.kalendarz);
  const dt = $derived(data ? dataImperialna(stan.d, data) : null);
  let mies = $state(0), dzien = $state(1), rok = $state<number | ''>('');
  $effect(() => { if (dt) { mies = K.miesiace.indexOf(dt.miesiac); dzien = dt.dzien_miesiaca; rok = dt.rok ?? ''; } });
</script>

<div class="male" style="margin:6px 0">
  <b>Data:</b> {dt ? `${dt.opis} · ${dt.dzien_tygodnia}` : 'nie ustawiona'}
  <Podpowiedz tekst={K.opis + ' Upływ czasu przesuwa datę o 8 dni na tydzień.'} />
</div>
<div class="pasek">
  <label class="pole"><span>Miesiąc</span><select bind:value={mies}>
    {#each K.miesiace as m, i}<option value={i}>{m.nazwa} ({m.staroswiatowa}){m.swieto ? ' — ' + m.swieto : ''}</option>{/each}</select></label>
  <label class="pole waskie"><span>Dzień</span><input type="number" min="1" max={K.miesiace[mies].dni} bind:value={dzien} disabled={K.miesiace[mies].dni === 1} /></label>
  <label class="pole waskie"><span>Rok (KI)</span><input type="number" bind:value={rok} placeholder="2522" /></label>
  <button onclick={() => onUstaw({ dzien: dzienRoku(stan.d, mies, Math.max(1, dzien | 0)), rok: rok === '' ? null : +rok })}>Ustaw datę</button>
  {#if data}<button class="maly" onclick={() => onUstaw(null)}>Bez daty</button>{/if}
</div>
