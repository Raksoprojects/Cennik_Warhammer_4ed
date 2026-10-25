// Skarbiec Imperium — kupiec trwały (bez DOM, bez zależności).
// Zapisany sklep żyje w kampanii: MG zmienia towar i ceny, drużyna kupuje i sprzedaje, kupiec się przenosi,
// składa zamówienia, a z upływem tygodni sprzedaje i dokupuje. Seed przestaje odtwarzać sklep po pierwszej
// zmianie, więc zapisuje się cały stan. Ceny NIE są zapisane — liczy je wycen() z bieżących danych
// (po ustawieniach MG), tym samym wzorem co generujKupca. Wyjątek: cena ręczna MG (cena_reczna_p).
//
// Każda operacja zwraca NOWY obiekt kupca (wejście bez zmian). Błąd, który wymaga decyzji MG
// (np. towar spoza asortymentu), zwraca { blad, powod } zamiast kupca.
import {
  kosci, generujKupca, pulaTowaru, ilosc, zapasZRzutu, przesunieciePopytu, mnoznikRynku, cenaKoniunktury,
  popytKoniunktury, osobowoscKupca, cenaMinimalna, wycenZamowienie, wTowarze, jakoscLosowa, trefnyLosowy, generujPostac, koniunkturaEfektywna, mnoznikNielegalny, wahaniaZRzutu, etykietaOsady, etykietaKoniunktury, mon, sredniDochod, jakoscZ,
} from './silnik.js';

const clamp = (v, a, b) => v < a ? a : v > b ? b : v;
const kopia = x => JSON.parse(JSON.stringify(x));
const znajdz = (arr, id, co) => { const x = arr.find(e => e.id === id); if (!x) throw new Error(`Nieznany ${co}: ${id}`); return x; };
const kupiecZ = (d, K) => znajdz(d.kupcy.kupcy, K.kupiec, 'kupiec');
const osadaZ = (d, K) => znajdz(d.osady.osady, K.osada, 'osada');
const konZ = (d, K) => znajdz(d.koniunktura.koniunktury, K.koniunktura, 'koniunktura');
// v6c: sytuacja z porą roku, wahaniami rynku i strefą handlową osady.
const konEf = (d, K) => koniunkturaEfektywna(d, konZ(d, K), { osada: osadaZ(d, K), pora: K.pora ?? null, wahania: K.wahania ?? null });
const pozycja = (d, id) => d.cennik.pozycje.find(c => c.id === id);
export const nowyUid = () => Math.random().toString(36).slice(2, 10) + Date.now().toString(36).slice(-4);

// Parametry upływu czasu: data/rynek.json → uplyw_czasu (MG zmienia je w Edycji cen).
export function parametryCzasu(d) {
  return { sprzedaz: [0.05, 0.12, 0.25], dokupienie: 0.5, nowy_towar: 0.25, rynek_co: 4, gotowka_max: 2, ...(d.rynek.uplyw_czasu || {}) };
}
// Kolejne rzuty kupca: osobny strumień na każdą operację, powtarzalny dla tego samego stanu.
function rzuty(K) { K.licznik = (K.licznik || 0) + 1; return kosci((K.seed ^ Math.imul(K.licznik, 0x9e3779b1)) >>> 0); }
const wpis = (K, tekst) => K.dziennik.push({ tydzien: K.tydzien, tekst });

/* ------------------------------------------------------------ budżet i norma */
// Norma = ile sztuk kupiec chce mieć przy normalnym zapasie. Do niej uzupełnia rdzeń z upływem czasu.
const waga = (kup, kat) => kup.rdzen.includes(kat) ? 2 : 1;
function budzetPozycji(d, K, kat) {
  if (K.budzet_towaru_p == null) return Infinity;
  const kup = kupiecZ(d, K), suma = K.towar.reduce((s, w) => s + waga(kup, w.kat), 0) || 1;
  return K.budzet_towaru_p * waga(kup, kat) / suma;
}
function normaPozycji(d, K, c, ri) {
  const n = ilosc(d, ri, c.cena_ref_p ?? c.cena_p, 1);
  return Math.max(1, Math.min(n, Math.floor(budzetPozycji(d, K, c.kat) / c.cena_p)));
}
const zapasZeStanu = w => w.sztuk <= 0 ? 3 : w.sztuk < w.norma * 0.5 ? 2 : w.sztuk >= w.norma * 2 ? 0 : 1;

