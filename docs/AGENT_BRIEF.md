# AGENT_BRIEF — wszystko, co agent musi wiedzieć, zanim dotknie kodu

Ten plik jest dla agenta AI w VS Code (Copilot, Claude Code, Cline, Cursor i podobnych).
**Agent nie ma dostępu do rozmów, w których powstał ten projekt, ani do pamięci Claude.** Wszystko, co jest
potrzebne, jest w repozytorium. Jeśli czegoś tu nie ma, a decyzja zmienia ceny albo zasady — zapytaj MG,
nie zgaduj.

---

## 1. Co to jest

**Skarbiec Imperium** to pomoc dla Mistrza Gry w kampanii *Warhammer Fantasy Roleplay 4 ed.* (polskie wydanie).
Liczy ceny, zarobki, czynsze i generuje kupców. Świat gry to Imperium wzorowane na Świętym Cesarstwie Rzymskim,
Polsce i Francji XV–XVI w. Ceny są przebudowane na podstawie źródeł historycznych (Kraków 1526–35, Anglia,
Frankfurt 1450 i inne — `docs/ANALIZA_ZRODEL.md`).

Stan na 2026-10-24:

- **Silnik i dane są gotowe i przetestowane** (`src/silnik.js`, `src/spojnosc.js`, `data/*.json`, 34 testy).
- **Działający wzór interfejsu** to `reference/skarbiec_v5.html` — jednoplikowa strona z tym samym silnikiem.
  Otwórz ją w przeglądarce, zanim zaczniesz budować widoki. Aplikacja ma robić to samo, tylko lepiej zorganizowane.
- **Do zbudowania** jest aplikacja Vite + czysty JS (`TASKS.md`, `docs/APLIKACJA.md`).

Użytkownik (MG) pisze po polsku. Interfejs, komunikaty, komentarze w kodzie i dokumentacja — po polsku.
Identyfikatory w kodzie: polskie bez znaków diakrytycznych (`cena_p`, `generujKupca`), tak jak w istniejącym kodzie.

---

## 2. Waluta i jednostki

| | |
|---|---|
| 1 ZK (złota korona) | 20 s = 240 p |
| 1 s (szyling) | 12 p |
| Wszystkie kwoty w danych | **w pensach** (`*_p`), liczby całkowite |
| Kotwica | robotnik niewykwalifikowany (Brąz 3) zarabia **165 p brutto tygodniowo** (dniówka 27,5 p) |
| Wyświetlanie | `mon(p)` z silnika: `mon(828)` → `3 ZK 9 s`; `mon(0)` → `—` |

---

## 3. Zasady domowe (nie zmieniać bez zgody MG)

1. **Zarobek ze Statusu** jak w RAW, poza Złotem: Brąz N = 2N k10 p, Srebro N = N k10 s, **Złoto N = N k5 ZK**.
2. **Majętny**: +1k5 monet szczebla za każdy poziom Talentu (dodaje się do rzutu, czyli do netto).
3. **Rzut na zarobek = NETTO za jedną Robotę.** Brutto = 5 × netto. 80% brutto idzie na utrzymanie.
4. **Pieniądze nie znikają** między przygodami.
5. **Status ≠ zarobek.** Status zapisuje się jako para Pozycja / Dochód (`data/pozycja_dochod.json`, `data/audyt.json`).
6. **„Pod Bronią” zastępuje podręcznik główny** tam, gdzie oba podają to samo.
7. **Jakość (HR-024):** każda Wada ×½, każda Zaleta ×2.
8. **Miecz jest droższy, bo to symbol stanu** (premia znaku stanu ×1,5 dla mieczy, szabli, rapierów itd.). Miecz nie ma Wad.
9. **Topór jest tańszy od miecza**, bo sam z siebie gorzej paruje (−1 PS przy parowaniu) i zużywa mniej materiału.
10. **Ceny w cenniku to ceny wytwórcy.** Kupiec dolicza marżę. Gracz nigdy nie płaci ceny z cennika wprost.
11. **Karczma:** prywatny pokój 3 s za noc. **Marienburg w kryzysie mieszkaniowym:** mieszkanie ok. 5 ZK miesięcznie.
12. **Kolczuga 20 ZK** (kotwica z nowszego wydania). **Płytówka ≥ 2× strój dworski.** **Konie bojowe drogie.**
13. **Nie podnosić cen „dla zasady”.** Każdy mnożnik ma mieć źródło: dane historyczne, test rzemieślnika albo zasadę MG.
    Rozdział 3.3 w `docs/ANALIZA_v5.md` mówi, skąd jest każdy obecny mnożnik.

---

