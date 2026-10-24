# Narzędzia

| Plik | Co robi |
|---|---|
| `zrodla.py` | przelicza ceny ze źródeł na dniówki (analiza v2) |
| `propozycja.py` | buduje `propozycja/cennik_v2.json` |
| `buduj_v3.py` | v2 + 30 nowych pozycji + pola `typ`/`podtyp` + koniunktura czynszu + wyjątki wsi → `out/*.json` |
| `patch_silnik.py` | nakłada na `src/silnik.js` zmiany v3 (typy, limit wsi, funkcja `czynsz`) |
| `patch_testy.py` | dopisuje reguły spójności v3 i testy strukturalne |
| `zbuduj_artefakt.py` | składa jednoplikową stronę z `data/*.json` + `src/silnik.js` + `src/spojnosc.js` → `reference/skarbiec_v5.html` |
| `artefakt/patch_v5.py` | `artefakt/szablon_v4.html` → `artefakt/szablon.html` (widoki v5, panel Ustawienia MG) |
| `model_v4.py`, `raport_v4.py` | model klas cenowych i porównanie presetów (v4) |
| `buduj_v5.py` | z archiwum v4 buduje dane v5: klasy, presety, cennik zalecany, czynsze, koniunktura, nowe reguły |
| `analiza_v5.py` | przegląd wszystkich pozycji, klasy vs źródła, profesje vs ceny → `docs/analiza_v5/` |
| `weryfikuj.mjs` | ręczna kontrola: usługi poza handlem, zwierzęta we wsi, czynsz z koniunkturą |

Pełne odtworzenie v3 z oryginalnego zipa:

```
python3 narzedzia/buduj_v3.py && cp out/*.json data/
python3 narzedzia/patch_silnik.py
python3 narzedzia/patch_testy.py
node --test test/*.test.mjs
```

Odtworzenie v5 z danych v4 (archiwum w `propozycja/`):

```
python3 narzedzia/buduj_v5.py
python3 narzedzia/analiza_v5.py
python3 narzedzia/artefakt/patch_v5.py && python3 narzedzia/zbuduj_artefakt.py
npm test
```
