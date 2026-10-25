// v6c: handel wg Poradnika Staroświatowca — pora roku, wahania, strefy handlowe, nielegalne towary, podróż, własny interes.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import * as S from '../src/silnik.js';
import * as T from '../src/kupcy_trwali.js';
const rd = f => JSON.parse(fs.readFileSync(new URL('../' + f, import.meta.url)));
const d = Object.fromEntries(['cennik', 'kupcy', 'osady', 'koniunktura', 'rynek', 'nazwy', 'statusy', 'przedmioty_magiczne', 'czynsze', 'postacie', 'handel']
  .map(n => [n, rd(`data/${n}.json`)]));
const kon = id => d.koniunktura.koniunktury.find(k => k.id === id);
const os = id => d.osady.osady.find(o => o.id === id);

test('pora roku i wahania: zima drożej jedzenie, hossa drożej wszystko, bessa taniej', () => {
  const J = 'Jedzenie, picie, nocleg';
  const zima = S.koniunkturaEfektywna(d, kon('normalna'), { pora: 'zima' });
  assert.ok(S.cenaKoniunktury(zima, J) > 1.2);
  assert.equal(S.popytKoniunktury(zima, J), 1);
  assert.ok(S.cenaKoniunktury(S.koniunkturaEfektywna(d, kon('normalna'), { wahania: 'hossa' }), 'Pancerze') > 1);
  assert.ok(S.cenaKoniunktury(S.koniunkturaEfektywna(d, kon('normalna'), { wahania: 'bessa' }), 'Pancerze') < 1);
  assert.equal(S.wahaniaZRzutu(d, 1), 'hossa'); assert.equal(S.wahaniaZRzutu(d, 5), 'stabilny'); assert.equal(S.wahaniaZRzutu(d, 10), 'bessa');
});

test('ośrodki handlu z Poradnika: typ z populacji, zamożność w cenie, strefa zmienia kategorie', () => {
  const b = os('miasto-bogenhafen'), w = os('miasto-weissbruck'), n = os('miasto-nuln');
  assert.equal(b.dostepnosc, 'miasteczko'); assert.equal(w.dostepnosc, 'wioska'); assert.equal(n.typ, 'metropolia');
  assert.ok(n.mnoznik > os('metropolia').mnoznik, 'Nuln zamożność 5');
  const sk = S.generujKupca(d, { kupiec: 'kramarz', osada: 'miasto-salzenmund', seed: 3 });
  assert.ok(sk.towar.length > 0);
  assert.notEqual(os('miasto-salzenmund').kategorie['Ubranie i dodatki'].cena, undefined);
});

test('nielegalne towary tylko u pasera albo kupca z powiązaniami przestępczymi; cena wg zamożności', () => {
  const ma = (kupiec, x = {}) => Array.from({ length: 60 }, (_, i) => S.generujKupca(d, { kupiec, osada: 'metropolia', seed: i + 1, ...x }))
    .flatMap(s => s.towar).filter(t => d.cennik.pozycje.find(c => c.id === t.id).nielegalny);
  assert.equal(ma('kwatermistrz', { charaktery: ['dobry'] }).length, 0);
  const u = ma('paser');
  assert.ok(u.length > 0);
  assert.ok(u.every(t => t.skladowe.nielegalny === d.handel.zamoznosc.nielegalne['4'].cena));
});

test('zapisany kupiec: pora co 13 tygodni, wahania co 4, ceny jak w generatorze', () => {
  const sk = S.generujKupca(d, { kupiec: 'kramarz', osada: 'miasto', seed: 9, pora: 'zima', wahania: 'stabilny' });
  let K = T.utworzKupca(d, sk);
  const w = T.wycen(d, K);
  sk.towar.forEach(t => assert.equal(w.towar.find(x => x.id === t.id).cena_p, t.cena_p));
  K = T.uplywCzasu(d, K, 13);
  assert.equal(K.pora, 'wiosna');
  assert.ok(['stabilny', 'hossa', 'bessa'].includes(K.wahania));
  assert.equal(T.przenies(d, K, { pora: null }).pora, null);
});

test('podróż kupiecka i własny interes', () => {
  const z = S.podrozKupiecka(d, { km: 1000, teren: 'woda', pora: 'zima', seed: 7 });
  assert.ok(z.length > 0 && z.every(e => e.nazwa && e.km <= 1000));
  assert.ok(S.podrozKupiecka(d, { km: 1000, teren: 'lad', seed: 7 }).every(e => e.nazwa !== 'Piraci'));
  const a = S.dochodInteresu(d, { rodzaj: 'handel', jakosc: 'przecietna', ps: 5 });
  assert.equal(a.mnoznik, 2); assert.equal(a.nowa_jakosc, 'najlepsza');
  assert.equal(S.dochodInteresu(d, { jakosc: 'kiepska', ps: -2 }).nowa_jakosc, 'bankructwo');
});
