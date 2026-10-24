# Cennik a źródła historyczne – analiza i propozycja v2

Sprawdziłem cennik kampanii (331 pozycji) w dwóch krokach:

1. Porównałem go z 8 źródłami, na których oparto artefakt „Skarbiec Imperium” – **102 porównania** z konkretnymi
   cenami.
2. Sprawdziłem spójność wewnętrzną według **50 reguł** (`data/spojnosc.json`).

Wynik to **propozycja**: `propozycja/cennik_v2.json`, 94 zmiany. Obowiązujący cennik (`data/cennik.json`) jest
nietknięty, dopóki nie zatwierdzisz zmian.

- Obecny cennik łamie 8 z 50 reguł.
- Propozycja v2 przechodzi wszystkie (`node --test test/spojnosc.test.mjs`).

---

## 1. Metoda: każda cena w dniówkach ze swojego miejsca i czasu

Kotwica się nie zmienia: **1 dniówka robotnika = 27,5 p** (Brąz 3; Kraków 1530: 1,5 gr).

Zmieniam natomiast sposób przeliczania cen zagranicznych. Artefakt liczył każdą cenę angielską tak, jakby robotnik
zarabiał 4 d dziennie, niezależnie od stulecia. Tymczasem robotnik w Anglii zarabiał:

| Okres | Płaca dzienna robotnika | Źródło |
|---|---|---|
| 1281–1320 | 1–1,25 d | Dyer, tabela na stronie UC Davis |
| 1351–1390 | 2–2,5 d | j.w. |
| 1441–1520 | 3,25–4 d | j.w. |
| ok. 1560–90 | **7 d** (rzemieślnik 10–12 d) | Phelps Brown & Hopkins; piechur 8 d/dzień (UC Davis) |
| 1580–1600 | 8 d | j.w. |

Inne przeliczniki:

- Frankfurt 1425–50: robotnik winnicy 14–20 H; 1 gulden ≈ 17 dniówek (⚠ szacunek, ±30%).
- Kolonia 1390: stawka ucznia 36 Pf.

Skutek w artefakcie:

- **ceny z XIII–XIV w. są zaniżone** 1,5–3 razy;
- **ceny z końca XVI w. są zawyżone** ok. 1,8 raza – a stamtąd pochodzi cała lista broni (miecz, pika, łuki,
  kaliwer, korselet).

Wszystkie przeliczenia: `narzedzia/zrodla.py` → `narzedzia/zrodla_wynik.json`.

## 2. Co się zgadza, a co nie

| Grupa | Porównań | Mediana (cennik ÷ źródło) | Ocena |
|---|---|---|---|
| Dane krakowskie i polskie: konie, wół, wieprz, drób, buty, piwo, wino, płace | 26 | **1,03** | bardzo dobrze – to fundament cennika |
| Pozostałe (Anglia XIII–XV w., Frankfurt, Kolonia) | 55 | 1,09 | dobrze, ale z kilkoma dużymi wyjątkami (niżej) |
| Broń i pancerz municyjny z Anglii elżbietańskiej | 15 | **1,78** | systemowo za drogo – błąd przeliczenia |
| Czynsze | 6 | **3,65** | 3–5 razy za drogo |

**Potwierdzone, bez zmian:**

- konie (pociągowy 15 ZK, wierzchowy 38 ZK, rumak 550 ZK – dolna granica konia bojowego);
- wół, krowa, świnia, kurczak;
- pełna płytówka 48 ZK (zbroja giermka / mediolańska z 1441 r. = 36–57 ZK);
- zbroja mistrzowska 190 ZK (cały rynsztunek rycerza z 1374 r. ≈ 180 ZK);
- kupno domów (Frankfurt 1450: prosty dom, dom rzemieślnika, dom patrycjusza – po ±20%);
- płace robotnika, czeladnika, mistrza;
- piwo, prowiant, buty, kapelusze, pierścienie.

