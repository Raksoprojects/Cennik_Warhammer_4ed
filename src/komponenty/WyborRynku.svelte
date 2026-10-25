<script lang="ts">
  // Pora roku i wahania rynku (Poradnik Staroświatowca s. 38–39). Pusta wartość = bez modyfikatora.
  import { stan } from '../lib/stan.svelte';
  import { wahaniaZRzutu } from '../silnik.js';
  import Podpowiedz from './Podpowiedz.svelte';
  let { pora = $bindable(null), wahania = $bindable(null), onchange }:
    { pora?: string | null; wahania?: string | null; onchange?: (z: { pora?: string | null; wahania?: string | null }) => void } = $props();
  const H = $derived(stan.d.handel);
  let rzut = $state<number | null>(null);
  function ustawPore(v: string) { pora = v || null; onchange?.({ pora }); }
  function ustawWahania(v: string) { wahania = v || null; onchange?.({ wahania }); }
  function losuj() { rzut = 1 + Math.floor(Math.random() * 10); ustawWahania(wahaniaZRzutu(stan.d, rzut)); }
</script>

<label class="pole"><span>Pora roku <Podpowiedz tekst={H.pory_roku.opis} /></span>
  <select value={pora ?? ''} onchange={e => ustawPore(e.currentTarget.value)}>
    <option value="">bez pory roku</option>
    {#each H.pory_roku.lista as p}<option value={p.id}>{p.nazwa} ({p.uwaga})</option>{/each}
  </select></label>
<label class="pole"><span>Rynek <Podpowiedz tekst={H.wahania.opis + ' 1–2 hossa, 3–8 stabilny, 9–10 bessa. Zapisany kupiec losuje je na nowo co kilka tygodni, jeśli są ustawione.'} /></span>
  <span style="display:flex;gap:6px">
    <select value={wahania ?? ''} onchange={e => ustawWahania(e.currentTarget.value)} style="flex:1">
      <option value="">bez wahań</option>
      {#each H.wahania.lista as w}<option value={w.id}>{w.nazwa}</option>{/each}
    </select>
    <button type="button" onclick={losuj} title="Rzut 1k10">1k10{rzut ? `: ${rzut}` : ''}</button>
  </span></label>
