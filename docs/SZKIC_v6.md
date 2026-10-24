# Skarbiec Imperium — szkic aplikacji (2026-10-24)

Plan przeniesienia artefaktu „Skarbiec Imperium” do aplikacji na GitHub Pages
(`https://raksoprojects.github.io/Cennik_Warhammer_4ed/`).

## 0. Decyzje MG (2026-10-24)

- Interfejs: **Svelte 5 + TypeScript + PWA**, jak Postać i Generator NPC. Silnik zostaje w czystym JS z testami node.
- Node.js 24 LTS zainstalowany lokalnie (winget). Istniejące 34 testy silnika przechodzą.
- Zapisany kupiec: upływ czasu, transakcje graczy, zmiana osady i sytuacji, eksport do pliku, ręczna edycja towaru.
- Cennik uzupełniony o wszystkie brakujące bronie z `weapons.json` (także krasnoludzkie).

---

## 1. Stan zastany

| Co | Gdzie | Stan |
|---|---|---|
| Silnik (kupiec, zamówienie, targ, zarobki, czynsze, presety, ustawienia MG) | `skarbiec-imperium-v5/…/src/silnik.js` | gotowy, 34 testy |
| Testy spójności cennika (59 reguł + arbitraż) | `src/spojnosc.js`, `data/spojnosc*.json` | gotowe |
| Cennik v5.2: 365 pozycji, 303 z ceną podręcznikową (PG 245, PB 58), 62 pozycje kampanii | `data/cennik.json` | gotowy |
| 15 kupców, 6 osad, 8 koniunktur, rynek, czynsze, statusy, audyt 66 profesji | `data/*.json` | gotowe |
| Wzór działania UI | `reference/skarbiec_v5.html` | działa, jeden plik |
| Szkielet aplikacji (router, 1 widok, 9 zaślepek) | `src/app/` | niegotowy |

Z innych programów:

- `Generator_NPC/public/data/weapons.json` — 95 broni i 14 pancerzy z **polskimi** Zaletami i Wadami.
  To zamyka otwarte zadanie T11 (`data/bron_cechy.json`) bez czytania PDF-ów.
- `Generator_NPC/public/data/professions.json` — wyposażenie (trappings) każdego poziomu 104 profesji.
  To zamyka otwartą sprawę „wyposażenie profesji”: koszt startowego ekwipunku vs Dochód poziomu.
- Wzór budowy i hostingu: Vite 5 + Svelte 5 + TypeScript + PWA, workflow `deploy-pages`.

Porządki:

- Projekt leży dwa poziomy w głąb (`skarbiec-imperium-v5/skarbiec-imperium-v5/`). Przenoszę go do katalogu głównego repo.
- `AGENT_BRIEF.md`, `ANALIZA_v5.md`, `cennik_przeglad_v5.csv` w katalogu głównym to **starsze kopie**
  (v5.0; wewnątrz projektu jest v5.2). Usuwam je po przeniesieniu.
- Na tym komputerze nie ma Node.js. Bez niego nie uruchomię testów ani podglądu lokalnie.

---

## 2. Zakładki

Siedem zakładek zamiast dziesięciu. Na telefonie pasek zakładek przewija się poziomo i zostaje przyklejony u góry.

1. **Cennik** — wszystkie ceny w podziale na kategorie.
2. **Kupcy** — generator i „Moi kupcy” (zapisani, edytowalni, starzejący się w czasie).
3. **Zamówienie** — rzecz na miarę u wybranego kupca.
4. **Zarobki** — Statusy, kalkulator z rzutem, „ile Robót odłożyć”, koszt wyposażenia profesji.
5. **Czynsze** — najem × okres, kupno, zwrot.
6. **Edycja cen** — ustawienia MG (sekcja 5).
7. **Zasady i tabele** — modyfikatory, macierz rynku, audyt, źródła historyczne, zasady domowe. Podzakładki.

---

## 3. Cennik

Cennik dzieli się na sekcje według kategorii (Broń biała, Pancerze, Jedzenie…). Każda sekcja jest zwijana.
Nad sekcjami: wyszukiwarka (bez polskich znaków), filtry-chipy, przełącznik kolumn.

Kolumny (od lewej):

| Kolumna | Pole | Uwagi |
|---|---|---|
| Przedmiot | `nazwa` | + znaczniki: PG/PB/kampania, „bez źródła”, „nie w handlu”, „zmienione przez MG” |
| Podręcznik | `cena_raw_p` | przekreślona, gdy różna od bazowej |
| ×1 | `cena_ref_p` | szary drobny druk |
| Klasa | `klasa` + mnożnik | np. „broń ×2 · znak stanu ×1,5” |
| **Cena bazowa** | `cena_p` | pogrubiona, główna kolumna |
| Tyg. pracy | `cena_p / 165` | robotnik Brąz 3 |

