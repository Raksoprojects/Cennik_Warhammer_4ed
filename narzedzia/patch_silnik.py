# -*- coding: utf-8 -*-
P='/home/claude/praca/repo/src/silnik.js'
t=open(P,encoding='utf-8').read()

t=t.replace("""function wTowarze(d, c) {
  return c.cena_p > 0 && !d.rynek.asortyment.wykluczone_kategorie.includes(c.kat);
}""","""function wTowarze(d, c) {
  if (!(c.cena_p > 0)) return false;
  // v3: handluje się tylko tym, co ma typ „towar". Nocleg, usługa i nieruchomość
  // mają ceny już detaliczne — marża kupca liczyłaby narzut drugi raz.
  const typy = d.rynek.asortyment.wykluczone_typy;
  if (typy && c.typ) return !typy.includes(c.typ);
  return !d.rynek.asortyment.wykluczone_kategorie.includes(c.kat);   // dane sprzed v3
}

// v3: wieś ma limit ceny i wymóg Dostępności Powszechnej, ale żywy inwentarz
// i podstawowa żywność są z nich wyjęte — wieś jest właśnie tym miejscem, gdzie kupuje się krowę.
function omijaLimitWsi(lok, c) {
  const w = lok.limit_omijaja_podtypy;
  return !!(w && c.podtyp && c.podtyp.some(p => w.includes(p)));
}""")

t=t.replace("""  const pula = kats => pozycje(d).filter(c =>
    kats.includes(c.kat) && wTowarze(d, c) && c.cena_p <= cap &&
    !(stosujDostepnosc && lok.tylko_powszechna && c.dostepnosc && c.dostepnosc !== 'Powszechna'));""",
"""  const pula = kats => pozycje(d).filter(c => {
    if (!kats.includes(c.kat) || !wTowarze(d, c)) return false;
    if (omijaLimitWsi(lok, c)) return true;                     // krowa we wsi mimo limitu
    if (c.cena_p > cap) return false;
    if (stosujDostepnosc && lok.tylko_powszechna && c.dostepnosc && c.dostepnosc !== 'Powszechna') return false;
    return true;
  });""")

t=t.rstrip()+"""

/* ------------------------------------------------------------ czynsz (v3) */
// Czynsz ma własny mnożnik koniunktury, niezależny od cen towarów: po zarazie
// komorne leci w dół (puste izby), w oblężeniu i w kryzysie mieszkaniowym w górę.
export function mnoznikCzynszu(d, koniunkturaId) {
  const k = d.koniunktura.koniunktury.find(x => x.id === koniunkturaId);
  return k?.czynsz?.mnoznik ?? 1;
}
export function czynsz(d, { kwatera, okres = 'miesiac', osada, koniunktura = 'normalna' }) {
  const k = d.czynsze.najem.find(x => x.kwatera === kwatera || norm(x.kwatera).includes(norm(kwatera)));
  if (!k) return null;
  const baza = k[okres + '_p'];
  if (baza == null) return null;
  const mOs = osada ? osadaZ(d, osada).mnoznik : 1;
  const mKon = mnoznikCzynszu(d, koniunktura);
  return {
    kwatera: k.kwatera, okres, baza_p: baza,
    skladowe: { osada: mOs, koniunktura: mKon }, mnoznik: mOs * mKon,
    cena_p: Math.round(baza * mOs * mKon),
  };
}
"""
open(P,'w',encoding='utf-8').write(t)
assert 'wykluczone_typy' in t and 'omijaLimitWsi' in t and 'export function czynsz' in t
print("silnik.js zaktualizowany")
