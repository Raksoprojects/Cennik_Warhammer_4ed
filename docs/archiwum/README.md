# Archiwum dokumentów

Dokumenty z wcześniejszych wersji. **Nie są źródłem obowiązujących liczb ani zasad.** Obowiązują:

- `data/*.json` — dane (jedyne źródło prawdy dla cen i mnożników),
- `docs/KOMPENDIUM_DANE.md` — wszystkie tabele i zasady wygenerowane z danych (`node narzedzia/eksport_kompendium.mjs`),
- `docs/DANE.md` — decyzje MG, otwarte punkty i mapa danych,
- `docs/AGENT_BRIEF.md` — kontekst, zasady domowe, niezmienniki dla agenta.

Archiwum czytaj tylko wtedy, gdy potrzebujesz historii decyzji albo źródła ceny.

| Plik | Stan | Do czego się przydaje |
|---|---|---|
| `ANALIZA_CEN.md` | v1 | pierwszy przegląd spójności cennika |
| `ANALIZA_ZRODEL.md` | v2 | źródła historyczne cen (Kraków 1526–35, Anglia, Frankfurt) — nadal cytowane w `cennik.json → podstawa_hist` |
| `PRZEGLAD_v3.md` | v3 | typy pozycji (nocleg i usługi poza handlem), czynsz w koniunkturze, macierz zapas × popyt |
| `ANALIZA_v4.md` | v4 | klasy cenowe, presety, testy arbitrażu |
| `ANALIZA_v5.md` | v5 | uzasadnienie każdego mnożnika klasy (rozdz. 3.3). Tabele `docs/analiza_v5/*.csv` generuje dalej `narzedzia/analiza_v5.py` |
| `ANALIZA_v6.md` | v6 | balans cen wobec zarobków (tabela `docs/analiza_v6/balans.csv` z `narzedzia/balans_v6.py`) |
| `APLIKACJA.md`, `SZKIC_v6.md`, `TASKS.md` | v5–v6 | plan budowy interfejsu i zadania T1–T11 (zrobione) |
| `SPECYFIKACJA.md` | artefakt 2026-09 | opis pierwotnego artefaktu claude.ai |

Co się zmieniło od v5 (najczęstsze pułapki w archiwum): targowanie −4% za PS (najwyżej −24%, zamówienia −16%), nie 10%;
jakość: Zaleta ×1,6, Wada ×0,6, nie ×2 i ×½; rok = 50 tygodni, nie 52; interfejs w Svelte 5, nie `src/app/*.js`.
