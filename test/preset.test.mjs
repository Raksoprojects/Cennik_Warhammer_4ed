// zastosujPreset w silniku daje to samo co gotowe pliki:
//   preset domyślny (zalecany v5) = data/cennik.json
//   zalecany_v4, drogi            = propozycja/cennik_v4_*.json (archiwum v4)
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { zastosujPreset } from '../src/silnik.js';
const rd = f => JSON.parse(fs.readFileSync(new URL('../' + f, import.meta.url)));
const cennik = rd('data/cennik.json'), K = rd('data/klasy_cenowe.json');
// Pozycje dopisane po archiwum (np. nocleg w stajni, v5.2) nie mają wzoru — pomijamy je.
const porownaj = (wynik, wzor) => {
  const wz = Object.fromEntries(wzor.pozycje.map(p => [p.id, p.cena_p]));
  return wynik.pozycje.filter(p => p.id in wz && p.cena_p !== wz[p.id]).map(p => `${p.id}: ${p.cena_p} ≠ ${wz[p.id]}`);
};
test(`preset domyślny (${K.domyslny}) = data/cennik.json`, () => {
  assert.deepEqual(porownaj(zastosujPreset(cennik, K, K.domyslny), cennik), []);
});
// v5 poprawiło bazę flambergu i łuku elfiego oraz klasę arkanu — te dwie pozycje celowo różnią się od archiwum v4.
// v6 (decyzja MG): łuki i kusze — porządny łuk 2 ZK, kusza 4 ZK, rodziny w tych samych proporcjach.
const ZMIENIONE_W_V5 = new Set(['flamberg', 'arkan', 'luk-elfi',
  'krotki-luk', 'luk', 'luk-dlugi', 'kusza', 'ciezka-kusza', 'kusza-pistoletowa', 'miecz', 'bulat']);   // v6b/v6c: miecz i bułat 3 ZK
for (const [pr, plik] of [['zalecany_v4', 'zalecany'], ['drogi', 'drogi']]) test(`preset ${pr} = propozycja/cennik_v4_${plik}.json`, () => {
  const roznice = porownaj(zastosujPreset(cennik, K, pr), rd(`propozycja/cennik_v4_${plik}.json`))
    .filter(r => !ZMIENIONE_W_V5.has(r.split(':')[0]));
  assert.deepEqual(roznice, []);
});
test('każda klasa z cennika ma mnożnik w każdym presecie', () => {
  const klasy = new Set(cennik.pozycje.map(p => p.klasa));
  const braki = [];
  for (const [n, pr] of Object.entries(K.presety)) for (const k of klasy) if (!(k in pr.mnozniki)) braki.push(`${n}: ${k}`);
  assert.deepEqual(braki, []);
});
