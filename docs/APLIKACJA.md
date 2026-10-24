# Skarbiec Imperium — aplikacja. Materiały do budowy w VS Code (v5)

Silnik i dane są gotowe i przetestowane. Zostaje interfejs. Ten dokument opisuje, co zbudować,
w jakiej kolejności i po czym poznać, że działa. Kolejność prac i kryteria odbioru: `TASKS.md`.
Kontekst dla agenta: `docs/AGENT_BRIEF.md`. Działający wzór: `reference/skarbiec_v5.html`.

`SPECYFIKACJA.md` mówi **co program liczy**. Ten plik mówi **jak go złożyć**.

---

## 1. Decyzje techniczne

### Stack: Vite + czysty JavaScript, bez frameworka

`src/silnik.js` to moduły ES bez zależności i bez DOM. Nie ma powodu, żeby dokładać do tego Reacta:
cała aplikacja to osiem widoków, w których jedyną interakcją jest „zmień filtr i przerysuj tabelę".
Framework dołożyłby 40 kB i warstwę, przez którą trzeba by przeprowadzać stan losowania.

```
npm create vite@latest skarbiec -- --template vanilla
```

Jeśli jednak wolisz React — silnik jest czysty, więc `generujKupca()` wywołasz z `useMemo`
i nic się nie zmienia. Wtedy pomiń `template vanilla`.

**TypeScript:** opcjonalnie, ale warto. Dane są mocno ustrukturyzowane i jeden plik `typy.d.ts`
(w § 4) wyłapie literówki w nazwach pól, które inaczej zobaczysz dopiero jako `undefined` w tabeli.

### Dane: import statyczny, nie fetch

```js
import cennik from '../data/cennik.json';
```

Vite wkompiluje JSON w bundle. Nie ma wtedy stanu ładowania, migotania i problemów ze ścieżkami
na GitHub Pages. Komplet to ok. 350 kB JSON-a — bez znaczenia dla strony, która i tak jest offline-first.

### Hosting: GitHub Pages

```js
// vite.config.js
export default { base: '/skarbiec-imperium/' }   // nazwa repozytorium
```

Workflow w `.github/workflows/pages.yml`: `npm ci && npm run build`, publikacja `dist/`.

---

## 2. Struktura projektu

```
skarbiec-imperium/
├─ AGENTS.md, CLAUDE.md, TASKS.md, .github/copilot-instructions.md   ← instrukcje dla agenta
├─ data/                   ← źródło prawdy (cennik v5, klasy, ustawienia, kupcy, osady…)
├─ src/
│  ├─ silnik.js            ← logika (gotowe)
│  ├─ spojnosc.js          ← testy spójności, wspólne z aplikacją (gotowe)
│  └─ app/
│     ├─ main.js           ← router po #hash, stan ustawień (szkielet gotowy)
│     ├─ dane.js           ← import wszystkich JSON-ów (gotowe)
│     ├─ format.js         ← mon(), proc(), pl(), tygodniePracy(), parsujCene() (gotowe)
│     ├─ ustawienia.js     ← localStorage, eksport, import, zastosujUstawienia (gotowe)
│     ├─ widoki/
│     │  ├─ cennik.js      ← wzór widoku (gotowe, do rozbudowy w T2)
│     │  ├─ kupiec.js, zamowienie.js, zarobki.js, czynsze.js, ustawienia.js,
│     │  └─ modyfikatory.js, audyt.js, historia.js, zasady.js      ← do zrobienia
│     └─ ui/
│        ├─ tabela.js      ← tabela z wyszukiwarką i filtrami (T1)
│        └─ styl.css
├─ test/                   ← 33 testy (node --test)
├─ narzedzia/              ← skrypty Pythona: budowa danych, analiza, artefakt
├─ reference/              ← skarbiec_v5.html (wzór UI), oryginał, pdf/ (lokalnie, poza gitem)
└─ index.html
```

Każdy widok eksportuje `montuj(el, ctx)`; `ctx = { d, ust, ustaw(nowe), nawiguj(hash) }`. `ctx.d` to dane **po**
ustawieniach MG. Po `ustaw()` router montuje widok od nowa.

`dane.js` (stan v5 jest w `src/app/dane.js` — ten fragment to wersja skrócona):

