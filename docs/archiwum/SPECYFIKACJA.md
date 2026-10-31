> **ARCHIWUM — stan artefakt z 2026-09-16.** Liczby i zasady tutaj mogą być nieaktualne. Obowiązują: `data/*.json`, `docs/KOMPENDIUM_DANE.md` (generowany z danych), `docs/DANE.md` (decyzje MG) i `docs/AGENT_BRIEF.md`. Czytaj ten plik tylko po historię decyzji i źródła. Indeks: `docs/archiwum/README.md`.

# Skarbiec Imperium – specyfikacja programu

Dokument opisuje wszystko, co robi artefakt „Skarbiec Imperium” (claude.ai, wersja z 2026-09-16), plus zmiany
przyjęte później w kampanii. Według niego da się odtworzyć program 1:1. Liczby i teksty są w `data/*.json`,
logika obliczeń w `src/silnik.js` (sprawdzona na 1680 kupcach i 300 zamówieniach z oryginału – `test/`).
Oryginalny plik HTML: `reference/skarbiec_oryginal.html` (teksty sekcji opisowych biorę stamtąd).

**Waluta:** 1 ZK = 20 s = 240 p; 1 s = 12 p. Wszystkie kwoty w danych są w **pensach** (liczby całkowite).
Format wyświetlania: `mon(p)` → „2 ZK 1 s 6 p”, zero → „—” (zaokrąglenie do pensa, pomija zerowe człony).

> **Aktualizacja v3 (2026-10-23).** Cennik ma 361 pozycji i nowe pola `typ`/`podtyp`; nocleg, usługi
> i nieruchomości są wyłączone z handlu (`rynek.asortyment.wykluczone_typy`), czynsz ma własny mnożnik
> koniunktury (`koniunktura.json → czynsz`, funkcja `czynsz()` w silniku), a limit wsi nie dotyczy
> żywego inwentarza (`osady.wies.limit_omijaja_podtypy`). Różnice i uzasadnienia: `PRZEGLAD_v3.md`.

---

## 1. Źródła danych i co jest nadrzędne

| Plik | Zawartość | Skąd |
|---|---|---|
| `cennik.json` | 331 pozycji: cena wytwórcy, cena RAW, Obc., Dostępność, podstawa historyczna, komentarz | kompendium ekonomiczne (2026-09-23) = 302 pozycje z artefaktu + 29 dopisanych |
| `statusy.json` | drabina Statusu (18 szczebli), wzory rzutów, Majętny | artefakt + HR-018, HR-021 |
| `kupcy.json` | 15 archetypów handlarzy | artefakt (kod) |
| `osady.json` | 6 typów osady | artefakt (kod) |
| `koniunktura.json` | 7 sytuacji × 14 kategorii (mnożnik ceny, przesunięcie popytu) | artefakt (kod) |
| `rynek.json` | zapas, popyt, macierz, ilość sztuk, skup, targowanie, jakość, zamówienia | artefakt + HR-024 |
| `czynsze.json` | najem i kupno nieruchomości | artefakt |
| `nazwy.json` | 32 imiona, 24 nazwiska, 14 dziwactw | artefakt |
| `pozycja_dochod.json` | Pozycja/Dochód, dochód ryzykowny, jałmużna, instytucje, utrzymanie | artefakt + HR-024 |
| `audyt.json` | 66 profesji (264 poziomy): werdykt, Pozycja, Dochód, uzasadnienie | artefakt |
| `historia.json` | 113 pozycji historycznych (cena oryginalna, źródło, dniówki, moneta Imperium) | artefakt |
| `przedmioty_magiczne.json` | koszty artefaktów | HR-026 (AI2 s.51–53) |
| `kalkulator.json` | lista „ile Robót trzeba odłożyć” | artefakt |

**Gdzie artefakt różni się od zasad kampanii, obowiązują zasady kampanii** (HR-024 > artefakt):

