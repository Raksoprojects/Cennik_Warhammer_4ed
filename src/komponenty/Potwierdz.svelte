<script lang="ts">
  // Okno decyzji MG („niedostępne u tego kupca — czy chcesz kontynuować?”).
  let { tytul, tekst, tak = 'Tak, kontynuuj', onTak, onNie }:
    { tytul: string; tekst: string; tak?: string; onTak: () => void; onNie: () => void } = $props();
</script>

<div class="zaslona" role="presentation" onclick={onNie} onkeydown={e => e.key === 'Escape' && onNie()}>
  <!-- svelte-ignore a11y_click_events_have_key_events -->
  <div class="okno" role="dialog" aria-modal="true" aria-label={tytul} tabindex="-1" onclick={e => e.stopPropagation()}>
    <h3>{tytul}</h3>
    <p>{tekst}</p>
    <div class="przyciski">
      <button class="glowny" onclick={onTak}>{tak}</button>
      <button onclick={onNie}>Anuluj</button>
    </div>
  </div>
</div>
