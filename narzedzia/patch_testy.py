# -*- coding: utf-8 -*-
import json
R='/home/claude/praca/repo/'
P=R+'data/spojnosc.json'
s=json.load(open(P,encoding='utf-8'))
c={p['id']:p for p in json.load(open(R+'data/cennik.json',encoding='utf-8'))['pozycje']}
NOWE=[
 {"opis":"Żywy inwentarz rośnie z masą zwierzęcia","typ":"rosnaco",
  "ids":["kurczak","ges","kaplon","owca-baran","ciele","swinia","krowa"]},
 {"opis":"Zboża: owies (obrok) < jęczmień < żyto < pszenica","typ":"rosnaco",
  "ids":["owies-cwiertnia-obrok","jeczmien-cwiertnia","zyto-cwiertnia","pszenica-cwiertnia"]},
 {"opis":"Przyprawy rosną z egzotyką: pieprz < cynamon < szafran","typ":"rosnaco",
  "ids":["pieprz-funt-0-4-kg","cynamon-funt","szafran-funt"]},
 {"opis":"Płótno wielokrotnie tańsze od sukna","typ":"stosunek","a":"sukno-lokiec","b":"plotno-lokiec","min":5},
 {"opis":"Siekiera (narzędzie) tańsza od topora bojowego","typ":"rosnaco","ids":["siekiera","topor"]},
 {"opis":"Świeca woskowa droższa od łojowej (cena tuzina)","typ":"stosunek",
  "a":"swieca-woskowa-sztuka","b":"swiece-tuzin","min":1.0},
 {"opis":"Siennik < prześcieradło < koc","typ":"rosnaco","ids":["siennik","przescieradlo","koc"]},
 {"opis":"Bochenek chleba to ułamek dziennego prowiantu","typ":"stosunek",
  "a":"chleb-zytni-bochenek","b":"prowiant-na-1-dzien","max":0.5},
 {"opis":"Sukno droższe od dziennego prowiantu (łokieć to majątek)","typ":"rosnaco",
  "ids":["prowiant-na-1-dzien","sukno-lokiec"]},
]
dod=0
for r in NOWE:
    ids=[i for i in (r.get('ids',[])+[r.get('a'),r.get('b')]) if i]
    brak=[i for i in ids if i not in c]
    if brak: print("POMIJAM:",r['opis'],brak); continue
    s['reguly'].append(r); dod+=1
s['opis']="Reguły spójności cennika (v3). Test: node --test test/spojnosc.test.mjs"
json.dump(s,open(P,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print("reguł:",len(s['reguly']),"| dodanych:",dod)

# --- test: domyślnie sprawdza OBOWIĄZUJĄCY cennik + reguły strukturalne ---
T=R+'test/spojnosc.test.mjs'
t=open(T,encoding='utf-8').read()
t=t.replace("const plik = process.env.CENNIK || 'propozycja/cennik_v2.json';",
            "const plik = process.env.CENNIK || 'data/cennik.json';")
t=t.rstrip()+"""

/* --- v3: reguły strukturalne --- */
test('typ: usługi, nocleg i nieruchomości nie są towarem', () => {
  const cennik = rd(plik), rynek = rd('data/rynek.json');
  const zle = cennik.pozycje.filter(p => !p.typ);
  assert.deepEqual(zle.map(p => p.id), [], 'pozycje bez pola typ');
  const wykl = rynek.asortyment.wykluczone_typy;
  assert.ok(Array.isArray(wykl) && wykl.length, 'rynek.asortyment.wykluczone_typy musi istnieć');
  for (const p of cennik.pozycje) {
    if (p.kat === 'Czynsze i mieszkanie') assert.equal(p.typ, 'nieruchomosc', p.id);
    if (p.kat === 'Najmici i usługi (za tydzień)') assert.equal(p.typ, 'usluga', p.id);
  }
});

test('czynsze: cennik i czynsze.json podają to samo', () => {
  const cennik = rd(plik), cz = rd('data/czynsze.json');
  const C = Object.fromEntries(cennik.pozycje.map(x => [x.id, x.cena_p]));
  const slug = s => s.toLowerCase().replace(/ł/g, 'l').normalize('NFD').replace(/[\\u0300-\\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  const bledy = [];
  for (const k of cz.najem) for (const [okres, pole] of [['tydzien', 'tydzien_p'], ['miesiac', 'miesiac_p'], ['rok', 'rok_p']]) {
    const id = slug(k.kwatera) + '-' + okres;
    if (id in C && C[id] !== k[pole]) bledy.push(`${id}: cennik ${C[id]} ≠ czynsze ${k[pole]}`);
  }
  assert.deepEqual(bledy, [], '\\n' + bledy.join('\\n'));
});

test('ceny: wszystkie dodatnie i całkowite', () => {
  const cennik = rd(plik);
  const zle = cennik.pozycje.filter(p => !Number.isInteger(p.cena_p) || p.cena_p < 0);
  assert.deepEqual(zle.map(p => p.id), []);
});

test('id: unikalne', () => {
  const ids = rd(plik).pozycje.map(p => p.id);
  assert.equal(new Set(ids).size, ids.length);
});
"""
open(T,'w',encoding='utf-8').write(t)
print("test zaktualizowany")
