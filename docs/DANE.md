# Do rozpatrzenia przez MG (przegląd 2026-10-26)

Rozbieżności i niejasności znalezione w przeglądzie aplikacji. Każdy punkt: co jest nie tak → propozycja.

**Stan po v6d (2026-10-30):** rozwiązane 3 (pora z daty), 5 (Middenheim = metropolia, decyzja MG), 6 (Altdorf
i Marienburg działają), 8 (wahania zmieniają cenę i Dostępność), 9 (strefa jako odchylenie od średniej Imperium),
10 (Egzotyczne: metropolia 3%, Marienburg 6%, gdzie indziej 0,1%), 11 (Zalety rzadsze we wsi), 13 (krasnolud zostaje
wszędzie, jego towar we wsi jak Ograniczony), 14 (nielegalne rozszerzone, broń prochowa legalna), 15 (konie),
17 (dane do Kompendium: `docs/KOMPENDIUM_DANE.md`), 21 (dymek przypomnienia), 23 (dopisek w kalkulatorze).
Otwarte: 1, 2 (propozycja czynszów czeka na zgodę), 4 (Nuln może być droższy — zostaje), 7, 12, 16, 18, 19, 20, 22.

**Czas i kalendarz**

1. **Tydzień ma 8 dni, a kotwica cen liczy 6 dniówek.** Robotnik: 27,5 p × 6 = 165 p brutto „tygodniowo”. Tydzień
   imperialny ma 8 dni (Festag wolny → 7 dni pracy = 192,5 p). Robota, czynsze tygodniowe i upływ czasu kupca liczą już
   tydzień 8-dniowy. → Albo kotwica = 7 dniówek (wszystkie zarobki +17%), albo przyjąć, że „tydzień pracy” to 6 dni roboczych.
2. **Czynsz miesięczny jest tani wobec tygodniowego.** Miesiąc ma 33 dni (ponad 4 tygodnie), a czynsz za miesiąc to 2,7–3,7×
   tygodniowego. → Zostawić (najem długoterminowy taniej) albo podnieść miesiąc do ok. 3,5–4×.
3. **Pora roku ustawiona ręcznie nie zmienia daty.** Gdy kupiec ma datę, ręczna zmiana pory zostaje nadpisana przy upływie
   czasu. → Ukrywać wybór pory, gdy data jest ustawiona.

**Osady i ceny lokalne**

4. **Nuln (×1,32) i Talabheim (×1,26) są droższe niż ogólna „Metropolia” (×1,2), a Nuln droższy niż Altdorf (×1,3).**
   Zamożność 5 mnoży się na typ osady. → Ustalić hierarchię: czy Altdorf ma być najdroższy w Imperium poza Marienburgiem.
5. **Middenheim wg Poradnika ma 15 000 mieszkańców, więc wychodzi „miasto”,** a ogólna osada nazywa się „Metropolia
   (Nuln, Middenheim)”. → Wybrać: liczba z Poradnika albo Middenheim jako metropolia.
6. **Flaga Altdorfu „Rzadkie o stopień łatwiej” nie działa** (`osady.json → rzadkie_latwiej` nie jest używane w silniku),
   tak samo opis Marienburga „wszystko z importu”. → Wdrożyć: w Altdorfie Rzadka liczy się jak Ograniczona, w Marienburgu
   import (Egzotyczne?) dostępny.
7. **Pora roku nakłada się na sytuację.** „Zamknięte szlaki (bandyci, lód)” + zima liczy zimę dwa razy. → Opisać w sytuacji
   „bez zimy” albo zostawić MG.
8. **Wahania rynku to mój szacunek:** hossa ceny ×1,1 i popyt +1, bessa ×0,9 i popyt −1. W Poradniku Rynek Byka zmienia
   dostępność, nie cenę. → Potwierdzić albo zamienić na zmianę Dostępności.
9. **Strefa handlowa → kategorie Skarbca to uproszczenie** (np. broń biała = „wyroby metalowe”). Mnożniki stopni ×1,4…×0,85
   to szacunek. → Przejrzeć tabelę w Zasady → Handel.

**Asortyment i dostępność**

10. **20 rzeczy Egzotycznych nigdy nie leży na półce** (flamberg, arkebuz, muszkiet hochlandzki, broń pistoletowa, księga
    magii, lusterko, warsztat…), są tylko na zamówienie (PG s. 290). → Zostawić albo dopuścić je u rusznikarza
    i płatnerza w metropoliach (np. 5%).
11. **Jakość nie zmienia Dostępności w generatorze.** PG: każda Zaleta o stopień rzadsza. Mistrz cechu we wsi może mieć
    przedmiot Wyśmienity 2. → Wdrożyć albo zostawić.
12. **15 pozycji bez Dostępności** (zboże, mięso, nowe pozycje kampanii) liczy się jak Powszechne. → Uzupełnić.
13. **Kupiec krasnoludzki pojawia się wszędzie, także we wsi** (śr. 35 pozycji). → Ograniczyć do metropolii i stref
    krasnoludzkich (Stary Trakt, Trakt do Zhufbaru).
14. **Nielegalne są tylko 4 narkotyki i trucizny.** Czy dodać: Księżycowy kwiat, Nocny cień, Księgę (magia) dla
    nie-czarodziejów, broń prochową bez pozwolenia? → Decyzja MG.
