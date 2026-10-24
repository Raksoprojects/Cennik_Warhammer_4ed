# Skarbiec Imperium

Narzędzie ekonomiczne do kampanii WFRP 4 ed. (wyd. polskie). Zawiera:

- cennik kampanii (**365 pozycji**, ceny bazowe = ceny wytwórcy, preset „zalecany” v5.2);
- zarobki wg Statusu z zasadami domowymi;
- generator kupców (marża, osada, koniunktura, popyt i zapas);
- zamówienia na miarę, skup i targowanie;
- audyt Statusu profesji i tabelę danych historycznych;
- koszty magicznych przedmiotów.

Odtworzone z artefaktu „Skarbiec Imperium” (claude.ai, 2026-09-16) i uzupełnione o zasady domowe kampanii.

Aplikacja: **https://raksoprojects.github.io/Cennik_Warhammer_4ed/** (działa też offline jako PWA, na telefonie i komputerze).

## Wersja v6 (2026-10-24) — aplikacja

Svelte 5 + TypeScript + Vite + PWA, jak Program_postac_GUI i Generator_NPC. Ciemny motyw, klikane podpowiedzi „?”,
zwijane objaśnienia; na telefonie wiersze tabel zamieniają się w karty.

Zakładki:

| Zakładka | Co robi |
|---|---|
| Cennik | 376 pozycji w zwijanych kategoriach: podręcznik (RAW), ×1, klasa, cena bazowa, tygodnie pracy. Filtry, „ceny u kupca” (marża × osada × sytuacja), klik w wiersz: źródło, Zalety i Wady broni, kto sprzedaje, zmiana ceny. Mnożnik dla wszystkich widocznych pozycji. |
| Kupcy | Generator (seed w adresie) i **baza kupców**: nazwa, grupa (np. miasto), notatka, modyfikator MG cen (taniej/drożej), przenosiny i zmiana sytuacji, ręczna cena i ilość, dodawanie towaru (spoza asortymentu tylko po potwierdzeniu), dogenerowanie, przelosowanie, transakcje drużyny, zamówienia w toku z terminem i zaliczką, **upływ czasu** (sprzedaż, dokupienie, nowy towar), dziennik, eksport/import pliku. |
| Zamówienie | wycena na miarę: robi / sprowadza / odmawia (i do kogo odsyła). |
| Zarobki | Statusy, kalkulator z rzutem, „ile Robót odłożyć”, jałmużna. |
| Czynsze | najem × okres w osadzie i sytuacji, kupno. |
| Edycja cen | preset, mnożniki klas i kategorii, ceny pozycji, nowe pozycje MG, osady, marże, sytuacje, rynek i upływ czasu, spójność, JSON / eksport / import. |
| Zasady i tabele | wzór ceny, marże, osady, sytuacje, macierz rynku, zasady domowe, audyt profesji, źródła historyczne. |

Kod: `src/silnik.js` (ceny, generator), `src/kupcy_trwali.js` (zapisany kupiec: wycena na żywo, edycja, czas, zamówienia),
`src/spojnosc.js` (testy cennika), `src/lib/` (stan, formatowanie), `src/widoki/`, `src/komponenty/`.

Dane v6 (`narzedzia/dodaj_v6.py`):

- 11 broni z podręczników ras (Krasnoludy s. 93–94, Wysokie Elfy s. 31) z ceną RAW; poziom ×1 w tej samej proporcji do RAW
  co ludzki odpowiednik. Uwaga: dodatkowe pozycje w kategoriach broni zmieniają sklepy wylosowane starymi seedami
  u kupców, którzy handlują bronią.
- `data/bron_cechy.json`: grupa, obrażenia, zasięg, Zalety i Wady każdej broni z `Generator_NPC/public/data/weapons.json`.
  „Sprawdź spójność” pokazuje pary, w których broń z lepszym bilansem cech jest tańsza (raport, bez automatycznych zmian).
- `data/rynek.json` → `uplyw_czasu`: parametry upływu czasu dla zapisanych kupców.
- Ustawienia MG: nowe pola `kategorie` (mnożnik kategorii) i `nowe` (pozycje dopisane przez MG).

## Wersja v5 (2026-10-24)

**Agent w VS Code:** zacznij od `AGENTS.md` → `docs/AGENT_BRIEF.md` → `TASKS.md`.
Działający wzór interfejsu: `reference/skarbiec_v5.html` (otwórz w przeglądarce).

- `data/cennik.json` = **v5-zalecany** (cena bazowa w `cena_p`, poziom ×1 w `cena_ref_p`). Preset „zalecany” po
  analizie wszystkich pozycji: mnożniki bez podstawy w danych zniknęły (codzienne 1,5→1,2; palna 1,5→1;
  alchemia 1,5→1; prestiż 3→1,5; konie robocze 1,5→1; pancerz skórzany 2→1,5). 168 pozycji tańszych, 0 droższych.
- `data/klasy_cenowe.json`: presety `zalecany` (domyślny), `zalecany_v4`, `baza`, `drogi` + uzasadnienie każdej klasy.
- `data/ustawienia.json` + `zastosujUstawienia()` w silniku: MG zmienia mnożniki, ceny pozycji, osady, koniunktury,
  kupców i rynek na żywo, bez ruszania danych.
- Silnik: **cena minimalna** kupca (dolna granica targowania), **osobowość kupca** (preferencja rdzeń/boczne,
  kaprys 1k10, granice −15% … +20%), **etykiety z modyfikatorem** („Altdorf (+30%)”, „Wojna (… +80% …)”).