// losujJakosc: jak w generatorze — szansa kupca na Zalety albo Wady przedmiotu i na towar trefny (ręcznie dodany towar jest zwykły).
function nowyWiersz(d, K, c, r, { zapas, sztuk, poza = false, losujJakosc = false } = {}) {
  const jak = losujJakosc ? jakoscLosowa(d, kupiecZ(d, K), c, r) : null;
  const trefny = losujJakosc ? trefnyLosowy(d, kupiecZ(d, K), c, r, K.postac?.cecha?.efekt) : null;
  const z = zapas ?? zapasZRzutu(d, r.k(10));
  const norma = normaPozycji(d, K, c, r.ri);
  const szt = sztuk ?? (z === 1 ? norma : Math.max(z === 3 ? 0 : 1, Math.min(ilosc(d, r.ri, c.cena_ref_p ?? c.cena_p, z),
    Math.floor(budzetPozycji(d, K, c.kat) * (z === 0 ? 1.5 : 1) / c.cena_p))));
  return { id: c.id, nazwa: c.nazwa, kat: c.kat, sztuk: szt, norma, zapas: z, przes_popytu: przesunieciePopytu(d, r.k(10)),
    rzut_kaprysu: r.k(10), cena_wytworcy_p: c.cena_p, cena_reczna_p: null, poza_asortymentem: poza, cechy: jak?.cechy ?? null, trefny };
}

// v6c: nowa osobowość (charakter, motywacja, cecha kupiecka…) dla zapisanego kupca. charaktery = dozwolone.
export function przelosujPostac(d, K0, { charaktery = null, seed = (Math.random() * 1e9) | 0 } = {}) {
  const K = kopia(K0);
  K.postac = generujPostac(d, kosci(seed >>> 0), { charaktery });
  wpis(K, `Nowa osobowość: ${K.postac?.motywacja?.nazwa ?? '—'}, ${K.postac?.cecha?.nazwa ?? '—'}.`);
  return K;
}

/* ------------------------------------------------------------ zapis wygenerowanego sklepu */
/** @param {any} d @param {any} sklep @param {Record<string, any>} [opcje] */
export function utworzKupca(d, sklep, { nazwa, grupa = '', notatka = '', data = new Date().toISOString().slice(0, 10) } = {}) {
  const K = {
    wersja: 1, uid: nowyUid(), nazwa: nazwa || sklep.imie, imie: sklep.imie, dziwactwo: sklep.dziwactwo,
    kupiec: sklep.kupiec.id, osada: sklep.osada.id, koniunktura: sklep.koniunktura.id, seed: sklep.seed,
    tydzien: 0, modyfikator: 1, grupa, notatka, gotowka_p: sklep.gotowka_p ?? 0, gotowka_start_p: sklep.gotowka_p ?? 0, budzet_towaru_p: sklep.budzet_towaru_p,
    utworzony: data, zmieniony: data, licznik: 0, towar: [], zamowienia: [], dziennik: [],
  };
  K.towar = sklep.towar.map(t => ({ id: t.id, nazwa: t.nazwa, kat: t.kat, sztuk: t.sztuk, norma: 0, zapas: t.zapas,
    przes_popytu: przesunieciePopytu(d, t.rzuty.popyt), rzut_kaprysu: t.rzuty.kaprys, cena_wytworcy_p: t.cena_cennik_p ?? t.cena_wytworcy_p,
    cena_reczna_p: null, poza_asortymentem: false, cechy: t.cechy ?? null, trefny: t.trefny ?? null }));
  K.postac = sklep.postac ?? null;
  K.pora = sklep.pora ?? null; K.wahania = sklep.wahania ?? null;
  const r = rzuty(K);
  for (const w of K.towar) {
    const c = pozycja(d, w.id);
    w.norma = w.zapas === 1 ? Math.max(1, w.sztuk) : w.zapas === 0 ? Math.max(1, Math.round(w.sztuk / 2.5)) : normaPozycji(d, K, c, r.ri);
  }
  wpis(K, `Zapisany: ${sklep.kupiec.nazwa}, ${sklep.osada.nazwa}, ${sklep.koniunktura.nazwa}. Gotówka ${mon(K.gotowka_p)}.`);
  return K;
}

