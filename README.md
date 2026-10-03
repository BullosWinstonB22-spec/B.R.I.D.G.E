# B.R.I.D.G.E
**B**aranggay **R**esident **I**nformation and **D**igital **G**overnment **E**nvironment

A full-stack barangay information system built with:

| Layer        | Technology                                  | Host          |
|--------------|---------------------------------------------|---------------|
| Frontend     | React 18 + TypeScript (TSX) + Vite          | Firebase Hosting |
| Backend API  | Django 5 + Django REST Framework (Python)   | Render        |
| Database     | PostgreSQL (production) / SQLite (local dev)| Render Postgres |
| Realtime/Auth/Storage | Firebase (Auth, Firestore optional, Storage) | Firebase |
| Serverless   | Node.js (Firebase Cloud Functions, optional)| Firebase      |

> Note on spelling: the project name uses your exact "Baranggay" spelling. The official Philippine term is "Barangay" — you may rename it in `frontend/index.html` and this README if you prefer.

---

## 1. Project layout

```
B.R.I.D.G.E/
├── .env/                  # ALL environment variables live here (gitignored)
│   ├── backend.env.example
│   ├── frontend.env.example
│   ├── firebase.env.example
│   └── README.md
├── backend/               # Django API (deployed to Render)
│   ├── bridge_core/       # Django project settings
│   ├── residents/         # Resident / household / documents / blotter app
│   ├── manage.py
│   ├── requirements.txt
│   ├── Procfile
│   └── runtime.txt
├── frontend/              # React + TSX (deployed to Firebase Hosting)
│   ├── src/
│   ├── firebase.json
│   └── vite.config.ts     # configured to read ../.env/frontend.env
├── functions/             # Node.js Firebase Cloud Functions (optional)
├── render.yaml            # Render blueprint (backend + Postgres)
└── .github/workflows/deploy.yml   # auto-deploy frontend to Firebase on push
```

---

## 2. First-time setup (local)

### 2.1 Environment variables
```bash
cd .env
cp backend.env.example  backend.env
cp frontend.env.example frontend.env
cp firebase.env.example firebase.env   # only needed for CI / service-account use
```
Fill in the real values. **Never commit `*.env` files** — the `.gitignore` already blocks them.

### 2.2 Backend (Django)
```bash
cd backend
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate          # uses SQLite when DATABASE_URL is empty
python manage.py createsuperuser
python manage.py runserver
```
API root: http://localhost:8000/api/  ·  Admin: http://localhost:8000/admin/

### 2.3 Frontend (React + TSX)
```bash
cd frontend
npm install
npm run dev            # http://localhost:5173, proxies /api -> :8000
npm run build          # production build -> dist/
```

---

## 3. Push to GitHub

```bash
git init
git add .
git commit -m "Initial B.R.I.D.G.E scaffold"
git branch -M main
git remote add origin https://github.com/<your-username>/B.R.I.D.G.E.git
git push -u origin main
```

---

## 4. Deploy backend to Render (with PostgreSQL)

**Option A — Blueprint (easiest):** In Render dashboard → **New → Blueprint** → connect this repo.
`render.yaml` auto-creates the Django web service **and** a free PostgreSQL database, and wires `DATABASE_URL` automatically.

**Option B — Manual:**
1. New → **PostgreSQL** (free tier, Singapore region). Copy its **Internal Database URL**.
2. New → **Web Service** → connect repo → set **Root Directory** = `backend`, **Runtime** = Python 3.
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - Start Command: `gunicorn bridge_core.wsgi:application`
3. Add environment variables (from `.env/backend.env`): `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, `DATABASE_URL` (the internal Postgres URL).

Your API will be live at `https://<service-name>.onrender.com`.

---

## 5. Deploy frontend to Firebase Hosting

1. Install CLI: `npm install -g firebase-tools`
2. `firebase login`
3. Create a project at https://console.firebase.google.com (enable **Authentication** and **Storage** if you use them).
4. In `frontend/.firebaserc`, replace `bridge-barangay` with your Firebase project ID.
5. Fill `VITE_FIREBASE_*` values in `.env/frontend.env` (from Firebase console → Project settings → General → Your apps → Web app).
6. First deploy:
   ```bash
   cd frontend
   npm run build
   firebase deploy --only hosting
   ```
After that, every `git push` to `main` auto-deploys via GitHub Actions — just add these **GitHub repo secrets** (Settings → Secrets and variables → Actions):
- `VITE_API_URL`, `VITE_FIREBASE_API_KEY`, `VITE_FIREBASE_AUTH_DOMAIN`, `VITE_FIREBASE_PROJECT_ID`, `VITE_FIREBASE_STORAGE_BUCKET`, `VITE_FIREBASE_MESSAGING_SENDER_ID`, `VITE_FIREBASE_APP_ID`
- `FIREBASE_SERVICE_ACCOUNT_BRIDGE` (paste the whole JSON of a service account key — see `.env/firebase.env.example`)

---

## 6. Data-privacy note
This system stores residents' personal data. Under the Philippine **Data Privacy Act of 2012 (RA 10173)**, register as a personal information controller, publish a privacy notice, and restrict admin access. HTTPS is enforced by both Render and Firebase in production.
