# Migrating your old Barangay Management System (BMS) data

Your old system (custom Python stdlib server + SQLite + optional Mongo) has been
rebuilt on Django + React/TSX. **All 21 tables were migrated and verified** —
row counts match the original exactly.

## Run the import yourself (idempotent, safe to re-run)

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py migrate_old_bms --db /path/to/your/bms.sqlite3
```

This imports: users (8), residents (16), resident-ID issuances (16) + sequence,
classifications, barangay officials (3), announcements, programs, requests (2),
certificate issuances (2), tasks (6) + assignments + updates, staff-assignment
history, conversations (1) + messages (12) + recipients (12), notifications (38),
gallery (3), activity logs (177), and all 35 system settings (branding, hero,
contact info, watermark/content-protection flags).

## Images / uploads
Copy your old `uploads/` and `assets/` folders into `backend/media/` (already
done in this package — 28 files). In production on Render, mount a persistent
disk at `/data` and set `MEDIA_ROOT` accordingly, or serve uploads via Firebase
Storage (frontend `src/firebase.ts` is wired for it).

## Passwords
The old BMS used a custom password-hash algorithm that is **not portable**.
Imported users get an unusable password. Do ONE of:
- `python manage.py createsuperuser` for a fresh admin, then set passwords for
  other users via `/admin/`.
- Or let users reset via Django's password-reset flow (add an email backend).

## Old features preserved
- Resident ID auto-sequence (`resident_id_prefix` + `resident_id_sequence_length`
  settings → `ResidentIDSequence` model).
- Classifications (Senior Citizen / PWD / Solo Parent / Student / Regular).
- Document requests + certificate issuance tracking.
- Task assignment → staff → updates (acknowledge / progress / complete).
- Internal messaging (conversations, messages, recipients, read tracking).
- Notifications + activity-log audit trail.
- Public CMS: hero banner, welcome text, officials, announcements, programs,
  gallery, contact block — all driven by `system_settings` and served at
  `GET /api/public-site/` (the React landing page consumes it).
- Content-protection flags (watermark text/opacity/position, right-click,
  drag-prevention) are stored in settings; server-side watermarking is available
  via Pillow (in requirements.txt).

## Retired
- MongoDB (data was already in SQLite; Mongo was optional). Use PostgreSQL on
  Render as the single source of truth.
- Custom stdlib HTTP server + rate limiter → Gunicorn + DRF throttling.
- `.bat`/`.vbs` Windows autostart scripts → Render/Firebase hosting.