/* ------------------------------------------------------------ ceny na żywo */
// Ten sam wzór co generujKupca: cena bazowa × marża × (preferencja × kaprys) × osada × koniunktura × rynek,
// plus modyfikator MG kupca (np. 0,9 dla zaprzyjaźnionego, 1,2 dla wrogiego).
export function wycen(d, K) {
  const kup = kupiecZ(d, K), lok = osadaZ(d, K), kon = konEf(d, K), R = d.rynek, mod = K.modyfikator ?? 1;
  const E = K.postac?.cecha?.efekt ?? {};   // v6c: cecha kupiecka (Chciwy: ceny ×1,1, skup ×0,85…)
  const towar = K.towar.map((w, ix) => {
    const c0 = pozycja(d, w.id) ?? { id: w.id, nazwa: w.nazwa, kat: w.kat, cena_p: w.cena_wytworcy_p, cena_raw_p: null };
    // v6: egzemplarz z Zaletami / Wadami przedmiotu — cena bazowa egzemplarza = cena z cennika × jakość.
    const jak = w.cechy && Object.keys(w.cechy).length ? jakoscZ(d, w.cechy) : null;
    const c = jak ? { ...c0, cena_p: Math.round(c0.cena_p * jak.mnoznik) } : c0;
    const popyt = clamp(R.popyt.start + popytKoniunktury(kon, c.kat) + w.przes_popytu, 0, 2);
    const mKon = cenaKoniunktury(kon, c.kat), mRynek = mnoznikRynku(d, w.zapas, popyt);
    const os = osobowoscKupca(d, kup, c, E.kaprys === false ? null : w.rzut_kaprysu);
    const mNiel = mnoznikNielegalny(d, lok, c);
    const mnoznik = kup.marza * os.mnoznik * lok.mnoznik * mKon * mRynek * mod * (E.ceny ?? 1) * mNiel;
    const cenaW = c.cena_p * mnoznik, cena_p = w.cena_reczna_p ?? Math.round(cenaW);
    const skupU = Math.max(R.skup.minimum, kup.skup + (popyt === 2 ? R.skup.popyt_wysoki : popyt === 0 ? R.skup.popyt_niski : 0)) * (E.skup ?? 1);
    const min = cenaMinimalna(d, { kupiec: kup, pozycja: c, osada: lok, koniunktura: kon, mRynek, cena_p });
    return { ...w, ix, nazwa: c.nazwa, kat: c.kat, cena_raw_p: c.cena_raw_p ?? null, cena_wytworcy_p: c.cena_p, mnoznik, cena_p,
      cena_cennik_p: c0.cena_p, jakosc: jak ? { nazwa: jak.nazwa, mnoznik: jak.mnoznik } : null,
      skup_p: Math.round((w.cena_reczna_p ?? cenaW) * skupU), koszt_p: min.koszt_p, cena_min_p: min.cena_min_p, wyprzedaz: min.wyprzedaz,
      popyt, zapas_nazwa: R.zapas.progi[w.zapas].nazwa, popyt_nazwa: R.popyt.nazwy[popyt], rzuty: { kaprys: os.rzut },
      skladowe: { marza: kup.marza, preferencja: os.preferencja, kaprys: os.kaprys, osada: lok.mnoznik, koniunktura: mKon, rynek: mRynek, modyfikator: mod, charakter: E.ceny ?? 1, nielegalny: mNiel },
      brak_w_cenniku: !pozycja(d, w.id) };
  }).sort((a, b) => b.cena_cennik_p - a.cena_cennik_p);   // jak w generatorze: po cenie z cennika, bez jakości
  return { kupiec: kup, osada: lok, koniunktura: kon, towar,
    wartosc_towaru_p: towar.reduce((s, t) => s + t.sztuk * t.cena_wytworcy_p, 0),
    etykiety: { osada: etykietaOsady(lok), koniunktura: etykietaKoniunktury(d, kon) } };
}

