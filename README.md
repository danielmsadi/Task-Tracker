# Module 1 Task Tracker API

A minimal learning-project REST API built with **Python**, **FastAPI**, and **Pydantic**.

## Project Description

This is the backend skeleton for the Module 1 Task Tracker, a single-shared-list
task tracking application. Per ADR-001, task data will be stored in a local JSON
file at `backend/data/tasks.json` rather than a production database.

This skeleton intentionally excludes:
- Authentication / user accounts / multi-tenancy
- Real-time updates
- Mobile app
- Notifications
- Production database
- Docker / cloud deployment setup
- Frontend files
- CRUD endpoints (to be added in a later step)

Currently, only a `/health` endpoint is implemented to verify the API is running.

## Project Structure

task-tracker/
├── README.md
└── backend/
├── .env.example
├── .gitignore
├── requirements.txt
├── app/
│   ├── init.py
│   └── main.py
└── data/
└── tasks.json

## Setup Instructions

1. Navigate to the backend folder:
```bash
   cd backend
```

2. Create a virtual environment:
```bash
   python -m venv venv
```

3. Activate the virtual environment:

   **Linux/macOS:**
```bash
   source venv/bin/activate
```

   **Windows (PowerShell):**
```powershell
   venv\Scripts\Activate.ps1
```

4. Install dependencies:
```bash
   pip install -r requirements.txt
```

5. Copy the example environment file:

   **Linux/macOS:**
```bash
   cp .env.example .env
```

   **Windows (PowerShell):**
```powershell
   Copy-Item .env.example .env
```

## Running the Server

From the `backend` folder, with the virtual environment activated:

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://127.0.0.1:8000`.

## Testing the Health Endpoint

```bash
curl http://127.0.0.1:8000/health
```

Expected response shape:
```json
{
  "status": "ok",
  "timestamp": "2026-06-30T12:34:56.789012+00:00"
}
```

## API Documentation (Swagger)

Once the server is running, open the following URL in your browser: