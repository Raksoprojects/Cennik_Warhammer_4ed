> **ARCHIWUM — stan v4.** Liczby i zasady tutaj mogą być nieaktualne. Obowiązują: `data/*.json`, `docs/KOMPENDIUM_DANE.md` (generowany z danych), `docs/DANE.md` (decyzje MG) i `docs/AGENT_BRIEF.md`. Czytaj ten plik tylko po historię decyzji i źródła. Indeks: `docs/archiwum/README.md`.

# Ceny ×3 — analiza i spójność wewnętrzna (cennik v4)

Odpowiedź na pytanie: czy podnosić ceny ×3, gdzie to ma sens, a gdzie nie — i jak dopilnować,
żeby po podwyżce nie dało się kupić jednej rzeczy taniej niż jej własnych składników.

**Krótko:**

- ×3 przy niezmienionych zarobkach oznacza Imperium trzy razy biedniejsze w wyrobach. Dla broni,
  koni, pancerza, prestiżu, prochu i mikstur to działa. Dla narzędzi, ubrań, wozów, ksiąg, zwierząt
  rzeźnych, biżuterii i najtańszych kwater — łamie się, i to w sposób, który gracze znajdą.
- Są dwa gotowe, spójne warianty: **`drogi`** (najbliżej Twojego ×3) i **`zalecany`**. Oba przechodzą
  wszystkie 10 rodzin testów. Ślepe ×3 łamie 7 z nich.
- Niezależnie od poziomu cen, w v3 były błędy typu „płachta za koce": koc był tańszy od sukna, z którego
  jest zrobiony, prześcieradło kosztowało 3 s przy materiale za 9 s. Te poprawki obowiązują już teraz
  (`data/cennik.json` = v4-baza).

Testy: `node --test test/*.test.mjs` (22/22). Presety:
`CENNIK=propozycja/cennik_v4_drogi.json CZYNSZE=propozycja/czynsze_v4.json node --test test/spojnosc.test.mjs test/arbitraz.test.mjs` (14/14).

---

## 1. Co naprawdę znaczy ×3

Zarobki zostają z RAW, więc ×3 na przedmioty to nie „wszystko drożeje", tylko **siła nabywcza zarobków
spada trzykrotnie wobec rzeczy, a wobec jedzenia zostaje ta sama**. To ma trzy skutki.

**Kto to odczuje.** Biedni wydają prawie wszystko na jedzenie i dach nad głową, więc ×3 na rzeczy ich
nie dotknie — o ile jedzenie i najtańsza kwatera zostaną ×1. Najbardziej odczuje to środek drabiny:
mieszczanin, żołnierz, awanturnik, czyli ludzie, którzy kupują sprzęt. Dla kampanii to dobra wiadomość:
podwyżka trafia dokładnie w graczy.

**Jak to czytać w świecie.** Jako Imperium wyniszczone wojną, z cechami trzymającymi ceny i z drogim
żelazem. To uczciwa decyzja ponuro-fantastyczna, nie błąd.

**Kto na tym zarabia.** Tu jest haczyk. Jeśli nóż kosztuje trzy razy więcej, a kowal ma ten sam Status,
to różnicę ktoś zgarnia. Test rzemieślnika (rozdz. 4) pokazuje, że przy ×3 wiejski kowal zarabiałby
na sierpie **4× swoje brutto**, a szewc na butach — 3×. Czyli albo podnosisz Status rzemieślników
(i cała drabina się sypie), albo ×3 dla prostych wyrobów jest za dużo.

---

## 2. Twoje dwa argumenty

### Karczma a najem

Twój rachunek jest poprawny: prywatny pokój w karczmie 3 s × 33 noce = **4 ZK 19 s** miesięcznie.
Najem musi być tańszy niż mieszkanie w karczmie — inaczej nikt by nie wynajmował — ale nie absurdalnie
tańszy. Przyjąłem pasmo: miesiąc najmu = 10–50% miesiąca w odpowiedniej izbie karczmy.