/* ------------------------------------------------------------ asortyment */
// Czy kupiec może mieć tę rzecz na stanie? { ok, powod } — powod do pokazania MG przed decyzją „mimo to”.
export function czyWAsortymencie(d, K, id) {
  const c = pozycja(d, id);
  if (!c) return { ok: false, powod: 'brak w cenniku' };
  if (!wTowarze(d, c)) return { ok: false, powod: 'to nie towar (usługa, nocleg, nieruchomość)' };
  const kup = kupiecZ(d, K);
  if (!kup.rdzen.includes(c.kat) && !kup.boczne.includes(c.kat)) return { ok: false, powod: `${kup.nazwa} nie handluje kategorią „${c.kat}”` };
  if (!pulaTowaru(d, { kupiec: K.kupiec, osada: K.osada, kats: [c.kat], nielegalne: !!K.postac?.cecha?.efekt?.nielegalne }).some(x => x.id === id))
    return { ok: false, powod: 'za droga albo za rzadka na ten sklep i tę osadę' };
  return { ok: true, powod: null };
}

/** @param {any} d @param {any} K0 @param {string} id @param {Record<string, any>} [opcje] */
export function dodajPozycje(d, K0, id, { sztuk, wymus = false } = {}) {
  const sp = czyWAsortymencie(d, K0, id);
  if (!sp.ok && (!wymus || sp.powod === 'brak w cenniku')) return { blad: 'poza_asortymentem', powod: sp.powod };
  const K = kopia(K0), c = pozycja(d, id), jest = K.towar.find(w => w.id === id);
  if (jest) { jest.sztuk += sztuk ?? jest.norma; jest.zapas = zapasZeStanu(jest); }
  else K.towar.push(nowyWiersz(d, K, c, rzuty(K), { zapas: 1, sztuk, poza: !sp.ok }));
  wpis(K, `Dodano: ${c.nazwa}${sp.ok ? '' : ` (mimo że: ${sp.powod})`}.`);
  return K;
}
export function usunPozycje(K0, id) {
  const K = kopia(K0), w = K.towar.find(x => x.id === id);
  K.towar = K.towar.filter(x => x.id !== id);
  if (w) wpis(K, `Usunięto: ${w.nazwa}.`);
  return K;
}
// Ręczna zmiana wiersza: { sztuk?, cena_reczna_p? (null = cena z wyliczenia), norma? }.
export function zmienPozycje(K0, id, zmiany) {
  const K = kopia(K0), w = K.towar.find(x => x.id === id);
  if (!w) return K0;
  Object.assign(w, zmiany);
  if ('sztuk' in zmiany) w.zapas = zapasZeStanu(w);
  return K;
}
export function przelosujPozycje(d, K0, id) {
  const K = kopia(K0), i = K.towar.findIndex(x => x.id === id), c = pozycja(d, id);
  if (i < 0 || !c) return K0;
  const stary = K.towar[i];
  K.towar[i] = { ...nowyWiersz(d, K, c, rzuty(K), { losujJakosc: true }), poza_asortymentem: stary.poza_asortymentem };
  return K;
}
// Dolosuj `ile` nowych pozycji z kategorii (albo z całego asortymentu, gdy kat pusta).
/** @param {any} d @param {any} K0 @param {Record<string, any>} [opcje] */
export function dogeneruj(d, K0, { kat = null, ile = 2 } = {}) {
  const K = kopia(K0), kup = kupiecZ(d, K), r = rzuty(K);
  const mam = new Set(K.towar.map(w => w.id));
  const pula = pulaTowaru(d, { kupiec: K.kupiec, osada: K.osada, kats: kat ? [kat] : [...kup.rdzen, ...kup.boczne], nielegalne: !!K.postac?.cecha?.efekt?.nielegalne }).filter(c => !mam.has(c.id));
  const nowe = [];
  while (nowe.length < ile && pula.length) nowe.push(pula.splice(r.ri(pula.length), 1)[0]);
  for (const c of nowe) K.towar.push(nowyWiersz(d, K, c, r, { losujJakosc: true }));
  wpis(K, nowe.length ? `Dogenerowano: ${nowe.map(c => c.nazwa).join(', ')}.` : 'Dogenerowanie: nic nowego nie pasuje do sklepu.');
  return K;
}
// Nowy asortyment, ta sama osoba (imię, dziwactwo, gotówka, notatki, zamówienia).
export function przelosujWszystko(d, K0, seed = (Math.random() * 1e9) | 0) {
  const sklep = generujKupca(d, { kupiec: K0.kupiec, osada: K0.osada, koniunktura: K0.koniunktura, seed });
  const nowy = utworzKupca(d, sklep);
  const K = kopia(K0);
  Object.assign(K, { towar: nowy.towar, budzet_towaru_p: nowy.budzet_towaru_p });
  wpis(K, 'Nowy asortyment (przelosowany).');
  return K;
}
// Przenosiny do innej osady albo zmiana sytuacji. Ceny przeliczą się same w wycen(); ręczne zostają.
/** @param {any} d @param {any} K0 @param {Record<string, any>} opcje */
// v6c: także pora roku i wahania rynku (null = bez).
export function przenies(d, K0, { osada, koniunktura, ...reszta }) {
  const K = kopia(K0), zm = [], H = d.handel;
  if (osada && osada !== K.osada) { K.osada = osada; zm.push('przeniósł się: ' + osadaZ(d, K).nazwa); }
  if (koniunktura && koniunktura !== K.koniunktura) { K.koniunktura = koniunktura; zm.push('sytuacja: ' + konZ(d, K).nazwa); }
  if ('pora' in reszta && reszta.pora !== (K.pora ?? null)) {
    K.pora = reszta.pora; zm.push('pora roku: ' + (H?.pory_roku.lista.find(p => p.id === K.pora)?.nazwa ?? 'bez'));
  }
  if ('wahania' in reszta && reszta.wahania !== (K.wahania ?? null)) {
    K.wahania = reszta.wahania; zm.push('rynek: ' + (H?.wahania.lista.find(w => w.id === K.wahania)?.nazwa ?? 'bez wahań'));
  }
  if (zm.length) wpis(K, zm.join(', ') + '.');
  return K;
}

