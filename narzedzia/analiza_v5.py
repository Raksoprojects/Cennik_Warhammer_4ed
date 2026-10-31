# -*- coding: utf-8 -*-
"""Analiza v5: przegląd wszystkich pozycji cennika zalecanego + zarobki profesji kontra ceny.

Uruchom z katalogu repo:  python3 narzedzia/analiza_v5.py
Wyniki:  docs/analiza_v5/cennik_przeglad.csv
         docs/analiza_v5/klasy.csv
         docs/analiza_v5/profesje.csv
         docs/analiza_v5/wyniki.json   (liczby cytowane w docs/archiwum/ANALIZA_v5.md)
Nie zmienia danych. Tylko czyta data/cennik.json, data/klasy_cenowe.json, data/audyt.json, data/statusy.json.
"""
import json, re, csv, os, statistics as st, sys

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
J = lambda f: json.load(open(R + f, encoding='utf-8'))
OUT = R + 'docs/analiza_v5/'
os.makedirs(OUT, exist_ok=True)

CEN = J(sys.argv[1] if len(sys.argv) > 1 else 'data/cennik.json')['pozycje']
KLASY = J('data/klasy_cenowe.json')
AUD = J('data/audyt.json')
STAT = J('data/statusy.json')
PRESET = KLASY['domyslny']
MN = KLASY['presety'][PRESET]['mnozniki']

def mon(p):
    p = round(p)
    if p == 0: return '—'
    z, r = divmod(p, 240); s, pe = divmod(r, 12); o = []
    if z: o.append(f"{z} ZK")
    if s: o.append(f"{s} s")
    if pe or not o: o.append(f"{pe} p")
    return ' '.join(o)

# ---------------------------------------------------------------- 1. źródło historyczne → pensy
# Przeliczniki zgodne z docs/archiwum/ANALIZA_ZRODEL.md (kotwica: Brąz 3 = 165 p/tydz.).
# Gdy opis ma już przeliczenie („= 2 ZK 1 s”), bierzemy przeliczenie autora. W przeciwnym razie
# przeliczamy walutę: grosz krakowski 18 p, floren/gulden 550 p, funt ang. 1651 p, szyling ang. 82,6 p, pens ang. 6,9 p.
WAL = [(r'gr\b', 18), (r'(?:floren|gulden)\w*', 550), (r'£', 1651), (r's ang\.?', 82.6), (r'd ang\.?', 6.88), (r'\bd\b', 6.88), (r'\bs\b', 82.6)]
num = lambda s: float(s.replace(',', '.'))

def kwota_po_rownasie(t):
    """'2 ZK 1 s' / '14–16 ZK' / '17 s 2 p' → (lo, hi) w pensach."""
    t = t.strip()
    m = re.match(r'^(\d+(?:,\d+)?)\s*[–-]\s*(\d+(?:,\d+)?)\s*(ZK|s|p)\b', t)
    if m:
        k = {'ZK': 240, 's': 12, 'p': 1}[m.group(3)]
        return num(m.group(1)) * k, num(m.group(2)) * k
    tot, ok = 0, False
    for v, u in re.findall(r'(\d+(?:,\d+)?)\s*(ZK|s|p)\b', t[:30]):
        tot += num(v) * {'ZK': 240, 's': 12, 'p': 1}[u]; ok = True
    return (tot, tot) if ok else None

def kwota_waluta(t):
    # „£8 6 s 8 d”, „5 d”, „15–16 gr”, „6–7 florenów”, „2 s 6 d”
    m = re.search(r'£\s*(\d+(?:,\d+)?)(?:\s*[–-]\s*(\d+(?:,\d+)?))?', t)
    if m:
        lo = num(m.group(1)) * 1651; hi = num(m.group(2)) * 1651 if m.group(2) else lo
        return lo, hi
    for wz, k in WAL:
        m = re.search(r'(\d+(?:,\d+)?)(?:\s*[–-]\s*(\d+(?:,\d+)?))?\s*' + wz, t)
        if m:
            lo = num(m.group(1)) * k; hi = num(m.group(2)) * k if m.group(2) else lo
            # „2 s 6 d”: dodaj pensy
            m2 = re.search(r'(\d+)\s*s\s+(\d+)\s*d', t)
            if m2 and wz.startswith('s'): lo = hi = int(m2.group(1)) * 82.6 + int(m2.group(2)) * 6.88
            return lo, hi
    return None

def hist(h):
    if not h or h in ('—', 'j.w.') or h.startswith('j.w.'): return None
    if 'RAW' in h or 'cena luksusowa' in h or 'setki funtów' in h: return None
    if '=' in h:
        k = kwota_po_rownasie(h.split('=')[1])
        if k: return k
    if ':' in h or '–' in h or '-' in h:
        tail = re.split(r'[:–]', h, maxsplit=1)[-1]
        k = kwota_waluta(tail) or kwota_waluta(h)
        if k: return k
    return None

