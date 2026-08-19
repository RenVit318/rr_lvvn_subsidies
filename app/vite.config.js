import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  base: './',
  plugins: [
    vue({
      template: {
        compilerOptions: {
          // nldd-* zijn web components uit het design system
          isCustomElement: (tag) => tag.startsWith('nldd-'),
        },
      },
    }),
  ],
});
