# Skarbiec Imperium — dane do Kompendium MG

Wygenerowano 2026-10-30 z repozytorium (narzedzia/eksport_kompendium.mjs). Cennik: v5-zalecany+ustawienia.
Wszystkie ceny to ceny **bazowe (wytwórcy)**; gracz płaci u kupca więcej (marża, osada, sytuacja). 1 ZK = 20 s = 240 p.

## 1. Status i zarobki

Kotwica: robotnik niewykwalifikowany (Brąz 3) — 13 s 9 p brutto tygodniowo, dniówka 27,5 p.
Netto = rzut za jedną Robotę (tydzień pracy ponad normę). Brutto = 5 × netto; 80% brutto to utrzymanie w osadzie.
Majętny: +1k5 monet szczebla za poziom Talentu (do rzutu, czyli do netto).

| Status | Rzut | Netto / Robotę | Brutto / tydz. | Brutto / rok | Kto |
|---|---|---|---|---|---|
| Brąz 0 | brak | — | — | — | Żebrak, pokutnik, kaleka. Dochód wyłącznie z jałmużny. |
| Brąz 1 | 2k10 pensów | 11 p | 4 s 7 p | 11 ZK 18 s 4 p | Nędzarz z pracą dorywczą. Zimą głoduje. |
| Brąz 2 | 4k10 pensów | 1 s 10 p | 9 s 2 p | 23 ZK 16 s 8 p | Parobek, wyrobnik, komornik, sługa bez ziemi. |
| Brąz 3 | 6k10 pensów | 2 s 9 p | 13 s 9 p | 35 ZK 15 s | JEDNOSTKA ODNIESIENIA: robotnik niewykwalifikowany, chłop małorolny. Kraków 1526–35: 1,5 gr dziennie, 9 gr tygodniowo, 13,5 zł rocznie. |
| Brąz 4 | 8k10 pensów | 3 s 8 p | 18 s 4 p | 47 ZK 13 s 4 p | Robotnik wykwalifikowany, młodszy czeladnik. |
| Brąz 5 | 10k10 pensów | 4 s 7 p | 1 ZK 2 s 11 p | 59 ZK 11 s 8 p | Czeladnik cechowy (Kraków: 2,5 gr dziennie = 15 gr tygodniowo), kmieć z pełnym łanem, wolny gwarek. |
| Srebro 1 | 1k10 szylingów | 5 s 6 p | 1 ZK 7 s 6 p | 71 ZK 10 s | Mistrz rzemieślnik z własnym warsztatem, drobny kupiec. Dwa razy tyle, co robotnik. |
| Srebro 2 | 2k10 szylingów | 11 s | 2 ZK 15 s | 143 ZK | Zamożny mistrz cechowy, niższy urzędnik miejski, lancknecht (4 guldeny reńskie miesięcznie). |
| Srebro 3 | 3k10 szylingów | 16 s 6 p | 4 ZK 2 s 6 p | 214 ZK 10 s | Mistrz z kilkoma czeladnikami, przedsiębiorca budowlany (Kraków: murarz 60 gr/tydzień), trębacz miejski. |
| Srebro 4 | 4k10 szylingów | 1 ZK 2 s | 5 ZK 10 s | 286 ZK | Kupiec hurtowy, notariusz, oficer najemny. |
| Srebro 5 | 5k10 szylingów | 1 ZK 7 s 6 p | 6 ZK 17 s 6 p | 357 ZK 10 s | Kupiec dalekomorski, lekarz miejski, Doppelsöldner (8 guldenów miesięcznie). Ok. 156 florenów rocznie – więcej niż golibroda królewski (100 fl.). |
| Złoto 1 | 1k5 ZK | 3 ZK | 15 ZK | 780 ZK | Patrycjusz, kanonik, profesor, drobna szlachta. Ok. 340 florenów rocznie brutto – poziom doktora teologii w Krakowie (400 fl.). |
| Złoto 2 | 2k5 ZK | 6 ZK | 30 ZK | 1560 ZK | Wielki kupiec, rycerz z lennem, arcykapłan, arcymag Kolegium. |
| Złoto 3 | 3k5 ZK | 9 ZK | 45 ZK | 2340 ZK | Baron, wysoki urzędnik prowincji, Lektor, lekarz nadworny (700 fl./rok). Ok. 1000 florenów – tyle, co marszałek nadworny. |
| Złoto 4 | 4k5 ZK | 12 ZK | 60 ZK | 3120 ZK | Hrabia, arcybiskup, patrycjat kupiecki formatu Fuggerów, mistrz szpiegów. |
| Złoto 5 | 5k5 ZK | 15 ZK | 75 ZK | 3900 ZK | Wielki magnat, Patriarcha bogatego Kolegium, gubernator prowincji, Najwyższy Lektor. |
| Złoto 6 | 6k5 ZK | 18 ZK | 90 ZK | 4680 ZK | Książę prowincji, wielki ród arystokratyczny. |
| Złoto 7 | 7k5 ZK | 21 ZK | 105 ZK | 5460 ZK | Arystokrata najwyższego rzędu: elektor, wielki książę. Dochód to przybliżenie po wydatkach stanu — utrzymanie dworu, świty i pozycji pochłania większość przychodu. Do tego poziomy Talentu Majętny (+1k5 ZK za poziom); figury państwowe ×10 (zasady). |

## 2. Cena u kupca

Cena u kupca = cena bazowa × marża × (preferencja × kaprys) × osada × sytuacja × pora roku × wahania × strefa handlowa × zapas/popyt × cecha kupca.
Cena minimalna = koszt nabycia × 1,05 (wyprzedaż: × 0,9); koszt nabycia = cena bazowa × osada × sytuacja (wytwórca × 0,8).
Preferencja: rdzeń ×0,95, boczny ×1,1. Kaprys 1k10: ≤1 ×0,9, ≤3 ×0,95, ≤7 ×1, ≤9 ×1,05, ≤10 ×1,1; razem w granicach ×0,85–×1,2.

### Kupcy

| Kupiec | Status | Marża | Skup | Limit towaru | Rdzeń | Boczne | Robi sam | Zalety / Wady | Trefne |
|---|---|---|---|---|---|---|---|---|---|
| Domokrążca | Brąz 4 | +15% | 45% | 3 ZK | Wyposażenie różne, Amunicja | Narzędzia i zestawy, Zioła, mikstury, narkotyki, Ubranie i dodatki, Jedzenie, picie, nocleg | — | 0% / 35% | 12% |
| Kramarz na targu | Srebro 1 | +5% | 40% | 6 ZK | Jedzenie, picie, nocleg, Wyposażenie różne | Ubranie i dodatki, Narzędzia i zestawy | — | 0% / 15% | 6% |
| Kowal wiejski | Brąz 5 | -10% | 35% | 8 ZK | Narzędzia i zestawy | Broń biała, Amunicja | Narzędzia i zestawy, Broń biała, furmanka, woz | 5% / 10% | 4% |
| Rzemieślnik cechowy | Srebro 3 | -5% | 45% | 25 ZK | Narzędzia i zestawy, Wyposażenie różne | Broń biała, Ubranie i dodatki | Narzędzia i zestawy, Wyposażenie różne, Broń biała | 10% / 5% | 4% |
| Mistrz cechu, wyroby przednie | Złoto 1 | +40% | 40% | 250 ZK | Narzędzia i zestawy, Wyposażenie różne, Ubranie i dodatki | Broń biała, Księgi i dokumenty | Narzędzia i zestawy, Wyposażenie różne, Ubranie i dodatki, Broń biała | 35% / 0% | 1% |
| Zbrojmistrz | Srebro 4 | +10% | 45% | 80 ZK | Broń biała, Broń zasięgowa, Amunicja | Pancerze, Wyposażenie różne | Broń biała, Amunicja | 10% / 5% | 4% |
| Płatnerz mistrzowski | Złoto 1 | +45% | 40% | 500 ZK | Pancerze | Broń biała | Pancerze, Broń biała | 25% / 0% | 2% |
| Rusznikarz z Nuln | Srebro 5 | +30% | 45% | 150 ZK | Broń zasięgowa, Amunicja | Narzędzia i zestawy, Wyposażenie różne | Broń zasięgowa, Amunicja | 10% / 5% | 4% |
| Aptekarz | Srebro 3 | +15% | 40% | 60 ZK | Zioła, mikstury, narkotyki | Księgi i dokumenty, Wyposażenie różne, Narzędzia i zestawy | Zioła, mikstury, narkotyki | — | 4% |
| Handlarz koni | Srebro 4 | +25% | 50% | 700 ZK | Zwierzęta i pojazdy | Narzędzia i zestawy | — | — | 4% |
| Kupiec bławatny | Srebro 5 | +30% | 40% | 400 ZK | Ubranie i dodatki | Wyposażenie różne, Protezy | Ubranie i dodatki | 20% / 0% | 4% |
| Księgarz i drukarz | Srebro 3 | +15% | 35% | 100 ZK | Księgi i dokumenty | Narzędzia i zestawy, Wyposażenie różne | Księgi i dokumenty | — | 3% |
| Paser | Srebro 2 | -35% | 30% | 150 ZK | Broń biała, Ubranie i dodatki, Wyposażenie różne | Pancerze, Księgi i dokumenty, Narzędzia i zestawy, Broń zasięgowa, Protezy | — | 5% / 30% | 75% |
| Kwatermistrz wojskowy | Srebro 4 | -15% | 50% | 120 ZK | Broń biała, Pancerze, Amunicja, Broń zasięgowa | Jedzenie, picie, nocleg, Wyposażenie różne, Zioła, mikstury, narkotyki | — | 5% / 15% | 8% |
| Medyk i balwierz | Srebro 3 | +20% | 35% | 80 ZK | Zioła, mikstury, narkotyki, Protezy | Narzędzia i zestawy, Księgi i dokumenty | Protezy | — | 4% |
| Kołodziej / cieśla wiejski | Brąz 5 | -10% | 35% | 8 ZK | Narzędzia i zestawy | Wyposażenie różne | Narzędzia i zestawy, furmanka, woz | 5% / 10% | 4% |
| Krasnoludzki kupiec (Dawi) | Srebro 3 | +20% | 40% | 150 ZK | Broń biała, Narzędzia i zestawy | Pancerze, Broń zasięgowa, Jedzenie, picie, nocleg, Amunicja | Broń biała, Narzędzia i zestawy, Pancerze | 30% / 0% | 1% |

