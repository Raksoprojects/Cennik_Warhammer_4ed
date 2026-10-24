# Buduje propozycję cennika v2: korekty ze źródeł historycznych + korekty spójności.
# Wynik: propozycja/cennik_v2.json, propozycja/czynsze_v2.json, propozycja/zmiany.json
import json, copy, os
os.makedirs("propozycja", exist_ok=True)
C = json.load(open("data/cennik.json"))
P = {x["id"]: x for x in C["pozycje"]}

def ladna(p):
    """Zaokrąglenie do monet, jakie podałby kupiec."""
    if p < 24: return max(1, round(p))
    if p < 120: return round(p / 6) * 6
    if p < 2400: return round(p / 12) * 12
    if p < 24000: return round(p / 120) * 120
    return round(p / 240) * 240

ORYG = {i: x["cena_p"] for i, x in P.items()}
Z = {}        # id -> zmiana (stara cena = oryginał, ostatnia korekta wygrywa)
def ustaw(i, nowa, typ, uz):
    P[i]["cena_p"] = nowa
    if nowa == ORYG[i]: Z.pop(i, None); return
    Z[i] = dict(id=i, nazwa=P[i]["nazwa"], kat=P[i]["kat"], stara_p=ORYG[i], nowa_p=nowa, typ=typ, uzasadnienie=uz)

# ---------- A. Broń i amunicja bez prochu: przeliczenie angielskich cen elżbietańskich po 7 d zamiast 4 d (×4/7)
PROCH = ("rusznica", "garlacz", "muszkiet", "pistolet", "pieprzniczka", "arkebuz", "gryfia", "mozdzierz",
         "halabarda-pistoletowa", "topor-pistoletowy", "laska-pistoletowa", "bomba", "ladunek", "proch", "patron", "pocisk-hakowy")
for x in C["pozycje"]:
    if x["kat"] not in ("Broń biała", "Broń zasięgowa", "Amunicja"): continue
    if any(k in x["id"] for k in PROCH): continue
    if x["dostepnosc"] == "Egzotyczna": continue
    nowa = ladna(x["cena_p"] * 4 / 7)
    if x["cena_p"] <= 12: nowa = x["cena_p"]           # grosze zostają (garota, tłuk, kij, proca)
    ustaw(x["id"], nowa, "historyczna",
          "Ceny broni z angielskich list milicji (kaliwer, korselet → ok. 1560–90) artefakt liczył po 4 d za dniówkę; "
          "w tym okresie robotnik brał 7–8 d. Cała grupa ×4/7 (miecz 6 s = 10 dniówek → 1 ZK 3 s 7 p).")

