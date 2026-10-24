# -*- coding: utf-8 -*-
import sys; sys.path.insert(0,"/home/claude/praca/v4")
import json, copy
from model import *
PR=['baza','x3_naiwny','x3','zalecany']
C={p:zbuduj(p) for p in PR}
KNIGHT=358*240  # Srebro 5 brutto/rok, p
SR3_NETTO=198   # netto za Robotę, Srebro 3
print("=== KLUCZOWE POZYCJE ===")
KEY=['chleb-zytni-bochenek','prowiant-na-1-dzien','prywatny-pokoj-na-1-noc','koc','plocienna-plandeka','ubranie','buty',
 'sierp','noz','topor','miecz','rapier','luk','kusza','rusznica','pistolet','skorzana-kurta','kolczuga','napiersnik',
 'pelna-plytowka-4-elementy','kon-pociagowy','kon-wierzchowy','rumak','wol','woz','pierscien-zloty','stroj-dworski',
 'ksiega-medycyna','mikstura-lecznicza','izba-w-kamienicy-miesiac','mieszkanie-mieszczanskie-23-izby-miesiac',
 'kupno-dom-rzemieslnika','warsztat']
print(f"{'':36}"+''.join(f"{p:>15}" for p in PR)+f"{'tyg.Brąz3 (zal.)':>18}")
for i in KEY:
    print(f"{B[i]['nazwa'][:35]:36}"+''.join(f"{mon(C[p][i]):>15}" for p in PR)+f"{C['zalecany'][i]/165:>18.1f}")
print("\n=== PUNKTY ODNIESIENIA ===")
for p in PR:
    c=C[p]
    print(f"\n[{p}]")
    print(f"  kolczuga {mon(c['kolczuga'])} (nowe wydanie WFRP: 20 ZK)   płytówka {mon(c['pelna-plytowka-4-elementy'])} (nowe wydanie: 50–60 ZK)")
    print(f"  płytówka = {c['pelna-plytowka-4-elementy']/KNIGHT:.0%} rocznego brutto rycerza (hist. Mediolan 1441 vs £20–40: 20–40%)")
    print(f"  rumak = {c['rumak']/KNIGHT:.1f} roku brutto rycerza (hist. 1–4)")
    print(f"  miecz = {c['miecz']/SR3_NETTO:.1f} Robót Srebra 3; kolczuga = {c['kolczuga']/SR3_NETTO:.0f} Robót")
    print(f"  magiczny miecz (×50, 1 właściwość) = {mon(c['miecz']*50)}")
    mies=c['mieszkanie-mieszczanskie-23-izby-miesiac']
    print(f"  karczma: prywatny pokój × 33 noce = {mon(c['prywatny-pokoj-na-1-noc']*33)};  mieszkanie/mies.: miasto {mon(mies*1.1)}, Marienburg {mon(mies*1.45)}, Marienburg+kryzys×1,7 {mon(mies*1.45*1.7)}")
print("\n=== TEST RZEMIEŚLNIKA (cena ÷ koszt warsztatu; norma 0,7–2,2) ===")
print(f"{'':30}{'warsztat':>16}{'dni':>6}"+''.join(f"{p:>11}" for p in PR))
_,rows0=t_rzemieslnik(C['baza'],raport=True)
for (i,w,dni,koszt,_c,_q) in rows0:
    qs=[]
    for p in PR:
        _,rr=t_rzemieslnik(C[p],raport=True); q=[r for r in rr if r[0]==i][0][5]; qs.append(q)
    print(f"{B[i]['nazwa'][:29]:30}{w:>16}{dni:>6}"+''.join(f"{q:>11.2f}" for q in qs))
