// Eksport wszystkich liczb Skarbca do jednego pliku Markdown — do przepisania Kompendium MG (rozdziały Status, Handel, Cennik).
// Czyta te same dane co aplikacja (data/*.json, ustawienia domyślne) i liczy tym samym silnikiem.
// Uruchom: node narzedzia/eksport_kompendium.mjs   → docs/KOMPENDIUM_DANE.md
import fs from 'node:fs';
import * as S from '../src/silnik.js';
const R = new URL('../', import.meta.url);
const rd = f => JSON.parse(fs.readFileSync(new URL(f, R)));
const PLIKI = ['cennik', 'kupcy', 'osady', 'koniunktura', 'rynek', 'nazwy', 'statusy', 'przedmioty_magiczne', 'czynsze', 'postacie', 'handel', 'kalendarz'];
const d0 = Object.fromEntries(PLIKI.map(n => [n, rd(`data/${n}.json`)]));
d0.klasy = rd('data/klasy_cenowe.json');
const ust = rd('data/ustawienia.json'); delete ust.przyklad; delete ust.opis;
const d = S.zastosujUstawienia(d0, ust);
const { mon, proc } = S;
const pl = x => String(+(+x).toFixed(3)).replace('.', ',');
const ZR = { PG: 'PG', PB: 'Pod Bronią', KR: 'Krasnoludy', WE: 'Wysokie Elfy' };
const out = [];
const w = (...l) => out.push(...l);
const tab = (nag, wiersze) => { w('| ' + nag.join(' | ') + ' |', '|' + nag.map(() => '---').join('|') + '|'); for (const r of wiersze) w('| ' + r.join(' | ') + ' |'); w(''); };

w('# Skarbiec Imperium — dane do Kompendium MG', '',
  `Wygenerowano ${new Date().toISOString().slice(0, 10)} z repozytorium (narzedzia/eksport_kompendium.mjs). Cennik: ${d.cennik.wersja}.`,
  'Wszystkie ceny to ceny **bazowe (wytwórcy)**; gracz płaci u kupca więcej (marża, osada, sytuacja). 1 ZK = 20 s = 240 p.', '');

w('## 1. Status i zarobki', '', `Kotwica: robotnik niewykwalifikowany (Brąz 3) — ${mon(d.statusy.robotnik_brutto_p)} brutto tygodniowo, dniówka ${pl(d.statusy.dniowka_p)} p.`,
  'Netto = rzut za jedną Robotę (tydzień pracy ponad normę). Brutto = 5 × netto; 80% brutto to utrzymanie w osadzie.',
  `Majętny: +1k${d.statusy.majetny.k} monet szczebla za poziom Talentu (do rzutu, czyli do netto).`, '');
tab(['Status', 'Rzut', 'Netto / Robotę', 'Brutto / tydz.', 'Brutto / rok', 'Kto'],
  d.statusy.poziomy.map(s => [`${s.tier} ${s.lvl}`, s.kostka, mon(s.netto_p), mon(s.brutto_p), mon(s.brutto_rok), s.opis]));

w('## 2. Cena u kupca', '', 'Cena u kupca = cena bazowa × marża × (preferencja × kaprys) × osada × sytuacja × pora roku × wahania × strefa handlowa × zapas/popyt × cecha kupca.',
  `Cena minimalna = koszt nabycia × ${pl(d.rynek.cena_minimalna.narzut_min)} (wyprzedaż: × ${pl(d.rynek.cena_minimalna.wyprzedaz)}); koszt nabycia = cena bazowa × osada × sytuacja (wytwórca × ${pl(d.rynek.cena_minimalna.koszt_wlasny)}).`,
  `Preferencja: rdzeń ×${pl(d.rynek.preferencje.rdzen)}, boczny ×${pl(d.rynek.preferencje.boczne)}. Kaprys 1k10: ${d.rynek.kaprys.progi.map(p => `≤${p.do} ×${pl(p.mnoznik)}`).join(', ')}; razem w granicach ×${pl(d.rynek.kaprys.granice[0])}–×${pl(d.rynek.kaprys.granice[1])}.`, '');
w('### Kupcy', '');
tab(['Kupiec', 'Status', 'Marża', 'Skup', 'Limit towaru', 'Rdzeń', 'Boczne', 'Robi sam', 'Zalety / Wady', 'Trefne'],
  d.kupcy.kupcy.map(k => [k.nazwa, k.status, proc(k.marza), `${Math.round(k.skup * 100)}%`, mon(k.limit_p), k.rdzen.join(', '), k.boczne.join(', '),
    [...k.robota, ...(k.robota_pozycje ?? [])].join(', ') || '—', k.jakosc ? `${Math.round(k.jakosc.zalety * 100)}% / ${Math.round(k.jakosc.wady * 100)}%` : '—',
    `${Math.round((k.trefne ?? d.rynek.trefne.domyslna_szansa) * 100)}%`]));
