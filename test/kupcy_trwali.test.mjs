// v6: zapisany kupiec (src/kupcy_trwali.js) i nowe warstwy ustawień MG (kategorie, nowe pozycje).
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import * as S from '../src/silnik.js';
import * as T from '../src/kupcy_trwali.js';
const rd = f => JSON.parse(fs.readFileSync(new URL('../' + f, import.meta.url)));
const d = Object.fromEntries(['cennik', 'kupcy', 'osady', 'koniunktura', 'rynek', 'nazwy', 'statusy', 'przedmioty_magiczne', 'czynsze', 'postacie']
  .map(n => [n, rd(`data/${n}.json`)]));
d.klasy = rd('data/klasy_cenowe.json');
const sklep = S.generujKupca(d, { kupiec: 'zbrojmistrz', osada: 'altdorf', koniunktura: 'wojna', seed: 48213 });

test('zapisany kupiec ma te same ceny co wygenerowany sklep', () => {
  const K = T.utworzKupca(d, sklep), w = T.wycen(d, K);
  assert.equal(K.imie, sklep.imie);
  assert.equal(K.gotowka_p, sklep.gotowka_p);
  assert.equal(w.towar.length, sklep.towar.length);
  sklep.towar.forEach((t, i) => {
    const x = w.towar[i];
    assert.equal(x.id, t.id);
    for (const k of ['sztuk', 'cena_p', 'cena_min_p', 'skup_p', 'koszt_p', 'popyt', 'zapas']) assert.equal(x[k], t[k], `${t.id}.${k}`);
  });
});

test('modyfikator MG i cena ręczna', () => {
  let K = T.utworzKupca(d, sklep);
  const przed = T.wycen(d, K).towar[0];
  K.modyfikator = 0.9;
  assert.equal(T.wycen(d, K).towar[0].cena_p, Math.round(przed.cena_wytworcy_p * przed.mnoznik * 0.9));
  K = T.zmienPozycje(K, przed.id, { cena_reczna_p: 1234 });
  assert.equal(T.wycen(d, K).towar[0].cena_p, 1234);
});

test('przeniesienie i zmiana sytuacji przeliczają ceny, dziennik to zapisuje', () => {
  const K = T.utworzKupca(d, sklep);
  const K2 = T.przenies(d, K, { osada: 'wies', koniunktura: 'normalna' });
  assert.equal(K.osada, 'altdorf', 'wejście bez zmian');
  const a = T.wycen(d, K).towar[0], b = T.wycen(d, K2).towar[0];
  assert.ok(b.cena_p < a.cena_p);
  assert.match(K2.dziennik.at(-1).tekst, /Wieś/);
});

test('towar spoza asortymentu wymaga decyzji MG', () => {
  const K = T.utworzKupca(d, sklep);
  const r = T.dodajPozycje(d, K, 'kapelusz');
  assert.equal(r.blad, 'poza_asortymentem');
  const K2 = T.dodajPozycje(d, K, 'kapelusz', { wymus: true });
  assert.ok(K2.towar.find(w => w.id === 'kapelusz').poza_asortymentem);
});

test('transakcje zmieniają ilość i gotówkę', () => {
  const K = T.utworzKupca(d, sklep), w = T.wycen(d, K).towar.find(x => x.sztuk > 0);
  const K2 = T.transakcja(d, K, { id: w.id, typ: 'kupno', ilosc: 1, cena_p: w.cena_p });
  assert.equal(K2.gotowka_p, K.gotowka_p + w.cena_p);
  assert.equal(K2.towar.find(x => x.id === w.id).sztuk, w.sztuk - 1);
  assert.equal(T.transakcja(d, K, { id: w.id, typ: 'sprzedaz', ilosc: 1, cena_p: K.gotowka_p + 1 }).blad, 'brak_gotowki');
});

test('zamówienie: odmowa bez decyzji, zaliczka, gotowe po terminie, odbiór', () => {
  const kowal = T.utworzKupca(d, S.generujKupca(d, { kupiec: 'kowal', osada: 'wies', seed: 1 }));
  assert.equal(T.zamow(d, kowal, { id: 'ksiega' }).blad ?? T.zamow(d, kowal, { id: 'kodeks' }).blad, 'odmowa');
  const K = T.utworzKupca(d, sklep);
  const K2 = T.zamow(d, K, { id: 'miecz', dla: 'Ulryka' });
  const z = K2.zamowienia[0];
  assert.equal(K2.gotowka_p, K.gotowka_p + z.zaliczka_p);
  const K3 = T.uplywCzasu(d, K2, z.tydzien_gotowe);
  assert.equal(K3.zamowienia[0].status, 'gotowe');
  const K4 = T.odbierzZamowienie(K3, z.uid);
  assert.equal(K4.gotowka_p, K3.gotowka_p + z.cena_p - z.zaliczka_p);
});