### Osady

| Osada | Mnożnik | Limit towaru | Dostępność jak | Uwagi |
|---|---|---|---|---|
| Wieś | -15% | 2 ZK | wioska | Limit 2 ZK i wymóg Dostępności Powszechnej nie dotyczą żywego inwentarza ani podstawowej żywności — wieś jest właśnie tym miejscem, gdzie kupuje się krowę. |
| Miasteczko | 0% | 15 ZK | miasteczko |  |
| Miasto | +10% | 60 ZK | miasto |  |
| Metropolia (Nuln, Middenheim) | +20% | bez limitu | metropolia |  |
| Altdorf | +30% | bez limitu | metropolia | Rzadkie o stopień łatwiej (szansa jak Ograniczonej). |
| Marienburg | +45% | bez limitu | metropolia | Wszystko z importu: Rzadkie o stopień łatwiej, Egzotyczne częściej niż w innych metropoliach. |

### Ośrodki handlu (Poradnik Staroświatowca, tab. 3-2)

| Miasto | Strefa | Populacja | Zamożność | Typ | Mnożnik | Specjalności |
|---|---|---|---|---|---|---|
| Carroburg | Dorzecze Reiklandzkie | 12000 | 4 | miasto | +16% |  |
| Bögenhafen | Dorzecze Reiklandzkie | 5000 | 3 | miasteczko | 0% |  |
| Helmgart | Dorzecze Reiklandzkie | 2200 | 2 | miasteczko | -5% |  |
| Ubersreik | Dorzecze Reiklandzkie | 3500 | 4 | miasteczko | +5% |  |
| Weissbruck | Dorzecze Reiklandzkie | 272 | 2 | wies | -19% |  |
| Kemperbad | Enklawa Kemperbadu | 7500 | 4 | miasteczko | +5% |  |
| Auerswald | Enklawa Kemperbadu | 5000 | 3 | miasteczko | 0% |  |
| Grunburg | Enklawa Kemperbadu | 2400 | 2 | miasteczko | -5% |  |
| Stimmigen | Enklawa Kemperbadu | 1750 | 3 | miasteczko | 0% |  |
| Nuln | Strefa Handlowa Nuln | 85000 | 5 | metropolia | +32% | prochowa ×0,85, eksperymentalna ×0,85, warsztatowe ×0,92 |
| Ambosstein | Strefa Handlowa Nuln | 80 | 3 | wies | -15% |  |
| Furtzhausen | Strefa Handlowa Nuln | 74 | 3 | wies | -15% |  |
| Kotzenheim | Strefa Handlowa Nuln | 61 | 3 | wies | -15% |  |
| Wissenburg | Strefa Handlowa Nuln | 9000 | 4 | miasteczko | +5% |  |
| Pfeildorf | Dolina Górnego Solu | 6800 | 3 | miasteczko | 0% |  |
| Geschburg | Dolina Górnego Solu | 600 | 3 | wies | -15% |  |
| Kreutzhofen | Dolina Górnego Solu | 515 | 4 | wies | -11% |  |
| Kroppenleben | Dolina Górnego Solu | 85 | 3 | wies | -15% |  |
| Wuppertal | Dolina Górnego Solu | 1100 | 3 | miasteczko | 0% |  |
| Wusterburg | Dolina Górnego Solu | 800 | 3 | wies | -15% |  |
| Averheim | Stary Trakt Krasnoludzki | 9400 | 4 | miasteczko | +5% |  |
| Wurtbad | Stary Trakt Krasnoludzki | 8800 | 4 | miasteczko | +5% |  |
| Gersdorf | Stary Trakt Krasnoludzki | 425 | 3 | wies | -15% |  |
| Hocheleben | Stary Trakt Krasnoludzki | 375 | 3 | wies | -15% |  |
| Krugenheim | Stary Trakt Krasnoludzki | 4500 | 4 | miasteczko | +5% |  |
| Pfungzig | Stary Trakt Krasnoludzki | 3580 | 3 | miasteczko | 0% |  |
| Streissen | Stary Trakt Krasnoludzki | 5500 | 3 | miasteczko | 0% |  |
| Eicheschatten | Trakt do Zhufbaru | 3375 | 3 | miasteczko | 0% |  |
| Schramleben | Trakt do Zhufbaru | 675 | 3 | wies | -15% |  |
| Waldenhof | Trakt do Zhufbaru | 4200 | 2 | miasteczko | -5% |  |
| Talabheim | Stara Droga Leśna | 72000 | 4 | metropolia | +26% |  |
| Ahlenhof | Stara Droga Leśna | 4200 | 3 | miasteczko | 0% |  |
| Hergig | Stara Droga Leśna | 500 | 3 | wies | -15% |  |
| Küsel | Stara Droga Leśna | 6500 | 4 | miasteczko | +5% |  |
| Talagaad | Stara Droga Leśna | 450 | 3 | wies | -15% |  |
| Bechafen | Przejście Północno-Wschodnie | 7600 | 4 | miasteczko | +5% |  |
| Wolfenburg | Przejście Północno-Wschodnie | 1100 | 3 | miasteczko | 0% |  |
| Wurzen | Przejście Północno-Wschodnie | 1450 | 2 | miasteczko | -5% |  |
| Salzenmund | Wybrzeże Salzenmund | 7500 | 4 | miasteczko | +5% |  |
| Ferlangen | Wybrzeże Salzenmund | 130 | 3 | wies | -15% |  |
| Grafenrich | Wybrzeże Salzenmund | 252 | 2 | wies | -19% |  |
| Neue Emskrank | Wybrzeże Salzenmund | 895 | 3 | wies | -15% |  |
| Norden | Wybrzeże Salzenmund | 3200 | 3 | miasteczko | 0% |  |
| Middenheim | Korytarz Drakwaldzki | 15000 | 5 | metropolia | +32% | futra ×0,8, warsztatowe ×0,9, prosta ×0,92, wojskowa ×0,92, tarcze ×0,92 |
| Beeckerhoven | Korytarz Drakwaldzki | 408 | 3 | wies | -15% |  |
| Delberz | Korytarz Drakwaldzki | 4500 | 3 | miasteczko | 0% |  |
| Schoninghagen | Korytarz Drakwaldzki | 980 | 3 | wies | -15% |  |
| Scheinfeld | Delta Marienburga | 850 | 3 | wies | -15% |  |
| Schilderheim | Delta Marienburga | 5500 | 3 | miasteczko | 0% |  |

### Dostępność (PG s. 290 + zasady kampanii)

| Dostępność | wioska | miasteczko | miasto | metropolia |
|---|---|---|---|---|
| Powszechna | 100% | 100% | 100% | 100% |
| Ograniczona | 30% | 60% | 90% | 90% |
| Rzadka | 15% | 30% | 45% | 45% |
| Egzotyczna | 0,1% | 0,1% | 0,1% | 3% |

Altdorf i Marienburg: Rzadkie jak Ograniczone. Marienburg (import): Egzotyczne 6%. Towar krasnoludzki / elfi u kupca innej rasy: × 0,3.

### Sytuacje

