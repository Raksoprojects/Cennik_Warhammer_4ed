// v6: zapisany kupiec (src/kupcy_trwali.js) i nowe warstwy ustawień MG (kategorie, nowe pozycje).
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import * as S from '../src/silnik.js';
import * as T from '../src/kupcy_trwali.js';
const rd = f => JSON.parse(fs.readFileSync(new URL('../' + f, import.meta.url)));
const d = Object.fromEntries(['cennik', 'kupcy', 'osady', 'koniunktura', 'rynek', 'nazwy', 'statusy', 'przedmioty_magiczne', 'czynsze']
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
