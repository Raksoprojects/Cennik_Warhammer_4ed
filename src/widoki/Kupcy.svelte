<script lang="ts">
  import { stan } from '../lib/stan.svelte';
  import Generator from './Generator.svelte';
  import BazaKupcow from './BazaKupcow.svelte';
  import KartaKupca from './KartaKupca.svelte';
  let pod = $state<'generator' | 'baza'>(stan.kupcy.length ? 'baza' : 'generator');
  const uid = $derived(stan.trasa.sciezka);
  $effect(() => { if (stan.trasa.param.has('s')) pod = 'generator'; });
</script>

{#if uid}
  {#if stan.kupiec(uid)}<KartaKupca {uid} />
  {:else}<p>Nie ma takiego kupca w bazie. <a href="#kupcy">Wróć do listy</a>.</p>{/if}
{:else}
  <div class="podzakladki nie-drukuj">
    <button class="chip" aria-pressed={pod === 'baza'} onclick={() => (pod = 'baza')}>Moi kupcy ({stan.kupcy.length})</button>
    <button class="chip" aria-pressed={pod === 'generator'} onclick={() => (pod = 'generator')}>Generator</button>
  </div>
  {#if pod === 'generator'}<Generator />{:else}<BazaKupcow onNowy={() => (pod = 'generator')} />{/if}
{/if}
