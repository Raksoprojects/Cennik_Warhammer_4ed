// Spójność cennika: reguły z data/spojnosc.json.
// Domyślnie sprawdza propozycja/cennik_v2.json; CENNIK=data/cennik.json node --test test/spojnosc.test.mjs – obecny.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
const rd = f => JSON.parse(fs.readFileSync(new URL('../' + f, import.meta.url)));
import { sprawdzReguly as sprawdz } from '../src/spojnosc.js';
export { sprawdz };
const plik = process.env.CENNIK || 'data/cennik.json';
test(`spójność: ${plik}`, () => {
  const bledy = sprawdz(rd(plik), rd('data/spojnosc.json').reguly);
  assert.deepEqual(bledy, [], '\n' + bledy.join('\n'));
});

/* --- v3: reguły strukturalne --- */
test('typ: usługi, nocleg i nieruchomości nie są towarem', () => {
  const cennik = rd(plik), rynek = rd('data/rynek.json');
  const zle = cennik.pozycje.filter(p => !p.typ);
  assert.deepEqual(zle.map(p => p.id), [], 'pozycje bez pola typ');
  const wykl = rynek.asortyment.wykluczone_typy;
  assert.ok(Array.isArray(wykl) && wykl.length, 'rynek.asortyment.wykluczone_typy musi istnieć');
  for (const p of cennik.pozycje) {
    if (p.kat === 'Czynsze i mieszkanie') assert.equal(p.typ, 'nieruchomosc', p.id);
    if (p.kat === 'Najmici i usługi (za tydzień)') assert.equal(p.typ, 'usluga', p.id);
  }
});

test('czynsze: cennik i czynsze.json podają to samo', () => {
  const cennik = rd(plik), cz = rd(process.env.CZYNSZE || 'data/czynsze.json');
  const C = Object.fromEntries(cennik.pozycje.map(x => [x.id, x.cena_p]));
  const slug = s => s.toLowerCase().replace(/ł/g, 'l').normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  const bledy = [];
  for (const k of cz.najem) for (const [okres, pole] of [['tydzien', 'tydzien_p'], ['miesiac', 'miesiac_p'], ['rok', 'rok_p']]) {
    const id = slug(k.kwatera) + '-' + okres;
    if (id in C && C[id] !== k[pole]) bledy.push(`${id}: cennik ${C[id]} ≠ czynsze ${k[pole]}`);
  }
  assert.deepEqual(bledy, [], '\n' + bledy.join('\n'));
});

test('ceny: wszystkie dodatnie i całkowite', () => {
  const cennik = rd(plik);
  const zle = cennik.pozycje.filter(p => !Number.isInteger(p.cena_p) || p.cena_p < 0);
  assert.deepEqual(zle.map(p => p.id), []);
});

test('id: unikalne', () => {
  const ids = rd(plik).pozycje.map(p => p.id);
  assert.equal(new Set(ids).size, ids.length);
});
