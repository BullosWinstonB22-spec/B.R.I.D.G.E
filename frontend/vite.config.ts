import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";
import fs from "fs";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Load ../.env/frontend.env explicitly. Only VITE_* vars are exposed to the
// browser bundle (matching the names in .env/frontend.env.example exactly).
function loadFrontendEnv(): Record<string, string> {
  const envFile = path.resolve(__dirname, "../.env/frontend.env");
  const out: Record<string, string> = {};
  if (!fs.existsSync(envFile)) return out;
  const lines = fs.readFileSync(envFile, "utf-8").split(/\r?\n/);
  for (const line of lines) {
    const m = line.match(/^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)\s*$/);
    if (!m) continue;
    let val = m[2].trim();
    if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
      val = val.slice(1, -1);
    }
    out[m[1]] = val;
  }
  return out;
}

export default defineConfig(() => {
  const env = loadFrontendEnv();
  const define: Record<string, string> = {};
  for (const [key, val] of Object.entries(env)) {
    if (key.startsWith("VITE_")) define[`import.meta.env.${key}`] = JSON.stringify(val);
  }
  return {
    plugins: [react()],
    envDir: path.resolve(__dirname, "../.env"),
    define,
    build: { outDir: "dist", sourcemap: false },
    server: {
      port: 5173,
      proxy: {
        "/api": { target: "http://localhost:8000", changeOrigin: true },
      },
    },
  };
});