⚠ **Wycofuję jedną propozycję** z poprzedniej analizy: świnia 3 ZK jest dobrze (wieprz 36 gr w Krakowie =
2 ZK 15 s).

## 3. Zmiany w propozycji v2

Pełna lista z uzasadnieniem każdej pozycji: `propozycja/zmiany.json`.

### 3.1 Broń biała, łuki, kusze, amunicja bez prochu: ×4/7

Lista milicji Robertsa zawiera kaliwer i korselet, więc pochodzi z lat 1560–90. Wtedy robotnik brał 7 d, nie 4 d.

| Przedmiot | Źródło | Dniówki | Teraz | v2 |
|---|---|---|---|---|
| Miecz | 6 s | 10,3 | 2 ZK | **1 ZK 3 s** |
| Pika | 2 s | 3,4 | 14 s | **9 s** (włócznia 8 s) |
| Łuk długi / łuk / krótki | 3 s 4 d / 2 s 6 d / 2 s | 5,7 / 4,3 / 3,4 | 1 ZK 3 s / 17 s / 14 s | **13 s / 9 s 6 p / 8 s** |
| Strzały (12) | 2 s 4 d – 5 s za 24 | 2–4,3 | 8 s | **5 s** (= RAW) |

Żeby nie rozbić kolejności w grupie, przeliczyłem całą grupę jednym mnożnikiem (54 pozycje). Wyjątki: przedmioty o Dostępności
Egzotycznej oraz drobiazgi do 1 s.

Poziom wychodzi blisko RAW: miecz 1 ZK 3 s przy RAW 1 ZK.

### 3.2 Pancerze

| Przedmiot | Teraz | v2 | Dlaczego |
|---|---|---|---|
| Hełm otwarty (morion) | 1 ZK 3 s | **12 s** | morion 3 s 4 d, burgonet 4 s (1590) = 5–6 dniówek |
| Hełm zamknięty | 6 ZK | **8 ZK** | basinet z podszyciem (1369) = 80 dniówek; teraz napierśnik + naramienniki + nagolenniki + hełm = 48 ZK = pełna płytówka |
| Półzbroja municyjna | 11 ZK 3 s | **7 ZK 6 s** | 1 Wada (×½) od napierśnika + morionu; korselet z 1590 r. = 5–6 ZK |

### 3.3 Spanie, obóz, naczynia

| Przedmiot | Teraz | v2 | Dlaczego |
|---|---|---|---|
| Koc | 1 s 6 p | **15 s** | koc w inwentarzu z 1349–52 r. ≈ 8 dniówek; sukno 23 gr/łokieć |
| Zwijane posłanie | 8 s | **18 s** | koc + siennik + rzemienie |
| Płócienna plandeka | 15 s | **1 ZK 5 s** | ok. 15 łokci płótna po 1 gr + nasycenie |
| Namiot | 1 ZK 10 s | **3 ZK** | ok. 2 plandeki + szycie, maszty, linki |
| Butelka wina | 2 s | **5 s** | 2 s to sama zawartość (Kraków); pusta butelka 3 s (Anglia 1457) |
| Kielich wina | 2 p | **6 p** | hurt 5 p za 0,15 l |
| Beczułka 45 l / beczka 145 l | 6 s / 15 s | **3 s / 8 s** | beczka 3 d (1457); powrót do RAW |
| Beczułka piwa 10 l | 1 s 6 p | **2 s 6 p** | piwo 1 s 6 p + mała beczułka |

### 3.4 Zwierzęta, pojazdy, ubrania, narzędzia, cechy

