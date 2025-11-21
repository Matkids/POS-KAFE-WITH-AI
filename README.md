# POS-KAFE-WITH-AI
POS sederhana dengan AI Assistant untuk menambah produk secara manual atau via instruksi bahasa alami (AI parsing + validasi server).

## Prasyarat
- Python 3.9+ (venv disarankan)
- PostgreSQL (opsional; bisa mulai dengan SQLite)
- pip (sudah ada di Python)
- Akses internet untuk panggilan AI (opsional; tanpa API key akan pakai parser fallback)

## Setup cepat (backend)
1) Clone repo dan masuk ke folder proyek.
2) Buat virtualenv dan aktifkan:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   ```
3) Install dependensi backend:
   ```bash
   python3 -m pip install -r backend/requirements.txt
   ```
4) Salin `.env.example` → `.env`, lalu isi:
   - `DJANGO_SECRET_KEY`: bebas (untuk dev)
   - `DEBUG=True`
   - Database: kosongkan `DB_NAME` dkk untuk pakai SQLite, atau isi untuk PostgreSQL.
   - AI: isi `OPENAI_API_KEY` dengan key GLM Anda, `OPENAI_MODEL=glm-4.6`, `OPENAI_BASE_URL=https://api.z.ai/api/coding/paas/v4`. Jika tidak ada key, biarkan kosong (fallback parser aktif).
5) Jalankan migrasi:
   ```bash
   cd backend
   python3 manage.py migrate
   ```
6) Jalankan server:
   ```bash
   python3 manage.py runserver
   ```
   API tersedia di `http://127.0.0.1:8000/api/...`.

## Menjalankan frontend
Frontend bersifat static pages di `frontend/public`.
```bash
cd frontend
python3 -m http.server 3000
```
Buka `http://localhost:3000/public/index.html`.

## Endpoint utama
- `POST /api/ai/add-products/` body: `{"instruction": "Add iced latte 25000 stock 10, ..."}`
- `GET /api/products/`
- `GET /api/ai/logs/`

Contoh curl:
```bash
curl -X POST http://127.0.0.1:8000/api/ai/add-products/ \
  -H "Content-Type: application/json" \
  -d '{"instruction":"Add iced latte 25000 stock 10, matcha 27000 stock 5"}'
```

## Catatan AI
- Jika `OPENAI_API_KEY` kosong atau kuota habis, sistem otomatis pakai parser fallback sederhana (tetap memvalidasi harga/stock di server).
- Untuk GLM, pastikan base URL dan model sesuai provider.

## Troubleshooting singkat
- Error DB: gunakan SQLite dengan mengosongkan variabel DB di `.env` atau pastikan PostgreSQL + role/database tersedia.
- 401/429 AI: cek key/kuota di penyedia GLM; atau kosongkan key untuk fallback.
