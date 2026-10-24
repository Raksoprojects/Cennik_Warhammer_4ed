import * as S from '../src/silnik.js';
import { readFileSync } from 'node:fs';
const B=new URL('../',import.meta.url).pathname;
const j = n => JSON.parse(readFileSync(B+n,'utf8'));
const d = { cennik:j('data/cennik.json'), kupcy:j('data/kupcy.json'), osady:j('data/osady.json'),
  koniunktura:j('data/koniunktura.json'), rynek:j('data/rynek.json'), nazwy:j('data/nazwy.json'),
  statusy:j('data/statusy.json'), przedmioty_magiczne:j('data/przedmioty_magiczne.json'),
  czynsze:j('data/czynsze.json') };

console.log('1) Usługi i nocleg znikły z asortymentu?');
let zle=0;
for (const k of d.kupcy.kupcy) for (const o of ['wies','miasteczko','miasto','altdorf'])
  for (let s=1;s<=15;s++){
    const sk=S.generujKupca(d,{kupiec:k.id,osada:o,koniunktura:'normalna',seed:s});
    for (const t of sk.towar) if (['usluga','nocleg','nieruchomosc'].includes(d.cennik.pozycje.find(p=>p.id===t.id).typ)) zle++;
  }
console.log('   niedozwolonych pozycji w 900 sklepach:', zle);

console.log('\n2) Wieś: czy da się kupić zwierzęta mimo limitu 2 ZK?');
const wies=S.generujKupca(d,{kupiec:'kramarz',osada:'wies',koniunktura:'normalna',seed:3});
const zw=wies.towar.filter(t=>/krowa|wol|swinia|owca|kurczak|kon-pociagowy|ges|kaplon|ciele/.test(t.id));
console.log('   kramarz we wsi, zwierzęta:', zw.length?zw.map(t=>`${t.nazwa} ${S.mon(t.cena_p)}`).join(', '):'(brak w tym losowaniu)');
const kon=S.generujKupca(d,{kupiec:'konie',osada:'wies',koniunktura:'normalna',seed:3});
console.log('   handlarz koni we wsi:', kon.towar.map(t=>`${t.nazwa} ${S.mon(t.cena_p)}`).join(' · ') || '(pusto)');

console.log('\n3) Czynsz z koniunkturą — Marienburg');
for (const kk of ['normalna','zaraza','oblezenie','kryzys_mieszkaniowy']) {
  const c=S.czynsz(d,{kwatera:'Mieszkanie mieszczańskie (2–3 izby)',okres:'miesiac',osada:'marienburg',koniunktura:kk});
  console.log(`   ${kk.padEnd(22)} ${S.mon(c.cena_p)}  (baza ${S.mon(c.baza_p)} × osada ${c.skladowe.osada} × koniunktura ${c.skladowe.koniunktura})`);
}

console.log('\n4) Sprzedaż nowych towarów — kramarz w Altdorfie');
const kr=S.generujKupca(d,{kupiec:'kramarz',osada:'altdorf',koniunktura:'normalna',seed:21});
console.log('   pozycji:', kr.towar.length, '| próbka:', kr.towar.slice(0,6).map(t=>`${t.nazwa} ${S.mon(t.cena_p)}`).join(' · '));
