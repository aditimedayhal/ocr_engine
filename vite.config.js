import { defineConfig } from 'vite';

export default defineConfig({
  server: {
    proxy: {
      '/upload': 'http://localhost:5000',
    },
  },
});