| Sytuacja | Ceny | Popyt | Czynsz |
|---|---|---|---|
| Normalna | (ceny bez zmian) | bez zmian | 0% |
| Nadmiar towaru po jarmarku | (wszystko -20%) | popyt o stopień niżej | 0% |
| Niedobór na rynku | (wszystko +40% · czynsz +10%) | popyt o stopień wyżej | +10% |
| Wojna | (Broń biała, Broń zasięgowa, Amunicja, Pancerze +80% · Jedzenie, picie, nocleg +30% · reszta +5% · czynsz +30%) | broń i pancerz +1 | +30% |
| Zaraza | (Zioła, mikstury, narkotyki, Protezy +150% · Jedzenie, picie, nocleg +60% · reszta -15% · czynsz -40%) | leki i prowiant +1, reszta −1 | -40% |
| Oblężenie | (Jedzenie, picie, nocleg +250% · Broń biała, Broń zasięgowa, Amunicja, Pancerze +40% · reszta -30% · czynsz +100%) | prowiant +1, broń 0, reszta −1 | +100% |
| Zamknięte szlaki (bandyci, lód) | (Ubranie i dodatki, Księgi i dokumenty, Zioła, mikstury, narkotyki +60% · reszta +5% · czynsz +10%) | ubranie i księgi +1 | +10% |
| Kryzys mieszkaniowy | (ceny bez zmian · czynsz +70%) |  | +70% |
| Napływ ludzi (pielgrzymi, uchodźcy, święto) | (Jedzenie, picie, nocleg +25% · Ubranie i dodatki, Wyposażenie różne +10% · reszta +5% · czynsz +40%) | jedzenie, ubranie, wyposażenie +1 | +40% |
| Braki w dostawach (zła droga, cło, zima) | (Jedzenie, picie, nocleg +30% · Narzędzia i zestawy, Zioła, mikstury, narkotyki +20% · reszta +10%) | jedzenie +1 | 0% |
| Kryzys (podatki, bankructwa, zła moneta) | (Jedzenie, picie, nocleg +10% · Ubranie i dodatki, Księgi i dokumenty -15% · reszta -5% · czynsz -10%) | popyt o stopień niżej, jedzenie bez zmian | -10% |
| Dobry sezon (urodzaj, spokój na szlakach) | (Zwierzęta i pojazdy -10% · Jedzenie, picie, nocleg -20% · reszta -5% · czynsz +5%) | ubranie, wyposażenie, księgi +1 — ludzie mają pieniądze | +5% |

### Pora roku i wahania rynku

| Pora | Ceny | Kategorie | Zagrożenia w podróży |
|---|---|---|---|
| Wiosna | ×1 | Jedzenie, picie, nocleg ×1,1 | +10 |
| Lato | ×0,95 | Jedzenie, picie, nocleg ×0,95 | +0 |
| Jesień | ×1 | Jedzenie, picie, nocleg ×0,85; Zwierzęta i pojazdy ×0,9 | +10 |
| Zima | ×1,05 | Jedzenie, picie, nocleg ×1,2, popyt +1; Ubranie i dodatki ×1,1, popyt +1 | +20 |

| 1k10 | Rynek | Ceny | Popyt | Dostępność |
|---|---|---|---|---|
| 3–8 | Rynek stabilny | ×1 | 0 | ×1 |
| 1–2 | Rynek Byka (hossa) | ×1,1 | 1 | ×0,7 |
| 9–10 | Rynek Niedźwiedzia (bessa) | ×0,9 | -1 | ×1,3 |

### Zapas × popyt

| Zapas \ popyt | niski popyt | normalny popyt | wysoki popyt |
|---|---|---|---|
| pełen skład (1k10 ≤ 2) | -35% | -20% | -5% |
| normalny zapas (1k10 ≤ 7) | -15% | 0% | +20% |
| ostatnie sztuki (1k10 ≤ 9) | -25% | +5% | +50% |
| brak — na zamówienie (1k10 ≤ 10) | +5% | +25% | +70% |

### Targowanie, skup

Przeciwstawny Test Targowania: każdy PS −4%, najwyżej −24% (zamówienia −16%). Talenty (Żyłka Handlowa) dodają upust ponad limit. Nigdy poniżej ceny minimalnej kupca.
Skup: odsetek ceny kupca z tabeli kupców; wysoki popyt +15 pkt, niski -15 pkt, minimum 20%.

## 3. Jakość przedmiotu

Cena w cenniku = wariant podstawowy. Każda Zaleta przedmiotu ×1,6, każda Wada ×0,6 (Wyśmienity i Wytrzymały — każdy poziom osobno).

| Cecha | Rodzaj | Efekt |
|---|---|---|
| Poręczny | Zaleta | Obciążenie −1. |
| Praktyczny | Zaleta | Nieudany Test z tym przedmiotem +1 PS; kary za noszenie pancerza o poziom niżej. |
| Wyśmienity | Zaleta (wielokrotna) | Oznaka pozycji społecznej; im wyższy poziom, tym bardziej imponuje. |
| Wytrzymały | Zaleta (wielokrotna) | +1 Punkt Uszkodzeń na poziom; rzut obronny przeciw złamaniu 9+, łatwiejszy o 1 na poziom. |
| Brzydki | Wada | Testy Ogłady nawet −10. |
| Nieporęczny | Wada | Obciążenie +1; w zbroi kary za Zmęczenie podwojone. |
| Tandetny | Wada | Łamie się przy nieudanym Teście z dublem; pancerz pęka od Trafienia Krytycznego. |
| Zawodny | Wada | Nieudany Test −1 PS; kary za noszenie pancerza podwojone. |

| Wykonanie | Mnożnik | Pełna płytówka |
|---|---|---|
| Tandetna i Brzydka (2 Wady) | ×0,36 | 34 ZK 11 s 2 p |
| Tandetna albo Brzydka (1 Wada) | ×0,6 | 57 ZK 12 s |
| Zwykła | ×1 | 96 ZK |
| Wyśmienita (1 Zaleta) | ×1,6 | 153 ZK 12 s |
| Mistrzowska (2 Zalety) | ×2,56 | 245 ZK 15 s 2 p |

## 4. Zamówienia

Narzut za własną robotę ×1,25, za sprowadzenie ×1,45. Zaliczka 50%. Materiał zamawiającego: płaci 50% ceny.
Termin: < 1 ZK: 1k5 dni; < 10 ZK: 1k3 tygodni; < 50 ZK: 4 + 1k6 tygodni; więcej: 3 + 1k4 miesięcy. Tydzień = 8 dni.
Rzadkość tutaj (szansa w sklepie < 50%): Ograniczona +2 tyg., ×1,1; Rzadka +4 tyg., ×1,25; Egzotyczna +8 tyg., ×1,5. We wsi nikt nie sprowadzi rzeczy egzotycznej — trzeba jechać do miasta.

## 5. Towar trefny

v6c: szansa na pozycję z kupcy.json → trefne (domyślnie domyslna_szansa); cecha kupiecka może ją podnieść (Szarlatan, Powiązania przestępcze) albo wyzerować (Skrupulatnie uczciwy). wartosc = prawdziwa wartość ÷ cena, jaką kupiec podaje. swiadomosc = szansa, że kupiec wie (oszust wie zawsze). Widoczne tylko dla MG.

| Rodzaj | Prawdziwa wartość | Wykrycie | Opis |
|---|---|---|---|
| Kradziony | 100% | Wycena tego nie wykaże. Rozpoznanie: Intuicja, Wiedza (lokalna) albo świadek. | Towar z kradzieży albo niewiadomego pochodzenia. Wart tyle, ile kosztuje, ale prawowity właściciel albo straż może go rozpoznać. |
| Podróbka | 20% | Trudny (−20) Test Wyceny. | Udaje coś cenniejszego: cyna zamiast srebra, farbowane sukno, fałszywa pieczęć, rozcieńczona mikstura. |
| Ukryta Wada | 60% | Wymagający (−10) Test Wyceny albo Rzemiosła. | Wygląda porządnie, ale ma Wadę przedmiotu (Tandetny albo Zawodny) — np. jeden z dziesięciu płaszczy. |
| Oszukana miara | wg skali oszustwa | Test Wyceny wg skali oszustwa. | Niepełne skrzynie, zawyżona waga, zepsute sztuki na dnie, nadmiar opakowania. |

| Oszukane | Test Wyceny |
|---|---|
| 5% towaru | Prosty (+10) |
| 10% towaru | Przeciętny (+0) |
| 20% towaru | Wymagający (−10) |
| 30% towaru | Trudny (−20) |
| 40% towaru | Bardzo trudny (−30) |

## 6. Czynsze

| Kwatera | Tydzień | Miesiąc | Rok |
|---|---|---|---|
| Kąt w izbie czeladnej | 2 s | 7 s | 3 ZK |
| Izba na poddaszu | 3 s | 8 s | 4 ZK |
| Izba w kamienicy | 8 s | 1 ZK 4 s | 12 ZK |
| Mieszkanie mieszczańskie (2–3 izby) | 12 s | 2 ZK | 20 ZK |
| Dom mistrza z warsztatem | 1 ZK 4 s | 4 ZK | 40 ZK |
| Kamienica kupiecka | 3 ZK | 11 ZK | 110 ZK |

| Kupno | Cena |
|---|---|
| Prosty dom | 120 ZK |
| Dom rzemieślnika | 320 ZK |
| Kamienica patrycjuszowska | 3600 ZK |

