# -*- coding: utf-8 -*-
"""v6c: handel wg Poradnika Staroświatowca (data/handel.json → osady, cennik, kupcy). Idempotentny.

  1. data/osady.json  ← ośrodki handlu z tab. 3-2: typ osady z populacji (<1000 wieś, <10 000 miasteczko, <50 000 miasto,
                        więcej metropolia), mnożnik = mnożnik typu × zamożność, ceny kategorii wg strefy handlowej
                        (siatka „Dostępność towarów handlowych”, s. 41). Altdorf i Marienburg dostają strefę i zamożność.
  2. data/cennik.json ← nielegalny: true dla narkotyków i trucizn
  3. data/kupcy.json  ← paser handluje nielegalnym towarem
Uruchom z katalogu repo: py narzedzia/dane_v6c.py && npm test
"""
import json, os, re, unicodedata
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
J = lambda f: json.load(open(R + f, encoding='utf-8'))
def W(f, d): json.dump(d, open(R + f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print('zapisano', f)
def slug(s):
    s = unicodedata.normalize('NFD', s.lower().replace('ł', 'l')).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')

H = J('data/handel.json')
ST = H['stopnie']
STREFY = {s['id']: s for s in H['strefy']}
# v6d: strefa daje ODCHYLENIE od średniej Imperium (inaczej rzeczy rzadkie wszędzie, np. zioła, drożałyby w całym kraju).
# Cena = 1 − krok × (stopień strefy − średni stopień Imperium dla tej kategorii), w granicach [min, max].
KROK, LO, HI = H['strefa_cena']['krok'], H['strefa_cena']['min'], H['strefa_cena']['max']
def stopien(sid, kat):
    st = dict(zip(H['towary_poradnika'], STREFY[sid]['siatka'].split()))
    towary = H['kategorie_z_towarow'][kat]
    return sum(ST.index(st[t]) for t in towary) / len(towary)
KATY = [k for k in H['kategorie_z_towarow'] if k != 'opis']
SREDNIA = {k: sum(stopien(s, k) for s in STREFY) / len(STREFY) for k in KATY}
def ceny_strefy(sid):
    return {k: {'cena': round(min(HI, max(LO, 1 - KROK * (stopien(sid, k) - SREDNIA[k]))), 3)} for k in KATY}

OS = J('data/osady.json')
TYP = {o['id']: o for o in OS['osady'] if not o['id'].startswith('miasto-')}
ZAMOZ = {'wies': 2, 'miasteczko': 3, 'miasto': 3, 'metropolia': 4, 'altdorf': 5, 'marienburg': 5}
STREFA_TYPU = {'altdorf': 'reik', 'marienburg': 'marienburg'}
for o in TYP.values():
    o['zamoznosc'] = ZAMOZ.get(o['id'], 3)
    o.pop('kategorie', None); o.pop('strefa', None)
    if o['id'] in STREFA_TYPU:
        o['strefa'] = STREFA_TYPU[o['id']]
        o['kategorie'] = ceny_strefy(o['strefa'])
nowe = []
for nazwa, pop, zam, prow, strefa, wolne in H['miasta']:
    if nazwa in ('Altdorf', 'Marienburg'): continue
    typ = 'wies' if pop < 1000 else 'miasteczko' if pop < 10000 else 'miasto' if pop < 50000 else 'metropolia'
    t = TYP[typ]
    o = {'id': 'miasto-' + slug(nazwa), 'nazwa': nazwa, 'grupa': STREFY[strefa]['nazwa'],
         'mnoznik': round(t['mnoznik'] * H['zamoznosc']['mnoznik_cen'][str(zam)], 3), 'limit_p': t['limit_p'],
         'dostepnosc': t['dostepnosc'], 'typ': typ, 'populacja': pop, 'zamoznosc': zam, 'prowincja': prow, 'strefa': strefa,
         'wolne_miasto': wolne, 'kategorie': ceny_strefy(strefa)}
    if 'limit_omijaja_podtypy' in t: o['limit_omijaja_podtypy'] = t['limit_omijaja_podtypy']
    if wolne: o['uwaga'] = 'Wolne miasto.'
    nowe.append(o)
OS['osady'] = list(TYP.values()) + nowe
OS['opis'] = ('Osady. v6c: ośrodki handlu z Poradnika Staroświatowca (tab. 3-2) — mnożnik = typ osady × zamożność, '
              'kategorie = ceny wg strefy handlowej (narzedzia/dane_v6c.py, data/handel.json).')
W('data/osady.json', OS)

C = J('data/cennik.json')
NIELEGALNE = {'rozkosz-ranalda', 'grzybki-szalonego-kapelusznika', 'dziwnokorzen', 'czarny-lotos', 'sercoboj'}
for c in C['pozycje']:
    c.pop('nielegalny', None)
    if c['id'] in NIELEGALNE: c['nielegalny'] = True
W('data/cennik.json', C)

KU = J('data/kupcy.json')
for k in KU['kupcy']:
    k.pop('nielegalne', None)
    if k['id'] == 'paser':
        k['nielegalne'] = True   # nielegalny towar dolosowuje generator osobnym przebiegiem (bez zmiany kategorii)
        if 'Zioła, mikstury, narkotyki' in k['boczne']: k['boczne'].remove('Zioła, mikstury, narkotyki')
W('data/kupcy.json', KU)
