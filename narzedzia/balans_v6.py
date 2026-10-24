# -*- coding: utf-8 -*-
"""v6: balans cen wobec zarobków. Ile Robót (netto) i tygodni brutto kosztuje koszyk rzeczy na każdym szczeblu Statusu.

Robota = netto za tydzień pracy ponad normę (rzut na Dochód). Brutto = 5 × netto, 80% brutto to utrzymanie w osadzie.
Wynik: docs/analiza_v6/balans.csv i tabela na standardowe wyjście (do docs/ANALIZA_v6.md).
Uruchom z katalogu repo: py narzedzia/balans_v6.py
"""
import csv, json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
J = lambda f: json.load(open(R + f, encoding='utf-8'))
C = {c['id']: c for c in J('data/cennik.json')['pozycje']}
S = [p for p in J('data/statusy.json')['poziomy'] if p['brutto_p'] > 0]

KOSZYK = [
    ('chleb na tydzień (2 bochenki/dzień)', C['chleb-zytni-bochenek']['cena_p'] * 14),
    ('jedzenie na zimno, tydzień', C['jedzenie-na-zimno-na-1-dzien']['cena_p'] * 7),
    ('kąt w izbie czeladnej, tydzień', C['kat-w-izbie-czeladnej-tydzien']['cena_p']),
] + [(C[i]['nazwa'], C[i]['cena_p']) for i in [
    'ubranie', 'buty', 'koc', 'siekiera', 'bron-reczna-topor-maczuga', 'wlocznia', 'luk', 'miecz', 'kusza',
    'rusznica-lontowa', 'pistolet', 'skorzany-kaftan', 'kolczuga', 'pelna-plytowka-4-elementy',
    'mikstura-lecznicza', 'narzedzia-pracy', 'krowa', 'wol', 'kon-pociagowy', 'furmanka', 'woz', 'kon-wierzchowy',
    'lekki-kon-bojowy', 'rumak', 'kupno-prosty-dom']]
POZIOMY = ['Brąz 1', 'Brąz 2', 'Brąz 3', 'Brąz 5', 'Srebro 1', 'Srebro 3', 'Srebro 5', 'Złoto 1', 'Złoto 3']
S = {f"{p['tier']} {p['lvl']}": p for p in S}
mon = lambda p: (f"{p // 240} ZK " if p >= 240 else '') + (f"{p % 240 // 12} s " if p % 240 >= 12 else '') + (f"{p % 12} p" if p % 12 or p < 12 else '')
def ile(p, netto):
    r = p / netto
    return '<1' if r < 1 else f'{r:.0f}' if r < 400 else '400+'

os.makedirs(R + 'docs/analiza_v6', exist_ok=True)
with open(R + 'docs/analiza_v6/balans.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['pozycja', 'cena_p'] + [f'{s} Robót' for s in POZIOMY] + [f'{s} tyg. brutto' for s in POZIOMY])
    for n, p in KOSZYK:
        w.writerow([n, p] + [round(p / S[s]['netto_p'], 1) for s in POZIOMY] + [round(p / S[s]['brutto_p'], 1) for s in POZIOMY])

print('| Rzecz | Cena | ' + ' | '.join(POZIOMY) + ' |')
print('|---|---:|' + '---:|' * len(POZIOMY))
for n, p in KOSZYK:
    print(f'| {n} | {mon(p).strip()} | ' + ' | '.join(ile(p, S[s]['netto_p']) for s in POZIOMY) + ' |')
print()
for s in POZIOMY:
    b = S[s]['brutto_p']
    print(f'{s}: brutto {b} p, utrzymanie {round(b * 0.8)} p, netto {S[s]["netto_p"]} p')
WIES = 25
print(f'\nWieś {WIES} gospodarstw Brąz 3: netto razem {WIES * 33} p/tydz.; wóz = {C["woz"]["cena_p"] / (WIES * 33):.1f} tyg., '
      f'wóz + koń pociągowy = {(C["woz"]["cena_p"] + C["kon-pociagowy"]["cena_p"]) / (WIES * 33):.1f} tyg. całej nadwyżki wsi')
