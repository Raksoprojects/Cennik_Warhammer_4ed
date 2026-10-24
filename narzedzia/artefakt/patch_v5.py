# -*- coding: utf-8 -*-
"""szablon_v4.html → szablon.html (v5): cena bazowa obok ceny kupca, modyfikatory w nawiasach,
cena minimalna, osobowość kupca, targowanie w sklepie, panel „Ustawienia MG”, test spójności na żywo."""
import os
H = os.path.dirname(os.path.abspath(__file__)) + '/'
t = open(H + 'szablon_v4.html', encoding='utf-8').read()
def R(old, new, cnt=1):
    global t
    assert t.count(old) == cnt, (t.count(old), old[:80])
    t = t.replace(old, new)

# ---------------------------------------------------------------- CSS
R(""".kv b{font-family:var(--mono);font-variant-numeric:tabular-nums}""",
""".kv b{font-family:var(--mono);font-variant-numeric:tabular-nums}
/* --- v5 --- */
.baza{color:var(--ink-3);font-size:12px}
.minp{color:var(--ink-2)}
.targ{color:var(--ok);font-weight:700}
.mods{font-size:12px;color:var(--ink-2);margin-top:6px}
.ustgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(300px,100%),1fr));gap:14px}
.rule,.ustgrid>*,.rules>*{min-width:0}
#ustawienia .genbar{grid-template-columns:repeat(auto-fit,minmax(min(200px,100%),1fr))!important}
.ust input.numin{padding:5px 7px;width:84px;text-align:right;font-family:var(--mono)}
.ust td{vertical-align:middle}
.ust .wide{width:100%;text-align:left}
.zr-dane{background:var(--ok-bg);color:var(--ok)}
.zr-zasada{background:var(--nowe-bg);color:var(--nowe)}
.zr-brak{background:var(--surface-2);color:var(--ink-3)}
.zr-sprzeczne{background:var(--zmiana-bg);color:var(--zmiana)}
.btnrow{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
.btn2{padding:7px 12px;border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:3px;font:inherit;font-size:13px;cursor:pointer}
.btn2:hover{border-color:var(--accent)}
textarea.json{width:100%;min-height:180px;font-family:var(--mono);font-size:12px;padding:8px;border:1px solid var(--line);border-radius:3px;background:var(--surface);color:var(--ink)}
.okline{color:var(--ok)} .errline{color:var(--gora)}
.ustbadge{display:inline-block;margin-left:8px;font-size:11px;padding:2px 8px;border-radius:999px;background:var(--zmiana-bg);color:var(--zmiana);font-weight:700}
""")

# ---------------------------------------------------------------- nagłówek i „co nowego”
start = t.index('<header class="top">'); end = t.index('<section id="kurs">')
t = t[:start] + """<header class="top">
  <div class="top-in">
    <div class="eyebrow">Warhammer Fantasy Roleplay 4 ed. &middot; cennik v5 &middot; 24 października 2026<span class="ustbadge" id="ustBadge" hidden>własne ustawienia</span></div>
    <h1>Skarbiec <em>Imperium</em></h1>
    <p class="lede">Cennik, zarobki i generator kupców na jednych danych z repozytorium kampanii.
      W v5 każdy mnożnik ceny ma podane źródło. Tam, gdzie źródła nie było, mnożnik zniknął.
      Cena z cennika stoi teraz zawsze obok ceny kupca, a miasto i sytuacja pokazują, ile dokładają.</p>
    <div class="keystats">
      <div class="keystat"><b>365</b><span>pozycji cennika, preset „zalecany” v5.2</span></div>
      <div class="keystat"><b>134 / 42</b><span>pozycji tańszych / droższych niż w v4</span></div>
      <div class="keystat"><b>186</b><span>pozycji ze źródłem; 179 bez &mdash; oznaczone</span></div>
      <div class="keystat"><b>34</b><span>testów, wszystkie przechodzą</span></div>
    </div>
  </div>
</header>

<nav class="sticky">
  <div class="nav-in">
    <a href="#v5">Co nowego</a>
    <a href="#kurs">Kurs</a>
    <a href="#status">Zarobki</a>
    <a href="#cennik">Cennik</a>
    <a href="#kupcy">Kupiec</a>
    <a href="#zamowienie">Zamówienie</a>
    <a href="#czynsze">Czynsze</a>
    <a href="#modyfikatory">Modyfikatory</a>
    <a href="#ustawienia">Ustawienia MG</a>
    <a href="#historia">Historia</a>
    <a href="#audyt">Audyt</a>
    <a href="#zasady">Zasady</a>
    <button id="themeBtn" type="button">tryb</button>
  </div>
</nav>

<div class="wrap">

<section id="v5">
  <div class="sec-head"><h2>Co się zmieniło w v5</h2><span class="note">analiza wszystkich 364 pozycji</span></div>
  <div class="findings">
    <div class="finding err">
      <div class="fnum">DROŻEJ DLA DROŻEJ</div>
      <div>
        <h3>Pięć mnożników nie miało żadnej podstawy &mdash; zniknęły</h3>
        <p>Sprawdziłem każdą klasę cenową wobec źródeł i testu rzemieślnika. Codzienne ×1,5, broń palna ×1,5,
          alchemia ×1,5, prestiż ×3 i konie robocze ×1,5 nie wynikały z niczego. Teraz: codzienne ×1,2
          (źródła i test kowala dają 1,15), palna ×1 (baza = źródło = RAW), alchemia ×1 (brak danych),
          prestiż ×1,5, konie robocze ×1 (Kraków trafia co do floreny). Konie bojowe zostają ×1,5.</p>
        <p>Prestiż ×3 łamał też Twoją zasadę: strój dworski kosztował 90 ZK, płytówka 96 ZK. Teraz 45 ZK,
          a nowa reguła pilnuje, żeby płytówka była co najmniej 2× droższa.</p>
        <p><strong>168 pozycji potaniało, żadna nie podrożała.</strong> Preset „zalecany v4” jest w Ustawieniach MG &mdash; jedno kliknięcie przywraca stare ceny.</p>
      </div>
    </div>
    <div class="finding fix">
      <div class="fnum">NOWE</div>
      <div>
        <h3>Cena bazowa obok ceny kupca. Osada i sytuacja z modyfikatorem w nawiasie</h3>
        <p>U kupca każda pozycja ma teraz trzy ceny: <strong>bazową</strong> (z cennika),
          <strong>jego</strong> (z wszystkimi mnożnikami) i <strong>minimalną</strong> &mdash; poniżej niej nie zejdzie
          przy targowaniu, bo traci na transakcji. Lista wyboru pokazuje np. „Altdorf (+30%)” i
          „Wojna (broń, strzelecka, amunicja, pancerze +80% · jedzenie +30% · reszta +5% · czynsz +30%)”.</p>
        <p>Kupiec ma też <strong>osobowość</strong>: swój rdzeń sprzedaje 5% taniej, boczny asortyment 10% drożej,
          a na każdą pozycję rzuca 1k10 na kaprys (od −10% do +10%). Razem nigdy poza −15% … +20%.
          Kaprys ma osobny strumień losowania: stare seedy dają ten sam asortyment.</p>
      </div>
    </div>
    <div class="finding fix">
      <div class="fnum">SPRAWDZONE</div>
      <div>
        <h3>Zarobki profesji pasują do cen</h3>
        <p>Codzienne życie Brązu 3 mieści się w 80% brutto. Narzędzia zawodu kosztują 1&ndash;8 tygodni brutto
          profesji, która ich używa (halabarda strażnika, łuk łowczyni, pistolet łowcy czarownic). Kapitał
          kosztuje od pół roku do 2,5 roku: płytówka = 27% roku rycerza (źródła 20&ndash;40%), rumak = 2,3 roku
          (źródła 1&ndash;4), wół = 8,7 tygodnia chłopa (Kraków 8,3).</p>
      </div>
    </div>
    <div class="finding">
      <div class="fnum">DECYZJE MG</div>
      <div>
        <h3>Konie i broń palna drogie, alchemia osiągalna, kramarz bez 47 namiotów</h3>
        <p><strong>Konie bojowe</strong>: rumak 825 ZK. <strong>Wozy ×1,5</strong>: furmanka 6 ZK, wóz 18 ZK.
          <strong>Łuk elfi</strong> = 5× łuk długi. <strong>Broń palna ×2</strong>: pistolet 20 ZK, rusznica 6 ZK.
          <strong>Alchemia</strong>: składniki po cenach podręcznika, mikstury i eliksiry ×2 (mikstura lecznicza 1 ZK 10 s).</p>
        <p><strong>Kupiec ma majątek</strong>: towar na stanie i gotówkę zależne od Statusu. Kramarz trzyma drobiazgi po sztuce,
          płatnerz kilka zbroi; skup ponad gotówkę oznaczony. <strong>Trzy ceny</strong> po kolei: podręcznik, cennik, kupiec.
          <strong>Wspólna izba</strong> to ława albo podłoga; doszedł nocleg w stajni na sianie.
          <strong>Dochód</strong> 17 poziomów profesji obniżony (służba, straż, wojsko, dokerzy) &mdash; Pozycja bez zmian.</p>
      </div>
    </div>
  </div>
</section>

""" + t[end:]

