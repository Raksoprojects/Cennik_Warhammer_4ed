# -*- coding: utf-8 -*-
"""Model v4: poprawki bazy (×1), klasy cenowe, presety mnożników, testy spójności."""
import json, math, copy, statistics as st
R='/home/claude/praca/repo/'
O='/home/claude/praca/v4/'
J=lambda f: json.load(open(R+f,encoding='utf-8'))
cen=J('data/cennik.json'); REG=J('data/spojnosc.json')['reguly']; STAT=J('data/statusy.json')
for r in REG:
    if r.get('ids')==['koc','zwijane-poslanie','plocienna-plandeka','namiot']:
        r['ids']=['koc','plocienna-plandeka','namiot']; r['opis']='Obozowanie: koc < plandeka < namiot'
REG.append({'opis':'Posłanie = koc + siennik, więc droższe od koca','typ':'rosnaco','ids':['koc','zwijane-poslanie']})

def mon(p):
    p=round(p)
    if p==0: return '—'
    z,r=divmod(p,240); s,pe=divmod(r,12); o=[]
    if z:o.append(f"{z} ZK")
    if s:o.append(f"{s} s")
    if pe or not o:o.append(f"{pe} p")
    return ' '.join(o)
def ladna(p):
    """Zaokrągla do 'ładnej' monety: <2 s do pensa, <1 ZK do 6 p, <10 ZK do szylinga, wyżej do 5 s."""
    r=lambda x: math.floor(x+0.5)          # połówka w górę — tak jak Math.round w JS
    if p<24: return max(1,r(p))
    if p<240: return int(r(p/6)*6)
    if p<2400: return int(r(p/12)*12)
    return int(r(p/60)*60)

B={p['id']:p for p in copy.deepcopy(cen['pozycje'])}

# ===================================================================
# 1. POPRAWKI BAZY (poziom ×1) — wewnętrzne niespójności v3
# ===================================================================
POPR=[]
def nowa(id_,kat,nazwa,cena,podst,kom,typ='towar',pod=None):
    B[id_]=dict(id=id_,kat=kat,nazwa=nazwa,zrodlo=None,cena_raw_p=None,cena_p=cena,obc=None,
                dostepnosc='Powszechna',podstawa_hist=podst,komentarz=kom,dopisane='2026-11',
                uwagi_danych=None,pozycja_kampanii=True,typ=typ,podtyp=pod)
    POPR.append((id_,None,cena,'dopisane: '+kom))
def ustaw(id_,cena,powod):
    POPR.append((id_,B[id_]['cena_p'],cena,powod)); B[id_]['cena_p']=cena
    B[id_]['uwagi_danych']=((B[id_].get('uwagi_danych') or '')+' v4: '+powod).strip()

# 1a. Tkaniny: brakuje sukna zwykłego i płótna zgrzebnego — a z nich szyje się 90% rzeczy.
nowa('sukno-szare-lokiec','Ubranie i dodatki','Sukno szare, samodział (łokieć)',72,
     '',"SZACUNEK, nie cytat: wyprowadzone z ceny ubrania (Kolonia 1390) minus robota krawca. "
        "Sukno krakowskie po 23 gr to sukno cienkie, importowane.")
nowa('plotno-zgrzebne-lokiec','Ubranie i dodatki','Płótno zgrzebne, konopne (łokieć)',8,
     '',"SZACUNEK: ok. ½ płótna krakowskiego; zgodne z angielskimi cenami siennika i prześcieradła z 1457 r. "
        "po uwzględnieniu, że to wyceny inwentarzowe rzeczy używanych.")
B['sukno-lokiec']['nazwa']='Sukno cienkie, importowane (łokieć)'

