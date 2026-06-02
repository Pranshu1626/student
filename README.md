# Student Management System

Full-stack Student Management System with a **FastAPI** backend and a **React (Vite)** frontend.

## Tech Stack

### Backend
- **FastAPI** (Python)
- **Uvicorn** server
- Versioned API prefix: `/api/v1`
- CORS configured for the frontend dev URL: `http://localhost:5173`

### Frontend
- **React + Vite**
- **React Router**
- **@tanstack/react-query**
- **Axios**
- **Tailwind CSS**
- **Framer Motion**

## Repository Structure

- `backend/` — FastAPI application (API server)
- `frontend/` — React application (web client)

## Quick Start (Development)

### 1) Backend
See `backend/README.md` for backend setup and environment configuration.

### 2) Frontend
See `frontend/README.md` for frontend setup and scripts.

## API Notes

- Base URL (dev): `http://localhost:8000`
- Health check: `GET /health`
- OpenAPI (Swagger) JSON: `GET /api/v1/openapi.json`
- API routes are mounted under: `/api/v1`

## Local Development URLs (typical)
- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`

## License
Add a license if you plan to open-source this project.
