<script lang="ts">
  import { stan } from '../lib/stan.svelte';
  import { mon, pl, norm } from '../lib/format';
  import { sredniDochod, rzutDochodu, jalmuzna } from '../silnik.js';
  import Podpowiedz from '../komponenty/Podpowiedz.svelte';

  const d = $derived(stan.d);
  let status = $state('Srebro 3'), majetny = $state(0), rzut = $state<any>(null), wlasne = $state<string[]>([]), dodaj = $state('');
  let psJal = $state(2), swieto = $state(false), jal = $state<number | null>(null);
  const KOSZYK = ['miecz', 'kolczuga', 'pelna-plytowka-4-elementy', 'kon-wierzchowy', 'rumak'];
  const sr = $derived(sredniDochod(d, status, majetny));
  const poz = $derived(d.statusy.poziomy.find((s: any) => s.tier + ' ' + s.lvl === status));
  const koszyk = $derived([...KOSZYK, ...wlasne].map(id => d.cennik.pozycje.find((c: any) => c.id === id)).filter(Boolean));
  const ileRobot = (p: number) => {
    const n = sr.netto_p; if (n <= 0) return 'nigdy';
    const t = p / n; return t <= 1 ? 'jedna Robota' : t < 40 ? Math.round(t) + ' Robót' : 'ponad 40 Robót — realnie tylko z łupu albo spadku';
  };
  function dodajDoKoszyka() {
    const n = norm(dodaj.trim()), c = d.cennik.pozycje.find((x: any) => norm(x.nazwa) === n);
    if (c && !wlasne.includes(c.id) && !KOSZYK.includes(c.id)) wlasne = [...wlasne, c.id];
    dodaj = '';
  }
</script>

<h2>Zarobki wg Statusu</h2>
<details class="opis">
  <summary>Jak to działa</summary>
  <p>Rzut to <b>netto</b> — co zostaje po jednej Robocie (tygodniu pracy ponad normę). Nie mnóż przez 52: między przygodami
    postać ma zwykle 1–3 Roboty. Brutto = 5 × netto; 80% brutto idzie na utrzymanie w osadzie.</p>
  <p>Brąz N = 2N k10 p, Srebro N = N k10 s, Złoto N = N k5 ZK. Majętny: +1k5 monet szczebla za poziom Talentu, dodawane do rzutu (netto).</p>
</details>

<div class="siatka">
  <div class="panel">
    <h3>Kalkulator</h3>
    <div class="pasek">
      <label class="pole"><span>Status</span><select bind:value={status} onchange={() => (rzut = null)}>
        {#each d.statusy.poziomy as s}<option>{s.tier} {s.lvl}</option>{/each}</select></label>
      <label class="pole waskie"><span>Majętny</span><select bind:value={majetny} onchange={() => (rzut = null)}>
        {#each [0, 1, 2, 3] as m}<option value={m}>{m || 'brak'}</option>{/each}</select></label>
      <button class="glowny" onclick={() => (rzut = rzutDochodu(d, { status, majetny }))}>Rzuć na Dochód</button>
    </div>
    {#if poz}<p class="drugi male">{poz.opis}</p>{/if}
    <div class="liczby">
      <div><span>Netto / Robotę (średnio)</span><b class="cena">{mon(sr.netto_p)}</b></div>
      <div><span>Ostatni rzut</span><b>{rzut ? mon(rzut.netto_p) : '—'}</b></div>
      <div><span>Brutto tygodniowo</span><b>{mon(sr.brutto_p)}</b></div>
      <div><span>× robotnik</span><b>{pl(sr.x_robotnik, 1)}×</b></div>
    </div>
    {#if rzut}<p class="male drugi" style="margin-top:8px">Z kości {mon(rzut.z_kosci_p)}{rzut.majetny_p ? `, Majętny ${mon(rzut.majetny_p)}` : ''}; brutto {mon(rzut.brutto_p)}.</p>{/if}
  </div>
  <div class="panel">
    <h3>Ile Robót odłożyć <Podpowiedz tekst="Ceny z cennika po Twoich zmianach w Edycji cen. To cena bazowa — u kupca dojdzie marża." /></h3>
    <ul>{#each koszyk as c (c.id)}<li>{c.nazwa} ({mon(c.cena_p)}) — <b>{ileRobot(c.cena_p)}</b></li>{/each}</ul>
    <div class="pasek">
      <label class="pole"><span>Dodaj rzecz</span><input bind:value={dodaj} list="zar-towary" onkeydown={e => e.key === 'Enter' && dodajDoKoszyka()} />
        <datalist id="zar-towary">{#each d.cennik.pozycje as c}<option value={c.nazwa}></option>{/each}</datalist></label>
      <button onclick={dodajDoKoszyka}>Dodaj</button>
    </div>
  </div>
  <div class="panel">
    <h3>Jałmużna (Brąz 0)</h3>
    <p class="male drugi">Test Charyzmy albo Plotkowania: za każde 2 PS 1k10 pensów, podwojone w święto i podczas zarazy.</p>
    <div class="pasek">
      <label class="pole waskie"><span>PS</span><input type="number" min="0" bind:value={psJal} /></label>
      <label style="display:flex;gap:6px;align-items:center"><input type="checkbox" bind:checked={swieto} /> święto / zaraza</label>
      <button onclick={() => (jal = jalmuzna({ ps: psJal, swieto }))}>Rzuć</button>
      {#if jal != null}<b class="cena">{mon(jal) === '—' ? '0 p' : mon(jal)}</b>{/if}
    </div>
  </div>
</div>

<div class="tabela karty">
  <table class="karty">
    <thead><tr><th>Status</th><th>Rzut</th><th class="num">Netto / Robotę</th><th class="num">Brutto / tydz.</th><th class="num">Brutto / rok</th><th class="num">× robotnik</th><th>Kto</th></tr></thead>
    <tbody>
      {#each d.statusy.poziomy as s}
        <tr class:otwarty={s.tier + ' ' + s.lvl === status}>
          <td class="tytul">{s.tier} {s.lvl}</td><td data-l="Rzut">{s.kostka}</td>
          <td class="num" data-l="Netto / Robotę"><span class="cena">{mon(s.netto_p)}</span></td>
          <td class="num" data-l="Brutto / tydz.">{mon(s.brutto_p)}</td><td class="num zwin" data-l="Brutto / rok">{mon(s.brutto_rok)}</td>
          <td class="num" data-l="× robotnik">{pl(s.tyg_robotnika, 1)}×</td><td class="pelna drugi male">{s.opis}</td>
        </tr>
      {/each}
    </tbody>
  </table>
</div>
