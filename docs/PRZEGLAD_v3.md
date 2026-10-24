# Przegląd analizy i cennik v3

Odpowiedź na `ANALIZA_ZRODEL.md` i `Skarbiec_podsumowanie_rozmowy.md`. Sprawdziłem analizę u źródła,
przyjąłem ją w całości, dołożyłem trzy rzeczy, których w niej nie było, i zamykam sześć otwartych decyzji.

**Wynik:** `data/cennik.json` = **v3**, 361 pozycji. Testy: `node --test test/` — 11 przypadków, wszystkie
przechodzą (5 spójności + 6 zgodności z oryginałem).

---

## 1. Weryfikacja: analiza ma rację

Sprawdziłem najważniejsze twierdzenie bezpośrednio na stronie UC Davis, bo od niego zależą 94 zmiany.

**Potwierdza się.** Strona reprodukuje tabelę Christophera Dyera (*Standards of Living in the Later Middle
Ages*, s. 206) i podaje dzienne płace dekada po dekadzie. Jedna rzecz wymaga doprecyzowania, bo bez niej
nikt tego nie odtworzy: **to jest tabela strzecharza i jego pomocnika**, a nie „robotnika" w ogóle.
Analiza słusznie wzięła kolumnę **pomocnika** jako odpowiednik robotnika niewykwalifikowanego:

| Dekada | Strzecharz | **Pomocnik** |
|---|---|---|
| 1301–10 | 2,5 d | **1 d** |
| 1341–50 | 3 d | **1,25 d** |
| 1351–60 | 3,5 d | **2 d** |
| 1441–50 | 5,25 d | **4 d** |
| 1501–10 | 5,75 d | **4 d** |
| 1511–20 | 5,25 d | **4 d** |

Tabela Dyera kończy się na 1520 r. Dla czasów elżbietańskich analiza sięga po Phelps Browna i Hopkinsa
(7–8 d) — i strona UC Davis to **niezależnie potwierdza**: piechota w końcu XVI w. brała **8 d dziennie**,
a jazda 18 d. Dwa niezależne tory dają ten sam rząd wielkości.

**Konsekwencja dla mojej pierwotnej pracy:** przyjąłem 4 d na dniówkę dla wszystkich cen angielskich,
od 1281 do 1650 roku. To jest poprawne wyłącznie dla okresu 1441–1520. Dla XIII–XIV w. zaniżałem,
dla czasów elżbietańskich — zawyżałem o ok. 1,75×. Lista milicji Robertsa (kaliwer, korselet) pochodzi
z lat 1560–90, więc **cała grupa broni białej i łuków była w cenniku zawyżona**. Przyjmuję korektę ×4/7
w całości.

Sprawdziłem też arytmetykę na dwunastu pozycjach — mnożniki wychodzą 0,55–0,64 (zaokrąglenia do równej
monety), czyli zgodnie z deklarowanym ×4/7. Czynsze: Frankfurt 1450, murarz płaci 1,6 guldena rocznie
= 3 ZK 13 s. Mój stary cennik kazał mu płacić 15 ZK. Korekta o ⅔ jest słuszna.

---

## 2. Czego w analizie nie było

### 2.1 Defekt: handlarze sprzedają nocleg i cudzą pracę

Uruchomiłem silnik na 900 wygenerowanych sklepach. Kramarz na targu w miasteczku, seed 7:

```
Wspólna izba na 1 noc        sztuk:  37   cena 11 p    odkupi za 4 p
Ciepły posiłek w gospodzie   sztuk:  58   cena  1 s    odkupi za 7 p
Stajnia na 1 noc             sztuk:  15   cena 10 p    odkupi za 2 p
```

Straganiarz ma na stanie 37 noclegów i odkupi od ciebie przespaną noc za 4 pensy. Kwatermistrz
w oblężeniu sprzedaje wspólną izbę po 2 s 10 p przy cenie wytwórcy 10 p.

Dwa błędy naraz. Po pierwsze, nocleg i posiłek to **usługi**, nie towar — nie mają stanu magazynowego
i nie da się ich odkupić. Po drugie, ich ceny w cenniku są **już detaliczne**: karczmarz jest
detalistą, więc marża kupca nalicza narzut drugi raz.

**Poprawka.** Każda pozycja ma teraz pole `typ`:

