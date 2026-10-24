<script lang="ts">
  // Towar kupca: trzy ceny po kolei (podręcznik → bazowa → jego), minimalna, targ, skup, „dlaczego tyle”.
  // W trybie edycji (zapisany kupiec) wiersz po rozwinięciu daje zmianę ilości, cenę ręczną i transakcje.
  import { mon, proc, mnoz, parsujCene } from '../lib/format';
  import { stan } from '../lib/stan.svelte';
  import { targuj, modyfikatorTargowania } from '../silnik.js';

  let { towar, ps = 0, gotowka = null, edycja = false, onZmien, onUsun, onPrzelosuj, onTransakcja }: {
    towar: any[]; ps?: number; gotowka?: number | null; edycja?: boolean;
    onZmien?: (id: string, z: any) => void; onUsun?: (id: string) => void; onPrzelosuj?: (id: string) => void;
    onTransakcja?: (id: string, typ: 'kupno' | 'sprzedaz', ilosc: number, cena_p: number) => void;
  } = $props();
  const d = $derived(stan.d);
  let otwarte = $state<string | null>(null), ile = $state(1), cenaReczna = $state('');
  const kaprysOpis = (rzut: number | null) => rzut == null ? '' : d.rynek.kaprys.progi.find((p: any) => rzut <= p.do)?.opis ?? '';
  const poTargu = (t: any) => targuj(d, { cena_p: t.cena_p, cena_cennik_p: t.cena_wytworcy_p, cena_min_p: t.cena_min_p, ps }).cena_p;
  function otworz(id: string) { otwarte = otwarte === id ? null : id; ile = 1; cenaReczna = ''; }
  function ustawCene(t: any) {
    const p = parsujCene(cenaReczna);
    if (p === null) onZmien?.(t.id, { cena_reczna_p: null });
    else if (!Number.isNaN(p)) onZmien?.(t.id, { cena_reczna_p: p });
    cenaReczna = '';
  }
</script>

<div class="tabela karty">
  <table class="karty">
    <thead><tr>
      <th>Towar</th><th class="num">Sztuk</th><th class="num">Podręcznik</th><th class="num">Bazowa</th>
      <th class="num">Jego cena</th><th class="num">Minimalna</th>{#if ps > 0}<th class="num">Po targu</th>{/if}<th class="num">Odkupi za</th>
    </tr></thead>
    <tbody>
      {#each towar as t (t.id)}
        <tr class="klik" class:otwarty={otwarte === t.id} onclick={() => otworz(t.id)}>
          <td class="tytul">{t.nazwa}
            {#if t.sztuk === 0}<span class="znacznik">brak — na zamówienie</span>{:else if t.zapas === 2}<span class="znacznik czerwony">ostatnie sztuki</span>{:else if t.zapas === 0}<span class="znacznik zielony">pełen skład</span>{/if}
            {#if t.cena_reczna_p != null}<span class="znacznik zloty">cena MG</span>{/if}
            {#if t.poza_asortymentem}<span class="znacznik fiolet">spoza asortymentu</span>{/if}
          </td>
          <td class="num" data-l="Sztuk">{t.sztuk}</td>
          <td class="num szary zwin" data-l="Podręcznik">{t.cena_raw_p == null ? '—' : mon(t.cena_raw_p)}</td>
          <td class="num drugi" data-l="Bazowa">{mon(t.cena_wytworcy_p)}</td>
          <td class="num" data-l="Jego cena"><span><span class="cena">{mon(t.cena_p)}</span>
            <span class="male" class:plus={t.cena_p > t.cena_wytworcy_p} class:minus={t.cena_p < t.cena_wytworcy_p}>{proc(t.cena_p / t.cena_wytworcy_p)}</span></span></td>
          <td class="num zwin" data-l="Minimalna"><span>{mon(t.cena_min_p)}{#if t.wyprzedaz}<span class="znacznik zielony">wyprzedaż</span>{/if}</span></td>
          {#if ps > 0}<td class="num" data-l="Po targu ({ps} PS)">{mon(poTargu(t))}</td>{/if}
          <td class="num zwin" data-l="Odkupi za"><span>{mon(t.skup_p)}{#if gotowka != null && t.skup_p > gotowka}<span class="znacznik czerwony">brak gotówki</span>{/if}</span></td>
        </tr>
        {#if otwarte === t.id}
          {@const s = t.skladowe}
          <tr class="szczegoly"><td class="pelna" colspan="8">
            <dl class="szczegoly-siatka">
              <div><dt>Rynek</dt><dd>{t.zapas_nazwa}, {t.popyt_nazwa} → {mnoz(s.rynek)}<br />
                <span class="drugi male">Modyfikator Testu Targowania: {modyfikatorTargowania(t) > 0 ? '+' : ''}{modyfikatorTargowania(t)}</span></dd></div>
              <div><dt>Mnożniki</dt><dd>marża {mnoz(s.marza)} · preferencja {mnoz(s.preferencja)} · kaprys {mnoz(s.kaprys)}
                {#if t.rzuty?.kaprys != null}<span class="drugi">(1k10 = {t.rzuty.kaprys}: {kaprysOpis(t.rzuty.kaprys)})</span>{/if}
                · osada {mnoz(s.osada)} · sytuacja {mnoz(s.koniunktura)}{#if s.modyfikator != null && s.modyfikator !== 1} · MG {mnoz(s.modyfikator)}{/if}
                = <b>{mnoz(t.mnoznik)}</b></dd></div>
              <div><dt>Koszt nabycia · minimalna</dt><dd>{mon(t.koszt_p)} · {mon(t.cena_min_p)}
                <span class="drugi male">— poniżej minimalnej nie zejdzie w targowaniu</span></dd></div>
            </dl>
            {#if edycja}
              <div class="pasek nie-drukuj" style="margin-top:10px">
                <label class="pole waskie"><span>Sztuk</span>
                  <input type="number" min="0" value={t.sztuk} onchange={e => onZmien?.(t.id, { sztuk: Math.max(0, +e.currentTarget.value | 0) })} /></label>
                <label class="pole waskie"><span>Cena ręczna</span><input bind:value={cenaReczna} placeholder={mon(t.cena_p)} /></label>
                <button onclick={() => ustawCene(t)}>{cenaReczna ? 'Ustaw cenę' : 'Cena z wyliczenia'}</button>
                <button onclick={() => onPrzelosuj?.(t.id)}>Przelosuj</button>
                <button class="niebezp" onclick={() => onUsun?.(t.id)}>Usuń</button>
              </div>
              <div class="pasek nie-drukuj">
                <label class="pole waskie"><span>Ile</span><input type="number" min="1" bind:value={ile} /></label>
                <button class="glowny" disabled={t.sztuk < ile} onclick={() => onTransakcja?.(t.id, 'kupno', ile, ps > 0 ? poTargu(t) : t.cena_p)}>
                  Drużyna kupuje za {mon((ps > 0 ? poTargu(t) : t.cena_p) * ile)}</button>
                <button onclick={() => onTransakcja?.(t.id, 'sprzedaz', ile, t.skup_p)}>Drużyna sprzedaje za {mon(t.skup_p * ile)}</button>
              </div>
            {/if}
          </td></tr>
        {/if}
      {:else}
        <tr><td class="pelna szary" colspan="8">Pusty sklep.</td></tr>
      {/each}
    </tbody>
  </table>
</div>
