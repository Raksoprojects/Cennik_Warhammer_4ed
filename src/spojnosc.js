// Skarbiec Imperium — testy spójności cennika (bez DOM, bez zależności).
// Wspólne dla testów node (test/*.test.mjs) i aplikacji (przycisk „Sprawdź spójność” w panelu MG).
//
//   import { sprawdzWszystko } from './spojnosc.js';
//   const wynik = sprawdzWszystko(cennik, { reguly: spojnosc.reguly, testy: spojnosc_v4, czynsze, rynek });
//   // → [{ id, nazwa, bledy: [...], ostrzezenie: false }, ...]
//
// Błąd = cennik pozwala na arbitraż albo łamie zasadę domową. Ostrzeżenie = test oparty na szacunkach
// (rzemieślnik), pokazujemy, ale nie blokujemy.

const mapaCen = cennik => Object.fromEntries(cennik.pozycje.map(x => [x.id, x.cena_p]));

/* ------------------------------------------------------------ 59+ reguł z data/spojnosc.json */
export function sprawdzReguly(cennik, reguly) {
  const C = mapaCen(cennik);
  const g = i => { if (!(i in C)) throw new Error('Brak pozycji ' + i); return C[i]; };
  const sum = (ids, plus = []) => ids.reduce((s, i) => s + g(i), 0) + plus.reduce((s, [i, n]) => s + g(i) * n, 0);
  const bledy = [];
  for (const r of reguly) {
    let ok = true, opis = '';
    switch (r.typ) {
      case 'rosnaco': for (let k = 1; k < r.ids.length; k++) if (!(g(r.ids[k - 1]) < g(r.ids[k]))) { ok = false; opis += ` ${r.ids[k - 1]}=${g(r.ids[k - 1])} ≥ ${r.ids[k]}=${g(r.ids[k])}`; } break;
      case 'min': ok = g(r.a) >= g(r.b); opis = ` ${r.a}=${g(r.a)} < ${r.b}=${g(r.b)}`; break;
      case 'suma_min': ok = g(r.a) > sum(r.skladniki); opis = ` ${r.a}=${g(r.a)} ≤ ${sum(r.skladniki)}`; break;
      case 'max_suma': ok = g(r.a) <= sum(r.skladniki, r.plus); opis = ` ${r.a}=${g(r.a)} > ${sum(r.skladniki, r.plus)}`; break;
      case 'suma_zakres': { const q = g(r.a) / sum(r.skladniki); ok = q >= r.min && q <= r.max; opis = ` stosunek ${q.toFixed(2)}`; break; }
      case 'stosunek': { const q = g(r.a) / g(r.b); ok = q >= (r.min ?? -Infinity) && q <= (r.max ?? Infinity); opis = ` stosunek ${q.toFixed(2)}`; break; }
      case 'zakres': ok = g(r.a) >= r.min && g(r.a) <= r.max; opis = ` ${g(r.a)}`; break;
      default: throw new Error('Nieznany typ reguły ' + r.typ);
    }
    if (!ok) bledy.push(r.opis + ':' + opis);
  }
  return bledy;
}

