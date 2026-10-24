# Analiza v5 — cennik Starego Świata pozycja po pozycji i zarobki profesji

Data: 2026-10-24. Dotyczy: `data/cennik.json` w wersji `v5-zalecany`.
Liczby w tym dokumencie pochodzą z `narzedzia/analiza_v5.py`. Pełne tabele są w `docs/analiza_v5/*.csv`
(średnik jako separator, otwierają się w Excelu i LibreOffice).

---

## 1. Wynik w skrócie

1. **Zalecany zostaje, ale bez „drożej dla drożej”.** Sprawdziłem, skąd pochodzi każdy mnożnik klasy.
   Pięć z nich nie miało żadnej podstawy w danych: codzienne ×1,5, broń palna ×1,5, alchemia ×1,5,
   prestiż ×3 i konie robocze ×1,5. W v5 te pięć klas spada do poziomu, który wynika ze źródeł.
   Dodatkowo pancerz skórzany przestał być liczony jak płyta.
2. **Nic nie podrożało.** 168 pozycji jest tańszych, 196 bez zmian, 0 droższych.
3. **Zarobki pasują do cen.** Codzienne życie Brązu 3 mieści się w 80% jego brutto. Narzędzia zawodu kosztują
   od 1 do 8 tygodni brutto profesji, która ich używa. Kapitał (koń, łódź, warsztat, rumak) kosztuje od pół roku
   do dwóch i pół roku. Tam, gdzie mamy źródło, te proporcje zgadzają się z historią (rozdz. 5).
4. **Decyzje MG z v5.1** (rozdz. 7): konie bojowe zostają drogie, pojazdy ×1,5, łuk elfi = 5× łuk długi,
   cena z podręcznika widoczna wszędzie do porównania.
5. **Testy:** 33 z 33 przechodzą, w tym 59 reguł spójności, 10 rodzin arbitrażu i 2 nowe reguły rodzin.
   Test rzemieślnika nie zgłasza żadnego ostrzeżenia.

---

## 2. Jak czytać „cenę bazową”

W Skarbcu są trzy poziomy ceny. Każdy ma swoje miejsce:

| Poziom | Pole | Co to jest | Gdzie widać |
|---|---|---|---|
| ×1 | `cena_ref_p` | poziom przed mnożnikiem klasy; z niego liczy się presety, limity osad i ilości w sklepie | panel MG, kolumna „×1” w cenniku |
| **cena bazowa** | `cena_p` | cena wytwórcy w obowiązującym presecie (zalecany v5) — **to jest cena z cennika** | cennik, kolumna „Cena bazowa”; u kupca obok jego ceny |
| cena kupca | wynik `generujKupca` | cena bazowa × marża × preferencja × kaprys × osada × koniunktura × rynek | widok kupca |

Gracz nigdy nie płaci ceny bazowej. Płaci cenę kupca albo cenę zamówienia. Cena bazowa to punkt odniesienia:
„w cenniku 20 ZK, ten tu chce 31”.

---

## 3. Przegląd wszystkich pozycji

### 3.1 Źródła

| | Liczba |
|---|---|
| Pozycji w cenniku | 364 |
| Z opisem źródła (`podstawa_hist`) | 187 |
| — w tym „j.w.” (źródło pozycji powyżej, przeniesione proporcjonalnie) | 32 |
| Bez źródła | 177 |
| Ze źródłem, które da się przeliczyć na liczbę i porównać | 66 |
| — w tym cena v5 w przedziale źródła (−20% … +25%) | 46 |

177 pozycji bez źródła to w większości drobiazgi z podręcznika (gwoździe, miotła, grzebień) i rzeczy fantastyczne
(łuk elfi, proch nasączony aqshy, sercobój). Dla nich ceną jest RAW przeliczony do naszej kotwicy albo szacunek
z rodziny podobnych rzeczy. Plik `cennik_przeglad.csv` ma dla każdej pozycji flagi:

- `bez źródła` — brak `podstawa_hist`;
- `źródło j.w.` — źródło pozycji powyżej, przeniesione proporcjonalnie (np. kaftan kolczy z kolczugi);
- `baza≠RAW bez źródła` — poziom ×1 różni się od podręcznika, a nie ma źródła, które by to tłumaczyło (127 pozycji;
  prawie wszystkie to przeliczenie kotwicy, a nie decyzja co do konkretnej rzeczy);