Nocleg i posiłek wg gospody (× osada): Podła spelunka ×0,6, Zwykła gospoda ×1, Dobra gospoda ×1,8, Wytworny zajazd ×3,5.

## 7. Klasy cenowe (preset domyślny)

| Klasa | Mnożnik | Skąd |
|---|---|---|
| utrzymanie | ×1 | Jedzenie, nocleg, usługi: ceny ze źródeł (mediana 1,02× źródła). Budżet Brązu 3 nie pozwala na więcej. |
| surowiec | ×1 | Sukno i płótno z Krakowa 1526–35. Wyżej = arbitraż (koc tańszy niż jego sukno). |
| rzezne | ×1 | Drób, owce, świnie z Krakowa. Wyżej = mięso z tuszy tańsze od żywego zwierzęcia. |
| kruszec | ×1 | Biżuteria z kruszcu. Wyżej = opłaca się przetapiać monety. |
| najem_dolny | ×1 | Kąt i poddasze. Wyżej = Brązu 3 nie stać na dach nad głową. |
| najem | ×2 | ×2 wobec Frankfurtu 1450 — wynika z Twojej karczmy 3 s/noc i Marienburga 5 ZK. Idzie w parze z kupnem. |
| kupno | ×2 | Razem z najmem (zwrot z kupna 7–25 lat). Zmieniasz jedno — zmieniaj drugie. |
| robocze | ×1 | Wół, krowa: Kraków i Anglia trafiają co do grosza (1,04× źródła). |
| konie | ×1 | Konie robocze i wierzchowe: Kraków — pociągowy 14–16 ZK, siodłowy 34–46 ZK. ×1 trafia w środek. |
| pojazd | ×1,5 | Decyzja MG: trochę drogo, ale chłop musi mieć wóz. ×1,5 — furmanka 6 ZK (8,7 tyg. Brązu 3), wóz 18 ZK. Źródła dają 2–3×. |
| codzienne | ×1,2 | Narzędzia, naczynia, koce. Źródła 1,15×, test kowala 1,15× → 1,2. Wcześniejsze 1,5 nie miało podstawy. |
| odziez | ×1,5 | Test szewca i krawca 1,4–1,8× → 1,5. |
| prestiz | ×1,5 | Zbytek. ×1,5, żeby strój dworski (45 ZK) nie był porównywalny z płytówką (96 ZK) — Twoja reguła. |
| bron | ×2 | Baza była poniżej źródeł (0,57×). ×2 daje 1,16× źródła i zbrojmistrz zarabia na swój Status. |
| palna | ×2 | Decyzja MG: broń palna ma być droga. ×2 ponad RAW i źródła (pistolet 20 ZK, rusznica 6 ZK). Proch też ×2. |
| pancerz | ×2 | ×2: kolczuga 20 ZK (nowe wydanie, Twoja kotwica), test płatnerza 2,0. Źródła angielskie dają ok. połowę. |
| ksiega | ×2 | Rękopis medyczny £5–20 = 35–140 ZK; test skryby 1,4. ×2 = środek. |
| alchemia | ×1 | Brak źródeł. Baza i tak 1,5× RAW. Chcesz, żeby leczenie bolało — podnieś suwak. |
| konie_bojowe | ×1,5 | „Królestwo za konia” — konie bojowe drogie. ×1,5: rumak 825 ZK = 2,3 roku brutto rycerza (źródła: 1–4 lata). |
| pancerz_skorzany | ×1,5 | Skórznie robi rymarz (Srebro 1–2), nie płatnerz. Jak odzież: ×1,5. Kurta 1 ZK 13 s, źródło 14–27 s. |
| alchemia_skladnik | ×1 | Zioła, korzenie, grzyby: ceny RAW. Alchemik i gracze mają je kupić bez łamania sakiewki. |
| alchemia_wyrob | ×2 | Mikstury, eliksiry, trucizny: ×2, bo wymagają aparatury. Mikstura lecznicza 1 ZK 10 s = tydzień brutto Srebra 1. |

Znak stanu (miecze, szable, rapiery…): ×1,5.

## 8. Cennik kampanii

Kolumny: cena bazowa (wytwórcy) · podręcznik (RAW) · Obciążenie · Dostępność · źródło i strona. ⚠ = nielegalny.

### Broń biała

| Przedmiot | Cena | Podręcznik | Obc. | Dostępność | Źródło |
|---|---|---|---|---|---|
| Miecz | 3 ZK | 1 ZK | 1 | Powszechna | Pod Bronią |
| Broń ręczna (topór, maczuga) | 1 ZK 14 s | 1 ZK | 1 | Powszechna | PG 294 |
| Bułat | 3 ZK | 1 ZK | 1 | Ograniczona | Pod Bronią |
| Szabla | 5 ZK 2 s | 2 ZK | 1 | Ograniczona | Pod Bronią |
| Nóż | 1 s | 8 s | 0 | Powszechna | Pod Bronią |
| Sztylet | 11 s | 16 s | 0 | Powszechna | Pod Bronią |
| Mizerykordia | 11 s | 16 s | 0 | Ograniczona | Pod Bronią |
| Kastet | 3 s | 2 s 6 p | 0 | Powszechna | PG 294 |
| Kostur | 7 p | 3 s | 2 | Powszechna | PG 294 |
| Pałka | 7 p | 4 s | 1 | Powszechna | Pod Bronią |
| Topór | 16 s | 10 s | 1 | Powszechna | Pod Bronią |
| Buzdygan | 1 ZK 2 s | 15 s | 1 | Powszechna | Pod Bronią |
| Nadziak jednoręczny | 17 s | 9 s | 1 | Ograniczona | Pod Bronią |
| Młot jednoręczny | 1 ZK 14 s | 1 ZK | 1 | Ograniczona | Pod Bronią |
| Cep bojowy | 14 s | 10 s | 1 | Powszechna | PG 294 |
| Korbacz | 1 ZK 14 s | 2 ZK | 1 | Ograniczona | PG 294 |
| Kiścień | 3 ZK 8 s | 3 ZK | 2 | Rzadka | PG 294 |
| Lewak | 1 ZK 2 s | 1 ZK | 0 | Rzadka | PG 294 |
| Łamacz mieczy | 1 ZK 6 s | 1 ZK 2 s 6 p | 1 | Ograniczona | PG 294 |
| Włócznia | 16 s | 15 s | 2 | Powszechna | PG 294 |
| Pika | 18 s | 18 s | 4 | Rzadka | PG 294 |
| Halabarda | 1 ZK 12 s | 2 ZK | 3 | Powszechna | PG 294 |
| Wielki topór | 3 ZK 8 s | 4 ZK | 3 | Powszechna | PG 294 |
| Młot bojowy | 2 ZK 6 s | 3 ZK | 3 | Powszechna | PG 294 |
| Półtorak | 12 ZK | 8 ZK | 3 | Ograniczona | PG 294 |
| Miecz dwuręczny | 17 ZK | 10 ZK | 3 | Ograniczona | PG 294 |
| Floret | 10 ZK 5 s | 5 ZK | 1 | Ograniczona | PG 294 |
| Rapier | 13 ZK 15 s | 5 ZK | 1 | Ograniczona | PG 294 |
| Szpada | 10 ZK 5 s | 4 ZK | 1 | Ograniczona | Pod Bronią |
| Młot kawaleryjski | 3 ZK 8 s | 3 ZK | 3 | Ograniczona | PG 294 |
| Kopia | 1 ZK 2 s | 1 ZK | 3 | Rzadka | PG 294 |
| Lanca | 1 ZK 2 s | 1 ZK | 2 | Ograniczona | Pod Bronią |
| Tarcza (puklerz) | 8 s | 18 s 2 p | 0 | Powszechna | Pod Bronią |
| Tarcza | 1 ZK 2 s | 2 ZK | 1 | Powszechna | Pod Bronią |
| Tarcza (duża) | 1 ZK 14 s | 3 ZK | 3 | Powszechna | Pod Bronią |
| Pawęż | 2 ZK 6 s | 3 ZK 15 s | 4 | Rzadka | Pod Bronią |
| Garota | 2 s | 1 s | 0 | Rzadka | Pod Bronią |
| Tłuk | 2 s | 1 s | 0 | Rzadka | Pod Bronią |
| Kolczasta rękawica | 3 ZK 8 s | 2 ZK | 1 | Ograniczona | Pod Bronią |
| Zamykana rękawica | 1 ZK 14 s | 1 ZK | 1 | Ograniczona | Pod Bronią |
| Obciążona sieć | 2 ZK 6 s | 1 ZK 10 s | 1 | Rzadka | Pod Bronią |
| Łapacz | 2 ZK 6 s | 2 ZK | 3 | Rzadka | Pod Bronią |
| Partyzana / glewia | 1 ZK 12 s | 2 ZK | 3 | Ograniczona | Pod Bronią |
| Sierpak | 1 ZK 2 s | 2 ZK | 3 | Ograniczona | Pod Bronią |
| Szydło | 1 ZK 12 s | 2 ZK | 2 | Ograniczona | Pod Bronią |
| Topór drzewcowy | 2 ZK 6 s | 2 ZK | 3 | Ograniczona | Pod Bronią |
| Flamberg | 51 ZK | 30 ZK | 3 | Egzotyczna | Pod Bronią |
| Nadziak dwuręczny | 1 ZK 8 s | 9 s | 3 | Powszechna | Pod Bronią |
| Krasnoludzki topór | 1 ZK 14 s | 1 ZK | 1 | Powszechna | Krasnoludy 93 |
| Krasnoludzki młot bojowy | 1 ZK 14 s | 1 ZK | 1 | Powszechna | Krasnoludy 93 |
| Wirujące ostrza śmierci | 5 ZK 13 s | 5 ZK | 2 | Rzadka | Krasnoludy 93 |
| Krasnoludzki wielki topór | 3 ZK 8 s | 4 ZK | 3 | Powszechna | Krasnoludy 93 |
| Krasnoludzki wielki młot | 3 ZK 1 s | 4 ZK | 3 | Powszechna | Krasnoludy 93 |
| Krasnoludzki kilof | 1 ZK 14 s | 1 ZK | 3 | Powszechna | Krasnoludy 93 |
| Wielki miecz Hoetha | 2280 ZK | 2000 ZK | 2 | Egzotyczna | Wysokie Elfy 31 |

