// v5: ustawienia MG na żywo, cena minimalna, etykiety modyfikatorów, osobowość kupca.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import * as S from '../src/silnik.js';
import { sprawdzWszystko } from '../src/spojnosc.js';
const rd = f => JSON.parse(fs.readFileSync(new URL('../' + f, import.meta.url)));
const d = Object.fromEntries(['cennik', 'kupcy', 'osady', 'koniunktura', 'rynek', 'nazwy', 'statusy', 'przedmioty_magiczne', 'czynsze']
  .map(n => [n, rd(`data/${n}.json`)]));
d.klasy = rd('data/klasy_cenowe.json');
const ceny = x => Object.fromEntries(x.cennik.pozycje.map(c => [c.id, c.cena_p]));

test('puste ustawienia = cennik bez zmian', () => {
  const n = S.zastosujUstawienia(d, rd('data/ustawienia.json'));
  assert.deepEqual(S.roznicaCen(d, n), []);
  assert.deepEqual(n.czynsze, d.czynsze);
});

test('przykład z data/ustawienia.json działa i nie psuje danych wejściowych', () => {
  const przed = JSON.stringify(d);
  const n = S.zastosujUstawienia(d, rd('data/ustawienia.json').przyklad);
  assert.equal(JSON.stringify(d), przed, 'zastosujUstawienia nie może mutować wejścia');
  const C = ceny(n);
  assert.equal(C.miecz, 960);
  assert.equal(C.rumak, ceny(d).rumak / 1.5 * 2);
  assert.equal(n.osady.osady.find(o => o.id === 'altdorf').mnoznik, 1.4);
  assert.equal(n.koniunktura.koniunktury.find(k => k.id === 'wojna').kategorie.Pancerze.cena, 2);
  assert.equal(n.kupcy.kupcy.find(k => k.id === 'zbrojmistrz').marza, 1.2);
  assert.deepEqual(n.rynek.kaprys.granice, [0.9, 1.1]);
  assert.ok(n.rynek.kaprys.progi.length, 'scalenie sekcji rynku jest płytkie — progi zostają');
});

test('zmiana mnożnika najmu przenosi się na czynsze.json', () => {
  const n = S.zastosujUstawienia(d, { mnozniki: { najem: 3 } });
  const C = ceny(n);
  const izba = n.czynsze.najem.find(k => k.kwatera === 'Izba w kamienicy');
  assert.equal(izba.miesiac_p, C['izba-w-kamienicy-miesiac']);
  const w = sprawdzWszystko(n.cennik, { czynsze: n.czynsze }).find(x => x.id === 'struktura');
  assert.deepEqual(w.bledy, []);
});

test('obowiązujący cennik przechodzi wszystkie testy spójności (bez ostrzeżeń)', () => {
  const w = sprawdzWszystko(d.cennik, { reguly: rd('data/spojnosc.json').reguly, testy: rd('data/spojnosc_v4.json'), czynsze: d.czynsze });
  const zle = w.flatMap(x => x.bledy.map(b => `${x.nazwa}: ${b}`));
  assert.deepEqual(zle, []);
});

test('cena minimalna: koszt nabycia × 1,05, nigdy powyżej ceny kupca; wyprzedaż poniżej kosztu', () => {
  for (let seed = 1; seed <= 60; seed++) {
    const r = S.generujKupca(d, { kupiec: 'zbrojmistrz', osada: 'miasto', koniunktura: 'wojna', seed });
    for (const t of r.towar) {
      assert.ok(t.cena_min_p <= t.cena_p, `${t.id}: min ${t.cena_min_p} > cena ${t.cena_p}`);
      const prog = Math.round(t.koszt_p * (t.wyprzedaz ? 0.9 : 1.05));
      assert.ok(Math.abs(t.cena_min_p - Math.min(t.cena_p, prog)) <= 1, `${t.id} seed ${seed}`);
    }
  }
});

test('wytwórca liczy własny koszt taniej (koszt_wlasny 0,8)', () => {
  const kup = d.kupcy.kupcy.find(k => k.id === 'kowal'), lok = d.osady.osady.find(o => o.id === 'miasteczko');
  const kon = d.koniunktura.koniunktury.find(k => k.id === 'normalna');
  const sierp = d.cennik.pozycje.find(c => c.id === 'sierp');
  const m = S.cenaMinimalna(d, { kupiec: kup, pozycja: sierp, osada: lok, koniunktura: kon, mRynek: 1, cena_p: 1e9 });
  assert.equal(m.koszt_p, Math.round(sierp.cena_p * 0.8));
  assert.ok(m.wlasny_wyrob);
});