- `skrajne wobec RAW ×…` — cena v5 jest ponad 4× wyższa albo poniżej ⅓ RAW;
- `ponad źródło ×…` / `poniżej źródła ×…` — cena v5 wychodzi poza przedział źródła.

### 3.2 Pozycje poza przedziałem źródła — i dlaczego

**Ponad źródłem**, z przyczyną:

| Pozycja | Cena v5 | × źródła | Dlaczego |
|---|---|---|---|
| Miecz, półtorak | 3 ZK 9 s, 12 ZK | 1,7 | Twoja zasada: miecz to znak stanu (premia ×1,5). Bez premii byłby 1,1× źródła. |
| Pełna płytówka | 96 ZK | 1,7 | Klasa pancerz ×2: test płatnerza i Twoja kotwica (kolczuga 20 ZK). Wciąż 27% rocznego brutto rycerza — źródła mówią 20–40%. |
| Hełm zamknięty | 16 ZK | 2,8 | Źródło to bascinet z 1369 r. Nasz hełm jest jedną czwartą płytówki (96 = 28 + 24 + 28 + 16). Spójne z płytówką, nie ze źródłem. |
| Rumak | 825 ZK | 1,5 | Twoje „konie bojowe drogie”. 2,3 roku brutto rycerza; źródła: 1–4 lata. |
| Najem i kupno domów | ×1,4–2,0 | | Klasy najem i kupno ×2. Wynikają z Twojej karczmy (3 s za noc) i Marienburga (5 ZK). Frankfurt 1450 daje połowę. |
| Buty, kapelusz | 18 s, 10 s 6 p | 1,6–1,8 | Odzież ×1,5 z testu szewca. Kraków i Anglia dają mniej, bo mistrz szewski ma u nas Srebro 1. |
| Prześcieradło, siennik, ręcznik | | 2,5–5,2 | Źródłem są **angielskie inwentarze z 1457 r.**, czyli wyceny rzeczy używanych. Nowe prześcieradło to 6 łokci płótna po 1 gr — sam materiał kosztuje 9 s. Zostawiam. |
| Siekiera | 4 s | 1,4 | W granicy błędu (Anglia 1457, też inwentarz). |

**Poniżej źródła:**

| Pozycja | Cena v5 | × źródła | Co z tym |
|---|---|---|---|
| Wóz | 18 ZK | 0,53 | Źródło: 15 guldenów = 34 ZK. v5.1: pojazd ×1,5 — chłopa ma być stać (rozdz. 7). |
| Furmanka | 6 ZK | 0,86 | Źródło: 3–5 guldenów = 7–11 ZK. Jak wyżej. |
| Barka rzeczna | 225 ZK | 0,98 | Źródło: 100–300 florenów = 230–690 ZK. Jak wyżej. |
| Nóż | 1 s | 0,57 | Źródło: 3 d ang. = 1 s 9 p. Mała różnica w małej kwocie; nóż jest w klasie codzienne. |
| Wspólna izba | 10 p | 0,71 | Źródło: łóżko w gospodzie 1331 r. = 1 s 2 p. Nasza cena trzyma budżet Brązu 3. |
| Strzały (12) | 10 s | 0,62 | Źródło: snop 24 strzał = 16 s, czyli 8 s za 12. Po przeliczeniu jednostki: 1,25×. W porządku. |

### 3.3 Klasy cenowe: skąd jest każdy mnożnik

Kolumny: mediana „cena ÷ źródło” liczona dla pozycji ze źródłem liczbowym; mnożnik, przy którym test rzemieślnika
daje 1,4× kosztu warsztatu (zdrowy zysk mistrza); mnożnik v4 i v5.

