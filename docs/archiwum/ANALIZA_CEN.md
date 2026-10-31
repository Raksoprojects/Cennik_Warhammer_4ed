> **ARCHIWUM — stan v1 (2026-10-23).** Liczby i zasady tutaj mogą być nieaktualne. Obowiązują: `data/*.json`, `docs/KOMPENDIUM_DANE.md` (generowany z danych), `docs/DANE.md` (decyzje MG) i `docs/AGENT_BRIEF.md`. Czytaj ten plik tylko po historię decyzji i źródła. Indeks: `docs/archiwum/README.md`.

# Analiza spójności cennika (pierwsza wersja)

> **Zastąpione przez `ANALIZA_ZRODEL.md`** (2026-10-23) – tam ceny sprawdzone ze źródłami i gotowa propozycja v2.
> Zmiany względem tej wersji: koc 15 s (nie 6 s), lina i arkan po 10 s, świnia zostaje 3 ZK,
> czynsze obniżone zamiast podnoszenia cen kupna domów, wieś – bez zmian w propozycji (decyzja nadal otwarta).

Sprawdziłem wszystkie 331 pozycje pod kątem logiki wewnętrznej:

- czy rzecz nie jest tańsza od swojej części albo od pustego pojemnika;
- czy podobne rzeczy stoją w sensownej kolejności;
- czy cena jest rozsądna wobec dniówki robotnika (27,5 p).

To są **propozycje** – nic nie zostało zmienione w `data/cennik.json`. Jeśli przyjmiesz którąś, staje się zasadą domową
(dopisek do HR-024) i zmianą w danych.

Skala: 🔴 absurd widoczny przy stole · 🟠 niespójność · 🟡 do rozważenia.

---

## 1. Koce, posłania, płachty, namioty 🔴

| Pozycja | Teraz | Dniówki | Propozycja |
|---|---|---|---|
| Koc | 1 s 6 p | 0,65 | **6 s** (2,6 dniówki) |
| Zwijane posłanie | 8 s | 3,5 | **10 s** |
| Płócienna plandeka | 15 s | 6,5 | 15 s (bez zmian) |
| Namiot | 1 ZK 10 s | 13 | 1 ZK 10 s (bez zmian) |

Problem dotyczy tylko koca. Wełniany koc to około 3 m² sukna, prawie tyle co na ubranie (1 ZK). Teraz kosztuje mniej
niż sztućce (6 s), torba na ramię (2 s) i miska z dzbanem razem. Plandeka jest od niego 10 razy droższa, a zwykle to
płótno (konopne, lniane) jest tańsze od sukna na metr.

Po zmianie powstaje kolejność:

**koc 6 s < posłanie 10 s (koc + mata, rzemienie) < plandeka 15 s < namiot 1 ZK 10 s (plandeka ×2 + maszty, linki, śledzie)**

Proporcja koca do ubrania wyniesie 30% – to tylko sukno, bez kroju i szycia.

## 2. Pojemnik droższy niż pojemnik z zawartością 🔴

| Pozycja | Teraz | Porównanie | Propozycja |
|---|---|---|---|
| Butelka wina | 2 s | pusta butelka kosztuje 3 s | **4 s** (wino ok. 10–12 p + butelka) |
| Beczułka piwa (10 l) | 1 s 6 p | pusta beczułka 45 l kosztuje 6 s | **4 s 6 p** (beczułka ok. 3 s + piwo 1 s 6 p) |

Druga możliwość: zostawić ceny, ale dopisać „do własnego naczynia”.

Komentarz w cenniku („hurt musi być tańszy od detalu”) zostaje prawdziwy: 20 półlitrów w karczmie to 5 s.

## 3. Arkan tańszy niż lina 🔴

- Lina 10 m: 1 ZK.
- Arkan: 6 s.

Arkan to lina z pętlą, a jest o ponad połowę tańszy.

Możliwe rozwiązania:

- **lina 10 m → 10 s, arkan → 10 s** (rekomendacja: lina nadal droższa niż w RAW, ale nie kosztuje tyle co buzdygan);
- albo arkan → 1 ZK 2 s, a lina zostaje.

Kotwiczka (1 ZK 10 s) bez zmian, jeśli to sam hak.

## 4. Kucyk droższy niż koń pociągowy 🔴

Kucyk kosztuje 18 ZK, koń pociągowy 15 ZK, a muł 12 ZK. Kucyk to najsłabsze zwierzę robocze w tej trójce.

Propozycja: **kucyk 10 ZK**. Kolejność: wół 6 < kucyk 10 < muł 12 < koń pociągowy 15 < koń wierzchowy 38.

## 5. Dom zwraca się w 2 lata 🔴 (czynsze vs kupno)

| Nieruchomość | Kupno | Odpowiedni czynsz roczny | Zwrot |
|---|---|---|---|
| Dom rzemieślnika | 160 ZK | dom mistrza z warsztatem: 75 ZK | **2,1 roku** |
| Prosty dom | 60 ZK | mieszkanie 2–3 izby: 32 ZK | **1,9 roku** |
| Kamienica patrycjuszowska | 1800 ZK | kamienica kupiecka: 190 ZK | 9,5 roku |

Gracz z 160 ZK kupuje dom i wynajmuje go za 47% rocznie. Kupno albo czynsz musi się zmienić. Sensowna reguła to
**cena kupna ≈ 12 × czynsz roczny** (ok. 8% zwrotu rocznie):

- prosty dom **~180 ZK** (jak izba w kamienicy ×12);
- dom rzemieślnika **~900 ZK**;
- kamienica patrycjuszowska **~2300 ZK**.