# ---------------------------------------------------------------- cennik
R("""  <div class="sec-head"><h2>Cennik</h2><span class="note">361 pozycji &middot; ceny wytwórcy</span></div>
  <p class="muted">To są <strong>ceny wytwórcy</strong> &mdash; u źródła, hurtem. Cena, którą zapłaci gracz,
    powstaje dopiero w zakładce <a href="#kupcy">Kupiec</a>. „Tyg. pracy" to liczba tygodni <em>całego</em>
    dochodu prostego robotnika (165 p).</p>""",
"""  <div class="sec-head"><h2>Cennik</h2><span class="note" id="cenyNote">364 pozycji &middot; ceny bazowe</span></div>
  <p class="muted"><strong>Cena bazowa</strong> to cena wytwórcy w obowiązującym presecie &mdash; u źródła, hurtem.
    Cena, którą zapłaci gracz, powstaje dopiero w zakładce <a href="#kupcy">Kupiec</a>. „×1” to poziom przed
    mnożnikiem klasy. „Tyg. pracy” to liczba tygodni <em>całego</em> dochodu prostego robotnika (165 p).</p>""")
R("""    <thead><tr><th>Przedmiot</th><th>RAW</th><th>Cena wytwórcy</th><th>Tyg. pracy</th><th>Podstawa historyczna</th><th>Komentarz</th></tr></thead>
    <tbody id="cenyBody"></tbody>""",
"""    <thead><tr><th>Przedmiot</th><th>Podręcznik (RAW)</th><th>Cena bazowa (cennik)</th><th>Klasa cenowa</th><th>Tyg. pracy</th><th>Podstawa historyczna</th><th>Komentarz</th></tr></thead>
    <tbody id="cenyBody"></tbody>""")

# ---------------------------------------------------------------- kupiec
R("""    <div class="seedrow">
      <div style="flex:1"><label class="lab" for="genSeed">Seed</label><input class="numin" id="genSeed" type="text" inputmode="numeric"></div>
      <button class="genbtn" id="genBtn" type="button">Losuj</button>
    </div>
  </div>
  <div class="shop" id="shop"></div>""",
"""    <div class="seedrow">
      <div style="flex:1"><label class="lab" for="genSeed">Seed</label><input class="numin" id="genSeed" type="text" inputmode="numeric"></div>
      <button class="genbtn" id="genBtn" type="button">Losuj</button>
    </div>
    <div><label class="lab" for="genPS">PS gracza w Targowaniu</label><input class="numin" id="genPS" type="number" min="0" max="10" step="1" value="0"></div>
  </div>
  <p class="mods" id="genMods"></p>
  <div class="shop" id="shop"></div>""")

# ---------------------------------------------------------------- modyfikatory
R("""  <div class="callout"><p class="mono" style="font-size:14px">cena u kupca = cena wytwórcy × marża zawodu ×
    mnożnik osady × koniunktura[kategoria] × macierz[zapas][popyt]</p></div>""",
"""  <div class="callout"><p class="mono" style="font-size:14px">cena u kupca = cena bazowa × marża zawodu ×
    preferencja × kaprys × osada × koniunktura[kategoria] × macierz[zapas][popyt]</p>
    <p class="mono" style="font-size:13px">cena minimalna = koszt nabycia × 1,05 (przy wyprzedaży × 0,9) &middot;
    koszt nabycia = cena bazowa × osada × koniunktura (wytwórca: × 0,8)</p></div>""")
R("""    <div class="rule"><h3>4. Popyt i zapas</h3>""",
"""    <div class="rule"><h3>2a. Osobowość kupca (v5)</h3>
      <p>Specjalista sprzedaje swój rdzeń taniej, a to, czym handluje przy okazji, drożej. Na każdą pozycję
        rzuca 1k10 na kaprys. Iloczyn preferencji i kaprysu mieści się w granicach poniżej.</p>
      <div id="osobDoc"></div></div>
    <div class="rule"><h3>4. Popyt i zapas</h3>""")

