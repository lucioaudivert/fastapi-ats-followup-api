# fastapi-ats-followup-api

A lightweight ATS follow-up tracker built with FastAPI, SQLModel, and SQLite. It demonstrates clean API design, basic persistence, tests, and Docker packaging.

Public sanitized portfolio sample; production work is under NDA.

## Features
- Candidate + follow-up tracking
- SQLite persistence (easy to switch to Postgres)
- Filtered listing by stage or search query
- Clean service layer and tests

## Project Structure
```
app/
  main.py
  db.py
  models.py
  schemas.py
  services.py
  settings.py
tests/
  test_api.py
  test_services.py
```

## Run Locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

## Run Tests
```bash
pytest
```

## Run with Docker
```bash
docker build -t fastapi-ats-followup-api:latest .
docker run --rm -p 8000:8000 fastapi-ats-followup-api:latest
```

## Environment Variables
- `ATS_DATABASE_URL` (default: `sqlite:///./app.db`)
- `ATS_LOG_LEVEL` (default: `INFO`)

## API Examples
### Health Check
```bash
curl http://localhost:8000/health
```

### Create Candidate
```bash
curl -X POST http://localhost:8000/candidates \
  -H "Content-Type: application/json" \
  -d '{"name":"Ana Lopez","email":"ana@example.com","stage":"sourced"}'
```

### List Candidates
```bash
curl http://localhost:8000/candidates
curl "http://localhost:8000/candidates?stage=hired"
curl "http://localhost:8000/candidates?q=ana"
```

### Candidate Detail
```bash
curl http://localhost:8000/candidates/1
```

### Create Follow-up
```bash
curl -X POST http://localhost:8000/candidates/1/followups \
  -H "Content-Type: application/json" \
  -d '{"message":"Sent a reminder","channel":"email"}'
```

### List Follow-ups
```bash
curl http://localhost:8000/candidates/1/followups
```