# Receptury: łokcie materiału + drobne dodatki (p). Produkt nie może kosztować mniej niż jego materiał.
RECEPTURY={
 'koc':                {'sukno-szare-lokiec':3},
 'zwijane-poslanie':   {'koc':1,'siennik':1,'_rzemien':12},
 'siennik':            {'plotno-zgrzebne-lokiec':4,'_slome':4},
 'przescieradlo':      {'plotno-lokiec':6},
 'recznik':            {'plotno-lokiec':2},
 'worek':              {'plotno-zgrzebne-lokiec':2},
 'duzy-worek':         {'plotno-zgrzebne-lokiec':4},
 'plocienna-plandeka': {'plotno-lokiec':14,'_impregnacja':24},
 'namiot':             {'plocienna-plandeka':2,'_maszty':48},
 'ubranie':            {'sukno-szare-lokiec':3,'plotno-lokiec':4},
 'plaszcz':            {'sukno-szare-lokiec':4},
 'oponcza':            {'sukno-szare-lokiec':5,'plotno-lokiec':2},
 'szata':              {'sukno-szare-lokiec':7},
 'kaptur-lub-maska':   {'sukno-szare-lokiec':1},
 'mundur':             {'ubranie':1},
 'stroj-dworski':      {'sukno-lokiec':10},
}
ROBOTA_MIN=1.10   # najmniej 10% ponad materiał (szycie, tkanie, wykończenie)
def koszt_materialu(id_,ceny):
    s=0
    for k,n in RECEPTURY[id_].items():
        s+= n if k.startswith('_') else ceny[k]*n
    return s
# kolejność: najpierw składniki
for id_ in ['siennik','koc','przescieradlo','recznik','worek','duzy-worek','plocienna-plandeka',
            'ubranie','plaszcz','oponcza','szata','kaptur-lub-maska','zwijane-poslanie','namiot','mundur','stroj-dworski']:
    ceny={k:v['cena_p'] for k,v in B.items()}
    m=koszt_materialu(id_,ceny); floor=m*ROBOTA_MIN
    if B[id_]['cena_p']<floor:
        ustaw(id_,ladna(math.ceil(floor)),f"tańsze niż własny materiał ({mon(m)}); podniesione do materiał +10%")

# 1b. Ćwiertnia: założenie robocze ~120 l (patrz analiza). Opis w nazwie, ceny bez zmian.
for i in ['zyto-cwiertnia','pszenica-cwiertnia','jeczmien-cwiertnia','owies-cwiertnia-obrok']:
    B[i]['uwagi_danych']=('Ćwiertnia ≈ 120 l — założenie robocze. Korzec krakowski 36–60 l (Gilewicz, Rybarski); '
      'ćwiertnię 128 l przyjął Grodecki. Przy 44 l chleb i obrok w stajni byłyby tańsze od zboża, z którego powstają.')

# 1c. Oliwa to import (oliwkowa). Lampa pali olej rzepakowy/tran.
nowa('olej-do-lampy-litr','Wyposażenie różne','Olej do lampy, rzepakowy albo tran (litr)',24,'',
     "SZACUNEK: ok. ⅕ oliwy importowanej. Bez tego godzina lampy kosztuje 20× więcej niż godzina świecy łojowej.")

# 1d. Miecz jako znak stanu — zasada Oskara. Sprawdzamy, nie zmieniamy bazy.
BAZA={k:v['cena_p'] for k,v in B.items()}

# ===================================================================
# 2. KLASY CENOWE
# ===================================================================
PALNA_ID={'rusznica','rusznica-lontowa','rusznica-dwulufowa','rusznica-samopowtarzalna','garlacz','garlacz-lontowy',
 'pistolet','pistolet-samopowtarzalny','muszkiet-kaliwer','muszkiet-hochlandzki','arkebuz','pieprzniczka',
 'gryfia-lapa','laska-pistoletowa','halabarda-pistoletowa','topor-pistoletowy','mozdzierz-reczny','bomba',
 'ladunek-zapalajacy'}
ZNAK_STANU={'miecz','poltorak','miecz-dwureczny','szabla','bulat','rapier','floret','szpada','flamberg'}
RZEZNE={'kurczak','ges','kaplon','owca-baran','swinia','robaki-6'}
ROBOCZE={'wol','krowa','ciele','pies-mysliwski','golab-pocztowy','malpa'}
KONIE={'kon-pociagowy','kon-wierzchowy','lekki-kon-bojowy','rumak','mul','kucyk'}
POJAZD={'furmanka','woz','powoz','lodka-dlubanka','lodz-wioslowa','barka-rzeczna','uprzaz-z-siodlem'}
KRUSZEC={'pierscien-srebrny','pierscien-zloty','pierscien-z-klejnotem','sygnet','berlo','grawerowana-pieczec'}
PRESTIZ={'stroj-dworski','stroj-ceremonialny-aksamit-zlotoglow-futra','perfumy','puder-do-twarzy','laska',
 'jedwabna-bielizna','strusie-pioro','lusterko-reczne'}
