# Analiza v6 — balans cen wobec zarobków (2026-10-24)

Pytanie MG: czy rzeczy mają sens? Chłopa ma być stać na przeżycie, ale nie na pistolet. Wóz wieś kupi,
ale po namyśle. Tabela z `narzedzia/balans_v6.py` (CSV: `docs/analiza_v6/balans.csv`).

## 1. Jak czytać

- **Robota** = netto za tydzień pracy ponad normę (rzut na Dochód). Tyle postać realnie odkłada.
- Liczba w tabeli = **ile Robót trzeba odłożyć**. „<1” = stać od ręki.
- Brąz 3 = robotnik, chłop małorolny (netto 33 p, brutto 165 p). Brąz 5 = kmieć, czeladnik. Srebro 1 = mistrz.

| Rzecz | Cena | Brąz 1 | Brąz 2 | Brąz 3 | Brąz 5 | Srebro 1 | Srebro 3 | Srebro 5 | Złoto 1 | Złoto 3 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| chleb na tydzień (2 bochenki/dzień) | 2 s 4 p | 3 | 1 | <1 | <1 | <1 | <1 | <1 | <1 | <1 |
| jedzenie na zimno, tydzień | 5 s 10 p | 6 | 3 | 2 | 1 | 1 | <1 | <1 | <1 | <1 |
| kąt w izbie czeladnej, tydzień | 2 s | 2 | 1 | <1 | <1 | <1 | <1 | <1 | <1 | <1 |
| Ubranie | 2 ZK 2 s | 46 | 23 | 15 | 9 | 8 | 3 | 2 | <1 | <1 |
| Buty | 18 s | 20 | 10 | 7 | 4 | 3 | 1 | <1 | <1 | <1 |
| Koc | 1 ZK 4 s | 26 | 13 | 9 | 5 | 4 | 1 | <1 | <1 | <1 |
| Siekiera | 4 s | 4 | 2 | 1 | <1 | <1 | <1 | <1 | <1 | <1 |
| Broń ręczna (topór, maczuga) | 1 ZK 14 s | 37 | 19 | 12 | 7 | 6 | 2 | 1 | <1 | <1 |
| Włócznia | 16 s | 17 | 9 | 6 | 3 | 3 | <1 | <1 | <1 | <1 |
| Łuk | 2 ZK | 44 | 22 | 15 | 9 | 7 | 2 | 1 | <1 | <1 |
| Miecz | 3 ZK 9 s | 75 | 38 | 25 | 15 | 13 | 4 | 3 | 1 | <1 |
| Kusza | 4 ZK | 87 | 44 | 29 | 17 | 15 | 5 | 3 | 1 | <1 |
| Rusznica lontowa | 4 ZK | 87 | 44 | 29 | 17 | 15 | 5 | 3 | 1 | <1 |
| Pistolet | 20 ZK | 400+ | 218 | 145 | 87 | 73 | 24 | 15 | 7 | 2 |
| Skórzany kaftan | 1 ZK 10 s | 33 | 16 | 11 | 7 | 5 | 2 | 1 | <1 | <1 |
| Kolczuga | 20 ZK | 400+ | 218 | 145 | 87 | 73 | 24 | 15 | 7 | 2 |
| Pełna płytówka (4 elementy) | 96 ZK | 400+ | 400+ | 400+ | 400+ | 349 | 116 | 70 | 32 | 11 |
| Mikstura lecznicza | 1 ZK 10 s | 33 | 16 | 11 | 7 | 5 | 2 | 1 | <1 | <1 |
| Narzędzia Pracy | 7 ZK 4 s | 157 | 79 | 52 | 31 | 26 | 9 | 5 | 2 | <1 |
| Krowa | 5 ZK | 109 | 55 | 36 | 22 | 18 | 6 | 4 | 2 | <1 |
| Wół | 6 ZK | 131 | 65 | 44 | 26 | 22 | 7 | 4 | 2 | <1 |
| Koń pociągowy | 15 ZK | 327 | 164 | 109 | 65 | 55 | 18 | 11 | 5 | 2 |
| Furmanka | 6 ZK | 131 | 65 | 44 | 26 | 22 | 7 | 4 | 2 | <1 |
| Wóz | 18 ZK | 393 | 196 | 131 | 79 | 65 | 22 | 13 | 6 | 2 |
| Koń wierzchowy | 38 ZK | 400+ | 400+ | 276 | 166 | 138 | 46 | 28 | 13 | 4 |
| Lekki koń bojowy | 262 ZK 10 s | 400+ | 400+ | 400+ | 400+ | 400+ | 318 | 191 | 88 | 29 |
| Rumak | 825 ZK | 400+ | 400+ | 400+ | 400+ | 400+ | 400+ | 400+ | 275 | 92 |
| Kupno: prosty dom | 120 ZK | 400+ | 400+ | 400+ | 400+ | 400+ | 145 | 87 | 40 | 13 |

