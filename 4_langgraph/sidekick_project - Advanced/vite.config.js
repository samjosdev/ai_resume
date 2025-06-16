import { defineConfig } from 'vite'

export default defineConfig({
  root: 'frontend',
  server: {
    port: 3000,
    proxy: {
      '/chat': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
}) 