### Broń zasięgowa

| Przedmiot | Cena | Podręcznik | Obc. | Dostępność | Źródło |
|---|---|---|---|---|---|
| Krótki łuk | 1 ZK 14 s | 3 ZK | 1 | Powszechna | PG 295 |
| Łuk | 2 ZK | 4 ZK | 2 | Powszechna | PG 295 |
| Łuk długi | 2 ZK 15 s | 5 ZK | 3 | Ograniczona | PG 295 |
| Łuk elfi | 13 ZK 15 s | 10 ZK | 2 | Egzotyczna | PG 295 |
| Kusza | 4 ZK | 5 ZK | 2 | Powszechna | PG 295 |
| Ciężka kusza | 6 ZK | 7 ZK | 3 | Rzadka | PG 295 |
| Kusza pistoletowa | 5 ZK 16 s | 6 ZK | 0 | Ograniczona | PG 295 |
| Rusznica | 6 ZK | 4 ZK | 2 | Ograniczona | PG 295 |
| Garłacz | 6 ZK | 2 ZK | 1 | Ograniczona | PG 295 |
| Muszkiet (kaliwer) | 14 ZK | 7 ZK | 2 | Ograniczona | Pod Bronią |
| Muszkiet hochlandzki | 200 ZK | 100 ZK | 3 | Egzotyczna | PG 295 |
| Pistolet | 20 ZK | 8 ZK | 0 | Rzadka | PG 295 |
| Pieprzniczka | 30 ZK | 12 ZK | 1 | Rzadka | Pod Bronią |
| Rusznica samopowtarzalna | 40 ZK | 10 ZK | 3 | Rzadka | PG 295 |
| Pistolet samopowtarzalny | 50 ZK | 15 ZK | 1 | Rzadka | PG 295 |
| Bomba | 6 ZK | 3 ZK | 0 | Rzadka | PG 295 |
| Ładunek zapalający | 2 ZK | 1 ZK | 0 | Ograniczona | PG 295 |
| Proca | 2 s | 1 s | 0 | Powszechna | PG 295 |
| Proca drzewcowa | 5 s | 4 s | 2 | Ograniczona | PG 295 |
| Oszczep | 14 s | 10 s 6 p | 1 | Ograniczona | PG 295 |
| Nóż do rzucania | 7 s | 18 s | 0 | Powszechna | PG 295 |
| Topór do rzucania | 16 s | 1 ZK | 1 | Powszechna | PG 295 |
| Strzałka | 2 s 6 p | 2 s | 0 | Ograniczona | PG 295 |
| Bolas | 7 s | 10 s | 0 | Rzadka | PG 295 |
| Arkan | 12 s | 6 s | 0 | Powszechna | PG 295 |
| Bicz | 9 s | 5 s | 0 | Powszechna | PG 295 |
| Arkebuz | 6 ZK | 5 ZK | 3 | Egzotyczna | Pod Bronią |
| Rusznica lontowa | 4 ZK | 2 ZK | 2 | Rzadka | Pod Bronią |
| Rusznica dwulufowa | 14 ZK | 7 ZK | 3 | Egzotyczna | Pod Bronią |
| Garłacz lontowy | 3 ZK | 1 ZK | 1 | Rzadka | Pod Bronią |
| Gryfia łapa | 50 ZK | 20 ZK | 1 | Egzotyczna | Pod Bronią |
| Halabarda pistoletowa | 30 ZK | 10 ZK | 3 | Egzotyczna | Pod Bronią |
| Topór pistoletowy | 24 ZK | 8 ZK | 1 | Egzotyczna | Pod Bronią |
| Laska pistoletowa | 40 ZK | 15 ZK | 1 | Egzotyczna | Pod Bronią |
| Moździerz ręczny | 100 ZK | 50 ZK | 3 | Egzotyczna | Pod Bronią |
| Krasnoludzka kusza | 4 ZK | 5 ZK | 2 | Powszechna | Krasnoludy 94 |
| Krasnoludzka hakownica | 7 ZK 4 s | 6 ZK | 2 | Rzadka | Krasnoludy 94 |
| Krasnoludzki pistolet | 30 ZK | 12 ZK | 0 | Rzadka | Krasnoludy 94 |
| Krasnoludzki topór do rzucania | 16 s | 1 ZK | 1 | Powszechna | Krasnoludy 94 |

### Amunicja

| Przedmiot | Cena | Podręcznik | Obc. | Dostępność | Źródło |
|---|---|---|---|---|---|
| Strzała (12) | 10 s | 5 s | 0 | Powszechna | PG 296 |
| Bełt (12) | 10 s | 5 s | 0 | Powszechna | PG 296 |
| Strzała elfia (1) | 16 s | 6 s | 0 | Egzotyczna | PG 296 |
| Śrut i proch (12) | 7 s | 3 s 3 p | 0 | Powszechna | PG 296 |
| Pocisk i proch (12) | 7 s | 3 s 3 p | 0 | Powszechna | PG 296 |
| Improwizowany śrut i proch (1) | 6 p | 3 p | 0 | Powszechna | PG 296 |
| Pocisk ołowiany (12) | 1 s | 4 p | 0 | Powszechna | PG 296 |
| Pocisk kamienny (12) | 4 p | 2 p | 0 | Powszechna | PG 296 |
| Strzała przebijająca (12) | 14 s | 8 s | 0 | Ograniczona | Pod Bronią |
| Strzała ząbkowana (12) | 14 s | 8 s | 0 | Ograniczona | Pod Bronią |
| Patron (12) | 11 s | 5 s | 0 | Ograniczona | Pod Bronią |
| Precyzyjny pocisk i proch | 10 s | 3 s | 0 | Powszechna | Pod Bronią |
| Szmelc i proch (12) | 6 s 6 p | 2 s | 0 | Powszechna | Pod Bronią |
| Duży pocisk i proch (12) | 2 ZK | 1 ZK | 0 | Ograniczona | Pod Bronią |
| Nasączony Aqshy proch (12) | 3 ZK | 1 ZK | 0 | Egzotyczna | Pod Bronią |
| Pocisk hakowy (1) | 7 ZK | 2 ZK | 1 | Ograniczona | Pod Bronią |

### Pancerze

| Przedmiot | Cena | Podręcznik | Obc. | Dostępność | Źródło |
|---|---|---|---|---|---|
| Skórzana kurta | 1 ZK 13 s | 12 s | 1 | Powszechna | PG 300 |
| Skórzany kaftan | 1 ZK 10 s | 10 s | 1 | Powszechna | PG 300 |
| Skórzane nogawice | 1 ZK 13 s | 14 s | 1 | Powszechna | PG 300 |
| Skórzany hełm | 15 s | 8 s | 0 | Powszechna | PG 300 |
| Kolet | 2 ZK 5 s | 18 s | 2 | Ograniczona | PG 300 |
| Kolczuga | 20 ZK | 3 ZK | 3 | Powszechna | PG 300 |
| Kaftan kolczy | 12 ZK | 2 ZK | 2 | Ograniczona | PG 300 |
| Nogawice kolcze | 12 ZK | 2 ZK | 3 | Ograniczona | PG 300 |
| Czepiec kolczy | 6 ZK | 1 ZK | 2 | Ograniczona | PG 300 |
| Hełm otwarty (morion) | 1 ZK 4 s | 2 ZK | 1 | Powszechna | PG 300 |
| Hełm zamknięty | 16 ZK | 3 ZK | 2 | Rzadka | PG 300 |
| Napierśnik | 28 ZK | 10 ZK | 3 | Ograniczona | PG 300 |
| Naramienniki | 24 ZK | 8 ZK | 3 | Rzadka | PG 300 |
| Nagolenniki płytowe | 28 ZK | 10 ZK | 3 | Rzadka | PG 300 |
| PEŁNA PŁYTÓWKA (4 elementy) | 96 ZK | 31 ZK | 11 | Rzadka | PG 300 |
| Półzbroja municyjna (napierśnik + morion) | 14 ZK 10 s | — | 4 | Ograniczona | kampania |
| Zbroja mistrzowska na miarę (Mediolan, Norymberga) | 380 ZK | — | 11 | Egzotyczna | kampania |
| Lekki pancerz (opcja) | 5 ZK | 2 ZK | 1 | Powszechna | PG 301 |
| Średni pancerz (opcja) | 16 ZK | 5 ZK | 5 | Ograniczona | PG 301 |
| Ciężki pancerz (opcja) | 96 ZK | 30 ZK | 6 | Rzadka | PG 301 |

