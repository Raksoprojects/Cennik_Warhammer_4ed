# -*- coding: utf-8 -*-
"""Buduje dane v5: preset „zalecany” (v5) staje się obowiązującym cennikiem.

Co robi (idempotentnie, z danych v4):
  1. data/klasy_cenowe.json  ← propozycja/klasy_cenowe_v4.json + klasa „konie_bojowe” + preset zalecany v5
                                + preset zalecany_v4 (stary, do porównań) + uzasadnienia klas + „domyslny”
  2. data/cennik.json        ← cena_p = cena_ref_p × mnożnik klasy presetu domyślnego (jak zastosujPreset w JS)
  3. data/czynsze.json       ← propozycja/czynsze_v4.json (najem ×2 — bez zmian w v5)
  4. data/koniunktura.json   ← propozycja/koniunktura_v4.json (kryzys mieszkaniowy ×1,7)
  5. data/spojnosc_v4.json   ← + reguła rodziny „płytówka ÷ strój dworski ≥ 2”
Uruchom z katalogu repo: python3 narzedzia/buduj_v5.py && node --test test/*.test.mjs
"""
import json, math, os, copy
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
J = lambda f: json.load(open(R + f, encoding='utf-8'))
def W(f, d): json.dump(d, open(R + f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print('zapisano', f)

def ladna(p):  # identyczne z zastosujPreset w src/silnik.js (Math.round = połówka w górę)
    r = lambda x: math.floor(x + 0.5)
    if p < 24: return max(1, r(p))
    if p < 240: return int(r(p / 6) * 6)
    if p < 2400: return int(r(p / 12) * 12)
    return int(r(p / 60) * 60)

K = J('propozycja/klasy_cenowe_v4.json')
BOJOWE = ['rumak', 'lekki-kon-bojowy']
for i in BOJOWE: K['klasy'][i] = 'konie_bojowe'
# Skóra robi rymarz i kaletnik (Srebro 1–2), nie płatnerz — test płatnerza (×2) jej nie dotyczy.
SKORA = ['skorzana-kurta', 'skorzany-kaftan', 'skorzane-nogawice', 'skorzany-helm', 'kolet']
for i in SKORA: K['klasy'][i] = 'pancerz_skorzany'
K['klasy']['arkan'] = 'codzienne'          # arkan to lina z pętlą, nie wyrób zbrojmistrza
# v5.2: alchemia dzieli się na składniki (zioła, korzenie, grzyby — do kupienia dla alchemika i graczy)
# i wyroby (mikstury, eliksiry, trucizny, narkotyki przetworzone — wymagają aparatury, więc droższe).
SKLADNIKI = ['salwort', 'nocny-cien', 'ziemny-korzen', 'korzen-mandragory', 'ksiezycowy-kwiat', 'pluja',
             'fakstoryl', 'dziwnokorzen', 'grzybki-szalonego-kapelusznika', 'czarny-lotos']
WYROBY = ['mikstura-lecznicza', 'eliksir-zywotnosci', 'kataplazm-leczniczy', 'tonik-na-trawienie', 'rozkosz-ranalda', 'sercoboj']
for i in SKLADNIKI: K['klasy'][i] = 'alchemia_skladnik'
for i in WYROBY: K['klasy'][i] = 'alchemia_wyrob'
K['klasy']['nocleg-w-stajni-na-sianie'] = 'utrzymanie'
# Poprawki poziomu ×1 (cena_ref_p) — tylko spójność wewnętrzna, opisane w docs/archiwum/ANALIZA_v5.md rozdz. 3.
POPRAWKI_BAZY = {
 'flamberg': (4080, 'v5: baza = RAW bez źródła, a miecz dwuręczny ma bazę 0,57× RAW ze źródła. '
                    'Proporcja RAW flamberg ÷ miecz dwuręczny = 3 → 4080 p.'),
 'luk-elfi': (780, 'v5: decyzja MG — łuk elfi = 5× łuk długi (156 p × 5 = 780 p na poziomie ×1).'),
}

v4 = copy.deepcopy(K['presety']['zalecany'])
v4['opis'] = 'zalecany z v4 (przed analizą v5) — do porównań i do powrotu jednym kliknięciem'
v4['mnozniki']['konie_bojowe'] = v4['mnozniki']['konie']
v4['mnozniki']['pancerz_skorzany'] = v4['mnozniki']['pancerz']
for k in ('alchemia_skladnik', 'alchemia_wyrob'):
    v4['mnozniki'][k] = v4['mnozniki']['alchemia']
    for n in ('baza', 'drogi'): K['presety'][n]['mnozniki'][k] = K['presety'][n]['mnozniki']['alchemia']
for n in ('baza', 'drogi'):
    K['presety'][n]['mnozniki']['konie_bojowe'] = K['presety'][n]['mnozniki']['konie']
    K['presety'][n]['mnozniki']['pancerz_skorzany'] = K['presety'][n]['mnozniki']['pancerz']

v5 = copy.deepcopy(v4)
v5['opis'] = ('v5: zalecany po analizie wszystkich pozycji. Mnożnik zostaje tylko tam, gdzie wynika ze źródła, '
              'z testu rzemieślnika albo z zasady domowej MG. Zmiany wobec v4: codzienne 1,5→1,2; palna 1,5→1; '
              'alchemia 1,5→1; prestiż 3→1,5; konie robocze 1,5→1 (bojowe zostają 1,5); pancerz skórzany 2→1,5; '
              'pojazd 1→1,5 (decyzja MG: wozy trochę drogie, ale chłopa stać na furmankę). v5.2: broń palna ×2, '
              'alchemia rozdzielona: składniki ×1, wyroby (mikstury, eliksiry, trucizny) ×2.')
v5['mnozniki'].update({'codzienne': 1.2, 'palna': 1, 'alchemia': 1, 'prestiz': 1.5, 'konie': 1, 'konie_bojowe': 1.5,
                       'pancerz_skorzany': 1.5, 'pojazd': 1.5,
                       # v5.2 (decyzje MG): broń palna droga; alchemia droga, ale składniki osiągalne
                       'palna': 2, 'alchemia_skladnik': 1, 'alchemia_wyrob': 2})
K['presety'] = {'baza': K['presety']['baza'], 'zalecany': v5, 'zalecany_v4': v4, 'drogi': K['presety']['drogi']}
K['domyslny'] = 'zalecany'
K['opis'] = ('Klasy cenowe i presety. Cena w cenniku = cena_ref_p (poziom ×1) × mnożnik klasy (× premia znaku stanu '
             'dla mieczy). data/cennik.json ma już nałożony preset „domyslny”. Panel MG może nakładać inny preset albo '
             'własne mnożniki w locie: zastosujPreset() / zastosujUstawienia() w src/silnik.js.')
# Uzasadnienie każdej klasy — wyświetla je panel ustawień. „zrodlo” mówi, SKĄD jest mnożnik.
K['uzasadnienia'] = {
 'utrzymanie': {'zrodlo': 'dane', 'tekst': 'Jedzenie, nocleg, usługi: ceny ze źródeł (mediana 1,02× źródła). Budżet Brązu 3 nie pozwala na więcej.'},
 'surowiec': {'zrodlo': 'dane', 'tekst': 'Sukno i płótno z Krakowa 1526–35. Wyżej = arbitraż (koc tańszy niż jego sukno).'},
 'rzezne': {'zrodlo': 'dane', 'tekst': 'Drób, owce, świnie z Krakowa. Wyżej = mięso z tuszy tańsze od żywego zwierzęcia.'},
 'kruszec': {'zrodlo': 'dane', 'tekst': 'Biżuteria z kruszcu. Wyżej = opłaca się przetapiać monety.'},
 'najem_dolny': {'zrodlo': 'dane', 'tekst': 'Kąt i poddasze. Wyżej = Brązu 3 nie stać na dach nad głową.'},
 'najem': {'zrodlo': 'zasada domowa', 'tekst': '×2 wobec Frankfurtu 1450 — wynika z Twojej karczmy 3 s/noc i Marienburga 5 ZK. Idzie w parze z kupnem.'},
 'kupno': {'zrodlo': 'zasada domowa', 'tekst': 'Razem z najmem (zwrot z kupna 7–25 lat). Zmieniasz jedno — zmieniaj drugie.'},
 'robocze': {'zrodlo': 'dane', 'tekst': 'Wół, krowa: Kraków i Anglia trafiają co do grosza (1,04× źródła).'},
 'konie': {'zrodlo': 'dane', 'tekst': 'Konie robocze i wierzchowe: Kraków — pociągowy 14–16 ZK, siodłowy 34–46 ZK. ×1 trafia w środek.'},
 'konie_bojowe': {'zrodlo': 'zasada domowa', 'tekst': '„Królestwo za konia” — konie bojowe drogie. ×1,5: rumak 825 ZK = 2,3 roku brutto rycerza (źródła: 1–4 lata).'},
 'pojazd': {'zrodlo': 'zasada domowa', 'tekst': 'Decyzja MG: trochę drogo, ale chłop musi mieć wóz. ×1,5 — furmanka 6 ZK (8,7 tyg. Brązu 3), wóz 18 ZK. Źródła dają 2–3×.'},
 'codzienne': {'zrodlo': 'dane', 'tekst': 'Narzędzia, naczynia, koce. Źródła 1,15×, test kowala 1,15× → 1,2. Wcześniejsze 1,5 nie miało podstawy.'},
 'odziez': {'zrodlo': 'dane', 'tekst': 'Test szewca i krawca 1,4–1,8× → 1,5.'},
 'prestiz': {'zrodlo': 'zasada domowa', 'tekst': 'Zbytek. ×1,5, żeby strój dworski (45 ZK) nie był porównywalny z płytówką (96 ZK) — Twoja reguła.'},
 'bron': {'zrodlo': 'dane', 'tekst': 'Baza była poniżej źródeł (0,57×). ×2 daje 1,16× źródła i zbrojmistrz zarabia na swój Status.'},
 'palna': {'zrodlo': 'zasada domowa', 'tekst': 'Decyzja MG: broń palna ma być droga. ×2 ponad RAW i źródła (pistolet 20 ZK, rusznica 6 ZK). Proch też ×2.'},
 'alchemia_skladnik': {'zrodlo': 'dane', 'tekst': 'Zioła, korzenie, grzyby: ceny RAW. Alchemik i gracze mają je kupić bez łamania sakiewki.'},
 'alchemia_wyrob': {'zrodlo': 'zasada domowa', 'tekst': 'Mikstury, eliksiry, trucizny: ×2, bo wymagają aparatury. Mikstura lecznicza 1 ZK 10 s = tydzień brutto Srebra 1.'},
 'pancerz_skorzany': {'zrodlo': 'dane', 'tekst': 'Skórznie robi rymarz (Srebro 1–2), nie płatnerz. Jak odzież: ×1,5. Kurta 1 ZK 13 s, źródło 14–27 s.'},
 'pancerz': {'zrodlo': 'dane + zasada', 'tekst': '×2: kolczuga 20 ZK (nowe wydanie, Twoja kotwica), test płatnerza 2,0. Źródła angielskie dają ok. połowę.'},
 'ksiega': {'zrodlo': 'dane', 'tekst': 'Rękopis medyczny £5–20 = 35–140 ZK; test skryby 1,4. ×2 = środek.'},
 'alchemia': {'zrodlo': 'brak danych', 'tekst': 'Brak źródeł. Baza i tak 1,5× RAW. Chcesz, żeby leczenie bolało — podnieś suwak.'},
}
W('data/klasy_cenowe.json', K)

# ---------------------------------------------------------------- cennik
C = J('data/cennik.json')
# v5.2: noclegi wg MG — wspólna izba to ława albo podłoga; dochodzi nocleg w stajni na sianie;
# „stajnia na 1 noc” to miejsce dla konia z obrokiem.
NOWE_V52 = [dict(id='nocleg-w-stajni-na-sianie', kat='Jedzenie, picie, nocleg', nazwa='Nocleg w stajni (na sianie)',
                 zrodlo=None, cena_raw_p=None, cena_p=4, cena_ref_p=4, obc=None, dostepnosc='Powszechna',
                 podstawa_hist='', komentarz='Najtańsze spanie pod dachem: na sianie przy koniach. Często gratis do posiłku albo za pomoc w stajni.',
                 dopisane='2026-10-24', uwagi_danych='v5.2: dopisane na prośbę MG. SZACUNEK: ok. 0,4× wspólnej izby.',
                 pozycja_kampanii=True, typ='nocleg', podtyp=None, klasa='utrzymanie')]
for n in NOWE_V52:
    if not any(c['id'] == n['id'] for c in C['pozycje']):
        i = next(k for k, c in enumerate(C['pozycje']) if c['id'] == 'wspolna-izba-na-1-noc')
        C['pozycje'].insert(i, n)
for c in C['pozycje']:
    if c['id'] == 'wspolna-izba-na-1-noc':
        c['nazwa'] = 'Wspólna izba na 1 noc (ława albo podłoga)'
        c['podstawa_hist'] = ''
        c['komentarz'] = 'Spanie na ławie albo na podłodze we wspólnej izbie, nie łóżko. Cena RAW. Łóżko to prywatny pokój.'
        c['uwagi_danych'] = 'v5.2: poprawiony opis (MG). Dawne źródło „łóżko w gospodzie 1331 = 2 d” dotyczyło łóżka, nie ławy — usunięte.'
    if c['id'] == 'stajnia-na-1-noc':
        c['nazwa'] = 'Stajnia dla konia na 1 noc (z obrokiem)'
pr = K['presety'][K['domyslny']]; znak = set(K['znak_stanu'])
poz = []
for c in C['pozycje']:
    c = dict(c); base = c.get('cena_ref_p') or c['cena_p']
    if c['id'] in POPRAWKI_BAZY:
        base, powod = POPRAWKI_BAZY[c['id']]
        if powod not in (c.get('uwagi_danych') or ''): c['uwagi_danych'] = ((c.get('uwagi_danych') or '') + ' ' + powod).strip()
    c['klasa'] = K['klasy'].get(c['id'], c.get('klasa'))
    m = pr['mnozniki'].get(c['klasa'], 1) * (pr.get('premia_znak_stanu', 1) if c['id'] in znak else 1)
    c['cena_ref_p'] = base; c['cena_p'] = ladna(base * m); poz.append(c)
P = {c['id']: c for c in poz}
kpoj = pr['mnozniki'].get('codzienne', 1)
P['butelka-wina']['cena_p'] = P['butelka']['cena_p'] + 24
P['beczulka-piwa-10-l']['cena_p'] = ladna(18 + 13 * kpoj)
P['sledzie-beczka']['cena_p'] = ladna(P['sledzie-beczka']['cena_ref_p'] - P['beczka-145-l']['cena_ref_p'] + P['beczka-145-l']['cena_p'])
C['pozycje'] = poz
C['wersja'] = 'v5-zalecany'
C['opis'] = ('Cennik v5 — obowiązujący. cena_p = cena wytwórcy w presecie „zalecany” v5 (to jest „cena bazowa” '
             'wyświetlana w Skarbcu). cena_ref_p = poziom ×1 przed mnożnikiem klasy (limity i ilości w generatorze, '
             'przeliczanie presetów). klasa = klasa cenowa z data/klasy_cenowe.json.')
W('data/cennik.json', C)

W('data/czynsze.json', J('propozycja/czynsze_v4.json'))
W('data/koniunktura.json', J('propozycja/koniunktura_v4.json'))

S = J('data/spojnosc_v4.json')
if not any(r['a'] == 'pelna-plytowka-4-elementy' and r['b'] == 'stroj-dworski' for r in S['rodziny']):
    S['rodziny'].append({'a': 'pelna-plytowka-4-elementy', 'b': 'stroj-dworski', 'min': 2.0, 'max': 10.0,
                         'opis': 'płytówka ÷ strój dworski (zasada MG: strój nie może być porównywalny z płytówką)'})
    S['rodziny'].append({'a': 'flamberg', 'b': 'miecz-dwureczny', 'min': 1.5, 'max': 3.5,
                         'opis': 'flamberg ÷ miecz dwuręczny (RAW 3)'})
    S['rodziny'].append({'a': 'rumak', 'b': 'kon-wierzchowy', 'min': 8.0, 'max': 40.0,
                         'opis': 'rumak ÷ koń wierzchowy (destrier = wielokrotność konia siodłowego)'})
W('data/spojnosc_v4.json', S)

# ---------------------------------------------------------------- rynek: osobowość kupca i cena minimalna (v5)
RY = J('data/rynek.json')
RY.setdefault('preferencje', {'opis': 'v5: mnożnik kupca za kategorię. Rdzeń taniej (specjalista, kupuje hurtem), boczny asortyment drożej. '
    'Kupiec może nadpisać per kategoria w kupcy.json → preferencje.', 'rdzen': 0.95, 'boczne': 1.1})
RY.setdefault('kaprys', {'opis': 'v5: 1k10 na pozycję (osobny strumień losowania, nie zmienia rzutów zapasu i popytu). '
    'Preferencja × kaprys mieści się w granicach.', 'rzut': '1k10',
    'progi': [{'do': 1, 'mnoznik': 0.9, 'opis': 'chce się tego pozbyć'}, {'do': 3, 'mnoznik': 0.95, 'opis': 'zalega'},
              {'do': 7, 'mnoznik': 1, 'opis': 'zwykła cena'}, {'do': 9, 'mnoznik': 1.05, 'opis': 'lubi tę rzecz'},
              {'do': 10, 'mnoznik': 1.1, 'opis': '„to najlepsza sztuka w mieście”'}], 'granice': [0.85, 1.2]})
RY.setdefault('cena_minimalna', {'opis': 'v5: koszt nabycia = cennik × osada × koniunktura (wytwórca: × koszt_wlasny). '
    'Cena minimalna = koszt × narzut_min; przy wyprzedaży (rynek < 1) koszt × wyprzedaz. Dolna granica targowania.',
    'narzut_min': 1.05, 'wyprzedaz': 0.9, 'koszt_wlasny': 0.8})
RY['targowanie']['dolna_granica'] = ('v5: cena minimalna kupca (cena_min_p z generatora). Bez niej — jak dawniej: '
    'nie poniżej ceny z cennika × jakość.')
W('data/rynek.json', RY)

# v5.1: decyzje MG z 2026-10-24
S = J('data/spojnosc_v4.json')
if not any(r['a'] == 'luk-elfi' for r in S['rodziny']):
    S['rodziny'].append({'a': 'luk-elfi', 'b': 'luk-dlugi', 'min': 4.5, 'max': 5.5, 'opis': 'łuk elfi ÷ łuk długi (decyzja MG: ×5)'})
for w in S['rzemieslnik']['wzorce']:
    if w['id'] == 'woz' and w['dni'] == 8:
        w['dni'] = 12; w['uwaga'] = ('v5.1: 8 → 12 dni. Wóz czterokołowy z żelaznymi obręczami to robota kołodzieja i kowala; '
                                     'źródło (15 guldenów = 34 ZK) pokazywało, że 8 dni było za mało.')
W('data/spojnosc_v4.json', S)

# v5.2: kolejność noclegów
SP = J('data/spojnosc.json')
if not any(r.get('ids') == ['nocleg-w-stajni-na-sianie', 'wspolna-izba-na-1-noc', 'prywatny-pokoj-na-1-noc'] for r in SP['reguly']):
    SP['reguly'].append({'opis': 'Noclegi: stajnia na sianie < wspólna izba (ława, podłoga) < prywatny pokój', 'typ': 'rosnaco',
                         'ids': ['nocleg-w-stajni-na-sianie', 'wspolna-izba-na-1-noc', 'prywatny-pokoj-na-1-noc']})
    W('data/spojnosc.json', SP)

# ---------------------------------------------------------------- v5.2: korekty Dochodu (Pozycja bez zmian)
# Zasada domowa: Status (Pozycja) ≠ zarobek. Porównanie z płacami historycznymi w wielokrotnościach robotnika
# (Brąz 3 = 165 p brutto tygodniowo): lancknecht 4 fl./mies. ≈ 3×, Doppelsöldner ≈ 6×, rajtar z koniem ≈ 9×,
# strażnik miejski ≈ 1,5–2×, tragarz w porcie ≈ 1–1,3×, służba z wiktem: gotówki 0,3–0,7× robotnika.
# Drabina Dochodu: Brąz N = N/3×, Srebro 1 = 2×, S2 = 4×, S3 = 6×, S4 = 8×, S5 = 10×, Złoto 1 ≈ 22×.
KOREKTY_DOCHODU = {
 ('Służąca', 'Służąca'): ('Brąz 2 + wikt', 'Służba z wiktem dostaje 4–6 zł rocznie gotówką (Kraków XVI w.) — ok. 0,4× robotnika.'),
 ('Służąca', 'Pokojowa'): ('Brąz 3 + wikt', 'Pokojowa pani domu: gotówka jak robotnik, reszta w wikcie, stroju i podarkach.'),
 ('Służąca', 'Ochmistrzyni'): ('Srebro 1 + wikt', 'Ochmistrzyni bogatego domu: 2× robotnik gotówką plus pełne utrzymanie.'),
 ('Żołnierz', 'Żołnierz'): ('Srebro 2', 'Lancknecht: 4 guldeny miesięcznie ≈ 3× robotnik. Srebro 3 (6×) to żołd Doppelsöldnera.'),
 ('Żołnierz', 'Sierżant'): ('Srebro 3', 'Podoficer: podwójny żołd (Doppelsold) ≈ 6× robotnik.'),
 ('Strażnik', 'Sierżant Straży'): ('Srebro 2', 'Straż miejska płaciła mniej niż wojsko: sierżant ≈ 4× robotnik.'),
 ('Strażnik', 'Kapitan Straży'): ('Srebro 4', 'Kapitan straży miejskiej to urzędnik rady, nie oficer polowy: ≈ 8× robotnik.'),
 ('Strażnik Dróg', 'Sierżant Strażników Dróg'): ('Srebro 3', 'Jak sierżant wojska (Doppelsold).'),
 ('Strażnik Dróg', 'Kapitan Strażników Dróg'): ('Srebro 5', 'Dowódca kilku posterunków: ≈ 10× robotnik, nie 22×.'),
 ('Kawalerzysta', 'Sierżant Kawalerii'): ('Srebro 5', 'Rajtar z koniem ≈ 9× robotnik; sierżant nieco więcej. Złoto 1 (22×) to płaca rotmistrza.'),
 ('Kawalerzysta', 'Oficer Kawalerii'): ('Złoto 1', 'Rotmistrz: ≈ 20× robotnik.'),
 ('Doker', 'Doker'): ('Brąz 5', 'Tragarz portowy zarabiał jak czeladnik, nie jak mistrz.'),
 ('Doker', 'Brygadzista'): ('Srebro 2', 'Brygadzista tragarzy: ≈ 4× robotnik.'),
 ('Doker', 'Mistrz Dokerów'): ('Srebro 3', 'Starszy cechu tragarzy: ≈ 6× robotnik.'),
 ('Strażnik', 'Strażnik Rzeczny'): ('Srebro 1', 'Straż rzeczna płaciła jak straż miejska.'),
 ('Strażnik', 'Żołnierz Okrętowy'): ('Srebro 2', 'Jak lancknecht.'),
 ('Strażnik', 'Mistrz Żołnierzy Okrętowych'): ('Srebro 4', 'Jak kapitan straży.'),
}
AU = J('data/audyt.json'); trafione = set()
for prof in AU:
    for l in prof['poziomy']:
        k = (prof['profesja'], l['nazwa'])
        if k in KOREKTY_DOCHODU:
            doch, powod = KOREKTY_DOCHODU[k]; trafione.add(k)
            l['doch'] = doch
            if l['w'] == 'ok': l['w'] = 'dochod'
            if 'v5.2' not in (l.get('powod') or ''):
                l['powod'] = ((l.get('powod') or '') + ' v5.2: Dochód ' + doch + '. ' + powod).strip()
brak = set(KOREKTY_DOCHODU) - trafione
assert not brak, f'Nie znaleziono poziomów: {brak}'
W('data/audyt.json', AU)
