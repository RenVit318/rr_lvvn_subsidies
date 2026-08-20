<template>
  <div class="chip">
    <nldd-badge :text="`art. ${item.route.artikel}`"></nldd-badge>
    <span class="chip-titel">{{ item.route.titel }}</span>
    <nldd-tag
      v-if="item.status === 'mogelijk_onzeker'"
      size="sm"
      text="analyse onvolledig"
      title="De polariteits-analyse doorgrondt de IF-structuur van dit artikel nog niet volledig; deze route krijgt daarom geen machinaal uitsluitingsoordeel. Verdiepingskandidaat voor cyclus 2."
    ></nldd-tag>
    <nldd-tag
      v-if="item.indicatief"
      size="sm"
      text="indicatief"
      title="Uitsluiting vastgesteld met enkelvoudige variaties over onzeker geanalyseerde feiten; combinaties zijn niet uitputtend verkend."
    ></nldd-tag>
    <nldd-tag
      v-if="item.route.untranslatables.length"
      size="sm"
      :text="`${item.route.untranslatables.length} menselijke toets(en)`"
    ></nldd-tag>
    <nldd-button variant="secondary" size="sm" text="Waarom?" @click="$emit('uitleg', item.route.artikel)"></nldd-button>
  </div>
</template>

<script setup>
defineProps({ item: { type: Object, required: true } });
defineEmits(['uitleg']);
</script>

<style scoped>
/* Aanvullende CSS: chip-regel-layout (geen NDD-patroon voor compacte
   route-chips met inline-actie). */
.chip { display: flex; align-items: center; gap: 0.5rem; padding: 0.3rem 0; flex-wrap: wrap; }
.chip-titel { font-size: 0.85em; }
</style>
