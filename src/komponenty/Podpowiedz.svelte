<script lang="ts">
  // Klikalna podpowiedź „?”. Drugi klik albo klik obok zamyka. Na telefonie dymek wychodzi od dołu ekranu.
  import type { Snippet } from 'svelte';
  let { tekst = '', children }: { tekst?: string; children?: Snippet } = $props();
  let otwarte = $state(false);
</script>

<svelte:window onclick={() => (otwarte = false)} onkeydown={e => e.key === 'Escape' && (otwarte = false)} />
<span class="pp">
  <button type="button" class="pp-btn" aria-label="Podpowiedź" aria-expanded={otwarte}
    onclick={e => { e.stopPropagation(); otwarte = !otwarte; }}>?</button>
  {#if otwarte}
    <!-- svelte-ignore a11y_click_events_have_key_events -->
    <span class="pp-dymek" role="note" onclick={e => e.stopPropagation()}>{tekst}{@render children?.()}</span>
  {/if}
</span>
