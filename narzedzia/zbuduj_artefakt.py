# -*- coding: utf-8 -*-
"""Składa jednoplikową stronę Skarbca z data/*.json + src/silnik.js + src/spojnosc.js.

Uruchom z katalogu repo:  python3 narzedzia/zbuduj_artefakt.py [plik_wyjściowy]
Domyślnie zapisuje reference/skarbiec_v5.html (działająca strona — wzór dla aplikacji).
Szablon: narzedzia/artefakt/szablon.html (powstaje z szablon_v4.html przez patch_v5.py).
"""
import json, re, os, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
A = R + 'narzedzia/artefakt/'
j = lambda n: json.load(open(R + n, encoding='utf-8'))
dane = {k: j('data/%s.json' % k) for k in
        ['cennik', 'kupcy', 'osady', 'koniunktura', 'rynek', 'nazwy', 'statusy', 'czynsze',
         'audyt', 'historia', 'pozycja_dochod', 'przedmioty_magiczne', 'spojnosc', 'spojnosc_v4']}
dane['klasy'] = j('data/klasy_cenowe.json')
# ceny v4 dla pozycji zmienionych w v5 (znacznik „zmienione w v5” w cenniku)
v4 = {p['id']: p['cena_p'] for p in j('propozycja/cennik_v4_zalecany.json')['pozycje']}
dane['zmiany_v5'] = {p['id']: v4[p['id']] for p in dane['cennik']['pozycje'] if p['id'] in v4 and v4[p['id']] != p['cena_p']}
blob = json.dumps(dane, ensure_ascii=False, separators=(',', ':'))
assert '</script' not in blob.lower()

def jako_skrypt(plik):
    s = open(R + plik, encoding='utf-8').read()
    s = re.sub(r'^export (function|const|let|var)', r'\1', s, flags=re.M)
    assert 'export ' not in s, [l for l in s.split('\n') if 'export ' in l][:3]
    return s
sil = open(R + 'src/silnik.js', encoding='utf-8').read()
sil = re.sub(r'^export const ZK = 240, S = 12;', 'var ZK = 240, S_ = 12;', sil, flags=re.M)
sil = sil.replace('p % ZK, s = Math.floor(r / S)', 'p % ZK, s = Math.floor(r / S_)').replace('pe = r % S,', 'pe = r % S_,')
sil = re.sub(r'^export (function|const|let|var)', r'\1', sil, flags=re.M)
assert 'export ' not in sil
spo = jako_skrypt('src/spojnosc.js')

css = open(A + 'styl.css', encoding='utf-8').read()
t = open(A + 'szablon.html', encoding='utf-8').read()
t = t.replace('/*__CSS__*/', css).replace('/*__SILNIK__*/', sil).replace('/*__SPOJNOSC__*/', spo).replace('/*__DANE__*/', blob)
out = sys.argv[1] if len(sys.argv) > 1 else R + 'reference/skarbiec_v5.html'
open(out, 'w', encoding='utf-8').write(t)
print("artefakt:", out, len(t) // 1024, "KB  (dane", len(blob) // 1024, "KB, silnik", len(sil) // 1024, "KB)")
