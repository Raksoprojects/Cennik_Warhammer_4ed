# -*- coding: utf-8 -*-
"""v6d: decyzje MG z 2026-10-30. Idempotentny. Uruchamiaj po dane_v6c.py.

  1. data/cennik.json  ← źródło ze stroną (strona: PG z narzedzia/strony_pg.json, KR, WE), nielegalne +4,
                         lekki koń bojowy Ograniczona, rumak Rzadka
  2. data/osady.json   ← metropolie (Nuln, Talabheim, Middenheim, Altdorf, Marienburg, ogólna) z tabelą Dostępności „metropolia”,
                         Middenheim jako metropolia (MG: 15 000 z Poradnika nie ma sensu), Altdorf „Rzadkie o stopień łatwiej”,
                         Marienburg „import”, lokalne specjalności (tagi): Middenheim futra i żelazo, Nuln proch, Marienburg import
  3. data/rynek.json   ← Egzotyczne: 3% w metropolii, 0,1% gdzie indziej; wahania zmieniają też Dostępność;
                         Zalety rzadziej we wsi; krasnoludzki towar we wsi rzadziej; standard gospody (nocleg, posiłek)
  4. czynsze miesięczne i roczne
  5. rok = 50 tygodni (statusy), domyślna sytuacja osad północy, Dostępność 15 pozycji
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
         uwaga='')
O['altdorf']['rzadkie_latwiej'] = True
O['altdorf']['uwaga'] = 'Rzadkie o stopień łatwiej (szansa jak Ograniczonej).'
O['marienburg']['rzadkie_latwiej'] = True
O['marienburg']['import'] = True
O['marienburg']['uwaga'] = 'Wszystko z importu: Rzadkie o stopień łatwiej, Egzotyczne częściej niż w innych metropoliach.'
# v6e: źródła dochodu ośrodków — kolumna „Dochody” z indeksów geograficznych Dziedzictwa Sigmara (WFRP 2 ed., rozdz. VI,
# stan na 2522 KI, te same miasta co tab. 3-2 Poradnika). „Handel” i „administracja” nie zmieniają cen.
DOCHODY = {
    'altdorf': 'handel, administracja', 'miasto-carroburg': 'handel, szkło i ceramika', 'miasto-bogenhafen': 'handel, wino, drewno',
    'miasto-helmgart': 'handel, rudy metali', 'miasto-ubersreik': 'handel, rudy i obróbka metali', 'miasto-weissbruck': 'handel, transport',
    'miasto-kemperbad': 'handel, wino, brandy', 'miasto-auerswald': 'handel, rudy metali', 'miasto-grunburg': 'handel, szkutnictwo',
    'miasto-stimmigen': 'handel, uprawy', 'miasto-nuln': 'handel, metalurgia, administracja, wino', 'miasto-ambosstein': 'handel, uprawy',
    'miasto-furtzhausen': 'handel, uprawy', 'miasto-kotzenheim': 'handel, uprawy, rybołówstwo',
    'miasto-wissenburg': 'administracja, handel, rudy metali', 'miasto-pfeildorf': 'handel, rybołówstwo, ubrania',
    'miasto-geschburg': 'uprawy, handel, hodowla', 'miasto-kreutzhofen': 'uprawy, handel', 'miasto-kroppenleben': 'handel, futra',
    'miasto-wuppertal': 'handel, uprawy, wyroby drewniane', 'miasto-wusterburg': 'uprawy, handel',
    'miasto-averheim': 'handel, administracja, bydło, uprawy', 'miasto-wurtbad': 'handel, administracja, uprawy, wino',
    'miasto-gersdorf': 'handel, drewno, rybołówstwo', 'miasto-hocheleben': 'handel, futra, rudy metali',
    'miasto-krugenheim': 'handel, uprawy, rybołówstwo', 'miasto-pfungzig': 'uprawy, bydło, handel', 'miasto-streissen': 'uprawy, handel, wino',
    'miasto-eicheschatten': 'uprawy, handel, piwo, administracja', 'miasto-schramleben': 'handel, piwo, bydło',
    'miasto-waldenhof': 'handel, administracja, uprawy', 'miasto-talabheim': 'handel, administracja, uprawy',
    'miasto-ahlenhof': 'drewno, handel, uprawy, bydło', 'miasto-hergig': 'handel, administracja, drewno, uprawy',
    'miasto-kusel': 'handel, administracja, uprawy, rybołówstwo', 'miasto-talagaad': 'rybołówstwo, uprawy, drewno, handel',
    'miasto-bechafen': 'handel, administracja, drewno, uprawy, budowa łodzi', 'miasto-wolfenburg': 'handel, drewno, administracja, wyroby z cyny',
    'miasto-wurzen': 'bydło, drewno, handel, ser', 'miasto-salzenmund': 'handel, administracja, wyroby drewniane',
    'miasto-ferlangen': 'antyki, handel, drewno', 'miasto-grafenrich': 'drewno, handel', 'miasto-neue-emskrank': 'handel, rybołówstwo, drewno',
    'miasto-norden': 'rybołówstwo, handel, bursztyn, transport więźniów', 'miasto-middenheim': 'handel, usługi, administracja',
    'miasto-beeckerhoven': 'drewno, handel', 'miasto-delberz': 'wino, drewno', 'miasto-schoninghagen': 'drewno, handel',
    'miasto-scheinfeld': 'handel, uprawy, rybołówstwo', 'miasto-schilderheim': 'handel, rybołówstwo, uprawy',
}
# Słowo z „Dochodów” → tagi branż (cennik → branze) i mnożnik ceny. Szacunek MG.
Z_DOCHODU = [
    (('rudy', 'metal', 'żelazo'), {'warsztatowe': 0.92, 'prosta': 0.95, 'wojskowa': 0.95, 'tarcze': 0.95}),
    (('wino', 'brandy', 'piwo'), {'trunki': 0.85}),
    (('uprawy', 'bydło', 'hodowla', 'rybołówstwo', 'ser'), {'zywnosc': 0.92, 'zboze': 0.92}),
    (('ubrania', 'wełna'), {'odziez': 0.92, 'tkaniny': 0.9}),
    (('futra',), {'futra': 0.8, 'mysliwska': 0.95}),
    (('drewn', 'cyny', 'szkło'), {'domowe': 0.92, 'pojemniki': 0.92}),
    (('bursztyn', 'srebro'), {'kosztownosci': 0.9}),
]
# Ręcznie (MG i Zbrojownia Starego Świata s. 13) — nadpisują wyliczone z „Dochodów”.
TAGI = {
    'miasto-middenheim': {'futra': 0.8, 'warsztatowe': 0.9, 'prosta': 0.92, 'wojskowa': 0.92, 'tarcze': 0.92,
                          'zywnosc': 1.1, 'zboze': 1.1},   # ZSŚ: okoliczne wsie ledwie wykarmiają miasto
    'miasto-nuln': {'prochowa': 0.85, 'eksperymentalna': 0.85, 'warsztatowe': 0.92, 'trunki': 0.9},
    'marienburg': {'kolonialne': 0.8, 'luksus': 0.9, 'tkaniny': 0.9},
    'miasto-hergig': {'futra': 0.85, 'mysliwska': 0.95},       # ZSŚ: łowcy i myśliwi z Hochlandu i Talabeklandu
    'miasto-kusel': {'futra': 0.85, 'mysliwska': 0.95},
    'miasto-talabheim': {'futra': 0.85, 'mysliwska': 0.95},
    'miasto-eicheschatten': {'zywnosc': 0.85, 'tkaniny': 0.92},  # ZSŚ: najlepsze mięso i wełna w Krainie Zgromadzenia
}
for o in OS['osady']:
    o.pop('tagi', None); o.pop('dochody', None)
    t = {}
    if o['id'] in DOCHODY:
        o['dochody'] = DOCHODY[o['id']]
        for slowa, tagi in Z_DOCHODU:
            if any(s in o['dochody'] for s in slowa): t.update(tagi)
    t.update(TAGI.get(o['id'], {}))
    if t: o['tagi'] = t
# Populacje kampanii (MG, 2525 KI): liczby z Poradnika są za małe jak na skalę Imperium. Wartość z Poradnika zostaje obok.
# Pozostałe ośrodki: Poradnik × 5. Typ osady (a więc ceny) zostaje z liczb Poradnika (dane_v6c.py) — progi w skali kampanii:
# wieś < 5 000, miasteczko < 50 000, miasto < 250 000, metropolia więcej.
SKALA_POP = 5
# Uzasadnienie (2026-10-31): Imperium ≈ Święte Cesarstwo × 5 (80–100 mln, ok. 10% w miastach); największa stolica ≈ 1% ludności.
# Middenheim: 95 000 sprzed wojny × 5 = 475 000; oblężenie −20–30% (Paryż 1590, Lejda 1574), uchodźcy +20–40%, 3 lata głodu −10%.
POPULACJA_MG = {'miasto-middenheim': 400000, 'altdorf': 900000, 'miasto-nuln': 700000, 'marienburg': 1000000}
POPULACJA_PORADNIK = {'altdorf': 105000, 'marienburg': 135000}   # osady ogólne nie mają liczby z tab. 3-2 w osady.json
# Przed Burzą Chaosu (Dziedzictwo Sigmara, uwagi w indeksach) × 5. Splądrowane miasta zostają na poziomie z 2522 × 5.
PRZED_WOJNA = {'miasto-middenheim': 95000, 'miasto-carroburg': 8000, 'miasto-delberz': 2000, 'miasto-ahlenhof': 2200,
               'miasto-wolfenburg': 8900, 'miasto-hergig': 9200, 'miasto-ferlangen': 2500}
for o in OS['osady']:
    if o.get('populacja') and o['id'] not in POPULACJA_MG:
        o['populacja_poradnik'] = o.get('populacja_poradnik', o['populacja'])
        o['populacja'] = o['populacja_poradnik'] * SKALA_POP
for i, p in POPULACJA_MG.items():
    O[i]['populacja_poradnik'] = O[i].get('populacja_poradnik') or O[i].get('populacja') or POPULACJA_PORADNIK.get(i)
    O[i]['populacja'] = p
for o in OS['osady']: o.pop('populacja_przed_wojna', None)
for i, p in PRZED_WOJNA.items(): O[i]['populacja_przed_wojna'] = p * SKALA_POP
O['altdorf']['uwaga'] = 'Ok. 900 000 mieszkańców (MG; Poradnik: 105 000). Rzadkie o stopień łatwiej (szansa jak Ograniczonej).'
O['marienburg']['uwaga'] = ('Ok. 1 000 000 mieszkańców (MG). Wszystko z importu: Rzadkie o stopień łatwiej, '
                            'Egzotyczne częściej niż w innych metropoliach.')
O['miasto-middenheim']['uwaga'] = ('MG (2525 KI): ok. 400 000 — przed wojną 475 000 (95 000 × 5, Dziedzictwo Sigmara s. 70), '
                                    'oblężenie 2522 −20–30%, uchodźcy z Middenlandu +20–40%, głód −10%. Poradnik: 15 000. '
                                    'Futra i żelazo z Middenlandu tanie, żywność droga.')
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
# v6e: wyroby rzemieślnicze taniej w mieście (warsztaty, materiał na miejscu), żywność i zwierzęta taniej na wsi. Zakres 0,8–1,2 (MG).
WYROBY = ['Broń biała', 'Broń zasięgowa', 'Amunicja', 'Pancerze', 'Ubranie i dodatki', 'Narzędzia i zestawy',
          'Księgi i dokumenty', 'Wyposażenie różne', 'Protezy']
TYP = {'wioska': (1.2, 0.85, 0.9), 'miasteczko': (1, 1, 1), 'miasto': (0.9, 1.05, 1.05), 'metropolia': (0.8, 1.15, 1.1)}
RY['typ_osady'] = {
    'opis': 'v6e: mnożnik kategorii wg wielkości osady (klucz = osady → dostepnosc). Działa razem z mnożnikiem osady: '
            'wyroby rzemieślnicze w metropolii taniej niż na wsi, żywność odwrotnie. Szacunek MG, zakres 0,8–1,2.',
    'kategorie': {typ: {**{k: w for k in WYROBY}, 'Jedzenie, picie, nocleg': z, 'Zwierzęta i pojazdy': z, 'Zioła, mikstury, narkotyki': zi}
                  for typ, (w, z, zi) in TYP.items()}}
W('data/rynek.json', RY)

# ---------------------------------------------------------------- 4. czynsze (MG 2026-10-31)
# Miesiąc (33 dni, ponad 4 tygodnie) ≈ 3,5 × tydzień (rabat 15% za dłuższy najem), rok ≈ 10,8 × miesiąc (rabat 10%).
# Zbrojownia Starego Świata s. 91: najem domu 8–10% jego wartości rocznie — rząd wielkości się zgadza.
NAJEM = {  # kwatera: (tydzień, miesiąc, rok) w pensach
    'Kąt w izbie czeladnej': (24, 84, 900), 'Izba na poddaszu': (36, 120, 1200), 'Izba w kamienicy': (96, 336, 3600),
    'Mieszkanie mieszczańskie (2–3 izby)': (144, 504, 5280), 'Dom mistrza z warsztatem': (288, 1008, 10800),
    'Kamienica kupiecka': (720, 2520, 26400)}
CZ = J('data/czynsze.json')
for k in CZ['najem']: k['tydzien_p'], k['miesiac_p'], k['rok_p'] = NAJEM[k['kwatera']]
CZ['opis'] = CZ['opis'].split(' v6d:')[0] + ' v6d: miesiąc ≈ 3,5 × tydzień, rok ≈ 10,8 × miesiąc (decyzja MG).'
W('data/czynsze.json', CZ)
OKRES = {'tydzień': 0, 'miesiąc': 1, 'rok': 2}
C = J('data/cennik.json')
for c in C['pozycje']:
    if c['kat'] != 'Czynsze i mieszkanie' or ' / ' not in c['nazwa']: continue
    kw, okres = c['nazwa'].split(' / ')
    nowa = next(v[OKRES[okres]] for n, v in NAJEM.items() if n.startswith(kw))
    c['cena_ref_p'] = round(c['cena_ref_p'] * nowa / c['cena_p'])   # cena_ref = przed mnożnikiem klasy cenowej
    c['cena_p'] = nowa
W('data/cennik.json', C)

H = J('data/handel.json')
for w in H['wahania']['lista']:
    w['dostepnosc'] = {'stabilny': 1, 'hossa': 0.7, 'bessa': 1.3}[w['id']]
H['wahania']['opis'] = ('Poradnik s. 39 (opcjonalnie): 1k10 przed testem popytu. Rynek Byka: towaru mniej (Dostępność ×0,7), drożej. '
                        'Rynek Niedźwiedzia: towaru więcej (×1,3), taniej. Mnożniki — szacunek MG.')
W('data/handel.json', H)

# ---------------------------------------------------------------- 5. decyzje MG 2026-10-31
# Rok imperialny = 400 dni = 50 tygodni po 8 dni (było 52). Robota liczy dalej 6 dniówek: to tydzień pracy, nie kalendarzowy.
TYG = 50
ST = J('data/statusy.json')
ST['tygodni_w_roku'] = TYG
ST['opis'] = ST['opis'].split(' Netto = ')[0] + (' Netto = rzut za jedną Robotę; brutto = 5 × netto; rok = brutto × 50 '
             '(rok imperialny: 400 dni = 50 tygodni po 8 dni). Kotwica robotnika: 6 dniówek — tydzień pracy, nie kalendarzowy.')
for s in ST['poziomy']: s['netto_rok'], s['brutto_rok'] = s['netto_p'] * TYG, s['brutto_p'] * TYG
W('data/statusy.json', ST)

# Domyślna sytuacja osady: północ po Burzy Chaosu (kampania 2525 KI). Ustawia się przy wyborze osady; MG może ją zmienić.
SPLADROWANE = ['miasto-wolfenburg', 'miasto-hergig', 'miasto-ferlangen', 'miasto-delberz', 'miasto-ahlenhof']
UCHODZCY = ['miasto-middenheim', 'miasto-carroburg']
POLNOC = ('Middenland', 'Hochland', 'Ostland', 'Nordland', 'Ostermark')
OS = J('data/osady.json')
for o in OS['osady']:
    o.pop('sytuacja', None)
    if o['id'] in SPLADROWANE: o['sytuacja'] = 'wojna'          # zgliszcza, bandy zwierzoludzi, garnizony
    elif o['id'] in UCHODZCY: o['sytuacja'] = 'naplyw'          # odbudowa, uchodźcy z prowincji
    elif o.get('prowincja') in POLNOC: o['sytuacja'] = 'braki'  # spalone wsie, niepewne drogi
W('data/osady.json', OS)

# Pozycje bez Dostępności (DANE.md p. 12) — decyzja MG.
DOST = {'Powszechna': ['owca-baran', 'swinia', 'krowa', 'wol', 'prowiant-wojskowy-na-1-tydzien', 'oselka', 'cieciwa'],
        'Ograniczona': ['bandolier', 'lont-prochowy-1-m', 'focza-skora'],
        'Rzadka': ['stroj-ceremonialny-aksamit-zlotoglow-futra', 'jedwabna-bielizna', 'kompas', 'teodolit', 'strusie-pioro']}
C = J('data/cennik.json'); P = {c['id']: c for c in C['pozycje']}
for dost, ids in DOST.items():
    for i in ids: P[i]['dostepnosc'] = dost
W('data/cennik.json', C)