w('### Osady', '');
tab(['Osada', 'Mnożnik', 'Limit towaru', 'Dostępność jak', 'Uwagi'],
  d.osady.osady.filter(o => !o.grupa).map(o => [o.nazwa, proc(o.mnoznik), o.limit_p == null ? 'bez limitu' : mon(o.limit_p), o.dostepnosc, o.uwaga ?? '']));
w('### Ośrodki handlu (Poradnik Staroświatowca, tab. 3-2)', '');
tab(['Miasto', 'Strefa', 'Populacja', 'Zamożność', 'Typ', 'Mnożnik', 'Specjalności'],
  d.osady.osady.filter(o => o.grupa).map(o => [o.nazwa, o.grupa, o.populacja, o.zamoznosc, o.typ, proc(o.mnoznik),
    o.tagi ? Object.entries(o.tagi).map(([t, m]) => `${t} ×${pl(m)}`).join(', ') : '']));
w('### Dostępność (PG s. 290 + zasady kampanii)', '');
tab(['Dostępność', ...Object.keys(d.rynek.dostepnosc.tabela)], ['Powszechna', 'Ograniczona', 'Rzadka', 'Egzotyczna'].map(x =>
  [x, ...Object.values(d.rynek.dostepnosc.tabela).map(t => `${pl(t[x] * 100)}%`)]));
w(`Altdorf i Marienburg: Rzadkie jak Ograniczone. Marienburg (import): Egzotyczne ${pl(d.rynek.dostepnosc.import_egzotyczne * 100)}%. Towar krasnoludzki / elfi u kupca innej rasy: × ${pl(d.rynek.dostepnosc.obce_pochodzenie)}.`, '');
w('### Sytuacje', '');
tab(['Sytuacja', 'Ceny', 'Popyt', 'Czynsz'], d.koniunktura.koniunktury.map(k => [k.nazwa, S.etykietaKoniunktury(d, k).replace(k.nazwa + ' ', ''), k.opis_popytu ?? '', proc(k.czynsz?.mnoznik ?? 1)]));
w('### Pora roku i wahania rynku', '');
tab(['Pora', 'Ceny', 'Kategorie', 'Zagrożenia w podróży'], d.handel.pory_roku.lista.map(p => [p.nazwa, `×${pl(p.ceny)}`,
  Object.entries(p.kategorie).map(([k, v]) => `${k} ×${pl(v.cena)}${v.popyt ? ', popyt +' + v.popyt : ''}`).join('; '), `+${p.zagrozenia}`]));
tab(['1k10', 'Rynek', 'Ceny', 'Popyt', 'Dostępność'], d.handel.wahania.lista.map(x => [`${x.od}–${x.do}`, x.nazwa, `×${pl(x.ceny)}`, x.popyt, `×${pl(x.dostepnosc)}`]));
w('### Zapas × popyt', '');
tab(['Zapas \\ popyt', ...d.rynek.popyt.nazwy], d.rynek.macierz_zapas_x_popyt.wartosci.map((r, i) => [`${d.rynek.zapas.progi[i].nazwa} (1k10 ≤ ${d.rynek.zapas.progi[i].do})`, ...r.map(m => proc(m))]));
w('### Targowanie, skup', '',
  `Przeciwstawny Test Targowania: każdy PS −${Math.round(d.rynek.targowanie.za_ps * 100)}%, najwyżej −${Math.round(d.rynek.targowanie.max * 100)}% (zamówienia −${Math.round(d.rynek.targowanie.max_zamowienie * 100)}%). Talenty (Żyłka Handlowa) dodają upust ponad limit. Nigdy poniżej ceny minimalnej kupca.`,
  `Skup: odsetek ceny kupca z tabeli kupców; wysoki popyt +${Math.round(d.rynek.skup.popyt_wysoki * 100)} pkt, niski ${Math.round(d.rynek.skup.popyt_niski * 100)} pkt, minimum ${Math.round(d.rynek.skup.minimum * 100)}%.`, '');

w('## 3. Jakość przedmiotu', '', `Cena w cenniku = wariant podstawowy. Każda Zaleta przedmiotu ×${pl(d.rynek.jakosc.za_zalete)}, każda Wada ×${pl(d.rynek.jakosc.za_wade)} (Wyśmienity i Wytrzymały — każdy poziom osobno).`, '');
tab(['Cecha', 'Rodzaj', 'Efekt'], [...d.rynek.jakosc.zalety.map(z => [z.nazwa, 'Zaleta' + (z.wielokrotna ? ' (wielokrotna)' : ''), z.opis]),
  ...d.rynek.jakosc.wady.map(z => [z.nazwa, 'Wada', z.opis])]);