| Klasa | Poz. | Baza ÷ źródło | Test rzemieślnika | v4 | **v5** | Skąd mnożnik v5 |
|---|---|---|---|---|---|---|
| utrzymanie | 49 | 1,02 | — | 1 | **1** | dane |
| surowiec | 4 | 1,01 | — | 1 | **1** | dane |
| rzeźne | 6 | 1,00 | — | 1 | **1** | dane |
| kruszec | 6 | 0,71 | — | 1 | **1** | dane (wyżej opłaca się przetapiać monety) |
| najem dolny | 3 | — | — | 1 | **1** | budżet Brązu 3 |
| najem | 6 | 0,87 | — | 2 | **2** | zasada domowa (karczma 3 s, Marienburg 5 ZK) |
| kupno | 4 | 1,00 | — | 2 | **2** | idzie z najmem |
| robocze (bydło) | 6 | 1,04 | — | 1 | **1** | dane |
| konie | 4 | 0,97 | — | 1,5 | **1** | dane: Kraków trafia w środek |
| konie bojowe | 2 | 1,00 | — | 1,5 | **1,5** | zasada domowa: „konie bojowe drogie” |
| pojazd | 7 | 0,35 | 0,9 | 1 | **1,5** | decyzja MG (v5.1): drogo, ale chłopa stać na furmankę |
| codzienne | 103 | 1,15 ¹ | 1,15 | 1,5 | **1,2** | dane |
| odzież | 15 | 1,04 | 1,57 | 1,5 | **1,5** | test szewca i krawca |
| prestiż | 8 | — | — | 3 | **1,5** | zasada domowa: strój dworski ≠ płytówka |
| broń | 67 | 0,57 | 2,56 | 2 | **2** | dane: baza była za niska |
| broń palna | 29 | 1,05 | — | 1,5 | **1** | dane: baza = źródło = RAW |
| pancerz | 15 | 0,84 | 1,99 | 2 | **2** | test płatnerza + kolczuga 20 ZK |
| pancerz skórzany | 5 | 1,07 | — | (2) | **1,5** | nowa klasa: robi rymarz, nie płatnerz |
| księga | 9 | 0,34 | 1,42 | 2 | **2** | środek między źródłem a testem skryby |
| alchemia | 16 | — | — | 1,5 | **1** | brak danych |

¹ Bez trzech angielskich inwentarzy rzeczy używanych (prześcieradło, siennik, ręcznik). Z nimi mediana wynosi 1,24.

**Jak to rozumieć.** „Dane” znaczy: źródło albo test rzemieślnika mówi, że tyle. „Zasada domowa” znaczy: Ty
ustaliłeś punkt odniesienia (karczma 3 s, kolczuga 20 ZK, konie bojowe drogie, strój dworski tańszy od płytówki),
a mnożnik jest najmniejszy, który go spełnia. „Brak danych” znaczy, że nie ma czego się trzymać — wtedy v5 nie
dokłada mnożnika, a Ty możesz go dołożyć suwakiem w panelu MG.

### 3.4 Pięć zmian v4 → v5, każda z uzasadnieniem

| Klasa | v4 → v5 | Dlaczego | Przykłady (v4 → v5) |
|---|---|---|---|
| codzienne | 1,5 → 1,2 | Źródła 1,15×, test wiejskiego kowala 1,15×. Przy 1,5 kowal brał 2× swój koszt za sierp. | sierp 4 s 6 p → 3 s 6 p; koc 1 ZK 10 s → 1 ZK 4 s; namiot 4 ZK 10 s → 3 ZK 12 s; latarnia 1 ZK 3 s → 18 s |
| broń palna | 1,5 → 1 | Baza = źródło (arkebuz 8 s ang., pistolety £2 16 s za parę) = RAW. Rzadkość prochu załatwia Dostępność, nie cena. | pistolet 15 → 10 ZK; rusznica 4 ZK 10 s → 3 ZK; muszkiet hochlandzki 150 → 100 ZK (= RAW) |
| alchemia | 1,5 → 1 | Ani jednego źródła. Baza i tak jest 1,5× RAW (mikstura lecznicza = 3 wizyty lekarza). | mikstura lecznicza 1 ZK 3 s → 15 s; czarny lotos 45 → 30 ZK |
| prestiż | 3 → 1,5 | Przy ×3 strój dworski kosztował 90 ZK, a płytówka 96 ZK. To łamie Twoją zasadę z drugiej rundy. Nowa reguła: płytówka ≥ 2× strój dworski. | strój dworski 90 → 45 ZK; perfumy 3 ZK → 1 ZK 10 s |
| konie | 1,5 → 1 (robocze) | Kraków: koń pociągowy 14–16 ZK, siodłowy 34–46 ZK — ×1 trafia w środek. Bojowe (rumak, lekki koń bojowy) wydzielone i zostają ×1,5. | koń pociągowy 22 ZK 10 s → 15 ZK; wierzchowy 57 → 38 ZK; rumak bez zmian 825 ZK |

Do tego trzy poprawki pojedynczych pozycji:

- **Pancerz skórzany** (kurta, kaftan, nogawice, hełm, kolet) — nowa klasa ×1,5. Test płatnerza, który uzasadnia ×2
  dla pancerza, dotyczy stali, a skórę szyje rymarz ze Statusem Srebro 1–2. Kurta: 2 ZK 4 s → 1 ZK 13 s
  (źródło: 14–27 s). Kolczuga ÷ kurta = 12, w normie 4–20.