| Przedmiot | Teraz | v2 | Dlaczego |
|---|---|---|---|
| Owca / baran | 1 ZK 10 s | **18 s** | baran 7–10 gr (Kraków), owca 1 s 5 d (Anglia XIV w.) |
| Kucyk | 18 ZK | **10 ZK** | nie może być droższy od muła i konia pociągowego |
| Furmanka / wóz / powóz | 10 / 35 / 250 ZK | **3 / 12 / 100 ZK** | wóz okuty 4 s (1350), powóz £8 (1381) |
| Barka rzeczna | 500 ZK | **150 ZK** | barka £10 (XIV w.) |
| Ubranie | 1 ZK | **1 ZK 8 s** | kitel + nogawice 36 s (Kolonia 1390) = 12 dniówek |
| Płaszcz / opończa | 1 ZK 12 s / 1 ZK 5 s | **1 ZK 5 s / 1 ZK 12 s** | zamiana, jak w RAW |
| Szpadel, motyka / grabie | 4 s, 2 s / 2 s | **1 s 6 p / 1 s** | łopata i szufla 3 d za parę (1457) |
| Lina 10 m / arkan | 1 ZK / 6 s | **10 s / 10 s** | arkan to lina z pętlą |
| Wpis ucznia / licencja cechowa | 3 ZK / 25 ZK | **1 ZK / 15 ZK** | wpisowe 1–2 s; przyjęcie do cechu 20 s; list mistrzowski 2 fl |

### 3.5 Czynsze: o ⅔ w dół

Oba źródła są zgodne. W Anglii XIV w. roczny czynsz wynosił:

- chata: 5 s;
- dom rzemieślnika: 20 s;
- dom kupca: 40–60 s.

We Frankfurcie 1450 płacili rocznie:

- murarz: 1,6 fl;
- piwowar: 4 fl;
- złotnik: 10 fl.

To 3–5 razy mniej niż w cenniku. Ceny kupna domów się zgadzają, więc obniżam czynsz. Dom kupiony na wynajem zwraca się
teraz w 8–10 lat, nie w 2 (kamienica patrycjuszowska – 33 lata, bo jest większa od kupieckiej).

| Kwatera | tydzień | miesiąc | rok (teraz → v2) |
|---|---|---|---|
| Kąt w izbie czeladnej | 2 s | 7 s | — → 3 ZK |
| Izba na poddaszu | 3 s | 8 s | 8 ZK → 4 ZK |
| Izba w kamienicy | 4 s | 12 s | 15 ZK → 6 ZK |
| Mieszkanie mieszczańskie (2–3 izby) | 6 s | 1 ZK | 32 ZK → 10 ZK |
| Dom mistrza z warsztatem | 12 s | 2 ZK | 75 ZK → 20 ZK |
| Kamienica kupiecka | 1 ZK 10 s | 5 ZK 10 s | 190 ZK → 55 ZK |

Czynsz to teraz 7–15% brutto rocznego najemcy z danego szczebla (kąt – Brąz 3, mieszkanie – Srebro 2, kamienica – Srebro 5); wcześniej 15–55%.

## 4. Do Twojej decyzji

1. **Broń palna.** Według źródeł arkebuz (rusznica) kosztowałby 1 ZK 11 s, kaliwer 4 ZK, pistolet ok. 5 ZK.
   W propozycji **zostawiłem obecne ceny** (3 / 7 / 10 ZK) jako wyjątek świata Warhammera: proch i zamki kołowe
   z Nuln, Dostępność Ograniczona albo Rzadka. Możesz też przeliczyć je jak resztę broni.
2. **Poziom broni białej (3.1).** Jeśli broń ma być celowo droższa niż w historii (Imperium w ciągłej wojnie),
   można zostawić stare ceny. Reguły spójności przejdą w obu wariantach – ważne, by cała grupa była przeliczona
   jednym mnożnikiem.
3. **Marienburg za 5 ZK.** Przy nowych czynszach mieszkanie kosztuje 1 ZK/mies., w Marienburgu ×1,45 ≈ 1 ZK 9 s.
   Żeby wyszło 5 ZK, kryzys musiałby podbić czynsz ok. 3,4 razy. Można też uznać, że gracze wynajmują cały dom mistrza
   (2 ZK × 1,45 × kryzys 1,7 ≈ 5 ZK).