```js
import cennik from '../data/cennik.json';
import kupcy from '../data/kupcy.json';
import osady from '../data/osady.json';
import koniunktura from '../data/koniunktura.json';
import rynek from '../data/rynek.json';
import nazwy from '../data/nazwy.json';
import statusy from '../data/statusy.json';
import czynsze from '../data/czynsze.json';
import audyt from '../data/audyt.json';
import historia from '../data/historia.json';
import pozycja_dochod from '../data/pozycja_dochod.json';
import przedmioty_magiczne from '../data/przedmioty_magiczne.json';
import kalkulator from '../data/kalkulator.json';

export const d = { cennik, kupcy, osady, koniunktura, rynek, nazwy, statusy, czynsze,
                   audyt, historia, pozycja_dochod, przedmioty_magiczne, kalkulator };
export const poId = Object.fromEntries(cennik.pozycje.map(p => [p.id, p]));
```

---

## 3. Widoki

Osiem zakładek. Trzy pierwsze to serce programu — reszta to tabele do przeglądania.

### 3.1 Kupiec (najważniejszy)

Trzy listy wyboru: handlarz (z marżą), osada (`etykietaOsady` → „Altdorf (+30%)”), sytuacja
(`etykietaKoniunktury(d, k, { krotko: true })`). Przycisk **Losuj**, pole **seed**, pole **PS z Targowania**.
Pod listami pełna etykieta sytuacji.

Nagłówek: imię, archetyp, Status, osada, rdzeń asortymentu, opis + dziwactwo, plakietki z mnożnikami.

Tabela (v5): Towar · Sztuk · **Cena bazowa** · **Jego cena** (+%) · **Minimalna** · Po targu (gdy PS > 0) ·
Odkupi za · Dlaczego tyle (zapas, popyt, modyfikator testu, marża, preferencja, kaprys, osada, koniunktura, rynek, koszt).

Czego **nie ma** w oryginale, a przy stole jest potrzebne:

- **Seed w adresie.** `#kupiec?k=zbrojmistrz&o=miasto&n=wojna&s=48213`. Ten sam link = ten sam
  kupiec, zawsze. MG może przygotować sklep przed sesją i wrócić do niego za trzy tygodnie.
- **Pole „PS z Targowania"** jedno na cały sklep. Wywołuje
  `targuj(d, {cena_p, cena_cennik_p, cena_min_p, ps})` — dolną granicą jest cena minimalna kupca.
- **Zapisz kupca** → `localStorage`, lista „Moi kupcy" z nazwą i miastem. Kupiec wraca między sesjami.
- **Druk** — `@media print` ukrywa nawigację i formularze, zostaje czysta karta sklepu na kartkę A4.

### 3.2 Zamówienie na miarę

Pole z podpowiedziami (`<datalist>` ze wszystkich pozycji o `typ === 'towar'`), lista jakości,
przycisk **Wyceń**. Pokazać pełne rozbicie mnożników, zaliczkę i termin.

Trzy stany odpowiedzi z silnika: `wykonuje` · `sprowadza` · `odmowa` (wtedy wypisać, do kogo odsyła).

### 3.3 Cennik

Wyszukiwarka (`norm()` — bez polskich znaków), filtr kategorii, filtr kierunku, **filtr typu**
(towar / nocleg / usługa / nieruchomość — nowy w v3).

Kolumny: Przedmiot (+ źródło, kategoria, typ) · RAW (przekreślone przy zmianie) · ×1 · Klasa (mnożnik) ·
**Cena bazowa** · Tyg. pracy · Podstawa historyczna · Komentarz.

Dwie rzeczy do pokazania wprost, bo inaczej nikt się nie domyśli:

- pozycja z pustym `podstawa_hist` dostaje szary znacznik **„bez źródła"** — to 177 z 364 pozycji
  i użytkownik ma prawo wiedzieć, które liczby są oszacowane;
- pozycja z `typ ≠ 'towar'` dostaje znacznik **„nie w handlu"** z wyjaśnieniem, że cena jest już detaliczna.

### 3.4 Zarobki i kalkulator

Tabela 18 szczebli z `statusy.json`. Kalkulator: Status + Majętny + przycisk **Rzuć**
(`rzutDochodu`) obok wartości średniej (`sredniDochod`). Oryginał pokazywał tylko średnią.

Lista „ile Robót odłożyć" — **czytać ceny po `id` z cennika**, nie z `kalkulator.json`.
Dziś kalkulator ma kolczugę za 7 ZK, a cennik za 10 ZK i będzie się to rozjeżdżać po każdej zmianie.
`kalkulator.json` zostaw jako listę `id` do pokazania, bez cen.

### 3.5 Czynsze (nowy widok, nie było go w artefakcie)

