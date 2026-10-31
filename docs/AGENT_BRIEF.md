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
Frankfurt 1450 i inne — `docs/archiwum/ANALIZA_ZRODEL.md`).

Stan na 2026-10-31 (v6d):

- **Aplikacja działa** (Svelte 5 + TS + Vite + PWA, GitHub Pages). Silnik `src/silnik.js`, zapisani kupcy
  `src/kupcy_trwali.js`, spójność `src/spojnosc.js`; 61 testów (`npm test`).
- Kampania MG toczy się w **2525 KI, po Burzy Chaosu** — północ zniszczona, populacje w skali kampanii (`docs/DANE.md`).
- **Hierarchia dokumentów:** `data/*.json` > `docs/KOMPENDIUM_DANE.md` (generowany z danych) > `docs/DANE.md`
  (decyzje MG, otwarte punkty) > ten plik > `docs/archiwum/` (tylko historia, liczby mogą być nieaktualne).

Użytkownik (MG) pisze po polsku. Interfejs, komunikaty, komentarze w kodzie i dokumentacja — po polsku.
Identyfikatory w kodzie: polskie bez znaków diakrytycznych (`cena_p`, `generujKupca`), tak jak w istniejącym kodzie.

---

## 2. Waluta i jednostki

| | |
|---|---|
| 1 ZK (złota korona) | 20 s = 240 p |
| 1 s (szyling) | 12 p |
| Wszystkie kwoty w danych | **w pensach** (`*_p`), liczby całkowite |
| Kotwica | robotnik niewykwalifikowany (Brąz 3) zarabia **165 p brutto tygodniowo** (dniówka 27,5 p × 6 dni pracy) |
| Kalendarz | tydzień 8 dni (kotwica liczy 6 dni roboczych — „tydzień pracy”, decyzja MG), miesiąc 33 dni, **rok 400 dni = 50 tygodni** |
| Wyświetlanie | `mon(p)` z silnika: `mon(828)` → `3 ZK 9 s`; `mon(0)` → `—` |

---

## 3. Zasady domowe (nie zmieniać bez zgody MG)

1. **Zarobek ze Statusu** jak w RAW, poza Złotem: Brąz N = 2N k10 p, Srebro N = N k10 s, **Złoto N = N k5 ZK**.
2. **Majętny**: +1k5 monet szczebla za każdy poziom Talentu (dodaje się do rzutu, czyli do netto).
3. **Rzut na zarobek = NETTO za jedną Robotę.** Brutto = 5 × netto. 80% brutto idzie na utrzymanie.
4. **Pieniądze nie znikają** między przygodami.
5. **Status ≠ zarobek.** Status zapisuje się jako para Pozycja / Dochód (`data/pozycja_dochod.json`, `data/audyt.json`).
6. **„Pod Bronią” zastępuje podręcznik główny** tam, gdzie oba podają to samo.
7. **Jakość (HR-024, v6b):** każda Zaleta ×1,6, każda Wada ×0,6 (PG: ×2 i ×½).
   **Targowanie (v6b):** −4% za każdy PS, najwyżej −24%; zamówienia −16%.
8. **Miecz jest droższy, bo to symbol stanu** (premia znaku stanu ×1,5 dla mieczy, szabli, rapierów itd.). Miecz nie ma Wad.
9. **Topór jest tańszy od miecza**, bo sam z siebie gorzej paruje (−1 PS przy parowaniu) i zużywa mniej materiału.
10. **Ceny w cenniku to ceny wytwórcy.** Kupiec dolicza marżę. Gracz nigdy nie płaci ceny z cennika wprost.
11. **Karczma:** prywatny pokój 3 s za noc. **Marienburg w kryzysie mieszkaniowym:** mieszkanie ok. 5 ZK miesięcznie.
12. **Kolczuga 20 ZK** (kotwica z nowszego wydania). **Płytówka ≥ 2× strój dworski.** **Konie bojowe drogie.**
13. **Nie podnosić cen „dla zasady”.** Każdy mnożnik ma mieć źródło: dane historyczne, test rzemieślnika albo zasadę MG.
    Rozdział 3.3 w `docs/archiwum/ANALIZA_v5.md` mówi, skąd jest każdy mnożnik klasy; nowsze decyzje — `docs/DANE.md`.

