<script lang="ts">
  import { stan } from '../lib/stan.svelte';
  import { mon, proc, mnoz } from '../lib/format';
  import { czynsz, etykietaOsady } from '../silnik.js';

  const d = $derived(stan.d);
  let o = $state('miasteczko'), n = $state('normalna');
  const mCz = (k: any) => k.czynsz?.mnoznik ?? 1;
  const wiersze = $derived(d.czynsze.najem.map((k: any) => {
    const z = (okres: string) => czynsz(d, { kwatera: k.kwatera, okres, osada: o, koniunktura: n });
    return { kwatera: k.kwatera, t: z('tydzien'), m: z('miesiac'), r: z('rok') };
  }));
  const domMistrza = $derived(d.czynsze.najem.find((k: any) => /mistrza/.test(k.kwatera)));
</script>

<h2>Czynsze</h2>
<p class="drugi">Najem: baza × osada × sytuacja. Czynsz ma własny mnożnik sytuacji: po zarazie spada (puste izby), w oblężeniu i kryzysie mieszkaniowym rośnie.</p>
<div class="pasek">
  <label class="pole"><span>Osada</span><select bind:value={o}>{#each d.osady.osady as x}<option value={x.id}>{etykietaOsady(x)}</option>{/each}</select></label>
  <label class="pole"><span>Sytuacja</span><select bind:value={n}>
    {#each d.koniunktura.koniunktury as k}<option value={k.id}>{k.nazwa} (czynsz {mCz(k) === 1 ? 'bez zmian' : proc(mCz(k))})</option>{/each}</select></label>
</div>
<div class="tabela karty">
  <table class="karty">
    <thead><tr><th>Kwatera</th><th class="num">Tydzień</th><th class="num">Miesiąc</th><th class="num">Rok</th><th class="num">Mnożnik</th></tr></thead>
    <tbody>
      {#each wiersze as w}
        <tr><td class="tytul">{w.kwatera}</td>
          <td class="num" data-l="Tydzień">{mon(w.t?.cena_p ?? 0)}</td>
          <td class="num" data-l="Miesiąc"><span class="cena">{mon(w.m?.cena_p ?? 0)}</span></td>
          <td class="num" data-l="Rok">{mon(w.r?.cena_p ?? 0)}</td>
          <td class="num" data-l="Mnożnik" class:plus={w.m.mnoznik > 1.001} class:minus={w.m.mnoznik < 0.999}>{mnoz(w.m.mnoznik)}</td></tr>
      {/each}
    </tbody>
  </table>
</div>
<div class="siatka" style="margin-top:14px">
  <div class="panel">
    <h3>Kupno</h3>
    {#each d.czynsze.kupno as k}<div>{k.nazwa}: <b class="cena">{mon(k.cena_p)}</b>
      {#if domMistrza}<span class="drugi male"> — {Math.round(k.cena_p / domMistrza.rok_p)} lat najmu domu mistrza</span>{/if}</div>{/each}
  </div>
  <div class="panel">
    <h3>Mnożnik czynszu wg sytuacji</h3>
    {#each d.koniunktura.koniunktury as k}<div>{k.nazwa}: <b class:plus={mCz(k) > 1} class:minus={mCz(k) < 1}>{mCz(k) === 1 ? 'bez zmian' : proc(mCz(k))}</b>
      {#if k.czynsz?.uwaga}<div class="male szary">{k.czynsz.uwaga}</div>{/if}</div>{/each}
  </div>
</div>
