// Wszystkie dane w jednym obiekcie. Vite wkompilowuje JSON w bundle — bez fetch, bez stanu ładowania.
import cennik from '../../data/cennik.json';
import kupcy from '../../data/kupcy.json';
import osady from '../../data/osady.json';
import koniunktura from '../../data/koniunktura.json';
import rynek from '../../data/rynek.json';
import nazwy from '../../data/nazwy.json';
import statusy from '../../data/statusy.json';
import czynsze from '../../data/czynsze.json';
import audyt from '../../data/audyt.json';
import historia from '../../data/historia.json';
import pozycja_dochod from '../../data/pozycja_dochod.json';
import przedmioty_magiczne from '../../data/przedmioty_magiczne.json';
import kalkulator from '../../data/kalkulator.json';
import klasy from '../../data/klasy_cenowe.json';
import ustawienia from '../../data/ustawienia.json';
import spojnosc from '../../data/spojnosc.json';
import spojnosc_v4 from '../../data/spojnosc_v4.json';
import bron_cechy from '../../data/bron_cechy.json';
import postacie from '../../data/postacie.json';
import handel from '../../data/handel.json';
import kalendarz from '../../data/kalendarz.json';

// Dane BAZOWE — nigdy ich nie mutuj. Widoki dostają dane po ustawieniach MG (stan.d).
// Typ luźny celowo: kształt danych opisuje docs/archiwum/APLIKACJA.md § 4, a silnik jest w JS.
export type Dane = any;
export const daneBazowe: Dane = Object.freeze({
  cennik, kupcy, osady, koniunktura, rynek, nazwy, statusy, czynsze, audyt, historia,
  pozycja_dochod, przedmioty_magiczne, kalkulator, klasy, spojnosc, spojnosc_v4, bron_cechy, postacie, handel, kalendarz,
});
export const ustawieniaDomyslne: any = ustawienia;
