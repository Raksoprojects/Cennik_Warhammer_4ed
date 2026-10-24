# Instrukcje dla GitHub Copilot

Przeczytaj `AGENTS.md` (zasady), `docs/AGENT_BRIEF.md` (kontekst, API, niezmienniki) i `TASKS.md` (kolejność prac).

Najważniejsze:
- Odpowiadaj i pisz interfejs po polsku. Identyfikatory polskie bez diakrytyków.
- Kwoty w pensach (1 ZK = 20 s = 240 p). Do wyświetlania `mon()` z `src/silnik.js`.
- Cena bazowa (`cena_p` z cennika) zawsze obok ceny kupca (`generujKupca`). Osada i sytuacja z modyfikatorem w nawiasie
  (`etykietaOsady`, `etykietaKoniunktury`).
- Ustawienia MG: `zastosujUstawienia(dane, ust)` → `stan.d` w `src/lib/stan.svelte.ts`; widoki Svelte przeliczają się same.
- Zapisany kupiec: `src/kupcy_trwali.js` (operacje zwracają nowy obiekt; ceny liczy `wycen()` z bieżących danych).
- Nie zmieniaj kolejności losowań w `generujKupca`. Nie zmieniaj ręcznie `data/cennik.json`. `npm test` przed commitem.
- Nie podnoś cen bez źródła. Otwarte decyzje cenowe (AGENT_BRIEF rozdz. 10) zostaw MG.