- **Flamberg** — 90 → 51 ZK. Miał bazę równą RAW bez źródła, a miecz dwuręczny ma bazę obniżoną ze źródła (0,57× RAW).
  Teraz trzyma proporcję z podręcznika: 3× miecz dwuręczny. Nowa reguła rodziny pilnuje 1,5–3,5.
- **Arkan** — z klasy broń do codzienne. To lina z pętlą, a nie wyrób zbrojmistrza. 1 ZK → 12 s (lina 10 m kosztuje 12 s).

Preset `zalecany_v4` zostaje w `data/klasy_cenowe.json`. Jedno kliknięcie w panelu MG przywraca stare ceny.

---

## 4. Broń: Zalety, Wady i cena

### 4.1 Zasada

Cena broni wynika z trzech rzeczy: materiału i pracy (test rzemieślnika), stanu (premia znaku stanu dla mieczy)
oraz jakości, czyli Zalet i Wad. HR-024 wycenia jakość jako mnożnik: każda Wada ×½, każda Zaleta ×2.

To, co potwierdziłeś: **topór jest tańszy od miecza, bo sam z siebie gorzej paruje (−1 PS przy parowaniu)
i zużywa mniej stali**. Miecz nie ma Wad i jest droższy, bo jest symbolem stanu.

### 4.2 Co sprawdziłem bez podręcznika

PDF-y z podręcznikiem i „Pod Bronią” zniknęły z sesji, więc nie mam pełnej tabeli Zalet i Wad.
Sprawdziłem to, co da się sprawdzić z cen i Twoich zasad:

| Para | Cena v5 | Stosunek | Reguła | Wynik |
|---|---|---|---|---|
| miecz ÷ topór | 3 ZK 9 s ÷ 16 s | 4,3 | 2–6 | zgodne |
| miecz ÷ broń ręczna | 3 ZK 9 s ÷ 1 ZK 14 s | 2,0 | 1,3–4 | zgodne |
| topór < nadziak < buzdygan < młot jednoręczny | 16 s < 17 s < 1 ZK 2 s < 1 ZK 14 s | — | rośnie z ilością stali | zgodne |
| flamberg ÷ miecz dwuręczny | 51 ÷ 17 ZK | 3,0 | 1,5–3,5 (nowa) | zgodne po poprawce |
| szabla ÷ miecz | 5 ZK 2 s ÷ 3 ZK 9 s | 1,5 | — | szabla droższa, jak w RAW (2× miecz) |
| łuk elfi ÷ łuk długi | 6 ZK 10 s ÷ 1 ZK 6 s | 5 | 4,5–5,5 (decyzja MG) | zgodne (v5.1) |

### 4.3 Co zostaje do zrobienia z podręcznikiem

`data/bron_cechy.json` ma szablon dla 83 pozycji broni białej i zasięgowej (z palną): pola `zalety` i `wady`
są puste, a wpisane jest tylko to, co sam ustaliłeś (miecz bez Wad, topór gorzej paruje). Kiedy agent albo Ty
uzupełnicie je z podręcznika (s. 294–295) i z „Pod Bronią” (s. 91–93), test `bron_cechy` sprawdzi regułę:
**w obrębie jednej grupy broni (np. jednoręczna, drzewcowa) więcej Zalet minus Wad = nie taniej**.
Wyjątki muszą być opisane w polu `wyjatek` (znak stanu, inny materiał, egzotyka).

---

## 5. Zarobki profesji a ceny

### 5.1 Metoda

Dla 33 profesji, które mają oczywiste „narzędzie zawodu”, policzyłem trzy miary dla każdego poziomu profesji.
Status dochodu wziąłem z audytu (`data/audyt.json`): najpierw poprawiony dochód, potem poprawiona pozycja, potem RAW.

- **Robót netto** — ile Robót trzeba odłożyć (rzut na zarobek = netto za jedną Robotę). To tempo gry.
- **Tygodni brutto** — ile tygodni pełnego zarobku kosztuje rzecz. To porównuje się ze źródłami.
- **% rocznego brutto** — dla kapitału (koń, łódź, warsztat).

Lista zakupów jest moim wyborem: to, czego profesja używa do pracy. To nie jest wyposażenie z podręcznika.
Wyposażenie startowe dostaje się za darmo, więc jego cena liczy się dopiero wtedy, gdy trzeba je odkupić.

