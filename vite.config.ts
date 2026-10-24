import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";
import { VitePWA } from "vite-plugin-pwa";

// Repozytorium projektowe (Raksoprojects/Cennik_Warhammer_4ed) -> GitHub Pages serwuje
// aplikację pod /Cennik_Warhammer_4ed/, więc base musi zawierać tę ścieżkę.
export default defineConfig({
  base: "/Cennik_Warhammer_4ed/",
  plugins: [
    svelte(),
    VitePWA({
      registerType: "autoUpdate",
      injectRegister: false,
      includeAssets: ["favicon.svg", "icon-192.png", "icon-512.png"],
      manifest: {
        name: "Skarbiec Imperium — cennik i kupcy WFRP 4ed",
        short_name: "Skarbiec",
        description: "Cennik, generator kupców, zarobki i czynsze dla kampanii Warhammer Fantasy Roleplay 4ed",
        theme_color: "#14161b",
        background_color: "#14161b",
        display: "standalone",
        lang: "pl",
        icons: [
          { src: "icon-192.png", sizes: "192x192", type: "image/png" },
          { src: "icon-512.png", sizes: "512x512", type: "image/png" },
          { src: "icon-512.png", sizes: "512x512", type: "image/png", purpose: "maskable" }
        ]
      },
      workbox: { globPatterns: ["**/*.{js,css,html,svg,png}"], maximumFileSizeToCacheInBytes: 4 * 1024 * 1024 }
    })
  ],
  build: { target: "es2020", sourcemap: false }
});
