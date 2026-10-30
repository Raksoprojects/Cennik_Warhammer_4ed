// Pomocnicze wyliczenia do widoków (bez losowania). Wzory jak w silniku.
import { osobowoscKupca, cenaKoniunktury, koniunkturaEfektywna, mnoznikLokalny, mnoznikNielegalny } from '../silnik.js';
import type { Dane } from './dane';

export const ZRODLA: Record<string, string> = {
  PG: 'Podręcznik główny', PB: '„Pod Bronią”', KR: 'Podręcznik „Krasnoludy”', WE: 'Podręcznik „Wysokie Elfy”',
};
export const zrodloNazwa = (z: string | null, strona?: number | null) =>
  (z ? ZRODLA[z] ?? z : 'pozycja kampanii') + (strona ? `, s. ${strona}` : z === 'PB' ? ' (strona nieznana)' : '');
export const TYPY: Record<string, string> = { towar: 'towar', nocleg: 'nocleg', usluga: 'usługa', nieruchomosc: 'nieruchomość' };

// Mnożnik klasy w bieżącym presecie z ustawieniami MG i premia znaku stanu (miecze).
export function mnoznikKlasy(d: Dane, ust: any, c: any) {
  const K = d.klasy, pr = K.presety[ust.preset || K.domyslny] ?? K.presety[K.domyslny];
  const m = { ...pr.mnozniki, ...(ust.mnozniki || {}) }[c.klasa] ?? 1;
  const znak = K.znak_stanu.includes(c.id) ? (ust.premia_znak_stanu ?? pr.premia_znak_stanu ?? 1) : 1;
  return { m, znak };
}
// Cena u kupca bez losowych składników (kaprys = 1, zapas i popyt normalne). Uwzględnia strefę handlową osady (v6c).
export function cenaTypowa(d: Dane, kup: any, lok: any, kon: any, c: any) {
  const os = osobowoscKupca(d, kup, c, null);
  return Math.round(c.cena_p * kup.marza * os.mnoznik * lok.mnoznik * cenaKoniunktury(koniunkturaEfektywna(d, kon, { osada: lok }), c.kat)
    * mnoznikLokalny(lok, c) * mnoznikNielegalny(d, lok, c));
}
// Kupcy, którzy mają tę rzecz w asortymencie (kategoria i branże; nielegalne tylko u pasera).
export const handlujacy = (d: Dane, c: any) =>
  d.kupcy.kupcy.filter((k: any) => (k.rdzen.includes(c.kat) || k.boczne.includes(c.kat))
    && (!k.branze?.[c.kat] || c.branze?.some((t: string) => k.branze[c.kat].includes(t)))
    && (!c.nielegalny || k.nielegalne));
export const tygodniePracy = (d: Dane, p: number) => p / d.statusy.robotnik_brutto_p;
// Roboty (netto) do odłożenia: chłop / robotnik (Brąz 3) i mistrz z czeladnikami (Srebro 3).
export const POROWNANIE = ['Brąz 3', 'Srebro 3'];
export const robot = (d: Dane, p: number, status: string) => p / d.statusy.poziomy.find((s: any) => `${s.tier} ${s.lvl}` === status).netto_p;