---

## 4. Trzy ceny — najważniejsze pojęcie w interfejsie

| Nazwa w UI | Pole | Znaczenie |
|---|---|---|
| **×1** | `cena_ref_p` | poziom przed mnożnikiem klasy. Służy do przeliczania presetów, limitów osad i ilości w sklepie. Pokazywać małym szarym drukiem albo w panelu MG. |
| **Podręcznik (RAW)** | `cena_raw_p` | **pierwsza z trzech cen**: z podręcznika głównego / „Pod Bronią”, bez naszych zmian. Zawsze widoczna do porównania (cennik, kupiec, zamówienie); `null` = pozycja kampanii. |
| **Cena bazowa** | `cena_p` w cenniku | cena wytwórcy w obowiązującym presecie („zalecany” v5). **Zawsze widoczna obok ceny kupca.** |
| **Jego cena** | `towar[i].cena_p` z `generujKupca` | cena bazowa × marża × preferencja × kaprys × osada × lokalne specjalności (`tagi`, 0,8–1,2) × koniunktura efektywna × rynek. Koniunktura efektywna = sytuacja × pora roku × wahania × strefa handlowa × typ osady |
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
| `koniunkturaEfektywna(d, kon, { pora, wahania, osada })` | v6c: sytuacja + pora roku + wahania + strefa + typ osady w jednej koniunkturze |
| `mnoznikLokalny(osada, pozycja)`, `szansaDostepnosci(d, {...})` | v6d: specjalności ośrodka (0,8–1,2); szansa, że rzecz jest na półce |
| `sytuacjaOsady(d, id)` | v6d: domyślna sytuacja osady (północ po wojnie); widoki podstawiają ją przy wyborze osady |
| `rzutDochodu`, `sredniDochod`, `jalmuzna` | zarobki |
| `czynsz(d, { kwatera, okres, osada, koniunktura })` | czynsz z mnożnikiem osady i koniunktury czynszu |
| `cenaMagiczna`, `cenaZJakoscia` | przedmioty magiczne (HR-026), jakość (HR-024) |
| `zastosujPreset(cennik, klasy, nazwa)` | przelicza cennik na inny preset |
| `zastosujUstawienia(d, ust)` | **nakłada ustawienia MG** (preset, mnożniki klas, ceny pozycji, osady, koniunktury, kupcy, rynek). Zwraca nowy obiekt, nie mutuje wejścia. Wymaga `d.klasy`. |
| `roznicaCen(przed, po)` | lista zmienionych cen |
| `mon`, `proc`, `norm` | formatowanie: pensy → „3 ZK 9 s”, mnożnik → „+30%”, wyszukiwanie bez polskich znaków |

`src/spojnosc.js`: `sprawdzWszystko(cennik, { reguly, testy, czynsze })` → `[{ id, nazwa, bledy[], ostrzezenie }]`.
Ten sam kod chodzi w testach node i w panelu MG („Sprawdź spójność”).

Obiekt `d` (dane) składa się z plików `data/*.json` — wzór w `src/lib/dane.ts`.

---

## 6. Dane

Pełna mapa (który skrypt co tworzy, kolejność uruchamiania): `docs/DANE.md` → „Gdzie co jest”.

