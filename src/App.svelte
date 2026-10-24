<script lang="ts">
  import { stan } from './lib/stan.svelte';
  import Cennik from './widoki/Cennik.svelte';
  import Kupcy from './widoki/Kupcy.svelte';
  import Zamowienie from './widoki/Zamowienie.svelte';
  import Zarobki from './widoki/Zarobki.svelte';
  import Czynsze from './widoki/Czynsze.svelte';
  import EdycjaCen from './widoki/EdycjaCen.svelte';
  import Tabele from './widoki/Tabele.svelte';

  const WIDOKI = [
    ['cennik', 'Cennik', Cennik], ['kupcy', 'Kupcy', Kupcy], ['zamowienie', 'Zamówienie', Zamowienie],
    ['zarobki', 'Zarobki', Zarobki], ['czynsze', 'Czynsze', Czynsze], ['edycja', 'Edycja cen', EdycjaCen],
    ['tabele', 'Zasady i tabele', Tabele],
  ] as const;
  const biezacy = $derived(WIDOKI.find(w => w[0] === stan.trasa.widok) ?? WIDOKI[0]);
  const Widok = $derived(biezacy[2]);
</script>

<header class="naglowek">
  <div class="naglowek-gora">
    <h1>Skarbiec Imperium</h1>
    {#if stan.wlasne}<a class="znacznik zloty" href="#edycja" title="Cennik zmieniony w Edycji cen">własne ceny</a>{/if}
  </div>
  <nav class="zakladki" aria-label="Zakładki">
    {#each WIDOKI as [id, nazwa]}
      <a href="#{id}" aria-current={id === biezacy[0] ? 'page' : undefined}>{nazwa}</a>
    {/each}
  </nav>
</header>
<main>
  {#if stan.wynik.blad}<div class="komunikat zly">Błąd w ustawieniach MG: {stan.wynik.blad}. Pokazuję cennik domyślny.</div>{/if}
  <Widok />
</main>