# ---------------------------------------------------------------- ustawienia MG
R("""<section id="historia">""", """<section id="ustawienia">
  <div class="sec-head"><h2>Ustawienia MG</h2><span class="note">zapisywane w tej przeglądarce</span></div>
  <p class="muted">Zmieniasz mnożnik klasy, marżę kupca, osadę albo cenę jednej pozycji &mdash; cała strona przelicza się od razu.
    Ustawienia zostają w tej przeglądarce. <strong>Eksport</strong> daje plik w formacie <span class="mono">data/ustawienia.json</span>:
    wklej go do repozytorium, żeby stał się domyślny dla aplikacji.</p>
  <div class="genbar" style="grid-template-columns:1fr 1fr auto">
    <div><label class="lab" for="ustPreset">Preset cennika</label><select id="ustPreset"></select></div>
    <div><label class="lab" for="ustPremia">Premia znaku stanu (miecze)</label><input class="numin" id="ustPremia" type="number" step="0.05" min="0.5" max="5"></div>
    <div><button class="genbtn" id="ustSpoj" type="button">Sprawdź spójność</button></div>
  </div>
  <div id="ustSpojWynik"></div>
  <div class="ustgrid ust" style="margin-top:14px">
    <div class="rule" style="grid-column:1/-1"><h3>Mnożniki klas</h3>
      <p class="small muted">Tag mówi, skąd jest mnożnik: <span class="pill zr-dane">dane</span> źródło albo test rzemieślnika,
        <span class="pill zr-zasada">zasada domowa</span> Twoja kotwica, <span class="pill zr-brak">brak danych</span>,
        <span class="pill zr-sprzeczne">sprzeczne</span>.</p>
      <div class="tablewrap" style="margin-top:8px"><table><thead><tr><th>Klasa</th><th>Poz.</th><th>Mnożnik</th><th>Skąd</th></tr></thead>
      <tbody id="ustKlasy"></tbody></table></div></div>
    <div class="rule"><h3>Osady</h3>
      <div class="tablewrap" style="margin-top:8px"><table><thead><tr><th>Osada</th><th>Mnożnik</th></tr></thead>
      <tbody id="ustOsady"></tbody></table></div>
      <h3 style="margin-top:16px">Kupcy &mdash; marża</h3>
      <div class="tablewrap" style="margin-top:8px"><table><thead><tr><th>Kupiec</th><th>Marża</th><th>Skup</th></tr></thead>
      <tbody id="ustKupcy"></tbody></table></div></div>
    <div class="rule"><h3>Rynek</h3>
      <div class="tablewrap" style="margin-top:8px"><table><tbody id="ustRynek"></tbody></table></div>
      <h3 style="margin-top:16px">Koniunktura &mdash; mnożnik kategorii</h3>
      <div class="genbar" style="grid-template-columns:1fr;padding:0;border:0;background:none;margin:6px 0">
        <select id="ustKon"></select></div>
      <div class="tablewrap"><table><tbody id="ustKonKat"></tbody></table></div></div>
    <div class="rule"><h3>Cena jednej pozycji</h3>
      <p class="small muted">Nadpisuje cenę bazową. Wpisz np. „4 ZK”, „15 s 6 p” albo samą liczbę pensów. Puste pole usuwa nadpisanie.</p>
      <div class="genbar" style="grid-template-columns:2fr 1fr auto;padding:0;border:0;background:none;margin:6px 0">
        <div><input class="numin wide" id="ustPozNazwa" list="ustPozLista" placeholder="pozycja…" autocomplete="off"><datalist id="ustPozLista"></datalist></div>
        <div><input class="numin wide" id="ustPozCena" placeholder="cena"></div>
        <div><button class="btn2" id="ustPozBtn" type="button">Ustaw</button></div>
      </div>
      <div id="ustPozLista2"></div></div>
  </div>
  <div class="rule" style="margin-top:14px"><h3>Zmienione ceny względem cennika v5</h3><div id="ustRoznice" class="small"></div></div>
  <div class="rule" style="margin-top:14px"><h3>Ustawienia jako JSON</h3>
    <textarea class="json" id="ustJson" spellcheck="false"></textarea>
    <div class="btnrow">
      <button class="btn2" id="ustJsonBtn" type="button">Zastosuj JSON</button>
      <button class="btn2" id="ustEksport" type="button">Eksportuj plik</button>
      <label class="btn2" for="ustImport" style="display:inline-block">Importuj plik<input id="ustImport" type="file" accept="application/json,.json" hidden></label>
      <button class="btn2" id="ustReset" type="button">Przywróć domyślne</button>
    </div>
    <p class="small" id="ustMsg" style="margin-top:6px"></p></div>
</section>

<section id="historia">""")

# ---------------------------------------------------------------- zasady: targowanie
R("""Ostatnie sztuki przy wysokim popycie: kara −20. <strong>Dolna granica to cena z cennika</strong> &mdash;
        kto już sprzedaje taniej (paser, kowal), nie schodzi dalej.</p></div>""",
"""Ostatnie sztuki przy wysokim popycie: kara −20. <strong>Dolna granica to cena minimalna kupca</strong>
        (koszt nabycia + 5%, przy wyprzedaży koszt − 10%) &mdash; kto już sprzedaje taniej (paser), nie schodzi dalej.</p></div>""")
R("""  <p>Dane i silnik: repozytorium <strong>skarbiec-imperium</strong>, cennik v3 (23.10.2026), 361 pozycji.
    Ta strona liczy dokładnie tym samym kodem co <span class="mono">src/silnik.js</span> i czyta te same
    pliki <span class="mono">data/*.json</span> &mdash; nie da się ich rozjechać.</p>""",
"""  <p>Dane i silnik: repozytorium <strong>skarbiec-imperium</strong>, cennik v5 (24.10.2026), 364 pozycje.
    Ta strona liczy dokładnie tym samym kodem co <span class="mono">src/silnik.js</span> i <span class="mono">src/spojnosc.js</span>
    i czyta te same pliki <span class="mono">data/*.json</span> &mdash; nie da się ich rozjechać.</p>""")