## 2. Co się zgadza z założeniami MG

1. **Przeżycie.** Utrzymanie Brązu 3 to 132 p tygodniowo (80% brutto). Kąt w izbie i chleb to 52 p.
   Jedzenie na zimno z kątem to 94 p. Robotnika stać na dach i jedzenie, zostaje mu na ubranie i podatki.
   Brąz 2 (88 p) wiąże koniec z końcem na chlebie. Brąz 1 (44 p) nie opłaci kąta i chleba (52 p): „zimą głoduje”.
2. **Pistolet.** Chłop (Brąz 3) odkładałby 145 Robót, czyli lata. Mistrz (Srebro 1): 73 Roboty. Kupiec dalekomorski
   (Srebro 5): 15. Szlachcic (Złoto 1): 7. Pistolet jest bronią bogatych.
3. **Wóz.** Wieś 25 gospodarstw Brązu 3 ma razem 825 p nadwyżki tygodniowo. Wóz to 5 tygodni całej nadwyżki,
   wóz z koniem pociągowym prawie 10. Wieś go kupi, ale po zebraniu i z oszczędności. Kmieć (Brąz 5) sam na furmankę
   odkłada pół roku (26 Robót).
4. **Broń chłopa.** Siekiera, włócznia, łuk i proca są w zasięgu (1–7 Robót). Topór bojowy 12 Robót, miecz 25.
   Miecz pozostaje znakiem stanu.
5. **Zbroja.** Kolczuga to 3–4 tygodnie brutto doświadczonego najemnika (Srebro 5). Płytówka dopiero od Złota 1.
6. **Konie.** Rumak kosztuje rycerza (Złoto 2) ok. 27 tygodni brutto, barona (Złoto 3) 92 Roboty. Zgodne z decyzją MG.

## 3. Luki i rozjazdy — do decyzji MG

