# FastAPI Backend for Runsite

A minimal FastAPI starter that runs on Runsite. It has email and password sign-up, JWT access and refresh tokens, a
user account and a profile, stored in PostgreSQL through async SQLAlchemy and Alembic migrations. Use it as the base
for an API of your own: the code is split into routes, services and repositories, so a new feature is a few small
files next to the existing ones.

[![Deploy on Runsite](https://img.shields.io/badge/Deploy%20on-Runsite-0f172a?style=for-the-badge)](https://dashboard.runsite.app)

Runsite builds the service from the `Dockerfile` in this repository. On every start the container applies the
database migrations and then starts the API, so a new deploy needs no manual steps.

- Runsite: https://runsite.app
- Dashboard: https://dashboard.runsite.app
- Docs: https://docs.runsite.app
- Template gallery: https://dashboard.runsite.app/templates
- FastAPI docs: https://fastapi.tiangolo.com

## What's inside

- **Authentication:** register and log in with email and password, a short-lived access token (30 minutes) and a
  refresh token (7 days), both signed with `SECRET_KEY`. Passwords are hashed with bcrypt.
- **Users and profiles:** read, update and delete your own account, and a profile (first name, last name, bio,
  avatar URL) created together with the user.
- **Database:** PostgreSQL 16, SQLAlchemy 2.0 async with `asyncpg`, Alembic migrations in `alembic/versions/`.
  A `postgres://` or `postgresql://` URL with `sslmode=...` is converted to the `asyncpg` format automatically.
- **API:** Swagger UI at `/docs`, ReDoc at `/redoc`, a health check at `/health`, pagination helpers from
  `fastapi-pagination`, CORS and a JSON 500 handler that logs the error.
- **`Dockerfile`:** Python 3.12 slim. Runs `alembic upgrade head`, then Uvicorn on `PORT` (default `8000`).
- **`docker-compose.yml`:** a local copy of the Runsite setup: PostgreSQL and the API.

Project layout:

```
app/
  main.py            FastAPI app, CORS, error handler, /health
  dependencies.py    get_current_user (Bearer token -> User)
  config/            settings (environment variables), database session, logger
  routes/            HTTP endpoints, one file per feature
  services/          business logic: auth, users, profiles
  repositories/      database queries, BaseRepository with CRUD and pagination
  models/            SQLAlchemy models: User, Profile
  schemas/           Pydantic request and response models
alembic/versions/    database migrations
```

## Deploy on Runsite

1. Push this repository to your GitHub account.
2. In the [Runsite dashboard](https://dashboard.runsite.app) create a project and add a **PostgreSQL** database.
3. Add a **web service** from the repository. Build type **Dockerfile**, port **8000**.
4. Open the web service → **Environment** and set the variables below. Saving redeploys the service.
5. When the build finishes, the deploy logs show `Running upgrade  -> 0001, initial` and `Uvicorn running on
   http://0.0.0.0:8000`. Open `{service URL}/docs` to try the API.

| Variable | Value |
|---|---|
| `DATABASE_URL` | Internal URL of the PostgreSQL database |
| `SECRET_KEY` | A random string, for example from `python3 -c "import secrets; print(secrets.token_urlsafe(48))"` |
| `CORS_ORIGINS` | The URLs of your frontend, for example `["https://app.example.com"]` |

## API

All endpoints except `/health` live under `/api/v1`. Protected endpoints take the access token in the
`Authorization: Bearer <access_token>` header.

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/auth/register` | none | Create an account. Returns an access and a refresh token. |
| POST | `/api/v1/auth/login` | none | Log in with email and password. Returns new tokens. |
| POST | `/api/v1/auth/refresh` | none | Exchange a refresh token for new tokens. |
| POST | `/api/v1/auth/logout` | JWT | Returns 204. Tokens stay valid until they expire; the client deletes them. |
| GET | `/api/v1/users/me` | JWT | Current user. |
| PATCH | `/api/v1/users/me` | JWT | Change the email. |
| DELETE | `/api/v1/users/me` | JWT | Delete the account and its profile. |
| GET | `/api/v1/users/me/profile` | JWT | Current user's profile. |
| PATCH | `/api/v1/users/me/profile` | JWT | Update first name, last name, bio or avatar URL. |
| GET | `/health` | none | Returns `{"status": "ok"}`. |

Example:

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secret123"}'
```

## Configuration

Settings are read from environment variables and, locally, from `.env` (see `.env.example`).

| Variable | Default | Purpose |
|---|---|---|
| `DATABASE_URL` | `postgresql+asyncpg://postgres:postgres@localhost:5432/app_db` | PostgreSQL connection. `postgres://` and `sslmode=require` are converted for `asyncpg`. |
| `SECRET_KEY` | `your-secret-key-change-me` | Signs the tokens. Always set your own in production. Changing it signs everyone out. |
| `ALGORITHM` | `HS256` | JWT signing algorithm. |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Access token lifetime. |
| `REFRESH_TOKEN_EXPIRE_DAYS` | `7` | Refresh token lifetime. |
| `CORS_ORIGINS` | `["http://localhost:3000", "http://localhost:8000"]` | Origins allowed to call the API from a browser, as a JSON list. |
| `DEBUG` | `false` | Debug logging and SQL query logging. |
| `PORT` | `8000` | Port Uvicorn listens on inside the container. |

## Local development

### With Docker

Requirements: Docker.

```bash
docker compose up --build
```

The API applies the migrations and starts on http://localhost:8000. Open http://localhost:8000/docs. If port 8000
or 5432 is taken, run `APP_PORT=8001 DB_PORT=5433 docker compose up --build`. `docker compose down -v` stops the
containers and deletes the data.

### Without Docker

Requirements: Python 3.12, Docker for the database (or your own PostgreSQL 16).

```bash
cp .env.example .env
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

docker compose up db -d
alembic upgrade head
uvicorn app.main:app --reload
```

Open http://localhost:8000/docs.

## Database migrations

After changing a model in `app/models/`, generate a migration, review the new file in `alembic/versions/` and apply
it:

```bash
alembic revision --autogenerate -m "add orders"
alembic upgrade head
```

A new model must be imported in `app/models/__init__.py`, otherwise Alembic does not see it. On Runsite the
migration runs by itself on the next deploy.

## Adding a feature

Copy the profile feature layer by layer:

1. Model in `app/models/`, imported in `app/models/__init__.py`, plus a migration.
2. Schemas in `app/schemas/`.
3. Repository in `app/repositories/`, extending `BaseRepository`.
4. Service in `app/services/` with the business rules.
5. Routes in `app/routes/`, included in `app/routes/router.py`. Use `Depends(get_current_user)` for protected
   endpoints.

## Limitations

- **Logout:** tokens are stateless, so logout does not revoke them. Revoking needs a token blacklist, for example in
  Redis.
- **No email verification or password reset.** For a starter with these, teams, billing and an admin panel, see
  [Runsite SaaS Kit](https://github.com/runsite-platform/runsite-saas-kit).
- **No tests yet.**