SUROWIEC={'sukno-lokiec','sukno-szare-lokiec','plotno-lokiec','plotno-zgrzebne-lokiec'}
NARZEDZIE_ID={'noz','kostur','palka'}   # robi wiejski kowal / kij — narzędzie, nie broń
UTRZ_EXTRA={'oliwa-litr','olej-do-lampy-litr','fajka-i-tyton','tatuaz','dokument-prawny','wpis-ucznia-do-cechu',
 'wykup-licencji-cechowej'}
POJEMNIK={'butelka','beczka-145-l','beczulka-45-l','buklak','dzban'}
NAJEM_DOLNY={'kat-w-izbie-czeladnej-tydzien','kat-w-izbie-czeladnej-miesiac','izba-na-poddaszu-miesiac'}
def klasa(p):
    i,k=p['id'],p['kat']
    if i in UTRZ_EXTRA: return 'utrzymanie'
    if i in NARZEDZIE_ID: return 'codzienne'
    if i in SUROWIEC: return 'surowiec'
    if i in KRUSZEC: return 'kruszec'
    if i in PRESTIZ: return 'prestiz'
    if k=='Czynsze i mieszkanie':
        return 'kupno' if i.startswith('kupno') else ('najem_dolny' if i in NAJEM_DOLNY else 'najem')
    if i=='warsztat': return 'kupno'
    if k in ('Jedzenie, picie, nocleg','Najmici i usługi (za tydzień)'): return 'utrzymanie'
    if i in RZEZNE: return 'rzezne'
    if i in ROBOCZE: return 'robocze'
    if i in KONIE: return 'konie'
    if i in POJAZD: return 'pojazd'
    if i in PALNA_ID or 'proch' in i or i in ('patron-12','pocisk-hakowy-1'): return 'palna'
    if k in ('Broń biała','Broń zasięgowa','Amunicja'): return 'bron'
    if k=='Pancerze': return 'pancerz'
    if k=='Księgi i dokumenty': return 'ksiega' if i.startswith('ksiega') or i=='mapa' else 'codzienne'
    if k=='Zioła, mikstury, narkotyki': return 'alchemia'
    if k=='Ubranie i dodatki': return 'odziez'
    return 'codzienne'   # narzędzia, wyposażenie, protezy, zwierzęta reszta
KL={i:klasa(p) for i,p in B.items()}

PRESETY={
 'baza':      {'opis':'v3 po poprawkach spójności, bez mnożników'},
 'x3_naiwny': {'opis':'×3 na wszystko poza jedzeniem, piciem, noclegiem i usługami — bez żadnych poprawek'},
 'drogi':     {'opis':'najbliżej ×3 Oskara: ×3 tam, gdzie spójność pozwala, mniej tam, gdzie nie'},
 'zalecany':  {'opis':'mnożniki wyprowadzone z testu rzemieślnika, budżetu Brązu 3 i punktów odniesienia z podręcznika'},
}
M={
 #            baza   drogi zalecany  x3_naiwny
 'utrzymanie':(1,1,1,1),
 'surowiec':(1,1,1,3),
 'rzezne':(1,1,1,3),
 'kruszec':(1,1,1,3),
 'najem_dolny':(1,1,1,3),
 'najem':(1,2,2,3),
 'kupno':(1,2,2,3),
 'robocze':(1,2,1,3),
 'konie':(1,2.5,1.5,3),
 'pojazd':(1,1.25,1,3),
 'codzienne':(1,1.5,1.5,3),
 'odziez':(1,2,1.5,3),
 'prestiz':(1,3,3,3),
 'bron':(1,2.5,2,3),
 'palna':(1,3,1.5,3),
 'pancerz':(1,2.25,2,3),
 'ksiega':(1,2,2,3),
 'alchemia':(1,3,1.5,3),
}
ZNAK_STANU_PREMIA={'baza':1,'drogi':1.2,'zalecany':1.5,'x3_naiwny':1}
IDX={'baza':0,'drogi':1,'zalecany':2,'x3_naiwny':3}

