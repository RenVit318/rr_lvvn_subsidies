<template>
  <nldd-page>
    <nldd-top-title-bar>
      <nldd-title level="1">LVV-routeverkenner</nldd-title>
    </nldd-top-title-bar>

    <nldd-simple-section v-if="kaart">
      <p class="intro">
        Verken welke artikelen van de Landbouwvrijstellingsverordening
        (geconsolideerd {{ kaart.valid_from }}, geldig t/m {{ kaart.valid_to }})
        een route bieden voor een steun-idee. Dit is de statische laag: filteren
        op feiten uit de verordening zelf. De vragenflow met engine-oordeel is
        laag&nbsp;1.
      </p>

      <div class="filters">
        <nldd-search-field
          placeholder="Zoek in titels en artikelnummers"
          :value="zoek"
          @input="zoek = $event.target.value"
        ></nldd-search-field>

        <nldd-toggle-button-group class="facetten">
          <nldd-toggle-button
            v-for="f in alleFacetten"
            :key="f"
            :pressed="facetKeuze.has(f)"
            @click="wisselFacet(f)"
          >{{ f }}</nldd-toggle-button>
        </nldd-toggle-button-group>

        <div class="bedrag-filter">
          <nldd-number-field
            label="Voorgenomen steunbedrag (EUR, optioneel)"
            :value="bedragEur"
            @input="bedragEur = $event.target.value"
          ></nldd-number-field>
          <nldd-switch-field
            label="Alleen routes zonder kmo-vereiste"
            :checked="zonderKmo"
            @change="zonderKmo = $event.target.checked"
          ></nldd-switch-field>
        </div>
      </div>

      <p class="telling">
        {{ gefilterd.length }} van {{ kaart.routes.length }} routes
        <template v-if="bedragCent !== null">
          — routes met een overschreden aanmeldingsdrempel zijn gemarkeerd
        </template>
      </p>

      <nldd-list>
        <nldd-list-item v-for="r in gefilterd" :key="r.artikel">
          <div class="route" :class="{ open: openArtikel === r.artikel }">
            <button class="route-kop" @click="toggle(r.artikel)">
              <nldd-badge>art. {{ r.artikel }}</nldd-badge>
              <span class="route-titel">{{ r.titel }}</span>
              <span class="route-meta">
                <nldd-tag v-if="r.kmo_vereist">kmo</nldd-tag>
                <nldd-tag v-for="f in r.facetten.filter((x) => x !== 'kmo')" :key="f">{{ f }}</nldd-tag>
                <nldd-tag v-if="r.max_intensiteit_pct">&le; {{ r.max_intensiteit_pct }}%</nldd-tag>
                <nldd-tag v-if="drempelTekst(r)">{{ drempelTekst(r) }}</nldd-tag>
                <nldd-tag v-if="drempelOverschreden(r)" class="waarschuwing">boven drempel</nldd-tag>
                <nldd-tag v-if="r.untranslatables.length">{{ r.untranslatables.length }} menselijke toets(en)</nldd-tag>
              </span>
            </button>

            <div v-if="openArtikel === r.artikel" class="route-detail">
              <nldd-banner v-if="drempelOverschreden(r)" variant="warning">
                Het opgegeven bedrag overschrijdt de aanmeldingsdrempel van dit
                artikel; deze route vergt dan een reguliere aanmelding bij de
                Commissie.
              </nldd-banner>

              <template v-if="r.untranslatables.length">
                <nldd-title level="4">Voorwaarden die menselijke beoordeling vergen</nldd-title>
                <ul>
                  <li v-for="(u, i) in r.untranslatables" :key="i">
                    <strong>{{ u.construct }}</strong> — {{ u.reason }}
                  </li>
                </ul>
              </template>

              <nldd-title level="4">Feiten die deze route uitvraagt ({{ r.parameters.length }})</nldd-title>
              <ul class="param-lijst">
                <li v-for="p in r.parameters" :key="p.name">
                  <code>{{ p.name }}</code>
                  <span class="param-descr">{{ p.description }}</span>
                </li>
              </ul>

              <nldd-button variant="secondary" @click="openTekst(r)">
                Lees de wettekst (EUR-Lex)
              </nldd-button>
            </div>
          </div>
          <nldd-divider></nldd-divider>
        </nldd-list-item>
      </nldd-list>
    </nldd-simple-section>

    <nldd-simple-section v-else>
      <nldd-banner v-if="laadfout" variant="error">{{ laadfout }}</nldd-banner>
      <p v-else>Routekaart laden…</p>
    </nldd-simple-section>
  </nldd-page>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';