# Pozycje, w których opis źródła mówi o innej jednostce niż pozycja cennika — nie porównujemy.
INNA_JEDNOSTKA = {'bomba', 'srut-i-proch-12', 'pocisk-olowiany-12', 'pistolet', 'beczulka-piwa-10-l', 'butelka-wina',
                  'pol-litra-piwa', 'kat-w-izbie-czeladnej-tydzien', 'mieszkanie-mieszczanskie-23-izby-miesiac',
                  'robotnik-niewykwalifikowany', 'czeladnik', 'mistrz-rzemiosla', 'doswiadczony-najemnik',
                  'prawnik', 'czarny-lotos', 'stroj-ceremonialny-aksamit-zlotoglow-futra', 'ubranie', 'uprzaz-z-siodlem',
                  'arkusz-pergaminu', 'ksiega-religia', 'prowiant-na-1-dzien', 'wykup-licencji-cechowej',
                  'wpis-ucznia-do-cechu', 'chleb-zytni-bochenek', 'mieso-kg', 'jedwabna-bielizna', 'stroj-dworski',
                  'warsztat', 'polzbroja-municyjna-napiersnik-morion', 'ciezki-pancerz-opcja', 'kaftan-kolczy',
                  'kolczuga', 'napiersnik', 'krowa', 'butelka'}
# Źródło podaje inną liczbę sztuk: snop 24 strzał, a pozycja to 12.
SKALA = {'strzala-12': 0.5}
# Uwaga: wyjęte też te, gdzie opis łączy dwie epoki (kolczuga XII/XVI w.), dwa przedmioty (ubranie + koszula)
# albo daje cenę surowca, nie wyrobu (jedwab za jard, proch za funt). Te sprawdzamy ręcznie w docs/archiwum/ANALIZA_v5.md.

# ---------------------------------------------------------------- 2. flagi pozycji
ZNAK = set(KLASY['znak_stanu'])
WIERSZE = []
for p in CEN:
    ref = p.get('cena_ref_p') or p['cena_p']; cena = p['cena_p']; raw = p.get('cena_raw_p')
    kl = p.get('klasa', '?'); m = MN.get(kl, 1) * (KLASY['presety'][PRESET].get('premia_znak_stanu', 1) if p['id'] in ZNAK else 1)
    h = None if p['id'] in INNA_JEDNOSTKA else hist(p.get('podstawa_hist'))
    if h and p['id'] in SKALA: h = (h[0] * SKALA[p['id']], h[1] * SKALA[p['id']])
    hs = (p.get('podstawa_hist') or '').strip()
    zr = hs not in ('', '—')                       # „j.w.” = źródło pozycji powyżej, przeniesione proporcjonalnie
    flagi = []
    if not zr: flagi.append('bez źródła')
    elif hs.startswith('j.w.'): flagi.append('źródło j.w.')
    if raw and ref != raw and not zr: flagi.append('baza≠RAW bez źródła')
    if raw and (cena / raw > 4 or cena / raw < 0.34): flagi.append(f'skrajne wobec RAW ×{cena/raw:.2f}')
    q_h = None
    if h:
        lo, hi = h; mid = (lo + hi) / 2
        q_h = cena / mid
        if cena > hi * 1.25: flagi.append(f'ponad źródło ×{cena/hi:.1f}')
        elif cena < lo * 0.8: flagi.append(f'poniżej źródła ×{cena/lo:.2f}')
    WIERSZE.append(dict(id=p['id'], nazwa=p['nazwa'], kat=p['kat'], klasa=kl, typ=p.get('typ'),
        raw_p=raw, baza_p=ref, mnoznik=round(m, 3), cennik_p=cena, cennik=mon(cena),
        x_raw=round(cena / raw, 2) if raw else None,
        hist_lo_p=round(h[0]) if h else None, hist_hi_p=round(h[1]) if h else None,
        x_hist=round(q_h, 2) if q_h else None,
        tyg_brazu3=round(cena / STAT['robotnik_brutto_p'], 2),
        zrodlo=(p.get('podstawa_hist') or ''), flagi='; '.join(flagi)))

