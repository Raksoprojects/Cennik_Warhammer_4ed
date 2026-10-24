// Testy arbitrażu i spójności v4/v5: data/spojnosc_v4.json, logika w src/spojnosc.js (wspólna z aplikacją).
// Domyślnie obowiązujący cennik; CENNIK=propozycja/cennik_v4_zalecany.json node --test test/arbitraz.test.mjs
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { sprawdzArbitraz } from '../src/spojnosc.js';
const rd = f => JSON.parse(fs.readFileSync(new URL('../' + f, import.meta.url)));
const plik = process.env.CENNIK || 'data/cennik.json';
for (const w of sprawdzArbitraz(rd(plik), rd('data/spojnosc_v4.json'))) {
  if (w.ostrzezenie) test(`${w.nazwa} — ${plik}`, t => { for (const b of w.bledy) t.diagnostic(b); });
  else test(`${w.nazwa} — ${plik}`, () => assert.deepEqual(w.bledy, [], '\n' + w.bledy.join('\n')));
}