4. **Nowe towary ze źródeł** – 30 gotowych pozycji w `propozycja/nowe_pozycje.json`, z cen krakowskich. Przydadzą się
   kupcowi korzennemu i kramarzowi:
   - przyprawy (pieprz 1 ZK 4 s/funt, szafran 10 ZK 10 s/funt), cukier, ryż, migdały, śledzie (beczka 11 ZK 10 s);
   - zboże na ćwiertnie, masło, sery, jaja, chleb, mięso;
   - sukno i płótno na łokcie;
   - gęś, kapłon, cielę, siekiera, prześcieradło, siennik, oliwa, świeca woskowa.

## 5. Skutki uboczne po zatwierdzeniu

- **Magiczna broń** (HR-026: cena × 50) stanieje razem z bronią zwykłą – magiczny miecz 1 właściwość: 100 → 57 ZK.
  Pancerze się nie zmieniają.
- **Kompendium MG** (strony z cennikiem i statusem) i karty broni trzeba przegenerować.
- **Kalkulator** „ile Robót odłożyć” – miecz 1 ZK 3 s zamiast 2 ZK.
- **Pozycje bez źródła.** Nóż, sztylet, puklerz, halabarda i podobne przeliczyłem razem z grupą broni. Ich
  źródło (z tamtego czatu) jest nieznane. Jeśli były z początku XVI w. (4 d), stare ceny były dobre – wtedy całą
  grupę trzeba by zostawić.

## 6. Pewność danych

- ✅ Kraków 1526–35 – ceny i płace z jednego okresu i miejsca; najlepsza podstawa.
- ✅ Anglia XIII–XV w. – płace z tabeli Dyera na tej samej stronie co ceny.
- ⚠ Anglia elżbietańska – lista Robertsa nie ma daty; okres wnioskuję z kaliweru i korseletu (po 1560).
  Płaca 7 d wg Phelps Brown & Hopkins.
- ⚠ Frankfurt – kurs guldena do płacy oszacowany (±30%).
- ⚠ Husaria (dwa artykuły) – tylko porównania w srebrze, bez cen. Potwierdzają rząd wielkości rumaka (kilkanaście kg
  srebra ≈ kilka tysięcy dniówek).
- ⚠ Landsknechci (kriegsreisende.de) – tylko żołd 4 guldeny miesięcznie.

## Źródła

- [Ceny i zarobki w Krakowie w XVI wieku – historia.org.pl](https://historia.org.pl/2025/08/09/ile-kosztowalo-zycie-w-zlotym-wieku-w-krakowie-ceny-i-zarobki-w-xvi-wieku/)
- [Ceny i pensje w XVI wieku – WielkaHistoria](https://wielkahistoria.pl/ceny-i-pensje-w-xvi-wieku-ile-zarabiali-polacy-500-lat-temu/)
- [Medieval price list – UC Davis](https://medieval.ucdavis.edu/120D/Money.html)
- [16th Century Prices of Weapons – Bow vs Musket](https://bowvsmusket.com/2015/07/01/16th-century-prices-of-weapons/)
- [Preise im Mittelalter – Wikipedia (DE)](https://de.wikipedia.org/wiki/Preise_im_Mittelalter)
- [Landsknechte – kriegsreisende.de](https://www.kriegsreisende.de/neuzeit/landsknechte.htm)
- [Stawki żołdu husarii – WielkaHistoria](https://wielkahistoria.pl/ile-zarabiali-husarze-mamy-dokladne-stawki-zoldu-i-wyliczenia/)
- [Konie husarskie – rasy i ceny – kronikidziejow.pl](https://kronikidziejow.pl/aktualnosci/historia-polski/konie-husarskie-rasy-ceny/)
- [Relative Value of Sums of Money (płace wg Phelps Brown & Hopkins)](https://freepages.rootsweb.com/~stanier/family/N-Money.html)