| Plik | Rola |
|---|---|
| `cennik.json` | 376 pozycji (346 towarów). `cena_p` = cena bazowa (preset zalecany v5), `cena_ref_p` = ×1, `klasa`, `typ`, `podtyp`, `podstawa_hist`, `cena_raw_p` |
| `klasy_cenowe.json` | presety (`zalecany` = domyślny, `zalecany_v4`, `baza`, `drogi`), mnożniki klas, `uzasadnienia`, `znak_stanu`, mapa `klasy` id → klasa |
| `ustawienia.json` | domyślne ustawienia MG (puste) + `przyklad` |
| `kupcy.json` | 17 kupców: marża, limit, skup, rdzeń, boczne, robota, `towar_tyg`, `gotowka_tyg` (v5.2); opcjonalnie `preferencje` per kategoria |
| `osady.json` | 55 osad: 6 ogólnych + 49 ośrodków handlu z Poradnika (strefa, populacja kampanii i z Poradnika, zamożność, dochody, `tagi`, domyślna `sytuacja`) |
| `koniunktura.json` | 12 sytuacji: mnożnik ceny i popytu per kategoria, mnożnik czynszu, `skroty` kategorii |
| `rynek.json` | zapas, popyt, macierz zapas × popyt, ilości, skup, targowanie, jakość, preferencje, kaprys, cena_minimalna, Dostępność wg osady, `typ_osady`, gospoda |
| `handel.json`, `kalendarz.json`, `postacie.json` | v6c: pory roku, wahania, strefy handlowe, nielegalne, podróż; kalendarz Imperium; postacie kupców |
| `czynsze.json` | najem × okres, kupno. Musi się zgadzać z cennikiem (test) |
| `statusy.json`, `audyt.json`, `pozycja_dochod.json` | drabina Statusu, audyt 66 profesji, Pozycja / Dochód |
| `spojnosc.json`, `spojnosc_v4.json` | reguły spójności i testy arbitrażu |
| `bron_cechy.json` | Zalety i Wady broni (z `Generator_NPC`, v6) |
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

| v6b–v6d | jakość ×1,6 / ×0,6; targowanie −4%/PS; łuki, kusze, miecz 3 ZK; strefy handlowe i pory roku (Poradnik Staroświatowca); metropolie; Egzotyczne na półce rzadko; czynsze miesiąc ≈ 3,5 × tydzień | decyzje MG — szczegóły i lista w `docs/DANE.md` |
| v6d | typ osady (wyroby taniej w mieście, żywność na wsi, 0,8–1,2); dochody i specjalności ośrodków z Dziedzictwa Sigmara; populacje kampanii 2525 KI; rok 50 tygodni; domyślna sytuacja północy po wojnie | decyzje MG 2026-10-31 |

Pełne uzasadnienia starszych decyzji: `docs/archiwum/ANALIZA_v4.md`, `docs/archiwum/ANALIZA_v5.md`, `docs/archiwum/PRZEGLAD_v3.md`.

---

## 10. Otwarte sprawy (czekają na MG — nie wprowadzać samodzielnie)

Lista otwartych punktów jest **tylko** w `docs/DANE.md` (na górze: „Stan po …”, potem punkty). Nie rozstrzygaj ich sam.

PDF-y podręczników leżą w `reference/pdf/` i `../Generator_NPC/Sources` — **nigdy nie commitować** (prawa autorskie).
Nazwy Talentów, Zalet i Wad wyłącznie z polskiego wydania — nie tłumacz z angielskiego.

Trwała decyzja cenowa MG → skrypt w `narzedzia/` (obecnie `dane_v6d.py`, idempotentny), potem `npm test`
i `node narzedzia/eksport_kompendium.mjs`. Doraźna → `data/ustawienia.json` albo panel Edycja cen. Nigdy ręcznie w `cennik.json`.

---

## 11. Jak pracować

```bash
npm install
npm test                            # testy silnika, danych i kupców — muszą przejść przed każdym commitem
npm run dev                         # aplikacja na http://localhost:5173/Cennik_Warhammer_4ed/
npm run build                       # svelte-check + dist/ do GitHub Pages
node narzedzia/eksport_kompendium.mjs   # docs/KOMPENDIUM_DANE.md po każdej zmianie danych
python3 narzedzia/analiza_v5.py     # przegląd cennika → docs/analiza_v5/*.csv
```

Skrypty danych (idempotentne), kolejność: `dodaj_v6.py` → `dane_v6b.py` → `dane_v6c.py` → `dane_v6d.py`
(v6c przebudowuje osady, więc v6d zawsze po nim).

- Nie zmieniaj `data/*.json` ręcznie w sposób, który omija testy. Ceny zmienia się przez presety, ustawienia albo skrypty w `narzedzia/`.
- Nie dodawaj zależności runtime.
- Dokument, który się zdezaktualizuje → `docs/archiwum/` z banerem „ARCHIWUM” i wpisem w `docs/archiwum/README.md`.