/* ------------------------------------------------------------ testy arbitrażu z data/spojnosc_v4.json */
export function sprawdzArbitraz(cennik, T) {
  const C = mapaCen(cennik);
  const ma = (...ids) => ids.every(i => i in C);           // pomija pozycje, których cennik nie ma
  const material = id => Object.entries(T.receptury.pozycje[id])
    .reduce((s, [k, n]) => s + (k.startsWith('_') ? n : (C[k] ?? NaN) * n), 0);
  const wynik = [];
  const dodaj = (id, nazwa, bledy, ostrzezenie = false) => wynik.push({ id, nazwa, bledy, ostrzezenie });

  dodaj('receptury', 'materiał ≤ produkt', Object.keys(T.receptury.pozycje)
    .filter(i => ma(i) && !Number.isNaN(material(i)) && C[i] < material(i))
    .map(i => `${i}: ${C[i]} < materiał ${material(i)}`));

  dodaj('naczynia', 'pełne naczynie ≥ puste + zawartość', T.naczynia
    .filter(n => ma(n.pelne, n.puste) && C[n.pelne] < C[n.puste] + n.zawartosc_min_p)
    .map(n => `${n.pelne} ${C[n.pelne]} < ${n.puste} ${C[n.puste]} + ${n.zawartosc_min_p}`));

  dodaj('rodziny', 'rodziny rzeczy', T.rodziny
    .filter(r => ma(r.a, r.b)).map(r => [r, C[r.a] / C[r.b]])
    .filter(([r, q]) => q < r.min || q > r.max).map(([r, q]) => `${r.opis}: ${q.toFixed(2)} poza [${r.min}; ${r.max}]`));

  dodaj('tusze', 'tusza vs żywe zwierzę', Object.entries(T.tusze.kg)
    .filter(([i]) => ma(i, T.tusze.mieso)).map(([i, kg]) => [i, C[T.tusze.mieso] * kg / C[i]])
    .filter(([, q]) => q < T.tusze.min || q > T.tusze.max).map(([i, q]) => `${i}: ${q.toFixed(2)}`));

  {
    const zG = 240 / T.kruszec.zk_gram_zlota, sG = zG / T.kruszec.zloto_do_srebra;
    dodaj('kruszec', 'biżuteria vs kruszec monety', T.kruszec.pozycje.filter(p => ma(p.id))
      .filter(p => C[p.id] > p.g * (p.metal === 'zloto' ? zG : sG) * T.kruszec.max_krotnosc)
      .map(p => `${p.id}: ${C[p.id]} > ${T.kruszec.max_krotnosc}× kruszcu — przetopione monety dają zysk`));
  }
  {
    const B = T.budzet, b = [];
    if (ma('plotno-lokiec', 'sukno-szare-lokiec')) {
      const jedz = 7 * B.jedzenie_dzien_p;
      const odz = Object.entries(B.odziez_rok).reduce((s, [i, n]) => s + C[i] * n, 0) / 52;
      for (const p of B.progi) {
        const s = jedz + C[p.kwatera] / p.tygodni + odz, u = B.udzial_utrzymania * p.brutto_tydz_p;
        if (s > u) b.push(`${p.status}: ${s.toFixed(0)} p > utrzymanie ${u.toFixed(0)} p/tydz.`);
      }
      for (const p of B.czynsz_najemcy) if (C[p.kwatera] / 4.33 > B.max_udzial_czynszu * p.brutto_tydz_p)
        b.push(`${p.kwatera} > ${B.max_udzial_czynszu * 100}% brutto (${p.status})`);
    }
    dodaj('budzet', 'budżet utrzymania', b);
  }
  dodaj('karczma', 'karczma vs najem', T.karczma.pary.filter(p => ma(p.najem, p.noc))
    .map(p => [p, C[p.najem] / (30 * C[p.noc])]).filter(([, q]) => q < T.karczma.min || q > T.karczma.max)
    .map(([p, q]) => `${p.najem}: ${q.toFixed(2)} × miesiąc w karczmie`));

  dodaj('zwrot', 'zwrot z kupna domu', T.zwrot.filter(z => ma(z.kupno, z.najem))
    .map(z => [z, C[z.kupno] / C[z.najem]]).filter(([z, q]) => q < z.min || q > z.max)
    .map(([z, q]) => `${z.kupno}: ${q.toFixed(0)} lat`));

  {
    const R = T.rzemieslnik, b = [];
    for (const w of R.wzorce) {
      if (!ma(w.id)) continue;
      const mat = w.material_p ?? (w.id in T.receptury.pozycje ? material(w.id) : 0);
      const q = C[w.id] / (w.dni * R.warsztaty_p_dzien[w.warsztat] + mat);
      if (q < R.min || q > R.max) b.push(`${w.id}: cena = ${q.toFixed(1)}× kosztu warsztatu (norma ${R.min}–${R.max})`);
    }
    dodaj('rzemieslnik', 'test rzemieślnika (szacunki — tylko ostrzeżenie)', b, true);
  }
  return wynik;
}

/* ------------------------------------------------------------ strukturalne */
export function sprawdzStrukture(cennik, { rynek, czynsze } = {}) {
  const b = [];
  const ids = cennik.pozycje.map(p => p.id);
  if (new Set(ids).size !== ids.length) b.push('powtórzone id');
  for (const p of cennik.pozycje) {
    if (!Number.isInteger(p.cena_p) || p.cena_p < 0) b.push(`${p.id}: cena ${p.cena_p} nie jest dodatnią liczbą całkowitą`);
    if (!p.typ) b.push(`${p.id}: brak pola typ`);
  }
  if (czynsze) {
    const C = mapaCen(cennik);
    const slug = s => s.toLowerCase().replace(/ł/g, 'l').normalize('NFD').replace(/[̀-ͯ]/g, '')
      .replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
    for (const k of czynsze.najem) for (const [okres, pole] of [['tydzien', 'tydzien_p'], ['miesiac', 'miesiac_p'], ['rok', 'rok_p']]) {
      const id = slug(k.kwatera) + '-' + okres;
      if (id in C && C[id] !== k[pole]) b.push(`${id}: cennik ${C[id]} ≠ czynsze ${k[pole]}`);
    }
  }
  return b;
}

/* ------------------------------------------------------------ wszystko naraz (panel MG) */
export function sprawdzWszystko(cennik, { reguly, testy, czynsze, rynek } = {}) {
  const out = [];
  if (reguly) out.push({ id: 'reguly', nazwa: `reguły spójności (${reguly.length})`, bledy: sprawdzReguly(cennik, reguly), ostrzezenie: false });
  if (testy) out.push(...sprawdzArbitraz(cennik, testy));
  out.push({ id: 'struktura', nazwa: 'struktura cennika i czynsze', bledy: sprawdzStrukture(cennik, { rynek, czynsze }), ostrzezenie: false });
  return out;
}
