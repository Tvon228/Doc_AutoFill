import { defineConfig } from 'vite';
import solidPlugin from 'vite-plugin-solid';

export default defineConfig({
  plugins: [solidPlugin()],
  server: {
    proxy: {
      '/auth': {
        target: `http://localhost:${process.env.PORT || 8000}`,
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/auth/, '/auth'), 
      },
    },
  },
});