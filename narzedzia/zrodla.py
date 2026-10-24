# Dane historyczne z 8 źródeł artefaktu (pobrane 2026-10-23) + jedno źródło płac (Phelps Brown & Hopkins).
# Każdą cenę przeliczam na DNIÓWKI niewykwalifikowanego robotnika W TYM MIEJSCU I CZASIE,
# a dopiero potem na pensy Imperium (1 dniówka = 27,5 p). Artefakt liczył Anglię zawsze po 4 d/dzień –
# to zawyżało ceny z końca XVI w. (~7–8 d) i zaniżało ceny z XIII–XIV w. (1–2,5 d).
import json, math

DNIOWKA_P = 27.5

# dzienna płaca robotnika niewykwalifikowanego, w jednostkach lokalnych
PLACE = {
 "krk":    (1.5,  "gr",  "Kraków 1526–35: robotnik 1,5 gr/dzień [historia.org.pl]"),
 "pl16":   (1.5,  "gr",  "Polska poł. XVI w.: przyjęto jak Kraków, 1 zł = 30 gr = 20 dniówek [wielkahistoria]"),
 "en1285": (1.0,  "d",   "Anglia 1281–90: pomocnik strzecharza 1 d [UC Davis, Dyer]"),
 "en1313": (1.25, "d",   "Anglia 1311–20: 1,25 d [UC Davis, Dyer]"),
 "en1335": (1.25, "d",   "Anglia 1331–50: 1,25 d [UC Davis, Dyer]"),
 "en1350": (2.0,  "d",   "Anglia 1351–60: 2 d [UC Davis, Dyer]"),
 "en1375": (2.5,  "d",   "Anglia 1371–80: 2,5 d [UC Davis, Dyer]"),
 "en1385": (2.25, "d",   "Anglia 1381–90: 2,25 d [UC Davis, Dyer]"),
 "en1441": (4.0,  "d",   "Anglia 1441–50: 4 d [UC Davis, Dyer]"),
 "en1457": (3.25, "d",   "Anglia 1451–60: 3,25 d [UC Davis, Dyer]"),
 "en1475": (3.75, "d",   "Anglia 1461–80: 3,75 d [UC Davis, Dyer]"),
 "en1514": (4.0,  "d",   "Anglia 1501–20: 4 d [UC Davis, Dyer]"),
 "en_eliz":(7.0,  "d",   "Anglia ok. 1560–90 (lista milicji Robertsa: kaliwer, korselet): ok. 7 d – rzemieślnik 10–12 d, robotnik ~2/3 [Phelps Brown & Hopkins via rootsweb]; piechur 8 d [UC Davis]"),
 "en1590": (8.0,  "d",   "Anglia 1580–1600: robotnik 8 d [Phelps Brown & Hopkins via rootsweb; piechur 8 d, UC Davis]"),
 "ffm":    (17.0, "H",   "Frankfurt 1425–50: robotnik winnicy 14–20 H [Wikipedia DE]"),
 "fl_ffm": (1/17, "fl",  "Frankfurt XV w.: 1 gulden ≈ 17 dniówek (⚠ szacunek, ±30%)"),
 "kol":    (36.0, "Pf",  "Kolonia ok. 1390: uczeń 36 Pf/dzień jako stawka robotnika [Wikipedia DE]"),
 "rzesza": (1/20, "fl",  "Rzesza XVI w.: 1 gulden reński ≈ 20 dniówek (jak w artefakcie)"),
}
# lokalne jednostki → najmniejsza jednostka: d (pens ang.), gr, H, Pf, fl
SD = lambda s=0, d=0, L=0: L * 240 + s * 12 + d   # funty/szylingi/pensy → pensy angielskie