/* ------------------------------------------------------------ transakcje drużyny */
// typ 'kupno' = drużyna kupuje od kupca; 'sprzedaz' = drużyna sprzedaje kupcowi. cena_p = za sztukę.
export function transakcja(d, K0, { id, typ, ilosc: n = 1, cena_p, wymus = false }) {
  const K = kopia(K0), c = pozycja(d, id);
  let w = K.towar.find(x => x.id === id);
  const suma = n * cena_p, nazwa = w?.nazwa ?? c?.nazwa ?? id;
  if (typ === 'kupno') {
    if (!w || w.sztuk < n) return { blad: 'brak_towaru', powod: `kupiec ma ${w?.sztuk ?? 0} szt.` };
    w.sztuk -= n; w.zapas = zapasZeStanu(w); K.gotowka_p += suma;
    wpis(K, `Drużyna kupiła: ${nazwa} × ${n} za ${mon(suma)}.`);
  } else {
    if (suma > K.gotowka_p && !wymus) return { blad: 'brak_gotowki', powod: `kupiec ma ${mon(K.gotowka_p)}, a to ${mon(suma)}` };
    if (!c) return { blad: 'brak_w_cenniku', powod: 'brak w cenniku' };
    if (!w) { w = nowyWiersz(d, K, c, rzuty(K), { zapas: 1, sztuk: 0, poza: !czyWAsortymencie(d, K, id).ok }); K.towar.push(w); }
    w.sztuk += n; w.zapas = zapasZeStanu(w); K.gotowka_p -= suma;
    wpis(K, `Drużyna sprzedała: ${nazwa} × ${n} za ${mon(suma)}.`);
  }
  return K;
}

