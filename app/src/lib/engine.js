/**
 * Engine-lader: haalt de WASM-build van de regelrecht-engine uit
 * public/wasm/pkg en laadt de LVV erin (untranslatables tijdelijk op
 * accepted zodat verkennend draaien mogelijk is — de UI toont ze als
 * menselijke-toets-voorwaarden per route).
 * Zelfde fetch+blob-aanpak als de regelrecht-editor (useEngine.js).
 */
let instance = null;
let initPromise = null;

export function laadEngine() {
  if (initPromise) return initPromise;
  initPromise = (async () => {
    const base = import.meta.env.BASE_URL;
    const jsText = await (await fetch(`${base}wasm/pkg/regelrecht_engine.js`)).text();
    const blob = new Blob([jsText], { type: 'application/javascript' });
    const blobUrl = URL.createObjectURL(blob);
    const wasm = await import(/* @vite-ignore */ blobUrl);
    URL.revokeObjectURL(blobUrl);
    await wasm.default(`${base}wasm/pkg/regelrecht_engine_bg.wasm`);
    const engine = new wasm.WasmEngine();
    const yaml = await (await fetch(`${base}lvv.yaml`)).text();
    // Verkenningsmodus: onbeoordeelde untranslatables blokkeren executie
    // (RFC-012); voor het filter zetten we ze op accepted en tonen we ze
    // expliciet als voorwaarden die menselijke beoordeling vergen.
    const lawId = engine.loadLaw(yaml.replaceAll('accepted: false', 'accepted: true'));
    instance = { engine, lawId };
    return instance;
  })();
  return initPromise;
}