test('upływ czasu: powtarzalny, sprzedaje, dokupuje, pisze dziennik', () => {
  const K = T.utworzKupca(d, sklep);
  const A = T.uplywCzasu(d, K, 6), B = T.uplywCzasu(d, K, 6);
  assert.deepEqual(A.towar, B.towar);
  assert.equal(A.tydzien, 6);
  assert.match(A.dziennik.at(-1).tekst, /Minęło 6 tyg\./);
  assert.ok(A.towar.every(w => w.sztuk >= 0));
  assert.notDeepEqual(A.towar.map(w => w.sztuk), K.towar.map(w => w.sztuk));
});

test('dogenerowanie dodaje nowe pozycje z asortymentu', () => {
  const K = T.utworzKupca(d, sklep), K2 = T.dogeneruj(d, K, { ile: 3 });
  assert.ok(K2.towar.length > K.towar.length);
  assert.ok(K2.towar.every(w => T.czyWAsortymencie(d, K2, w.id).ok));
});

test('wóz na zamówienie: kowal i kołodziej robią, wieś daje materiał', () => {
  for (const kupiec of ['kowal', 'kolodziej']) {
    const z = S.wycenZamowienie(d, { kupiec, osada: 'wies', przedmiot: 'woz', seed: 1 });
    assert.equal(z.status, 'wykonuje', kupiec);
    const m = S.wycenZamowienie(d, { kupiec, osada: 'wies', przedmiot: 'woz', material: true, seed: 1 });
    assert.equal(m.cena_p, Math.round(z.cena_p * d.rynek.zamowienie.material_wlasny));
    assert.equal(m.termin, z.termin, 'materiał nie skraca roboty');
  }
  assert.ok(S.wycenZamowienie(d, { kupiec: 'kowal', osada: 'wies', przedmiot: 'krowa' }).status === 'odmowa', 'kowal nie robi krów');
  assert.ok(S.ktoRobi(d, 'Zwierzęta i pojazdy', 'woz').some(k => k.id === 'kolodziej'));
});

test('jakość w sklepie: mistrz cechu ma Zalety, paser Wady; zapisany kupiec liczy tak samo', () => {
  const ile = (kupiec, co) => [1, 2, 3, 4, 5, 6, 7, 8].flatMap(seed => S.generujKupca(d, { kupiec, osada: 'metropolia', seed }).towar)
    .filter(t => t.jakosc && (co === 'z' ? t.jakosc.mnoznik > 1 : t.jakosc.mnoznik < 1)).length;
  assert.ok(ile('mistrzcechu', 'z') > 0);
  assert.equal(ile('mistrzcechu', 'w'), 0);
  assert.ok(ile('paser', 'w') > 0);
  const sk = S.generujKupca(d, { kupiec: 'mistrzcechu', osada: 'metropolia', seed: 3 });
  const t = sk.towar.find(x => x.jakosc);
  assert.ok(t, 'seed 3 ma egzemplarz z jakością');
  assert.equal(t.cena_wytworcy_p, Math.round(t.cena_cennik_p * t.jakosc.mnoznik));
  const w = T.wycen(d, T.utworzKupca(d, sk)).towar.find(x => x.id === t.id);
  assert.equal(w.cena_p, t.cena_p);
});

test('asortyment v6b: branże, Dostępność, pochodzenie', () => {
  const sklepy = (kupiec, osada = 'miasto') => Array.from({ length: 40 }, (_, i) => S.generujKupca(d, { kupiec, osada, seed: i + 1 }).towar).flat();
  const P = Object.fromEntries(d.cennik.pozycje.map(c => [c.id, c]));
  const wszystko = d.kupcy.kupcy.flatMap(k => sklepy(k.id));
  assert.ok(!wszystko.some(t => t.id === 'tatuaz'), 'tatuaż to usługa');
  assert.ok(!wszystko.some(t => P[t.id].dostepnosc === 'Egzotyczna' && !P[t.id].pochodzenie), 'egzotyki tylko na zamówienie');
  assert.ok(!sklepy('blawatny').some(t => /beczk|beczu/.test(t.id)), 'bławatny bez beczek');
  assert.ok(!sklepy('kowal', 'wies').some(t => ['teleskop', 'lusterko-reczne', 'rapier'].includes(t.id)));
  const bugman = k => sklepy(k).filter(t => t.id === 'pol-litra-piwa-bugmana').length;
  assert.ok(bugman('krasnolud') > bugman('kramarz'), 'Bugman częściej u krasnoluda');
  const wies = sklepy('kramarz', 'wies').map(t => P[t.id].dostepnosc);
  assert.ok(wies.filter(x => x === 'Ograniczona').length < wies.filter(x => x === 'Powszechna').length);
});