1. **Jakość:** w artefakcie „Tandetna (Wada) = ¼ ceny”. Obowiązuje: **każda Wada ×½, każda Zaleta ×2**
   (1 Wada ½, 2 Wady ¼, Wyśmienita ×2, Mistrzowska ×4).
2. **Cennik:** artefakt ma 302 pozycje, kompendium 331 (29 dopisanych 2026-09-23, głównie z *Pod Bronią*).
3. **Koniunktura:** sekcja „Zasady 5” w artefakcie podaje inne liczby niż kod (nadmiar ×0,75, niedobór ×1,5,
   wojna ×2, zaraza ×3/×1,8, oblężenie ×4/×0,8). **Obowiązują liczby z kodu** (= kompendium, rozdz. 6.3) –
   są w `koniunktura.json`. Tekst w zasadzie 5 trzeba poprawić.
4. **Majętny:** artefakt liczy stałą średnią (+3 monety). Przy rzucie: **+1k5 monet szczebla za poziom** (HR-018).
5. **Magiczne przedmioty** (HR-026) – w artefakcie ich nie ma; dodać jako nowy moduł.

---

## 2. Kotwica i kurs (sekcja „Kurs”)

```
Brąz 3 netto  = 6k10 p = śr. 33 p / Robotę
Brąz 3 brutto = 5 × 33 = 165 p / tydzień     ← ROBOTNIK = 165
dniówka       = 165 / 6 = 27,5 p
„tyg. pracy” danej rzeczy = cena_p / 165
```

Tabela kursów historycznych (stała, do wyświetlenia):

| Waluta | Kontekst | Dniówki | Moneta Imperium |
|---|---|---|---|
| 1 denar polski | 18 den. = 1 gr | 0,04 | 1 p |
| 1 grosz krakowski | 1526–1535 | 0,67 | 1 s 6 p |
| 1 złoty polski | 30 gr | 20 | 2 ZK 5 s 10 p |
| 1 gulden reński | Rzesza XVI w. | ≈ 20 | ≈ 2 ZK 6 s |
| 1 pens angielski | dniówka 4 d | 0,25 | 7 p |
| 1 szyling angielski | 12 d | 3 | 6 s 10 p |
| 1 funt szterling | 20 s | 60 | 6 ZK 17 s 6 p |
| 1 heller frankfurcki | ok. 1425 | 0,045 | 1 p |

Kontrola: rok pracy robotnika = 36 ZK brutto ≈ 15,7 zł (Kraków: ok. 13,5 zł).

---

## 3. Zarobki (sekcje „Zarobki” i „Kalkulator”)

### 3.1 Wzory (HR-021, HR-018)

| Szczebel | Rzut netto za jedną Robotę | Moneta | Średnia |
|---|---|---|---|
| Brąz N | 2N k10 | p | 11·N p |
| Srebro N | N k10 | s | 5,5·N s = 66·N p |
| Złoto N | **N k5** (zasada domowa) | ZK | 3·N ZK = 720·N p |
| Majętny (za poziom) | +1k5 | moneta szczebla | +3 p / +3 s / +3 ZK |

- **Netto** = rzut = to, co zostaje po jednej Robocie (tygodniu pracy ponad normę). **Nie mnożyć przez 52.**
- **Brutto** = 5 × netto (80% idzie na utrzymanie Statusu). Brutto/rok = brutto × 52.
- „× robotnik” = brutto / 165.
- Brąz 0: brak rzutu → jałmużna (§ 8.3).

Tabela `statusy.poziomy` zawiera gotowe średnie i opisy historyczne (Brąz 0–5, Srebro 1–5, Złoto 1–7).
Kolumny w artefakcie: Status · Rzut · Netto/Robotę · 3 Roboty · Brutto/tydz. · Brutto/rok · × robotnik · Majętny +1 · Odpowiednik historyczny.

### 3.2 Kalkulator

