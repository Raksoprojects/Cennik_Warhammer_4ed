<script lang="ts">
  import { stan } from '../lib/stan.svelte';
  import { mon, norm, pobierzPlik, wczytajPlik, dzis } from '../lib/format';
  let { onNowy }: { onNowy: () => void } = $props();
  const d = $derived(stan.d);
  let q = $state(''), msg = $state('');
  const nazwaZ = (arr: any[], id: string) => arr.find(x => x.id === id)?.nazwa ?? id;
  const widoczni = $derived(stan.kupcy.filter(K => !q || norm([K.nazwa, K.grupa, K.notatka, nazwaZ(d.kupcy.kupcy, K.kupiec)].join(' ')).includes(norm(q))));
  const grupy = $derived.by(() => {
    const m = new Map<string, any[]>();
    for (const K of widoczni) m.set(K.grupa || 'Bez grupy', [...(m.get(K.grupa || 'Bez grupy') ?? []), K]);
    return [...m].sort(([a], [b]) => a === 'Bez grupy' ? 1 : b === 'Bez grupy' ? -1 : a.localeCompare(b, 'pl'));
  });
  function eksportuj() {
    pobierzPlik(`kupcy-${dzis()}.json`, { typ: 'skarbiec-kupcy', wersja: 1, kupcy: stan.kupcy });
    stan.zapisanoEksport();
  }
  async function importuj(e: Event) {
    try {
      const j = await wczytajPlik(e); if (!j) return;
      const lista = j.typ === 'skarbiec-kupcy' ? j.kupcy : j.uid ? [j] : null;
      if (!lista) throw new Error('to nie jest plik kupców Skarbca');
      stan.importujKupcow(lista); msg = `Wczytano ${lista.length} kupców.`;
    } catch (err) { msg = 'Nie udało się wczytać: ' + (err as Error).message; }
  }
</script>

<h2>Moi kupcy</h2>
<div class="pasek nie-drukuj">
  <label class="pole"><span>Szukaj</span><input type="search" bind:value={q} placeholder="imię, grupa, notatka…" /></label>
  <button class="glowny" onclick={onNowy}>Nowy kupiec</button>
  <button onclick={eksportuj} disabled={!stan.kupcy.length}>Eksport wszystkich</button>
  <label class="chip" style="display:inline-flex;align-items:center;min-height:44px">Import z pliku<input type="file" accept=".json,application/json" hidden onchange={importuj} /></label>
</div>
{#if msg}<div class="komunikat">{msg}</div>{/if}
<p class="male drugi">Baza jest w tej przeglądarce. Między telefonem a komputerem przenosisz ją eksportem i importem pliku.</p>

{#each grupy as [g, lista] (g)}
  <details class="sekcja" open>
    <summary><span>{g}</span><span class="szary male">{lista.length}</span></summary>
    <div class="siatka" style="padding:10px 0">
      {#each lista as K (K.uid)}
        <a class="panel" href="#kupcy/{K.uid}" style="display:block;color:inherit;text-decoration:none;margin:0">
          <h3 style="margin-bottom:4px">{K.nazwa}</h3>
          <div class="male drugi">{nazwaZ(d.kupcy.kupcy, K.kupiec)} · {nazwaZ(d.osady.osady, K.osada)} · {nazwaZ(d.koniunktura.koniunktury, K.koniunktura)}</div>
          {#if K.notatka}<p class="male" style="margin:6px 0 0">{K.notatka.length > 140 ? K.notatka.slice(0, 140) + '…' : K.notatka}</p>{/if}
          <div class="male szary" style="margin-top:6px">gotówka <span class="cena">{mon(K.gotowka_p)}</span> · {K.towar.length} pozycji · tydzień {K.tydzien}
            {#if K.zamowienia.some((z: any) => z.status === 'gotowe')}<span class="znacznik zielony">zamówienie gotowe</span>{/if}
            {#if K.zamowienia.some((z: any) => z.status === 'w_toku')}<span class="znacznik niebieski">zamówienia w toku</span>{/if}</div>
        </a>
      {/each}
    </div>
  </details>
{:else}
  <p class="szary">{stan.kupcy.length ? 'Nic nie pasuje.' : 'Baza jest pusta. Wygeneruj kupca i zapisz go.'}</p>
{/each}
