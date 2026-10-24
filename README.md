# FastAPI Backend

## Requirements

- Python 3.12+
- PostgreSQL 16
- Docker & Docker Compose (optional)

## Run locally

**1. Clone and set up environment**

```bash
cp .env.example .env
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**2. Start the database**

```bash
docker compose up db -d
```

**3. Run migrations**

```bash
alembic upgrade head
```

**4. Start the server**

```bash
uvicorn app.main:app --reload
```

API docs available at [http://localhost:8000/docs](http://localhost:8000/docs)

## Run with Docker

```bash
docker compose up --build
```

## Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/v1/auth/register` | — | Register |
| POST | `/api/v1/auth/login` | — | Login |
| POST | `/api/v1/auth/refresh` | — | Refresh tokens |
| POST | `/api/v1/auth/logout` | JWT | Logout |
| GET | `/api/v1/users/me` | JWT | Get current user |
| PATCH | `/api/v1/users/me` | JWT | Update current user |
| DELETE | `/api/v1/users/me` | JWT | Delete account |
| GET | `/api/v1/users/me/profile` | JWT | Get profile |
| PATCH | `/api/v1/users/me/profile` | JWT | Update profile |
| GET | `/health` | — | Health check |
