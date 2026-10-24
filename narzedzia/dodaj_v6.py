# -*- coding: utf-8 -*-
"""v6: broń z podręczników ras + Zalety i Wady broni (zadanie T11).

Co robi (idempotentnie):
  1. data/cennik.json        ← 11 broni: Podręcznik Gracza „Krasnoludy” (s. 93–94), „Wysokie Elfy” (s. 31).
                                cena_ref_p = RAW × (×1 / RAW) najbliższego ludzkiego odpowiednika z cennika,
                                cena_p = cena_ref_p × mnożnik klasy presetu domyślnego (jak zastosujPreset w JS).
  2. data/klasy_cenowe.json  ← klasy nowych pozycji.
  3. data/bron_cechy.json    ← grupa, obrażenia, zasięg, Zalety i Wady z Generator_NPC/public/data/weapons.json
                                (polskie nazwy z podręcznika głównego i „Pod Bronią”).
Uruchom z katalogu repo: py narzedzia/dodaj_v6.py && npm test
"""
import json, math, os, re, unicodedata
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
J = lambda f: json.load(open(R + f, encoding='utf-8'))
def W(f, d): json.dump(d, open(R + f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print('zapisano', f)
def ladna(p):  # identyczne z zastosujPreset w src/silnik.js
    r = lambda x: math.floor(x + 0.5)
    if p < 24: return max(1, r(p))
    if p < 240: return int(r(p / 6) * 6)
    if p < 2400: return int(r(p / 12) * 12)
    return int(r(p / 60) * 60)
def slug(s):
    s = s.lower().replace('ł', 'l')
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')

C, K = J('data/cennik.json'), J('data/klasy_cenowe.json')
P = {c['id']: c for c in C['pozycje']}
ZK = 240
# (nazwa, kat, źródło, RAW w ZK, obc, dostępność, klasa, odpowiednik)
NOWE = [
    ('Krasnoludzki topór', 'Broń biała', 'KR', 1, 1, 'Powszechna', 'bron', 'bron-reczna-topor-maczuga'),
    ('Krasnoludzki młot bojowy', 'Broń biała', 'KR', 1, 1, 'Powszechna', 'bron', 'bron-reczna-topor-maczuga'),
    ('Wirujące ostrza śmierci', 'Broń biała', 'KR', 5, 2, 'Rzadka', 'bron', 'kiscien'),
    ('Krasnoludzki wielki topór', 'Broń biała', 'KR', 4, 3, 'Powszechna', 'bron', 'wielki-topor'),
    ('Krasnoludzki wielki młot', 'Broń biała', 'KR', 4, 3, 'Powszechna', 'bron', 'mlot-bojowy'),
    ('Krasnoludzki kilof', 'Broń biała', 'KR', 1, 3, 'Powszechna', 'bron', 'bron-reczna-topor-maczuga'),
    ('Krasnoludzka kusza', 'Broń zasięgowa', 'KR', 5, 2, 'Powszechna', 'bron', 'kusza'),
    ('Krasnoludzka hakownica', 'Broń zasięgowa', 'KR', 6, 2, 'Rzadka', 'palna', 'arkebuz'),
    ('Krasnoludzki pistolet', 'Broń zasięgowa', 'KR', 12, 0, 'Rzadka', 'palna', 'pistolet'),
    ('Krasnoludzki topór do rzucania', 'Broń zasięgowa', 'KR', 1, 1, 'Powszechna', 'bron', 'topor-do-rzucania'),
    ('Wielki miecz Hoetha', 'Broń biała', 'WE', 2000, 2, 'Egzotyczna', 'bron', 'miecz-dwureczny'),
]
ZRODLA = {'KR': 'Podręcznik Gracza „Krasnoludy”, s. 93–94', 'WE': 'Podręcznik Gracza „Wysokie Elfy”, s. 31'}
pr = K['presety'][K['domyslny']]
for nazwa, kat, zr, raw_zk, obc, dost, klasa, wzor in NOWE:
    i, raw, w = slug(nazwa), raw_zk * ZK, P[wzor]
    ref = round(raw * w['cena_ref_p'] / w['cena_raw_p'])
    poz = dict(id=i, kat=kat, nazwa=nazwa, zrodlo=zr, cena_raw_p=raw, cena_p=ladna(ref * pr['mnozniki'][klasa]),
               obc=obc, dostepnosc=dost, podstawa_hist='',
               komentarz=f'{ZRODLA[zr]}. Poziom ×1 w tej samej proporcji do RAW co „{w["nazwa"]}”.',
               dopisane='2026-10-24', uwagi_danych='v6: dopisane na prośbę MG (broń z weapons.json bez wpisu w cenniku).',
               pozycja_kampanii=False, typ='towar', podtyp=None, cena_ref_p=ref, klasa=klasa)
    if i == 'wielki-miecz-hoetha':
        poz['komentarz'] += ' Broń unikatowa (Dostępność: Unikatowa) — praktycznie nie do kupienia.'
    K['klasy'][i] = klasa
    if i in P: P[i].update(poz)
    else:
        j = max(k for k, c in enumerate(C['pozycje']) if c['kat'] == kat)
        C['pozycje'].insert(j + 1, poz); P[i] = poz
W('data/cennik.json', C)
W('data/klasy_cenowe.json', K)

# ---------------------------------------------------------------- Zalety i Wady
WB = J('../Generator_NPC/public/data/weapons.json') if os.path.exists(R + '../Generator_NPC/public/data/weapons.json') else None
if WB:
    ALIAS = {'bron-reczna-topor-maczuga': 'Topór', 'tarcza-puklerz': 'Puklerz', 'tarcza-duza': 'Tarcza duża',
             'nadziak-dwureczny': 'Nadziak', 'muszkiet-kaliwer': 'Arkebuz'}
    zrodlo = {**{n: ('Broń biała', v) for n, v in WB['melee'].items()}, **{n: ('Broń zasięgowa', v) for n, v in WB['ranged'].items()}}
    poSlug = {slug(n): n for n in zrodlo}
    B = J('data/bron_cechy.json')
    istn = {p['id']: p for p in B['pozycje']}
    for c in C['pozycje']:
        if c['kat'] not in ('Broń biała', 'Broń zasięgowa'): continue
        n = ALIAS.get(c['id']) or poSlug.get(c['id'])
        if not n: continue
        v = zrodlo[n][1]
        p = istn.get(c['id']) or dict(id=c['id'], nazwa=c['nazwa'], kat=c['kat'], zrodlo=c['zrodlo'], wyjatek=None, uwagi=None)
        p.update(grupa=v.get('group'), obrazenia=('+SB+' if v.get('sb') else '+') + str(v.get('damage')),
                 zasieg=v.get('reach') or v.get('range'), zalety=[{'nazwa': q} for q in v.get('qualities', [])],
                 wady=[{'nazwa': q} for q in v.get('flaws', [])], wzor_cech=n)
        if c['id'] not in istn: B['pozycje'].append(p); istn[c['id']] = p
    B['opis'] = ('Cechy broni do testu „więcej Zalet = nie taniej” (test/bron_cechy.test.mjs). v6: uzupełnione z '
                 'Generator_NPC/public/data/weapons.json (nazwy z polskiego podręcznika głównego i „Pod Bronią”); '
                 'wzor_cech = nazwa w tamtym pliku. wyjatek: tekst, gdy cena celowo łamie regułę (znak stanu, egzotyka, materiał).')
    B.pop('grupy_podpowiedz', None)
    W('data/bron_cechy.json', B)

# ---------------------------------------------------------------- kupcy: wozy na zamówienie, jakość towaru
# Decyzja MG (2026-10-24): wóz robi kowal albo kołodziej, wieś zbiera się razem i daje drewno i materiały.
# Decyzja MG: generator losuje jakość wg kupca — mistrz cechu i płatnerz Zalety, paser i domokrążca Wady.
KU = J('data/kupcy.json')
P_WOZY = ['furmanka', 'woz']
KOLODZIEJ = dict(id='kolodziej', nazwa='Kołodziej / cieśla wiejski', status='Brąz 5', marza=0.9, limit_p=1920,
                 rdzen=['Narzędzia i zestawy'], boczne=['Wyposażenie różne'], robota=['Narzędzia i zestawy'],
                 robota_pozycje=P_WOZY, skup=0.35, towar_tyg=10, gotowka_tyg=3,
                 opis='Koła, osie, wozy i beczki. Wóz robi na zamówienie; wieś zwykle składa się na niego i daje drewno.')
if not any(k['id'] == 'kolodziej' for k in KU['kupcy']): KU['kupcy'].append(KOLODZIEJ)
JAKOSC = {  # szansa na pozycję: Zalety / Wady przedmiotu (szacunek MG do korekty w kupcy.json)
    'mistrzcechu': (0.35, 0), 'platnerz': (0.25, 0), 'blawatny': (0.2, 0), 'rzemieslnik': (0.1, 0.05),
    'zbrojmistrz': (0.1, 0.05), 'rusznikarz': (0.1, 0.05), 'kolodziej': (0.05, 0.1), 'kowal': (0.05, 0.1),
    'kramarz': (0, 0.15), 'kwatermistrz': (0.05, 0.15), 'paser': (0.05, 0.3), 'domokrazca': (0, 0.35)}
for k in KU['kupcy']:
    if k['id'] == 'kowal': k['robota_pozycje'] = P_WOZY
    if k['id'] in JAKOSC: k['jakosc'] = dict(zip(('zalety', 'wady'), JAKOSC[k['id']]))
KU['opis'] = KU['opis'].split(' v6:')[0] + (' v6: robota_pozycje = id pozycji, które kupiec robi na zamówienie poza swoimi kategoriami'
    ' (wozy u kowala i kołodzieja); jakosc = szansa na pozycję z Zaletami / Wadami przedmiotu w sklepie.')
W('data/kupcy.json', KU)