# ---------- B. Korekty z konkretnych danych historycznych
H = "historyczna"
ustaw("pika", 108, H, "Pika 2 s (Anglia elżb.) = 3,4 dniówki ≈ 8 s; podniesione do 9 s, żeby pika (5 m drzewca) była droższa od włóczni.")
ustaw("wlocznia", 96, "spójność", "Włócznia ≤ pika (krótsze drzewce, ten sam grot).")
ustaw("strzala-12", 60, H, "Snop 24 strzał 2 s 4 d – 5 s (Anglia elżb.) = 2–4 dniówki za tuzin → 5 s (= RAW).")
ustaw("belt-12", 60, "spójność", "Bełty jak strzały.")
ustaw("helm-otwarty-morion", 144, H, "Morion 3 s 4 d, burgonet 4 s (Anglia 1590) = 5–6 dniówek → 12 s.")
ustaw("helm-zamkniety", 1920, H, "Basinet z podszyciem 16 s 8 d (Anglia 1369) = 80 dniówek ≈ 9 ZK; 8 ZK domyka sumę płytówki: 14 + 12 + 14 + 8 = 48 ZK.")
ustaw("koc", 180, H, "Koc w inwentarzu z 1349–52: ok. 16 d = 8 dniówek ≈ 18 s; sukno w Krakowie 23 gr/łokieć. Wełniany koc nie może kosztować mniej niż dniówka. → 15 s.")
ustaw("zwijane-poslanie", 216, "spójność", "Posłanie = koc + siennik (2 d w 1457 ≈ 1 s 5 p) + rzemienie → 18 s.")
ustaw("plocienna-plandeka", 300, H, "Płótno 1 gr/łokieć (Kraków) ≈ 1 s 6 p; plandeka ok. 3×3 m to ~15 łokci + nasycenie → 1 ZK 5 s.")
ustaw("namiot", 720, "spójność", "Namiot = ok. dwie plandeki płótna + szycie, maszty, linki, śledzie → 3 ZK.")
ustaw("butelka-wina", 60, H, "Wino: garniec (3,77 l) 6–7 gr → 0,75 l ≈ 2 s (to jest dotychczasowa cena – sama zawartość). Pusta butelka 3 s (Anglia 1457: 4 d ≈ 2 s 10 p). Razem 5 s.")
ustaw("kielich-wina", 6, H, "Kielich 0,15 l wina = 5 p w hurcie (Kraków) → 6 p w gospodzie. Wino nie może być tańsze od piwa (3 p za 0,5 l) w przeliczeniu na łyk.")
ustaw("beczulka-45-l", 36, H, "Beczka 3 d (Anglia 1457) ≈ 2 s; powrót do RAW 3 s.")
ustaw("beczka-145-l", 96, "spójność", "Powrót do RAW 8 s; ok. 2,7× beczułki 45 l.")
ustaw("beczulka-piwa-10-l", 30, "spójność", "Piwo 10 l w hurcie 1 s 6 p (Kraków: achtel 137 l za 13–14 gr) + mała beczułka ok. 1 s → 2 s 6 p.")
ustaw("owca-baran", 216, H, "Baran 7–10 gr (Kraków) = 6 dniówek ≈ 13 s; Anglia XIV w. 19–24 s → 18 s.")
ustaw("kucyk", 2400, "spójność", "Kucyk nie może być droższy niż koń pociągowy (15 ZK, potwierdzony: 6–7 zł) ani muł (12 ZK) → 10 ZK.")
ustaw("ubranie", 336, H, "Kitel + nogawice 36 s (Kolonia 1390) = 12 dniówek ≈ 1 ZK 8 s; tunika chłopska z 1313 jeszcze droższa.")
ustaw("plaszcz", 300, "spójność", "Płaszcz (prostszy krój) ≤ opończa; RAW 10 s < 18 s. Kożuch 21 gr (Kraków) ≈ 1 ZK 12 s.")
ustaw("oponcza", 384, "spójność", "Zamiana z płaszczem – jak w RAW opończa droższa.")
ustaw("szpadel", 18, H, "Łopata i szufla 3 d za parę (Anglia 1457) ≈ 1 s 1 p za sztukę → 1 s 6 p.")
ustaw("motyka", 18, "spójność", "≤ szpadel.")
ustaw("grabie", 12, "spójność", "Drewniane, tańsze od żelaznej motyki.")
ustaw("lina-10-metrow", 120, "spójność", "Arkan to lina z pętlą; lina 1 ZK kosztowała tyle co buzdygan. Lina 10 s (RAW 8 s 4 p).")
ustaw("arkan", 120, "spójność", "= lina 10 m.")
ustaw("furmanka", 720, H, "Wóz okuty żelazem 4 s (Anglia ok. 1350) = 24 dniówki ≈ 2 ZK 15 s → 3 ZK.")
ustaw("woz", 2880, "spójność", "Duży wóz czterokołowy ≈ 4× furmanka → 12 ZK.")
ustaw("powoz", 24000, H, "Powóz £8 (Anglia 1381) = 850 dniówek ≈ 98 ZK → 100 ZK; królewskie £400–1000 to osobna liga.")
ustaw("barka-rzeczna", 36000, H, "Barka £10 (Anglia XIV w.) = 1200 dniówek ≈ 137 ZK → 150 ZK.")
ustaw("wpis-ucznia-do-cechu", 240, H, "Wpisowe ucznia 1–2 s (Anglia XIV w.) = 6–12 dniówek ≈ 1 ZK.")
ustaw("wykup-licencji-cechowej", 3600, H, "Przyjęcie do cechu 6 s 8 d – £3, bławatnicy 20 s (= 120 dniówek ≈ 14 ZK); list mistrzowski 2 fl (Frankfurt) ≈ 4 ZK → 15 ZK.")
# półzbroja = 1 Wada od (napierśnik + morion)
ustaw("polzbroja-municyjna-napiersnik-morion", ladna((P["napiersnik"]["cena_p"] + P["helm-otwarty-morion"]["cena_p"]) / 2), "spójność",
      "1 Wada (×½) od napierśnika + morionu (HR-024). Korselet 30 s (Anglia 1590) = 45–51 dniówek ≈ 5–6 ZK – zgodne.")
# floret ≤ szpada (po przeliczeniu grupy)
ustaw("floret", P["szpada"]["cena_p"], "spójność", "Floret (+BS+3, Tępy) słabszy od rapiera → cena szpady.")

# ---------- C. Czynsze: źródła dają 3–5× mniej
CZ = {"izba-na-poddaszu-miesiac": 96, "izba-w-kamienicy-miesiac": 144, "izba-w-kamienicy-rok": 1440,
      "mieszkanie-mieszczanskie-23-izby-miesiac": 240, "mieszkanie-mieszczanskie-rok": 2400,
      "dom-mistrza-z-warsztatem-rok": 4800, "kamienica-kupiecka-rok": 13200}
for i, v in CZ.items():
    ustaw(i, v, H, "Czynsze roczne w źródłach: chata 5 s, dom rzemieślnika 20 s, dom kupca 40–60 s (Anglia XIV w.); "
                   "murarz 1,6 fl, piwowar 4 fl, złotnik 10 fl (Frankfurt 1450) – 3–5× mniej niż w cenniku. "
                   "Ceny kupna domów zgadzają się ze źródłami, więc obniżam czynsz, nie podnoszę kupna. Zwrot z najmu wychodzi 7–15 lat.")

json.dump({**C, "opis": C["opis"] + " PROPOZYCJA v2 – nie zatwierdzona."}, open("propozycja/cennik_v2.json", "w"), ensure_ascii=False, indent=1)
cz = json.load(open("data/czynsze.json"))
nowe = {"Kąt w izbie czeladnej": (24, 84, 3 * 240), "Izba na poddaszu": (36, 96, 4 * 240), "Izba w kamienicy": (48, 144, 6 * 240),
        "Mieszkanie mieszczańskie (2–3 izby)": (72, 240, 10 * 240), "Dom mistrza z warsztatem": (144, 480, 20 * 240), "Kamienica kupiecka": (360, 1320, 55 * 240)}
for r in cz["najem"]:
    r["tydzien_p"], r["miesiac_p"], r["rok_p"] = nowe[r["kwatera"]]
json.dump(cz, open("propozycja/czynsze_v2.json", "w"), ensure_ascii=False, indent=1)
zmiany = list(Z.values())
json.dump(zmiany, open("propozycja/zmiany.json", "w"), ensure_ascii=False, indent=1)
print(len(zmiany), "zmian")
