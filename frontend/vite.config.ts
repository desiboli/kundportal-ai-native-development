import { resolve } from "node:path"
import tailwindcss from "@tailwindcss/vite"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": resolve(import.meta.dirname, "./src"),
    },
  },
  server: {
    // Requests to /api/... are forwarded to the backend on port 8010 without /api,
    // so /api/health becomes /health. This way the backend needs no CORS.
    proxy: {
      "/api": {
        target: "http://localhost:8010",
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
})