Wejście: Status (domyślnie Srebro 3), Majętny 0–3.
`net = netto_śr + m × bonus`, `bru = brutto_śr + m × bonus` (sic: artefakt dodaje bonus Majętnego do brutto
bez mnożenia ×5 – do decyzji przy odtwarzaniu).
Kafelki: netto/Robotę, 3 Roboty, brutto/tydz., brutto/rok (bru × 52), × robotnik.
Lista „ile Robót odłożyć” (`kalkulator.json`): `cena / net` → ≤1 „jedna Robota”, <40 „N Robót”, ≥40 „ponad 40 Robót –
realnie tylko z łupu lub spadku”, net ≤ 0 → „nigdy”. Pozycja „tydzień w drodze” (34 p × 7) ma tryb tak/nie.
⚠ Kalkulator ma kolczugę za 7 ZK, a cennik 10 ZK – brać cenę z cennika.

---

## 4. Cennik (sekcja „Cennik”)

Pola pozycji (`cennik.json → pozycje[]`):

| Pole | Znaczenie |
|---|---|
| `id` | slug nazwy, unikalny |
| `kat` | jedna z 14 kategorii (lista w `koniunktura.json → kategorie`) |
| `zrodlo` | `PG`, `PB` albo `null` (pozycja kampanii) |
| `cena_raw_p` | cena z PG/PB; `null` = brak w podręcznikach |
| `cena_p` | **cena wytwórcy** – wejście do wszystkich obliczeń |
| `obc` | Obciążenie (liczba), `null` = nie dotyczy / nieznane |
| `dostepnosc` | Powszechna / Ograniczona / Rzadka / Egzotyczna / `null` |
| `podstawa_hist`, `komentarz`, `dopisane`, `pozycja_kampanii`, `uwagi_danych` | opisy |

Widok: wyszukiwarka (bez polskich znaków – `norm()`), filtr kategorii, filtr kierunku
(`w górę` cena>RAW · `w dół` · `bez zmian` · `dopisane` gdy brak RAW). Kolumny: Przedmiot (+źródło, kategoria) ·
RAW (przekreślone przy zmianie) · Po korekcie · Tyg. pracy · Kierunek · Podstawa historyczna · Komentarz.

Pozycje z `uwagi_danych` (9 szt. z PB: jedwabna bielizna, focza skóra, osełka, bandolier, cięciwa, lont, kompas,
teodolit, strusie pióro) mają nieznane Obc./Dost. – brak strony PB przed s.89.

---

## 5. Generator kupców

### 5.1 Wzór

```
cena u kupca = cena_p × marża zawodu × mnożnik osady × koniunktura[kat].cena × macierz[zapas][popyt]
```

### 5.2 Algorytm (kolejność losowań ma znaczenie dla odtwarzalności seeda)

Generator: `mulberry32(seed)`; `ri(n) = floor(rnd()·n)`; `k10 = 1 + ri(10)`; `pick(a) = a[ri(len)]`.

1. `limit = min(kupiec.limit_p, osada.limit_p ?? ∞)`.
2. **Pula** dla listy kategorii = pozycje z cennika, w kolejności z pliku, gdzie: kategoria ∈ lista, `cena_p > 0`,
   `cena_p ≤ limit`, kategoria ∉ {Czynsze i mieszkanie, Najmici i usługi}.
   *Wieś:* dodatkowo tylko Dostępność Powszechna (albo `null`) – opisane w zasadach, w oryginale niezaimplementowane;
   w silniku włączone (`stosujDostepnosc: true`).
3. **Rdzeń:** dla każdej pozycji puli rdzenia `rnd() < 0,72` → bierze.
4. **Kategorie boczne**, po kolei: `ile = min(2 + ri(4), długość puli)`; losuje `ri(len)` aż zbierze `ile`
   nieużytych (maks. 200 prób).
