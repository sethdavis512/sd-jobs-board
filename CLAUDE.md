# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Flask application designed for deployment on Railway. It serves job listings from a Postgres database and provides a REST API to access them.

## Development Commands

### Setup
```bash
pip install -r requirements.txt
```

### Running the Application
```bash
# Development (runs on port 5000 by default, configurable via PORT env var)
python3 main.py
```

### Production
```bash
# Production server (used by Railway)
gunicorn main:app
```

## Architecture

- **main.py**: Single-file Flask application entry point
  - Contains Flask app instance and route definitions
  - Reads PORT from environment variable (defaults to 5000)
  - Debug mode enabled for local development
  - Database connection via `get_db_connection()` function

- **templates/**: HTML templates for the web UI
  - `base.html` - Base template with header, nav, and footer
  - `index.html` - Home page with hero section
  - `jobs.html` - Job listings page with card-based layout

### Database

- **Connection**: Uses `DATABASE_URL` environment variable for Postgres connection
- **Table**: `job_postings` - contains job listing data
- **Driver**: psycopg2-binary for Postgres connectivity

### Routes

**Web UI Routes:**
- `GET /` - Home page with welcome message and features
- `GET /jobs` - Job listings page with HTML UI

**API Routes:**
- `GET /api/jobs` - Returns all job postings as JSON
  - Returns JSON: `{"jobs": [...], "count": n}`
  - Orders by id

## Environment Variables

- `DATABASE_URL` - Postgres connection string (required for database operations)
- `PORT` - Server port (default: 5000)

## Deployment

Configured for Railway deployment via `railway.json`:
- Uses Nixpacks builder
- Starts with `gunicorn main:app`
- Restarts on failure (max 10 retries)
- DATABASE_URL should be set in Railway environment variables
