<script lang="ts">
  // Osobowość kupca (data/postacie.json): charakter, wygląd, znak rozpoznawczy, manieryzm, Motywacja, cecha kupiecka,
  // potrzeba, sekret. Sekret i efekty cechy są dla MG.
  import Podpowiedz from './Podpowiedz.svelte';
  let { postac, onPrzelosuj }: { postac: any; onPrzelosuj?: () => void } = $props();
  const KOLOR: Record<string, string> = { dobry: 'zielony', neutralny: 'niebieski', zly: 'czerwony' };
  const NAZWA: Record<string, string> = { dobry: 'dobry', neutralny: 'neutralny', zly: 'zły' };
  const efekt = (e: any) => [
    e.ceny && `ceny ×${String(e.ceny).replace('.', ',')}`, e.skup && `skup ×${String(e.skup).replace('.', ',')}`,
    e.targowanie && `Targowanie ${e.targowanie > 0 ? '+' : ''}${e.targowanie}`, e.bez_targu && 'nie targuje się',
    e.trefne === 0 && 'nigdy nie oszukuje', e.trefne > 0 && `trefne ≥ ${Math.round(e.trefne * 100)}%`, e.gotowka && `gotówka ×${e.gotowka}`,
    e.termin && `zamówienia ×${String(e.termin).replace('.', ',')} czasu`].filter(Boolean).join(', ');
</script>

{#if postac}
  <div class="postac">
    <div><span class="znacznik {KOLOR[postac.charakter]}">{NAZWA[postac.charakter]}</span>
      <b>{postac.motywacja.nazwa}</b> <Podpowiedz tekst={'Motywacja: ' + postac.motywacja.opis} />
      · <b>{postac.cecha.nazwa}</b> <Podpowiedz tekst={postac.cecha.opis + (efekt(postac.cecha.efekt) ? ` Efekt: ${efekt(postac.cecha.efekt)}.` : '')} />
      {#if onPrzelosuj}<button class="maly nie-drukuj" onclick={onPrzelosuj}>Przelosuj osobowość</button>{/if}</div>
    <div class="male"><span class="szary">Wygląd:</span> {postac.wyglad.join(', ')}. <span class="szary">Znak:</span> {postac.znak}</div>
    <div class="male"><span class="szary">Mówi:</span> {postac.manieryzm}</div>
    <div class="male"><span class="szary">Potrzeba:</span> {postac.potrzeba} <span class="szary nie-drukuj">Sekret (MG):</span> <span class="nie-drukuj">{postac.sekret}</span></div>
  </div>
{/if}

<style>
  .postac { display: flex; flex-direction: column; gap: 4px; margin: 8px 0; padding: 8px 10px; border-left: 3px solid var(--linia-mocna); }
</style>
