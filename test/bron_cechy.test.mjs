// Cechy broni (data/bron_cechy.json, z narzedzia/dodaj_v6.py) i jakość egzemplarza (PG s. 292, HR-024).
// Cechy broni (Szybka, Precyzyjna…) są w cenie wariantu podstawowego — nie porównuje się po nich cen różnych broni.
// Cenę zmieniają Zalety i Wady PRZEDMIOTU: każda Zaleta (każdy poziom Wyśmienity / Wytrzymały) ×2, każda Wada ×½.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import * as S from '../src/silnik.js';
const rd = f => JSON.parse(fs.readFileSync(new URL('../' + f, import.meta.url)));

test('cechy broni: każda broń z cennika ma wpis, wpisy wskazują istniejące pozycje', () => {
  const C = rd('data/cennik.json'), B = rd('data/bron_cechy.json');
  const ids = new Set(C.pozycje.map(p => p.id)), wpisy = new Set(B.pozycje.map(p => p.id));
  const bron = C.pozycje.filter(p => p.kat === 'Broń biała' || p.kat === 'Broń zasięgowa').map(p => p.id);
  assert.deepEqual(bron.filter(i => !wpisy.has(i)), []);
  assert.deepEqual([...wpisy].filter(i => !ids.has(i)), []);
});

test('jakość egzemplarza: poziomy Zalet mnożą, Wady dzielą (PG s. 292; v6b: ×1,6 i ×0,6)', () => {
  const d = { rynek: rd('data/rynek.json') };
  const m = c => +S.jakoscZ(d, c).mnoznik.toFixed(4);
  assert.equal(m({ 'Wytrzymały': 2, 'Wyśmienity': 2 }), 6.5536);
  assert.equal(m({ 'Wyśmienity': 1, 'Wytrzymały': 1 }), 2.56);   // przykład ze szpadą
  assert.equal(m({ 'Nieporęczny': 1, 'Zawodny': 1 }), 0.36);     // przykład z kolczugą
  assert.equal(m({ 'Poręczny': 1, 'Tandetny': 1 }), 0.96);
  assert.equal(m({ 'Zaleta broni: Szybka': 1, 'Bez Wady: Tępa': 1 }), 2.56);  // niezwykłe = Zalety
  assert.equal(S.jakoscZ(d, 'wysmienita').mnoznik, 1.6);
  assert.throws(() => S.jakoscZ(d, { 'Ostra': 1 }));
});
