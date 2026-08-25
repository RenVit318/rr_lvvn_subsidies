<template>
  <div>
    <p class="intro">
      Beantwoord vragen over het steun-idee; elke vraag verdeelt de
      {{ totaal }} routes opnieuw over drie emmers. <em>Weet niet</em> laten
      staan mag altijd — dan blijft de route in "mogelijk, mits".
    </p>

    <nldd-banner v-if="fout" variant="error" :text="fout"></nldd-banner>
    <p v-else-if="!klaar">Engine en corpus laden…</p>

    <template v-else>
      <div class="kolommen">
        <section class="vragen">
          <nldd-title size="4"><h4>Wat voor steun is het?</h4></nldd-title>
          <p class="vraag-meta">Artikel 1, lid 1 — kies alles wat van toepassing is; de rest geldt dan als niet van toepassing.</p>
          <div class="chips">
            <nldd-toggle-button
              v-for="p in categorieParams" :key="p"
              :value="p"
              :text="humaniseer(p)"
              :title="beschrijvingVan(p)"
              size="sm"
              :selected="categorieKeuze.has(p) || undefined"
              @click="wisselCategorie(p)"
            ></nldd-toggle-button>
          </div>

          <nldd-spacer size="16"></nldd-spacer>
          <nldd-title size="4"><h4>Bijzonderheden</h4></nldd-title>
          <p class="vraag-meta">Artikel 1, leden 3-7 — uitsluitingen en uitzonderingen. Meestal geldt hier niets van.</p>
          <nldd-switch-field
            label="Geen van deze bijzonderheden is van toepassing"
            :checked="geenBijzonderheden || undefined"
            @change="zetGeenBijzonderheden($event.detail?.checked ?? $event.target.checked)"
          ></nldd-switch-field>
          <div class="chips">
            <nldd-toggle-button
              v-for="p in bijzonderParams" :key="p"
              :value="p"
              :text="humaniseer(p)"
              :title="beschrijvingVan(p)"
              size="sm"
              :selected="antwoorden[p] === true || undefined"
              @click="wisselBijzonderheid(p)"
            ></nldd-toggle-button>
          </div>

          <nldd-spacer size="16"></nldd-spacer>
          <nldd-title size="4"><h4>{{ routeFilter ? `Vragen voor art. ${routeFilter}` : 'Vervolgvragen' }}</h4></nldd-title>
          <div v-if="routeFilter" class="filter-regel">
            <nldd-tag size="sm" :text="`gefilterd op art. ${routeFilter}`"></nldd-tag>
            <nldd-button variant="secondary" size="sm" text="Toon algemene vragen" @click="routeFilter = null; herbeoordeel()"></nldd-button>
          </div>
          <div v-for="v in vragen" :key="v.param" class="vraag">
            <p class="vraag-tekst">
              {{ kortLabel(v.param) }}
              <span class="vraag-meta">
                <template v-if="routeFilter">{{ v.eigenVraag ? 'artikel-specifiek' : 'gemeenschappelijke voorwaarde' }}</template>
                <template v-else>raakt {{ v.raaktRoutes }} routes · art. {{ v.artikelen.join(', ') }}</template>
              </span>
            </p>
            <p v-if="v.beschrijving" class="vraag-toelichting" :title="v.beschrijving">{{ v.beschrijving }}</p>
            <div v-if="v.type === 'boolean'" class="antwoord">
              <nldd-toggle-button-group type="radio" size="sm" :accessible-label="v.param">
                <nldd-toggle-button value="ja" text="Ja" :selected="antwoorden[v.param] === true || undefined" @click="zetKeuze(v, 'ja')"></nldd-toggle-button>
                <nldd-toggle-button value="nee" text="Nee" :selected="antwoorden[v.param] === false || undefined" @click="zetKeuze(v, 'nee')"></nldd-toggle-button>
                <nldd-toggle-button value="weet_niet" text="Weet niet" :selected="!(v.param in antwoorden) || undefined" @click="zetKeuze(v, 'weet_niet')"></nldd-toggle-button>
              </nldd-toggle-button-group>
            </div>
            <div v-else-if="v.opties.length" class="antwoord">
              <nldd-toggle-button-group type="radio" size="sm" :accessible-label="v.param">
                <nldd-toggle-button
                  v-for="o in v.opties" :key="o"
                  :value="o"
                  :text="o.toLowerCase().replaceAll('_', ' ')"
                  :selected="antwoorden[v.param] === o || undefined"
                  @click="zetOptie(v, o)"
                ></nldd-toggle-button>
                <nldd-toggle-button value="__weet_niet__" text="Weet niet" :selected="!(v.param in antwoorden) || undefined" @click="zetOptie(v, '__weet_niet__')"></nldd-toggle-button>
              </nldd-toggle-button-group>
            </div>
            <div v-else class="antwoord">
              <nldd-number-field
                :label="v.type === 'amount' ? 'Bedrag in EUR' : 'Waarde'"
                :value="ruweInvoer[v.param] ?? ''"
                @input="zetNumeriek(v, $event.target.value)"
                @change="zetNumeriek(v, $event.detail?.value ?? $event.target.value)"
              ></nldd-number-field>
            </div>
          </div>
          <nldd-button v-if="beantwoord" variant="secondary" text="Begin opnieuw" @click="reset"></nldd-button>
        </section>

        <section class="emmers-wrap">
          <p class="antwoord-teller">
            {{ Object.keys(antwoorden).length }} feiten beantwoord · beoordeling #{{ beoordelingsTeller }}
          </p>
          <div class="emmers">
          <div class="emmer">
            <nldd-title size="4"><h4>Voldoet al ({{ oordeel.voldoet.length }})</h4></nldd-title>
            <p class="emmer-uitleg">Alle machinaal toetsbare voorwaarden zijn met deze antwoorden vervuld.</p>
            <RouteChip v-for="x in oordeel.voldoet" :key="x.route.artikel" :item="x" @uitleg="toonUitleg" @vragen="filterOpRoute" />
          </div>
          <div class="emmer">
            <nldd-title size="4"><h4>Mogelijk, mits… ({{ oordeel.mogelijk.length }})</h4></nldd-title>
            <p class="emmer-uitleg">Nog open; sommige met onvolledige analyse (gemarkeerd). Klik "vragen" om gericht één route rond te maken.</p>
            <RouteChip v-for="x in oordeel.mogelijk" :key="x.route.artikel" :item="x" :toonVragenKnop="true" @uitleg="toonUitleg" @vragen="filterOpRoute" />
          </div>
          <div class="emmer">
            <nldd-title size="4"><h4>Uitgesloten ({{ oordeel.uitgesloten.length }})</h4></nldd-title>
            <p class="emmer-uitleg">Geen invulling van de open vragen maakt deze route nog toelaatbaar.</p>
            <RouteChip v-for="x in oordeel.uitgesloten" :key="x.route.artikel" :item="x" @uitleg="toonUitleg" />
          </div>
          </div>
        </section>
      </div>

      <div v-if="uitlegTekst" class="uitleg">
        <nldd-title size="5"><h5>Engine-trace — art. {{ uitlegArtikel }}</h5></nldd-title>
        <nldd-button variant="secondary" text="Sluit" @click="uitlegTekst = null"></nldd-button>
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