# ---------------------------------------------------------------- skrypt: wczytanie danych + ustawienia
R("""<script>
/*__SILNIK__*/
</script>""", """<script>
/*__SILNIK__*/
/*__SPOJNOSC__*/
</script>""")
R("""var D = JSON.parse(document.getElementById('dane').textContent);
var ROBOTNIK = D.statusy.robotnik_brutto_p;
var poId = {}; D.cennik.pozycje.forEach(function(p){ poId[p.id] = p; });
""", """var D_BAZA = JSON.parse(document.getElementById('dane').textContent);
var KLUCZ_UST = 'skarbiec-ustawienia-v5';
function ustPuste(){ return {wersja:1,preset:D_BAZA.klasy.domyslny,mnozniki:{},premia_znak_stanu:null,pozycje:{},osady:{},koniunktury:{},kupcy:{},rynek:{}}; }
function wczytajUst(){ try{ var s=localStorage.getItem(KLUCZ_UST); if(s) return Object.assign(ustPuste(),JSON.parse(s)); }catch(e){} return ustPuste(); }
function zapiszUst(){ try{ localStorage.setItem(KLUCZ_UST,JSON.stringify(UST)); }catch(e){} }
var UST = wczytajUst(), D, poId, ODSWIEZ = [];
function przelicz(){
  try{ D = zastosujUstawienia(D_BAZA, UST); }
  catch(e){ UST = ustPuste(); D = zastosujUstawienia(D_BAZA, UST); }
  poId = {}; D.cennik.pozycje.forEach(function(p){ poId[p.id] = p; });
}
przelicz();
var ROBOTNIK = D.statusy.robotnik_brutto_p;
function odswiez(){ przelicz(); ODSWIEZ.forEach(function(f){ f(); }); zapiszUst();
  var wlasne=JSON.stringify(UST)!==JSON.stringify(ustPuste()); document.getElementById('ustBadge').hidden=!wlasne; }
function etOsady(o){ return etykietaOsady(o); }
function etKon(k){ return etykietaKoniunktury(D,k,{krotko:true}); }
""")
R("""function fill(sel,arr,val,lab,def){
  sel.innerHTML=arr.map(function(x,i){""", """function fill(sel,arr,val,lab,def){
  if(def==null && sel.value) def=sel.value;
  sel.innerHTML=arr.map(function(x,i){""")

# zarobki: render do ODSWIEZ
R("""  sel.addEventListener('change',function(){ostatniRzut=null;render();});
  maj.addEventListener('change',function(){ostatniRzut=null;render();});""",
"""  sel.addEventListener('change',function(){ostatniRzut=null;render();});
  maj.addEventListener('change',function(){ostatniRzut=null;render();});
  ODSWIEZ.push(render);""")

# ---------------------------------------------------------------- cennik: kolumny
R("""      if(stF.val==='zmienione wobec RAW' && (c.cena_raw_p==null || c.cena_raw_p===c.cena_p)) return false;
      if(stF.val==='dopisane' && !c.dopisane) return false;""",
"""      if(stF.val==='zmienione wobec RAW' && (c.cena_raw_p==null || c.cena_raw_p===c.cena_p)) return false;
      if(stF.val==='dopisane' && !c.dopisane) return false;
      if(stF.val==='zmienione w v5' && !(c.id in D.zmiany_v5)) return false;
      if(stF.val==='nadpisane' && !c.nadpisane) return false;""")
R("""    count.textContent=rows.length+' z '+D.cennik.pozycje.length;
    body.innerHTML=rows.map(function(c){
      var zm=c.cena_raw_p!=null&&c.cena_raw_p!==c.cena_p;
      var flagi='';""", """    count.textContent=rows.length+' z '+D.cennik.pozycje.length;
    var PR=D.klasy.presety[UST.preset]||D.klasy.presety[D.klasy.domyslny];
    body.innerHTML=rows.map(function(c){
      var zm=c.cena_raw_p!=null&&c.cena_raw_p!==c.cena_p;
      var m=(UST.mnozniki&&UST.mnozniki[c.klasa]!=null)?UST.mnozniki[c.klasa]:(PR.mnozniki[c.klasa]||1);
      var v4=D.zmiany_v5[c.id];
      var flagi='';
      if(c.nadpisane) flagi+=' <span class="pill warn">nadpisane</span>';""")
R("""        +'<td class="num'+(zm?' strike':'')+'">'+(c.cena_raw_p==null?'&mdash;':mon(c.cena_raw_p))+'</td>'
        +'<td class="num" style="font-weight:600">'+mon(c.cena_p)+'</td>'""",
"""        +'<td class="num" style="color:var(--ink-2)">'+(c.cena_raw_p==null?'&mdash;':mon(c.cena_raw_p))+'</td>'
        +'<td class="num" style="font-weight:600">'+mon(c.cena_p)+(c.cena_raw_p?'<div class="baza">'+proc(c.cena_p/c.cena_raw_p)+' wobec RAW</div>':'')+(v4!=null?'<div class="baza">v4: '+mon(v4)+'</div>':'')+'</td>'
        +'<td class="small" style="color:var(--ink-2)">'+esc(c.klasa||'')+' <span class="mono">×'+pl(m,2)+'</span><div class="baza">×1 = '+mon(c.cena_ref_p||c.cena_p)+'</div></td>'""")
R("""    }).join('')||'<tr><td colspan="6" style="color:var(--ink-3);padding:20px">Nic nie pasuje.</td></tr>';
  }
  chips(document.getElementById('cenyFlagi'),['zmienione wobec RAW','dopisane','bez źródła','nie w handlu'],stF,render,'Wszystko');""",
"""    }).join('')||'<tr><td colspan="7" style="color:var(--ink-3);padding:20px">Nic nie pasuje.</td></tr>';
  }
  chips(document.getElementById('cenyFlagi'),['zmienione w v5','nadpisane','zmienione wobec RAW','dopisane','bez źródła','nie w handlu'],stF,render,'Wszystko');
  ODSWIEZ.push(render);""")

