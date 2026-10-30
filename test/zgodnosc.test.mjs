// Test zgodności: silnik.js vs oryginalny artefakt (1680 przypadków zarejestrowanych w przeglądarce).
// Uruchom: node --test test/   (wymaga pliku test/fixtures/oryginal_przypadki.json i reference/dane_oryginal.json)
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import * as S from '../src/silnik.js';

const wczytaj = f => JSON.parse(fs.readFileSync(new URL('../' + f, import.meta.url)));
const dane = Object.fromEntries(['kupcy', 'osady', 'koniunktura', 'rynek', 'nazwy', 'statusy', 'przedmioty_magiczne', 'cennik']
  .map(n => [n, wczytaj(`data/${n}.json`)]));
// cennik w wersji z artefaktu (302 pozycje), żeby porównać 1:1
const orig = wczytaj('reference/dane_oryginal.json');
// v6b: MG zmienił jakość (×1,6 / ×0,6) i targowanie (−4%/PS) — porównanie z oryginałem idzie na jego parametrach.
const rynekOrig = { ...dane.rynek,
  jakosc: { ...dane.rynek.jakosc, opcje: [['2wady', 0.25], ['wada', 0.5], ['zwykla', 1], ['wysmienita', 2], ['mistrzowska', 4]].map(([id, mnoznik]) => ({ id, nazwa: id, mnoznik })) },
  targowanie: { ...dane.rynek.targowanie, za_ps: 0.1, max: 0.3, max_zamowienie: 0.2 }, typ_osady: undefined };
// v6c–v6e: ceny strefy (osady → kategorie), specjalności miast (tagi) i typ osady to dodatki MG — oryginał ich nie miał.
const osadyOrig = { ...dane.osady, osady: dane.osady.osady.map(({ kategorie, tagi, ...o }) => o) };
const daneOrig = { ...dane, osady: osadyOrig, rynek: rynekOrig, cennik: { pozycje: orig.ceny.map(c => ({ id: c.nazwa, kat: c.kat, nazwa: c.nazwa, cena_p: c.nowa })) } };
const przypadki = wczytaj('test/fixtures/oryginal_przypadki.json');

test('generator kupców daje to samo co oryginał', () => {
  const K = dane.kupcy.kupcy, O = dane.osady.osady, N = dane.koniunktura.koniunktury;
  let n = 0;
  for (const c of przypadki) {
    const r = S.generujKupca(daneOrig, { kupiec: K[c.t].id, osada: O[c.l].id, koniunktura: N[c.k].id, seed: c.s, stosujDostepnosc: false, osobowosc: false });
    assert.equal(r.imie, c.h);
    assert.ok(c.q.endsWith(r.dziwactwo));
    assert.equal(r.towar.length, c.rows.length);
    r.towar.forEach((w, i) => {
      const row = c.rows[i];
      assert.equal(w.nazwa, row[0].split('\n')[0]);
      assert.equal(String(w.sztuk), row[1]);
      assert.equal(S.proc(w.mnoznik).replace('-', '−'), row[3].replace('-', '−'));
      assert.equal(S.mon(w.cena_p), row[4], `${w.nazwa} seed ${c.s}`);
      assert.equal(S.mon(w.skup_p), row[5], `${w.nazwa} skup seed ${c.s}`);
      assert.ok(row[6].startsWith(w.zapas_nazwa + ' · ' + w.popyt_nazwa));
    });
    n++;
  }
  assert.equal(n, przypadki.length);
});

test('dochód: średnie zgodne z tabelą statusów', () => {
  for (const s of dane.statusy.poziomy) {
    if (s.lvl === 0) continue;
    const m = S.sredniDochod(dane, `${s.tier} ${s.lvl}`);
    assert.ok(Math.abs(m.netto_p - s.netto_p) < 0.01, `${s.tier} ${s.lvl}`);
    assert.ok(Math.abs(m.brutto_p - s.brutto_p) < 0.01);
  }
});

test('magiczne przedmioty wg HR-026', () => {
  assert.equal(S.cenaMagiczna(dane, { rodzaj: 'zwoj', pz: 0 }), 4 * 240);
  assert.equal(S.cenaMagiczna(dane, { rodzaj: 'rozdzka', pz: 0 }), 20 * 240);
  assert.equal(S.cenaMagiczna(dane, { rodzaj: 'pierscien', pz: 3 }), 600 * 240);
  assert.equal(S.cenaMagiczna(dane, { rodzaj: 'bron', cena_p: 480, wlasciwosci: 1, zalety: 1 }), 480 * 50 * 2);
  assert.equal(S.cenaMagiczna(dane, { rodzaj: 'kostur' }), null);
});

test('jakość: Wada ×½ (HR-024, oryginał); v6b: ×0,6', () => {
  assert.equal(S.cenaZJakoscia(daneOrig, 11520, 'wada'), 5760);
  assert.equal(S.cenaZJakoscia(daneOrig, 11520, '2wady'), 2880);
  assert.equal(S.cenaZJakoscia(dane, 11520, 'wada'), 6912);
});

test('targowanie: 10%/PS, maks. 30%, nie poniżej cennika (oryginał)', () => {
  assert.equal(S.targuj(daneOrig, { cena_p: 1000, cena_cennik_p: 500, ps: 2 }).cena_p, 800);
  assert.equal(S.targuj(daneOrig, { cena_p: 1000, cena_cennik_p: 500, ps: 9 }).cena_p, 700);
  assert.equal(S.targuj(daneOrig, { cena_p: 1000, cena_cennik_p: 900, ps: 3 }).cena_p, 900);
  assert.equal(S.targuj(daneOrig, { cena_p: 1000, cena_cennik_p: 500, ps: 5, zamowienie: true }).cena_p, 800);
});

test('zamówienia na miarę: ta sama cena, zaliczka i odmowy co w oryginale', () => {
  const Zs = wczytaj('test/fixtures/oryginal_zamowienia.json');
  const K = dane.kupcy.kupcy, O = dane.osady.osady, N = dane.koniunktura.koniunktury;
  const JAK = { '0.25': '2wady', '1': 'zwykla', '2': 'wysmienita', '4': 'mistrzowska' };
  for (const z of Zs) {
    const r = S.wycenZamowienie(daneOrig, { kupiec: K[z.t].id, osada: O[z.l].id, koniunktura: N[z.k].id, przedmiot: z.n, jakosc: JAK[z.q], seed: 1 });
    if (!z.tr.length) { assert.equal(r.status, z.txt.includes('tego nie tknie') ? 'odmowa' : 'brak_w_cenniku', z.n); continue; }
    const razem = z.tr.find(x => x.startsWith('Razem')), zal = z.tr.find(x => x.startsWith('Zaliczka'));
    assert.ok(razem.endsWith('→ ' + S.mon(r.cena_p)), `${z.n}: ${razem} vs ${S.mon(r.cena_p)}`);
    assert.ok(zal.endsWith(S.mon(r.zaliczka_p)), `${z.n}: ${zal}`);
  }
});