Z drugiej strony jest budżet robotnika. Brąz 3 ma 132 p tygodniowo na utrzymanie (80% z 165 p).
Jedzenie to ok. 98 p, kąt w izbie 24 p, odzież z samodziału ok. 6 p — razem **128 p ze 132 p**.
Kąt w izbie czeladnej nie zniesie więc żadnej podwyżki (maks. ×1,1). Historycznie tak właśnie było:
czeladź mieszkała u mistrza, bo na własny kąt nie było jej stać.

Wychodzi z tego:

| Kwatera | v3 | v4 (drogi, zalecany) | Uzasadnienie |
|---|---|---|---|
| Kąt w izbie czeladnej | 7 s/mies. | **7 s** | budżet Brązu 3 — ×1 to maksimum |
| Izba na poddaszu | 8 s | **8 s** | budżet Brązu 4 |
| Izba w kamienicy | 12 s | **1 ZK 4 s** | ≤ 25% brutto Srebra 1 |
| Mieszkanie (2–3 izby) | 1 ZK | **2 ZK** | ≤ 25% brutto Srebra 2 |
| Dom mistrza z warsztatem | 2 ZK | **4 ZK** | — |
| Kamienica kupiecka | 5 ZK 10 s | **11 ZK** | — |

Kupno domów idzie tym samym mnożnikiem ×2, bo stosunek ceny kupna do rocznego czynszu (7–25 lat) to
jedyna rzecz, którą znamy ze źródeł na pewno (Frankfurt 1450, Anglia XIV w.).

**Marienburg.** Mieszkanie: 2 ZK × 1,45 = 2 ZK 18 s w zwykłych czasach. Z kryzysem mieszkaniowym ×1,7
wychodzi **4 ZK 18 s** — czyli Twoje 5 ZK. W v3 kryzys musiał wynosić ×3,0, bo czynsze były o połowę
niższe. Przy czynszach v4 kryzys spada na ×1,7 (`propozycja/koniunktura_v4.json`), co jest
rozsądniejszą liczbą dla „kryzysu", a nie „katastrofy".

### Miecz jako znak stanu

Masz rację i to da się uzasadnić historycznie: prawo do noszenia miecza było przywilejem stanowym,
miecz wymaga więcej stali i umiejętności niż topór, a w *Pod Bronią* miecz jako jedyny w swojej grupie
nie ma żadnej Wady. Wprowadziłem **premię znaku stanu** dla mieczy: miecz, półtorak, dwuręczny, szabla,
bułat, rapier, floret, szpada, flamberg.

W obu wariantach miecz kosztuje **3 ZK 9 s** — dokładnie tyle, ile wychodzi Ci z ×3. Miecz jest
3–4,5 raza droższy od topora i co najmniej 1,3 raza od zwykłej broni ręcznej; pilnuje tego test.

---

## 3. Za i przeciw — klasa po klasie

Każda pozycja cennika dostała **klasę cenową** (`klasa`). Cena w wariancie = cena bazowa × mnożnik
klasy. Przedział spójny to zakres mnożnika, przy którym przechodzą wszystkie testy (pozostałe klasy
na wartościach zalecanych).