test('majątek kupca: kramarz nie trzyma drogich rzeczy ani stosów namiotów', () => {
  for (let seed = 1; seed <= 60; seed++) {
    const r = S.generujKupca(d, { kupiec: 'kramarz', osada: 'miasto', seed });
    const nam = r.towar.find(t => t.id === 'namiot');
    assert.ok(!nam || nam.sztuk <= 1, `namiotów: ${nam?.sztuk}`);
    assert.ok(r.gotowka_p > 0 && r.gotowka_p < 330 * 2 * 1.5, `gotówka ${r.gotowka_p}`);
    assert.ok(r.wartosc_towaru_p < r.budzet_towaru_p * 3, `towar ${r.wartosc_towaru_p} vs budżet ${r.budzet_towaru_p}`);
  }
});

test('osobowość kupca mieści się w granicach i nie zmienia asortymentu ani rzutów', () => {
  const [lo, hi] = d.rynek.kaprys.granice;
  for (let seed = 1; seed <= 40; seed++) {
    const a = S.generujKupca(d, { kupiec: 'kramarz', osada: 'miasto', seed });
    const b = S.generujKupca(d, { kupiec: 'kramarz', osada: 'miasto', seed, osobowosc: false });
    // v5.2: majątek kupca może usunąć za drogie pozycje i zmniejszyć liczbę sztuk, ale nie zmienia rzutów.
    const B = Object.fromEntries(b.towar.map(x => [x.id, x]));
    for (const x of a.towar) {
      assert.ok(B[x.id], x.id);
      assert.deepEqual([x.rzuty.zapas, x.rzuty.popyt], [B[x.id].rzuty.zapas, B[x.id].rzuty.popyt]);
      assert.ok(x.sztuk <= B[x.id].sztuk);
    }
    for (const t of a.towar) {
      const m = t.skladowe.preferencja * t.skladowe.kaprys;
      assert.ok(m >= lo - 1e-9 || Math.abs(t.mnoznik / (t.skladowe.marza * t.skladowe.osada * t.skladowe.koniunktura * t.skladowe.rynek) - lo) < 1e-9);
      assert.ok(t.mnoznik / (t.skladowe.marza * t.skladowe.osada * t.skladowe.koniunktura * t.skladowe.rynek) <= hi + 1e-9);
    }
  }
});

test('etykiety: miasto i sytuacja pokazują modyfikator w nawiasie', () => {
  const O = id => d.osady.osady.find(o => o.id === id), K = id => d.koniunktura.koniunktury.find(k => k.id === id);
  assert.equal(S.etykietaOsady(O('altdorf')), 'Altdorf (+30%)');
  assert.equal(S.etykietaOsady(O('wies')), 'Wieś (-15%)');
  assert.equal(S.etykietaOsady(O('miasteczko')), 'Miasteczko (ceny bez zmian)');
  assert.equal(S.etykietaKoniunktury(d, K('normalna')), 'Normalna (ceny bez zmian)');
  assert.equal(S.etykietaKoniunktury(d, K('nadmiar')), 'Nadmiar towaru po jarmarku (wszystko -20%)');
  assert.match(S.etykietaKoniunktury(d, K('wojna')), /^Wojna \(Broń biała, Broń zasięgowa, Amunicja, Pancerze \+80% · Jedzenie, picie, nocleg \+30% · reszta \+5% · czynsz \+30%\)$/);
  assert.equal(S.etykietaKoniunktury(d, K('kryzys_mieszkaniowy')), 'Kryzys mieszkaniowy (ceny bez zmian · czynsz +70%)');
  assert.equal(S.etykietaKoniunktury(d, K('wojna'), { krotko: true }), 'Wojna (broń, strzelecka, amunicja, pancerze +80% · jedzenie +30% · reszta +5% · czynsz +30%)');
});

test('targowanie z ceną minimalną nie schodzi poniżej niej', () => {
  const r = S.targuj(d, { cena_p: 1000, cena_cennik_p: 1000, cena_min_p: 800, ps: 9 });
  assert.equal(r.cena_p, 800);
  const r2 = S.targuj(d, { cena_p: 1000, cena_cennik_p: 1000, cena_min_p: 970, ps: 1 });
  assert.equal(r2.cena_p, 970);
});

test('targowanie v6b: −4% za PS, najwyżej −24%, talent ponad limit, przegrany test bez upustu', () => {
  const t = x => S.targuj(d, { cena_p: 1000, cena_cennik_p: 100, ...x }).cena_p;
  assert.equal(t({ ps: 1 }), 960);
  assert.equal(t({ ps: 6 }), 760);
  assert.equal(t({ ps: 9 }), 760);
  assert.equal(t({ ps: 6, talent: 0.04 }), 720);
  assert.equal(t({ ps: -2, talent: 0.04 }), 1000);
});