- `src/spojnosc.js`: testy spójności wspólne dla node i aplikacji.
- Analiza: `docs/ANALIZA_v5.md`, tabele `docs/analiza_v5/*.csv`. 34 testy przechodzą.
- Szkielet aplikacji: `package.json`, `vite.config.js`, `index.html`, `src/app/`.

## Wersja v3 (2026-10-23)

Cennik `data/cennik.json` jest **zatwierdzoną** wersją v3. Co weszło:

- propozycja v2 w całości (94 zmiany — korekta płac angielskich wg stulecia, czynsze o ⅔ w dół);
- 30 pozycji ze źródeł krakowskich (przyprawy, zboże, sukno, drób, oliwa, świece);
- dwie korekty własne: furmanka 3 → 4 ZK, barka 150 ZK z adnotacją, że to górna granica;
- **pola `typ` i `podtyp`** — nocleg, usługi i nieruchomości przestały być towarem
  (wcześniej kramarz miał na stanie 37 noclegów i odkupywał przespaną noc za 4 p);
- **mnożnik czynszu dla koniunktury** — zaraza ×0,6, oblężenie ×2,0, nowy kryzys mieszkaniowy ×3,0;
- **wyjątki od limitu wsi** dla żywego inwentarza i podstawowej żywności;
- 9 nowych reguł spójności i 4 testy strukturalne.

Szczegóły i uzasadnienia: `docs/PRZEGLAD_v3.md`. Materiały do zbudowania interfejsu: `docs/APLIKACJA.md`.

## Wersja v4 (2026-11) — poziom cen i arbitraż

- `data/cennik.json` = **v4-baza**: poprawki spójności na poziomie ×1 (koc, siennik, prześcieradło,
  worki, okrycia tańsze od własnego materiału; nowe: sukno szare, płótno zgrzebne, olej do lampy;
  nóż przeniesiony do narzędzi). Każda pozycja ma `klasa` (klasa cenowa) i `cena_ref_p` (cena bazowa).
- Dwa warianty poziomu cen do wyboru: `propozycja/cennik_v4_drogi.json` (najbliżej ×3) i
  `propozycja/cennik_v4_zalecany.json`, plus `czynsze_v4.json` i `koniunktura_v4.json`.
- `zastosujPreset()` w silniku nakłada mnożniki klas w locie (`propozycja/klasy_cenowe_v4.json`).
- Generator liczy limity i ilości od `cena_ref_p`, więc poziom cen nie wycina asortymentu.
- Nowe testy: `test/arbitraz.test.mjs` (materiał ≤ produkt, pełne ≥ puste naczynie, rodziny rzeczy,
  tusze, biżuteria vs kruszec, budżet utrzymania, karczma vs najem, zwrot z kupna, test rzemieślnika).
- Analiza z za i przeciw: `docs/ANALIZA_v4.md`.

## Zawartość

```
data/        wszystkie liczby i teksty (JSON) – tu się edytuje ceny i zasady; spojnosc.json = 59 reguł
src/silnik.js   logika obliczeń, bez DOM i zależności (ES module)
test/        testy: zgodność z oryginałem + spójność cennika (node --test test/*.test.mjs)
propozycja/  cennik_v2.json, czynsze_v2.json, zmiany.json, nowe_pozycje.json – ZATWIERDZONE, weszły do v3
narzedzia/   zrodla.py (przeliczenie źródeł na dniówki), propozycja.py (buduje v2)
docs/
  SPECYFIKACJA.md        co robi program, krok po kroku, z wzorami
  PRZEGLAD_v3.md         weryfikacja analizy, defekty, odpowiedzi na otwarte decyzje  ← zacznij tutaj
  APLIKACJA.md           stack, struktura, widoki, kolejność prac, kryteria odbioru
  ANALIZA_ZRODEL.md      cennik vs 8 źródeł historycznych + propozycja v2 (przyjęta)
  ANALIZA_CEN.md         pierwsza wersja przeglądu (zastąpiona)
  ZASADY_DOMOWE_ekonomia.md  HR-018, 021–024, 026
reference/
  skarbiec_oryginal.html  oryginalny artefakt (wygląd, teksty sekcji)
  dane_oryginal.json      dane z artefaktu (302 pozycje) – tylko do testów
```

## Jak tego użyć

- **Interfejs:** do napisania — patrz `docs/APLIKACJA.md`. Szkic w `reference/skarbiec_oryginal.html`; program czyta `data/*.json`
  i wołać funkcje z `src/silnik.js`:
  - `generujKupca`, `wycenZamowienie`, `targuj`;
  - `rzutDochodu`, `sredniDochod`, `jalmuzna`;
  - `cenaMagiczna`, `mon`.
- **Hosting:** GitHub Pages wystarczy (statyczna strona, `fetch('data/cennik.json')`).
- **Zmiana ceny:** edytuj `cena_p` w `data/cennik.json` (w pensach: 1 ZK = 240 p, 1 s = 12 p).
- **Nowy kupiec / osada / koniunktura:** dopisz wpis w odpowiednim JSON; silnik go podchwyci.

## Zgodność z oryginałem

Testy porównują silnik z oryginałem uruchomionym w przeglądarce:

- 1680 wygenerowanych kupców: 15 archetypów × 6 osad × 7 koniunktur, kilka seedów – ten sam seed daje tego samego
  kupca, towar, ilości i ceny;
- 300 zamówień na miarę.

Różnice celowe:

- Wada = ×½ (HR-024; w oryginale ¼);
- cennik 331 pozycji (w oryginale 302);
- wieś trzyma tylko Dostępność Powszechną (zasada była opisana, ale niezaimplementowana) – wyłączysz to przez
  `stosujDostepnosc: false`.
