<script lang="ts">
  // Lista osad: typy osad, potem ośrodki handlu z Poradnika pogrupowane wg strefy handlowej.
  import { stan } from '../lib/stan.svelte';
  import { etykietaOsady } from '../silnik.js';
  let { value = $bindable(), onchange }: { value: string; onchange?: (v: string) => void } = $props();
  const osady = $derived(stan.d.osady.osady as any[]);
  const grupy = $derived([...new Set(osady.filter(o => o.grupa).map(o => o.grupa))] as string[]);
  // Domyślna sytuacja osady (np. północ po wojnie) — dopisek, żeby MG wiedział, skąd zmiana sytuacji.
  const syt = (o: any) => o.sytuacja ? ' · ' + (stan.d.koniunktura.koniunktury.find((k: any) => k.id === o.sytuacja)?.nazwa ?? o.sytuacja) : '';
  const opis = (o: any) => (o.populacja ? `${o.nazwa} — ${o.populacja.toLocaleString('pl')} mieszk., zamożność ${o.zamoznosc}${o.wolne_miasto ? ', wolne miasto' : ''} (${etykietaOsady(o).split('(').pop()}` : etykietaOsady(o)) + syt(o);
</script>

<select bind:value onchange={e => onchange?.(e.currentTarget.value)}>
  <optgroup label="Typy osad">{#each osady.filter(o => !o.grupa) as o}<option value={o.id}>{etykietaOsady(o)}</option>{/each}</optgroup>
  {#each grupy as g}
    <optgroup label={g}>{#each osady.filter(o => o.grupa === g) as o}<option value={o.id}>{opis(o)}</option>{/each}</optgroup>
  {/each}
</select>