### 5.2 Wynik

| Profesja (dochód) | Zakup | Cena v5 | Robót netto | Tyg. brutto | % roku | Źródło dla porównania |
|---|---|---|---|---|---|---|
| Rycerz (Srebro 5) | pełna płytówka | 96 ZK | 70 | 14 | 27% | Mediolan 1441: 20–40% rocznego dochodu rycerza — **zgodne** |
| Rycerz (Srebro 5) | rumak | 825 ZK | 600 | 120 | 231% | destrier 1–4 lata dochodu — **zgodne** |
| Rekrut (Srebro 1) | półzbroja municyjna | 14 ZK 10 s | 53 | 10,5 | 20% | korselet + morion 1590 ≈ 5,5 tyg. żołdu lancknechta — 2× drożej, ale w granicy |
| Żołnierz (Srebro 3) | półzbroja municyjna | 14 ZK 10 s | 18 | 3,5 | 7% | jak wyżej — **zgodne** |
| Żołnierz (Srebro 3) | kolczuga | 20 ZK | 24 | 4,8 | 9% | Twoja kotwica (nowe wydanie) |
| Chłopka (Brąz 3) | wół | 6 ZK | 44 | 8,7 | 17% | Kraków: wół 75 gr ÷ 9 gr tygodniowo = 8,3 tyg. — **zgodne** |
| Zwiadowca (Brąz 5) | koń wierzchowy | 38 ZK | 166 | 33 | 64% | Kraków: koń siodłowy ÷ płaca czeladnika = 30–40 tyg. — **zgodne** |
| Woźnica (Srebro 2) | wóz + 2 konie pociągowe | 42 ZK | 76 | 15 | 29% | v5.1 (pojazd ×1,5): wóz 18 ZK → 48 ZK = 17,5 tyg. |
| Kapitan Barki (Srebro 5) | barka rzeczna | 150 ZK | 109 | 22 | 42% | v5.1: barka 225 ZK = 63% roku; źródło 64–190% |
| Mistrzyni Rzemiosła (Srebro 3) | warsztat | 320 ZK | 388 | 78 | 149% | Frankfurt: dom rzemieślnika 0,7–1,6 roku zarobku mistrza — **zgodne** (górna granica) |
| Rzemieślniczka (Srebro 1) | narzędzia pracy | 7 ZK 4 s | 26 | 5,2 | 10% | — |
| Kawalerzysta (Srebro 4) | lekki koń bojowy | 262 ZK 10 s | 239 | 48 | 92% | brak źródła; MG: konie bojowe mają być drogie |
| Czarodziej (Srebro 4) | księga magii | 120 ZK | 109 | 22 | 42% | brak źródła; rękopis medyczny £5–20 = 35–140 ZK |
| Medyczka (Srebro 3) | księga medycyny | 60 ZK | 73 | 14,5 | 28% | rękopis medyczny 35–140 ZK — **zgodne** |
| Łowca Czarownic (Srebro 3) | pistolet | 10 ZK | 12 | 2,4 | 5% | para pistoletów £2 16 s — **zgodne** |
| Strażnik (Srebro 1) | halabarda | 1 ZK 12 s | 6 | 1,2 | 2% | halabarda 4 s ang. — **zgodne** |
| Łowczyni (Brąz 4) | łuk długi | 1 ZK 6 s | 7 | 1,4 | 3% | łuk 3 s 4 d — **zgodne** |
| Złodziej (Brąz 3) | wytrychy | 1 ZK 4 s | 9 | 1,7 | 3% | — |

Pełna tabela: `docs/analiza_v5/profesje.csv` (33 profesje × 4 poziomy × zakupy).

### 5.3 Czy to ma sens

**Tak, z trzema zastrzeżeniami z rozdz. 7.** Wzór jest taki sam jak w źródłach:

- **Codzienne życie** jest skalibrowane na Brąz 3 i tak ma zostać. Jedzenie (14 p dziennie), kąt w izbie czeladnej
  (24 p tygodniowo) i odzież z samodziału (ok. 6 p tygodniowo) dają 128 p z 132 p, które Brąz 3 ma na utrzymanie
  (80% z 165 p). Test budżetu pilnuje tego automatycznie.
- **Narzędzia zawodu** kosztują 1–8 tygodni brutto profesji, która ich używa. Halabarda strażnika, łuk łowczyni,
  pistolet łowcy czarownic i półzbroja żołnierza leżą w tym przedziale — tak jak w źródłach.