/* ------------------------------------------------------------ zamówienia w toku */
// Termin z wycenZamowienie („3 dni”, „2 tygodni”, „4 miesięcy”) → tygodnie kampanii.
export function terminTygodnie(txt) {
  const [n, j] = String(txt).split(' '), x = +n;
  return /dni/.test(j) ? Math.max(1, Math.ceil(x / 7)) : /mies/.test(j) ? x * 4 : x;
}
// Zamówienie na miarę u tego kupca. Odmowa (kupiec tego nie robi ani nie sprowadza) wymaga wymus: true —
// wtedy kupiec sprowadza rzecz z narzutem sprowadzenia. Zaliczka od razu trafia do jego gotówki.
/** @param {any} d @param {any} K0 @param {Record<string, any>} opcje */
export function zamow(d, K0, { id, jakosc = 'zwykla', dla = '', wymus = false, cena_p = null, material = false }) {
  const K = kopia(K0), r = rzuty(K), mod = K.modyfikator ?? 1;
  const w = wycenZamowienie(d, { kupiec: K.kupiec, osada: K.osada, koniunktura: K.koniunktura, przedmiot: id, jakosc, material, pora: K.pora ?? null, wahania: K.wahania ?? null, seed: r.ri(1e9) });
  if (w.status === 'brak_w_cenniku') return { blad: 'brak_w_cenniku', powod: 'tej rzeczy nie da się zamówić' };
  let cena, termin, stan = w.status;
  if (w.status === 'odmowa') {
    if (!wymus) return { blad: 'odmowa', powod: `${kupiecZ(d, K).nazwa} tego nie robi ani nie sprowadza. Odsyła do: ${w.odsyla_do.join(', ') || '—'}` };
    const kup = kupiecZ(d, K);
    cena = w.przedmiot.cena_p * jakoscZ(d, jakosc).mnoznik * kup.marza * osadaZ(d, K).mnoznik * cenaKoniunktury(konEf(d, K), w.przedmiot.kat) * d.rynek.zamowienie.narzut_sprowadzenie;
    termin = 4 + r.ri(6); stan = 'sprowadza';
  } else { cena = w.cena_p; termin = terminTygodnie(w.termin) + (w.rzadkosc?.termin_tyg ?? 0); }
  termin = Math.max(1, Math.round(termin * (K.postac?.cecha?.efekt?.termin ?? 1)));   // v6c: Obieżyświat szybciej, Leniwy wolniej
  cena *= K.postac?.cecha?.efekt?.ceny ?? 1;
  const cenaP = cena_p ?? Math.round(cena * mod), zaliczka = Math.round(cenaP * d.rynek.zamowienie.zaliczka);
  const jak = jakoscZ(d, jakosc);
  K.zamowienia.push({ uid: nowyUid(), id, nazwa: w.przedmiot.nazwa, jakosc: jak.nazwa, cechy: jak.cechy ?? null, sposob: stan, dla, cena_p: cenaP, zaliczka_p: zaliczka,
    tydzien_zlozenia: K.tydzien, tydzien_gotowe: K.tydzien + termin, status: 'w_toku', wymuszone: w.status === 'odmowa', material: !!w.material });
  K.gotowka_p += zaliczka;
  wpis(K, `Zamówienie: ${w.przedmiot.nazwa} (${jak.nazwa})${dla ? ' dla ' + dla : ''}${w.material ? ', materiał zamawiającego' : ''}, ${mon(cenaP)}, zaliczka ${mon(zaliczka)}, za ${termin} tyg.`);
  return K;
}
export function odbierzZamowienie(K0, uid) {
  const K = kopia(K0), z = K.zamowienia.find(x => x.uid === uid);
  if (!z || z.status === 'odebrane' || z.status === 'anulowane') return K0;
  K.gotowka_p += z.cena_p - z.zaliczka_p; z.status = 'odebrane';
  wpis(K, `Odebrano: ${z.nazwa}, dopłata ${mon(z.cena_p - z.zaliczka_p)}.`);
  return K;
}
export function anulujZamowienie(K0, uid, { zwrotZaliczki = false } = {}) {
  const K = kopia(K0), z = K.zamowienia.find(x => x.uid === uid);
  if (!z || z.status === 'odebrane' || z.status === 'anulowane') return K0;
  if (zwrotZaliczki) K.gotowka_p -= z.zaliczka_p;
  z.status = 'anulowane';
  wpis(K, `Anulowano: ${z.nazwa}${zwrotZaliczki ? ', zaliczka zwrócona' : ', zaliczka przepada'}.`);
  return K;
}