### Zwierzęta i pojazdy

| Przedmiot | Cena | Podręcznik | Obc. | Dostępność | Źródło |
|---|---|---|---|---|---|
| Kurczak | 1 s 6 p | 5 p | 1 | Powszechna | PG 306 |
| Gołąb pocztowy | 5 s | 3 s | 1 | Ograniczona | PG 306 |
| Robaki (6) | 1 p | 1 p | 0 | Powszechna | PG 306 |
| Owca / baran | 18 s | — | — | — | kampania |
| Świnia | 3 ZK | — | — | — | kampania |
| Krowa | 5 ZK | — | — | — | kampania |
| Wół | 6 ZK | — | — | — | kampania |
| Pies myśliwski | 3 ZK | 2 ZK | — | Rzadka | PG 306 |
| Małpa | 15 ZK | 10 ZK | 2 | Rzadka | PG 306 |
| Muł | 12 ZK | 5 ZK | — | Powszechna | PG 306 |
| Kucyk | 10 ZK | 10 ZK | — | Powszechna | PG 306 |
| Koń pociągowy | 15 ZK | 4 ZK | — | Powszechna | PG 306 |
| Koń wierzchowy | 38 ZK | 15 ZK | — | Powszechna | PG 306 |
| Lekki koń bojowy | 262 ZK 10 s | 70 ZK | — | Ograniczona | PG 306 |
| Rumak | 825 ZK | 230 ZK | — | Rzadka | PG 306 |
| Uprząż z siodłem | 7 ZK 10 s | 6 ZK | 4 | Powszechna | PG 306 |
| Obroża i smycz dla psa | 2 s 6 p | 1 s 7 p | 0 | Powszechna | PG 306 |
| Furmanka | 6 ZK | 20 ZK | — | Powszechna | PG 306 |
| Wóz | 18 ZK | 75 ZK | — | Powszechna | PG 306 |
| Powóz | 150 ZK | 150 ZK | — | Rzadka | PG 306 |
| Łódka dłubanka | 6 ZK | 2 ZK | 6 | Ograniczona | PG 306 |
| Łódź wiosłowa | 18 ZK | 6 ZK | — | Ograniczona | PG 306 |
| Barka rzeczna | 225 ZK | 225 ZK | — | Rzadka | PG 306 |
| Gęś | 2 s 6 p | — | — | Powszechna | kampania |
| Kapłon | 3 s | — | — | Powszechna | kampania |
| Cielę | 1 ZK | — | — | Powszechna | kampania |

### Jedzenie, picie, nocleg

| Przedmiot | Cena | Podręcznik | Obc. | Dostępność | Źródło |
|---|---|---|---|---|---|
| Prowiant na 1 dzień | 2 s | 2 s | 0 | Powszechna | PG 302 |
| Ciepły posiłek w gospodzie (nie w handlu) | 1 s | 1 s | 0 | Powszechna | PG 302 |
| Jedzenie na zimno na 1 dzień | 10 p | 10 p | 1 | Powszechna | PG 302 |
| Nocleg w stajni (na sianie) (nie w handlu) | 4 p | — | — | Powszechna | kampania |
| Wspólna izba na 1 noc (ława albo podłoga) (nie w handlu) | 10 p | 10 p | — | Powszechna | PG 302 |
| Prywatny pokój na 1 noc (nie w handlu) | 3 s | 10 s | — | Powszechna | PG 302 |
| Stajnia dla konia na 1 noc (z obrokiem) (nie w handlu) | 1 s 2 p | 10 p | — | Powszechna | PG 302 |
| Pół litra piwa | 3 p | 3 p | 0 | Powszechna | PG 302 |
| Pół litra mocnego trunku | 2 s | 2 s | 0 | Powszechna | PG 302 |
| Kielich wina | 6 p | 1 p | 0 | Powszechna | PG 302 |
| Butelka wina | 5 s 6 p | 10 p | 0 | Powszechna | PG 302 |
| Beczułka piwa (10 l) | 3 s | 3 s | 2 | Powszechna | PG 302 |
| Pół litra Piwa Bugmana | 1 s 6 p | 9 p | 0 | Rzadka | PG 302 |
| Prowiant wojskowy na 1 tydzień | 10 s | — | — | — | kampania |
| Pieprz (funt, 0,4 kg) | 1 ZK 4 s | — | — | Powszechna | kampania |
| Cynamon (funt) | 4 ZK 4 s | — | — | Powszechna | kampania |
| Szafran (funt) | 10 ZK 10 s | — | — | Powszechna | kampania |
| Goździki (kamień) | 3 ZK 1 s | — | — | Powszechna | kampania |
| Cukier (kamień) | 9 ZK 3 s | — | — | Powszechna | kampania |
| Ryż (kamień) | 2 ZK 13 s | — | — | Powszechna | kampania |
| Migdały (kamień) | 6 ZK 4 s | — | — | Powszechna | kampania |
| Rodzynki (kamień) | 4 ZK 4 s | — | — | Powszechna | kampania |
| Śledzie (beczka) | 11 ZK 10 s | — | — | Powszechna | kampania |
| Masło (garniec, 3,77 l) | 2 ZK 4 s | — | — | Powszechna | kampania |
| Sery (kopa = 60 szt.) | 1 ZK 9 s | — | — | Powszechna | kampania |
| Jaja (kopa = 60 szt.) | 4 s 6 p | — | — | Powszechna | kampania |
| Żyto (ćwiertnia) | 1 ZK 2 s | — | — | Powszechna | kampania |
| Pszenica (ćwiertnia) | 1 ZK 15 s | — | — | Powszechna | kampania |
| Jęczmień (ćwiertnia) | 1 ZK 1 s | — | — | Powszechna | kampania |
| Owies (ćwiertnia) – obrok | 11 s | — | — | Powszechna | kampania |
| Groch (korzec, 43,7 l) | 9 s | — | — | Powszechna | kampania |
| Chleb żytni (bochenek) | 2 p | — | — | Powszechna | kampania |
| Mięso (kg) | 1 s 6 p | — | — | Powszechna | kampania |

### Czynsze i mieszkanie

| Przedmiot | Cena | Podręcznik | Obc. | Dostępność | Źródło |
|---|---|---|---|---|---|
| Kąt w izbie czeladnej / tydzień (nie w handlu) | 2 s | — | — | — | kampania |
| Kąt w izbie czeladnej / miesiąc (nie w handlu) | 7 s | — | — | — | kampania |
| Izba na poddaszu / miesiąc (nie w handlu) | 8 s | — | — | — | kampania |
| Izba w kamienicy / miesiąc (nie w handlu) | 1 ZK 4 s | — | — | — | kampania |
| Izba w kamienicy / rok (nie w handlu) | 12 ZK | — | — | — | kampania |
| Mieszkanie mieszczańskie (2–3 izby) / miesiąc (nie w handlu) | 2 ZK | — | — | — | kampania |
| Mieszkanie mieszczańskie / rok (nie w handlu) | 20 ZK | — | — | — | kampania |
| Dom mistrza z warsztatem / rok (nie w handlu) | 40 ZK | — | — | — | kampania |
| Kamienica kupiecka / rok (nie w handlu) | 110 ZK | — | — | — | kampania |
| Kupno: prosty dom (nie w handlu) | 120 ZK | — | — | — | kampania |
| Kupno: dom rzemieślnika (nie w handlu) | 320 ZK | — | — | — | kampania |
| Kupno: kamienica patrycjuszowska (nie w handlu) | 3600 ZK | — | — | — | kampania |

### Ubranie i dodatki