5. Sortowanie malejąco po `cena_p` (sortowanie stabilne).
6. Imię: `pick(imiona) + ' ' + pick(nazwiska)`; dziwactwo: `pick(dziwactwa)`.
7. Dla każdej pozycji, w kolejności po sortowaniu:
   - `zapas` z `k10`: 1–2 pełen skład (0) · 3–7 normalny (1) · 8–9 ostatnie sztuki (2) · 10 brak (3);
   - `popyt = clamp(1 + koniunktura[kat].popyt + przesunięcie, 0, 2)`, przesunięcie z `k10`: 1–2 → −1, 9–10 → +1;
   - mnożnik i cena jak w 5.1;
   - **ilość** (zawsze jedno `ri`, poza najwyższym progiem):

     | cena_p | baza |
     |---|---|
     | < 12 | 20 + ri(60) |
     | < 120 | 6 + ri(18) |
     | < 240 | 3 + ri(8) |
     | < 2400 | 1 + ri(5) |
     | < 12000 | 1 + ri(2) |
     | ≥ 12000 | 1 (bez losowania) |

     pełen skład → `ceil(baza × 2,5)`; ostatnie sztuki → `max(1, ceil(baza × 0,15))`; brak → 0;
   - **skup** = cena × `max(0,20; kupiec.skup + (popyt wysoki +0,15 | niski −0,15))`.
8. Domyślny widok po załadowaniu: Domokrążca, Miasteczko, Normalna, seed 20260916. Zmiana któregokolwiek pola
   lub przycisk „Losuj kupca” → nowy losowy seed.

Wiersz tabeli: Towar (kat.) · Sztuk · Cena wytwórcy · Mod. (`proc(mnożnik)`) · Jego cena · Odkupi za ·
„Dlaczego tyle” (zapas · popyt, rynek %, koniunktura %). Nagłówek: imię, archetyp, Status, osada, rdzeń, opis + dziwactwo,
plakietki: marża, osada, koniunktura, liczba pozycji, „nic powyżej X” (gdy jest limit).

### 5.3 Macierz zapas × popyt

| | niski | normalny | wysoki |
|---|---|---|---|
| pełen skład | 0,65 | 0,80 | 0,95 |
| normalny zapas | 0,85 | 1,00 | 1,20 |
| ostatnie sztuki | 0,75 | 1,05 | 1,50 |
| brak, na zamówienie | 1,05 | 1,25 | 1,70 |

### 5.4 Archetypy (skrót; pełne dane w `kupcy.json`)

| Handlarz | Status | Marża | Limit | Skup |
|---|---|---|---|---|
| Domokrążca | Brąz 4 | ×1,15 | 3 ZK | 45% |
| Kramarz na targu | Srebro 1 | ×1,05 | 6 ZK | 40% |
| Kowal wiejski | Brąz 5 | ×0,90 | 8 ZK | 35% |
| Rzemieślnik cechowy | Srebro 3 | ×0,95 | 25 ZK | 45% |
| Mistrz cechu | Złoto 1 | ×1,40 | 250 ZK | 40% |
| Zbrojmistrz | Srebro 4 | ×1,10 | 80 ZK | 45% |
| Płatnerz mistrzowski | Złoto 1 | ×1,45 | 500 ZK | 40% |
| Rusznikarz z Nuln | Srebro 5 | ×1,30 | 150 ZK | 45% |
| Aptekarz | Srebro 3 | ×1,15 | 60 ZK | 40% |
| Handlarz koni | Srebro 4 | ×1,25 | 700 ZK | 50% |
| Kupiec bławatny | Srebro 5 | ×1,30 | 400 ZK | 40% |
| Księgarz i drukarz | Srebro 3 | ×1,15 | 100 ZK | 35% |
| Paser | Srebro 2 | ×0,65 | 150 ZK | 30% |
| Kwatermistrz wojskowy | Srebro 4 | ×0,85 | 120 ZK | 50% |
| Medyk i balwierz | Srebro 3 | ×1,20 | 80 ZK | 35% |