| typ | ile | handlowalne |
|---|---|---|
| `towar` | 333 | tak |
| `nocleg` | 4 | nie |
| `usluga` | 12 | nie |
| `nieruchomosc` | 12 | nie |

`rynek.asortyment.wykluczone_typy` wyklucza trzy ostatnie z asortymentu, skupu i zamówień. Pozycje
zostają w cenniku i w wyszukiwarce — wypadają tylko z handlu. Po poprawce: **0 niedozwolonych pozycji
w 900 sklepach**.

### 2.2 Czynsz nie reagował na koniunkturę

Zasada mówiła „stosuj mnożnik osady i koniunktury", ale `koniunktura.json` nie miał dla czynszu nic.
A czynsz jest najbardziej nieelastycznym dobrem, jakie istnieje, i reaguje **odwrotnie niż żywność**.

| Sytuacja | Czynsz | Dlaczego |
|---|---|---|
| Normalna | ×1,0 | — |
| Nadmiar po jarmarku | ×1,0 | jarmark nie rusza komornego |
| Niedobór | ×1,1 | drożyzna przenosi się z opóźnieniem |
| Wojna | ×1,3 | uchodźcy ze wsi, kwaterunek wojska |
| **Zaraza** | **×0,6** | puste izby po zmarłych — dokładnie to, co stało się po czarnej śmierci |
| Oblężenie | ×2,0 | nikt nie wychodzi, nikt nie buduje |
| Zamknięte szlaki | ×1,1 | kupcy utknęli w mieście |
| **Kryzys mieszkaniowy** (nowy) | **×3,0** | pożar dzielnicy, napływ uchodźców, zajęcie kwater |

Zaraza obniżająca czynsze to najlepszy hak fabularny z całej tabeli: miasto umiera, a mieszkanie
nagle tanieje.

### 2.3 Dwa miejsca, gdzie v2 nie dociągnęła do własnego źródła

- **Furmanka.** Źródło: wóz okuty 4 s (1350). Pomocnik strzecharza brał wtedy 1,25 d, więc
  4 s = 48 d = 38 dniówek = **4 ZK 8 p**. v2 dała 3 ZK. Podnoszę do 4 ZK.
- **Barka rzeczna.** £10 w XIV w. przy dniówce 2,5 d = 960 dniówek ≈ 110 ZK. v2 dała 150 ZK, co jest
  powyżej źródła — ale RAW opisuje jednostkę o Udźwigu 300 z trzyosobową załogą, więc zostawiam
  **150 ZK** jako świadomą górną granicę i zapisuję to w `uwagi_danych`, zamiast udawać, że to wynik
  przeliczenia.

---

## 3. Rzecz najważniejsza: 200 z 361 pozycji nie ma źródła

Spór o ×4/7 dotyczy 54 pozycji. Tymczasem **200 z 361 nie ma żadnej podstawy historycznej** — to moje
oszacowania z wyczucia, które przeszły przez wszystkie kolejne wersje bez weryfikacji, bo nikt ich
nie podważył.

Gorzej: w **jedenastu** przypadkach zapisałem własny szacunek w gramatyce cytatu — „Nóż kuchenny
– 3 d ang.", „Halabarda – 4 s ang.", „Sierp – ok. 5 d ang." Te liczby nie padły w żadnym źródle.
Wyglądają na cytaty, bo tak je sformatowałem, i analiza słusznie oznaczyła je jako „źródło nieznane".

Pełna lista pozycji, których „podstawa historyczna" jest moim szacunkiem, a nie cytatem:

> Nóż · Sztylet · Kostur · Topór · Halabarda · Tarcza (puklerz) · Tarcza · Skórzana kurta ·
> Ciepły posiłek w gospodzie · Prywatny pokój na 1 noc · Sierp

Pozostałe pozycje z monetą angielską **są** cytatami: kaliwer 20 s, snop strzał 2 s 4 d i proch
1 s/funt (lista Robertsa), ołów 2 d/funt, jedwab 10–12 s/jard, pergamin 1–2 d (UC Davis).

**Wniosek praktyczny:** to zamyka otwartą decyzję nr 6. Te pozycje nie mają źródła z początku XVI w.,
bo nie mają żadnego. Przeliczenie ich razem z grupą broli jednym mnożnikiem jest nie tylko dopuszczalne —
jest jedyną uczciwą metodą, bo zachowuje proporcje, które były jedyną realną treścią tych liczb.

