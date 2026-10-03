# .env folder — single source of truth for secrets

Copy each `*.example` file to its matching `*.env` name and fill in real values.
All `*.env` files are gitignored; only `*.example` files are tracked.

| File               | Used by                                  | Loaded by                          |
|--------------------|------------------------------------------|------------------------------------|
| `backend.env`      | Django backend (Render + local)          | `backend/bridge_core/settings.py` (python-dotenv, explicit path) |
| `frontend.env`     | React/TSX app (Firebase Hosting + local) | `frontend/vite.config.ts` (custom loader, `VITE_` prefix only) |
| `firebase.env`     | CI / service-account scripts             | GitHub Actions / `functions/` (optional) |

Variable names below match the code **exactly** — do not rename them.