# Pełne naczynia: cena = naczynie (jego klasa) + zawartość (utrzymanie). Wartości zawartości w ×1.
ZAWARTOSC={'butelka-wina':('butelka',24),'beczulka-piwa-10-l':(None,18,13),'sledzie-beczka':('beczka-145-l',None)}

def zbuduj(preset):
    ix=IDX[preset]; P={}
    for i,p in B.items():
        k=M[KL[i]][ix]
        if i in ZNAK_STANU: k*=ZNAK_STANU_PREMIA[preset]
        P[i]=BAZA[i]*k
    if preset=='x3_naiwny':
        return {i:ladna(v) for i,v in P.items()}
    # pełne naczynia
    kpoj=M['codzienne'][ix]
    P['butelka-wina']=P['butelka']+24
    P['beczulka-piwa-10-l']=18+13*kpoj
    P['sledzie-beczka']=(BAZA['sledzie-beczka']-BAZA['beczka-145-l'])+P['beczka-145-l']
    return {i:(ladna(v) if preset!='baza' else round(v)) for i,v in P.items()}

# ===================================================================
# 3. TESTY
# ===================================================================
def t_reguly(C):
    g=lambda i:C[i]; b=[]
    S=lambda ids,plus=[]: sum(g(i) for i in ids)+sum(g(i)*n for i,n in plus)
    for r in REG:
        t=r['typ']
        try:
            if t=='rosnaco': ok=all(g(r['ids'][k-1])<g(r['ids'][k]) for k in range(1,len(r['ids'])))
            elif t=='min': ok=g(r['a'])>=g(r['b'])
            elif t=='suma_min': ok=g(r['a'])>S(r['skladniki'])
            elif t=='max_suma': ok=g(r['a'])<=S(r['skladniki'],r.get('plus',[]))
            elif t=='suma_zakres': q=g(r['a'])/S(r['skladniki']); ok=r['min']<=q<=r['max']
            elif t=='stosunek': q=g(r['a'])/g(r['b']); ok=r.get('min',-1e9)<=q<=r.get('max',1e9)
            elif t=='zakres': ok=r['min']<=g(r['a'])<=r['max']
        except KeyError as e: ok=False
        if not ok: b.append(r['opis'])
    return b

def t_receptury(C):
    b=[]
    for i in RECEPTURY:
        m=koszt_materialu(i,C)
        if C[i]<m: b.append(f"{B[i]['nazwa']}: {mon(C[i])} < materiał {mon(m)}")
    return b

def t_naczynia(C):
    b=[]
    if C['butelka-wina']<C['butelka']: b.append(f"pełna butelka wina {mon(C['butelka-wina'])} < pusta {mon(C['butelka'])}")
    if C['butelka-wina']<C['butelka']+20: b.append("butelka wina tańsza niż butelka + wino")
    if C['sledzie-beczka']<C['beczka-145-l']: b.append("beczka śledzi tańsza niż pusta beczka")
    return b

# Rodziny rzeczy, które gracz porównuje wzrokiem: przedział stosunku cen.
RODZINY=[
 ('plocienna-plandeka','koc',0.8,3.0,'plandeka ÷ koc'),
 ('namiot','koc',2.0,8.0,'namiot ÷ koc'),
 ('plaszcz','koc',0.8,2.5,'płaszcz ÷ koc'),
 ('ubranie','koc',1.0,3.0,'ubranie ÷ koc'),
 ('koc','przescieradlo',1.0,4.0,'koc ÷ prześcieradło'),
 ('przescieradlo','siennik',1.5,6.0,'prześcieradło ÷ siennik'),
 ('buty','rekawiczki',1.2,4.0,'buty ÷ rękawiczki'),
 ('miecz','topor',2.0,6.0,'miecz ÷ topór (znak stanu)'),
 ('miecz','bron-reczna-topor-maczuga',1.3,4.0,'miecz ÷ broń ręczna (znak stanu)'),
 ('sierp','noz',2.0,8.0,'sierp ÷ nóż'),
 ('siekiera','sierp',1.0,2.0,'siekiera ÷ sierp'),
 ('kolczuga','skorzana-kurta',4.0,20.0,'kolczuga ÷ skórzana kurta'),
 ('pelna-plytowka-4-elementy','kolczuga',2.0,8.0,'płytówka ÷ kolczuga'),
 ('kon-wierzchowy','kon-pociagowy',1.8,4.0,'koń wierzchowy ÷ pociągowy (Kraków 2,6)'),
 ('wol','krowa',1.0,1.6,'wół ÷ krowa'),
 ('krowa','ciele',2.5,8.0,'krowa ÷ cielę (2 lata chowu)'),
 ('woz','furmanka',1.5,5.0,'wóz ÷ furmanka'),
 ('lampa-oliwna','swiece-tuzin',0.8,4.0,'lampa ÷ tuzin świec'),
 ('pierscien-zloty','pierscien-srebrny',5.0,15.0,'złoty ÷ srebrny pierścień (kruszec ~11:1)'),
]
def t_rodziny(C):
    return [f"{o}: {C[a]/C[b]:.2f} poza [{lo};{hi}]" for a,b,lo,hi,o in RODZINY if not (lo<=C[a]/C[b]<=hi)]