Druga możliwość: zostawić ceny kupna i obniżyć czynsze o połowę. Psuje to jednak przykład kontrolny z kampanii
(5 ZK/miesiąc w Marienburgu).

Przy okazji: dom rzemieślnika kosztuje tyle samo co Warsztat (160 ZK, same narzędzia i urządzenia). Po zmianie przestaje
to dziwić.

## 6. Płaszcz i opończa zamienione miejscami 🟠

- RAW: płaszcz 10 s, opończa 18 s.
- Po korekcie: płaszcz 1 ZK 12 s, opończa 1 ZK 5 s.

Kolejność odwróciła się bez komentarza. Propozycja: **zamienić**: płaszcz 1 ZK 5 s, opończa 1 ZK 12 s.

## 7. Półzbroja municyjna liczona starą zasadą jakości 🟠

Napierśnik 14 ZK + morion 1 ZK 3 s = 15 ZK 3 s. W cenniku stoi 11 ZK 3 s (×0,74). To nie pasuje ani do starej ¼, ani
do obecnej Wady ×½.

Według HR-024:

- 1 Wada: **7 ZK 11 s 6 p**;
- 2 Wady: **3 ZK 15 s 9 p**.

Komentarz pozycji mówi „Wada Brzydki albo Tandetny”, czyli jedna Wada → **7 ZK 12 s**.

## 8. Limit wsi blokuje bydło 🟠 (zasada generatora, nie cena)

Wieś ma limit 2 ZK, więc w żadnej wsi nie kupisz krowy (5 ZK), wołu (6 ZK), świni (3 ZK) ani konia pociągowego. A to
właśnie wieś je hoduje i sprzedaje.

Propozycja: **zwierzęta hodowlane i robocze** (owca, świnia, krowa, wół, muł, kucyk, koń pociągowy) bez limitu wsi;
konie wierzchowe i bojowe dalej tylko w mieście. W silniku to jedna lista wyjątków przy osadzie.

## 9. Do rozważenia 🟡

- **Floret = rapier (8 ZK).** Floret jest słabszy (+BS+3, Wada Tępy – PB s.93). Propozycja: 6 ZK (jak szpada).
- **Pika = włócznia (14 s).** Pika ma drzewce 2–3 razy dłuższe. Propozycja: pika 18 s (RAW). To nadal najtańsza broń
  zbrojnego, zgodnie z komentarzem.
- **Świnia 3 ZK przy krowie 5 ZK.** Świnia za 60% krowy to dużo. Propozycja: 1 ZK 10 s (jak owca).
- **Stajnia 1 s 2 p > wspólna izba 10 p.** To ma sens tylko z obrokiem. Propozycja: dopisać „z obrokiem” w nazwie.
- **Strzała (12) 8 s.** Cena może zostać, ale komentarz „wyrób bednarski” jest błędny. Strzały robi strzelarz
  (łuczarz), bednarz robi beczki.

## 10. Błędy w danych i tekstach (bez decyzji, do poprawy)

- Komentarz przy „Mieszkanie mieszczańskie / miesiąc”: „mnożnik Marienburga 1,6” – w osadach jest **1,45**.
- Kalkulator w artefakcie liczy kolczugę za **7 ZK**, cennik ma **10 ZK**.
- Zasada 5 w artefakcie podaje inne mnożniki koniunktury niż kod (opis w SPECYFIKACJA § 1).
- Zbroja mistrzowska 190 ZK, a według wzoru (2 Zalety ×4 × 48 ZK) wychodzi 192 ZK – zaokrąglenie, można zostawić.
- Nagłówek artefaktu „302 pozycje, w tym 28 dopisanych” – teraz 331. Rumak: „15 lat” w nagłówku, „16 lat”
  w komentarzu.

## Co sprawdziłem i jest w porządku

- **Narzędzia rolne.** Sierp 3 s, motyka i grabie 2 s, szpadel 4 s, kilof 10 s.
- **Broń.** Nóż 1 s 6 p < nóż do rzucania 6 s < sztylet 10 s < miecz 2 ZK.
- **Pancerze.** Suma elementów płytowych 46 ZK, cała płytówka 48 ZK. Kolczuga 10 ZK < kaftan + nogawice kolcze 12 ZK.
- **Jedzenie i nocleg.**
  - Prowiant 2 s/dzień, a wojskowy 1 s 5 p/dzień. Prowiant jest droższy od jedzenia na zimno (10 p), bo to trwała żywność.
  - Wspólna izba 10 p/noc, a kąt w izbie czeladnej ok. 3,4 p/noc przy najmie tygodniowym. Prywatny pokój za miesiąc
    (4 ZK 10 s) wychodzi drożej niż mieszkanie (3 ZK), bo gospoda bierze więcej.
- **Odzież.** Buty 12 s < wysokie buty 1 ZK. Ubranie 1 ZK < mundur, kostium 2 ZK < szata 3 ZK < strój dworski 30 ZK <
  ceremonialny 220 ZK.
- **Pojemniki.**
  - Worek 1 s < duży worek 2 s.
  - Sakiewka 1 s < torba 2 s < plecak 8 s < juki 1 ZK 5 s.
  - Beczułka 45 l 6 s < beczka 145 l 15 s.
- **Usługi.** Robotnik i tragarz 14 s/tydz. odpowiadają brutto Brązu 3. Czeladnik 1 ZK 3 s odpowiada Brązowi 5.
  Mistrz 2 ZK 15 s odpowiada Srebru 2. Doktor 5 ZK/tydz. odpowiada Srebru 4.
- **Dostępność u kupców.** Każdą pozycję cennika ktoś z 15 handlarzy może mieć na stanie (żadna nie przekracza
  wszystkich limitów).
