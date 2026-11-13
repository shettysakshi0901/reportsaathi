# Backend FastAPI Application

## Overview
- FastAPI application exposing health and value endpoints.
- Uses SQLAlchemy with a SQLite default; can be configured via `DATABASE_URL`.
- Dockerized for deployment.

## Project Structure
```
backend/
├─ app/
│  ├─ __init__.py
│  ├─ main.py
│  ├─ routers/
│  │   ├─ __init__.py
│  │   ├─ health.py
│  │   └─ value.py
│  ├─ models/
│  │   ├─ __init__.py
│  │   ├─ database.py
│  │   └─ value.py
│  └─ shared/   # place for shared utilities
├─ tests/
│  ├─ __init__.py
│  ├─ conftest.py
│  ├─ test_health.py
│  └─ test_value.py
├─ pyproject.toml
├─ Dockerfile
└─ poetry.lock  (generated after `poetry install`)
```