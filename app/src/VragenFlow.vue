<template>
  <div>
    <p class="intro">
      Beantwoord vragen over het steun-idee; elke vraag verdeelt de
      {{ totaal }} routes opnieuw over drie emmers. <em>Weet niet</em> laten
      staan mag altijd — dan blijft de route in "mogelijk, mits".
    </p>

    <nldd-banner v-if="fout" variant="error">{{ fout }}</nldd-banner>
    <p v-else-if="!klaar">Engine en corpus laden…</p>

    <template v-else>
      <div class="kolommen">
        <section class="vragen">
          <nldd-title level="3">Vragen</nldd-title>
          <div v-for="v in vragen" :key="v.param" class="vraag">
            <p class="vraag-tekst">
              {{ v.beschrijving || v.param }}
              <span class="vraag-meta">raakt {{ v.raaktRoutes }} routes · art. {{ v.artikelen.join(', ') }}</span>
            </p>
            <div v-if="v.type === 'boolean'" class="antwoord">
              <nldd-toggle-button-group>
                <nldd-toggle-button :pressed="antwoorden[v.param] === true" @click="zet(v.param, true)">ja</nldd-toggle-button>
                <nldd-toggle-button :pressed="antwoorden[v.param] === false" @click="zet(v.param, false)">nee</nldd-toggle-button>
                <nldd-toggle-button :pressed="!(v.param in antwoorden)" @click="wis(v.param)">weet niet</nldd-toggle-button>
              </nldd-toggle-button-group>
            </div>
            <div v-else-if="v.opties.length" class="antwoord">
              <nldd-toggle-button-group>
                <nldd-toggle-button
                  v-for="o in v.opties" :key="o"
                  :pressed="antwoorden[v.param] === o"
                  @click="antwoorden[v.param] === o ? wis(v.param) : zet(v.param, o)"
                >{{ o.toLowerCase().replaceAll('_', ' ') }}</nldd-toggle-button>
              </nldd-toggle-button-group>
            </div>
            <div v-else class="antwoord">
              <nldd-number-field
                :label="v.type === 'amount' ? 'bedrag in EUR' : 'waarde'"
                :value="ruweInvoer[v.param] ?? ''"
                @input="zetNumeriek(v, $event.target.value)"
              ></nldd-number-field>
            </div>
          </div>
          <nldd-button v-if="beantwoord" variant="secondary" @click="reset">Begin opnieuw</nldd-button>
        </section>

        <section class="emmers">
          <div class="emmer">
            <nldd-title level="3">Voldoet al ({{ oordeel.voldoet.length }})</nldd-title>
            <p class="emmer-uitleg">Met de gegeven antwoorden zijn alle machinaal toetsbare voorwaarden vervuld.</p>
            <RouteChip v-for="x in oordeel.voldoet" :key="x.route.artikel" :item="x" @uitleg="toonUitleg" />
          </div>
          <div class="emmer">
            <nldd-title level="3">Mogelijk, mits … ({{ oordeel.mogelijk.length }})</nldd-title>
            <p class="emmer-uitleg">Nog open; sommige met onvolledige analyse (gemarkeerd).</p>
            <RouteChip v-for="x in oordeel.mogelijk" :key="x.route.artikel" :item="x" @uitleg="toonUitleg" />
          </div>
          <div class="emmer">
            <nldd-title level="3">Uitgesloten ({{ oordeel.uitgesloten.length }})</nldd-title>
            <p class="emmer-uitleg">Geen enkele invulling van de open vragen maakt deze route nog toelaatbaar.</p>
            <RouteChip v-for="x in oordeel.uitgesloten" :key="x.route.artikel" :item="x" @uitleg="toonUitleg" />
          </div>
        </section>
      </div>

      <div v-if="uitlegTekst" class="uitleg">
        <nldd-title level="4">Engine-trace — art. {{ uitlegArtikel }}</nldd-title>
        <nldd-button variant="secondary" @click="uitlegTekst = null">Sluit</nldd-button>
        <pre>{{ uitlegTekst }}</pre>
      </div>
    </template>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref, shallowRef } from 'vue';
import RouteChip from './RouteChip.vue';
import { laadEngine } from './lib/engine.js';
import { maakVerkenner } from './lib/buckets.js';

const props = defineProps({ routekaart: { type: Object, required: true } });

const klaar = ref(false);
const fout = ref(null);
const antwoorden = reactive({});
const ruweInvoer = reactive({});
const verkenner = shallowRef(null);
const oordeel = ref({ uitgesloten: [], voldoet: [], mogelijk: [] });
const vragen = ref([]);
const uitlegTekst = ref(null);
const uitlegArtikel = ref(null);

const totaal = computed(() => props.routekaart.routes.length);
const beantwoord = computed(() => Object.keys(antwoorden).length > 0);

onMounted(async () => {
  try {
    const { engine, lawId } = await laadEngine();
    const vf = await (await fetch(`${import.meta.env.BASE_URL}vragenflow.json`)).json();
    verkenner.value = maakVerkenner({
      engine,
      lawId,
      vragenflow: vf,
      routekaart: props.routekaart,
    });
    herbeoordeel();
    klaar.value = true;
  } catch (e) {
    fout.value = String(e);
  }
});

function herbeoordeel() {
  oordeel.value = verkenner.value.beoordeel({ ...antwoorden });
  vragen.value = verkenner.value.volgendeVragen({ ...antwoorden }, oordeel.value);
}

function zet(param, waarde) {
  antwoorden[param] = waarde;
  herbeoordeel();
}
function wis(param) {
  delete antwoorden[param];
  delete ruweInvoer[param];
  herbeoordeel();
}
function zetNumeriek(v, ruw) {
  ruweInvoer[v.param] = ruw;
  const n = Number(ruw);
  if (ruw === '' || !Number.isFinite(n)) {
    delete antwoorden[v.param];
  } else {
    antwoorden[v.param] = v.type === 'amount' ? Math.round(n * 100) : n;
  }
  herbeoordeel();
}
function reset() {
  for (const k of Object.keys(antwoorden)) delete antwoorden[k];
  for (const k of Object.keys(ruweInvoer)) delete ruweInvoer[k];
  herbeoordeel();
}
function toonUitleg(artikel) {
  const res = verkenner.value.uitleg(artikel, { ...antwoorden });
  uitlegArtikel.value = artikel;
  uitlegTekst.value = res.trace ?? res.fout ?? 'Geen trace beschikbaar.';
}
</script>

<style scoped>
/* Aanvullende CSS bovenop het design system: kolom-layout voor de
   vragen/emmers-verdeling en de trace-weergave; hiervoor bestaat geen
   NDD-patroon. */
.intro { max-width: 60rem; }
.kolommen { display: grid; grid-template-columns: minmax(20rem, 1fr) 2fr; gap: 2rem; align-items: start; }
.vraag { margin: 1rem 0; }
.vraag-tekst { margin: 0 0 0.25rem; font-weight: 600; }
.vraag-meta { display: block; font-weight: 400; font-size: 0.8em; color: var(--nldd-color-text-secondary, #555); }
.emmers { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }
.emmer-uitleg { font-size: 0.85em; color: var(--nldd-color-text-secondary, #555); }
.uitleg pre { overflow-x: auto; background: var(--nldd-color-background-secondary, #f5f5f5); padding: 1rem; font-size: 0.75em; }
@media (max-width: 70rem) { .kolommen, .emmers { grid-template-columns: 1fr; } }
</style>