# Mięso z tuszy vs żywe zwierzę: rzeźnik zarabia 0,7–2,5×.
TUSZA={'kurczak':1,'ges':3,'kaplon':1.5,'owca-baran':12,'swinia':45,'ciele':25,'krowa':110,'wol':150}
def t_tusze(C):
    return [f"{B[i]['nazwa']}: mięso {mon(C['mieso-kg']*kg)} ÷ żywe {mon(C[i])} = {C['mieso-kg']*kg/C[i]:.2f}"
            for i,kg in TUSZA.items() if not (0.7<=C['mieso-kg']*kg/C[i]<=2.5)]

# Monety są z kruszcu. 1 ZK ≈ 1,5 g złota (złoty polski 3,5 g = 2,29 ZK); Au:Ag ≈ 1:11.
def t_kruszec(C):
    b=[]; zloto_g_p=240/1.53; srebro_g_p=zloto_g_p/11
    for i,g,met,mx in [('pierscien-zloty',5,zloto_g_p,4),('pierscien-srebrny',5,srebro_g_p,4)]:
        w=g*met
        if C[i]>w*mx: b.append(f"{B[i]['nazwa']}: {mon(C[i])} > {mx}× wartości kruszcu ({mon(w)}) — przetopione monety dają zysk")
    return b

# Utrzymanie Brązu 3: 80% brutto musi pokryć jedzenie + kąt + odzież (samodział).
def t_budzet(C):
    b=[]; ROB=STAT['robotnik_brutto_p']
    jedz=7*14; odz=(6*C['plotno-lokiec']+3*C['sukno-szare-lokiec'])/52
    for st_,brutto,kw,okres in [('Brąz 3',165,'kat-w-izbie-czeladnej-tydzien',1),
                                ('Brąz 4',220,'izba-na-poddaszu-miesiac',4.33)]:
        utrz=0.8*brutto; czynsz=C[kw]/okres; s=jedz+czynsz+odz
        if s>utrz: b.append(f"{st_}: jedzenie {mon(jedz)} + czynsz {mon(czynsz)} + odzież {mon(odz)} = {mon(s)} > utrzymanie {mon(utrz)}/tydz.")
    # czynsz ≤ 25% brutto najemcy
    for kw,st_,brutto_tydz in [('izba-w-kamienicy-miesiac','Srebro 1',330),('mieszkanie-mieszczanskie-23-izby-miesiac','Srebro 2',660)]:
        if C[kw]/4.33>0.25*brutto_tydz: b.append(f"{B[kw]['nazwa']} > 25% brutto ({st_})")
    return b

# Karczma vs najem: miesiąc najmu ≤ ½ × 30 nocy w odpowiedniej izbie karczmy, ale ≥ ⅒ (inaczej nikt nie mieszka w karczmie).
def t_karczma(C):
    b=[]
    for kw,noc in [('kat-w-izbie-czeladnej-miesiac','wspolna-izba-na-1-noc'),('izba-w-kamienicy-miesiac','prywatny-pokoj-na-1-noc')]:
        q=C[kw]/(30*C[noc])
        if not (0.10<=q<=0.5): b.append(f"{B[kw]['nazwa']} = {q:.2f} × miesiąc w karczmie (oczekiwane 0,10–0,50)")
    return b

