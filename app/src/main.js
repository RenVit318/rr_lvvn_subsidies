import { createApp } from 'vue';
import App from './App.vue';
import '@nldd/design-system/styles';
// Eén import per gebruikt nldd-component (conventie uit de regelrecht-frontend).
import '@nldd/design-system/badge';
import '@nldd/design-system/banner';
import '@nldd/design-system/box';
import '@nldd/design-system/button';
import '@nldd/design-system/divider';
import '@nldd/design-system/icon';
import '@nldd/design-system/list';
import '@nldd/design-system/list-item';
import '@nldd/design-system/number-field';
import '@nldd/design-system/page';
import '@nldd/design-system/search-field';
import '@nldd/design-system/simple-section';
import '@nldd/design-system/spacer';
import '@nldd/design-system/switch-field';
import '@nldd/design-system/tag';
import '@nldd/design-system/title';
import '@nldd/design-system/toggle-button';
import '@nldd/design-system/toggle-button-group';
import '@nldd/design-system/top-title-bar';

createApp(App).mount('#app');