## 4. Trzy ceny — najważniejsze pojęcie w interfejsie

| Nazwa w UI | Pole | Znaczenie |
|---|---|---|
| **×1** | `cena_ref_p` | poziom przed mnożnikiem klasy. Służy do przeliczania presetów, limitów osad i ilości w sklepie. Pokazywać małym szarym drukiem albo w panelu MG. |
| **Podręcznik (RAW)** | `cena_raw_p` | **pierwsza z trzech cen**: z podręcznika głównego / „Pod Bronią”, bez naszych zmian. Zawsze widoczna do porównania (cennik, kupiec, zamówienie); `null` = pozycja kampanii. |
| **Cena bazowa** | `cena_p` w cenniku | cena wytwórcy w obowiązującym presecie („zalecany” v5). **Zawsze widoczna obok ceny kupca.** |
| **Jego cena** | `towar[i].cena_p` z `generujKupca` | cena bazowa × marża × preferencja × kaprys × osada × koniunktura × rynek |
| **Minimalna** | `towar[i].cena_min_p` | poniżej tej ceny kupiec nie zejdzie w targowaniu (koszt nabycia + 5%, przy wyprzedaży koszt − 10%) |

Wymagania MG dotyczące wyświetlania (dosłownie z jego prośby, v5):

- Skarbiec **zawsze** pokazuje cenę bazową bez mnożnika, a obok cenę z mnożnikiem zależnym od kupca, miasta i sytuacji.
- Kupiec może chcieć za coś więcej, a za coś innego mniej — w rozsądnych granicach (preferencja + kaprys, granice −15% … +20%).
- **Miasto i sytuacja pokazują w nawiasie modyfikator ceny**, który wywołują: `etykietaOsady(osada)` → „Altdorf (+30%)”,
  `etykietaKoniunktury(d, kon, { krotko: true })` → „Wojna (broń, strzelecka, amunicja, pancerze +80% · jedzenie +30% · reszta +5% · czynsz +30%)”.
- Cena minimalna rozstrzyga test targowania.

---

## 5. Silnik — API

`src/silnik.js` (moduł ES, bez DOM, bez zależności). Najważniejsze funkcje:

| Funkcja | Co robi |
|---|---|
| `generujKupca(d, { kupiec, osada, koniunktura, seed, osobowosc = true })` | sklep: imię, dziwactwo, `towar[]` z rozbiciem `skladowe`, `koszt_p`, `cena_min_p`, `wyprzedaz`, `etykiety` |
| `wycenZamowienie(d, { kupiec, osada, koniunktura, przedmiot, jakosc, seed })` | zamówienie na miarę: `wykonuje` / `sprowadza` / `odmowa` / `brak_w_cenniku` |
| `targuj(d, { cena_p, cena_cennik_p, cena_min_p, ps, zamowienie })` | cena po targu; granica = `cena_min_p` (gdy podana) |
| `modyfikatorTargowania({ zapas, popyt })` | modyfikator testu: pełen skład +10, ostatnie sztuki przy wysokim popycie −20 |
| `cenaMinimalna(d, { kupiec, pozycja, osada, koniunktura, mRynek, cena_p })` | koszt nabycia i cena minimalna |
| `majatekKupca(d, kup, seed)` | v5.2: towar na stanie i gotówka kupca w tygodniach brutto jego Statusu (`kupcy.json` → `towar_tyg`, `gotowka_tyg`) |
| `osobowoscKupca(d, kup, pozycja, rzut)` | preferencja (rdzeń/boczne) × kaprys (1k10), w granicach |
| `etykietaOsady`, `etykietaKoniunktury`, `modyfikatorKoniunktury` | teksty z modyfikatorem w nawiasie |
| `rzutDochodu`, `sredniDochod`, `jalmuzna` | zarobki |
| `czynsz(d, { kwatera, okres, osada, koniunktura })` | czynsz z mnożnikiem osady i koniunktury czynszu |
| `cenaMagiczna`, `cenaZJakoscia` | przedmioty magiczne (HR-026), jakość (HR-024) |
| `zastosujPreset(cennik, klasy, nazwa)` | przelicza cennik na inny preset |
| `zastosujUstawienia(d, ust)` | **nakłada ustawienia MG** (preset, mnożniki klas, ceny pozycji, osady, koniunktury, kupcy, rynek). Zwraca nowy obiekt, nie mutuje wejścia. Wymaga `d.klasy`. |
| `roznicaCen(przed, po)` | lista zmienionych cen |
| `mon`, `proc`, `norm` | formatowanie: pensy → „3 ZK 9 s”, mnożnik → „+30%”, wyszukiwanie bez polskich znaków |