def t_zwrot(C):
    b=[]
    for kup,naj,lo,hi in [('kupno-dom-rzemieslnika','dom-mistrza-z-warsztatem-rok',7,25),
                          ('kupno-prosty-dom','izba-w-kamienicy-rok',7,25),
                          ('kupno-kamienica-patrycjuszowska','kamienica-kupiecka-rok',7,40)]:
        q=C[kup]/C[naj]
        if not (lo<=q<=hi): b.append(f"{B[kup]['nazwa']}: zwrot w {q:.0f} lat (oczekiwane {lo}–{hi})")
    return b

# Test rzemieślnika: cena ÷ (dni warsztatu × dzienne brutto warsztatu + materiał). SZACUNKI czasu pracy.
WARSZTAT={  # dzienne brutto (p) — z drabiny Statusu
 'kuznia_wiejska': 275/6+165/6,            # kowal Brąz 5 + pomocnik Brąz 3
 'cechowy':        990/6+275/6,            # mistrz Srebro 3 + czeladnik Brąz 5
 'zbrojmistrz':    1320/6+2*275/6,         # mistrz Srebro 4 + 2 czeladników
 'platnernia':     3600/6+2*275/6+110/6,   # mistrz Złoto 1 + 2 czeladników + uczeń
 'szewc_krawiec':  330/6+220/6,            # mistrz Srebro 1 + czeladnik Brąz 4
 'tkacz':          330/6+165/6,
 'luczarz':        330/6+220/6,
 'skryba':         330/6,
 'kolodziej':      660/6+275/6,            # Srebro 2 + czeladnik
}
WZORCE=[ # id, warsztat, dni, materiał (p, poziom ×1)
 ('noz','kuznia_wiejska',0.1,3),('sierp','kuznia_wiejska',0.25,8),('siekiera','kuznia_wiejska',0.3,12),
 ('topor','zbrojmistrz',0.5,20),('miecz','zbrojmistrz',1.5,40),('kolczuga','zbrojmistrz',10,300),
 ('napiersnik','platnernia',5,150),('pelna-plytowka-4-elementy','platnernia',25,600),
 ('buty','szewc_krawiec',1,50),('ubranie','szewc_krawiec',1.5,None),('koc','tkacz',1,120),
 ('luk-dlugi','luczarz',2,40),('ksiega-medycyna','skryba',100,1800),('woz','kolodziej',8,600),
]
def t_rzemieslnik(C,mat_mult=1,raport=False):
    b=[]; rows=[]
    for i,w,dni,mat in WZORCE:
        if mat is None: mat=koszt_materialu('ubranie',C)
        koszt=dni*WARSZTAT[w]+mat
        q=C[i]/koszt; rows.append((i,w,dni,koszt,C[i],q))
        if not (0.7<=q<=2.2): b.append(f"{B[i]['nazwa']}: cena {mon(C[i])} = {q:.1f}× kosztu warsztatu ({mon(koszt)})")
    return (b,rows) if raport else b

TESTY=[('59 reguł spójności',t_reguly),('materiał ≤ produkt',t_receptury),('pełne ≥ puste naczynie',t_naczynia),
 ('rodziny rzeczy',t_rodziny),('tusza vs żywe zwierzę',t_tusze),('biżuteria vs kruszec monety',t_kruszec),
 ('budżet utrzymania',t_budzet),('karczma vs najem',t_karczma),('zwrot z kupna domu',t_zwrot),
 ('test rzemieślnika',t_rzemieslnik)]

if __name__=='__main__':
    WYN={}
    for pr in PRESETY:
        C=zbuduj(pr); WYN[pr]={}
        print(f"\n=================== {pr.upper()} — {PRESETY[pr]['opis']}")
        for n,f in TESTY:
            b=f(C); WYN[pr][n]=b
            print(f"  {'OK ' if not b else 'ŹLE'} {n:28} {len(b)}")
            for x in b[:6]: print('        -',x)
    print("\n=== POPRAWKI BAZY ===")
    for i,a,bb,pw in POPR: print(f"  {i:28} {mon(a) if a else '(nowe)':>12} -> {mon(bb):>12}   {pw[:80]}")