- **Kapitał** kosztuje od pół roku do 2,5 roku: koń dla Brązu 5, warsztat dla mistrza, płytówka i rumak dla rycerza.
  Historycznie te rzeczy kupowało się na kredyt, w spadku albo z łupu, a nie z pensji. W grze to samo:
  gracz dostaje je z przygody, od patrona albo z wyposażenia startowego.

**Tempo gry (Roboty).** Netto to tylko 20% brutto, więc w Robotach wszystko jest 5× wolniejsze niż w tygodniach brutto.
Żołnierz odkłada na kolczugę 24 Roboty. To celowe: pieniądze z Robót mają być powolne, a duże zakupy mają
pochodzić z przygód. Jeśli chcesz szybciej, zmienia się to w zasadzie zarobku (netto/brutto), a nie w cenniku.

**Gdzie zarobki mogłyby się nie zgadzać.** Statusy profesji wojskowych są u nas wyższe niż historyczny żołd:
Żołnierz (Srebro 3) zarabia 2× tyle, co lancknecht z 4 guldenami miesięcznie. Rekrut (Srebro 1) zarabia
ok. ⅔ tego, co lancknecht. To decyzja z audytu Statusów, nie z cennika. Ceny broni i pancerza mierzone Rekrutem zgadzają się ze źródłem
w granicy 2×.

---

## 6. Co jeszcze sprawdziłem i zostawiam bez zmian

- **Księgi ×2.** Jedyne źródło (rękopis medyczny 35–140 ZK) mówi 2,9×, test skryby 1,4×. ×2 jest pośrodku.
- **Odzież ×1,5.** Test szewca 1,4, krawca 1,8. Źródła krakowskie są niższe, bo mistrz szewski ma u nas Srebro 1
  (2× robotnik), a w Krakowie zarabiał mniej.
- **Broń ×2.** Wygląda na „drożej”, ale baza broni była **poniżej** źródeł (0,57×). Po ×2 broń ma 1,16× źródła.
  To jedyna klasa, w której mnożnik przybliża do historii, zamiast od niej oddalać.
- **Pancerz ×2.** Oddala od źródeł angielskich (1,7×), ale tę cenę wyznacza Twoja kotwica: kolczuga 20 ZK.
  Test płatnerza (mistrz Złoto 1 + dwóch czeladników) daje to samo.
- **Pozycje ze skrajnym stosunkiem do RAW** (łuki ×0,25, kolczuga ×6,7, nóż ×0,12) — wszystkie mają źródło
  albo wynikają z kotwicy. RAW w tych miejscach jest niespójny z resztą podręcznika (łuk za 4 ZK przy mieczu za 1 ZK).

---

## 7. Decyzje MG (2026-10-24, v5.1)

| Sprawa | Decyzja MG | Wprowadzone |
|---|---|---|
| Konie bojowe | „Królestwo za konia” — mają być drogie | bez zmian: ×1,5. Rumak 825 ZK, lekki koń bojowy 262 ZK 10 s |
| Wozy, łodzie, barki | trochę drogie, ale chłop musi mieć wóz | pojazd ×1,5: furmanka 6 ZK, wóz 18 ZK, łódź wiosłowa 18 ZK, barka 225 ZK, powóz 150 ZK, uprząż z siodłem 7 ZK 10 s |
| Łuk elfi | 5× łuk długi | ×1 = 5 × 156 p; cena 6 ZK 10 s (było 30 ZK). Nowa reguła rodziny 4,5–5,5 |
| Cena z podręcznika | zawsze widoczna do porównania | kolumna „Podręcznik (RAW)” w cenniku, u kupca i w zamówieniu |

**Czy chłopa stać na wóz.** Furmanka 6 ZK to 8,7 tygodnia brutto Brązu 3 — tyle samo co wół (Kraków: 8,3).
Wóz czterokołowy 18 ZK to pół roku brutto chłopa: rzecz kmiecia albo kilku rodzin razem, nie komornika. Źródła
(wóz 15 guldenów = 34 ZK) dają więcej; ×1,5 zostawia wóz w zasięgu wsi.

**Test kołodzieja.** Czas pracy nad wozem poprawiony z 8 na 12 dni (koła z żelaznymi obręczami to robota kołodzieja
i kowala). Wóz za 18 ZK = 1,75× kosztu warsztatu, w normie.