Limity handlarzy nie są wypisane w kompendium (rozdz. 6.1) – są tylko w kodzie artefaktu. Warto je dopisać.

### 5.5 Osady

Wieś ×0,85 (limit 2 ZK, tylko Powszechne) · Miasteczko ×1,00 (15 ZK) · Miasto ×1,10 (60 ZK) ·
Metropolia ×1,20 · Altdorf ×1,30 (Rzadkie o stopień łatwiej – dotyczy testów Dostępności, nie generatora) ·
Marienburg ×1,45.

### 5.6 Koniunktura (grupy kategorii)

broń = Broń biała, Broń zasięgowa, Pancerze, Amunicja · prowiant = Jedzenie, picie, nocleg ·
leki = Zioła, mikstury, narkotyki + Protezy · import (cena) = Ubranie, Księgi, Zioła · import (popyt) = Ubranie, Księgi.

| Sytuacja | Ceny | Popyt |
|---|---|---|
| Normalna | ×1 | 0 |
| Nadmiar po jarmarku | ×0,80 | −1 |
| Niedobór | ×1,40 | +1 |
| Wojna | broń ×1,80 · prowiant ×1,30 · reszta ×1,05 | broń +1 |
| Zaraza | leki ×2,50 · prowiant ×1,60 · reszta ×0,85 | leki i prowiant +1, reszta −1 |
| Oblężenie | prowiant ×3,50 · broń ×1,40 · reszta ×0,70 | prowiant +1, broń 0, reszta −1 |
| Zamknięte szlaki | import ×1,60 · reszta ×1,05 | ubranie i księgi +1 |

---

## 6. Zamówienie na miarę

Wejście: nazwa (podpowiedzi = cennik bez czynszów i usług; szukanie: dokładne, potem najkrótsza nazwa
zawierająca frazę), jakość, aktualny kupiec/osada/koniunktura.

1. Nie ma w cenniku (albo czynsz/usługa) → komunikat „Nie ma takiej pozycji…”.
2. Kategoria spoza rdzenia, bocznych i roboty → **odmowa**, odsyła do handlarzy z tą kategorią w `robota`
   (a gdy brak – w `rdzen`).
3. `baza = cena_p × jakość`; `narzut` = ×1,25 gdy kategoria w `robota` („wykonuje u siebie”), inaczej ×1,45 („sprowadza”).
4. `cena = baza × marża × osada × koniunktura[kat].cena × narzut` (bez macierzy zapas/popyt).
5. Zaliczka 50%. Termin z ceny końcowej: <1 ZK → 1k5 dni · <10 ZK → 1k3 tygodni · <50 ZK → 4+1k6 tygodni · reszta 3+1k4 miesięcy.
6. `cena > 2 × limit` → „zażąda całości z góry”. Jakość ≥ ×2 → Test Rzemiosła (porażka: termin ×2; z dubletem: zwykła
   jakość za pełną cenę). Jakość < ×1 → „wyrób z Wadą, bez reklamacji”. Targowanie zamówień maks. −20%.

---

## 7. Skup i targowanie (HR-024)

- **Skup:** jak w 5.2/7, domyślnie 45% ceny sprzedaży kupca; minimum 20%.
- **Targowanie:** Przeciwstawny Test Targowania. Każdy PS gracza = −10%, maks. −30% (zamówienia −20%).
  Modyfikator testu: pełen skład +10 dla gracza; ostatnie sztuki przy wysokim popycie −20.
  **Dolna granica:** cena z cennika (× jakość). Interpretacja (⚠ do potwierdzenia): gdy kupiec już sprzedaje
  poniżej cennika (paser, kowal, pełen skład), targowanie nie obniża ceny dalej.
- W oryginale targowanie jest tylko opisem – w programie warto dać pole „PS” przy pozycji.

---

## 8. Zasady opisowe (sekcja „Zasady”, 8 mechanik)

