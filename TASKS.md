# TASKS — kolejność prac nad aplikacją

> **Stan v6 (2026-10-24):** T1–T10 zrobione w Svelte 5 (`src/widoki/`, opis w `README.md`). Zamiast `src/app/*.js`
> z `montuj(el, ctx)` są komponenty Svelte. T11: cechy broni uzupełnione z `Generator_NPC` (`narzedzia/dodaj_v6.py`),
> test `test/bron_cechy.test.mjs` wypisuje raport dla MG. Doszła baza kupców z upływem czasu (`src/kupcy_trwali.js`).
> Kryteria z seedem 48213 („Erika Nachtigall”) nie obowiązują: 11 nowych broni zmieniło pulę towaru zbrojmistrza.
> Otwarte: T13 (ładne zaokrąglanie ceny kupca) — czeka na decyzję MG.

Przeczytaj najpierw `AGENTS.md` i `docs/AGENT_BRIEF.md`. Wzór działania każdego widoku: `reference/skarbiec_v5.html`
(otwórz w przeglądarce). Szczegóły widoków: `docs/APLIKACJA.md`.

Każde zadanie kończy się czymś, co działa, zielonym `npm test` i commitem `T<n>: …`.
Odhaczaj `[x]` w tym pliku.

---

## [x] T0. Szkielet (zrobione)

`package.json`, `vite.config.js`, `index.html`, `src/app/main.js` (router po `#hash`), `src/app/dane.js`,
`src/app/format.js`, `src/app/ustawienia.js`, przykładowy widok `src/app/widoki/cennik.js`.

Sprawdź: `npm install && npm run dev` pokazuje 10 zakładek, Cennik działa, reszta to zaślepki.

**Uwaga:** szkielet był sprawdzony w przeglądarce bez Vite (w sesji, w której powstał, rejestr npm był niedostępny).
Pierwsze `npm install && npm run build` zrób od razu; jeśli wersja `vite` w `package.json` nie istnieje, weź najbliższą 5.4.x i zacommituj `package-lock.json`.

---

## [ ] T1. Tabela wielokrotnego użytku — `src/app/ui/tabela.js`

Wyszukiwarka (`norm()` z silnika), filtry-chipy, render wierszy, licznik „N z M”, komunikat „Nic nie pasuje”.
Przenieś na nią widok Cennik.

**Gotowe, gdy:** Cennik, Historia i Audyt używają tego samego komponentu; wyszukiwanie „kaplon” znajduje „Kapłon”.

## [ ] T2. Cennik

Kolumny: Przedmiot (+ źródło, kategoria, typ, znaczniki) · RAW (przekreślony, gdy różny) · ×1 · Klasa i jej mnożnik ·
**Cena bazowa** · Tyg. pracy (÷ 165 p) · Podstawa historyczna · Komentarz.
Filtry: kategoria, typ, „zmienione w v5”, „nadpisane w ustawieniach”, „bez źródła”, „nie w handlu”, „zmienione wobec RAW”.

**Gotowe, gdy:** 365 pozycji; „Miecz” pokazuje ×1 = 1 ZK 3 s, klasa broń ×2 (+ znak stanu ×1,5), cena bazowa 3 ZK 9 s;
filtr „bez źródła” daje 179 pozycji (pusta `podstawa_hist`).

## [ ] T3. Kupiec — najważniejszy widok

Listy wyboru: kupiec (z marżą w nawiasie), osada (`etykietaOsady` → „Altdorf (+30%)”), sytuacja
(`etykietaKoniunktury(d, k, { krotko: true })`). Pod listami pełna etykieta sytuacji (bez `krotko`).
Seed, **Losuj**, pole **PS z Targowania**.

Tabela (trzy ceny po kolei: podręcznik → cennik → kupiec): Towar · Sztuk · Podręcznik (RAW, bez modyfikacji) · **Cena bazowa** (cennik, bez modyfikatorów kupca) · **Jego cena** (+ % zmiany) · **Minimalna** (+ „wyprzedaż”) ·
Po targu (gdy PS > 0, `targuj` z `cena_min_p`) · Odkupi za · Dlaczego tyle
(zapas, popyt, modyfikator testu, marża, preferencja rdzeń/boczny, kaprys z opisem, osada, koniunktura, rynek, koszt).

Seed w adresie: `#kupiec?k=zbrojmistrz&o=altdorf&n=wojna&s=48213`. Zapis kupca do „Moi kupcy” (localStorage, try/catch).

**Gotowe, gdy:**
- link `#kupiec?k=zbrojmistrz&o=altdorf&n=wojna&s=48213` daje kupca **Erika Nachtigall** z gotówką 22 ZK
  i towarem za 106 ZK 3 s; wiersz Bomba: podręcznik 3 ZK, bazowa 6 ZK, jego 22 ZK 2 p, minimalna 14 ZK 14 s 10 p
  — tak samo jak w `reference/skarbiec_v5.html`;
- przy 3 PS cena po targu Bomby = 15 ZK 8 s 1 p (−30%, powyżej minimalnej);
- nagłówek sklepu pokazuje **gotówkę** i **wartość towaru**; skup ponad gotówkę ma znacznik „brak gotówki”;
- kramarz nigdy nie ma więcej niż 1 namiotu;
- iloczyn rozbicia × cena bazowa = jego cena (±1 p) dla każdego wiersza;
- w żadnym sklepie nie ma noclegu, posiłku, stajni, czynszu ani najmity.

## [ ] T4. Zamówienie na miarę

