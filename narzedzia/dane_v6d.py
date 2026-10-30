# -*- coding: utf-8 -*-
"""v6d: decyzje MG z 2026-10-30. Idempotentny. Uruchamiaj po dane_v6c.py.

  1. data/cennik.json  ← źródło ze stroną (strona: PG z narzedzia/strony_pg.json, KR, WE), nielegalne +4,
                         lekki koń bojowy Ograniczona, rumak Rzadka
  2. data/osady.json   ← metropolie (Nuln, Talabheim, Middenheim, Altdorf, Marienburg, ogólna) z tabelą Dostępności „metropolia”,
                         Middenheim jako metropolia (MG: 15 000 z Poradnika nie ma sensu), Altdorf „Rzadkie o stopień łatwiej”,
                         Marienburg „import”, lokalne specjalności (tagi): Middenheim futra i żelazo, Nuln proch, Marienburg import
  3. data/rynek.json   ← Egzotyczne: 3% w metropolii, 0,1% gdzie indziej; wahania zmieniają też Dostępność;
                         Zalety rzadziej we wsi; krasnoludzki towar we wsi rzadziej; standard gospody (nocleg, posiłek)
Uruchom z katalogu repo: py narzedzia/dane_v6d.py && npm test
"""
import json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
J = lambda f: json.load(open(R + f, encoding='utf-8'))
def W(f, d): json.dump(d, open(R + f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print('zapisano', f)

# ---------------------------------------------------------------- 1. cennik
C = J('data/cennik.json'); P = {c['id']: c for c in C['pozycje']}
STR = J('narzedzia/strony_pg.json')
UZUP = {'helm-zamkniety': 300, 'pelna-plytowka-4-elementy': 300, 'stajnia-na-1-noc': 302, 'pol-litra-piwa-bugmana': 302, 'kreda-wegiel-do-rysowania': 303}
for c in C['pozycje']:
    c.pop('strona', None)
    if c['zrodlo'] == 'PG': c['strona'] = STR.get(c['id']) or UZUP.get(c['id'])
    elif c['zrodlo'] == 'KR': c['strona'] = 94 if c['kat'] == 'Broń zasięgowa' else 93
    elif c['zrodlo'] == 'WE': c['strona'] = 31
NIELEGALNE = ['rozkosz-ranalda', 'grzybki-szalonego-kapelusznika', 'dziwnokorzen', 'czarny-lotos', 'sercoboj',
              'ksiezycowy-kwiat', 'nocny-cien', 'korzen-mandragory', 'ksiega-magia']
for c in C['pozycje']:
    c.pop('nielegalny', None); c.pop('nielegalny_uwaga', None)
    if c['id'] in NIELEGALNE: c['nielegalny'] = True
P['ksiega-magia']['nielegalny_uwaga'] = 'Legalna tylko dla magów Kolegiów (licencja); u innych — zakazana księga.'
P['lekki-kon-bojowy']['dostepnosc'] = 'Ograniczona'
P['rumak']['dostepnosc'] = 'Rzadka'
W('data/cennik.json', C)

# ---------------------------------------------------------------- 2. osady
OS = J('data/osady.json'); O = {o['id']: o for o in OS['osady']}
for i in ['metropolia', 'altdorf', 'marienburg', 'miasto-nuln', 'miasto-talabheim', 'miasto-middenheim']:
    O[i]['dostepnosc'] = 'metropolia'
m = O['miasto-middenheim']
m.update(typ='metropolia', mnoznik=round(O['metropolia']['mnoznik'] * 1.1, 3), limit_p=None,
         uwaga='MG: metropolia (Poradnik podaje 15 000 mieszkańców — odrzucone). Futra i żelazo z Middenlandu tanie.')
O['altdorf']['rzadkie_latwiej'] = True
O['altdorf']['uwaga'] = 'Rzadkie o stopień łatwiej (szansa jak Ograniczonej).'
O['marienburg']['rzadkie_latwiej'] = True
O['marienburg']['import'] = True
O['marienburg']['uwaga'] = 'Wszystko z importu: Rzadkie o stopień łatwiej, Egzotyczne częściej niż w innych metropoliach.'
# Lokalne specjalności (szacunek MG): tag branży → mnożnik ceny. Tylko tam, gdzie lore jest jednoznaczny.
TAGI = {
    'miasto-middenheim': {'futra': 0.8, 'warsztatowe': 0.9, 'prosta': 0.92, 'wojskowa': 0.92, 'tarcze': 0.92},
    'miasto-nuln': {'prochowa': 0.85, 'eksperymentalna': 0.85, 'warsztatowe': 0.92},
    'marienburg': {'kolonialne': 0.8, 'luksus': 0.9, 'tkaniny': 0.9},
}
for o in OS['osady']:
    o.pop('tagi', None)
    if o['id'] in TAGI: o['tagi'] = TAGI[o['id']]
W('data/osady.json', OS)

# ---------------------------------------------------------------- 3. rynek
RY = J('data/rynek.json'); D = RY['dostepnosc']
for typ in ('wioska', 'miasteczko', 'miasto'): D['tabela'][typ]['Egzotyczna'] = 0.001
D['tabela']['metropolia'] = {'Powszechna': 1, 'Ograniczona': 0.9, 'Rzadka': 0.45, 'Egzotyczna': 0.03}
D['import_egzotyczne'] = 0.06
D['opis'] = ('PG s. 290: szansa, że przedmiot jest w sprzedaży, wg wielkości osady. v6d (MG): Egzotyczne — 3% w metropolii, '
             '0,1% gdzie indziej, Marienburg (import) 6%. Altdorf i Marienburg: Rzadkie liczą się jak Ograniczone.')
D['obce_wies'] = 'Ograniczona'
D['obce_wies_opis'] = 'Kupiec innej rasy we wsi: jego własny towar (np. krasnoludzki u krasnoluda) dostępny jak Ograniczony.'
JK = RY['jakosc']
JK['osada_zalety'] = {'wioska': 0.5, 'miasteczko': 0.8, 'miasto': 1, 'metropolia': 1.2}
JK['osada_zalety_opis'] = 'Szansa na Zalety przedmiotu × ten mnożnik wg osady (we wsi rzadziej, w metropolii częściej).'
RY['gospoda'] = {
    'opis': 'v6d: nocleg, posiłek i stajnia nie są towarem kupca, ale cena zależy od miejsca: osada × standard gospody (szacunek MG).',
    'standardy': [{'id': 'podla', 'nazwa': 'Podła spelunka', 'mnoznik': 0.6}, {'id': 'zwykla', 'nazwa': 'Zwykła gospoda', 'mnoznik': 1},
                  {'id': 'dobra', 'nazwa': 'Dobra gospoda', 'mnoznik': 1.8}, {'id': 'wytworna', 'nazwa': 'Wytworny zajazd', 'mnoznik': 3.5}]}
W('data/rynek.json', RY)

H = J('data/handel.json')
for w in H['wahania']['lista']:
    w['dostepnosc'] = {'stabilny': 1, 'hossa': 0.7, 'bessa': 1.3}[w['id']]
H['wahania']['opis'] = ('Poradnik s. 39 (opcjonalnie): 1k10 przed testem popytu. Rynek Byka: towaru mniej (Dostępność ×0,7), drożej. '
                        'Rynek Niedźwiedzia: towaru więcej (×1,3), taniej. Mnożniki — szacunek MG.')
W('data/handel.json', H)