### 7.1 Otwarte: wyposażenie profesji z podręcznika

Plik z profesjami zniknął z sesji. Jeśli wgrasz go ponownie (albo położysz PDF w `reference/pdf/` dla agenta),
da się dla każdej ścieżki profesji policzyć, ile kosztuje odkupienie wyposażenia startowego w Robotach.

---

## 8. Decyzje MG z 2026-10-24, część 2 (v5.2)

Po v5 bilans wobec v4 to 134 pozycje tańsze i 42 droższe (broń palna, wyroby alchemiczne, pojazdy).

### 8.1 Broń palna droga: ×2

| | Podręcznik | v5.2 |
|---|---|---|
| Pistolet | 8 ZK | 20 ZK |
| Rusznica | 4 ZK | 6 ZK |
| Muszkiet hochlandzki | 100 ZK | 200 ZK |
| Śrut i proch (12) | 3 s 3 p | 7 s |

### 8.2 Alchemia: składniki osiągalne, wyroby drogie

Klasa „alchemia” rozdzielona na dwie:

- **Składniki** (salwort, korzeń mandragory, księżycowy kwiat, nocny cień, ziemny korzeń, pluja, fakstoryl,
  dziwnokorzeń, grzybki, czarny lotos) — ×1, ceny jak w podręczniku albo lekko wyżej (×1 naszego cennika).
- **Wyroby** (mikstura lecznicza, eliksir żywotności, kataplazm, tonik, rozkosz Ranalda, sercobój) — ×2, bo
  wymagają aparatury i Wiedzy.

| | Podręcznik | v5.2 |
|---|---|---|
| Mikstura lecznicza | 10 s | 1 ZK 10 s |
| Eliksir żywotności | 18 s | 2 ZK |
| Kataplazm leczniczy | 12 s | 1 ZK 4 s |
| Salwort (składnik) | 12 s | 12 s |
| Korzeń mandragory (składnik) | 1 ZK | 1 ZK |

### 8.3 Ile to kosztuje ludzi na różnych szczeblach

Tygodnie pełnego zarobku brutto / liczba Robót netto potrzebnych do odłożenia:

| Zakup | Brąz 3 | Brąz 5 | Srebro 1 | Srebro 3 | Srebro 5 | Złoto 1 |
|---|---|---|---|---|---|---|
| Pistolet 20 ZK | 29 tyg. / 145 R | 17,5 / 87 | 14,5 / 73 | 4,8 / 24 | 2,9 / 15 | 1,3 / 7 |
| Rusznica 6 ZK | 8,7 / 44 | 5,2 / 26 | 4,4 / 22 | 1,5 / 7 | 0,9 / 4 | 0,4 / 2 |
| Mikstura lecznicza 1 ZK 10 s | 2,2 / 11 | 1,3 / 7 | 1,1 / 5 | 0,4 / 2 | 0,2 / 1 | 0,1 / 1 |
| Eliksir żywotności 2 ZK | 2,9 / 15 | 1,7 / 9 | 1,5 / 7 | 0,5 / 2 | 0,3 / 1 | 0,1 / 1 |
| Korzeń mandragory 1 ZK | 1,5 / 7 | 0,9 / 4 | 0,7 / 4 | 0,2 / 1 | 0,1 / 1 | 0,1 / 0 |

Pistolet to broń Srebra 3 i wyżej; chłop go nie kupi. Rusznica jest w zasięgu żołnierza. Mikstura lecznicza kosztuje
około tygodnia pracy rzemieślnika — droga, ale gracze ją kupią.

### 8.4 Majątek kupca: towar i gotówka

Każdy kupiec ma w `kupcy.json` dwie liczby w tygodniach brutto swojego Statusu: **towar na stanie** i **gotówkę**
(gotówka × 0,5–1,4 z rzutu 1k10). Budżet towaru dzieli się na pozycje (główny asortyment waży 2, poboczny 1) i ogranicza
liczbę sztuk. Rzecz, której jedna sztuka kosztuje ponad 4× budżet pozycji, wypada ze sklepu — można ją zamówić.

Średnio na 50 sklepów (miasto):

