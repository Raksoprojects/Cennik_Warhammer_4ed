# -*- coding: utf-8 -*-
import json, copy, unicodedata, re
B='/home/claude/zip_in/skarbiec-imperium/'
O='/home/claude/praca/out/'
J=lambda f: json.load(open(B+f,encoding='utf-8'))
W=lambda f,d: json.dump(d,open(O+f,'w',encoding='utf-8'),ensure_ascii=False,indent=1)

def slug(s):
    s=s.replace('ł','l').replace('Ł','L')
    s=unicodedata.normalize('NFD',s).encode('ascii','ignore').decode()
    return re.sub(r'-+','-',re.sub(r'[^a-z0-9]+','-',s.lower())).strip('-')

cen=J('propozycja/cennik_v2.json')
nowe=J('propozycja/nowe_pozycje.json')['pozycje']
poz=cen['pozycje']
byid={p['id']:p for p in poz}

# ---------- 1. KOREKTY WŁASNE -------------------------------------------
KOREKTY = {
 'furmanka':      (960,  "Wóz okuty, Anglia 1350 – 4 s przy dniówce pomocnika 1,25 d = 38 dniówek = 4 ZK 8 p. "
                         "v2 dawało 3 ZK, czyli poniżej własnego źródła."),
 'barka-rzeczna': (36000,"Barka £10 (XIV w.) przy dniówce 2,5 d = 960 dniówek ≈ 110 ZK. RAW opisuje jednostkę "
                         "o Udźwigu 300 i trzyosobowej załodze, więc biorę górną granicę przedziału."),
}
for i,(c,u) in KOREKTY.items():
    byid[i]['cena_p']=c
    byid[i]['komentarz']=(byid[i].get('komentarz') or '').strip()
    byid[i]['uwagi_danych']=u

# ---------- 2. NOWE POZYCJE ---------------------------------------------
PODST = {'Pieprz':'Kraków 1526–35: 15–16 gr/funt','Cynamon':'Kraków: 55 gr/funt','Szafran':'Kraków: 135–140 gr/funt',
 'Cukier':'Kraków: 120 gr/kamień','Jaja':'Kraków: 3 gr za kopę','Sery':'Kraków: 18–20 gr za kopę',
 'Masło':'Kraków: 26–32 gr/garniec','Żyto':'Kraków: 14–15 gr/ćwiertnię','Pszenica':'Kraków: 22–24 gr/ćwiertnię',
 'Owies':'Kraków: 7,5 gr/ćwiertnię','Chleb':'Polska XVI w.: 1/10 gr za bochenek','Mięso':'Polska XVI w.: 1 gr/kg',
 'Gęś':'Kraków: 1,5–2 gr','Kapłon':'Kraków: 2 gr','Cielę':'Kraków: 12–14 gr',
 'Sukno':'Kraków: 23 gr/łokieć','Płótno':'Kraków: 1 gr/łokieć'}
dodane=[]
for n in nowe:
    i=slug(n['nazwa'])
    if i in byid: continue
    pierwsze=n['nazwa'].split()[0].strip('(,')
    p=dict(id=i, kat=n['kat'], nazwa=n['nazwa'], zrodlo=None, cena_raw_p=None, cena_p=n['cena_p'],
           obc=None, dostepnosc='Powszechna',
           podstawa_hist=PODST.get(pierwsze, n.get('zrodlo','')),
           komentarz='Dopisane ze źródeł — towar dla kramarza i kupca korzennego.',
           dopisane='2026-10-23', uwagi_danych=n.get('uwaga') or None, pozycja_kampanii=True)
    poz.append(p); byid[i]=p; dodane.append(i)

# ---------- 3. TYP I PODTYP ---------------------------------------------
NOCLEG={'wspolna-izba-na-1-noc','prywatny-pokoj-na-1-noc','stajnia-na-1-noc','cieply-posilek-w-gospodzie'}
ZWIERZ={'kurczak','owca-baran','swinia','krowa','wol','ges','kaplon','ciele','kon-pociagowy','mul','golab-pocztowy'}
ZYWNOSC_PODST={'zyto-cwiertnia','pszenica-cwiertnia','jeczmien-cwiertnia','owies-cwiertnia-obrok','groch-korzec-43-7-l',
 'chleb-zytni-bochenek','mieso-kg','jaja-kopa-60-szt','sery-kopa-60-szt','maslo-garniec-3-77-l',
 'prowiant-na-1-dzien','jedzenie-na-zimno-na-1-dzien','pol-litra-piwa','beczulka-piwa-10-l'}