const kaart = ref(null);
const laadfout = ref(null);
const zoek = ref('');
const facetKeuze = ref(new Set());
const bedragEur = ref('');
const zonderKmo = ref(false);
const openArtikel = ref(null);

onMounted(async () => {
  try {
    const res = await fetch(`${import.meta.env.BASE_URL}routekaart.json`);
    if (!res.ok) throw new Error(`routekaart.json: HTTP ${res.status}`);
    kaart.value = await res.json();
  } catch (e) {
    laadfout.value = String(e);
  }
});

const alleFacetten = computed(() => {
  if (!kaart.value) return [];
  const s = new Set();
  for (const r of kaart.value.routes) r.facetten.forEach((f) => s.add(f));
  return [...s].sort();
});

const bedragCent = computed(() => {
  const v = Number(bedragEur.value);
  return bedragEur.value !== '' && Number.isFinite(v) && v > 0 ? Math.round(v * 100) : null;
});

function wisselFacet(f) {
  const s = new Set(facetKeuze.value);
  s.has(f) ? s.delete(f) : s.add(f);
  facetKeuze.value = s;
}

function drempelOverschreden(r) {
  if (bedragCent.value === null) return false;
  return r.drempels.some((d) => bedragCent.value > d.bedrag_eurocent);
}

function drempelTekst(r) {
  if (!r.drempels.length) return null;
  const laagste = Math.min(...r.drempels.map((d) => d.bedrag_eurocent));
  return `drempel € ${(laagste / 100).toLocaleString('nl-NL')}`;
}

const gefilterd = computed(() => {
  if (!kaart.value) return [];
  const q = zoek.value.trim().toLowerCase();
  return kaart.value.routes.filter((r) => {
    if (q && !(`${r.artikel} ${r.titel ?? ''}`.toLowerCase().includes(q))) return false;
    if (zonderKmo.value && r.kmo_vereist) return false;
    for (const f of facetKeuze.value) if (!r.facetten.includes(f)) return false;
    return true;
  });
});

function toggle(artikel) {
  openArtikel.value = openArtikel.value === artikel ? null : artikel;
}

function openTekst(r) {
  window.open(r.url, '_blank', 'noopener');
}
</script>

<style scoped>
/* Aanvullende CSS bovenop het design system (gerapporteerd in de PoC-docs):
   lay-outlijm voor de routekaart-lijst; er bestaat geen NDD-patroon voor een
   filterbare kaart-lijst met inline-detail. */
.intro { max-width: 60rem; }
.filters { display: flex; flex-direction: column; gap: 0.75rem; margin: 1rem 0; }
.facetten { display: flex; flex-wrap: wrap; gap: 0.5rem; }
.bedrag-filter { display: flex; gap: 2rem; align-items: end; flex-wrap: wrap; }
.telling { color: var(--nldd-color-text-secondary, #555); }
.route-kop {
  display: flex; align-items: baseline; gap: 0.75rem; width: 100%;
  background: none; border: none; padding: 0.5rem 0; cursor: pointer;
  text-align: left; font: inherit;
}
.route-titel { font-weight: 600; }
.route-meta { display: flex; flex-wrap: wrap; gap: 0.25rem; margin-left: auto; }
.route-detail { padding: 0 0 1rem 0.5rem; }
.param-lijst { columns: 2; max-width: 70rem; }
.param-lijst li { break-inside: avoid; margin-bottom: 0.25rem; }
.param-descr { color: var(--nldd-color-text-secondary, #555); font-size: 0.85em; margin-left: 0.5rem; }
.waarschuwing { --nldd-tag-background: #fdecea; }
</style>
