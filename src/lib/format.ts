// Formatowanie do wyświetlania i pliki. Obliczenia zawsze na liczbach (pensach).
export { mon, proc, norm } from '../silnik.js';

export const pl = (n: number, dec = 2) => (n.toFixed(dec).replace(/\.?0+$/, '') || '0').replace('.', ',');
export const mnoz = (m: number) => '×' + pl(m);

// „4 ZK”, „15 s 6 p”, „1 ZK 2 s”, „300” (pensy) → pensy; null = puste; NaN = nie rozumiem
export function parsujCene(txt: string): number | null {
  const s = String(txt).trim().toLowerCase().replace(',', '.');
  if (!s) return null;
  if (/^\d+(\.\d+)?$/.test(s)) return Math.round(+s);
  let p = 0, ok = false;
  for (const m of s.matchAll(/(\d+(?:\.\d+)?)\s*(zk|s|p)\b/g)) { ok = true; p += +m[1] * ({ zk: 240, s: 12, p: 1 } as any)[m[2]]; }
  return ok ? Math.round(p) : NaN;
}
// „0,9”, „-10%”, „+15%”, „1.2” → mnożnik; null = puste; NaN = nie rozumiem
export function parsujMnoznik(txt: string): number | null {
  const s = String(txt).trim().replace(',', '.').replace('×', '').replace(/\s/g, '');
  if (!s) return null;
  const m = /^([+-]?\d+(?:\.\d+)?)%$/.exec(s);
  if (m) return 1 + +m[1] / 100;
  return /^\d+(\.\d+)?$/.test(s) ? +s : NaN;
}

export function pobierzPlik(nazwa: string, dane: unknown) {
  const a = Object.assign(document.createElement('a'), {
    href: URL.createObjectURL(new Blob([JSON.stringify(dane, null, 1)], { type: 'application/json' })), download: nazwa });
  document.body.append(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
}
export async function wczytajPlik(e: Event): Promise<any> {
  const inp = e.currentTarget as HTMLInputElement, f = inp.files?.[0];
  inp.value = '';
  if (!f) return null;
  return JSON.parse(await f.text());
}
export const dzis = () => new Date().toISOString().slice(0, 10);