| Klasa | Co zawiera | Przedział spójny | drogi | zalecany | Za ×3 | Przeciw ×3 |
|---|---|---|---|---|---|---|
| utrzymanie | jedzenie, picie, nocleg, usługi, płace | **1** | 1 | 1 | — | To jest kotwica. Ruszysz ją — musisz ruszyć zarobki. |
| surowiec | sukno, płótno | 0,5–1,5 | 1 | 1 | — | Biedni szyją z samodziału; drożej = Brąz 3 bez koszuli. |
| rzeźne | kurczak, gęś, kapłon, owca, świnia | 0,75–1,05 | 1 | 1 | — | Przy ×3 świnia kosztuje 9 ZK, a jej mięso 3 ZK 7 s. Nikt by nie zabijał świń. |
| kruszec | pierścienie, sygnet, berło | 0,5–1,15 | 1 | 1 | — | Monety są ze złota. Złoty pierścień za 30 ZK = przetapiasz 4 ZK w monetach i masz zysk ×7. |
| najem dolny | kąt, poddasze | 0,5–1,1 | 1 | 1 | — | Brąz 3 nie stać na łóżko. |
| najem | izba, mieszkanie, dom, kamienica | 1,65–2,25 ¹ | 2 | 2 | — | Przy ×3 mieszkanie zjada > 25% brutto Srebra 2. |
| kupno | domy, warsztat | 1,75–2,4 ¹ | 2 | 2 | — | Musi iść razem z najmem (zwrot 7–25 lat). |
| robocze | wół, krowa, cielę, pies | 0,95–2,35 | 2 | 1 | Bydło jako kapitał chłopa | Kraków daje wołu za 75 gr = 6 ZK; to najlepsze źródło w zestawie. |
| konie | wszystkie konie, muł, kucyk | bez granic wewn. | 2,5 | 1,5 | Rycerstwo naprawdę niedostępne | Przy ×3 rumak = 4,6 roku brutto rycerza; źródła mówią 1–4. |
| pojazd | wozy, łodzie, barka, uprząż | 0,5–1,4 | 1,25 | 1 | — | Kołodziej zarabiałby 4,7× swój Status. |
| codzienne | narzędzia, naczynia, worki, koce, lampy | 0,95–1,55 | 1,5 | 1,5 | — | Wiejski kowal: sierp 4×, siekiera 3,7× ponad koszt. Najciaśniejsza klasa. |
| odzież | ubrania, buty, kapelusze | 1,1–2,1 | 2 | 1,5 | — | Szewc 3× ponad koszt. |
| prestiż | strój dworski, perfumy, laska, jedwab | bez granic | 3 | 3 | Zbytek ma kosztować | — |
| broń | broń biała, łuki, kusze, amunicja | 1,5–2,7 | 2,5 | 2 | Broń jako inwestycja | Powyżej 2,7 zbrojmistrz zarabia ponad 2,2× koszt. |
| proch | broń palna, proch, bomby | bez granic | 3 | 1,5 | „Wyjątek Nuln" — koncesja | Pistolet 30 ZK = 22 tyg. pracy robotnika. |
| pancerz | skóra, kolczuga, płyta | 1,15–2,4 | 2,25 | 2 | Kolczuga 20–22 ZK = nowe wydanie WFRP | ×3 = płytówka 144 ZK wobec 50–60 w nowym wydaniu; napierśnik 2,7× koszt płatnerni. |
| księga | księgi, mapy | 0,75–2,2 | 2 | 2 | — | Skryba 3× ponad koszt. |
| alchemia | zioła, mikstury, narkotyki | bez granic | 3 | 1,5 | Leczenie ma boleć sakiewkę | Mikstura lecznicza 2 ZK 5 s = 2 tyg. pracy robotnika. |

¹ Najem i kupno są związane: zmieniasz jedno, zmieniaj drugie w tej samej proporcji.

**„Bez granic wewnętrznych"** znaczy, że żaden test się nie łamie — decyzja jest czysto o klimacie.
Konie, prestiż, proch i alchemia to dokładnie te klasy, w których możesz robić ×3 bez żadnych skutków
ubocznych.

---

## 4. Testy spójności

Dziesięć rodzin, w tym dokładnie ta, o którą pytałeś: czy kupno jednej rzeczy nie pozwala zdobyć
kilku innych.

