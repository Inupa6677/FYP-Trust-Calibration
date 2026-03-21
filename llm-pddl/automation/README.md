# LLM-PDDL Automated Pipeline

Complete automation system with React frontend and FastAPI backend for running the LLM-PDDL workflow planning pipeline.

## 📁 Project Structure

```
automation/
├── backend/               # FastAPI server
│   ├── main.py           # API endpoints
│   ├── config.py         # Configuration
│   ├── pipeline_orchestrator.py  # Core automation logic
│   ├── requirements.txt  # Python dependencies
│   └── README.md
└── frontend/             # React application
    ├── src/
    │   ├── components/   # React components
    │   ├── api/         # API client
    │   ├── App.jsx      # Main app component
    │   └── App.css      # Styles
    ├── package.json
    └── README.md
```

## 🚀 Quick Start

### 1. Start the Backend Server

```bash
cd automation/backend
python -m pip install -r requirements.txt
python main.py
```

The API will be available at **http://localhost:8000**
- API Docs: http://localhost:8000/docs

### 2. Start the Frontend

```bash
cd automation/frontend
npm install
npm run dev
```

The UI will be available at **http://localhost:5173**

## 💻 Using the Web Interface

1. **Select LLM Model** - Choose from available Ollama models
2. **Set Temperature** - Adjust creativity (0.0 = deterministic, 1.0 = creative)
3. **Choose Domain** - Select planning domain (barman, blocksworld, etc.)
4. **Pick Task** - Choose a specific task from the domain
5. **Set Run ID** - Specify the run identifier (default: run1)
6. **Click "Run Pipeline"** - Start the automated workflow

The interface will show real-time progress through all 5 pipeline steps:
- 📝 Generating PDDL Problem
- 🔧 Generating Plan (Fast Downward)
- ✅ Validating Plan (VAL)
- 🎯 Generating Optimal Plan
- 📊 Calculating Optimal Gap

## 📊 Pipeline Steps

Each pipeline run automatically executes:

1. **PDDL Generation** - LLM generates problem specification
2. **Plan Generation** - Fast Downward creates plan (lama-first)
3. **Plan Validation** - VAL validates plan correctness
4. **Optimal Plan** - Fast Downward generates optimal plan (seq-opt-lmcut)
5. **Gap Calculation** - Computes optimality gap metric

## 🔧 Configuration

### Domain-Task Mappings

The system includes pre-configured tasks for each domain:

- **Barman**: Tasks 0, 2, 3, 4, 5
- **Blocksworld**: Tasks 4, 7, 11, 12, 17
- **Floortile**: Tasks 3, 4, 5, 6, 7
- **Grippers**: Tasks 1, 2, 3, 6, 7
- **Storage**: Tasks 2, 3, 4, 5, 6

### Available Models

- qwen2.5:7b-instruct
- llama2:7b
- mistral:7b

## 📝 API Reference

### GET /api/config
Returns available models, domains, and task mappings

### POST /api/run-pipeline
Starts a new pipeline run

**Request:**
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
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "message": "Pipeline started successfully"
}
```

### GET /api/status/{job_id}
Get real-time status of a running job

### GET /api/jobs
List all jobs

## 🛠️ Development

### Backend Development

```bash
cd automation/backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
cd automation/frontend
npm run dev
```

## 📦 Prerequisites

- Python 3.8+
- Node.js 16+
- WSL (for Windows users)
- Ollama with models installed
- Fast Downward compiled

## 🧪 Testing

Test the backend API:
```bash
curl http://localhost:8000/api/config
```

Test a pipeline run:
```bash
curl -X POST http://localhost:8000/api/run-pipeline \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5:7b-instruct",
    "temperature": 0.5,
    "domain": "barman",
    "task_id": 0,
    "run_id": "run1"
  }'
```

## 📄 License

Part of the LLM-PDDL research project.
