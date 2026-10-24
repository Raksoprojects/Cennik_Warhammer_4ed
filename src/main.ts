import { mount } from 'svelte';
import { registerSW } from 'virtual:pwa-register';
import './styl.css';
import App from './App.svelte';

// Service worker (autoUpdate): po wdrożeniu nowej wersji strona przeładowuje się sama.
registerSW({ immediate: true });

export default mount(App, { target: document.getElementById('app')! });
