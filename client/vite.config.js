import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');

  return {
    plugins: [react()],
    server: {
      host: '0.0.0.0',
      port: 5173,
      allowedHosts: [env.CLIENT_CONTAINER_NAME, 'localhost', '127.0.0.1'],
      hmr: {
        protocol: 'ws',
        host: 'localhost',
        port: 5173,
        clientPort: 80,
        path: "/__vite_ws",
      },
      watch: {
        usePolling: true,
      },
    },
    css: {
      devSourcemap: true
    },
  }
})