| Przedmiot | Cena | Podręcznik | Obc. | Dostępność | Źródło |
|---|---|---|---|---|---|
| Ubranie | 2 ZK 2 s | 6 s | 1 | Powszechna | PG 302 |
| Buty | 18 s | 5 s | 0 | Powszechna | PG 302 |
| Wysokie buty | 1 ZK 10 s | 5 s | 1 | Powszechna | PG 302 |
| Płaszcz | 1 ZK 19 s | 10 s | 1 | Powszechna | PG 302 |
| Opończa | 2 ZK 14 s | 18 s | 1 | Powszechna | PG 302 |
| Kapelusz | 10 s 6 p | 4 s | 0 | Powszechna | PG 302 |
| Kaptur lub maska | 10 s | 5 s | 0 | Powszechna | PG 302 |
| Rękawiczki | 9 s | 4 s | 0 | Powszechna | PG 302 |
| Szata | 4 ZK 10 s | 2 ZK | 1 | Powszechna | PG 302 |
| Mundur | 3 ZK | 1 ZK 2 s | 1 | Ograniczona | PG 302 |
| Kostium | 3 ZK | 1 ZK | 1 | Ograniczona | PG 302 |
| Strój dworski | 45 ZK | 12 ZK | 1 | Ograniczona | PG 302 |
| Strój ceremonialny (aksamit, złotogłów, futra) | 330 ZK | — | 1 | — | kampania |
| Laska | 6 ZK | 3 ZK | 1 | Powszechna | PG 302 |
| Berło | 15 ZK | 8 ZK | 1 | Rzadka | PG 302 |
| Sygnet | 10 ZK | 5 ZK | 0 | Rzadka | PG 302 |
| Pierścień srebrny | 1 ZK | — | 0 | Powszechna | kampania |
| Pierścień złoty | 10 ZK | — | 0 | Powszechna | kampania |
| Pierścień z klejnotem | 45 ZK | — | 0 | Powszechna | kampania |
| Symbol religijny | 12 s | 6 s 8 p | 0 | Powszechna | PG 302 |
| Amulet | 5 p | 2 p | 0 | Powszechna | PG 302 |
| Perfumy | 1 ZK 10 s | 10 s | 0 | Powszechna | PG 302 |
| Puder do twarzy | 1 ZK 3 s | 10 s | 0 | Powszechna | PG 302 |
| Zapinki (6) | 1 ZK 10 s | 10 s | 0 | Ograniczona | PG 302 |
| Tatuaż (nie w handlu) | 6 s | 4 s | 0 | Ograniczona | PG 302 |
| Jedwabna bielizna | 3 ZK | 1 ZK | — | — | Pod Bronią |
| Focza skóra | 4 ZK 10 s | 1 ZK 10 s | — | — | Pod Bronią |
| Sukno cienkie, importowane (łokieć) | 1 ZK 15 s | — | — | Powszechna | kampania |
| Płótno (łokieć) | 1 s 6 p | — | — | Powszechna | kampania |
| Sukno szare, samodział (łokieć) | 6 s | — | — | Powszechna | kampania |
| Płótno zgrzebne, konopne (łokieć) | 8 p | — | — | Powszechna | kampania |

### Narzędzia i zestawy

| Przedmiot | Cena | Podręcznik | Obc. | Dostępność | Źródło |
|---|---|---|---|---|---|
| Narzędzia Pracy | 7 ZK 4 s | 3 ZK | 1 | Rzadka | PG 296 |
| Warsztat | 320 ZK | 80 ZK | nie do noszenia | Egzotyczna | PG 296 |
| Sierp | 3 s 6 p | 1 ZK | 1 | Powszechna | PG 303 |
| Motyka | 1 s 10 p | 4 s | 2 | Powszechna | PG 303 |
| Grabie | 1 s 2 p | 4 s 6 p | 2 | Powszechna | PG 303 |
| Szpadel | 1 s 10 p | 8 s | 2 | Powszechna | PG 303 |
| Kilof | 12 s | 18 s | 1 | Ograniczona | PG 303 |
| Młotek | 3 s 6 p | 3 s | 0 | Powszechna | PG 303 |
| Piła | 9 s 6 p | 6 s | 1 | Powszechna | PG 303 |
| Dłuto | 5 s | 4 s 2 p | 0 | Powszechna | PG 303 |
| Gwoździe (12) | 4 p | 2 p | 0 | Powszechna | PG 303 |
| Łom | 5 s | 2 s 6 p | 1 | Powszechna | PG 303 |
| Drąg (3 m) | 2 s 6 p | 8 s | 3 | Powszechna | PG 303 |
| Bosak | 7 s | 6 s | 0 | Powszechna | Pod Bronią |
| Lina, 10 metrów | 12 s | 8 s 4 p | 1 | Powszechna | PG 308 |
| Kotwiczka | 1 ZK 16 s | 1 ZK 10 s | 1 | Ograniczona | PG 308 |
| Wiadro | 3 s 6 p | 2 s 6 p | 1 | Powszechna | PG 303 |
| Miotła | 1 s | 10 p | 2 | Powszechna | PG 303 |
| Mop | 1 s 2 p | 1 s | 2 | Powszechna | PG 303 |
| Szczotka do podłogi | 1 s 10 p | 1 s 6 p | 0 | Powszechna | PG 303 |
| Kociołek do gotowania | 1 ZK 4 s | 8 s | 1 | Powszechna | PG 308 |
| Patelnia | 18 s | 7 s 6 p | 1 | Powszechna | PG 308 |
| Miska | 1 s 2 p | 1 s | 0 | Powszechna | PG 308 |
| Talerz | 1 s 2 p | 1 s | 0 | Powszechna | PG 308 |
| Kubek | 10 p | 8 p | 0 | Powszechna | PG 302 |
| Kufel cynowy | 9 s 6 p | 4 s | 0 | Powszechna | PG 301 |
| Sztućce | 7 s | 3 s 6 p | 0 | Powszechna | PG 308 |
| Moździerz z tłuczkiem | 17 s | 14 s | 0 | Powszechna | PG 303 |
| Wytrychy | 1 ZK 4 s | 15 s | 0 | Ograniczona | PG 303 |
| Kajdany | 1 ZK 4 s | 18 s | 0 | Ograniczona | PG 303 |
| Stalowe szczypce | 12 s | 16 s | 0 | Powszechna | PG 303 |
| Haczyki na ryby (12) | 1 s 2 p | 1 s | 0 | Powszechna | PG 303 |
| Sidła na zwierzęta | 3 s 6 p | 2 s 6 p | 1 | Powszechna | PG 303 |
| Kule | 3 s 6 p | 3 s | 2 | Powszechna | PG 303 |
| Klucz | 2 s 6 p | 1 s | 0 | Powszechna | PG 303 |
| Kołek | 7 p | 1 s | 0 | Powszechna | PG 303 |
| Liczydło | 6 s | 3 s 4 p | 0 | Ograniczona | PG 303 |
| Grzebień | 1 s 2 p | 10 p | 0 | Powszechna | PG 303 |
| Pinceta | 1 s 2 p | 1 s | 0 | Ograniczona | PG 303 |
| Pióro do pisania | 5 p | 3 s | 0 | Powszechna | PG 303 |
| Pędzel do malowania | 5 s | 4 s | 0 | Powszechna | PG 303 |
| Grawerowana pieczęć | 8 ZK | 5 ZK | 0 | Ograniczona | PG 303 |
| Młotek sędziego | 6 s | 1 ZK | 0 | Ograniczona | PG 303 |
| Soczewki do czytania | 2 ZK 8 s | 3 ZK | 0 | Rzadka | PG 303 |
| Teleskop | 18 ZK | 5 ZK | 0 | Rzadka | PG 303 |
| Zestaw do pisania | 2 ZK 8 s | 2 ZK | 0 | Ograniczona | PG 303 |
| Zestaw do charakteryzacji | 18 s | 6 s 6 p | 0 | Ograniczona | PG 303 |
| Zestaw na zatrucia | 4 ZK 16 s | 3 ZK | 0 | Ograniczona | PG 303 |
| Oselka | 3 s | 2 s 6 p | — | — | Pod Bronią |
| Bandolier | 9 s 6 p | 6 s | — | — | Pod Bronią |
| Cięciwa | 5 s | 4 s | — | — | Pod Bronią |
| Lont prochowy (1 m) | 4 p | 2 p | — | — | Pod Bronią |
| Kompas | 2 ZK 8 s | 10 s | — | — | Pod Bronią |
| Teodolit | 14 ZK 10 s | 6 ZK | — | — | Pod Bronią |
| Strusie pióro | 12 s | 3 s | — | — | Pod Bronią |
| Lusterko ręczne | 1 ZK 12 s | 1 ZK 1 s 6 p | 0 | Egzotyczna | PG 303 |
| Narzędzie do czyszczenia uszu | 2 s 6 p | 2 s | 0 | Ograniczona | PG 303 |
| Siekiera | 4 s | — | — | Powszechna | kampania |

### Księgi i dokumenty