| Test | Co sprawdza | Przykład |
|---|---|---|
| 59 reguł | kolejność w grupach (kucyk < muł < koń…), sumy elementów, proporcje | płytówka ≈ suma 4 elementów ±10% |
| **materiał ≤ produkt** | rzecz nie może być tańsza niż jej własny materiał | koc ≥ 3 łokcie sukna szarego + 10% |
| pełne ≥ puste naczynie | butelka wina ≥ pusta butelka + wino | przy ślepym ×3 pusta butelka (9 s) droższa od pełnej (5 s) |
| **rodziny rzeczy** | stosunki cen rzeczy, które gracz porównuje wzrokiem | plandeka ÷ koc 0,8–3; namiot ÷ koc 2–8; miecz ÷ topór 2–6 |
| tusza vs żywe zwierzę | mięso z tuszy = 0,7–2,5× ceny zwierzęcia | krowa: 110 kg mięsa |
| biżuteria vs kruszec | pierścień ≤ 4× wartości metalu w monetach | 1 ZK ≈ 1,5 g złota (z kursu złotego polskiego) |
| budżet utrzymania | 80% brutto Brązu 3–4 pokrywa jedzenie, kąt i odzież | 128 p ze 132 p |
| karczma vs najem | miesiąc najmu = 10–50% miesiąca w karczmie | Twój rachunek z 3 s × 33 |
| zwrot z kupna domu | kupno = 7–25 lat czynszu (kamienica 7–40) | Frankfurt 1450 |
| test rzemieślnika | cena ÷ koszt warsztatu = 0,7–2,2 | koszt = dni pracy × brutto mistrza i czeladników + materiał |

### Wyniki

| Test | v3 | ×3 ślepe | **drogi** | **zalecany** |
|---|---|---|---|---|
| 59 reguł | ✓ | ✗ butelka | ✓ | ✓ |
| materiał ≤ produkt | ✗ 6 pozycji | ✓ | ✓ | ✓ |
| pełne ≥ puste | ✓ | ✗ | ✓ | ✓ |
| rodziny rzeczy | ✗ koc = 5 prześcieradeł | ✓ | ✓ | ✓ |
| tusza vs zwierzę | ✓ | ✗ 8 zwierząt | ✓ | ✓ |
| biżuteria vs kruszec | ✓ | ✗ | ✓ | ✓ |
| budżet utrzymania | ✓ | ✗ Brąz 3 i 4 | ✓ | ✓ |
| karczma vs najem | ✓ | ✗ kąt = 84% karczmy | ✓ | ✓ |
| zwrot z kupna | ✓ | ✓ | ✓ | ✓ |
| test rzemieślnika | ✗ broń za tania ² | ✗ 8 wyrobów | ✓ | ✓ |

² Ciekawostka: przy v3 broń i płyta są **za tanie** — zbrojmistrz zarabia połowę swojego Statusu.
To jest twardy argument za Twoją intuicją, że broń powinna być droższa.

### Test rzemieślnika w liczbach

Cena ÷ koszt warsztatu. Norma 0,7–2,2. Czasy pracy to **szacunki rzędu wielkości**, nie dane ze źródeł.

| Wyrób | Warsztat | Dni | v3 | ×3 ślepe | drogi | zalecany |
|---|---|---|---|---|---|---|
| Nóż | kuźnia wiejska | 0,1 | 0,97 | **2,90** | 1,45 | 1,45 |
| Sierp | kuźnia wiejska | 0,25 | 1,37 | **4,10** | 2,05 | 2,05 |
| Siekiera | kuźnia wiejska | 0,3 | 1,24 | **3,71** | 1,94 | 1,94 |
| Topór | zbrojmistrz | 0,5 | **0,55** | 1,64 | 1,36 | 1,09 |
| Miecz | zbrojmistrz | 1,5 | **0,54** | 1,63 | 1,63 | 1,63 |
| Kolczuga | zbrojmistrz | 10 | 0,70 | 2,11 | 1,58 | 1,40 |
| Napierśnik | płatnernia | 5 | 0,91 | **2,72** | 2,04 | 1,82 |
| Pełna płytówka | płatnernia | 25 | **0,63** | 1,88 | 1,41 | 1,26 |
| Buty | szewc | 1 | 1,02 | **3,05** | 2,03 | 1,52 |
| Koc | tkacz | 1 | 1,19 | **3,56** | 1,78 | 1,78 |
| Łuk długi | łuczarz | 2 | 0,70 | 2,10 | 1,77 | 1,40 |
| Księga, medycyna | skryba | 100 | 0,99 | **2,96** | 1,97 | 1,97 |
| Wóz | kołodziej | 8 | 1,56 | **4,68** | 1,95 | 1,56 |