# ---------------------------------------------------------------- kupiec
R("""  fill(selT,D.kupcy.kupcy,function(k){return k.id;},function(k){return k.nazwa;});
  fill(selL,D.osady.osady,function(o){return o.id;},function(o){return o.nazwa;},'miasteczko');
  fill(selK,D.koniunktura.koniunktury.filter(function(k){return Object.keys(k.kategorie||{}).length||k.id==='normalna';}),
       function(k){return k.id;},function(k){return k.nazwa;});
""", """  var inPS=document.getElementById('genPS');
  function wypelnij(){
    fill(selT,D.kupcy.kupcy,function(k){return k.id;},function(k){return k.nazwa+' (marża '+proc(k.marza)+')';},selT.value||null);
    fill(selL,D.osady.osady,function(o){return o.id;},etOsady,selL.value||'miasteczko');
    fill(selK,D.koniunktura.koniunktury,function(k){return k.id;},etKon,selK.value||'normalna');
  }
  wypelnij();
  function opisKaprysu(k){ var P=D.rynek.kaprys&&D.rynek.kaprys.progi; if(!P) return ''; var p=P.find(function(x){return Math.abs(x.mnoznik-k)<1e-9;}); return p?p.opis:''; }
""")
R("""    var sk=generujKupca(D,{kupiec:selT.value,osada:selL.value,koniunktura:selK.value,seed:seed});
    AKT={kupiec:selT.value,osada:selL.value,koniunktura:selK.value};
    var rows=sk.towar.map(function(t){
      var s=t.skladowe;
      return '<tr><td><strong>'+esc(t.nazwa)+'</strong><div class="small" style="color:var(--ink-3)">'+esc(t.kat)+'</div></td>'
        +'<td class="num">'+(t.sztuk?t.sztuk:'<span style="color:var(--ink-3)">0</span>')+'</td>'
        +'<td class="num" style="color:var(--ink-3)">'+mon(t.cena_wytworcy_p)+'</td>'
        +'<td class="num '+(t.mnoznik>1.08?'up':t.mnoznik<0.92?'down':'same')+'" style="font-weight:700">'+proc(t.mnoznik)+'</td>'
        +'<td class="num" style="font-weight:600">'+mon(t.cena_p)+'</td>'
        +'<td class="num" style="color:var(--ink-2)">'+mon(t.skup_p)+'</td>'
        +'<td class="small" style="color:var(--ink-2)">'+esc(t.zapas_nazwa)+' · '+esc(t.popyt_nazwa)
          +'<div class="small" style="color:var(--ink-3)">marża '+proc(s.marza)+' · osada '+proc(s.osada)
          +(s.koniunktura!==1?' · koniunktura '+proc(s.koniunktura):'')+' · rynek '+proc(s.rynek)+'</div></td></tr>';
    }).join('');""", """    var sk=generujKupca(D,{kupiec:selT.value,osada:selL.value,koniunktura:selK.value,seed:seed});
    AKT={kupiec:selT.value,osada:selL.value,koniunktura:selK.value};
    var ps=Math.max(0,parseInt(inPS.value,10)||0);
    document.getElementById('genMods').innerHTML='<strong>'+esc(sk.etykiety.osada)+'</strong> &middot; '+esc(sk.etykiety.koniunktura);
    var rows=sk.towar.map(function(t){
      var s=t.skladowe, tg=ps?targuj(D,{cena_p:t.cena_p,cena_cennik_p:t.cena_wytworcy_p,cena_min_p:t.cena_min_p,ps:ps}):null;
      var modT=modyfikatorTargowania(t);
      var pref=s.preferencja===1?'':' · '+(s.preferencja<1?'rdzeń ':'boczny ')+proc(s.preferencja);
      var kap=s.kaprys===1?'':' · kaprys '+proc(s.kaprys)+' („'+esc(opisKaprysu(s.kaprys))+'”)';
      return '<tr><td><strong>'+esc(t.nazwa)+'</strong><div class="small" style="color:var(--ink-3)">'+esc(t.kat)+'</div></td>'
        +'<td class="num">'+(t.sztuk?t.sztuk:'<span style="color:var(--ink-3)">0</span>')+'</td>'
        +'<td class="num" style="color:var(--ink-3)">'+(t.cena_raw_p==null?'&mdash;':mon(t.cena_raw_p))+'</td>'
        +'<td class="num" style="color:var(--ink-2)">'+mon(t.cena_wytworcy_p)+'</td>'
        +'<td class="num" style="font-weight:600">'+mon(t.cena_p)+'<div class="small '+(t.mnoznik>1.08?'up':t.mnoznik<0.92?'down':'same')+'">'+proc(t.mnoznik)+'</div></td>'
        +'<td class="num minp">'+mon(t.cena_min_p)+(t.wyprzedaz?'<div class="small down">wyprzedaż</div>':'')+'</td>'
        +(ps?'<td class="num targ">'+mon(tg.cena_p)+(tg.upust>0?'<div class="small">−'+Math.round(tg.upust*100)+'%</div>':'<div class="small" style="color:var(--ink-3)">nie zejdzie</div>')+'</td>':'')
        +'<td class="num" style="color:var(--ink-2)">'+mon(t.skup_p)+(t.skup_ponad_gotowke?'<div class="small up">brak gotówki</div>':'')+'</td>'
        +'<td class="small" style="color:var(--ink-2)">'+esc(t.zapas_nazwa)+' · '+esc(t.popyt_nazwa)
          +(modT?' · <strong>test '+(modT>0?'+':'')+modT+'</strong>':'')
          +'<div class="small" style="color:var(--ink-3)">marża '+proc(s.marza)+pref+kap+' · osada '+proc(s.osada)
          +(s.koniunktura!==1?' · koniunktura '+proc(s.koniunktura):'')+' · rynek '+proc(s.rynek)
          +' · koszt '+mon(t.koszt_p)+'</div></td></tr>';
    }).join('');""")
R("""        +'<span class="tag '+(sk.osada.mnoznik>1?'t-gora':'t-dol')+'">osada '+proc(sk.osada.mnoznik)+'</span>'
        +'<span class="tag '+(sk.koniunktura.id==='normalna'?'t-ok':'t-zmiana')+'">'+esc(sk.koniunktura.nazwa)+'</span>'""",
"""        +'<span class="tag '+(sk.osada.mnoznik>1?'t-gora':'t-dol')+'">'+esc(sk.etykiety.osada)+'</span>'
        +(sk.gotowka_p!=null?'<span class="tag t-ok">gotówka '+mon(sk.gotowka_p)+'</span>':'')
        +(sk.budzet_towaru_p!=null?'<span class="tag t-nowe">towar '+mon(sk.wartosc_towaru_p)+'</span>':'')
        +'<span class="tag '+(sk.koniunktura.id==='normalna'?'t-ok':'t-zmiana')+'">'+esc(sk.koniunktura.nazwa)+'</span>'""")