| Przedmiot | Cena | Podręcznik | Obc. | Dostępność | Źródło |
|---|---|---|---|---|---|
| Arkusz pergaminu | 1 s 2 p | 1 s | 0 | Powszechna | PG 304 |
| Broszura | 7 p | 1 s | 0 | Powszechna | PG 304 |
| Dokument prawny | 5 s | 3 s | 0 | Powszechna | PG 304 |
| Księga, religia | 5 ZK | 1 ZK | 1 | Powszechna | PG 304 |
| Księga, inżynieria | 12 ZK | 3 ZK | 1 | Ograniczona | PG 304 |
| Księga, sztuka | 20 ZK | 5 ZK | 1 | Ograniczona | PG 304 |
| Księga, aptekarstwo | 30 ZK | 8 ZK | 1 | Ograniczona | PG 304 |
| Księga, kryptografia | 30 ZK | 8 ZK | 1 | Egzotyczna | PG 304 |
| Księga, medycyna | 60 ZK | 15 ZK | 1 | Rzadka | PG 304 |
| Księga, prawo | 60 ZK | 15 ZK | 1 | Rzadka | PG 304 |
| ⚠ Księga, magia | 120 ZK | 20 ZK | 1 | Egzotyczna | PG 304 |
| Mapa | 12 ZK | 3 ZK | 0 | Ograniczona | PG 304 |

### Zioła, mikstury, narkotyki

| Przedmiot | Cena | Podręcznik | Obc. | Dostępność | Źródło |
|---|---|---|---|---|---|
| Mikstura lecznicza | 1 ZK 10 s | 10 s | 0 | Ograniczona | PG 307 |
| Kataplazm leczniczy | 1 ZK 4 s | 12 s | 0 | Powszechna | PG 307 |
| Eliksir żywotności | 2 ZK | 18 s | 0 | Ograniczona | PG 307 |
| Salwort | 12 s | 12 s | 0 | Powszechna | PG 307 |
| Tonik na trawienie | 6 s | 3 s | 0 | Powszechna | PG 307 |
| Fakstoryl | 1 ZK | 15 s | 0 | Egzotyczna | PG 307 |
| ⚠ Nocny cień | 3 ZK | 3 ZK | 0 | Rzadka | PG 307 |
| Ziemny korzeń | 5 ZK | 5 ZK | 0 | Ograniczona | PG 307 |
| ⚠ Dziwnokorzeń | 4 s | 4 s | 0 | Rzadka | PG 306 |
| ⚠ Rozkosz Ranalda | 2 ZK | 18 s | 0 | Ograniczona | PG 306 |
| ⚠ Korzeń mandragory | 1 ZK | 1 ZK | 0 | Rzadka | PG 306 |
| Pluja | 1 ZK 5 s | 1 ZK 5 s | 0 | Rzadka | PG 306 |
| ⚠ Księżycowy kwiat | 6 ZK | 5 ZK | 0 | Ograniczona | PG 306 |
| ⚠ Grzybki Szalonego Kapelusznika | 5 ZK | 5 ZK | 0 | Egzotyczna | PG 306 |
| ⚠ Czarny lotos | 30 ZK | 20 ZK | 0 | Egzotyczna | PG 306 |
| ⚠ Sercobój | 120 ZK | 40 ZK | 0 | Egzotyczna | PG 306 |

### Wyposażenie różne

| Przedmiot | Cena | Podręcznik | Obc. | Dostępność | Źródło |
|---|---|---|---|---|---|
| Świece (tuzin) | 2 s 6 p | 1 s | 0 | Powszechna | PG 308 |
| Zapałka | 1 p | 1 p | 0 | Powszechna | PG 308 |
| Lampa oliwna | 3 s 6 p | 2 s | 0 | Powszechna | PG 308 |
| Latarnia | 18 s | 12 s | 1 | Powszechna | PG 308 |
| Lampa sztormowa | 1 ZK 16 s | 1 ZK | 1 | Ograniczona | PG 308 |
| Lampa Davricha | 4 ZK 16 s | 2 ZK | 1 | Rzadka | PG 308 |
| Koc | 1 ZK 4 s | 8 p | 0 | Powszechna | PG 308 |
| Zwijane posłanie | 1 ZK 12 s | 6 s | 1 | Powszechna | PG 308 |
| Namiot | 3 ZK 12 s | 12 s | 2 | Ograniczona | PG 308 |
| Płócienna plandeka | 1 ZK 10 s | 8 s | 1 | Powszechna | PG 308 |
| Pudełko na hubkę i krzesiwo | 6 s | 4 s 2 p | 0 | Powszechna | PG 308 |
| Kości do gry | 1 s 2 p | 10 p | 0 | Powszechna | PG 308 |
| Talia kart | 2 s 6 p | 1 s | 0 | Powszechna | PG 308 |
| Instrument | 4 ZK 16 s | 2 ZK | 1 | Rzadka | PG 308 |
| Bandaż | 7 p | 4 p | 0 | Powszechna | PG 308 |
| Kreda / węgiel do rysowania | 7 p | 10 p | 0 | Powszechna | PG 303 |
| Szmaty | 1 p | 1 p | 0 | Powszechna | PG 308 |
| Lalka | 2 s 6 p | 2 s | 0 | Powszechna | PG 308 |
| Piłka | 6 p | 5 p | 0 | Powszechna | PG 308 |
| Afisz | 7 p | 1 s | 2 | Powszechna | PG 308 |
| Fajka i tytoń | 6 s | 3 s 4 p | 0 | Ograniczona | PG 308 |
| Beczka (145 l) | 9 s 6 p | 8 s | 6 | Powszechna | PG 301 |
| Beczułka (45 l) | 3 s 6 p | 3 s | 2 | Powszechna | PG 301 |
| Bukłak | 3 s 6 p | 1 s 8 p | 1 | Powszechna | PG 301 |
| Butelka | 3 s 6 p | 5 s | 0 | Powszechna | PG 301 |
| Dzban | 3 s 6 p | 3 s 2 p | 1 | Powszechna | PG 301 |
| Plecak | 9 s 6 p | 4 s 10 p | 2 | Powszechna | PG 301 |
| Sakiewka | 1 s 2 p | 4 p | 0 | Powszechna | PG 301 |
| Duży worek | 3 s 6 p | 1 s 6 p | 3 | Powszechna | PG 301 |
| Worek | 1 s 10 p | 1 s | 2 | Powszechna | PG 301 |
| Torba na ramię | 2 s 6 p | 1 s | 1 | Powszechna | PG 301 |
| Juki | 1 ZK 10 s | 18 s | 4 | Powszechna | PG 301 |
| Tuba na zwoje | 7 s | 16 s | 0 | Ograniczona | PG 301 |
| Oliwa (litr) | 11 s | — | — | Powszechna | kampania |
| Świeca woskowa (sztuka) | 4 s | — | — | Powszechna | kampania |
| Prześcieradło | 12 s | — | — | Powszechna | kampania |
| Siennik | 4 s | — | — | Powszechna | kampania |
| Ręcznik | 8 s 6 p | — | — | Powszechna | kampania |
| Olej do lampy, rzepakowy albo tran (litr) | 2 s | — | — | Powszechna | kampania |

### Protezy

| Przedmiot | Cena | Podręcznik | Obc. | Dostępność | Źródło |
|---|---|---|---|---|---|
| Hak | 7 s | 3 s 4 p | 1 | Powszechna | PG 308 |
| Opaska na oko | 1 s 2 p | 6 p | 0 | Powszechna | PG 308 |
| Drewniane zęby | 1 ZK 4 s | 10 s | 0 | Rzadka | PG 308 |
| Sztuczna noga | 1 ZK 16 s | 16 s | 2 | Ograniczona | PG 308 |
| Sztuczne oko | 2 ZK 8 s | 1 ZK | 0 | Rzadka | PG 308 |
| Złoty nos | 2 ZK 8 s | 18 s | 0 | Ograniczona | PG 308 |
| Cud inżynierii | 72 ZK | 20 ZK | 1 | Egzotyczna | PG 308 |

### Najmici i usługi (za tydzień)

| Przedmiot | Cena | Podręcznik | Obc. | Dostępność | Źródło |
|---|---|---|---|---|---|
| Robotnik niewykwalifikowany (nie w handlu) | 14 s | — | — | — | kampania |
| Czeladnik (nie w handlu) | 1 ZK 3 s | — | — | — | kampania |
| Mistrz rzemiosła (nie w handlu) | 2 ZK 15 s | — | — | — | kampania |
| Tragarz (nie w handlu) | 14 s | 1 ZK 4 s | — | — | PG 309 |
| Miejscowy zwiadowca (nie w handlu) | 14 s | 10 s | — | — | PG 309 |
| Skryba (nie w handlu) | 2 ZK | 2 ZK 8 s | — | — | PG 309 |
| Prawnik (nie w handlu) | 3 ZK 12 s | 3 ZK 12 s | — | — | PG 309 |
| Doświadczony najemnik (nie w handlu) | 3 ZK | 3 ZK 12 s | — | — | PG 309 |
| Doktor (jedna wizyta) (nie w handlu) | 5 s | 5 s | — | — | PG 309 |
| Doktor (na tydzień) (nie w handlu) | 5 ZK | 5 ZK | — | — | PG 309 |
| Wpis ucznia do cechu (nie w handlu) | 1 ZK | — | — | — | kampania |
| Wykup licencji cechowej (nie w handlu) | 15 ZK | — | — | — | kampania |
