import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/ask': 'http://localhost:8000',
      '/upload': 'http://localhost:8000',
      '/refresh': 'http://localhost:8000',
      '/docss': 'http://localhost:8000',
      '/history': 'http://localhost:8000',
      '/status': 'http://localhost:8000',
      '/user': 'http://localhost:8000',
    }
  }
})
