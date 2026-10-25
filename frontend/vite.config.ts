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
    // Anrop till /api/... skickas vidare till backenden på port 8010 utan /api,
    // så /api/health blir /health. Då behövs ingen CORS i backenden.
    proxy: {
      "/api": {
        target: "http://localhost:8010",
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
})
