// T11: Zalety i Wady broni (data/bron_cechy.json, z narzedzia/dodaj_v6.py).
// Struktura musi się zgadzać. Naruszenia „więcej Zalet = nie taniej” to raport dla MG — test je wypisuje, nie blokuje.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { sprawdzCechyBroni } from '../src/spojnosc.js';
const rd = f => JSON.parse(fs.readFileSync(new URL('../' + f, import.meta.url)));

test('cechy broni: każda broń z cennika ma wpis, wpisy wskazują istniejące pozycje', () => {
  const C = rd('data/cennik.json'), B = rd('data/bron_cechy.json');
  const ids = new Set(C.pozycje.map(p => p.id)), wpisy = new Set(B.pozycje.map(p => p.id));
  const bron = C.pozycje.filter(p => p.kat === 'Broń biała' || p.kat === 'Broń zasięgowa').map(p => p.id);
  assert.deepEqual(bron.filter(i => !wpisy.has(i)), []);
  assert.deepEqual([...wpisy].filter(i => !ids.has(i)), []);
});

test('cechy broni: raport naruszeń dla MG', t => {
  const bledy = sprawdzCechyBroni(rd('data/cennik.json'), rd('data/bron_cechy.json'));
  t.diagnostic(`${bledy.length} par do przejrzenia`);
  for (const b of bledy) t.diagnostic(b);
});