R("""      +'<thead><tr><th>Towar</th><th>Sztuk</th><th>Cena wytwórcy</th><th>Mod.</th><th>Jego cena</th><th>Odkupi za</th><th>Dlaczego tyle</th></tr></thead>'""",
"""      +'<thead><tr><th>Towar</th><th>Sztuk</th><th>Podręcznik</th><th>Cena bazowa</th><th>Jego cena</th><th>Minimalna</th>'+(ps?'<th>Po targu ('+ps+' PS)</th>':'')+'<th>Odkupi za</th><th>Dlaczego tyle</th></tr></thead>'""")
R("""  inS.addEventListener('change',function(){ var v=parseInt(inS.value,10); render(isNaN(v)?(Math.random()*1e9)|0:v); });
  var z=czytajURL();
  render(z==null?20261023:z);""", """  inS.addEventListener('change',function(){ var v=parseInt(inS.value,10); render(isNaN(v)?(Math.random()*1e9)|0:v); });
  inPS.addEventListener('input',function(){ render(+inS.value); });
  var z=czytajURL();
  render(z==null?20261024:z);
  ODSWIEZ.push(function(){ wypelnij(); render(+inS.value); });""")

# zamówienie: nazewnictwo
R("""      +'<tr><td>Cena wytwórcy</td><td class="num">'+mon(r.przedmiot.cena_p)+'</td></tr>'""",
"""      +'<tr><td style="color:var(--ink-3)">Podręcznik (RAW), do porównania</td><td class="num" style="color:var(--ink-3)">'+(r.przedmiot.cena_raw_p==null?'&mdash;':mon(r.przedmiot.cena_raw_p))+'</td></tr>'
      +'<tr><td>Cena bazowa</td><td class="num">'+mon(r.przedmiot.cena_p)+'</td></tr>'""")
R("""      +'<tr><td>Osada</td><td class="num">'+proc(s.osada)+'</td></tr>'
      +'<tr><td>Koniunktura</td><td class="num">'+proc(s.koniunktura)+'</td></tr>'""",
"""      +'<tr><td>'+esc(etOsady(D.osady.osady.find(function(o){return o.id===AKT.osada;})))+'</td><td class="num">'+proc(s.osada)+'</td></tr>'
      +'<tr><td>'+esc(D.koniunktura.koniunktury.find(function(k){return k.id===AKT.koniunktura;}).nazwa)+' ('+esc(r.przedmiot.kat)+')</td><td class="num">'+proc(s.koniunktura)+'</td></tr>'""")

# czynsze: etykiety + odświeżanie
R("""  fill(selL,D.osady.osady,function(o){return o.id;},function(o){return o.nazwa;},'miasteczko');
  fill(selK,D.koniunktura.koniunktury,function(k){return k.id;},function(k){return k.nazwa;});
  function render(){""", """  function wypelnij(){
    fill(selL,D.osady.osady,function(o){return o.id;},etOsady,selL.value||'miasteczko');
    fill(selK,D.koniunktura.koniunktury,function(k){return k.id;},function(k){var m=k.czynsz?k.czynsz.mnoznik:1;return k.nazwa+' (czynsz '+(m===1?'bez zmian':proc(m))+')';},selK.value||'normalna');
  }
  wypelnij();
  function render(){""")
R("""  [selL,selK].forEach(function(s){s.addEventListener('change',render);});
  render();
})();

/* ---------------- modyfikatory ---------------- */
(function(){
  document.getElementById('kupcyDoc')""", """  [selL,selK].forEach(function(s){s.addEventListener('change',render);});
  render();
  ODSWIEZ.push(function(){ wypelnij(); render(); });
})();

/* ---------------- modyfikatory ---------------- */
(function(){
function render(){
  var R_=D.rynek, osob='';
  if(R_.preferencje) osob+='<div class="kv"><span>Rdzeń asortymentu</span><b>'+proc(R_.preferencje.rdzen)+'</b></div>'
    +'<div class="kv"><span>Boczny asortyment</span><b>'+proc(R_.preferencje.boczne)+'</b></div>';
  if(R_.kaprys) osob+=R_.kaprys.progi.map(function(p,i,a){var od=i?a[i-1].do+1:1;return '<div class="kv"><span>kaprys '+(od===p.do?p.do:od+'–'+p.do)+': '+esc(p.opis)+'</span><b>'+proc(p.mnoznik)+'</b></div>';}).join('')
    +'<div class="kv"><span>Granice preferencja × kaprys</span><b>'+proc(R_.kaprys.granice[0])+' … '+proc(R_.kaprys.granice[1])+'</b></div>';
  if(R_.cena_minimalna) osob+='<div class="kv"><span>Cena minimalna: narzut na koszt</span><b>'+proc(R_.cena_minimalna.narzut_min)+'</b></div>'
    +'<div class="kv"><span>Przy wyprzedaży (rynek &lt; 1)</span><b>'+proc(R_.cena_minimalna.wyprzedaz)+'</b></div>'
    +'<div class="kv"><span>Koszt własny wytwórcy</span><b>'+proc(R_.cena_minimalna.koszt_wlasny)+'</b></div>';
  document.getElementById('osobDoc').innerHTML=osob;
  document.getElementById('kupcyDoc')""")