# (źródło, miejsce/rok, pozycja historyczna, kwota lokalna, klucz płacy, ilość→pozycja cennika, id w cenniku, uwaga)
# „ile” = ile sztuk pozycji cennika odpowiada danej historycznej (np. snop 24 strzał = 2 × „Strzała (12)”).
DANE = [
 # --- Kraków / Polska
 ("historia.org.pl", "Kraków 1530", "para butów", 7.5, "krk", 1, "buty", ""),
 ("historia.org.pl", "Kraków 1530", "para trzewików", 4.5, "krk", 1, "buty", "tańsze obuwie"),
 ("historia.org.pl", "Kraków 1530", "kożuch", 21, "krk", 1, "oponcza", "ciepłe okrycie wierzchnie"),
 ("wielkahistoria", "Polska poł. XVI w.", "elegancki kożuch 1–2 zł", 45, "pl16", 1, "plaszcz", "okrycie lepsze"),
 ("wielkahistoria", "Polska poł. XVI w.", "para dobrych butów 1–2 zł", 45, "pl16", 1, "wysokie-buty", "dobre buty"),
 ("wielkahistoria", "Polska poł. XVI w.", "czapka (5 za 1 zł)", 6, "pl16", 1, "kapelusz", ""),
 ("historia.org.pl", "Kraków 1530", "koń", 280, "krk", 1, "kon-wierzchowy", "koń bez określenia"),
 ("wielkahistoria", "Polska poł. XVI w.", "koń pociągowy ≥6–7 zł", 195, "pl16", 1, "kon-pociagowy", ""),
 ("wielkahistoria", "Polska poł. XVI w.", "koń wierzchowy 12–20+ zł", 480, "pl16", 1, "kon-wierzchowy", ""),
 ("historia.org.pl", "Kraków 1530", "wół", 75, "krk", 1, "wol", ""),
 ("wielkahistoria", "Polska poł. XVI w.", "wół 2–3 zł", 75, "pl16", 1, "wol", ""),
 ("historia.org.pl", "Kraków 1530", "wieprz", 36, "krk", 1, "swinia", ""),
 ("historia.org.pl", "Kraków 1530", "baran", 8.5, "krk", 1, "owca-baran", ""),
 ("historia.org.pl", "Kraków 1530", "kurczę", 1, "krk", 1, "kurczak", ""),
 ("wielkahistoria", "Polska poł. XVI w.", "kury (30–40 za 1 zł)", 0.86, "pl16", 1, "kurczak", ""),
 ("historia.org.pl", "Kraków 1530", "piwo, achtel 137 l → 0,5 l (hurt)", 13.5 / 274, "krk", 1, "pol-litra-piwa", "hurt"),
 ("wielkahistoria", "Polska poł. XVI w.", "piwo, 100 l za 1 zł → 0,5 l", 30 / 200, "pl16", 1, "pol-litra-piwa", "detal"),
 ("historia.org.pl", "Kraków 1530", "wino, garniec 3,77 l → 0,75 l", 6.5 * 0.75 / 3.77, "krk", 1, "butelka-wina", "sama zawartość"),
 ("historia.org.pl", "Kraków 1530", "wino → kielich 0,15 l", 6.5 * 0.15 / 3.77, "krk", 1, "kielich-wina", "hurt, bez marży"),
 ("historia.org.pl", "Kraków 1530", "piwo, achtel 137 l → 10 l", 13.5 * 10 / 137, "krk", 1, "beczulka-piwa-10-l", "sama zawartość"),
 ("wielkahistoria", "Polska poł. XVI w.", "dzienne wyżywienie sługi (½–1 gr)", 0.75, "pl16", 1, "jedzenie-na-zimno-na-1-dzien", ""),
 ("wielkahistoria", "Polska poł. XVI w.", "dzienne wyżywienie „rzadko ponad 1 gr”", 1, "pl16", 1, "prowiant-na-1-dzien", "górna granica"),
 ("historia.org.pl", "Kraków 1530", "płótno, łokieć", 1, "krk", 1, None, "surowiec: płótno"),
 ("historia.org.pl", "Kraków 1530", "sukno, łokieć", 23, "krk", 1, None, "surowiec: sukno (dobre)"),
 ("wielkahistoria", "Polska poł. XVI w.", "świece (3–4 za ¼ zł)", 7.5 / 3.5, "pl16", 1, None, "1 świeca (woskowa?)"),
 # --- Anglia
 ("UC Davis", "Anglia 1457", "łopata i szufla (para)", 3, "en1457", 2, "szpadel", ""),
 ("UC Davis", "Anglia 1457", "siekiera", 5, "en1457", 1, None, "narzędzie"),
 ("UC Davis", "Anglia 1457", "beczka", 3, "en1457", 1, "beczulka-45-l", "rozmiar nieznany"),
 ("UC Davis", "Anglia 1457", "butelka", 4, "en1457", 1, "butelka", ""),
 ("UC Davis", "Anglia 1457", "wiadro (2 za 1 s)", 6, "en1457", 1, "wiadro", ""),
 ("UC Davis", "Anglia 1457", "prześcieradło", 4, "en1457", 1, None, "pościel"),
 ("UC Davis", "Anglia 1457", "siennik", 2, "en1457", 1, None, "pościel"),
 ("UC Davis", "Anglia 1349–52", "2 prześcieradła + 4 koce = 5 s 8 d → 1 koc", (SD(5, 8) - 2 * 6) / 4, "en1350", 1, "koc", "prześcieradło ≈ 6 d"),
 ("UC Davis", "Anglia 1349–52", "garnek mosiężny", 24, "en1350", 1, "kociolek-do-gotowania", ""),
 ("UC Davis", "Anglia 1349–52", "ręcznik", 6, "en1350", 1, None, ""),
 ("UC Davis", "Anglia 1338", "świece łojowe, funt (1,5–2,5 d)", 2, "en1335", 1.5, "swiece-tuzin", "tuzin ≈ 1,5 funta"),
 ("UC Davis", "Anglia XV w.", "świece łojowe, funt 1,5 d", 1.5, "en1457", 1.5, "swiece-tuzin", ""),
 ("UC Davis", "Anglia 1338", "wieprz (2–3 s)", 30, "en1335", 1, "swinia", ""),
 ("UC Davis", "Anglia 1338", "skop (9 d – 1 s 5 d)", 13, "en1335", 1, "owca-baran", ""),
 ("UC Davis", "Anglia 1338", "drób", 1, "en1335", 1, "kurczak", ""),
 ("UC Davis", "Anglia poł. XIV w.", "krowa 9 s 5 d", SD(9, 5), "en1350", 1, "krowa", ""),
 ("UC Davis", "Anglia poł. XIV w.", "wół 13 s 1 d", SD(13, 1), "en1350", 1, "wol", ""),
 ("UC Davis", "Anglia poł. XIV w.", "owca 1 s 5 d", SD(1, 5), "en1350", 1, "owca-baran", ""),
 ("UC Davis", "Anglia XIII w.", "koń pociągowy 10–20 s", 180, "en1285", 1, "kon-pociagowy", ""),
 ("UC Davis", "Anglia XIII w.", "dobry koń wierzchowy £10", SD(L=10), "en1285", 1, "lekki-kon-bojowy", "koń wysokiej klasy"),
 ("UC Davis", "Anglia XIII w.", "koń bojowy do £80", SD(L=80), "en1285", 1, "rumak", "górna granica"),
 ("UC Davis", "Anglia 1374", "2 konie rycerza £10 → 1 koń", SD(L=5), "en1375", 1, "lekki-kon-bojowy", ""),
 ("UC Davis", "Anglia 1350", "wóz okuty żelazem 4 s", 48, "en1350", 1, "furmanka", ""),
 ("UC Davis", "Anglia 1381", "powóz (chariot) £8", SD(L=8), "en1385", 1, "powoz", "zwykły; królewskie £400–1000"),
 ("UC Davis", "Anglia XIV w.", "barka £10", SD(L=10), "en1350", 1, "barka-rzeczna", ""),
 ("UC Davis", "Anglia 1470", "buty (gentry) 4 d", 4, "en1475", 1, "buty", ""),
 ("UC Davis", "Anglia 1470", "buty z cholewami 6 d", 6, "en1475", 1, "wysokie-buty", ""),
 ("UC Davis", "Anglia 1470", "sakiewka 1,5 d", 1.5, "en1475", 1, "sakiewka", ""),
 ("UC Davis", "Anglia 1470", "kapelusz 10 d – 1 s 2 d", 12, "en1475", 1, "kapelusz", ""),
 ("UC Davis", "Anglia 1313", "tunika chłopska 3 s", 36, "en1313", 1, "ubranie", "zamożny chłop"),
 ("Wikipedia DE", "Kolonia 1390", "kitel 8 s + nogawice 28 s", 96 + 336, "kol", 1, "ubranie", ""),
 ("Wikipedia DE", "Kolonia 1390", "para butów 8 s", 96, "kol", 1, "buty", ""),
 ("Wikipedia DE", "Frankfurt 1450", "para butów 90 H", 90, "ffm", 1, "buty", ""),
 ("UC Davis", "Anglia 1382", "pierścień złoty z rubinem 26 s 8 d", SD(26, 8), "en1385", 1, "pierscien-z-klejnotem", ""),
 ("UC Davis", "Anglia 1382", "pierścień złoty z diamentem (£15 za 2)", SD(L=7.5), "en1385", 1, "pierscien-z-klejnotem", "górna półka"),
 ("UC Davis", "Anglia 1382", "srebrna łyżka (14 s za 6)", 28, "en1385", 1, "pierscien-srebrny", "porównanie: drobne srebro"),
 ("UC Davis", "Anglia 1479", "książka (7 za £5)", 1200 / 7, "en1475", 1, "ksiega-religia", "rękopis"),
 # broń i pancerz
 ("bowvsmusket", "Anglia elżb.", "łuk najlepszy 3 s 4 d", 40, "en_eliz", 1, "luk-dlugi", ""),
 ("bowvsmusket", "Anglia elżb.", "łuk II klasy 2 s 6 d", 30, "en_eliz", 1, "luk", ""),
 ("bowvsmusket", "Anglia elżb.", "łuk III klasy 2 s", 24, "en_eliz", 1, "krotki-luk", ""),
 ("bowvsmusket", "Anglia elżb.", "snop strzał (24) 2 s 4 d", 28, "en_eliz", 2, "strzala-12", ""),
 ("bowvsmusket", "Anglia elżb.", "snop strzał liberyjnych 5 s", 60, "en_eliz", 2, "strzala-12", "lepsze"),
 ("bowvsmusket", "Anglia elżb.", "pika 2 s", 24, "en_eliz", 1, "pika", ""),
 ("bowvsmusket", "Anglia elżb.", "miecz 6 s", 72, "en_eliz", 1, "miecz", ""),
 ("bowvsmusket", "Anglia elżb.", "arkebuz 8 s", 96, "en_eliz", 1, "rusznica", "WFRP: rusznica = arkebuz"),
 ("bowvsmusket", "Anglia elżb.", "kaliwer 20 s", 240, "en_eliz", 1, "muszkiet-kaliwer", ""),
 ("bowvsmusket", "Anglia elżb.", "korselet 30 s", 360, "en_eliz", 1, "polzbroja-municyjna-napiersnik-morion", "zbroja municyjna"),
 ("bowvsmusket", "Anglia elżb.", "20 kul 2 d + proch ~½ funta (6 d) → 12 strzałów", 2 * 12 / 20 + 6, "en_eliz", 1, "pocisk-i-proch-12", "szacunek ładunku"),
 ("UC Davis", "Anglia 1590", "korselet kompletny 30 s", 360, "en1590", 1, "polzbroja-municyjna-napiersnik-morion", ""),
 ("UC Davis", "Anglia 1590", "napierśnik z naramiennikami 26 s 8 d", 320, "en1590", 1, None, "napierśnik+naramienniki, municyjne"),
 ("UC Davis", "Anglia 1590", "zbroja kopijnicza £3 6 s 8 d", 800, "en1590", 1, "pelna-plytowka-4-elementy", "municyjna, ¾"),
 ("UC Davis", "Anglia 1590", "morion 3 s 4 d", 40, "en1590", 1, "helm-otwarty-morion", ""),
 ("UC Davis", "Anglia 1590", "burgonet 4 s", 48, "en1590", 1, "helm-otwarty-morion", ""),
 ("UC Davis", "Anglia 1441", "gotowa zbroja mediolańska £8 6 s 8 d", 2000, "en1441", 1, "pelna-plytowka-4-elementy", "dobra, importowana"),
 ("UC Davis", "Anglia 1441", "zbroja giermka £5 – £6 16 s 8 d", 1420, "en1441", 1, "pelna-plytowka-4-elementy", ""),
 ("UC Davis", "Anglia 1369", "basinet 13 s 4 d + podszycie 3 s 4 d", 200, "en1375", 1, "helm-zamkniety", ""),
 ("UC Davis", "Anglia 1374", "cała zbroja rycerza £16 6 s 8 d", 3920, "en1375", 1, "zbroja-mistrzowska-na-miare-mediolan-norymberga", "cały rynsztunek"),
 ("UC Davis", "Anglia 1340", "tani miecz chłopski 6 d", 6, "en1335", 1, None, "= miecz z Wadami"),
 ("UC Davis", "Anglia poł. XVII w.", "para pistoletów kołowych £2 16 s → 1", 336, "en1590", 1, "pistolet", "⚠ XVII w., płaca ~8–12 d"),
 ("UC Davis", "Anglia poł. XVII w.", "muszkiet 16 s 6 d – 18 s 6 d", 210, "en1590", 1, "muszkiet-kaliwer", "⚠ XVII w."),
 # nieruchomości i usługi
 ("UC Davis", "Anglia pocz. XIV w.", "chata £2", 480, "en1313", 1, "kupno-prosty-dom", ""),
 ("UC Davis", "Anglia pocz. XIV w.", "dom rzemieślnika £10–15", 3000, "en1313", 1, "kupno-dom-rzemieslnika", ""),
 ("UC Davis", "Anglia pocz. XIV w.", "dom kupca £33–66", 11880, "en1313", 1, "kupno-kamienica-patrycjuszowska", "dom kupiecki"),
 ("UC Davis", "Anglia XIV w.", "czynsz: dom rzemieślnika 20 s/rok", 240, "en1313", 1, "dom-mistrza-z-warsztatem-rok", ""),
 ("UC Davis", "Anglia XIV w.", "czynsz: dom kupca 40–60 s/rok", 600, "en1313", 1, "kamienica-kupiecka-rok", ""),
 ("UC Davis", "Anglia XIV w.", "czynsz: chata 5 s/rok", 60, "en1313", 1, "izba-w-kamienicy-rok", "porównanie"),
 ("Wikipedia DE", "Frankfurt 1450", "dom prosty 20–30 fl", 25, "fl_ffm", 1, "kupno-prosty-dom", ""),
 ("Wikipedia DE", "Frankfurt 1450", "dom rzemieślnika 40–100 fl", 70, "fl_ffm", 1, "kupno-dom-rzemieslnika", ""),
 ("Wikipedia DE", "Frankfurt 1450", "dom patrycjusza ok. 800 fl", 800, "fl_ffm", 1, "kupno-kamienica-patrycjuszowska", ""),
 ("Wikipedia DE", "Frankfurt 1450", "czynsz: murarz 1,6 fl/rok", 1.6, "fl_ffm", 1, "izba-w-kamienicy-rok", ""),
 ("Wikipedia DE", "Frankfurt 1450", "czynsz: piwowar 4 fl/rok", 4, "fl_ffm", 1, "mieszkanie-mieszczanskie-rok", ""),
 ("Wikipedia DE", "Frankfurt 1450", "czynsz: złotnik 10 fl/rok", 10, "fl_ffm", 1, "dom-mistrza-z-warsztatem-rok", ""),
 ("Wikipedia DE", "Frankfurt 1425", "koń 20–24 fl", 22, "fl_ffm", 1, "kon-wierzchowy", ""),
 ("Wikipedia DE", "Frankfurt 1425", "bydlę 4 fl", 4, "fl_ffm", 1, "krowa", ""),
 ("UC Davis", "Anglia XIV w.", "wpis ucznia do cechu 1–2 s", 18, "en1350", 1, "wpis-ucznia-do-cechu", ""),
 ("UC Davis", "Anglia XIV w.", "przyjęcie do cechu (bławatnicy) 20 s", 240, "en1350", 1, "wykup-licencji-cechowej", ""),
 ("Wikipedia DE", "Frankfurt 1380", "list mistrzowski 2 fl", 2, "fl_ffm", 1, "wykup-licencji-cechowej", ""),
 ("UC Davis", "Anglia 1331", "łóżko w gospodzie, Londyn 1 d/os.", 1, "en1335", 1, "wspolna-izba-na-1-noc", ""),
 ("UC Davis", "Anglia 1331", "służba: 4 os. × 2 noce 1 d → 7 nocy", 7 / 8, "en1335", 1, "kat-w-izbie-czeladnej-tydzien", "nocleg sług"),
 ("UC Davis", "Anglia kon. XVI w.", "piechur 8 d/dzień ×6", 48, "en1590", 1, "robotnik-niewykwalifikowany", "żołd ≈ płaca robotnika"),
 ("UC Davis", "Anglia kon. XVI w.", "kawalerzysta 18 d/dzień ×6", 108, "en1590", 1, "doswiadczony-najemnik", ""),
 ("kriegsreisende", "Rzesza XVI w.", "lancknecht 4 fl/mies. → tydzień", 4 * 12 / 52, "rzesza", 1, "doswiadczony-najemnik", ""),
 ("historia.org.pl", "Kraków 1530", "czeladnik 2,5 gr/dzień ×6", 15, "krk", 1, "czeladnik", ""),
 ("historia.org.pl", "Kraków 1530", "robotnik 1,5 gr ×6", 9, "krk", 1, "robotnik-niewykwalifikowany", ""),
 ("historia.org.pl", "Kraków 1530", "cieśla 30–40 gr/tydz.", 35, "krk", 1, "mistrz-rzemiosla", ""),
 ("wielkahistoria", "Polska XVI w.", "golibroda królewski 100 zł/rok → tydzień", 3000 / 52, "pl16", 1, "doktor-na-tydzien", ""),
]

def policz(cennik):
    C = {x["id"]: x for x in cennik}
    out = []
    for z, gdzie, poz, kw, w, ile, cid, uw in DANE:
        val, unit, _ = PLACE[w]
        d = kw / val                      # dniówki = kwota / dzienna płaca (dla fl: płaca w guldenach)
        p = d * DNIOWKA_P / ile
        teraz = C[cid]["cena_p"] if cid else None
        out.append(dict(zrodlo=z, gdzie=gdzie, pozycja=poz, dniowki=round(d / ile, 2), hist_p=round(p),
                        id=cid, teraz_p=teraz, stosunek=round(teraz / p, 2) if teraz else None, uwaga=uw))
    return out

if __name__ == "__main__":
    c = json.load(open("data/cennik.json"))["pozycje"]
    r = policz(c)
    json.dump({"place": {k: v[2] for k, v in PLACE.items()}, "dane": r}, open("narzedzia/zrodla_wynik.json", "w"), ensure_ascii=False, indent=1)
    for x in r:
        print(f"{x['id'] or '-':34s} {x['hist_p']:>7}p  teraz {x['teraz_p'] or '-':>7}  ×{x['stosunek'] or '':<5} {x['gdzie']}: {x['pozycja']}")