Tabela najmu × okres, dwie listy wyboru: osada i koniunktura. Woła `czynsz(d, {...})`.
Pokazać rozbicie: baza × osada × koniunktura. Pod spodem ceny kupna i wyliczenie
„kupno zwraca się w N latach najmu".

### 3.6 Ustawienia MG (v5)

Edycja na żywo: preset, mnożniki klas (z tagiem źródła i uzasadnieniem z `klasy_cenowe.uzasadnienia`),
premia znaku stanu, osady, marże kupców, rynek (preferencje, kaprys, cena minimalna), koniunktura per kategoria,
cena pojedynczej pozycji. Podgląd zmienionych cen, JSON (zastosuj / eksport / import / przywróć), przycisk
**Sprawdź spójność** (`sprawdzWszystko`). Szczegóły i kryteria: `TASKS.md`, T7.

### 3.7 Audyt profesji · 3.8 Tabela historyczna · 3.9 Zasady

Tabele z wyszukiwarką i filtrami, bez logiki. Teksty zasad w `pozycja_dochod.json` i w HTML.
**Poprawić liczby koniunktury w tekście zasady 5** — w artefakcie były inne niż w kodzie.

---

## 4. Kontrakt danych (`typy.d.ts`)

```ts
export type Typ = 'towar' | 'nocleg' | 'usluga' | 'nieruchomosc';
export type Podtyp = 'zwierze_hodowlane' | 'zywnosc_podstawowa';
export type Dostepnosc = 'Powszechna' | 'Ograniczona' | 'Rzadka' | 'Egzotyczna' | null;

export interface Pozycja {
  id: string;  kat: string;  nazwa: string;
  zrodlo: 'PG' | 'PB' | null;
  cena_raw_p: number | null;      // z podręcznika; null = pozycja kampanii
  cena_p: number;                 // cena wytwórcy — wejście do WSZYSTKICH obliczeń
  obc: number | null;
  dostepnosc: Dostepnosc;
  typ: Typ;                       // v3
  podtyp: Podtyp[] | null;        // v3
  podstawa_hist: string;          // pusty = brak źródła
  komentarz: string;
  dopisane: string | null;
  uwagi_danych: string | null;
  pozycja_kampanii: boolean;
  cena_ref_p: number;             // v4: poziom ×1 przed mnożnikiem klasy
  klasa: string;                  // v4: klasa cenowa (data/klasy_cenowe.json)
  nadpisane?: boolean;            // v5: cena z ustawień MG
}

export interface Kupiec {
  id: string; nazwa: string; status: string;
  marza: number; limit_p: number; skup: number;
  rdzen: string[]; boczne: string[]; robota: string[];
  preferencje?: Record<string, number>;   // v5: mnożnik per kategoria (nadpisuje rynek.preferencje)
  opis: string;
}

export interface WierszSklepu {
  id: string; nazwa: string; kat: string; sztuk: number;
  cena_wytworcy_p: number; mnoznik: number; cena_p: number; skup_p: number;
  zapas: 0|1|2|3; zapas_nazwa: string; popyt: 0|1|2; popyt_nazwa: string;
  koszt_p: number; cena_min_p: number; wyprzedaz: boolean;        // v5
  rzuty: { zapas: number; popyt: number; kaprys: number | null };
  skladowe: { marza: number; preferencja: number; kaprys: number; osada: number; koniunktura: number; rynek: number };
}

export interface Ustawienia {                    // v5: data/ustawienia.json
  wersja: 1; preset: string;
  mnozniki: Record<string, number>; premia_znak_stanu: number | null;
  pozycje: Record<string, { cena_p?: number; mnoznik?: number }>;
  osady: Record<string, { mnoznik?: number; limit_p?: number | null }>;
  koniunktury: Record<string, { kategorie?: Record<string, { cena?: number; popyt?: number }>; czynsz?: number }>;
  kupcy: Record<string, Partial<Kupiec>>;
  rynek: Record<string, object>;
}
```

**Niezmiennik, który łatwo złamać:** `cena_p` to cena **bazowa (wytwórcy)**. Nigdzie w interfejsie nie wolno
pokazać jej jako „ceny w sklepie". Każda cena płacona przez gracza przechodzi przez `generujKupca` albo
`wycenZamowienie`. Cena bazowa ma być **widoczna obok** ceny kupca — jako punkt odniesienia.

---

## 5. Kolejność prac

**Obowiązuje `TASKS.md`** (v5, z ustawieniami MG). Tabela poniżej to plan z v3, zostawiony dla historii.