Warsztat = dzienne brutto mistrza i czeladników z drabiny Statusu, np. zbrojmistrz = Srebro 4 +
dwóch czeladników Brąz 5 = 312 p/dzień.

---

## 5. Niespójności v3 — poprawione teraz, bez względu na wybór

Te zmiany są na poziomie ×1 i już obowiązują w `data/cennik.json`.

**Tkaniny.** Cennik znał tylko sukno krakowskie po 23 gr łokieć — czyli sukno cienkie, importowane.
Z niego wychodziło, że koc za 15 s jest tańszy od 3 łokci materiału, a płaszcz od 4. Dopisałem dwa
materiały, z których szyje się 90% rzeczy:

| Nowa pozycja | Cena | Status |
|---|---|---|
| Sukno szare, samodział (łokieć) | 6 s | **szacunek**: cena ubrania (Kolonia 1390) minus robota krawca |
| Płótno zgrzebne, konopne (łokieć) | 8 p | **szacunek**: ok. ½ płótna krakowskiego |
| Olej do lampy (litr) | 2 s | **szacunek**: bez niego godzina lampy na oliwie z importu kosztowała 20× więcej niż godzina świecy |

I podniosłem rzeczy, które były tańsze od własnego materiału:

| Pozycja | v3 | v4 | Materiał |
|---|---|---|---|
| Koc | 15 s | **1 ZK** | 3 łokcie sukna szarego |
| Zwijane posłanie | 18 s | **1 ZK 7 s** | koc + siennik + rzemienie |
| Siennik | 1 s 5 p | **3 s 6 p** | 4 łokcie zgrzebnego |
| Prześcieradło | 3 s | **10 s** | 6 łokci płótna |
| Worek / duży worek | 1 s / 2 s | **1 s 6 p / 3 s** | 2 / 4 łokcie zgrzebnego |
| Płaszcz | 1 ZK 5 s | **1 ZK 6 s** | 4 łokcie szarego |
| Opończa | 1 ZK 12 s | **1 ZK 16 s** | 5 szarego + podszewka |
| Kaptur | 6 s | **6 s 6 p** | 1 łokieć szarego |

Skąd tak niskie ceny w v3? Część pochodziła z angielskich **inwentarzy pośmiertnych** (siennik 2 d
w 1457 r., koc z lat 1349–52). Inwentarze wyceniają rzeczy **używane** — nowa cena była wyższa.

**Reguła spania.** Stara reguła „koc < posłanie < plandeka < namiot” mieszała wełnianą pościel
z płócienną płachtą. Rozdzieliłem na dwa łańcuchy: koc < posłanie oraz koc < plandeka < namiot.
Przy okazji to odpowiada na Twoje pytanie wprost: **plandeka kosztuje 1,25 koca**, namiot 3 koce.
Nie da się sprzedać płachty i kupić za nią kilku kocy.

**Ćwiertnia.** Objętość krakowskiej ćwiertni w XVI w. nie jest ustalona: korzec krakowski to 36–60 l
(Gilewicz, Rybarski), ćwiertnię 128 l przyjął Grodecki, ale jego założenie jest kwestionowane.
Dwa niezależne łańcuchy w naszym cenniku — chleb i obrok w stajni — są spójne **tylko** jeśli ćwiertnia
ma ok. 100–130 l. Przy 44 l bochenek chleba i noc w stajni z owsem byłyby tańsze od zboża, z którego
powstają. Przyjąłem roboczo ~120 l i zapisałem to w opisie pozycji. Cen to nie zmienia.

