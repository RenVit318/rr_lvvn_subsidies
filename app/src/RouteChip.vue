<template>
  <div class="chip">
    <nldd-badge>art. {{ item.route.artikel }}</nldd-badge>
    <span class="chip-titel">{{ item.route.titel }}</span>
    <nldd-tag v-if="item.status === 'mogelijk_onzeker'" title="De polariteits-analyse kon dit artikel niet volledig doorgronden; het oordeel is indicatief.">analyse onvolledig</nldd-tag>
    <nldd-tag v-if="item.route.untranslatables.length">{{ item.route.untranslatables.length }} menselijke toets(en)</nldd-tag>
    <nldd-button variant="tertiary" @click="$emit('uitleg', item.route.artikel)">waarom?</nldd-button>
  </div>
</template>

<script setup>
defineProps({ item: { type: Object, required: true } });
defineEmits(['uitleg']);
</script>

<style scoped>
/* Aanvullende CSS: chip-regel-layout (geen NDD-patroon voor compacte
   route-chips met inline-actie). */
.chip { display: flex; align-items: center; gap: 0.5rem; padding: 0.25rem 0; flex-wrap: wrap; }
.chip-titel { font-size: 0.85em; }
</style>