| # | Krok | Gotowe, gdy |
|---|---|---|
| 1 | Szkielet: Vite, `dane.js`, `format.js`, nawigacja po `#hash` | osiem pustych zakładek przełącza się bez przeładowania |
| 2 | `ui/tabela.js` — wyszukiwarka + filtry + render | działa na cenniku |
| 3 | Widok **Cennik** | 361 pozycji, filtry kategorii, kierunku i typu, znaczniki „bez źródła" i „nie w handlu" |
| 4 | Widok **Kupiec** bez dodatków | odtwarza wynik `node weryfikuj.mjs` dla tego samego seeda |
| 5 | Seed w URL + **Losuj** | wklejony link daje tego samego kupca |
| 6 | **Zamówienie** | trzy stany: wykonuje / sprowadza / odmowa |
| 7 | **Zarobki** + kalkulator z rzutem | rzut i średnia obok siebie |
| 8 | **Czynsze** | Marienburg + kryzys mieszkaniowy = 4 ZK 7 s |
| 9 | **Audyt**, **Historia**, **Zasady** | tabele filtrują |
| 10 | Targowanie, zapis kupca, druk | karta sklepu wychodzi na A4 |
| 11 | GitHub Pages | działa pod publicznym adresem |

---

## 6. Kryteria odbioru

Do sprawdzenia ręcznie po złożeniu interfejsu. Testy jednostkowe (`node --test test/`) pilnują silnika;
to są rzeczy, które psuje się **w widoku**.

1. **Seed jest powtarzalny.** Ten sam link → identyczna lista towaru, co do sztuki i pensa.
2. **Nie ma noclegu w asortymencie.** Przejdź wszystkich 15 handlarzy; nigdzie nie pojawia się
   „Wspólna izba", „Ciepły posiłek", „Stajnia", czynsz ani najmita.
3. **Wieś ma zwierzęta.** Handlarz koni we wsi wystawia konia pociągowego (seed 1: 12 ZK 17 s 5 p) mimo limitu 2 ZK.
4. **Rozbicie się zgadza.** Dla dowolnego wiersza: `cena bazowa × marża × preferencja × kaprys × osada ×
   koniunktura × rynek` po zaokrągleniu = „Jego cena". Pokaż te liczby w podpowiedzi.
5. **Zaraza obniża czynsz.** Mieszkanie w Marienburgu: normalna 2 ZK 18 s, zaraza 1 ZK 14 s 10 p.
6. **Kalkulator zgadza się z cennikiem.** Kolczuga w kalkulatorze = 20 ZK, tyle samo co w cenniku (po ustawieniach).
7. **Tyg. pracy.** Rumak 825 ZK → 1200 tygodni pracy robotnika. Jeśli wychodzi co innego, `ROBOTNIK`
   nie jest 165.
8. **Targowanie nie schodzi poniżej ceny minimalnej.** U pasera (marża −35%) cena minimalna = jego cena, więc 3 PS nic nie dają.
9. **Druk.** Karta sklepu na A4 bez nawigacji i bez pól formularza.
10. **Telefon.** 400 px szerokości, tabele przewijają się poziomo we własnym kontenerze,
    strona nie przewija się na boki.

---

## 7. Pułapki

- **`norm()` zjada polskie znaki w wyszukiwarce, ale nie w `id`.** Generując `id` z nazwy, zamień
  `ł` na `l` **przed** normalizacją NFD — `ł` nie ma rozkładu kanonicznego i po prostu zniknie
  (`kapłon` → `kapon`). Zdarzyło mi się to przy dopisywaniu 30 pozycji.
- **Kolejność losowań.** `generujKupca` losuje w ściśle określonej kolejności (rdzeń → boczne →
  imię → dziwactwo → wiersze). Nie wolno przestawić, bo seed przestanie odtwarzać stare sklepy.
  To samo dotyczy sortowania — musi być stabilne, malejąco po `cena_p`.
- **`mon(0)` zwraca „—", nie „0 p".** W sumach i porównaniach używaj liczb, `mon()` tylko do wyświetlania.
- **Dwa źródła prawdy dla czynszu** (`czynsze.json` i wiersze w cenniku) pilnuje test. Jeśli zmienisz
  jedno, zmień drugie — albo generuj wiersze cennika z `czynsze.json` przy starcie.
- **Majętny dodaje się do rzutu, czyli do netto.** Brutto to `5 × (rzut + Majętny)`. Artefakt liczył
  to źle i dodawał bonus do brutto bez mnożenia.
- **`Infinity` w JSON nie istnieje.** Brak limitu osady to `null`, a nie duża liczba.