| # | Co | Dlaczego to problem | Propozycja |
|---|---|---|---|
| 1 | **Koc 1 ZK 4 s droższy niż łuk (19 s) i włócznia (16 s)** | Koc podniesiono w v4, żeby nie był tańszy od sukna. Przy stole wygląda dziwnie: chłop kupi łuk taniej niż koc. | Albo zostawić (sukno było drogie, łuk wiejski tani — historycznie prawda), albo obniżyć koc do ok. 12 s z sukna szarego zamiast importowanego. |
| 2 | **Łuk ¼ ceny RAW, kusza 1,4× RAW** (rozstrzygnięte, 3.1 pkt 4) | Kusza była 7× droższa od łuku; w RAW tylko 1,25×. | Łuk 2 ZK, kusza 4 ZK. |
| 3 | **Wieś nie ma wozu** | Limit wsi 2 ZK, a furmanka (6 ZK) i wóz nie są w wyjątkach (wyjątki: żywy inwentarz i żywność). Nikt nie robi pojazdów na zamówienie. Wieś musi jechać do miasteczka. | Dodać pojazdy chłopskie (furmanka, wóz) do wyjątków wsi albo dać kowalowi „robotę” na wozy (kołodziej). |
| 4 | **Generator nie daje towaru z Zaletami ani Wadami** | „Mistrz cechu, wyroby przednie” sprzedaje to samo co rzemieślnik, tylko drożej. Paser i domokrążca nie mają towaru Tandetnego. | Szansa na Zalety u mistrza cechu i płatnerza, na Wady u pasera i domokrążcy. Dziś MG ustawia jakość ręcznie w karcie kupca. |
| 5 | **Lekki koń bojowy: Dostępność Powszechna** | Rumak jest Ograniczony, a lżejszy koń bojowy Powszechny przy cenie 262 ZK. | Ograniczona. |
| 6 | **Najęty mistrz rzemiosła 2 ZK 15 s tygodniowo** | To 2× brutto mistrza z warsztatem (Srebro 1). Najemnik (Srebro 2–5) jest zgodny z płacą. | Zostawić (najmowany bierze więcej niż zarabia u siebie) albo zrównać ze Srebrem 2. |
| 7 | **Ubranie 15 Robót chłopa** | Pełny strój to 3 tygodnie brutto robotnika. Historycznie zgodne, ale gracze z Brązu nie odnowią stroju. | Zostawić — to dobry powód, żeby łachmany były łachmanami. |

### 3.1 Decyzje MG (2026-10-24)

1. Koc — zostaje (sukno było drogie, wiejski łuk tani).
2. Wóz — robi kowal albo nowy **Kołodziej / cieśla wiejski** (`kupcy.json → robota_pozycje`: furmanka, wóz).
   Wieś składa się na wóz i daje materiał: opcja „materiał zamawiającego” w zamówieniu, płaci się
   `rynek.zamowienie.material_wlasny` = 50% ceny (szacunek do korekty). Wóz we wsi u kołodzieja: 17 ZK 4 s 3 p,
   z materiałem wsi 8 ZK 12 s 2 p, robota 7 tygodni. Furmanka: 5 ZK 14 s 9 p, z materiałem 2 ZK 17 s 5 p.
3. Jakość w sklepach — losowana wg kupca (`kupcy.json → jakosc`): mistrz cechu 35% pozycji z Zaletami, płatnerz 25%,
   bławatny 20%; paser 30% z Wadami, domokrążca 35%, kramarz i kwatermistrz 15%. Szacunki do korekty.
4. Łuki i kusze (2026-10-25): porządny łuk 2 ZK, kusza 4 ZK; rodziny w tych samych proporcjach — krótki łuk
   1 ZK 14 s, łuk długi 2 ZK 15 s, łuk elfi 13 ZK 15 s (5× długi), ciężka kusza 6 ZK, kusza pistoletowa 5 ZK 16 s.
   Łuk „z kija z lasu” to łuk z Wadami przedmiotu (np. Tandetny i Brzydki: 10 s). Test rzemieślnika dla łuku długiego:
   materiał 80 p (dobry cis) i 3 dni pracy zamiast 40 p i 2 dni.
5. Lekki koń bojowy, najęty mistrz, ubranie — bez zmian.

## 4. Zmiany v6 bez wpływu na ceny

- Jakość egzemplarza: cena z cennika to wariant podstawowy. Cechy broni (Szybka, Precyzyjna…) są w niej wliczone.
  Każda Zaleta przedmiotu ×2 (każdy poziom Wyśmienity i Wytrzymały osobno), każda Wada ×½ (PG s. 292).
  Miecz z Wytrzymały 2 i Wyśmienity 2 kosztuje ×16.
- Upływ czasu u kupców: sprzedaż 5/12/25% sztuk tygodniowo zależnie od popytu, dokupienie za koszt nabycia,
  zysk ponad 2× gotówkę startową kupiec odkłada. W symulacji 12 tygodni u 15 kupców gotówka i towar wahają się
  wokół startu. W czasie wojny kupcy broni zarabiają dużo — tak ma być.