`src/spojnosc.js`: `sprawdzWszystko(cennik, { reguly, testy, czynsze })` → `[{ id, nazwa, bledy[], ostrzezenie }]`.
Ten sam kod chodzi w testach node i w panelu MG („Sprawdź spójność”).

Obiekt `d` (dane) składa się z plików `data/*.json` — wzór w `src/app/dane.js`.

---

## 6. Dane

| Plik | Rola |
|---|---|
| `cennik.json` | 365 pozycji. `cena_p` = cena bazowa (preset zalecany v5), `cena_ref_p` = ×1, `klasa`, `typ`, `podtyp`, `podstawa_hist`, `cena_raw_p` |
| `klasy_cenowe.json` | presety (`zalecany` = domyślny, `zalecany_v4`, `baza`, `drogi`), mnożniki klas, `uzasadnienia`, `znak_stanu`, mapa `klasy` id → klasa |
| `ustawienia.json` | domyślne ustawienia MG (puste) + `przyklad` |
| `kupcy.json` | 15 kupców: marża, limit, skup, rdzeń, boczne, robota, `towar_tyg`, `gotowka_tyg` (v5.2); opcjonalnie `preferencje` per kategoria |
| `osady.json` | 6 osad: mnożnik, limit, wyjątki wsi |
| `koniunktura.json` | 8 sytuacji: mnożnik ceny i popytu per kategoria, mnożnik czynszu, `skroty` kategorii |
| `rynek.json` | zapas, popyt, macierz zapas × popyt, ilości, skup, targowanie, jakość, **preferencje, kaprys, cena_minimalna** (v5) |
| `czynsze.json` | najem × okres, kupno. Musi się zgadzać z cennikiem (test) |
| `statusy.json`, `audyt.json`, `pozycja_dochod.json` | drabina Statusu, audyt 66 profesji, Pozycja / Dochód |
| `spojnosc.json`, `spojnosc_v4.json` | reguły spójności i testy arbitrażu |
| `bron_cechy.json` | **szablon** Zalet i Wad broni — do uzupełnienia z podręcznika (zadanie T11) |
| `historia.json`, `nazwy.json`, `przedmioty_magiczne.json`, `kalkulator.json` | tabela źródeł, imiona kupców, wzory magii, lista zakupów kalkulatora |

`propozycja/` to archiwum v2–v4 (do porównań i testów regresji). `reference/` to wzory: oryginalny artefakt, dane oryginału, `skarbiec_v5.html`.

---

## 7. Niezmienniki — tego nie wolno zepsuć

1. **Kolejność losowań w `generujKupca`**: rdzeń → boczne → imię → dziwactwo → wiersze (zapas, popyt, ilość).
   Kaprys ma **osobny** strumień (`seed ^ 0x5bd1e995`). Ten sam seed musi dawać ten sam sklep. Test `zgodnosc` to pilnuje.
2. **Sortowanie towaru**: stabilne, malejąco po `cena_p`.
3. **Nocleg, usługi, nieruchomości nie są towarem** (`typ ≠ 'towar'`): nie ma ich w asortymencie, skupie ani zamówieniach.
4. **Czynsze w `czynsze.json` = wiersze najmu w cenniku.** `zastosujUstawienia` przelicza je razem.
5. **Cennik przechodzi wszystkie testy spójności** (`npm test`). Każda zmiana cen → uruchom testy i `python3 narzedzia/analiza_v5.py`.
6. **`Infinity` nie istnieje w JSON.** Brak limitu osady to `null`.
7. **Id z nazwy**: `ł` → `l` **przed** normalizacją NFD (inaczej „kapłon” → „kapon”).
8. **`mon()` tylko do wyświetlania.** Sumy i porównania na liczbach.

---

## 8. Ustawienia MG (format `data/ustawienia.json`)

```json
{
  "wersja": 1,
  "preset": "zalecany",
  "mnozniki": { "pojazd": 2 },
  "premia_znak_stanu": null,
  "pozycje": { "lekki-kon-bojowy": { "cena_p": 36000 }, "miecz": { "mnoznik": 1.1 } },
  "osady": { "altdorf": { "mnoznik": 1.4 } },
  "koniunktury": { "wojna": { "kategorie": { "Pancerze": { "cena": 2 } }, "czynsz": 1.5 } },
  "kupcy": { "zbrojmistrz": { "marza": 1.2, "preferencje": { "Pancerze": 1.15 } } },
  "rynek": { "kaprys": { "granice": [0.9, 1.1] }, "cena_minimalna": { "narzut_min": 1.1 } }
}
```

