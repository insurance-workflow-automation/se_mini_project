import { defineConfig } from 'vite';
import { resolve } from 'node:path';

export default defineConfig({
  build: {
    rollupOptions: {
      input: Object.fromEntries(
        ['index', 'login', 'dashboard', 'application', 'applications', 'staff']
          .map((page) => [page, resolve(import.meta.dirname, page + '.html')]),
      ),
    },
  },
});
