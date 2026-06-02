# Backend (FastAPI) — Student Management System

This folder contains the **FastAPI** backend for the Student Management System.

## What’s inside

- Entry point: `run.py` (starts Uvicorn)
- App factory/module: `app/main.py`
- API is mounted under: `/api/v1`
- Health check: `GET /health`

The router includes endpoints for:
- Auth, users
- Students, teachers
- Courses, subjects, classes, lectures
- Attendance, marks, reports, notifications

> Exact endpoint paths are organized under `app/api/...` and grouped by router prefixes.

## Requirements

- Python 3.10+ (recommended)
- MongoDB running locally (default config points to `mongodb://localhost:27017`)

## Configuration

Settings live in `app/core/config.py`. Defaults include:

- `API_V1_STR=/api/v1`
- `MONGODB_URL=mongodb://localhost:27017`
- `DATABASE_NAME=student_management`
- CORS origins: `http://localhost:5173`

The app also supports loading variables from a `.env` file.

### Example `.env`
Create a `.env` file inside `backend/` if you want to override defaults:

```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=student_management
API_V1_STR=/api/v1
```

## Run the server (development)

From the `backend/` folder:

```bash
python run.py
```

This runs Uvicorn with:
- host: `0.0.0.0`
- port: `8000`
- reload enabled

## Useful URLs

- Root: `GET http://localhost:8000/`
- Health: `GET http://localhost:8000/health`
- OpenAPI JSON: `GET http://localhost:8000/api/v1/openapi.json`

## Notes / Improvements (recommended)

- Do not commit `venv/` to Git (it currently exists in this repo). Add it to `.gitignore`.
- Consider using a `requirements.txt` or `pyproject.toml` for reproducible installs.
- Consider making CORS origins configurable via environment variables.