W aplikacji: ustawienia z pliku są domyślne; panel MG trzyma własną kopię w `localStorage`
(klucz `skarbiec-ustawienia-v5`, zawsze w `try/catch`), eksportuje ją do pliku w tym samym formacie
i importuje z pliku. „Przywróć domyślne” czyści kopię z przeglądarki.

---

## 9. Decyzje, które już zapadły (i dlaczego) — nie otwierać ich na nowo

| Wersja | Decyzja | Dlaczego |
|---|---|---|
| v1→v2 | kotwica 27,5 p za dniówkę (nie 1 s) | przy 1 s płyta i konie wychodziły za tanio |
| v3 | płace angielskie wg stulecia (tabela Dyera) | 4 d za dniówkę było prawdą tylko dla 1441–1520 |
| v3 | `typ` pozycji, usługi poza handlem | kupiec sprzedawał nocleg z marżą |
| v3 | czynsz ma własny mnożnik koniunktury | po zarazie czynsze spadają, w oblężeniu rosną |
| v3 | macierz zapas × popyt | ostatnie sztuki przy niskim popycie = wyprzedaż, przy wysokim = drożej |
| v4 | klasy cenowe i presety; 10 rodzin testów arbitrażu | MG chciał drożej (×3), ale tak, żeby np. płachta nie pozwalała kupić kilku koców |
| v4 | najem ×2 | karczma 3 s za noc i Marienburg 5 ZK |
| v5 | **zalecany = domyślny cennik** | decyzja MG |
| v5 | codzienne 1,2; palna 1; alchemia 1; prestiż 1,5; konie robocze 1; pancerz skórzany 1,5 | te mnożniki nie miały podstawy w danych („nie chcę drożej tylko po to, żeby było drożej”) |
| v5 | cena minimalna, preferencje, kaprys, etykiety z modyfikatorem | prośba MG |
| v5.2 | broń palna ×2; alchemia: składniki ×1, wyroby ×2; majątek kupca (towar, gotówka); noclegi (ława/podłoga, stajnia); korekty Dochodu 17 poziomów | decyzje MG: „broń palna droga”, „alchemia droga, ale osiągalna”, „kramarz nie ma 47 namiotów”, „służka zarabiała za dużo” |
| v5.1 | pojazdy ×1,5; łuk elfi = 5× łuk długi; konie bojowe ×1,5 zostają; RAW widoczny wszędzie | decyzje MG: „królestwo za konia”, „chłop musi mieć wóz” |

Pełne uzasadnienia: `docs/ANALIZA_v4.md`, `docs/ANALIZA_v5.md`, `docs/PRZEGLAD_v3.md`.

---

## 10. Otwarte sprawy (czekają na MG — nie wprowadzać samodzielnie)

Rozstrzygnięte 2026-10-24 (v5.1, już w danych): konie bojowe drogie (×1,5), pojazdy ×1,5 (chłopa ma być stać na
furmankę), łuk elfi = 5× łuk długi, cena z podręcznika (RAW) widoczna wszędzie obok ceny bazowej.

Otwarte:

1. **Zalety i Wady broni** — `data/bron_cechy.json` do uzupełnienia z podręcznika (s. 294–295) i „Pod Bronią” (s. 91–93).
   PDF-y nie są w repozytorium. Jeśli MG położy je w `reference/pdf/` (folder jest w `.gitignore` — prawa autorskie,
   **nigdy nie commitować**), możesz z nich czytać. **Nazwy Zalet i Wad wyłącznie z polskiego wydania** — nie tłumacz z angielskiego.
2. **Wyposażenie profesji** — jak wyżej, z rozdziału profesji podręcznika.

Nowe decyzje cenowe MG idzie do `data/ustawienia.json` (albo, jeśli ma być trwała, do
`narzedzia/buduj_v5.py` i przebudowy danych), a nie ręcznie do `cennik.json`.

---

## 11. Jak pracować

```bash
npm install
npm test                            # 34 testy silnika i danych — muszą przejść przed każdym commitem
npm run dev                         # aplikacja na http://localhost:5173
npm run build                       # dist/ do GitHub Pages
python3 narzedzia/analiza_v5.py     # przegląd cennika → docs/analiza_v5/*.csv
python3 narzedzia/zbuduj_artefakt.py   # jednoplikowa strona → reference/skarbiec_v5.html
```

- Nie zmieniaj `data/*.json` ręcznie w sposób, który omija testy. Ceny zmienia się przez presety, ustawienia albo skrypty w `narzedzia/`.
- Nie dodawaj zależności runtime. Vite jest jedyną zależnością deweloperską.
- Commit po każdym zadaniu z `TASKS.md`, w opisie numer zadania.
