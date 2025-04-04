import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path';

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    host: '127.0.0.1', // Forces the dev server to use 127.0.0.1 instead of localhost
    port: 5173, // Optional: Explicitly set the port (default is 5173)
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  optimizeDeps: {
    include: ['bootstrap-vue-next'], // Force Vite to pre-bundle it
  },
})
