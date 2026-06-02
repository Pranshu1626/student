# Frontend (React + Vite) — Student Management System

This folder contains the **React** frontend for the Student Management System.

## Tech Stack

- React (Vite)
- React Router
- @tanstack/react-query
- Axios
- Tailwind CSS
- Framer Motion

## Getting Started

### Install dependencies

From the `frontend/` folder:

```bash
npm install
```

### Run dev server

```bash
npm run dev
```

By default, Vite runs at:

- `http://localhost:5173`

## Scripts

- `npm run dev` — start dev server
- `npm run build` — production build
- `npm run preview` — preview production build locally
- `npm run lint` — run ESLint

## Backend connectivity

The backend CORS is configured to allow the frontend dev origin:

- `http://localhost:5173`

Typical backend URL during development:

- `http://localhost:8000`

If you use Axios, consider setting a single API base URL (env-based) such as:
- `VITE_API_BASE_URL=http://localhost:8000/api/v1`

## UI Entry Point

- Main component: `src/App.jsx`
- App currently renders the title and is ready for route/pages integration.