for p in poz:
    if p['kat']=='Najmici i usługi (za tydzień)': p['typ']='usluga'
    elif p['kat']=='Czynsze i mieszkanie':        p['typ']='nieruchomosc'
    elif p['id'] in NOCLEG:                       p['typ']='nocleg'
    else:                                         p['typ']='towar'
    pod=[]
    if p['id'] in ZWIERZ: pod.append('zwierze_hodowlane')
    if p['id'] in ZYWNOSC_PODST: pod.append('zywnosc_podstawowa')
    p['podtyp']=pod or None

cen['opis']=("Cennik v3 (2026-10-23). Bazuje na propozycji v2 (korekta płac angielskich wg stulecia), "
             "plus 30 pozycji ze źródeł krakowskich, dwie korekty własne (furmanka, barka) oraz pola "
             "typ/podtyp rozdzielające towar od usług i noclegu.")
cen['wersja']='v3'
W('cennik.json',cen)

# ---------- 4. CZYNSZE ---------------------------------------------------
cz=J('propozycja/czynsze_v2.json')
cz['opis']=("Stawki bazowe dla miasteczka w normalnych czasach. Mnóż przez mnożnik osady ORAZ przez "
            "mnożnik czynszu z koniunktury (koniunktura.json → czynsz).")
W('czynsze.json',cz)

# ---------- 5. KONIUNKTURA: CZYNSZ --------------------------------------
kon=J('data/koniunktura.json')
CZYNSZ={'normalna':(1.0,'bez zmian'),
 'nadmiar':(1.0,'jarmark nie rusza czynszu'),
 'niedobor':(1.1,'drożyzna przenosi się na komorne z opóźnieniem'),
 'wojna':(1.3,'napływ uchodźców ze wsi, kwaterunek wojska'),
 'zaraza':(0.6,'puste izby po zmarłych — czynsze lecą w dół, tak jak po czarnej śmierci'),
 'oblezenie':(2.0,'nikt nie wychodzi, nikt nie buduje'),
 'szlaki':(1.1,'kupcy utknęli w mieście na dłużej, zajmują kwatery')}
for k in kon['koniunktury']:
    c,u=CZYNSZ.get(k['id'],(1.0,''))
    k['czynsz']={'mnoznik':c,'uwaga':u}
kon['koniunktury'].append({
 'id':'kryzys_mieszkaniowy','nazwa':'Kryzys mieszkaniowy',
 'opis':'Pożar dzielnicy, napływ uchodźców, zajęcie kwater przez wojsko albo blokada portu. Dotyczy wyłącznie dachu nad głową.',
 'kategorie':{}, 'czynsz':{'mnoznik':3.0,'uwaga':'Marienburg w kryzysie: mieszkanie mieszczańskie 1 ZK × 1,45 × 3,0 ≈ 4 ZK 7 s — tyle, ile płacą gracze.'}})
kon['uwaga_czynsz']=('Czynsz ma własny mnożnik, niezależny od cen towarów: dach nad głową jest najbardziej '
                     'nieelastycznym dobrem, jakie istnieje, i reaguje odwrotnie niż żywność.')
W('koniunktura.json',kon)

# ---------- 6. OSADY: WYJĄTKI OD LIMITU ---------------------------------
os_=J('data/osady.json')
for o in os_['osady']:
    if o['id']=='wies':
        o['limit_omijaja_podtypy']=['zwierze_hodowlane','zywnosc_podstawowa']
        o['uwaga']=('Limit 2 ZK i wymóg Dostępności Powszechnej nie dotyczą żywego inwentarza ani '
                    'podstawowej żywności — wieś jest właśnie tym miejscem, gdzie kupuje się krowę.')
W('osady.json',os_)

# ---------- 7. RYNEK: WYKLUCZENIE USŁUG ---------------------------------
ryn=J('data/rynek.json')
ryn['asortyment']['wykluczone_typy']=['usluga','nieruchomosc','nocleg']
ryn['asortyment']['uwaga_typy']=('Handlarz nie trzyma na stanie noclegu, posiłku w gospodzie ani cudzej pracy. '
  'Ceny tych pozycji są już detaliczne (karczmarz JEST detalistą), więc marża kupca podwajałaby narzut. '
  'Kategorie zostają w cenniku i w wyszukiwarce — wypadają tylko z asortymentu, skupu i zamówień.')
W('rynek.json',ryn)

print("pozycji:",len(poz),"| dopisanych:",len(dodane))
from collections import Counter
print("typy:",dict(Counter(p['typ'] for p in poz)))
print("handlowalnych:",sum(1 for p in poz if p['typ']=='towar'))
