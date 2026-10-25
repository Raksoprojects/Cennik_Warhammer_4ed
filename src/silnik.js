// Skarbiec Imperium – silnik obliczeń (bez DOM, bez zależności).
// Wierny port logiki z artefaktu „Skarbiec Imperium” (claude.ai, wersja 2026-09-16)
// + poprawki z zasad domowych kampanii (HR-018, HR-021, HR-024, HR-026).
// Wszystkie kwoty w pensach: 1 ZK = 20 s = 240 p, 1 s = 12 p.
//
// Użycie (przeglądarka lub Node ≥ 18):
//   import * as S from './silnik.js';
//   const dane = { cennik, kupcy, osady, koniunktura, rynek, nazwy, statusy, przedmioty_magiczne };
//   const sklep = S.generujKupca(dane, { kupiec: 'zbrojmistrz', osada: 'miasto', koniunktura: 'wojna', seed: 42 });

export const ZK = 240, S = 12;

/* ------------------------------------------------------------ losowanie */
// mulberry32 – ten sam generator co w artefakcie; ten sam seed = ten sam kupiec.
export function mulberry32(a) {
  return function () {
    a |= 0; a = a + 0x6D2B79F5 | 0;
    let t = Math.imul(a ^ a >>> 15, 1 | a);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}
export function kosci(seed) {
  const rnd = mulberry32(seed);
  const ri = n => Math.floor(rnd() * n);          // 0..n-1
  return {
    rnd, ri,
    k: n => 1 + ri(n),                              // 1kN
    pick: arr => arr[ri(arr.length)],
  };
}
const losowySeed = () => (Math.random() * 1e9) | 0;

/* ------------------------------------------------------------ format */
export function mon(p) {
  p = Math.round(p);
  if (p === 0) return '—';
  const zk = Math.floor(p / ZK), r = p % ZK, s = Math.floor(r / S), pe = r % S, out = [];
  if (zk) out.push(zk + ' ZK');
  if (s) out.push(s + ' s');
  if (pe || !out.length) out.push(pe + ' p');
  return out.join(' ');
}
export function proc(m) { const v = Math.round((m - 1) * 100); return (v > 0 ? '+' : '') + v + '%'; }
export function norm(s) {
  return String(s).toLowerCase().replace(/[ąćęłńóśżź]/g, c => ({ ą: 'a', ć: 'c', ę: 'e', ł: 'l', ń: 'n', ó: 'o', ś: 's', ż: 'z', ź: 'z' })[c]);
}
const clamp = (v, a, b) => v < a ? a : v > b ? b : v;

/* ------------------------------------------------------------ dostęp do danych */
const byId = (arr, id, co) => {
  const x = typeof id === 'object' ? id : arr.find(e => e.id === id);
  if (!x) throw new Error(`Nieznany ${co}: ${id}`);
  return x;
};
const pozycje = d => d.cennik.pozycje;
const kupiecZ = (d, id) => byId(d.kupcy.kupcy, id, 'kupiec');
const osadaZ = (d, id) => byId(d.osady.osady, id, 'osada');
const konZ = (d, id) => byId(d.koniunktura.koniunktury, id, 'koniunktura');
const limitOsady = o => o.limit_p == null ? Infinity : o.limit_p;

export function cenaKoniunktury(kon, kat) { return kon.kategorie[kat]?.cena ?? 1; }
export function popytKoniunktury(kon, kat) { return kon.kategorie[kat]?.popyt ?? 0; }

export function wTowarze(d, c) {
  if (!(c.cena_p > 0)) return false;
  // v3: handluje się tylko tym, co ma typ „towar". Nocleg, usługa i nieruchomość
  // mają ceny już detaliczne — marża kupca liczyłaby narzut drugi raz.
  const typy = d.rynek.asortyment.wykluczone_typy;
  if (typy && c.typ) return !typy.includes(c.typ);
  return !d.rynek.asortyment.wykluczone_kategorie.includes(c.kat);   // dane sprzed v3
}

// v3: wieś ma limit ceny i wymóg Dostępności Powszechnej, ale żywy inwentarz
// i podstawowa żywność są z nich wyjęte — wieś jest właśnie tym miejscem, gdzie kupuje się krowę.
function omijaLimitWsi(lok, c) {
  const w = lok.limit_omijaja_podtypy;
  return !!(w && c.podtyp && c.podtyp.some(p => w.includes(p)));
}

/* ------------------------------------------------------------ rynek: zapas, popyt, ilość */
export function zapasZRzutu(d, rzut) { return d.rynek.zapas.progi.find(p => rzut <= p.do).id; }
export function przesunieciePopytu(d, rzut) { return d.rynek.popyt.przesuniecie.find(p => rzut <= p.do).zmiana; }
export function mnoznikRynku(d, zapas, popyt) { return d.rynek.macierz_zapas_x_popyt.wartosci[zapas][popyt]; }

export function ilosc(d, ri, cena, zapas) {
  const prog = d.rynek.ilosc.progi_p.find(p => p.ponizej == null || cena < p.ponizej);
  const base = prog.baza_min + (prog.baza_losowa ? ri(prog.baza_losowa) : 0);
  if (zapas === 0) return Math.ceil(base * 2.5);
  if (zapas === 2) return Math.max(1, Math.ceil(base * 0.15));
  if (zapas === 3) return 0;
  return base;
}

/* ------------------------------------------------------------ generator kupca */
// Pozycje z kategorii `kats`, które kupiec może mieć na stanie w tej osadzie (limit ceny, branże kupca).
// v6b: kupiec.branze = { kategoria: [tagi] } — z tej kategorii tylko pozycje z jednym z tagów (cennik → branze).
export function pulaTowaru(d, { kupiec, osada, kats, stosujDostepnosc = true }) {
  const kup = kupiecZ(d, kupiec), lok = osadaZ(d, osada);
  const cap = Math.min(kup.limit_p, limitOsady(lok));
  return pozycje(d).filter(c => {
    if (!kats.includes(c.kat) || !wTowarze(d, c)) return false;
    const br = stosujDostepnosc && kup.branze?.[c.kat];
    if (br && !c.branze?.some(t => br.includes(t))) return false;
    if (omijaLimitWsi(lok, c)) return true;                     // krowa we wsi mimo limitu
    // v4: limit liczony od ceny bazowej (cena_ref_p), żeby poziom cen nie wycinał asortymentu
    if ((c.cena_ref_p ?? c.cena_p) > cap) return false;
    return true;
  });
}

// v6b: szansa, że rzecz jest w sprzedaży (PG s. 290: Dostępność × wielkość osady). Towar krasnoludzki u krasnoluda
// jest Powszechny, u kupca innej rasy szansa × rynek.dostepnosc.obce_pochodzenie. Brak tabeli w danych = 1.
const WLASNE_POCHODZENIE = { krasnolud: 'krasnoludzkie', elf: 'elfie' };
export function szansaDostepnosci(d, { kupiec, osada, pozycja }) {
  const T = d.rynek.dostepnosc;
  if (!T) return 1;
  if (pozycja.pochodzenie && WLASNE_POCHODZENIE[kupiec.rasa] === pozycja.pochodzenie) return 1;
  const p = T.tabela[osada.dostepnosc ?? 'miasto']?.[pozycja.dostepnosc ?? 'Powszechna'] ?? 1;
  return p * (pozycja.pochodzenie ? (T.obce_pochodzenie ?? 1) : 1);
}

// opcje.stosujDostepnosc: branże kupca i test Dostępności (v6b). false = zachowanie 1:1 z artefaktem.
/** @param {any} d @param {Record<string, any>} [opcje] */
export function generujKupca(d, { kupiec, osada, koniunktura = 'normalna', seed = losowySeed(), stosujDostepnosc = true, osobowosc = true, charaktery = null } = {}) {
  const kup = kupiecZ(d, kupiec), lok = osadaZ(d, osada), kon = konZ(d, koniunktura);
  const { rnd, ri, k, pick } = kosci(seed);
  const cap = Math.min(kup.limit_p, limitOsady(lok));
  const pula = kats => pulaTowaru(d, { kupiec: kup, osada: lok, kats, stosujDostepnosc });

  // v6b: test Dostępności — osobny strumień, więc rzuty asortymentu idą w tej samej kolejności.
  const dostRnd = kosci((seed ^ 0x2545f491) >>> 0);
  const dostepny = c => !stosujDostepnosc || omijaLimitWsi(lok, c) || dostRnd.rnd() < szansaDostepnosci(d, { kupiec: kup, osada: lok, pozycja: c });
  const wybor = [], uzyte = new Set();
  for (const c of pula(kup.rdzen)) if (rnd() < d.rynek.asortyment.rdzen_szansa && dostepny(c)) { uzyte.add(c.id); wybor.push(c); }
  for (const kat of kup.boczne) {
    const p = pula([kat]); const ile = Math.min(2 + ri(4), p.length);
    let n = 0, prob = 0;
    while (n < ile && prob < 200) {
      prob++;
      const c = p[ri(p.length)];
      if (uzyte.has(c.id)) continue;
      uzyte.add(c.id);
      if (!dostepny(c)) continue;
      wybor.push(c); n++;
    }
  }
  wybor.sort((a, b) => b.cena_p - a.cena_p);           // stabilne sortowanie

  const imie = pick(d.nazwy.imiona) + ' ' + pick(d.nazwy.nazwiska);
  const dziwactwo = pick(d.nazwy.dziwactwa);
  // v5: osobny strumień losowania na kaprys kupca — nie przesuwa rzutów zapasu i popytu,
  // więc ten sam seed daje ten sam asortyment, ilości i rynek co przed v5.
  const kaprysRnd = kosci((seed ^ 0x5bd1e995) >>> 0);
  // v5.2: majątek kupca. Towar na stanie i gotówka w tygodniach brutto jego Statusu (kupcy.json → towar_tyg, gotowka_tyg).
  // Budżet towaru dzieli się na pozycje (rdzeń waży 2, boczne 1) i ogranicza liczbę sztuk: kramarz nie ma 47 namiotów.
  const mjt = osobowosc ? majatekKupca(d, kup, seed) : null;
  const jakRnd = kosci((seed ^ 0x68e31da4) >>> 0);
  // v6c: postać kupca (charakter, motywacja, cecha kupiecka…) i towar trefny — osobne strumienie losowania.
  const postac = osobowosc ? generujPostac(d, kosci((seed ^ 0x3c6ef372) >>> 0), { charaktery }) : null;
  const E = postac?.cecha?.efekt ?? {};
  if (mjt && E.gotowka) mjt.gotowka_p = Math.round(mjt.gotowka_p * E.gotowka);
  const trefRnd = kosci((seed ^ 0x1b873593) >>> 0);
  const wagi = wybor.map(c => kup.rdzen.includes(c.kat) ? 2 : 1), sumaWag = wagi.reduce((a, b) => a + b, 0) || 1;
  const towar = wybor.map((c, ix) => {
    const rz = k(10), zapas = zapasZRzutu(d, rz);
    const rp = k(10);
    const popyt = clamp(d.rynek.popyt.start + popytKoniunktury(kon, c.kat) + przesunieciePopytu(d, rp), 0, 2);
    const mKon = cenaKoniunktury(kon, c.kat), mRynek = mnoznikRynku(d, zapas, popyt);
    const rk = osobowosc ? kaprysRnd.k(10) : null;
    const os = osobowosc ? osobowoscKupca(d, kup, c, E.kaprys === false ? null : rk) : { preferencja: 1, kaprys: 1, rzut: null, mnoznik: 1 };
    const mnoznik = kup.marza * os.mnoznik * lok.mnoznik * mKon * mRynek * (E.ceny ?? 1);
    // v6: egzemplarz z Zaletami / Wadami przedmiotu (osobny strumień losowania, tylko z osobowością kupca).
    const jak = osobowosc ? jakoscLosowa(d, kup, c, jakRnd) : null;
    const baza = jak ? Math.round(c.cena_p * jak.mnoznik) : c.cena_p;
    const cena = baza * mnoznik;
    let sztuk = ilosc(d, ri, c.cena_ref_p ?? c.cena_p, zapas);   // v4: ilość od ceny bazowej
    if (mjt && mjt.towar_p != null && sztuk > 1) {
      const budzet = mjt.towar_p * wagi[ix] / sumaWag * (zapas === 0 ? 1.5 : 1);
      sztuk = Math.min(sztuk, Math.max(1, Math.floor(budzet / c.cena_p)));
    }
    const skupU = Math.max(d.rynek.skup.minimum, kup.skup + (popyt === 2 ? d.rynek.skup.popyt_wysoki : popyt === 0 ? d.rynek.skup.popyt_niski : 0)) * (E.skup ?? 1);
    const cenaP = Math.round(cena);
    const trefny = osobowosc ? trefnyLosowy(d, kup, c, trefRnd, E) : null;
    const min = cenaMinimalna(d, { kupiec: kup, pozycja: jak ? { ...c, cena_p: baza } : c, osada: lok, koniunktura: kon, mRynek, cena_p: cenaP });
    return {
      id: c.id, nazwa: c.nazwa, kat: c.kat, sztuk,
      cena_raw_p: c.cena_raw_p ?? null,                              // v5.1: cena z podręcznika, do porównania
      cechy: jak?.cechy ?? null, jakosc: jak ? { nazwa: jak.nazwa, mnoznik: jak.mnoznik } : null, cena_cennik_p: c.cena_p, trefny,
      cena_wytworcy_p: baza, mnoznik, cena_p: cenaP, skup_p: Math.round(cena * skupU),
      skup_ponad_gotowke: !!(mjt && mjt.gotowka_p != null && cena * skupU > mjt.gotowka_p),
      koszt_p: min.koszt_p, cena_min_p: min.cena_min_p, wyprzedaz: min.wyprzedaz,
      zapas, zapas_nazwa: d.rynek.zapas.progi[zapas].nazwa, popyt, popyt_nazwa: d.rynek.popyt.nazwy[popyt],
      rzuty: { zapas: rz, popyt: rp, kaprys: os.rzut },
      skladowe: { marza: kup.marza, preferencja: os.preferencja, kaprys: os.kaprys, osada: lok.mnoznik, koniunktura: mKon, rynek: mRynek, charakter: E.ceny ?? 1 },
    };
  });
  // v5.2: rzecz, której jedna sztuka kosztuje ponad 4× budżet tej pozycji, jest poza zasięgiem sklepu — będzie na zamówienie.
  // Filtr po losowaniach, więc kolejność rzutów się nie zmienia.
  if (mjt && mjt.towar_p != null) {
    const zostaw = towar.filter((t, ix) => t.cena_wytworcy_p <= 4 * mjt.towar_p * wagi[ix] / sumaWag);
    towar.length = 0; towar.push(...zostaw);
  }
  const wartosc_towaru_p = towar.reduce((s, t) => s + t.sztuk * t.cena_wytworcy_p, 0);
  return { seed, imie, dziwactwo, postac, kupiec: kup, osada: lok, koniunktura: kon, limit_p: cap, towar,
    gotowka_p: mjt?.gotowka_p ?? null, budzet_towaru_p: mjt?.towar_p ?? null, wartosc_towaru_p,
    etykiety: { osada: etykietaOsady(lok), koniunktura: etykietaKoniunktury(d, kon) } };
}

/* ------------------------------------------------------------ v6c: postać kupca */
// data/postacie.json: charakter (dobry / neutralny / zly, wagi), wygląd (2 z 4 grup), znak rozpoznawczy, manieryzm,
// Motywacja, cecha kupiecka (z efektem), potrzeba, sekret, dziwactwo. Pozycje z polem charakter tylko dla tego charakteru;
// bez pola — dla każdego. charaktery = lista dozwolonych (domyślnie wszystkie). Brak danych = null.
export function generujPostac(d, r, { charaktery = null } = {}) {
  const P = d.postacie;
  if (!P) return null;
  const dozwolone = Object.keys(P.charaktery).filter(c => !charaktery || charaktery.includes(c));
  const lista = dozwolone.length ? dozwolone : Object.keys(P.charaktery);
  let los = r.rnd() * lista.reduce((s, c) => s + P.charaktery[c].waga, 0), charakter = lista[0];
  for (const c of lista) { los -= P.charaktery[c].waga; if (los < 0) { charakter = c; break; } }
  const pasuje = arr => { const p = arr.filter(x => !x.charakter || x.charakter === charakter); return p.length ? p : arr; };
  const wybierz = arr => arr[r.ri(arr.length)];
  const grupy = Object.keys(P.wyglad), g1 = r.ri(grupy.length), g2 = (g1 + 1 + r.ri(grupy.length - 1)) % grupy.length;
  return {
    charakter,
    wyglad: [wybierz(P.wyglad[grupy[g1]]), wybierz(P.wyglad[grupy[g2]])],
    znak: wybierz(P.znaki).tekst,
    manieryzm: wybierz(P.manieryzmy),
    motywacja: wybierz(pasuje(P.motywacje)),
    cecha: wybierz(pasuje(P.cechy_kupieckie)),
    potrzeba: wybierz(pasuje(P.potrzeby)).tekst,
    sekret: wybierz(pasuje(P.sekrety)).tekst,
    dziwactwo: wybierz(P.dziwactwa),
  };
}

/* ------------------------------------------------------------ v6c: towar trefny */
// Szansa: kupcy.json → trefne (domyślnie rynek.trefne.domyslna_szansa); cecha kupca: trefne 0 = nigdy, wyższa = co najmniej tyle.
// Rodzaj losowany z pasujących (kategoria albo tagi branż), wagi z kupcy.json → trefne_wagi albo rynek.trefne.wagi.
// Zwraca { rodzaj, nazwa, opis, swiadomy, wartosc, test } albo null. Rzutów tyle samo dla każdej pozycji.
export function trefnyLosowy(d, kup, c, r, E = {}) {
  const T = d.rynek.trefne;
  const a = r.rnd(), b = r.rnd(), s = r.rnd(), w = r.rnd();
  if (!T || E.trefne === 0) return null;
  const szansa = Math.max(kup.trefne ?? T.domyslna_szansa, E.trefne ?? 0);
  if (a >= szansa) return null;
  const wagi = kup.trefne_wagi ?? T.wagi;
  const pasuje = Object.entries(T.rodzaje).filter(([id, R]) => (wagi[id] ?? 0) > 0 &&
    (!R.kategorie && !R.tagi || R.kategorie?.includes(c.kat) || c.branze?.some(t => R.tagi?.includes(t))));
  if (!pasuje.length) return null;
  let los = b * pasuje.reduce((t, [id]) => t + wagi[id], 0), [id, R] = pasuje[0];
  for (const p of pasuje) { los -= wagi[p[0]]; if (los < 0) { [id, R] = p; break; } }
  const skala = R.wartosc === 'skala' ? T.skala_oszustwa[Math.floor(s * T.skala_oszustwa.length)] : null;
  return { rodzaj: id, nazwa: R.nazwa, opis: R.opis, swiadomy: !!E.oszust || w < (T.swiadomosc[id] ?? 0.5),
    wartosc: skala ? 1 - skala.udzial : R.wartosc,
    test: skala ? `Test Wyceny: ${skala.test} (oszukane ${Math.round(skala.udzial * 100)}% towaru)` : R.test_opis };
}

/* ------------------------------------------------------------ v6: losowa jakość towaru */
// kupcy.json → jakosc: { zalety, wady } = szansa na pozycję z kategorii rynek.jakosc.kategorie. Rzuty: zalety, wady, 1k10 na liczbę,
// potem wybór cech. Poręczny i Nieporęczny tylko dla rzeczy z Obciążeniem ≥ 1 (PG: małe szpargały nie mają tej Wady).
export function jakoscLosowa(d, kup, c, r) {
  const J = d.rynek.jakosc, sz = kup.jakosc_kat?.[c.kat] ?? kup.jakosc;   // v6b: jakość osobno dla kategorii
  if (!sz || !J.kategorie?.includes(c.kat) || c.branze?.some(t => J.bez_jakosci?.includes(t))) return null;
  const a = r.rnd(), b = r.rnd(), n = J.losowanie.ile.find(x => r.k(10) <= x.do).n;
  const lista = a < (sz.zalety ?? 0) ? J.zalety : b < (sz.wady ?? 0) ? J.wady : null;
  if (!lista) return null;
  const pula = lista.filter(z => !/porę/i.test(z.nazwa) || (c.obc ?? 0) >= 1);
  const cechy = {};
  for (let i = 0; i < n; i++) {
    const z = pula[r.ri(pula.length)];
    if (cechy[z.nazwa] && !z.wielokrotna) continue;
    cechy[z.nazwa] = (cechy[z.nazwa] ?? 0) + 1;
  }
  return jakoscZ(d, cechy);
}

/* ------------------------------------------------------------ v5.2: majątek kupca */
// Gotówka: tygodnie brutto Statusu × gotowka_tyg × (0,5 … 1,4 z rzutu 1k10). Towar: × towar_tyg (bez rzutu).
// Osobny strumień losowania (seed ^ 0x27d4eb2f) — nie przesuwa rzutów sklepu. Brak pól w kupcy.json = null (bez limitu).
export function majatekKupca(d, kup, seed) {
  const brutto = sredniDochod(d, kup.status).brutto_p;
  const { k } = kosci((seed ^ 0x27d4eb2f) >>> 0);
  const rzut = k(10);
  return {
    brutto_tyg_p: brutto,
    towar_p: kup.towar_tyg != null ? Math.round(brutto * kup.towar_tyg) : null,
    gotowka_p: kup.gotowka_tyg != null ? Math.round(brutto * kup.gotowka_tyg * (0.4 + rzut / 10)) : null,
    rzut_gotowki: rzut,
  };
}

/* ------------------------------------------------------------ v5: osobowość kupca */
// Preferencja: specjalista bierze za swój rdzeń mniej (kupuje hurtem, zna towar), za boczny asortyment więcej.
// Kupiec może nadpisać to per kategoria w kupcy.json → preferencje: { "Pancerze": 1.2 }.
// Kaprys: 1k10 na pozycję z tabeli rynek.kaprys.progi (domyślnie ×0,9 … ×1,1).
// Razem preferencja × kaprys mieści się w rynek.kaprys.granice — „zachowując rozsądek”.
// Brak rynek.preferencje / rynek.kaprys (dane sprzed v5) = 1, czyli zachowanie jak dawniej.
export function osobowoscKupca(d, kup, c, rzut) {
  const P = d.rynek.preferencje, K = d.rynek.kaprys;
  let preferencja = 1;
  if (kup.preferencje && c.kat in kup.preferencje) preferencja = kup.preferencje[c.kat];
  else if (P) preferencja = kup.rdzen.includes(c.kat) ? (P.rdzen ?? 1) : kup.boczne.includes(c.kat) ? (P.boczne ?? 1) : 1;
  let kaprys = 1;
  if (K && rzut != null) kaprys = K.progi.find(p => rzut <= p.do).mnoznik;
  const [lo, hi] = K?.granice ?? [0, Infinity];
  return { preferencja, kaprys, rzut: K ? rzut : null, mnoznik: clamp(preferencja * kaprys, lo, hi) };
}

/* ------------------------------------------------------------ v5: cena minimalna */
// Koszt nabycia = cena z cennika × osada × koniunktura (tyle kupiec zapłacił wytwórcy na miejscu).
// Wytwórca (kategoria w kupiec.robota) liczy własny koszt: × rynek.cena_minimalna.koszt_wlasny.
// Cena minimalna = koszt × narzut_min (zwykle +5%), a przy wyprzedaży (rynek < 1) × wyprzedaz (ze stratą).
// Jeśli kupiec już żąda mniej — nie schodzi niżej niż jego cena.
export function cenaMinimalna(d, { kupiec, pozycja, osada, koniunktura, mRynek = 1, cena_p }) {
  const M = d.rynek.cena_minimalna ?? { narzut_min: 1, wyprzedaz: 1, koszt_wlasny: 1 };
  const robi = robiTo(kupiec, pozycja);
  const koszt = pozycja.cena_p * osada.mnoznik * cenaKoniunktury(koniunktura, pozycja.kat) * (robi ? M.koszt_wlasny : 1);
  const wyprzedaz = mRynek < 1;
  const prog = Math.round(koszt * (wyprzedaz ? M.wyprzedaz : M.narzut_min));
  return { koszt_p: Math.round(koszt), cena_min_p: Math.min(cena_p, prog), wyprzedaz, wlasny_wyrob: !!robi };
}

/* ------------------------------------------------------------ v5: etykiety modyfikatorów */
// „Altdorf (+30%)”
export function etykietaOsady(lok) { return `${lok.nazwa} (${lok.mnoznik === 1 ? 'ceny bez zmian' : proc(lok.mnoznik)})`; }
// „Wojna (Broń biała, Broń zasięgowa, Amunicja, Pancerze +80% · Jedzenie, picie, nocleg +30% · reszta +5% · czynsz +30%)”
// krotko: true → nazwy kategorii ze słownika koniunktura.skroty („Wojna (broń, strzelecka, amunicja, pancerze +80% · …)”) — do list wyboru.
export function etykietaKoniunktury(d, kon, { krotko = false } = {}) {
  const kats = d.koniunktura.kategorie ?? Object.keys(kon.kategorie);
  const sk = krotko ? (d.koniunktura.skroty ?? {}) : {};
  const grupy = new Map();
  for (const k of kats) { const m = cenaKoniunktury(kon, k); grupy.set(m, [...(grupy.get(m) ?? []), sk[k] ?? k]); }
  const czynsz = kon.czynsz?.mnoznik ?? 1;
  const czesci = [];
  if (grupy.size === 1) {
    const [m] = grupy.keys();
    czesci.push(m === 1 ? 'ceny bez zmian' : `wszystko ${proc(m)}`);
  } else {
    // najliczniejsza grupa = „reszta”
    const reszta = [...grupy.entries()].sort((a, b) => b[1].length - a[1].length)[0][0];
    for (const [m, ks] of [...grupy.entries()].sort((a, b) => b[0] - a[0])) if (m !== reszta) czesci.push(`${ks.join(', ')} ${proc(m)}`);
    czesci.push(reszta === 1 ? 'reszta bez zmian' : `reszta ${proc(reszta)}`);
  }
  if (czynsz !== 1) czesci.push(`czynsz ${proc(czynsz)}`);
  return `${kon.nazwa} (${czesci.join(' · ')})`;
}
// Jedna kategoria: „Pancerze +80%” albo „bez zmian”.
export function modyfikatorKoniunktury(kon, kat) { const m = cenaKoniunktury(kon, kat); return m === 1 ? 'bez zmian' : proc(m); }

/* ------------------------------------------------------------ zamówienie na miarę */
export function znajdzPozycje(d, q) {
  const n = norm(String(q).trim()); if (!n) return null;
  const pula = pozycje(d).filter(c => wTowarze(d, c));
  return pula.find(c => norm(c.nazwa) === n)
    || pula.filter(c => norm(c.nazwa).includes(n)).sort((a, b) => a.nazwa.length - b.nazwa.length)[0]
    || null;
}
// v6: kupiec robi rzeczy ze swoich kategorii (robota) i pojedyncze pozycje spoza nich (robota_pozycje, np. wozy u kowala).
export const robiTo = (kup, c) => !!(kup.robota?.includes(c.kat) || kup.robota_pozycje?.includes(c.id));
export function ktoRobi(d, kat, id = null) {
  let m = d.kupcy.kupcy.filter(k => k.robota.includes(kat) || (id && k.robota_pozycje?.includes(id)));
  if (!m.length) m = d.kupcy.kupcy.filter(k => k.rdzen.includes(kat));
  return m;
}
// material: true — zamawiający daje materiał (v6: wieś składa się na wóz i daje drewno). Tylko u wytwórcy;
// płaci rynek.zamowienie.material_wlasny ceny (robociznę). Termin bez zmian — robota trwa tyle samo.
/** @param {any} d @param {Record<string, any>} opcje — jakosc: id opcji albo cechy { Wytrzymały: 2 } */
export function wycenZamowienie(d, { kupiec, osada, koniunktura = 'normalna', przedmiot, jakosc = 'zwykla', material = false, seed = losowySeed() }) {
  const kup = kupiecZ(d, kupiec), lok = osadaZ(d, osada), kon = konZ(d, koniunktura);
  const c = typeof przedmiot === 'object' ? przedmiot : (pozycje(d).find(x => x.id === przedmiot) || znajdzPozycje(d, przedmiot));
  if (!c || !wTowarze(d, c)) return { status: 'brak_w_cenniku' };   // czynsze i usługi się nie zamawia
  const jak = jakoscZ(d, jakosc);
  const robi = robiTo(kup, c);
  const handluje = kup.rdzen.includes(c.kat) || kup.boczne.includes(c.kat);
  if (!robi && !handluje) return { status: 'odmowa', przedmiot: c, odsyla_do: ktoRobi(d, c.kat, c.id).map(k => k.nazwa) };
  // v6b: rzecz, której w tej osadzie zwykle nie ma (Dostępność), trwa dłużej i kosztuje więcej; egzotyk we wsi — odmowa.
  const RZ = d.rynek.dostepnosc?.zamowienie, szansa = szansaDostepnosci(d, { kupiec: kup, osada: lok, pozycja: c });
  const rzadkosc = RZ && szansa < (RZ.prog ?? 1) ? (c.dostepnosc ?? 'Powszechna') : null;
  if (rzadkosc && lok.dostepnosc === 'wioska' && RZ.wioska_bez?.includes(rzadkosc))
    return { status: 'odmowa', przedmiot: c, odsyla_do: ['kupca w mieście'], powod: RZ.wioska_opis };
  const Z = d.rynek.zamowienie, { ri } = kosci(seed);
  const baza = c.cena_p * jak.mnoznik;
  const narzut = (robi ? Z.narzut_robota : Z.narzut_sprowadzenie) * (rzadkosc ? RZ.narzut[rzadkosc] ?? 1 : 1);
  const mKon = cenaKoniunktury(kon, c.kat);
  const mnoznik = kup.marza * lok.mnoznik * mKon * narzut;
  const cena = baza * mnoznik;
  const termin = cena < 240 ? (1 + ri(5)) + ' dni' : cena < 2400 ? (1 + ri(3)) + ' tygodni'
    : cena < 12000 ? (4 + ri(6)) + ' tygodni' : (3 + ri(4)) + ' miesięcy';
  const cap = Math.min(kup.limit_p, limitOsady(lok));
  const mat = material && robi ? (Z.material_wlasny ?? 1) : 1, razem = cena * mat;
  return {
    status: robi ? 'wykonuje' : 'sprowadza', przedmiot: c, jakosc: jak, material: mat < 1 ? mat : null,
    rzadkosc: rzadkosc ? { dostepnosc: rzadkosc, szansa, termin_tyg: RZ.termin_tyg[rzadkosc] ?? 0, narzut: RZ.narzut[rzadkosc] ?? 1 } : null,
    baza_p: baza, skladowe: { marza: kup.marza, osada: lok.mnoznik, koniunktura: mKon, narzut }, mnoznik,
    cena_p: Math.round(razem), zaliczka_p: Math.round(razem * Z.zaliczka), termin,
    calosc_z_gory: razem > cap * 2, test_rzemiosla: (jak.zalety ?? 0) > 0 || jak.mnoznik >= 2, max_targowanie: d.rynek.targowanie.max_zamowienie,
  };
}

/* ------------------------------------------------------------ targowanie (HR-024) */
// ps = Poziomy Sukcesu gracza w Przeciwstawnym Teście (ujemne = wygrał handlarz → bez zmian).
// Dolna granica: cena z cennika × jakość; jeśli kupiec już sprzedaje taniej – nie schodzi dalej.
export function modyfikatorTargowania({ zapas, popyt }) {
  if (zapas === 0) return 10;
  if (zapas === 2 && popyt === 2) return -20;
  return 0;
}
// v5: jeśli podasz cena_min_p (z generujKupca), to ona jest dolną granicą zamiast ceny z cennika.
// v6b: talent = dodatkowy upust (np. Żyłka Handlowa, 0,04 = −4%) ponad limit z PS, gdy gracz wygrał test (PS > 0).
// Cena minimalna kupca nadal obowiązuje.
/** @param {any} d @param {Record<string, any>} opcje */
export function targuj(d, { cena_p, cena_cennik_p, cena_min_p, ps, zamowienie = false, talent = 0 }) {
  const T = d.rynek.targowanie;
  const upust = clamp(Math.max(0, ps) * T.za_ps, 0, zamowienie ? T.max_zamowienie : T.max) + (ps > 0 ? Math.max(0, talent) : 0);
  const granica = Math.min(cena_p, cena_min_p ?? cena_cennik_p);
  const po = Math.max(granica, Math.round(cena_p * (1 - upust)));
  return { cena_p: po, upust: 1 - po / cena_p, granica_p: granica };
}

/* ------------------------------------------------------------ dochód (HR-018, HR-021, HR-024) */
export function drabina(d) { return d.statusy.poziomy.map(s => s.tier + ' ' + s.lvl); }
export function parsujStatus(txt) {
  const m = /^(Brąz|Srebro|Złoto)\s+(\d+)/.exec(String(txt).trim());
  if (!m) throw new Error('Status w formacie „Srebro 3”: ' + txt);
  return { tier: m[1], lvl: +m[2] };
}
// ryzykowny: rzut jak za Status o 2 szczeble wyższy na drabinie (Brąz 0–5, Srebro 1–5, Złoto 1–7).
export function rzutDochodu(d, { status, majetny = 0, ryzykowny = false, instytucja = false, seed = losowySeed() }) {
  let { tier, lvl } = parsujStatus(status);
  if (ryzykowny) {
    const D = drabina(d), i = Math.min(D.length - 1, D.indexOf(tier + ' ' + lvl) + 2);
    ({ tier, lvl } = parsujStatus(D[i]));
  }
  const W = d.statusy.wzory[tier], { k } = kosci(seed);
  const ile = W.kosci === '2N' ? 2 * lvl : lvl;
  let suma = 0; for (let i = 0; i < ile; i++) suma += k(W.k);
  let maj = 0; for (let i = 0; i < majetny; i++) maj += k(d.statusy.majetny.k);
  const netto = (suma + maj) * W.moneta_p * (instytucja ? 10 : 1);
  return { status_rzutu: tier + ' ' + lvl, netto_p: netto, z_kosci_p: suma * W.moneta_p, majetny_p: maj * W.moneta_p,
    brutto_p: netto * d.statusy.brutto_mnoznik, uwaga: ryzykowny ? 'Test Umiejętności: porażka = ½, porażka z dubletem = 0' : undefined };
}
export function sredniDochod(d, status, majetny = 0) {
  const { tier, lvl } = parsujStatus(status), W = d.statusy.wzory[tier];
  const ile = W.kosci === '2N' ? 2 * lvl : lvl;
  const netto = (ile * (W.k + 1) / 2 + majetny * 3) * W.moneta_p;
  return { netto_p: netto, brutto_p: netto * 5, brutto_rok_p: netto * 5 * 52, x_robotnik: netto * 5 / d.statusy.robotnik_brutto_p };
}
export function jalmuzna({ ps, swieto = false, seed = losowySeed() }) {
  const { k } = kosci(seed); let p = 0;
  for (let i = 0; i < Math.floor(Math.max(0, ps) / 2); i++) p += k(10);
  return p * (swieto ? 2 : 1);
}

/* ------------------------------------------------------------ magiczne przedmioty (HR-026) */
// rodzaj: bron|pancerz|tarcza → cena_p × 50 × właściwości × 2^zalety; strzala → cena_p × 30
// zwoj|rozdzka|pierscien → PZ (0 liczy się jak 0,4) × ZK za PZ, bez Zalet.
export function cenaMagiczna(d, { rodzaj, cena_p = 0, wlasciwosci = 1, zalety = 0, pz = 0 }) {
  const W = d.przedmioty_magiczne.wzory[rodzaj];
  if (!W) return null;                              // kostur, talizman: cena wg twórcy
  if (W.zk_za_pz) return Math.round((pz === 0 ? d.przedmioty_magiczne.pz0_jak : pz) * W.zk_za_pz * ZK);
  const zal = 2 ** zalety;
  return W.za ? cena_p * W.mnoznik * wlasciwosci * zal : cena_p * W.mnoznik * zal;
}

/* ------------------------------------------------------------ jakość */
export function cenaZJakoscia(d, cena_p, jakosc) { return cena_p * jakoscZ(d, jakosc).mnoznik; }
// v6: jakość jako id gotowej opcji („wysmienita”) albo jako cechy przedmiotu { Wytrzymały: 2, Wyśmienity: 2, Tandetny: 1 }.
// PG s. 292: każda Zaleta przedmiotu ×2 (Wyśmienity i Wytrzymały można brać kilka razy — każdy poziom to Zaleta),
// każda Wada ×½. Cena w cenniku to wariant podstawowy, bez Zalet i Wad przedmiotu (cechy broni są już w niej).
// v6b (MG): mnożniki z danych — rynek.jakosc.za_zalete ×1,6, za_wade ×0,6. Niezwykłe cechy („Zaleta broni: Szybka”,
// „Bez Wady: Tępa”, prefiksy z rynek.jakosc.niezwykle) liczą się jak Zaleta przedmiotu.
export function jakoscZ(d, jakosc) {
  if (jakosc == null || typeof jakosc === 'string') return byId(d.rynek.jakosc.opcje, jakosc ?? 'zwykla', 'jakość');
  const J = d.rynek.jakosc, N = J.niezwykle, nazwy = [];
  let zalety = 0, wady = 0;
  for (const [nazwa, ile] of Object.entries(jakosc)) {
    const n = Math.max(0, ile | 0); if (!n) continue;
    if (N && (nazwa.startsWith(N.prefiks_zalety) || nazwa.startsWith(N.prefiks_bez_wady))) zalety += n;
    else if (J.zalety.some(z => z.nazwa === nazwa)) zalety += n;
    else if (J.wady.some(z => z.nazwa === nazwa)) wady += n;
    else throw new Error('Nieznana Zaleta ani Wada przedmiotu: ' + nazwa);
    nazwy.push(n > 1 ? `${nazwa} ${n}` : nazwa);
  }
  return { id: 'cechy', nazwa: nazwy.join(', ') || 'Zwykła', zalety, wady, cechy: jakosc,
    mnoznik: (J.za_zalete ?? 2) ** zalety * (J.za_wade ?? 0.5) ** wady };
}

/* ------------------------------------------------------------ czynsz (v3) */
// Czynsz ma własny mnożnik koniunktury, niezależny od cen towarów: po zarazie
// komorne leci w dół (puste izby), w oblężeniu i w kryzysie mieszkaniowym w górę.
export function mnoznikCzynszu(d, koniunkturaId) {
  const k = d.koniunktura.koniunktury.find(x => x.id === koniunkturaId);
  return k?.czynsz?.mnoznik ?? 1;
}
export function czynsz(d, { kwatera, okres = 'miesiac', osada, koniunktura = 'normalna' }) {
  const k = d.czynsze.najem.find(x => x.kwatera === kwatera || norm(x.kwatera).includes(norm(kwatera)));
  if (!k) return null;
  const baza = k[okres + '_p'];
  if (baza == null) return null;
  const mOs = osada ? osadaZ(d, osada).mnoznik : 1;
  const mKon = mnoznikCzynszu(d, koniunktura);
  return {
    kwatera: k.kwatera, okres, baza_p: baza,
    skladowe: { osada: mOs, koniunktura: mKon }, mnoznik: mOs * mKon,
    cena_p: Math.round(baza * mOs * mKon),
  };
}

/* ------------------------------------------------------------ poziom cen (v4) */
// Cennik trzyma cenę bazową (cena_ref_p) i klasę cenową (klasa). Preset to mnożnik na klasę.
// Zwraca NOWY obiekt cennika: cena_p = cena_ref_p × mnożnik klasy (× premia znaku stanu),
// pełne naczynia liczone jako naczynie + zawartość. Limity i ilości w generatorze dalej idą od cena_ref_p.
export function zastosujPreset(cennik, klasyCenowe, nazwaPresetu) {
  const pr = klasyCenowe.presety[nazwaPresetu];
  if (!pr) throw new Error('Nieznany preset: ' + nazwaPresetu);
  const znak = new Set(klasyCenowe.znak_stanu);
  const ladna = p => p < 24 ? Math.max(1, Math.round(p)) : p < 240 ? Math.round(p / 6) * 6
    : p < 2400 ? Math.round(p / 12) * 12 : Math.round(p / 60) * 60;
  const poz = cennik.pozycje.map(c => {
    const baza = c.cena_ref_p ?? c.cena_p;
    let m = pr.mnozniki[c.klasa] ?? 1;
    if (znak.has(c.id)) m *= pr.premia_znak_stanu ?? 1;
    return { ...c, cena_ref_p: baza, cena_p: ladna(baza * m) };
  });
  const P = Object.fromEntries(poz.map(c => [c.id, c]));
  const kpoj = pr.mnozniki.codzienne ?? 1;
  if (P['butelka-wina'] && P['butelka']) P['butelka-wina'].cena_p = P['butelka'].cena_p + 24;
  if (P['beczulka-piwa-10-l']) P['beczulka-piwa-10-l'].cena_p = ladna(18 + 13 * kpoj);
  if (P['sledzie-beczka'] && P['beczka-145-l'])
    P['sledzie-beczka'].cena_p = ladna(P['sledzie-beczka'].cena_ref_p - P['beczka-145-l'].cena_ref_p + P['beczka-145-l'].cena_p);
  return { ...cennik, wersja: (cennik.wersja || '') + '+' + nazwaPresetu, pozycje: poz };
}

/* ------------------------------------------------------------ v5: ustawienia MG na żywo */
// Ustawienia (data/ustawienia.json albo panel MG → localStorage) nakładają się na dane bez ich niszczenia.
// Zwraca NOWY obiekt danych. Wymaga d.klasy (data/klasy_cenowe.json). Format: docs/AGENT_BRIEF.md, rozdz. „Ustawienia”.
//   preset            nazwa presetu z klasy_cenowe.presety (domyślnie klasy_cenowe.domyslny)
//   mnozniki          { klasa: mnożnik }       — nadpisuje mnożniki presetu
//   premia_znak_stanu liczba                    — nadpisuje premię mieczy
//   kategorie         { kat: mnożnik }         — v6: mnożnik całej kategorii (po presecie, przed pozycjami)
//   nowe              [pozycja]                 — v6: pozycje dopisane przez MG ({ id, nazwa, kat, cena_p, … })
//   pozycje           { id: { cena_p } | { mnoznik } }  — cena stała albo mnożnik względem ceny z presetu
//   osady             { id: { mnoznik?, limit_p? } }
//   koniunktury       { id: { kategorie?: { kat: { cena?, popyt? } }, czynsz? } }
//   kupcy             { id: { marza?, skup?, limit_p?, preferencje? } }
//   rynek             { preferencje?, kaprys?, cena_minimalna? }   — płytkie scalenie każdej sekcji
const kopia = x => JSON.parse(JSON.stringify(x));
const slugId = s => String(s).toLowerCase().replace(/ł/g, 'l').normalize('NFD').replace(/[̀-ͯ]/g, '')
  .replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
export function zastosujUstawienia(d, ust = {}) {
  const n = kopia(d);
  if (!n.klasy) throw new Error('zastosujUstawienia: brak d.klasy (data/klasy_cenowe.json)');
  const K = n.klasy, nazwa = ust.preset || K.domyslny || 'zalecany';
  const baza = K.presety[nazwa];
  if (!baza) throw new Error('Nieznany preset: ' + nazwa);
  const pr = { ...baza, mnozniki: { ...baza.mnozniki, ...(ust.mnozniki || {}) },
    premia_znak_stanu: ust.premia_znak_stanu ?? baza.premia_znak_stanu };
  const stare = Object.fromEntries(n.cennik.pozycje.map(c => [c.id, c.cena_p]));
  n.cennik = zastosujPreset(n.cennik, { ...K, presety: { ...K.presety, _ustawienia: pr } }, '_ustawienia');
  n.cennik.wersja = (d.cennik.wersja || '') + '+ustawienia';
  for (const c of n.cennik.pozycje) {
    const m = ust.kategorie?.[c.kat];
    if (m != null && m !== 1) { c.cena_p = Math.max(1, Math.round(c.cena_p * m)); c.nadpisane = true; }
  }
  for (const x of ust.nowe || []) {
    if (n.cennik.pozycje.some(c => c.id === x.id)) continue;
    n.cennik.pozycje.push({ zrodlo: null, cena_raw_p: null, obc: null, dostepnosc: 'Powszechna', podstawa_hist: '',
      komentarz: '', dopisane: 'MG', uwagi_danych: null, pozycja_kampanii: true, typ: 'towar', podtyp: null, klasa: 'wlasne',
      ...x, cena_ref_p: x.cena_ref_p ?? x.cena_p, wlasna: true });
  }
  for (const c of n.cennik.pozycje) {
    const o = ust.pozycje?.[c.id];
    if (o?.cena_p != null) c.cena_p = Math.round(o.cena_p);
    else if (o?.mnoznik != null) c.cena_p = Math.max(1, Math.round(c.cena_p * o.mnoznik));
    if (o) c.nadpisane = true;
  }
  // Czynsze idą za cennikiem: ta sama kwatera w cenniku (np. izba-w-kamienicy-miesiac) wyznacza proporcję.
  if (n.czynsze) {
    const C = Object.fromEntries(n.cennik.pozycje.map(c => [c.id, c.cena_p]));
    for (const k of n.czynsze.najem) {
      const id = ['miesiac', 'rok', 'tydzien'].map(o => slugId(k.kwatera) + '-' + o).find(i => i in C && stare[i]);
      if (!id) continue;
      const q = C[id] / stare[id];
      for (const o of ['tydzien_p', 'miesiac_p', 'rok_p']) if (k[o] != null) k[o] = Math.round(k[o] * q);
    }
    for (const k of n.czynsze.kupno ?? []) { const id = 'kupno-' + slugId(k.nazwa); if (id in C) k.cena_p = C[id]; }
  }
  for (const [id, o] of Object.entries(ust.osady || {})) Object.assign(osadaZ(n, id), o);
  for (const [id, o] of Object.entries(ust.koniunktury || {})) {
    const k = konZ(n, id);
    for (const [kat, v] of Object.entries(o.kategorie || {})) k.kategorie[kat] = { ...(k.kategorie[kat] || { cena: 1, popyt: 0 }), ...v };
    if (o.czynsz != null) k.czynsz = { ...(k.czynsz || {}), mnoznik: o.czynsz };
  }
  for (const [id, o] of Object.entries(ust.kupcy || {})) Object.assign(kupiecZ(n, id), o);
  for (const [sek, o] of Object.entries(ust.rynek || {})) n.rynek[sek] = { ...(n.rynek[sek] || {}), ...o };
  n.ustawienia = ust;
  return n;
}
// Różnice cen po ustawieniach: [{ id, nazwa, przed_p, po_p }] — do podglądu w panelu MG.
export function roznicaCen(przed, po) {
  const A = Object.fromEntries(przed.cennik.pozycje.map(c => [c.id, c]));
  return po.cennik.pozycje.filter(c => A[c.id] && A[c.id].cena_p !== c.cena_p)
    .map(c => ({ id: c.id, nazwa: c.nazwa, przed_p: A[c.id].cena_p, po_p: c.cena_p }));
}