1. **Pozycja / Dochód** – dwie liczby; przykłady w `pozycja_dochod.json`.
2. **Utrzymanie** (80% brutto) tylko za tygodnie w osadzie; w trasie realne ceny.
3. **Czynsze** – tabela w `czynsze.json`; stosować mnożnik osady i koniunktury. (⚠ w cenniku komentarz przy mieszkaniu
   mówi „Marienburg ×1,6” – poprawnie ×1,45.)
4. **Jakość zamiast przecen** – patrz § 1 pkt 1 (Wada ×½). Pełna płytówka: 2 Wady 12 ZK · 1 Wada 24 ZK · zwykła 48 ZK ·
   Wyśmienita 96 ZK · Mistrzowska 192 ZK (w cenniku 190).
5. **Mnożnik osady i koniunktury** – liczby z § 5.5–5.6 (nie z tekstu artefaktu).
6. **Dochód ryzykowny** (Łotrzy, Wodniacy – 36 poziomów z werdyktem `ryzyko` w audycie): rzut jak za Status
   o 2 szczeble wyżej, potem Test (Kradzież/Zastraszanie/Hazard/Oszustwo); porażka ½, porażka z dubletem 0 i oskarżenie.
   ⚠ „2 szczeble” w silniku = 2 stopnie na drabinie (Brąz 5 → Srebro 2) – do potwierdzenia.
7. **Jałmużna** zamiast Brązu 0: Test Charyzmy albo Plotkowania, za każde 2 PS 1k10 p; ×2 w święto lub w zarazę.
8. **Figury państwowe:** dochód ×10, bez rzutu.

---

## 9. Audyt profesji

`audyt.json`: 66 profesji (64 + 2 BN), 264 poziomy. Każdy poziom: `nazwa`, `raw` (Status z PG), `w` (werdykt:
`ok` · `zmiana` – zmień szczebel · `dochod` – rozdziel Pozycję i Dochód · `ryzyko` – dochód ryzykowny), `poz`, `doch`
(puste = bez zmian / = Pozycja), `powod`. Widok: wyszukiwarka, filtr klasy, filtr werdyktu; 173 poziomy bez zastrzeżeń.

## 10. Tabela historyczna

`historia.json`: 113 pozycji, pola `kat`, `poz`, `orig`, `zrodlo`, `dniowki`, `wfrp`. Wyszukiwarka i filtr kategorii.
Linki do źródeł – stopka oryginału.

## 11. Magiczne przedmioty (HR-026, nowy moduł)

| Rodzaj | Koszt |
|---|---|
| Broń, pancerz, tarcza | cena z cennika × 50 × liczba właściwości; u renomowanego twórcy każda Zaleta jakości ×2 |
| Strzały | cena strzał × 30 (⚠ przyjęto cenę pozycji z cennika – tuzin) |
| Zwój / różdżka / pierścień | PZ × 10 / 50 / 200 ZK; PZ 0 liczy się jak 0,4 (4 / 20 / 80 ZK); bez Zalet |
| Kostur, talizman | brak wzoru – cena wg twórcy |

Czas wytworzenia i k100 – `przedmioty_magiczne.json → tabela`.

---

## 12. Wygląd oryginału (do odtworzenia albo zmiany)

Jedna strona, przyklejona nawigacja: Co się zmieniło · Kurs · Zarobki · Kalkulator · Cennik · Generator kupców ·
Modyfikatory · Tabela historyczna · Audyt profesji · Zasady; przełącznik trybu jasny/ciemny.
Fonty: EB Garamond (nagłówki), Archivo (UI), IBM Plex Mono (liczby). Kolory metali: brąz `#8E6334`,
srebro `#6F7A86`, złoto `#9C7A18`; akcent `#2F6355`. Pełny CSS i teksty: `reference/skarbiec_oryginal.html`.
Sekcja „Co się zmieniło wobec wersji 1” to historia rozmowy – w programie można ją pominąć.