Pole z podpowiedziami (towary), jakość, **Wyceń**. Rozbicie: cena bazowa · jakość · marża · osada (z etykietą) ·
koniunktura (dla kategorii) · narzut · razem · zaliczka · termin. Trzy stany: wykonuje / sprowadza / odmowa (do kogo odsyła).

**Gotowe, gdy:** kowal odmawia zrobienia księgi i odsyła do Księgarza.

## [ ] T5. Zarobki i kalkulator

Tabela Statusów, kalkulator: Status + Majętny + **Rzuć** obok średniej. „Ile Robót odłożyć” czyta ceny z cennika
**po nałożeniu ustawień** (`kalkulator.json` to tylko lista id).

**Gotowe, gdy:** Srebro 3 bez Majętnego: średnio 16 s 6 p netto; kolczuga 20 ZK = 24 Roboty.

## [ ] T6. Czynsze

Osada i sytuacja w listach z modyfikatorem czynszu w nawiasie („Zaraza (czynsz −40%)”).
Tabela najmu × okres, kupno, „zwrot w N lat”.

**Gotowe, gdy:** mieszkanie mieszczańskie / miesiąc w Marienburgu: normalna 2 ZK 18 s, zaraza 1 ZK 14 s 10 p,
kryzys mieszkaniowy 4 ZK 18 s 7 p.

## [ ] T7. Ustawienia MG — edycja na żywo

To jest odpowiedź na „chciałbym móc modyfikować rzeczy na bieżąco”. Wzór: zakładka „Ustawienia MG” w `reference/skarbiec_v5.html`.

- wybór presetu; premia znaku stanu;
- tabela klas: mnożnik (pole liczbowe), liczba pozycji, tag źródła i tekst z `klasy_cenowe.uzasadnienia`;
- osady (mnożnik), kupcy (marża, skup), rynek (preferencje, granice kaprysu, cena minimalna), koniunktura (mnożnik każdej kategorii i czynszu);
- cena jednej pozycji (parser „4 ZK”, „15 s 6 p”, pensy), lista nadpisań z przyciskiem usuń;
- podgląd „zmienione ceny względem cennika v5”;
- JSON: zastosuj, eksport do pliku, import z pliku, przywróć domyślne;
- **Sprawdź spójność** → `sprawdzWszystko` z `src/spojnosc.js`, błędy na czerwono, ostrzeżenia osobno;
- znacznik „własne ustawienia” w nagłówku, gdy coś jest zmienione.

Każda zmiana → `zastosujUstawienia(daneBazowe, ust)` → przerysowanie **wszystkich** widoków.

**Gotowe, gdy:**
- konie bojowe ×2 → rumak 1100 ZK w cenniku i u handlarza koni, bez przeładowania strony;
- najem ×3 → czynsze w widoku Czynsze rosną, a „Sprawdź spójność” zgłasza błędy (karczma vs najem, budżet);
- eksport → import tego samego pliku daje identyczny stan;
- po „Przywróć domyślne” lista zmian jest pusta.

## [ ] T8. Modyfikatory, Audyt, Historia, Zasady

Tabele z wyszukiwarką. Modyfikatory pokazują wzór ceny kupca i ceny minimalnej, tabele marż, osad, koniunktur,
macierzy, preferencji i kaprysu — **czytane z danych po ustawieniach**, nie wpisane na sztywno.

## [ ] T9. Druk i telefon

`@media print`: karta sklepu na A4 bez nawigacji i formularzy. 390 px szerokości: strona nie przewija się na boki,
tabele przewijają się we własnym kontenerze.

## [ ] T10. GitHub Pages

`.github/workflows/pages.yml` jest gotowy. Włącz Pages (Settings → Pages → GitHub Actions).

**Gotowe, gdy:** aplikacja działa pod publicznym adresem, link z seedem otwiera tego samego kupca.

---

## Zadania wymagające MG albo podręcznika

## [ ] T11. Zalety i Wady broni (potrzebne PDF-y)

Uzupełnij `data/bron_cechy.json` z podręcznika (s. 294–295) i „Pod Bronią” (s. 91–93) — „Pod Bronią” ma pierwszeństwo.
PDF-y kładzie MG w `reference/pdf/` (w `.gitignore`, **nie commitować**). Nazwy wyłącznie z polskiego wydania.
Potem dopisz test `test/bron_cechy.test.mjs`: w obrębie jednej `grupy` broni, jeśli A ma więcej (Zalety − Wady) niż B,
to cena A ≥ cena B, chyba że A lub B ma `wyjatek`. Raport naruszeń → pokaż MG, **nie poprawiaj cen sam**.

## [x] T12. Decyzje cenowe z analizy v5

Rozstrzygnięte przez MG 2026-10-24 i wprowadzone w danych (v5.1): pojazdy ×1,5, łuk elfi = 5× łuk długi,
konie bojowe zostają ×1,5, RAW widoczny wszędzie. Nowe decyzje MG — tym samym trybem: `narzedzia/buduj_v5.py` → testy → analiza.

## [ ] T13. (opcjonalnie) Ładne zaokrąglanie ceny kupca

Dziś „130 ZK 18 s 11 p”. Propozycja: przy wyświetlaniu ceny kupca zaokrąglać jak `ladna()` w `zastosujPreset`
(< 1 ZK do 6 p, < 10 ZK do szylinga, wyżej do 5 s). Tylko w UI albo za flagą — **test `zgodnosc` nie może się zmienić**.
Zapytaj MG, zanim zrobisz.
