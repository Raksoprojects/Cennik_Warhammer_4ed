# -*- coding: utf-8 -*-
"""v6b: decyzje MG z 2026-10-25. Idempotentny — można uruchamiać wiele razy.

  1. data/cennik.json   ← branze (czym handluje kto), pochodzenie (krasnoludzkie / elfie), miecz 3 ZK,
                          tatuaż = usługa, Piwo Bugmana Rzadkie (u ludzi rzadko, u krasnoludów normalnie)
  2. data/kupcy.json    ← branze kupców (kategoria → tagi), kupiec krasnoludzki, jakość wg kategorii (ubrania u kramarza z Wadami)
  3. data/koniunktura.json ← napływ ludzi, braki w dostawach, kryzys, dobry sezon
  4. data/rynek.json    ← jakość ×1,6 / ×0,6, targowanie −4%/PS do −24%, Dostępność wg PG s. 290, rzadkość w zamówieniu
  5. data/osady.json    ← typ osady do tabeli Dostępności (wioska / miasteczko / miasto)
  6. data/statusy.json  ← opisy Złota (szczyt drabiny = arystokracja, dochód to przybliżenie po wydatkach stanu)
Uruchom z katalogu repo: py narzedzia/dane_v6b.py && npm test
"""
import json, math, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
J = lambda f: json.load(open(R + f, encoding='utf-8'))
def W(f, d): json.dump(d, open(R + f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print('zapisano', f)
def ladna(p):  # identyczne z zastosujPreset w src/silnik.js
    r = lambda x: math.floor(x + 0.5)
    if p < 24: return max(1, r(p))
    if p < 240: return int(r(p / 6) * 6)
    if p < 2400: return int(r(p / 12) * 12)
    return int(r(p / 60) * 60)

# ---------------------------------------------------------------- 1. branże przedmiotów
# Tag = czym handluje sklep. Kupiec z `branze` dla danej kategorii bierze z niej tylko pozycje z tymi tagami.
B = {
    # Narzędzia i zestawy
    'rolnicze': 'sierp motyka grabie szpadel siekiera drag-3-m kilof sidla-na-zwierzeta',
    'warsztatowe': 'narzedzia-pracy warsztat mlotek pila dluto gwozdzie-12 lom stalowe-szczypce oselka kolek kajdany klucz',
    'linowe': 'lina-10-metrow kotwiczka bosak haczyki-na-ryby-12',
    'domowe': 'wiadro miotla mop szczotka-do-podlogi kociolek-do-gotowania patelnia miska talerz kubek kufel-cynowy sztucce oliwa-litr',
    'aptekarskie': 'mozdzierz-z-tluczkiem pinceta zestaw-na-zatrucia',
    'pisarskie': 'pioro-do-pisania pedzel-do-malowania zestaw-do-pisania grawerowana-pieczec mlotek-sedziego liczydlo tuba-na-zwoje kreda-wegiel-do-rysowania afisz',
    'naukowe': 'soczewki-do-czytania teleskop kompas teodolit',
    'toaletowe': 'grzebien lusterko-reczne narzedzie-do-czyszczenia-uszu',
    'zlodziejskie': 'wytrychy zestaw-do-charakteryzacji',
    'strzeleckie': 'bandolier cieciwa lont-prochowy-1-m',
    'medyczne': 'kule bandaz szmaty',
    # Wyposażenie różne
    'oswietlenie': 'swiece-tuzin zapalka lampa-oliwna latarnia lampa-sztormowa lampa-davricha swieca-woskowa-sztuka olej-do-lampy-litr pudelko-na-hubke-i-krzesiwo',
    'podroz': 'koc zwijane-poslanie namiot plocienna-plandeka plecak juki buklak torba-na-ramie sakiewka worek duzy-worek',
    'pojemniki': 'beczka-145-l beczulka-45-l butelka dzban',
    'posciel': 'koc przescieradlo siennik recznik',
    'rozrywka': 'kosci-do-gry talia-kart instrument lalka pilka fajka-i-tyton',
    # Ubranie i dodatki
    'odziez': 'ubranie buty wysokie-buty plaszcz oponcza kapelusz kaptur-lub-maska rekawiczki szata mundur kostium',
    'luksus': 'stroj-dworski stroj-ceremonialny-aksamit-zlotoglow-futra laska perfumy puder-do-twarzy zapinki-6 jedwabna-bielizna strusie-pioro',
    'kosztownosci': 'berlo sygnet pierscien-srebrny pierscien-zloty pierscien-z-klejnotem',
    'dewocjonalia': 'symbol-religijny amulet',
    'tkaniny': 'sukno-lokiec plotno-lokiec sukno-szare-lokiec plotno-zgrzebne-lokiec',
    'futra': 'focza-skora',
    # Jedzenie, picie, nocleg
    'zywnosc': 'prowiant-na-1-dzien jedzenie-na-zimno-na-1-dzien chleb-zytni-bochenek mieso-kg jaja-kopa-60-szt sery-kopa-60-szt maslo-garniec-3-77-l groch-korzec-43-7-l prowiant-wojskowy-na-1-tydzien',
    'trunki': 'pol-litra-piwa pol-litra-mocnego-trunku kielich-wina butelka-wina beczulka-piwa-10-l pol-litra-piwa-bugmana',
    'zboze': 'zyto-cwiertnia pszenica-cwiertnia jeczmien-cwiertnia owies-cwiertnia-obrok',
    'kolonialne': 'pieprz-funt-0-4-kg cynamon-funt szafran-funt gozdziki-kamien cukier-kamien ryz-kamien migdaly-kamien rodzynki-kamien',
    'hurt': 'sledzie-beczka',
    # Broń biała
    'prosta': 'bron-reczna-topor-maczuga noz sztylet kostur palka topor buzdygan cep-bojowy wlocznia mlot-jednoreczny nadziak-jednoreczny',
    'tarcze': 'tarcza-puklerz tarcza tarcza-duza pawez',
    'wojskowa': 'miecz bulat szabla halabarda pika wielki-topor mlot-bojowy poltorak miecz-dwureczny flamberg korbacz kiscien partyzana-glewia sierpak szydlo topor-drzewcowy nadziak-dwureczny lapacz kolczasta-rekawica zamykana-rekawica mizerykordia',
    'szermiercza': 'floret rapier szpada lewak lamacz-mieczy',
    'rycerska': 'kopia lanca mlot-kawaleryjski',
    'zlodziejska': 'garota tluk kastet obciazona-siec',
    'krasnoludzka': 'krasnoludzki-topor krasnoludzki-mlot-bojowy wirujace-ostrza-smierci krasnoludzki-wielki-topor krasnoludzki-wielki-mlot krasnoludzki-kilof krasnoludzka-kusza krasnoludzka-hakownica krasnoludzki-pistolet krasnoludzki-topor-do-rzucania',
    'elfia': 'wielki-miecz-hoetha luk-elfi strzala-elfia-1',
    # Broń zasięgowa i amunicja
    'mysliwska': 'krotki-luk luk luk-dlugi proca proca-drzewcowa oszczep bolas arkan bicz noz-do-rzucania topor-do-rzucania strzalka',
    'kusze': 'kusza ciezka-kusza kusza-pistoletowa',
    'prochowa': 'rusznica garlacz muszkiet-kaliwer pistolet arkebuz rusznica-lontowa rusznica-dwulufowa garlacz-lontowy bomba ladunek-zapalajacy srut-i-proch-12 pocisk-i-proch-12 improwizowany-srut-i-proch-1 patron-12 precyzyjny-pocisk-i-proch szmelc-i-proch-12 duzy-pocisk-i-proch-12 pocisk-hakowy-1',
    'eksperymentalna': 'muszkiet-hochlandzki pieprzniczka rusznica-samopowtarzalna pistolet-samopowtarzalny gryfia-lapa halabarda-pistoletowa topor-pistoletowy laska-pistoletowa mozdzierz-reczny nasaczony-aqshy-proch-12',
    'amunicja_prosta': 'strzala-12 belt-12 pocisk-olowiany-12 pocisk-kamienny-12 strzala-przebijajaca-12 strzala-zabkowana-12',
    # bez Zalet i Wad przedmiotu w generatorze (materiał, coś do zużycia)
    'zuzywalne': 'olej-do-lampy-litr oliwa-litr swiece-tuzin swieca-woskowa-sztuka zapalka szmaty bandaz gwozdzie-12 kreda-wegiel-do-rysowania afisz lont-prochowy-1-m',
}
POCHODZENIE = {'krasnoludzkie': B['krasnoludzka'] + ' pol-litra-piwa-bugmana', 'elfie': B['elfia']}

C = J('data/cennik.json'); K = J('data/klasy_cenowe.json')
P = {c['id']: c for c in C['pozycje']}
for c in C['pozycje']: c.pop('branze', None); c.pop('pochodzenie', None)
for tag, ids in B.items():
    for i in ids.split():
        if i not in P: raise SystemExit(f'brak pozycji {i} (tag {tag})')
        P[i].setdefault('branze', []).append(tag)
for poch, ids in POCHODZENIE.items():
    for i in ids.split(): P[i]['pochodzenie'] = poch
# miecz 3 ZK (decyzja MG): ×1 = 3 ZK ÷ (broń ×2 × znak stanu ×1,5)
pr = K['presety'][K['domyslny']]
P['miecz']['cena_ref_p'] = 240
P['miecz']['cena_p'] = ladna(240 * pr['mnozniki']['bron'] * pr['premia_znak_stanu'])
P['miecz']['uwagi_danych'] = 'v6b: decyzja MG — miecz 3 ZK (×1 = 1 ZK).'
P['bulat']['cena_ref_p'] = 240
P['bulat']['cena_p'] = ladna(240 * pr['mnozniki']['bron'] * pr['premia_znak_stanu'])
P['bulat']['uwagi_danych'] = 'v6c: decyzja MG — bułat 3 ZK, jak miecz.'
# tatuaż to usługa, nie towar na półce
P['tatuaz']['typ'] = 'usluga'
# Piwo Bugmana: u ludzi rzadko, u krasnoludów zwykły trunek
P['pol-litra-piwa-bugmana']['dostepnosc'] = 'Rzadka'
W('data/cennik.json', C)

# ---------------------------------------------------------------- 2. kupcy
KU = J('data/kupcy.json')
BR = {
    'domokrazca': {'Wyposażenie różne': ['oswietlenie', 'podroz', 'rozrywka', 'medyczne', 'posciel'], 'Amunicja': ['amunicja_prosta'],
                   'Narzędzia i zestawy': ['domowe', 'linowe', 'toaletowe', 'rolnicze'], 'Ubranie i dodatki': ['odziez', 'dewocjonalia', 'tkaniny'],
                   'Jedzenie, picie, nocleg': ['zywnosc', 'trunki']},
    'kramarz': {'Jedzenie, picie, nocleg': ['zywnosc', 'trunki', 'zboze'], 'Wyposażenie różne': ['oswietlenie', 'podroz', 'pojemniki', 'posciel', 'rozrywka', 'medyczne'],
                'Ubranie i dodatki': ['odziez', 'dewocjonalia', 'tkaniny'], 'Narzędzia i zestawy': ['rolnicze', 'domowe']},
    'kowal': {'Narzędzia i zestawy': ['rolnicze', 'warsztatowe', 'domowe', 'linowe'], 'Broń biała': ['prosta', 'tarcze'], 'Amunicja': ['amunicja_prosta']},
    'kolodziej': {'Narzędzia i zestawy': ['rolnicze', 'warsztatowe'], 'Wyposażenie różne': ['pojemniki']},
    'rzemieslnik': {'Narzędzia i zestawy': ['warsztatowe', 'domowe', 'rolnicze', 'linowe'], 'Wyposażenie różne': ['oswietlenie', 'podroz', 'pojemniki', 'posciel'],
                    'Broń biała': ['prosta', 'tarcze'], 'Ubranie i dodatki': ['odziez']},
    'mistrzcechu': {'Narzędzia i zestawy': ['warsztatowe', 'pisarskie', 'naukowe', 'toaletowe', 'domowe'], 'Wyposażenie różne': ['oswietlenie', 'rozrywka', 'podroz'],
                    'Ubranie i dodatki': ['odziez', 'luksus', 'kosztownosci'], 'Broń biała': ['szermiercza', 'wojskowa']},
    'zbrojmistrz': {'Broń biała': ['prosta', 'wojskowa', 'szermiercza', 'tarcze', 'rycerska'], 'Broń zasięgowa': ['mysliwska', 'kusze', 'prochowa'],
                    'Amunicja': ['amunicja_prosta', 'prochowa'], 'Wyposażenie różne': ['podroz']},
    'platnerz': {'Broń biała': ['wojskowa', 'rycerska', 'tarcze', 'szermiercza']},
    'rusznikarz': {'Narzędzia i zestawy': ['warsztatowe', 'strzeleckie', 'naukowe'], 'Wyposażenie różne': ['oswietlenie', 'pojemniki']},
    'aptekarz': {'Wyposażenie różne': ['oswietlenie', 'pojemniki', 'medyczne'], 'Narzędzia i zestawy': ['aptekarskie', 'pisarskie', 'naukowe', 'medyczne']},
    'konie': {'Narzędzia i zestawy': ['rolnicze', 'linowe']},
    'blawatny': {'Wyposażenie różne': ['posciel', 'podroz']},
    'ksiegarz': {'Narzędzia i zestawy': ['pisarskie', 'naukowe'], 'Wyposażenie różne': ['oswietlenie', 'pisarskie']},
    'paser': {'Broń biała': ['prosta', 'wojskowa', 'szermiercza', 'zlodziejska'], 'Ubranie i dodatki': ['odziez', 'luksus', 'kosztownosci'],
              'Narzędzia i zestawy': ['zlodziejskie', 'warsztatowe', 'naukowe', 'toaletowe'], 'Broń zasięgowa': ['mysliwska', 'kusze', 'prochowa']},
    'kwatermistrz': {'Broń biała': ['prosta', 'wojskowa', 'tarcze'], 'Broń zasięgowa': ['mysliwska', 'kusze', 'prochowa'], 'Amunicja': ['amunicja_prosta', 'prochowa'],
                     'Jedzenie, picie, nocleg': ['zywnosc', 'trunki', 'zboze', 'hurt'], 'Wyposażenie różne': ['podroz', 'oswietlenie', 'pojemniki', 'medyczne', 'posciel']},
    'medyk': {'Narzędzia i zestawy': ['aptekarskie', 'medyczne']},
    'krasnolud': {'Broń biała': ['krasnoludzka', 'prosta', 'tarcze', 'wojskowa'], 'Narzędzia i zestawy': ['warsztatowe'],
                  'Broń zasięgowa': ['krasnoludzka', 'kusze', 'prochowa'], 'Jedzenie, picie, nocleg': ['trunki'], 'Amunicja': ['amunicja_prosta', 'prochowa']},
}
KRASNOLUD = dict(id='krasnolud', nazwa='Krasnoludzki kupiec (Dawi)', status='Srebro 3', rasa='krasnolud', marza=1.2, limit_p=36000,
                 rdzen=['Broń biała', 'Narzędzia i zestawy'], boczne=['Pancerze', 'Broń zasięgowa', 'Jedzenie, picie, nocleg', 'Amunicja'],
                 robota=['Broń biała', 'Narzędzia i zestawy', 'Pancerze'], skup=0.4, towar_tyg=10, gotowka_tyg=3,
                 jakosc={'zalety': 0.3, 'wady': 0},
                 opis='Kantor przy krasnoludzkiej kuźni. Towar porządny i drogi, targuje się zażarcie, ludziom nie ufa. Piwo Bugmana trzyma pod ladą.')
if not any(k['id'] == 'krasnolud' for k in KU['kupcy']): KU['kupcy'].append(KRASNOLUD)
# Ubrania u kramarza i domokrążcy: odzież dla gawiedzi — zwykle z Wadami (Brzydki, Nieporęczny…), u bławatnego porządna.
JAK_KAT = {'kramarz': {'Ubranie i dodatki': {'zalety': 0, 'wady': 0.7}}, 'domokrazca': {'Ubranie i dodatki': {'zalety': 0, 'wady': 0.7}},
           'rzemieslnik': {'Ubranie i dodatki': {'zalety': 0, 'wady': 0.3}}, 'blawatny': {'Ubranie i dodatki': {'zalety': 0.25, 'wady': 0}}}
# v6c: szansa na trefny towar; paser — większość z niewiadomego pochodzenia (dlatego skupuje tanio).
TREFNE = {'paser': (0.75, {'kradziony': 8, 'podrobka': 1, 'ukryta_wada': 1}), 'domokrazca': (0.12, None), 'kramarz': (0.06, None),
          'kwatermistrz': (0.08, {'kradziony': 3, 'ukryta_wada': 2, 'miara': 2}), 'mistrzcechu': (0.01, None), 'krasnolud': (0.01, None),
          'platnerz': (0.02, None), 'ksiegarz': (0.03, {'podrobka': 3, 'kradziony': 1})}
for k in KU['kupcy']:
    k.pop('trefne', None); k.pop('trefne_wagi', None)
    if k['id'] in TREFNE:
        k['trefne'] = TREFNE[k['id']][0]
        if TREFNE[k['id']][1]: k['trefne_wagi'] = TREFNE[k['id']][1]
    k['branze'] = BR.get(k['id'], {})
    k.pop('jakosc_kat', None)
    if k['id'] in JAK_KAT: k['jakosc_kat'] = JAK_KAT[k['id']]
KU['opis'] = KU['opis'].split(' v6b:')[0] + (' v6b: branze = { kategoria: [tagi] } — z tej kategorii kupiec bierze tylko pozycje z tymi tagami'
    ' (tagi w cennik.json → branze); bez wpisu = cała kategoria. jakosc_kat = szansa na Zalety / Wady dla jednej kategorii (nadpisuje jakosc).'
    ' rasa = krasnolud: towar krasnoludzki traktuje jak Powszechny.')
W('data/kupcy.json', KU)

# ---------------------------------------------------------------- 3. sytuacje
KO = J('data/koniunktura.json')
KATS = KO['kategorie']
def sytuacja(id, nazwa, opis_cen, opis_popytu, ceny, popyty, reszta, czynsz, uwaga):
    kat = {k: {'cena': ceny.get(k, reszta[0]), 'popyt': popyty.get(k, reszta[1])} for k in KATS}
    return dict(id=id, nazwa=nazwa, opis_cen=opis_cen, opis_popytu=opis_popytu, kategorie=kat, czynsz={'mnoznik': czynsz, 'uwaga': uwaga})
JEDZ, UBR, NARZ, ZIOL = 'Jedzenie, picie, nocleg', 'Ubranie i dodatki', 'Narzędzia i zestawy', 'Zioła, mikstury, narkotyki'
NOWE = [
    sytuacja('naplyw', 'Napływ ludzi (pielgrzymi, uchodźcy, święto)', 'jedzenie ×1,25 · ubranie i wyposażenie ×1,10 · reszta ×1,05',
             'jedzenie, ubranie, wyposażenie +1', {JEDZ: 1.25, UBR: 1.1, 'Wyposażenie różne': 1.1}, {JEDZ: 1, UBR: 1, 'Wyposażenie różne': 1},
             (1.05, 0), 1.4, 'każdy kąt wynajęty, gospody pełne'),
    sytuacja('braki', 'Braki w dostawach (zła droga, cło, zima)', 'jedzenie ×1,30 · narzędzia i zioła ×1,20 · reszta ×1,10',
             'jedzenie +1', {JEDZ: 1.3, NARZ: 1.2, ZIOL: 1.2}, {JEDZ: 1}, (1.1, 0), 1.0, 'czynsze się nie ruszają'),
    sytuacja('kryzys', 'Kryzys (podatki, bankructwa, zła moneta)', 'luksus i ubranie ×0,85 · jedzenie ×1,10 · reszta ×0,95',
             'popyt o stopień niżej, jedzenie bez zmian', {UBR: 0.85, 'Księgi i dokumenty': 0.85, JEDZ: 1.1}, {JEDZ: 0}, (0.95, -1), 0.9,
             'ludzie się wyprowadzają, właściciele obniżają komorne'),
    sytuacja('dobry_sezon', 'Dobry sezon (urodzaj, spokój na szlakach)', 'jedzenie ×0,80 · zwierzęta ×0,90 · reszta ×0,95',
             'ubranie, wyposażenie, księgi +1 — ludzie mają pieniądze', {JEDZ: 0.8, 'Zwierzęta i pojazdy': 0.9},
             {UBR: 1, 'Wyposażenie różne': 1, 'Księgi i dokumenty': 1}, (0.95, 0), 1.05, 'dobrze płacą, więc i czynsz idzie lekko w górę'),
]
KO['koniunktury'] = [k for k in KO['koniunktury'] if k['id'] not in {n['id'] for n in NOWE}] + NOWE
W('data/koniunktura.json', KO)

# ---------------------------------------------------------------- 4. rynek
RY = J('data/rynek.json')
JK = RY['jakosc']
JK['za_zalete'], JK['za_wade'] = 1.6, 0.6
JK['opis'] = ('HR-024 (v6b, MG): każda Zaleta przedmiotu ×1,6, każda Wada ×0,6 (PG: ×2 i ×½ — przy kilku Zaletach wymykało się spod kontroli). '
              'Cena w cenniku = wariant podstawowy bez Zalet i Wad przedmiotu.')
for o in JK['opcje']:
    o['mnoznik'] = {'2wady': 0.36, 'wada': 0.6, 'zwykla': 1, 'wysmienita': 1.6, 'mistrzowska': 2.56}[o['id']]
JK['bez_jakosci'] = ['zuzywalne', 'tkaniny']   # tagi branż: tych pozycji generator nie losuje z Zaletami ani Wadami
JK['niezwykle'] = {'opis': 'Niezwykle rzadko: Zaleta innej broni albo usunięta Wada broni. Każda liczy się jak Zaleta przedmiotu.',
                   'prefiks_zalety': 'Zaleta broni: ', 'prefiks_bez_wady': 'Bez Wady: '}
T = RY['targowanie']
T.update(za_ps=0.04, max=0.24, max_zamowienie=0.16,
         opis_v6b='Decyzja MG: −4% za każdy PS, najwyżej −24% (6 PS); zamówienia −16%. Talenty (np. Żyłka Handlowa) dodają upust ponad to.')
RY['dostepnosc'] = {
    'opis': 'PG s. 290: szansa, że przedmiot jest w sprzedaży, wg wielkości osady. Egzotyczne tylko na zamówienie (Zlecenie).',
    'tabela': {'wioska': {'Powszechna': 1, 'Ograniczona': 0.3, 'Rzadka': 0.15, 'Egzotyczna': 0},
               'miasteczko': {'Powszechna': 1, 'Ograniczona': 0.6, 'Rzadka': 0.3, 'Egzotyczna': 0},
               'miasto': {'Powszechna': 1, 'Ograniczona': 0.9, 'Rzadka': 0.45, 'Egzotyczna': 0}},
    'obce_pochodzenie': 0.3,
    'obce_opis': 'Towar krasnoludzki albo elfi u kupca innej rasy: szansa × 0,3.',
    'zamowienie': {'opis': 'Szacunek MG: rzecz, której tu zwykle nie ma (szansa z tabeli poniżej progu), kupiec sprowadza dłużej i drożej: termin + tyle tygodni, narzut × tyle.',
                   'prog': 0.5,
                   'termin_tyg': {'Ograniczona': 2, 'Rzadka': 4, 'Egzotyczna': 8}, 'narzut': {'Ograniczona': 1.1, 'Rzadka': 1.25, 'Egzotyczna': 1.5},
                   'wioska_bez': ['Egzotyczna'], 'wioska_opis': 'We wsi nikt nie sprowadzi rzeczy egzotycznej — trzeba jechać do miasta.'},
}
# v6c: towar trefny. Skala oszustwa i trudność Testu Wyceny wg Poradnika Staroświatowca (2 ed.), s. 41.
JAK_KATS = JK['kategorie']
RY['trefne'] = {
    'opis': 'v6c: szansa na pozycję z kupcy.json → trefne (domyślnie domyslna_szansa); cecha kupiecka może ją podnieść (Szarlatan, Powiązania przestępcze) albo wyzerować (Skrupulatnie uczciwy). '
            'wartosc = prawdziwa wartość ÷ cena, jaką kupiec podaje. swiadomosc = szansa, że kupiec wie (oszust wie zawsze). Widoczne tylko dla MG.',
    'domyslna_szansa': 0.04,
    'rodzaje': {
        'kradziony': {'nazwa': 'Kradziony', 'wartosc': 1, 'test_mod': None,
                      'opis': 'Towar z kradzieży albo niewiadomego pochodzenia. Wart tyle, ile kosztuje, ale prawowity właściciel albo straż może go rozpoznać.',
                      'test_opis': 'Wycena tego nie wykaże. Rozpoznanie: Intuicja, Wiedza (lokalna) albo świadek.'},
        'podrobka': {'nazwa': 'Podróbka', 'wartosc': 0.2, 'test_mod': -20, 'tagi': ['kosztownosci', 'luksus', 'dewocjonalia', 'pisarskie', 'naukowe'],
                     'kategorie': ['Księgi i dokumenty', 'Zioła, mikstury, narkotyki'],
                     'opis': 'Udaje coś cenniejszego: cyna zamiast srebra, farbowane sukno, fałszywa pieczęć, rozcieńczona mikstura.',
                     'test_opis': 'Trudny (−20) Test Wyceny.'},
        'ukryta_wada': {'nazwa': 'Ukryta Wada', 'wartosc': 0.6, 'test_mod': -10, 'kategorie': JAK_KATS,
                        'opis': 'Wygląda porządnie, ale ma Wadę przedmiotu (Tandetny albo Zawodny) — np. jeden z dziesięciu płaszczy.',
                        'test_opis': 'Wymagający (−10) Test Wyceny albo Rzemiosła.'},
        'miara': {'nazwa': 'Oszukana miara', 'wartosc': 'skala', 'tagi': ['tkaniny', 'pojemniki', 'zuzywalne', 'amunicja_prosta'],
                  'kategorie': ['Jedzenie, picie, nocleg', 'Amunicja'],
                  'opis': 'Niepełne skrzynie, zawyżona waga, zepsute sztuki na dnie, nadmiar opakowania.',
                  'test_opis': 'Test Wyceny wg skali oszustwa.'},
    },
    'wagi': {'kradziony': 1, 'podrobka': 1, 'ukryta_wada': 3, 'miara': 2},
    'skala_oszustwa': [{'udzial': 0.05, 'test': 'Prosty (+10)', 'mod': 10}, {'udzial': 0.1, 'test': 'Przeciętny (+0)', 'mod': 0},
                       {'udzial': 0.2, 'test': 'Wymagający (−10)', 'mod': -10}, {'udzial': 0.3, 'test': 'Trudny (−20)', 'mod': -20},
                       {'udzial': 0.4, 'test': 'Bardzo trudny (−30)', 'mod': -30}],
    'swiadomosc': {'kradziony': 0.9, 'podrobka': 0.6, 'ukryta_wada': 0.3, 'miara': 0.8},
}
W('data/rynek.json', RY)

# ---------------------------------------------------------------- 5. osady
OS = J('data/osady.json')
TYP = {'wies': 'wioska', 'miasteczko': 'miasteczko'}
for o in OS['osady']:
    o['dostepnosc'] = TYP.get(o['id'], 'miasto')
    o.pop('tylko_powszechna', None)
W('data/osady.json', OS)

# ---------------------------------------------------------------- 6. Złoto
ST = J('data/statusy.json')
OPIS = {5: 'Wielki magnat, Patriarcha bogatego Kolegium, gubernator prowincji, Najwyższy Lektor.',
        6: 'Książę prowincji, wielki ród arystokratyczny.',
        7: 'Arystokrata najwyższego rzędu: elektor, wielki książę. Dochód to przybliżenie po wydatkach stanu — utrzymanie dworu, '
           'świty i pozycji pochłania większość przychodu. Do tego poziomy Talentu Majętny (+1k5 ZK za poziom); figury państwowe ×10 (zasady).'}
for p in ST['poziomy']:
    if p['tier'] == 'Złoto' and p['lvl'] in OPIS: p['opis'] = OPIS[p['lvl']]
W('data/statusy.json', ST)