W `cennik.json` oznaczyłem to polem `uwagi_danych` tam, gdzie była korekta własna. Pozycje bez źródła
rozpoznasz po pustym `podstawa_hist`.

---

## 4. Sześć otwartych decyzji — odpowiedzi

**1. Broń palna: przeliczyć czy zostawić?**
**Zostawić** (rusznica 3 ZK, kaliwer 7 ZK, pistolet 10 ZK), ale zapisać jako świadomą zasadę świata,
a nie przeoczenie. Uzasadnienie jest mocne: w Imperium broń prochowa to produkt licencjonowany,
wychodzący z kilku hut w Nuln, objęty Dostępnością Ograniczoną i Rzadką. Historyczny arkebuz był tani,
bo robiło go pół Europy. Imperialna rusznica jest droga z tego samego powodu, z którego dziś drogie są
rzeczy koncesjonowane. Dopisane w `cennik.json → komentarz`.

**2. Poziom broni białej: ×4/7 czy zostawić drożej?**
**Przyjąć ×4/7.** Dwa argumenty. Po pierwsze, jest sourceowane, a alternatywa nie. Po drugie — i to
jest ciekawsze — wynik ląduje **blisko RAW** (miecz 1 ZK 3 s wobec 1 ZK w podręczniku). Kiedy niezależna
droga przez źródła historyczne wraca do liczby z podręcznika, to jest sygnał, że podręcznik miał rację,
a nie zbieg okoliczności.

**3. Marienburg za 5 ZK.**
Nie naciągać. Dodałem **mnożnik czynszu dla koniunktury** (2.2) i kryzys mieszkaniowy ×3,0.
Wynik: mieszkanie mieszczańskie 1 ZK/mies. × Marienburg 1,45 × kryzys 3,0 = **4 ZK 7 s**. To jest
praktycznie 5 ZK, które płacą gracze, i wychodzi z reguły, a nie z wyjątku dopisanego pod wynik.

**4. 30 nowych pozycji.**
**Dopisane.** Wszystkie pochodzą z danych krakowskich, czyli z najmocniejszego źródła w całym zestawie
(mediana cennik ÷ źródło = 1,03). Dają kupcowi korzennemu i kramarzowi prawdziwy asortyment:
przyprawy, zboże na ćwiertnie, sukno i płótno na łokcie, drób, śledzie, oliwę, świece woskowe.
Poprawiłem przy okazji generowanie identyfikatorów — polskie „ł" ginęło w normalizacji
(`kapłon` → `kapon`, `płótno` → `potno`).

**5. Zwierzęta we wsi.**
**Zrobione.** Limit wsi (2 ZK) i wymóg Dostępności Powszechnej nie dotyczą teraz pozycji z podtypem
`zwierze_hodowlane` ani `zywnosc_podstawowa`. Wieś jest dokładnie tym miejscem, gdzie kupuje się krowę.
Handlarz koni we wsi wystawia teraz konia pociągowego, muła, wołu, krowę, cielę, owcę, kapłona i gęś.

**6. Pozycje bez znanego źródła.**
Odpowiedź w rozdziale 3: **nie mają źródła z początku XVI w., bo nie mają żadnego.** Grupowy
mnożnik jest właściwym rozwiązaniem.

---

## 5. Co zostaje otwarte

1. **Kurs guldena frankfurckiego** (±30%) wisi nad wszystkimi cenami domów, czynszów i wozów.
   Jeśli kiedyś znajdzie się płaca dzienna frankfurckiego pomocnika wyrażona w guldenach, warto przeliczyć.
2. **Dwa źródła prawdy dla czynszu** — `czynsze.json` i wiersze w `cennik.json`. Na razie zgadzają się
   co do grosza i pilnuje tego nowy test, ale w aplikacji jedno powinno generować drugie.
3. **Kalkulator** ma zaszyte ceny (`kalkulator.json`). Po każdej zmianie cennika trzeba je odświeżyć —
   albo, lepiej, czytać po `id` z cennika. W specyfikacji aplikacji proponuję to drugie.
4. **Magiczna broń** (HR-026, cena × 50) staniała razem z bronią zwykłą: magiczny miecz o jednej
   właściwości z 100 ZK na 57 ZK. Jeśli to za tanio, mnożnik HR-026 trzeba podnieść — ale to decyzja
   o magii, nie o ekonomii.