// Groepering uit de modelstructuur van artikel 1 (param_context in
// vragenflow.json): categorie-OR van lid 1 vs de uitsluitings-leden.
const categorieParams = ref([]);
const bijzonderParams = ref([]);
const categorieKeuze = ref(new Set());
const geenBijzonderheden = ref(false);
let vragenData = null;

function humaniseer(p) {
  return p
    .replace(/^(betreft_|is_|heeft_|vormt_|steun_|verricht_)/, '')
    .replaceAll('_', ' ');
}
function beschrijvingVan(p) {
  return vragenData?.vragen?.[p]?.beschrijving ?? p;
}

onMounted(async () => {
  try {
    const { engine, lawId } = await laadEngine();
    const vf = await (await fetch(`${import.meta.env.BASE_URL}vragenflow.json`)).json();
    vragenData = vf;
    const ctx = vf.artikelen['1']?.param_context ?? {};
    categorieParams.value = Object.keys(ctx).filter((p) =>
      ctx[p].includes('valt_onder_categorie_lid_1'),
    );
    bijzonderParams.value = Object.keys(vf.artikelen['1']?.params ?? {}).filter(
      (p) => !categorieParams.value.includes(p),
    );
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

const routeFilter = ref(null);

function herbeoordeel() {
  oordeel.value = verkenner.value.beoordeel({ ...antwoorden });
  const gegroepeerd = new Set([...categorieParams.value, ...bijzonderParams.value]);
  if (routeFilter.value) {
    vragen.value = verkenner.value
      .vragenVoorRoute(routeFilter.value, { ...antwoorden })
      .filter((v) => !gegroepeerd.has(v.param));
  } else {
    vragen.value = verkenner.value
      .volgendeVragen({ ...antwoorden }, oordeel.value, 20)
      .filter((v) => !gegroepeerd.has(v.param))
      .slice(0, 8);
  }
}

function filterOpRoute(artikel) {
  routeFilter.value = artikel;
  herbeoordeel();
}

function kortLabel(p) {
  const kaal = p
    .replace(/^(betreft_|is_|heeft_|vormt_|wordt_|steun_voor_)/, '')
    .replaceAll('_', ' ');
  return kaal.charAt(0).toUpperCase() + kaal.slice(1) + '?';
}

function wisselCategorie(p) {
  const s = new Set(categorieKeuze.value);
  s.has(p) ? s.delete(p) : s.add(p);
  categorieKeuze.value = s;
  if (s.size === 0) {
    for (const q of categorieParams.value) delete antwoorden[q];
  } else {
    for (const q of categorieParams.value) antwoorden[q] = s.has(q);
  }
  herbeoordeel();
}

function zetGeenBijzonderheden(aan) {
  geenBijzonderheden.value = !!aan;
  for (const p of bijzonderParams.value) {
    if (geenBijzonderheden.value) antwoorden[p] = antwoorden[p] === true ? true : false;
    else if (antwoorden[p] === false) delete antwoorden[p];
  }
  herbeoordeel();
}

function wisselBijzonderheid(p) {
  if (antwoorden[p] === true) {
    if (geenBijzonderheden.value) antwoorden[p] = false;
    else delete antwoorden[p];
  } else {
    antwoorden[p] = true;
  }
  herbeoordeel();
}

function zetKeuze(v, keuze) {
  if (keuze === 'ja') antwoorden[v.param] = true;
  else if (keuze === 'nee') antwoorden[v.param] = false;
  else delete antwoorden[v.param];
  herbeoordeel();
}
function zetOptie(v, keuze) {
  if (!keuze || keuze === '__weet_niet__') delete antwoorden[v.param];
  else antwoorden[v.param] = keuze;
  herbeoordeel();
}
function zetNumeriek(v, ruw) {
  ruweInvoer[v.param] = ruw;
  const n = Number(ruw);
  if (ruw === '' || ruw === null || !Number.isFinite(n)) {
    delete antwoorden[v.param];
  } else {
    antwoorden[v.param] = v.type === 'amount' ? Math.round(n * 100) : n;
  }
  herbeoordeel();
}
function reset() {
  for (const k of Object.keys(antwoorden)) delete antwoorden[k];
  for (const k of Object.keys(ruweInvoer)) delete ruweInvoer[k];
  categorieKeuze.value = new Set();
  geenBijzonderheden.value = false;
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
   NDD-patroon. Alle interactie-elementen zijn NDD-componenten. */
.intro { max-width: 60rem; }
.kolommen { display: grid; grid-template-columns: minmax(22rem, 1fr) 2fr; gap: 2rem; align-items: start; }
.vraag { margin: 1.25rem 0; }
.chips { display: flex; flex-wrap: wrap; gap: 0.4rem; margin: 0.5rem 0 1rem; }
.filter-regel { display: flex; align-items: center; gap: 0.5rem; margin: 0.5rem 0; }
.vraag-toelichting {
  margin: 0.15rem 0 0.35rem;
  font-size: 0.8em;
  color: var(--nldd-color-text-secondary, #555);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.vraag-tekst { margin: 0 0 0.35rem; font-weight: 600; }
.vraag-meta { display: block; font-weight: 400; font-size: 0.8em; color: var(--nldd-color-text-secondary, #555); }
.emmers { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; }
.emmer-uitleg { font-size: 0.85em; color: var(--nldd-color-text-secondary, #555); }
.uitleg { margin-top: 2rem; }
.uitleg pre { overflow-x: auto; background: var(--nldd-color-background-secondary, #f5f5f5); padding: 1rem; font-size: 0.75em; }
@media (max-width: 70rem) { .kolommen, .emmers { grid-template-columns: 1fr; } }
</style>
