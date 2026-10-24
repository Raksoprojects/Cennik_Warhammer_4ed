# AGENTS.md — instrukcja dla agenta AI

Projekt: **Skarbiec Imperium** — cennik, generator i baza kupców, zarobki i czynsze dla kampanii WFRP 4 ed.
(polskie wydanie). Użytkownik to Mistrz Gry. Pisze po polsku; odpowiadaj po polsku.

**Nie masz dostępu do rozmów, w których powstał projekt, ani do pamięci Claude.** Wszystko jest tutaj:

1. `docs/AGENT_BRIEF.md` — kontekst, zasady domowe, słowniczek, API silnika, niezmienniki, decyzje. **Przeczytaj w całości.**
2. `README.md` — co jest w aplikacji (v6) i jak jest zbudowana.
3. `TASKS.md` — zadania z kryteriami odbioru.
4. `docs/ANALIZA_v5.md` — skąd są ceny i co czeka na decyzję MG.

## Polecenia

```bash
npm install
npm test          # testy silnika, danych i kupców — muszą przejść przed każdym commitem
npm run dev       # http://localhost:5173/Cennik_Warhammer_4ed/
npm run build     # svelte-check + dist/ (GitHub Pages)
python3 narzedzia/analiza_v5.py   # po każdej zmianie cen
python3 narzedzia/dodaj_v6.py     # broń z podręczników ras + Zalety i Wady (idempotentny)
```

## Twarde zasady

- `src/silnik.js`, `src/spojnosc.js`, `src/kupcy_trwali.js` to logika bez DOM, testowana w node. Zmieniaj ją tylko z testem.
- **Nie zmieniaj kolejności losowań** w `generujKupca`. Ten sam seed i te same dane mają dawać ten sam sklep.
- **Nie zmieniaj cen ręcznie w `data/cennik.json`.** Ceny idą przez presety (`data/klasy_cenowe.json`), ustawienia
  (`data/ustawienia.json`) albo skrypty w `narzedzia/`. Każda zmiana cen musi przejść `npm test`.
- **Nie podnoś cen bez źródła.** MG: „nie chcę, żeby było drożej tylko po to, żeby było drożej”.
- Decyzje oznaczone w `docs/AGENT_BRIEF.md` rozdz. 10 jako otwarte — **pytaj MG**, nie rozstrzygaj sam.
- W interfejsie **zawsze** cena bazowa obok ceny kupca; osada i sytuacja z modyfikatorem w nawiasie.
- Nazwy Talentów, Zalet i Wad tylko z polskiego wydania podręcznika. Nie tłumacz z angielskiego.
- PDF-y podręczników tylko w `reference/pdf/` (w `.gitignore`). **Nigdy ich nie commituj.**
- Interfejs: Svelte 5 + TypeScript + Vite + PWA (jak Program_postac_GUI i Generator_NPC). Bez zależności runtime.
- `localStorage` zawsze w `try/catch`; aplikacja musi działać bez niego.
- Kwoty w pensach, całkowite. `mon()` tylko do wyświetlania.
- Telefon (390 px): strona nie przewija się na boki; tabele z klasą `karty` zamieniają się w karty.

## Styl

Polski interfejs i komentarze. Identyfikatory polskie bez diakrytyków (`cena_p`, `generujKupca`). Krótkie funkcje.
Widok = `src/widoki/<Nazwa>.svelte`; stan wspólny w `src/lib/stan.svelte.ts` (`stan.d` = dane po ustawieniach MG).
Podpowiedzi klikane (`komponenty/Podpowiedz.svelte`), dłuższe objaśnienia w `<details class="opis">`.