const plyt = d.cennik.pozycje.find(c => c.id === 'pelna-plytowka-4-elementy');
tab(['Wykonanie', 'Mnożnik', 'Pełna płytówka'], d.rynek.jakosc.opcje.map(o => [o.nazwa, `×${pl(o.mnoznik)}`, mon(Math.round(plyt.cena_p * o.mnoznik))]));

w('## 4. Zamówienia', '', `Narzut za własną robotę ×${pl(d.rynek.zamowienie.narzut_robota)}, za sprowadzenie ×${pl(d.rynek.zamowienie.narzut_sprowadzenie)}. Zaliczka ${Math.round(d.rynek.zamowienie.zaliczka * 100)}%. Materiał zamawiającego: płaci ${Math.round(d.rynek.zamowienie.material_wlasny * 100)}% ceny.`,
  `Termin: ${d.rynek.zamowienie.termin.map(t => (t.ponizej_p ? `< ${mon(t.ponizej_p)}` : 'więcej') + ': ' + t.opis).join('; ')}. Tydzień = 8 dni.`,
  `Rzadkość tutaj (szansa w sklepie < ${Math.round(d.rynek.dostepnosc.zamowienie.prog * 100)}%): ${Object.entries(d.rynek.dostepnosc.zamowienie.termin_tyg).map(([k, v]) => `${k} +${v} tyg., ×${pl(d.rynek.dostepnosc.zamowienie.narzut[k])}`).join('; ')}. ${d.rynek.dostepnosc.zamowienie.wioska_opis}`, '');

w('## 5. Towar trefny', '', d.rynek.trefne.opis, '');
tab(['Rodzaj', 'Prawdziwa wartość', 'Wykrycie', 'Opis'], Object.values(d.rynek.trefne.rodzaje).map(r => [r.nazwa, r.wartosc === 'skala' ? 'wg skali oszustwa' : `${Math.round(r.wartosc * 100)}%`, r.test_opis, r.opis]));
tab(['Oszukane', 'Test Wyceny'], d.rynek.trefne.skala_oszustwa.map(s => [`${Math.round(s.udzial * 100)}% towaru`, s.test]));

w('## 6. Czynsze', '');
tab(['Kwatera', 'Tydzień', 'Miesiąc', 'Rok'], d.czynsze.najem.map(k => [k.kwatera, mon(k.tydzien_p), mon(k.miesiac_p), mon(k.rok_p)]));
tab(['Kupno', 'Cena'], d.czynsze.kupno.map(k => [k.nazwa, mon(k.cena_p)]));
w(`Nocleg i posiłek wg gospody (× osada): ${d.rynek.gospoda.standardy.map(s => `${s.nazwa} ×${pl(s.mnoznik)}`).join(', ')}.`, '');

w('## 7. Klasy cenowe (preset domyślny)', '');
const pr = d.klasy.presety[d.klasy.domyslny];
tab(['Klasa', 'Mnożnik', 'Skąd'], Object.entries(pr.mnozniki).map(([k, m]) => [k, `×${pl(m)}`, d.klasy.uzasadnienia[k]?.tekst ?? '']));
w(`Znak stanu (miecze, szable, rapiery…): ×${pl(pr.premia_znak_stanu)}.`, '');

w('## 8. Cennik kampanii', '', 'Kolumny: cena bazowa (wytwórcy) · podręcznik (RAW) · Obciążenie · Dostępność · źródło i strona. ⚠ = nielegalny.', '');
for (const kat of [...new Set(d.cennik.pozycje.map(c => c.kat))]) {
  w(`### ${kat}`, '');
  tab(['Przedmiot', 'Cena', 'Podręcznik', 'Obc.', 'Dostępność', 'Źródło'], d.cennik.pozycje.filter(c => c.kat === kat).map(c => [
    (c.nielegalny ? '⚠ ' : '') + c.nazwa + (c.typ !== 'towar' ? ' (nie w handlu)' : ''), mon(c.cena_p), c.cena_raw_p == null ? '—' : mon(c.cena_raw_p),
    c.obc ?? '—', c.dostepnosc ?? '—', c.zrodlo ? `${ZR[c.zrodlo] ?? c.zrodlo}${c.strona ? ' ' + c.strona : ''}` : 'kampania']));
}

fs.mkdirSync(new URL('docs/', R), { recursive: true });
fs.writeFileSync(new URL('docs/KOMPENDIUM_DANE.md', R), out.join('\n'));
console.log('zapisano docs/KOMPENDIUM_DANE.md,', out.length, 'wierszy');