| Kupiec | Status | Gotówka | Towar na stanie |
|---|---|---|---|
| Domokrążca | Brąz 4 | 1 ZK 14 s | 9 ZK |
| Kramarz | Srebro 1 | 2 ZK 12 s | 8 ZK |
| Kowal wiejski | Brąz 5 | 3 ZK 4 s | 13 ZK |
| Rzemieślnik cechowy | Srebro 3 | 11 ZK 12 s | 38 ZK |
| Zbrojmistrz | Srebro 4 | 20 ZK 12 s | 91 ZK |
| Płatnerz | Złoto 1 | 56 ZK | 174 ZK |
| Kupiec bławatny (hurt) | Srebro 5 | 39 ZK | 124 ZK |
| Kwatermistrz | Srebro 4 | 41 ZK | 171 ZK |

Kramarz ma kilkadziesiąt drobiazgów po 1–2 sztuki i kilkanaście sztuk najtańszych rzeczy (chleb, piwo).
Namiot ma najwyżej jeden. Skup droższy niż gotówka kupca jest oznaczony „brak gotówki”.

### 8.5 Noclegi

- **Wspólna izba** = spanie na ławie albo na podłodze, 10 p (RAW). Usunięte błędne źródło („łóżko w gospodzie”).
- **Nocleg w stajni (na sianie)** — nowa pozycja, 4 p. Szacunek; często za darmo do posiłku.
- **Stajnia dla konia na 1 noc (z obrokiem)** — 14 p, tylko nazwa doprecyzowana.
- Nowa reguła: stajnia < wspólna izba < prywatny pokój.

### 8.6 Zarobki profesji — dalsze korekty Dochodu

Pozycja (Status społeczny) zostaje bez zmian, poprawiony jest tylko Dochód. Punkt odniesienia — wielokrotność
robotnika (Brąz 3): lancknecht ≈ 3×, Doppelsöldner ≈ 6×, rajtar z koniem ≈ 9×, strażnik miejski 1,5–2×,
tragarz 1–1,3×, służba z wiktem: gotówki 0,3–0,7×. Drabina: Srebro 1 = 2×, S2 = 4×, S3 = 6×, S4 = 8×, S5 = 10×, Złoto 1 ≈ 22×.

| Profesja | Poziom | Było | v5.2 |
|---|---|---|---|
| Służąca | Służąca | Brąz 3 + wikt | **Brąz 2 + wikt** |
| Służąca | Pokojowa | Srebro 1 + wikt | **Brąz 3 + wikt** |
| Służąca | Ochmistrzyni | Srebro 4 + wikt | **Srebro 1 + wikt** |
| Żołnierz | Żołnierz | Srebro 3 | **Srebro 2** |
| Żołnierz | Sierżant | Srebro 5 | **Srebro 3** |
| Strażnik | Sierżant Straży | Srebro 3 | **Srebro 2** |
| Strażnik | Kapitan Straży | Złoto 1 | **Srebro 4** |
| Strażnik (rzeczny) | Strażnik Rzeczny | Srebro 2 | **Srebro 1** |
| Strażnik (rzeczny) | Żołnierz Okrętowy | Srebro 4 | **Srebro 2** |
| Strażnik (rzeczny) | Mistrz Żołnierzy Okrętowych | Złoto 1 | **Srebro 4** |
| Strażnik Dróg | Sierżant | Srebro 4 | **Srebro 3** |
| Strażnik Dróg | Kapitan | Złoto 1 | **Srebro 5** |
| Kawalerzysta | Sierżant Kawalerii | Złoto 1 | **Srebro 5** |
| Kawalerzysta | Oficer Kawalerii | Złoto 2 | **Złoto 1** |
| Doker | Doker | Srebro 1 | **Brąz 5** |
| Doker | Brygadzista | Srebro 3 | **Srebro 2** |
| Doker | Mistrz Dokerów | Srebro 5 | **Srebro 3** |

Reszta profesji mieści się w historycznych widełkach — szczegóły w `docs/analiza_v5/profesje.csv` i w Audycie.

## 9. Pliki

| Plik | Zawartość |
|---|---|
| `docs/analiza_v5/cennik_przeglad.csv` | 364 pozycje: RAW, ×1, mnożnik, cena v5, × RAW, przedział źródła, × źródła, tygodnie Brązu 3, flagi |
| `docs/analiza_v5/klasy.csv` | tabela z rozdz. 3.3 |
| `docs/analiza_v5/profesje.csv` | 33 profesje × poziomy × zakupy |
| `docs/analiza_v5/wyniki.json` | liczby z tego dokumentu |
| `narzedzia/analiza_v5.py` | skrypt; uruchom ponownie po każdej zmianie cennika |
| `narzedzia/buduj_v5.py` | buduje dane v5 z archiwum v4 |
