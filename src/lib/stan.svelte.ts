// Stan aplikacji: ustawienia MG (cennik na żywo), baza zapisanych kupców, trasa z #hash.
// localStorage zawsze w try/catch — aplikacja działa bez niego (tryb prywatny, zablokowane dane strony).
import { zastosujUstawienia } from '../silnik.js';
import { daneBazowe, ustawieniaDomyslne, type Dane } from './dane';
import { dzis } from './format';

const KLUCZ_UST = 'skarbiec-ustawienia-v5', KLUCZ_KUPCY = 'skarbiec-kupcy-v1';
function czytaj<T>(klucz: string, dom: T): T {
  try { const s = localStorage.getItem(klucz); if (s) return JSON.parse(s); } catch { /* brak dostępu */ }
  return dom;
}
function pisz(klucz: string, v: unknown) { try { localStorage.setItem(klucz, JSON.stringify(v)); } catch { /* brak dostępu */ } }

export function pusteUstawienia(): any {
  const { przyklad, opis, ...r } = structuredClone(ustawieniaDomyslne);
  return { kategorie: {}, nowe: [], ...r };
}

export interface Trasa { widok: string; sciezka: string; param: URLSearchParams }
function czytajTrase(): Trasa {
  const h = decodeURIComponent(location.hash.slice(1));
  const [p, q = ''] = h.split('?'), [widok = 'cennik', ...reszta] = p.split('/');
  return { widok: widok || 'cennik', sciezka: reszta.join('/'), param: new URLSearchParams(q) };
}

class Stan {
  ust = $state<any>({ ...pusteUstawienia(), ...czytaj(KLUCZ_UST, {}) });
  kupcy = $state<any[]>(czytaj(KLUCZ_KUPCY, []));
  trasa = $state<Trasa>(czytajTrase());

  // Dane po ustawieniach MG. Błędne ustawienia → dane domyślne + komunikat.
  wynik = $derived.by((): { d: Dane; blad: string | null } => {
    try { return { d: zastosujUstawienia(daneBazowe, $state.snapshot(this.ust)), blad: null }; }
    catch (e) { return { d: zastosujUstawienia(daneBazowe, pusteUstawienia()), blad: (e as Error).message }; }
  });
  get d(): Dane { return this.wynik.d; }
  get wlasne() { return JSON.stringify($state.snapshot(this.ust)) !== JSON.stringify(pusteUstawienia()); }

  ustaw(nowe: any) { this.ust = nowe; pisz(KLUCZ_UST, nowe); }
  // Zmiana w miejscu na kopii: stan.zmienUst(u => { u.mnozniki.bron = 2.5; })
  zmienUst(fn: (u: any) => void) { const u = structuredClone($state.snapshot(this.ust)); fn(u); this.ustaw(u); }
  przywrocUst() { this.ustaw(pusteUstawienia()); try { localStorage.removeItem(KLUCZ_UST); } catch { /* brak dostępu */ } }

  kupiec(uid: string) { return this.kupcy.find(k => k.uid === uid); }
  zapiszKupca(K: any) {
    const k = { ...K, zmieniony: dzis() }, i = this.kupcy.findIndex(x => x.uid === k.uid);
    this.kupcy = i < 0 ? [...this.kupcy, k] : this.kupcy.map((x, j) => j === i ? k : x);
    pisz(KLUCZ_KUPCY, this.kupcy);
  }
  usunKupca(uid: string) { this.kupcy = this.kupcy.filter(k => k.uid !== uid); pisz(KLUCZ_KUPCY, this.kupcy); }
  // Import pliku: kupcy o tym samym uid są zastępowani, reszta dopisana.
  importujKupcow(lista: any[]) {
    const m = new Map(this.kupcy.map(k => [k.uid, k]));
    for (const k of lista) if (k?.uid && Array.isArray(k.towar)) m.set(k.uid, k);
    this.kupcy = [...m.values()]; pisz(KLUCZ_KUPCY, this.kupcy);
  }

  idz(hash: string) { location.hash = hash; }
  odswiezTrase() { this.trasa = czytajTrase(); }
}
export const stan = new Stan();
addEventListener('hashchange', () => stan.odswiezTrase());