with open(OUT + 'cennik_przeglad.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(WIERSZE[0].keys()), delimiter=';'); w.writeheader(); w.writerows(WIERSZE)

# ---------------------------------------------------------------- 3. klasy: czy mnożnik wynika z danych
KL = {}
for r in WIERSZE:
    k = KL.setdefault(r['klasa'], dict(klasa=r['klasa'], n=0, ze_zrodlem=0, q_hist=[], q_baza_hist=[], bez_zrodla=0))
    k['n'] += 1
    if r['x_hist']:
        k['ze_zrodlem'] += 1; k['q_hist'].append(r['x_hist']); k['q_baza_hist'].append(r['baza_p'] / ((r['hist_lo_p'] + r['hist_hi_p']) / 2))
    if 'bez źródła' in r['flagi']: k['bez_zrodla'] += 1
# Test rzemieślnika (data/spojnosc_v4.json): mnożnik, przy którym cena = 1,4 × koszt warsztatu
T = J('data/spojnosc_v4.json')['rzemieslnik']
C = {r['id']: r['cennik_p'] for r in WIERSZE}; B = {r['id']: r['baza_p'] for r in WIERSZE}; KLI = {r['id']: r['klasa'] for r in WIERSZE}
REC = J('data/spojnosc_v4.json')['receptury']['pozycje']
def material(i, ceny):
    return sum(n if k.startswith('_') else ceny[k] * n for k, n in REC[i].items())
RZ = []
for wz in T['wzorce']:
    i = wz['id']
    if i not in C: continue
    mat_b = wz.get('material_p') if wz.get('material_p') is not None else (material(i, B) if i in REC else 0)
    mat_c = wz.get('material_p') if wz.get('material_p') is not None else (material(i, C) if i in REC else 0)
    koszt_b = wz['dni'] * T['warsztaty_p_dzien'][wz['warsztat']] + mat_b
    koszt_c = wz['dni'] * T['warsztaty_p_dzien'][wz['warsztat']] + mat_c
    RZ.append(dict(id=i, klasa=KLI[i], warsztat=wz['warsztat'], dni=wz['dni'], q_baza=round(B[i] / koszt_b, 2),
                   q_cennik=round(C[i] / koszt_c, 2), m_dla_1_4=round(1.4 * koszt_b / B[i], 2)))
UZAS = {}
for r in RZ: UZAS.setdefault(r['klasa'], []).append(r['m_dla_1_4'])

KLASY_OUT = []
for k, v in sorted(KL.items()):
    KLASY_OUT.append(dict(klasa=k, pozycji=v['n'], ze_zrodlem_liczbowym=v['ze_zrodlem'], bez_zrodla=v['bez_zrodla'],
        mnoznik=MN.get(k, 1),
        mediana_cennik_do_zrodla=round(st.median(v['q_hist']), 2) if v['q_hist'] else None,
        mediana_baza_do_zrodla=round(st.median(v['q_baza_hist']), 2) if v['q_baza_hist'] else None,
        mnoznik_z_testu_rzemieslnika=round(st.median(UZAS[k]), 2) if k in UZAS else None))
with open(OUT + 'klasy.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(KLASY_OUT[0].keys()), delimiter=';'); w.writeheader(); w.writerows(KLASY_OUT)

# ---------------------------------------------------------------- 4. profesje: dochód kontra zakupy
def status_dochodu(l):
    for pole in ('doch', 'poz', 'raw'):
        m = re.match(r'(Brąz|Srebro|Złoto)\s+(\d+)', l.get(pole) or '')
        if m: return m.group(1), int(m.group(2)), pole
    return None
def srednie(tier, lvl):
    W = STAT['wzory'][tier]; ile = 2 * lvl if W['kosci'] == '2N' else lvl
    netto = ile * (W['k'] + 1) / 2 * W['moneta_p']
    return netto, netto * 5

# Zakupy „narzędzia zawodu” — wybór autora analizy, nie lista z podręcznika (patrz docs/archiwum/ANALIZA_v5.md, rozdz. 5).
ZAKUPY = {
 'Żołnierz': ['polzbroja-municyjna-napiersnik-morion', 'halabarda', 'kolczuga'],
 'Rycerz': ['rumak', 'pelna-plytowka-4-elementy', 'kopia', 'miecz'],
 'Kawalerzysta': ['lekki-kon-bojowy', 'kon-wierzchowy', 'kolczuga', 'pistolet'],
 'Strażnik': ['halabarda', 'skorzana-kurta', 'helm-otwarty-morion'],
 'Ochroniarz': ['miecz', 'skorzana-kurta', 'tarcza'],
 'Oprych': ['topor', 'skorzana-kurta'],
 'Zwadźca': ['rapier', 'lewak', 'ubranie'],
 'Gladiator': ['tarcza', 'miecz', 'helm-zamkniety'],
 'Kapłan Bitewny': ['mlot-bojowy', 'kolczuga'],
 'Łowca Czarownic': ['pistolet', 'rapier', 'skorzana-kurta', 'kon-wierzchowy'],
 'Strażnik Dróg': ['kon-wierzchowy', 'pistolet', 'kusza'],
 'Posłaniec': ['kon-wierzchowy', 'uprzaz-z-siodlem'],
 'Woźnica': ['woz', 'kon-pociagowy', 'kon-pociagowy'],
 'Przewoźnik': ['barka-rzeczna'],
 'Flisak': ['lodz-wioslowa'],
 'Rzemieślnik': ['narzedzia-pracy', 'warsztat'],
 'Chłop': ['wol', 'krowa', 'sierp'],
 'Łowczy': ['luk-dlugi', 'sidla-na-zwierzeta', 'pies-mysliwski'],
 'Zwiadowca': ['kon-wierzchowy', 'luk', 'namiot'],
 'Aptekarz': ['mozdzierz-z-tluczkiem', 'ksiega-aptekarstwo'],
 'Medyk': ['ksiega-medycyna', 'zestaw-na-zatrucia'],
 'Czarodziej': ['ksiega-magia'],
 'Prawnik': ['ksiega-prawo', 'zestaw-do-pisania'],
 'Uczony': ['ksiega-sztuka', 'zestaw-do-pisania'],
 'Inżynier': ['ksiega-inzynieria', 'teodolit'],
 'Kupiec': ['woz', 'kon-pociagowy'],
 'Domokrążca': ['furmanka', 'mul'],
 'Szlachcic': ['stroj-dworski', 'kon-wierzchowy', 'miecz'],
 'Doradca': ['stroj-dworski'],
 'Mieszczanin': ['ubranie', 'izba-w-kamienicy-miesiac'],
 'Kuglarz': ['instrument', 'kostium'],
 'Złodziej': ['wytrychy', 'sztylet'],
 'Pilot Rzeczny': ['lodz-wioslowa'],
}
PROF = []
for c in AUD:
    if c['profesja'] not in ZAKUPY: continue
    for nr, l in enumerate(c['poziomy'], 1):
        s = status_dochodu(l)
        if not s: continue
        tier, lvl, pole = s
        netto, brutto = srednie(tier, lvl)
        if netto == 0: continue
        for i in ZAKUPY[c['profesja']]:
            if i not in C: continue
            PROF.append(dict(profesja=c['profesja'], poziom=nr, nazwa=l['nazwa'], dochod=f"{tier} {lvl}",
                skad=pole, netto_tydz_p=netto, brutto_tydz_p=brutto, zakup=i, cena_p=C[i], cena=mon(C[i]),
                rob_netto=round(C[i] / netto, 1), tyg_brutto=round(C[i] / brutto, 1),
                proc_rocznego_brutto=round(100 * C[i] / (brutto * 50), 1)))
with open(OUT + 'profesje.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(PROF[0].keys()), delimiter=';'); w.writeheader(); w.writerows(PROF)

# ---------------------------------------------------------------- 5. podsumowanie
liczba = lambda f: sum(1 for r in WIERSZE if f(r))
WYN = dict(
    preset=PRESET, pozycji=len(WIERSZE),
    ze_zrodlem=liczba(lambda r: 'bez źródła' not in r['flagi']),
    bez_zrodla=liczba(lambda r: 'bez źródła' in r['flagi']),
    porownywalne_ze_zrodlem=liczba(lambda r: r['x_hist']),
    w_przedziale_zrodla=liczba(lambda r: r['x_hist'] and 'ponad źródło' not in r['flagi'] and 'poniżej źródła' not in r['flagi']),
    ponad_zrodlo=[(r['id'], r['cennik'], r['flagi']) for r in WIERSZE if 'ponad źródło' in r['flagi']],
    ponizej_zrodla=[(r['id'], r['cennik'], r['flagi']) for r in WIERSZE if 'poniżej źródła' in r['flagi']],
    baza_ne_raw_bez_zrodla=liczba(lambda r: 'baza≠RAW bez źródła' in r['flagi']),
    skrajne_raw=[(r['id'], r['x_raw']) for r in WIERSZE if 'skrajne' in r['flagi']],
    klasy=KLASY_OUT, rzemieslnik=RZ)
json.dump(WYN, open(OUT + 'wyniki.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

if __name__ == '__main__':
    print(f"preset {PRESET}: {WYN['pozycji']} pozycji, ze źródłem {WYN['ze_zrodlem']}, bez {WYN['bez_zrodla']}")
    print(f"porównywalne liczbowo ze źródłem: {WYN['porownywalne_ze_zrodlem']}, w przedziale: {WYN['w_przedziale_zrodla']}")
    print('PONAD ŹRÓDŁO:'); [print('  ', *x) for x in WYN['ponad_zrodlo']]
    print('PONIŻEJ ŹRÓDŁA:'); [print('  ', *x) for x in WYN['ponizej_zrodla']]
    print('KLASY:')
    for k in KLASY_OUT: print('  ', k)
    print('RZEMIEŚLNIK:'); [print('  ', r) for r in RZ]