test('zamówienie rzadkiej rzeczy: dłużej i drożej, egzotyk we wsi — odmowa', () => {
  const miasto = S.wycenZamowienie(d, { kupiec: 'zbrojmistrz', osada: 'miasto', przedmiot: 'rapier', seed: 1 });
  const wies = S.wycenZamowienie(d, { kupiec: 'zbrojmistrz', osada: 'wies', przedmiot: 'rapier', seed: 1 });
  assert.ok(wies.rzadkosc && wies.rzadkosc.termin_tyg > 0);
  assert.ok(wies.skladowe.narzut > miasto.skladowe.narzut, 'we wsi narzut za rzadkość');
  assert.equal(S.wycenZamowienie(d, { kupiec: 'zbrojmistrz', osada: 'wies', przedmiot: 'flamberg', seed: 1 }).status, 'odmowa');
});

test('postać kupca: filtr charakteru, cecha działa na ceny, zapisany kupiec liczy tak samo', () => {
  for (const ch of ['dobry', 'neutralny', 'zly']) for (let s = 1; s <= 15; s++) {
    const p = S.generujKupca(d, { kupiec: 'kramarz', osada: 'miasto', seed: s, charaktery: [ch] }).postac;
    assert.equal(p.charakter, ch);
    assert.ok(!p.motywacja.charakter || p.motywacja.charakter === ch);
    assert.equal(p.wyglad.length, 2);
  }
  const chciwy = Array.from({ length: 300 }, (_, i) => S.generujKupca(d, { kupiec: 'zbrojmistrz', osada: 'miasto', seed: i, charaktery: ['zly'] }))
    .find(s => s.postac.cecha.nazwa === 'Chciwy');
  assert.ok(chciwy, 'jest Chciwy wśród złych');
  assert.ok(chciwy.towar.every(t => t.skladowe.charakter === 1.1));
  const w = T.wycen(d, T.utworzKupca(d, chciwy));
  chciwy.towar.forEach(t => assert.equal(w.towar.find(x => x.id === t.id).cena_p, t.cena_p));
});

test('towar trefny: paser większość, szarlatan ponad połowę i świadomie, uczciwy nigdy', () => {
  const udzial = sklepy => { const t = sklepy.flatMap(s => s.towar); return t.filter(x => x.trefny).length / t.length; };
  const gen = (kupiec, n = 40, x = {}) => Array.from({ length: n }, (_, i) => S.generujKupca(d, { kupiec, osada: 'miasto', seed: i + 1, ...x }));
  assert.ok(udzial(gen('paser')) > 0.6);
  assert.ok(udzial(gen('rzemieslnik')) < 0.1);
  const zli = gen('kramarz', 300, { charaktery: ['zly'] });
  const szarlatan = zli.filter(s => s.postac.cecha.nazwa === 'Szarlatan');
  assert.ok(szarlatan.length && udzial(szarlatan) > 0.5);
  assert.ok(szarlatan.flatMap(s => s.towar).filter(t => t.trefny).every(t => t.trefny.swiadomy));
  const uczciwi = gen('paser', 300, { charaktery: ['dobry'] }).filter(s => s.postac.cecha.nazwa === 'Skrupulatnie uczciwy');
  assert.ok(uczciwi.length && udzial(uczciwi) === 0);
});

test('ustawienia v6: mnożnik kategorii i nowe pozycje MG', () => {
  const C = Object.fromEntries(d.cennik.pozycje.map(c => [c.id, c.cena_p]));
  const n = S.zastosujUstawienia(d, { kategorie: { 'Pancerze': 1.5 },
    nowe: [{ id: 'lutnia-mg', nazwa: 'Lutnia', kat: 'Wyposażenie różne', cena_p: 480 }], pozycje: { 'lutnia-mg': { mnoznik: 2 } } });
  const N = Object.fromEntries(n.cennik.pozycje.map(c => [c.id, c]));
  assert.equal(N.kolczuga.cena_p, Math.round(C.kolczuga * 1.5));
  assert.equal(N.miecz.cena_p, C.miecz);
  assert.equal(N['lutnia-mg'].cena_p, 960);
  assert.equal(N['lutnia-mg'].typ, 'towar');
});
