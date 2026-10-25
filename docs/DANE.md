# Gdzie co jest — mapa danych dla MG

Wszystkie liczby i zasady są w plikach `data/*.json`. Aplikacja czyta je przy budowie, więc zmiana w pliku
działa po wypchnięciu na GitHub (albo od razu w `npm run dev`). Kwoty zawsze **w pensach** (1 ZK = 20 s = 240 p).

Dwie drogi zmian:

- **Na próbę, u siebie:** zakładka **Edycja cen** w aplikacji. Zapisuje się w przeglądarce, eksport daje plik.
- **Na stałe, dla wszystkich:** wgraj eksport do `data/ustawienia.json` albo zmień plik z tabeli poniżej.
  Zmian, które robią skrypty w `narzedzia/`, nie poprawiaj ręcznie — następne uruchomienie skryptu je nadpisze;
  zmień wtedy skrypt (`narzedzia/dane_v6b.py` itd.).

## Pliki

| Co | Plik | Pole | Uwagi |
|---|---|---|---|
| Ceny przedmiotów | `data/cennik.json` | `cena_p` (bazowa), `cena_ref_p` (×1), `cena_raw_p` (podręcznik) | `cena_p` = `cena_ref_p` × mnożnik klasy. Na stałe zmieniaj `cena_ref_p` przez skrypt albo `data/ustawienia.json → pozycje`. |
| Czym handluje sklep | `data/cennik.json` | `branze` (tagi pozycji) | np. Beczka → `pojemniki`. Lista tagów: `narzedzia/dane_v6b.py`, słownik `B`. |
| … a który kupiec co bierze | `data/kupcy.json` | `rdzen`, `boczne` (kategorie), `branze` ({kategoria: [tagi]}) | Bez wpisu w `branze` kupiec bierze całą kategorię. |
| Dostępność przedmiotu | `data/cennik.json` | `dostepnosc` | Powszechna / Ograniczona / Rzadka / Egzotyczna. |
| Szanse Dostępności w osadzie | `data/rynek.json` | `dostepnosc.tabela` | PG s. 290: wioska / miasteczko / miasto. Typ osady: `data/osady.json → dostepnosc`. |
| Towar krasnoludzki, elfi | `data/cennik.json` | `pochodzenie` | U kupca innej rasy szansa × `rynek.dostepnosc.obce_pochodzenie` (0,3). Kupiec ma `rasa`. |
| Zamówienie rzeczy rzadkiej | `data/rynek.json` | `dostepnosc.zamowienie` | Próg szansy, dodatkowe tygodnie, narzut; egzotyk we wsi — odmowa. |
| Klasy cenowe (×2 dla broni itd.) | `data/klasy_cenowe.json` | `presety.zalecany.mnozniki`, `uzasadnienia` | Edycja cen → Mnożniki klas. |
| Kupcy | `data/kupcy.json` | `marza`, `skup`, `limit_p`, `robota`, `robota_pozycje`, `towar_tyg`, `gotowka_tyg`, `opis` | Edycja cen → Osady i kupcy. |
| Szansa na Zalety / Wady w sklepie | `data/kupcy.json` | `jakosc: {zalety, wady}` (0–1), `jakosc_kat: {kategoria: {zalety, wady}}` | np. kramarz: ubrania z Wadami 70%. Edycja cen → kolumny Zalety % / Wady %. |
| Mnożniki Zalet i Wad | `data/rynek.json` | `jakosc.za_zalete` (1,6), `jakosc.za_wade` (0,6), `jakosc.zalety`, `jakosc.wady` | `jakosc.kategorie` = kategorie, w których generator losuje jakość; `bez_jakosci` = tagi wyłączone. |
| Targowanie | `data/rynek.json` | `targowanie.za_ps` (0,04), `max` (0,24), `max_zamowienie` | Edycja cen → Rynek. |
| Marża rdzeń / boczne, kaprys | `data/rynek.json` | `preferencje`, `kaprys` | |
| Zapas × popyt | `data/rynek.json` | `macierz_zapas_x_popyt`, `zapas`, `popyt` | |
| Upływ czasu kupców | `data/rynek.json` | `uplyw_czasu` | sprzedaż / tydzień, dokupienie, nowy towar, sufit gotówki. |
| Zamówienia | `data/rynek.json` | `zamowienie` | narzuty, zaliczka, materiał zamawiającego (0,5). |
| Osady | `data/osady.json` | `mnoznik`, `limit_p`, `dostepnosc`, `limit_omijaja_podtypy` | |
| Sytuacje (koniunktura) | `data/koniunktura.json` | `koniunktury[].kategorie[kat] = {cena, popyt}`, `czynsz.mnoznik` | Edycja cen → Sytuacje. Nową sytuację dopisz jako kolejny wpis. |
| Zarobki wg Statusu | `data/statusy.json` | `wzory`, `poziomy[].opis`, `majetny` | |
| Pozycja / Dochód profesji | `data/audyt.json` | `poziomy[].poz`, `doch`, `w`, `powod` | Puste = jak w podręczniku (`raw`). |
| Czynsze | `data/czynsze.json` | `najem`, `kupno` | Muszą się zgadzać z cennikiem (test). |
| Cechy broni | `data/bron_cechy.json` | `zalety`, `wady`, `grupa` | Z `Generator_NPC/public/data/weapons.json`. |
| Imiona, dziwactwa kupców | `data/nazwy.json` | | Pierwsze dziwactwo (stare, z artefaktu). |
| Osobowość kupca | `data/postacie.json` | `charaktery` (wagi), `motywacje`, `cechy_kupieckie` (z `efekt`), `wyglad`, `znaki`, `manieryzmy`, `potrzeby`, `sekrety`, `dziwactwa`, `imiona`, `nazwiska` | Pole `charakter` (dobry / neutralny / zly) — bez niego pasuje do każdego. Efekty cechy: `ceny`, `skup`, `targowanie`, `bez_targu`, `trefne`, `oszust`, `gotowka`, `termin`. Nazwy Motywacji wg Ekranu MG, cechy kupieckie wg Poradnika Staroświatowca (tab. 3-7); opisy własne. |
| Towar trefny | `data/rynek.json` → `trefne`; `data/kupcy.json` → `trefne`, `trefne_wagi` | rodzaje (kradziony, podróbka, ukryta Wada, oszukana miara), skala oszustwa i trudność Testu Wyceny (Poradnik s. 41), szansa, że kupiec wie | Paser 75% (głównie kradziony), domokrążca 12%, reszta zwykle 1–6%; Szarlatan ≥ 60%, Skrupulatnie uczciwy 0%. |
| Twoje bieżące zmiany | `data/ustawienia.json` | jak eksport z Edycji cen | Puste = cennik domyślny. |

Po każdej zmianie w `data/` uruchom `npm test` — testy spójności pilnują arbitrażu (np. koc tańszy niż jego sukno).
