# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Flask application designed for deployment on Railway. It serves job listings from a Postgres database and provides a REST API to access them. Users can track which jobs they've applied to using browser local storage.

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
  - `jobs.html` - Job listings page with card-based layout (clickable cards)
  - `job_detail.html` - Individual job details page with full information

### Database

- **Connection**: Uses `DATABASE_URL` environment variable for Postgres connection
- **Table**: `job_postings` - contains job listing data
- **Driver**: psycopg2-binary for Postgres connectivity

### Routes

**Web UI Routes:**
- `GET /` - Home page with welcome message and features
- `GET /jobs` - Job listings page with HTML UI (all jobs)
- `GET /jobs/<job_id>` - Individual job details page

**API Routes:**
- `GET /api/jobs` - Returns all job postings as JSON
  - Returns JSON: `{"jobs": [...], "count": n}`
  - Orders by id

### Application Tracking

The app includes client-side application tracking using browser localStorage:

- **Storage**: Job IDs are stored in `localStorage` under key `appliedJobs` as a JSON array
- **Jobs List Page**: Shows "Mark as Applied" button on each job card
  - Applied jobs show green "✓ Applied" badge instead
  - Click to toggle application status
- **Job Details Page**: Shows application status with larger badge
  - "Mark as Applied" button if not applied
  - "Remove Application" button if already applied
- **Persistence**: Application status persists across sessions in the same browser
- **Privacy**: All data stored locally in browser, not on server

## Environment Variables

- `DATABASE_URL` - Postgres connection string (required for database operations)
- `PORT` - Server port (default: 5000)

## Deployment

Configured for Railway deployment via `railway.json`:
- Uses Nixpacks builder
- Starts with `gunicorn main:app`
- Restarts on failure (max 10 retries)
- DATABASE_URL should be set in Railway environment variables