R("""      return '<td class="num '+(v>1?'up':v<1?'down':'same')+'">'+proc(v)+'</td>'; }).join('')+'</tr>';
  }).join('');""", """      return '<td class="num '+(v>1?'up':v<1?'down':'same')+'">'+proc(v)+'</td>'; }).join('')+'</tr>';
  }).join('');
}
render(); ODSWIEZ.push(render);
function render2(){""")
R("""    return '<div class="kv"><span>'+esc(p.kto||p.nazwa||'')+'</span><b>'+esc((p.pozycja||'')+' / '+(p.dochod||''))+'</b></div>';
  }).join('');
})();""", """    return '<div class="kv"><span>'+esc(p.kto||p.nazwa||'')+'</span><b>'+esc((p.pozycja||'')+' / '+(p.dochod||''))+'</b></div>';
  }).join('');
}
render2(); ODSWIEZ.push(render2);
})();""")
R("""  var cel=null;""" if False else """/* ---------------- historia ---------------- */""", """/* ---------------- ustawienia MG ---------------- */
(function(){
  var K=D_BAZA.klasy;
  var selP=document.getElementById('ustPreset'), inPrem=document.getElementById('ustPremia'), msg=document.getElementById('ustMsg');
  fill(selP,Object.keys(K.presety),function(n){return n;},function(n){return n+(n===K.domyslny?' (domyślny)':'')+' — '+(K.presety[n].opis||'').slice(0,70)+'…';},UST.preset);
  function parsujCene(s){
    s=String(s).trim().toLowerCase().replace(',','.'); if(!s) return null;
    if(/^\\d+(\\.\\d+)?$/.test(s)) return Math.round(+s);
    var p=0, ok=false, re=/(\\d+(?:\\.\\d+)?)\\s*(zk|s|p)\\b/g, m;
    while((m=re.exec(s))){ ok=true; p+=+m[1]*({zk:240,s:12,p:1})[m[2]]; }
    return ok?Math.round(p):NaN;
  }
  function liczba(v){ var x=parseFloat(String(v).replace(',','.')); return isFinite(x)&&x>0?x:null; }
  function pole(id,val,step){ return '<input class="numin" data-k="'+esc(id)+'" type="number" step="'+(step||0.05)+'" min="0" value="'+val+'">'; }
  function zrTag(z){ var c=/brak/.test(z)?'zr-brak':/sprzecz/.test(z)?'zr-sprzeczne':/zasada/.test(z)?'zr-zasada':'zr-dane'; return '<span class="pill '+c+'">'+esc(z)+'</span>'; }
  function render(){
    var PR=K.presety[UST.preset]||K.presety[K.domyslny];
    selP.value=UST.preset;
    inPrem.value=UST.premia_znak_stanu!=null?UST.premia_znak_stanu:PR.premia_znak_stanu;
    var ile={}; D.cennik.pozycje.forEach(function(c){ile[c.klasa]=(ile[c.klasa]||0)+1;});
    document.getElementById('ustKlasy').innerHTML=Object.keys(PR.mnozniki).filter(function(k){return ile[k];}).map(function(k){
      var u=K.uzasadnienia&&K.uzasadnienia[k], v=UST.mnozniki[k]!=null?UST.mnozniki[k]:PR.mnozniki[k];
      return '<tr><td><strong>'+esc(k)+'</strong>'+(UST.mnozniki[k]!=null?' <span class="pill warn">zmienione</span>':'')
        +(u?'<div class="small" style="color:var(--ink-3)">'+esc(u.tekst)+'</div>':'')+'</td><td class="num">'+ile[k]+'</td>'
        +'<td class="num">'+pole('klasa:'+k,v)+'</td><td>'+(u?zrTag(u.zrodlo):'')+'</td></tr>';
    }).join('');
    document.getElementById('ustOsady').innerHTML=D.osady.osady.map(function(o){
      return '<tr><td>'+esc(o.nazwa)+'</td><td class="num">'+pole('osada:'+o.id,o.mnoznik)+'</td></tr>'; }).join('');
    document.getElementById('ustKupcy').innerHTML=D.kupcy.kupcy.map(function(k){
      return '<tr><td>'+esc(k.nazwa)+'</td><td class="num">'+pole('marza:'+k.id,k.marza)+'</td><td class="num">'+pole('skup:'+k.id,k.skup)+'</td></tr>'; }).join('');
    var RY=D.rynek;
    document.getElementById('ustRynek').innerHTML=[
      ['Rdzeń asortymentu','rynek:preferencje:rdzen',RY.preferencje.rdzen],['Boczny asortyment','rynek:preferencje:boczne',RY.preferencje.boczne],
      ['Kaprys: dolna granica','rynek:kaprys:granice:0',RY.kaprys.granice[0]],['Kaprys: górna granica','rynek:kaprys:granice:1',RY.kaprys.granice[1]],
      ['Cena minimalna: narzut','rynek:cena_minimalna:narzut_min',RY.cena_minimalna.narzut_min],['Przy wyprzedaży','rynek:cena_minimalna:wyprzedaz',RY.cena_minimalna.wyprzedaz],
      ['Koszt własny wytwórcy','rynek:cena_minimalna:koszt_wlasny',RY.cena_minimalna.koszt_wlasny]
    ].map(function(r){ return '<tr><td>'+r[0]+'</td><td class="num">'+pole(r[1],r[2])+'</td></tr>'; }).join('');
    var selK=document.getElementById('ustKon');
    fill(selK,D.koniunktura.koniunktury,function(k){return k.id;},etKon,selK.value||'wojna');
    var kon=D.koniunktura.koniunktury.find(function(k){return k.id===selK.value;});
    document.getElementById('ustKonKat').innerHTML=D.koniunktura.kategorie.map(function(kat){
      return '<tr><td>'+esc(kat)+'</td><td class="num">'+pole('kon:'+kon.id+':'+kat,cenaKoniunktury(kon,kat))+'</td></tr>'; }).join('')
      +'<tr><td><strong>Czynsz</strong></td><td class="num">'+pole('konczynsz:'+kon.id,kon.czynsz?kon.czynsz.mnoznik:1)+'</td></tr>';
    document.getElementById('ustPozLista').innerHTML=D_BAZA.cennik.pozycje.map(function(c){return '<option value="'+esc(c.nazwa)+'"></option>';}).join('');
    var nad=Object.keys(UST.pozycje);
    document.getElementById('ustPozLista2').innerHTML=nad.length?nad.map(function(id){
      var b=D_BAZA.cennik.pozycje.find(function(c){return c.id===id;});
      return '<div class="kv"><span>'+esc(b?b.nazwa:id)+'</span><b>'+mon(poId[id]?poId[id].cena_p:0)+' <button class="btn2" data-usun="'+esc(id)+'" type="button" style="padding:2px 8px">×</button></b></div>'; }).join('')
      :'<p class="small muted">Brak nadpisanych pozycji.</p>';
    var r=roznicaCen(D_BAZA,D);
    document.getElementById('ustRoznice').innerHTML=r.length?('<p>'+r.length+' pozycji ma inną cenę niż cennik v5.</p>'
      +'<div class="tablewrap" style="margin-top:6px;max-height:320px;overflow:auto"><table><thead><tr><th>Pozycja</th><th>Cennik v5</th><th>Teraz</th><th>Zmiana</th></tr></thead><tbody>'
      +r.slice(0,400).map(function(x){return '<tr><td>'+esc(x.nazwa)+'</td><td class="num">'+mon(x.przed_p)+'</td><td class="num" style="font-weight:600">'+mon(x.po_p)+'</td><td class="num '+(x.po_p>x.przed_p?'up':'down')+'">'+proc(x.po_p/x.przed_p)+'</td></tr>';}).join('')
      +'</tbody></table></div>'):'<p class="muted">Bez zmian &mdash; obowiązuje cennik v5.</p>';
    document.getElementById('ustJson').value=JSON.stringify(UST,null,1);
  }
  function ustaw(k,v){
    var p=k.split(':'), x=liczba(v); if(x==null) return;
    if(p[0]==='klasa') UST.mnozniki[p[1]]=x;
    else if(p[0]==='osada') (UST.osady[p[1]]=UST.osady[p[1]]||{}).mnoznik=x;
    else if(p[0]==='marza') (UST.kupcy[p[1]]=UST.kupcy[p[1]]||{}).marza=x;
    else if(p[0]==='skup') (UST.kupcy[p[1]]=UST.kupcy[p[1]]||{}).skup=x;
    else if(p[0]==='kon'){ var o=UST.koniunktury[p[1]]=UST.koniunktury[p[1]]||{}; o.kategorie=o.kategorie||{}; o.kategorie[p.slice(2).join(':')]={cena:x}; }
    else if(p[0]==='konczynsz') (UST.koniunktury[p[1]]=UST.koniunktury[p[1]]||{}).czynsz=x;
    else if(p[0]==='rynek'){
      var sek=UST.rynek[p[1]]=UST.rynek[p[1]]||{};
      if(p[2]==='granice'){ var g=(sek.granice||D.rynek.kaprys.granice).slice(); g[+p[3]]=x; sek.granice=g; } else sek[p[2]]=x;
    }
    odswiez();
  }
  document.getElementById('ustawienia').addEventListener('change',function(e){
    var el=e.target;
    if(el.dataset&&el.dataset.k){ ustaw(el.dataset.k,el.value); return; }
    if(el.id==='ustKon'){ render(); }
  });
  selP.addEventListener('change',function(){ UST.preset=selP.value; UST.mnozniki={}; odswiez(); msg.textContent='Preset: '+selP.value+'. Własne mnożniki klas wyczyszczone.'; });
  inPrem.addEventListener('change',function(){ var x=liczba(inPrem.value); UST.premia_znak_stanu=x; odswiez(); });
  document.getElementById('ustPozBtn').addEventListener('click',function(){
    var n=document.getElementById('ustPozNazwa').value, c=document.getElementById('ustPozCena').value;
    var poz=D_BAZA.cennik.pozycje.find(function(x){return norm(x.nazwa)===norm(n.trim());})||znajdzPozycje(D_BAZA,n);
    if(!poz){ msg.innerHTML='<span class="errline">Nie znam pozycji „'+esc(n)+'”.</span>'; return; }
    var p=parsujCene(c);
    if(p===null){ delete UST.pozycje[poz.id]; msg.textContent='Usunięto nadpisanie: '+poz.nazwa+'.'; }
    else if(!(p>0)){ msg.innerHTML='<span class="errline">Nie rozumiem ceny „'+esc(c)+'”.</span>'; return; }
    else { UST.pozycje[poz.id]={cena_p:p}; msg.textContent=poz.nazwa+': '+mon(p)+'.'; }
    odswiez();
  });
  document.getElementById('ustPozLista2').addEventListener('click',function(e){ var b=e.target.closest('[data-usun]'); if(!b) return; delete UST.pozycje[b.dataset.usun]; odswiez(); });
  document.getElementById('ustJsonBtn').addEventListener('click',function(){
    try{ var j=JSON.parse(document.getElementById('ustJson').value); zastosujUstawienia(D_BAZA,j); UST=Object.assign(ustPuste(),j); odswiez(); msg.innerHTML='<span class="okline">Zastosowano.</span>'; }
    catch(e){ msg.innerHTML='<span class="errline">Błąd: '+esc(e.message)+'</span>'; }
  });
  document.getElementById('ustEksport').addEventListener('click',function(){
    var out=Object.assign({opis:'Ustawienia MG wyeksportowane ze Skarbca '+new Date().toISOString().slice(0,10)+'. Format: data/ustawienia.json.'},UST);
    var tekst=JSON.stringify(out,null,1);
    function lokalnie(){ var a=document.createElement('a'); a.href=URL.createObjectURL(new Blob([tekst],{type:'application/json'}));
      a.download='ustawienia.json'; document.body.appendChild(a); a.click(); a.remove(); }
    // Na claude.ai plik oddaje przeglądarka przez capability „downloads”; otwarta lokalnie strona — zwykłym linkiem.
    if(window.claude&&window.claude.use){
      window.claude.use('downloads').then(function(dl){
        if(!dl){ msg.textContent='Zapis pliku niedostępny w tym widoku — skopiuj JSON z pola powyżej.'; return; }
        return dl.save({filename:'ustawienia.json',data:tekst}).then(function(){ msg.innerHTML='<span class="okline">Zapisano ustawienia.json.</span>'; })
          .catch(function(e){ msg.textContent=e&&e.code==='declined'?'Zapis anulowany.':'Nie udało się zapisać — skopiuj JSON z pola powyżej.'; });
      });
    } else lokalnie();
  });
  document.getElementById('ustImport').addEventListener('change',function(e){
    var f=e.target.files[0]; if(!f) return; var r=new FileReader();
    r.onload=function(){ try{ var j=JSON.parse(r.result); zastosujUstawienia(D_BAZA,j); delete j.przyklad; UST=Object.assign(ustPuste(),j); odswiez(); msg.innerHTML='<span class="okline">Wczytano '+esc(f.name)+'.</span>'; }
      catch(err){ msg.innerHTML='<span class="errline">Błąd pliku: '+esc(err.message)+'</span>'; } };
    r.readAsText(f); e.target.value='';
  });
  document.getElementById('ustReset').addEventListener('click',function(){ UST=ustPuste(); odswiez(); msg.textContent='Przywrócono cennik v5.'; });
  document.getElementById('ustSpoj').addEventListener('click',function(){
    var w=sprawdzWszystko(D.cennik,{reguly:D.spojnosc.reguly,testy:D.spojnosc_v4,czynsze:D.czynsze});
    var bl=w.filter(function(x){return !x.ostrzezenie;}).reduce(function(s,x){return s+x.bledy.length;},0);
    document.getElementById('ustSpojWynik').innerHTML='<div class="callout">'+w.map(function(x){
      return '<p class="'+(x.bledy.length?(x.ostrzezenie?'':'errline'):'okline')+'"><strong>'+(x.bledy.length?(x.ostrzezenie?'uwaga':'BŁĄD'):'OK')+'</strong> &middot; '+esc(x.nazwa)
        +(x.bledy.length?'<br><span class="small">'+x.bledy.map(esc).join('<br>')+'</span>':'')+'</p>';
    }).join('')+'<p><strong>'+(bl?bl+' błędów — cennik pozwala na arbitraż albo łamie zasadę.':'Cennik spójny.')+'</strong></p></div>';
  });
  render(); ODSWIEZ.push(render);
  document.getElementById('ustBadge').hidden=JSON.stringify(UST)===JSON.stringify(ustPuste());
})();

/* ---------------- historia ---------------- */""")

open(H + 'szablon.html', 'w', encoding='utf-8').write(t)
print('szablon.html', len(t) // 1024, 'KB')