/* ------------------------------------------------------------ upływ czasu */
// Co tydzień: sprzedaż (udział sztuk wg popytu), dokupienie rdzenia do normy za koszt nabycia, szansa na nowy towar,
// co `rynek_co` tygodni nowy popyt i kaprys (poza cenami ręcznymi), zamówienia z minionym terminem są gotowe.
// Kupiec żyje ze sklepu: gotówkę ponad gotowka_max × gotówka startowa odkłada (życie, długi, skrzynia pod podłogą).
// Boczny towar dokupuje rzadziej niż rdzeń; ten, który się wyprzedał, znika z półki.
// Wynik powtarzalny: ten sam kupiec + te same tygodnie = to samo.
export function uplywCzasu(d, K0, tygodnie = 1) {
  const K = kopia(K0), P = parametryCzasu(d), kup = kupiecZ(d, K);
  const sprzedal = new Map(), dokupil = new Map(), nowe = [], gotowe = [];
  const dodaj = (m, nazwa, n, p) => { const x = m.get(nazwa) ?? { n: 0, p: 0 }; m.set(nazwa, { n: x.n + n, p: x.p + n * p }); };
  const sufit = Math.round(Math.max(K.gotowka_start_p ?? K.gotowka_p, sredniDochod(d, kup.status).brutto_p) * P.gotowka_max);
  const g0 = K.gotowka_p, zmianyRynku = [];
  let wydal = 0;
  for (let t = 0; t < tygodnie; t++) {
    K.tydzien++;
    const r = kosci((K.seed ^ Math.imul(K.tydzien, 0x85ebca6b)) >>> 0);
    const ceny = new Map(wycen(d, K).towar.map(w => [w.id, w]));
    for (const w of K.towar) {
      if (w.sztuk <= 0) continue;
      const f = P.sprzedaz[ceny.get(w.id).popyt];
      let n = 0;
      if (w.sztuk <= 40) for (let i = 0; i < w.sztuk; i++) n += r.rnd() < f ? 1 : 0;
      else n = Math.round(w.sztuk * f * (0.6 + 0.8 * r.rnd()));
      if (!n) continue;
      w.sztuk -= n; K.gotowka_p += n * ceny.get(w.id).cena_p;
      dodaj(sprzedal, w.nazwa, n, ceny.get(w.id).cena_p);
    }
    for (const w of K.towar) {
      const szansa = kup.rdzen.includes(w.kat) ? P.dokupienie : P.dokupienie / 2;
      if (w.sztuk >= w.norma || w.poza_asortymentem || r.rnd() >= szansa) continue;
      // Nie płaci więcej niż 80% swojej ceny — paser (marża ×0,65) kupuje od złodziei, nie od wytwórcy.
      const c = ceny.get(w.id), koszt = Math.min(c.koszt_p, Math.round(c.cena_p * 0.8)), n = Math.min(w.norma - w.sztuk, Math.floor(K.gotowka_p / Math.max(1, koszt)));
      if (n <= 0) continue;
      w.sztuk += n; K.gotowka_p -= n * koszt;
      dodaj(dokupil, w.nazwa, n, koszt);
    }
    K.towar = K.towar.filter(w => w.sztuk > 0 || kup.rdzen.includes(w.kat));
    if (r.rnd() < P.nowy_towar) {
      const mam = new Set(K.towar.map(w => w.id));
      const pula = pulaTowaru(d, { kupiec: K.kupiec, osada: K.osada, kats: [...kup.rdzen, ...kup.boczne], nielegalne: !!K.postac?.cecha?.efekt?.nielegalne }).filter(c => !mam.has(c.id));
      if (pula.length) {
        const c = pula[r.ri(pula.length)], w = nowyWiersz(d, K, c, r, { zapas: 1, losujJakosc: true });
        const koszt = Math.round(c.cena_p * (w.cechy ? jakoscZ(d, w.cechy).mnoznik : 1) * osadaZ(d, K).mnoznik * cenaKoniunktury(konEf(d, K), c.kat)) * w.sztuk;
        if (koszt <= K.gotowka_p) { K.towar.push(w); K.gotowka_p -= koszt; nowe.push(c.nazwa); }
      }
    }
    if (K.tydzien % P.rynek_co === 0) {
      for (const w of K.towar) if (w.cena_reczna_p == null) { w.przes_popytu = przesunieciePopytu(d, r.k(10)); w.rzut_kaprysu = r.k(10); }
      // v6c: wahania rynku — nowy rzut 1k10, jeśli kupiec je śledzi (pole wahania ustawione).
      if (K.wahania) { const nw = wahaniaZRzutu(d, r.k(10)); if (nw !== K.wahania) zmianyRynku.push(d.handel.wahania.lista.find(x => x.id === nw).nazwa); K.wahania = nw; }
    }
    // v6c: pora roku zmienia się co 13 tygodni (jeśli ustawiona).
    if (K.pora && K.tydzien % 13 === 0) {
      const L = d.handel.pory_roku.lista, i = L.findIndex(p => p.id === K.pora);
      K.pora = L[(i + 1) % L.length].id; zmianyRynku.push(L[(i + 1) % L.length].nazwa);
    }
    for (const w of K.towar) w.zapas = zapasZeStanu(w);
    for (const z of K.zamowienia) if (z.status === 'w_toku' && z.tydzien_gotowe <= K.tydzien) { z.status = 'gotowe'; gotowe.push(z.nazwa); }
    if (K.gotowka_p > sufit) { wydal += K.gotowka_p - sufit; K.gotowka_p = sufit; }
  }
  // „Sprzedał 87 szt. za 150 ZK (najwięcej: Kolczuga ×1, Miecz ×2, …)” — pięć pozycji o największej wartości.
  const lista = m => {
    const v = [...m], szt = v.reduce((s, [, x]) => s + x.n, 0), suma = v.reduce((s, [, x]) => s + x.p, 0);
    const top = v.sort((a, b) => b[1].p - a[1].p).slice(0, 5).map(([n, x]) => `${n} ×${x.n}`).join(', ');
    return `${szt} szt. za ${mon(suma)} (${v.length > 5 ? 'najwięcej: ' : ''}${top}${v.length > 5 ? ', …' : ''})`;
  };
  const czesci = [`Minęło ${tygodnie} tyg.`];
  if (zmianyRynku.length) czesci.push('Rynek: ' + zmianyRynku.join(' → ') + '.');
  if (sprzedal.size) czesci.push('Sprzedał ' + lista(sprzedal) + '.');
  if (dokupil.size) czesci.push('Dokupił ' + lista(dokupil) + '.');
  if (wydal) czesci.push(`Odłożył zysk ponad zapas gotówki: ${mon(wydal)}.`);
  if (nowe.length) czesci.push('Nowy towar: ' + nowe.join(', ') + '.');
  if (gotowe.length) czesci.push('Gotowe zamówienia: ' + gotowe.join(', ') + '.');
  const dg = K.gotowka_p - g0;
  czesci.push(`Gotówka ${dg >= 0 ? '+' : '−'}${mon(Math.abs(dg))} (teraz ${mon(K.gotowka_p)}).`);
  wpis(K, czesci.join(' '));
  return K;
}