**Nóż** przeszedł z klasy broni do narzędzi: robi go wiejski kowal, używa każdy chłop. Był
wąskim gardłem, które blokowało podwyżkę całej broni.

---

## 6. Kluczowe ceny

| Pozycja | v4-baza | ×3 ślepe | **drogi** | **zalecany** | tyg. pracy robotnika (zalec.) |
|---|---|---|---|---|---|
| Prowiant na 1 dzień | 2 s | 2 s | 2 s | 2 s | 0,1 |
| Prywatny pokój, noc | 3 s | 3 s | 3 s | 3 s | 0,2 |
| Koc | 1 ZK | 3 ZK | 1 ZK 10 s | 1 ZK 10 s | 2,2 |
| Ubranie | 1 ZK 8 s | 4 ZK 4 s | 2 ZK 16 s | 2 ZK 2 s | 3,1 |
| Buty | 12 s | 1 ZK 16 s | 1 ZK 4 s | 18 s | 1,3 |
| Sierp | 3 s | 9 s | 4 s 6 p | 4 s 6 p | 0,3 |
| Miecz | 1 ZK 3 s | 3 ZK 9 s | **3 ZK 9 s** | **3 ZK 9 s** | 5,0 |
| Rapier | 4 ZK 11 s | 13 ZK 15 s | 13 ZK 15 s | 13 ZK 15 s | 20 |
| Kusza | 3 ZK 9 s | 10 ZK 5 s | 8 ZK 13 s | 6 ZK 18 s | 10 |
| Pistolet | 10 ZK | 30 ZK | 30 ZK | 15 ZK | 22 |
| Kolczuga | 10 ZK | 30 ZK | 22 ZK 10 s | **20 ZK** | 29 |
| Pełna płytówka | 48 ZK | 144 ZK | 108 ZK | 96 ZK | 140 |
| Koń wierzchowy | 38 ZK | 114 ZK | 95 ZK | 57 ZK | 83 |
| Rumak | 550 ZK | 1650 ZK | 1375 ZK | 825 ZK | 1200 |
| Wół | 6 ZK | 18 ZK | 12 ZK | 6 ZK | 9 |
| Złoty pierścień | 10 ZK | 30 ZK | 10 ZK | 10 ZK | 15 |
| Mieszkanie / miesiąc | 1 ZK | 3 ZK | 2 ZK | 2 ZK | 2,9 |
| Dom rzemieślnika | 160 ZK | 480 ZK | 320 ZK | 320 ZK | 465 |

Punkty odniesienia:

| | v4-baza | ×3 ślepe | drogi | zalecany | odniesienie |
|---|---|---|---|---|---|
| Kolczuga | 10 ZK | 30 ZK | 22 ZK 10 s | 20 ZK | nowe wydanie WFRP: 20 ZK |
| Pełna płytówka | 48 ZK | 144 ZK | 108 ZK | 96 ZK | nowe wydanie: 50–60 ZK |
| Płytówka ÷ roczne brutto rycerza | 13% | 40% | 30% | 27% | Mediolan 1441 ÷ dochód rycerza £20–40: 20–40% |
| Rumak ÷ roczne brutto rycerza | 1,5 roku | 4,6 roku | 3,8 roku | 2,3 roku | źródła: 1–4 lata |
| Kolczuga w Robotach Srebra 3 | 12 | 36 | 27 | 24 | — |

---

## 7. Skutki uboczne

**Generator kupców.** Limity osad i kupców (wieś 2 ZK, domokrążca 3 ZK…) oraz progi ilości sztuk
liczone są teraz od **ceny bazowej** (`cena_ref_p`), a nie od ceny po mnożniku. Bez tego przy ×3 wiejski
handlarz traciłby część asortymentu tylko dlatego, że wszystko podrożało. Zmiana w `src/silnik.js`.