Widok **„Ceny u kupców”** (przełącznik nad tabelą): zamiast Klasy i Tyg. pracy pokazuje cenę bazową ×
marża każdego z 15 kupców, dla wybranej osady i koniunktury. Tylko u kupców, którzy tym handlują.

Klik w wiersz rozwija szczegóły: podstawa historyczna, komentarz, Zalety i Wady (broń, pancerz),
Obciążenie, Dostępność, kto to robi, kto to sprzedaje.

---

## 4. Kupcy

### 4.1 Generator

Listy wyboru: kupiec (z marżą), osada („Altdorf (+30%)”), sytuacja („Wojna (broń … +80% · …)”).
Seed, **Losuj**, **PS z Targowania**. Link z seedem odtwarza tego samego kupca.

Tabela towaru: Towar · Sztuk · Podręcznik · Bazowa · **Jego cena** (+%) · Minimalna · Po targu · Odkupi za.
Klik w wiersz rozwija „Dlaczego tyle”: zapas, popyt, marża, preferencja, kaprys, osada, koniunktura, rynek, koszt.

**Zapisz** zamienia wygenerowany sklep w kupca z „Moich kupców”.

### 4.2 Moi kupcy — kupiec trwały

Zapisany kupiec przestaje być seedem. Zapisuje się **cały stan sklepu**, bo po każdej edycji seed już go nie odtworzy.

```js
{
  id, imie, dziwactwo, kupiec: 'zbrojmistrz', osada: 'altdorf', koniunktura: 'wojna',
  seed, utworzony: '2026-10-24', tydzien: 0,          // tydzień kampanii od założenia
  gotowka_p, notatka,
  towar: [{ id, sztuk, cena_p, cena_min_p, zapas, popyt, skladowe, reczna_cena: false }],
  dziennik: [{ tydzien, opis }]                       // „Sprzedał 2 miecze”, „Dokupił strzały”
}
```

Operacje:

| Operacja | Co robi |
|---|---|
| Zmień cenę / ilość | ręcznie, w komórce; cena ręczna ma znacznik i nie zmienia się przy przeliczeniu |
| Usuń pozycję | — |
| Dodaj z cennika | wyszukiwarka; cena liczona jak w generatorze |
| Przelosuj pozycję | nowy zapas, popyt i kaprys dla jednego wiersza |
| Dogeneruj | dolosowuje pozycje z rdzenia albo z wybranej kategorii |
| Przelosuj wszystko | nowy sklep, ta sama osoba (imię, dziwactwo, gotówka) |
| Zmień osadę / sytuację | przelicza ceny wszystkich nieręcznych pozycji |
| Gracz kupuje / sprzedaje | ilość i gotówka kupca się zmieniają, wpis w dzienniku |
| **Minęło N tygodni** | patrz 4.3 |

Przechowywanie: `localStorage` + eksport/import pliku JSON (jeden kupiec albo wszyscy).

### 4.3 Upływ czasu

Jeden przycisk: „Minęło [N] tygodni”. Wynik jest powtarzalny (seed kupca + tydzień).

1. **Sprzedaż.** Każda pozycja traci część sztuk co tydzień. Udział zależy od popytu:
   niski 10%, normalny 20%, wysoki 35%. Gotówka rośnie o sprzedane sztuki × jego cena.
2. **Zakupy.** Kupiec uzupełnia rdzeń do poziomu startowego, jeśli ma gotówkę.
   Płaci koszt nabycia (`koszt_p`), nie swoją cenę.
3. **Nowy towar.** Szansa na 1–2 nowe pozycje z bocznego asortymentu.
4. **Rynek.** Co 4 tygodnie nowy rzut zapasu, popytu i kaprysu dla pozycji bez ręcznej ceny.
5. Utrzymanie: kupiec wydaje 80% brutto swojego Statusu tygodniowo (HR-003).
6. Dziennik dostaje podsumowanie: co sprzedał, co dokupił, zmiana gotówki.

Procenty trafiają do `data/rynek.json` → `uplyw_czasu`, więc MG je zmieni w Edycji cen.

### 4.4 Propozycje do decyzji MG

- **Zamówienia w toku.** Zamówienie u zapisanego kupca dostaje termin i zaliczkę. Upływ czasu je kończy.
- **Stały klient.** Licznik transakcji z drużyną. Od progu kupiec schodzi z marży (np. −5%).
- **Notatka i miejsce.** Wolny tekst MG oraz grupowanie kupców po mieście.
- **Kopia kupca.** Ten sam kupiec w innym mieście jako punkt wyjścia.

