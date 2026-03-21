# LLM-PDDL Automation Backend

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the FastAPI server:
```bash
python main.py
```

Or use uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### GET /api/config
Get available configuration options (models, domains, tasks)

### POST /api/run-pipeline
Start a new pipeline run

**Request Body:**
```json
{
  "model": "qwen2.5:7b-instruct",
  "temperature": 0.5,
  "domain": "barman",
  "task_id": 0,
  "run_id": "run1"
}
```

**Response:**
```json
{
  "job_id": "uuid-here",
  "status": "pending",
  "message": "Pipeline started successfully"
}
```

### GET /api/status/{job_id}
Get the status of a running or completed job

### GET /api/jobs
Get list of all jobs

### DELETE /api/jobs/{job_id}
Delete a job from history

### GET /api/health
Health check endpoint

## Testing the API

You can test the API using curl:

```bash
# Get configuration
curl http://localhost:8000/api/config

# Start a pipeline run
curl -X POST http://localhost:8000/api/run-pipeline \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5:7b-instruct",
    "temperature": 0.5,
    "domain": "barman",
    "task_id": 0,
    "run_id": "run1"
  }'

# Check job status (replace JOB_ID with actual ID)
curl http://localhost:8000/api/status/JOB_ID

# Get all jobs
curl http://localhost:8000/api/jobs
```