**Preset w locie.** Nowa funkcja `zastosujPreset(cennik, klasyCenowe, 'drogi')` nakłada mnożniki
klas na cenę bazową. Aplikacja nie musi trzymać trzech cenników — wystarczy jeden plik bazowy
i przełącznik „poziom cen". Test sprawdza, że funkcja daje to samo co gotowe pliki.

**Magiczne przedmioty** (HR-026, cena × 50). Magiczny miecz o jednej właściwości: v3 57 ZK →
**172 ZK** w obu wariantach. To przywraca mniej więcej poziom sprzed korekty ×4/7.

**Kalkulator Robót** liczy po `id` z cennika, więc sam się przeliczy.

**Majętny i Status** — bez zmian. Zarobki są Twoją kotwicą i żaden wariant ich nie rusza.

---

## 8. Założenia i niepewność

- **Czasy pracy w teście rzemieślnika to szacunki rzędu wielkości.** Granice przedziałów dla narzędzi,
  odzieży, wozów, ksiąg i pancerza zależą od nich. Wniosek „×3 to za dużo dla prostych wyrobów" jest
  odporny (ślepe ×3 przekracza normę 1,5–2 razy), ale dokładne liczby typu „maks. ×1,55" — nie.
- **Sukno szare, płótno zgrzebne, olej do lampy** — moje szacunki, oznaczone w cenniku jako takie.
- **Zawartość złota w ZK** wyprowadzona z kursu (złoty polski 3,5 g = 2,29 ZK → 1 ZK ≈ 1,5 g).
  WFRP nie podaje wagi monety.
- **Ćwiertnia ~120 l** — założenie robocze, rozdz. 5.

---

## 9. Do Twojej decyzji

1. **Który wariant.** `drogi` jeśli chcesz, żeby było jak najbliżej Twojego ×3; `zalecany` jeśli chcesz
   zostać bliżej źródeł (kolczuga trafia wtedy dokładnie w 20 ZK z nowego wydania).
   Pliki: `propozycja/cennik_v4_drogi.json`, `propozycja/cennik_v4_zalecany.json`,
   czynsze `propozycja/czynsze_v4.json`, koniunktura `propozycja/koniunktura_v4.json`.
2. **Własne mnożniki.** Zmień liczby w `propozycja/klasy_cenowe_v4.json → presety`, potem
   `node --test` z odpowiednim `CENNIK`. Trzymaj się przedziałów z rozdz. 3 — test powie, jeśli nie.
3. **Konie.** Jedyna klasa, gdzie ×3 nie łamie żadnej reguły wewnętrznej, a tylko punkt odniesienia
   z historii (rumak 4,6 roku brutto rycerza). Jeśli chcesz, żeby rycerstwo było praktycznie
   niedostępne poza dziedziczeniem — ×3 jest uczciwą decyzją.

---

## Źródła

- [K. Boroda, *Pojemność miar nasypnych w XVI-wiecznej Polsce*](https://repozytorium.uwb.edu.pl/jspui/bitstream/11320/16905/1/K_Boroda_Pojemnosc_miar_nasypnych.pdf) — korzec krakowski 36–60 l, ćwiertnia
- [Ceny i zarobki w Krakowie w XVI wieku — historia.org.pl](https://historia.org.pl/2025/08/09/ile-kosztowalo-zycie-w-zlotym-wieku-w-krakowie-ceny-i-zarobki-w-xvi-wieku/)
- [Medieval price list — UC Davis](https://medieval.ucdavis.edu/120D/Money.html) — inwentarze, zbroje, płace Dyera
- [Preise im Mittelalter — Wikipedia (DE)](https://de.wikipedia.org/wiki/Preise_im_Mittelalter) — Frankfurt 1450, Kolonia 1390