15. **Lekki koń bojowy (262 ZK) ma Dostępność Powszechną**, rumak Ograniczoną. → Ograniczona.
16. **Sufit gotówki kupca (2× startowa) i sprzedaż 5/12/25% tygodniowo** to szacunki. → Sprawdzić przy stole.

**Dokumenty i spójność**

17. **Kompendium MG (PDF) jest nieaktualne wobec aplikacji:** targowanie 10%/PS (jest 4%), jakość ×2 / ×½ (jest ×1,6 /
    ×0,6), pełna płytówka 48 ZK (jest 96 ZK), mistrzowska ×4 (jest ×2,56). → Wygenerować Kompendium na nowo z danych.
18. **Utrzymanie:** Kompendium (PG s. 51) „połowa Statusu dziennie”, Skarbiec 80% brutto tygodniowo, a dziwactwo z
    `nazwy.json` mówi o 10% zniżki za gotówkę. Dwie różne miary w użyciu. → Wybrać jedną.
19. **`docs/AGENT_BRIEF.md`, `docs/ANALIZA_v5.md`, `TASKS.md` opisują stan v5** (targowanie 10%, jakość ×2). → Odświeżyć.
20. **Edycja cen nie obejmuje `handel.json`, `postacie.json`, `kalendarz.json`** — zmiany tylko w plikach. → Dodać, jeśli
    potrzebne przy stole.
21. **Baza kupców jest tylko w przeglądarce.** Wyczyszczenie danych strony ją kasuje. → Eksportować regularnie
    (Kupcy → Eksport wszystkich); ewentualnie przypomnienie w aplikacji.
22. **Stare linki z seedem dają inne sklepy** po każdej zmianie cennika i kupców (v6–v6d). Zapisani kupcy są bezpieczni.
23. **Kalkulator „ile Robót” i kolumna „Robót” w Cenniku liczą cenę bazową,** a gracz płaci u kupca o 5–45% więcej. → Dopisać
    to w podpowiedzi albo liczyć od ceny typowej kupca.

---

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
| Kalendarz Imperium | `data/kalendarz.json` | `miesiace` (nazwa, staroświatowa, dni, święto, pora), `tydzien` (8 dni) | Księga Zbawienia s. 140–141 / Kompendium MG s. 31. Data kupca (`dzien` 1–400, `rok`) wyznacza porę roku; upływ czasu = 8 dni na tydzień. |
| Handel wg Poradnika Staroświatowca | `data/handel.json` | `pory_roku`, `wahania`, `strefy` (siatka stopni), `mnozniki_stopni`, `kategorie_z_towarow`, `miasta`, `zamoznosc`, `zagrozenia`, `oplaty`, `nielegalne`, `handel_lokalny`, `bogowie`, `zasady_dodatkowe` | Teksty z Poradnika (rozdz. III), bez cen 2. edycji. Mnożniki stopni dostępności i statusy dochodu interesu to szacunek MG. |
| Ośrodki handlu jako osady | `data/osady.json` (wpisy `miasto-*`) | `mnoznik` (typ × zamożność), `kategorie` (ceny strefy), `dostepnosc`, `populacja`, `zamoznosc`, `strefa` | Budowane przez `narzedzia/dane_v6c.py` z `data/handel.json` — zmieniaj tam i uruchom skrypt. |
| Nielegalne towary | `data/cennik.json` → `nielegalny`; `data/kupcy.json` → `nielegalne` | | Tylko paser i kupiec z cechą „Powiązania przestępcze”; cena × zamożność (tab. 3-11). |
| Twoje bieżące zmiany | `data/ustawienia.json` | jak eksport z Edycji cen | Puste = cennik domyślny. |

| Dostępność, specjalności miast (v6d) | `narzedzia/dane_v6d.py` → `data/cennik.json`, `data/osady.json`, `data/rynek.json`, `data/handel.json` | cennik: `strona`, `nielegalny`, `nielegalny_uwaga`; osady: `tagi` (branża → mnożnik ceny, np. Middenheim futra ×0,8), `rzadkie_latwiej`, `import`; rynek: `dostepnosc.tabela.metropolia`, `import_egzotyczne`, `obce_wies`, `jakosc.osada_zalety`, `gospoda.standardy`; handel: `strefa_cena` (krok, min, max), `wahania[].dostepnosc` | Specjalności miast to szacunek MG (Poradnik s. 34/38 odsyła do „Dziedzictwa Sigmara”, 2. ed.). Strony z `narzedzia/strony_pg.json`. |
| Dane do Kompendium MG | `docs/KOMPENDIUM_DANE.md` | | Generowany: `node narzedzia/eksport_kompendium.mjs`. Nie edytuj ręcznie. |

Kolejność skryptów danych: `narzedzia/dodaj_v6.py` → `narzedzia/dane_v6b.py` → `narzedzia/dane_v6c.py` → `narzedzia/dane_v6d.py`
(każdy idempotentny; v6c przebudowuje osady, więc v6d zawsze po nim).

Po każdej zmianie w `data/` uruchom `npm test` — testy spójności pilnują arbitrażu (np. koc tańszy niż jego sukno).