---

## 5. Edycja cen (ustawienia MG)

Warstwy, od najsłabszej do najsilniejszej:

1. dane (`cennik.json`, ×1);
2. preset (`zalecany`, `baza`, `drogi`);
3. mnożnik klasy cenowej (`bron ×2`);
4. **mnożnik kategorii** (`Pancerze ×1,2`) — nowe;
5. **mnożnik grupy**: filtr w Cenniku → „×m dla widocznych” — zapisuje się jako mnożnik pozycji;
6. cena pojedynczej pozycji („4 ZK”, „15 s 6 p”, pensy) albo jej mnożnik;
7. **nowe pozycje** dopisane przez MG — nowe.

Do tego: osady, marże i skup kupców, koniunktury per kategoria, rynek, upływ czasu.

Każda zmiana działa od razu we wszystkich zakładkach. Panel pokazuje listę zmienionych cen i przycisk
**Sprawdź spójność**. Ustawienia: `localStorage`, eksport/import JSON, „Przywróć domyślne”.
Plik eksportu wgrany do `data/ustawienia.json` w repo staje się domyślnym cennikiem dla wszystkich.

---

## 6. Balans cennika

Bez podnoszenia cen „dla zasady”. Każda zmiana ze źródłem. Kolejność:

1. **Zalety i Wady broni** z `weapons.json`. Test: w tej samej grupie broń z większą liczbą Zalet nie jest
   tańsza, chyba że ma `wyjatek` (znak stanu, egzotyka). Raport naruszeń idzie do MG, bez samodzielnych poprawek.
2. **Wyposażenie profesji.** Koszt ekwipunku z `professions.json` vs Dochód poziomu. Sygnał błędu:
   Uczeń, który nie odłoży na swoje narzędzia w rozsądnym czasie.
3. **Braki.** Bronie bez wpisu w cenniku: puklerz, tarcza duża, nadziak, broń krasnoludzka (8 pozycji),
   hełm, hełm otwarty, kamień.
4. Testy spójności i arbitrażu przechodzą po każdej zmianie.

---

## 7. Wygląd

- Ciemne tło (`#15171c`), tekst `#e8e6e1` (kontrast > 12:1), złoto akcentu `#d9b45a` tylko na ceny i aktywną zakładkę.
- Czcionka 16 px, cyfry tabelaryczne (`font-variant-numeric: tabular-nums`), ceny wyrównane do prawej.
- Podpowiedzi: ikona „?” przy nagłówkach i liczbach. Klik otwiera dymek, drugi klik albo klik obok zamyka.
  Bez najeżdżania myszą — na telefonie hover nie istnieje.
- Dłuższe objaśnienia: `<details>` zwijane, domyślnie zamknięte.

Telefon (< 640 px):

- tabela zamienia się w karty: nazwa + cena bazowa + jego cena w pierwszej linii, reszta po rozwinięciu;
- przyciski i komórki dotykowe ≥ 44 px;
- strona nigdy nie przewija się na boki;
- PWA: aplikacja instaluje się na ekranie telefonu i działa bez sieci.

Druk: karta sklepu na A4, bez nawigacji i formularzy.

---

## 8. Etapy

| # | Etap | Gotowe, gdy |
|---|---|---|
| 1 | Przeniesienie projektu, Node, build, Pages | pusta aplikacja działa pod adresem GitHub Pages |
| 2 | Cennik + rozwijane wiersze + karty na telefonie | 365 pozycji, filtry, sekcje; „Miecz”: 1 ZK 3 s ×1, bazowa 3 ZK 9 s |
| 3 | Edycja cen (warstwy 1–7) | konie bojowe ×2 → rumak 1100 ZK wszędzie, bez przeładowania |
| 4 | Generator kupca | seed 48213 zbrojmistrza w Altdorfie w wojnie = Erika Nachtigall, jak w `skarbiec_v5.html` |
| 5 | Moi kupcy: zapis, edycja, transakcje | kupiec po edycji wraca po odświeżeniu strony |
| 6 | Upływ czasu + testy | 4 tygodnie: sprzedaż, dokupienie, dziennik; ten sam wynik przy powtórzeniu |
| 7 | Zamówienie, Zarobki, Czynsze, Zasady i tabele | kryteria z `TASKS.md` T4–T8 |
| 8 | Balans: cechy broni, wyposażenie profesji, braki | raport dla MG |
| 9 | Druk, PWA, telefon 390 px | bez przewijania na boki |
