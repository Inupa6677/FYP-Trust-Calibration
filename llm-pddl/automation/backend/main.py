"""
FastAPI Server for Pipeline Automation
Provides REST API endpoints for running and monitoring the pipeline
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List
import uuid
from datetime import datetime
import asyncio
from pathlib import Path

from pipeline_orchestrator import PipelineRunner, PipelineStatus
from config import (
    AVAILABLE_MODELS, AVAILABLE_DOMAINS, DOMAIN_TASK_MAPPING,
    TEMPERATURE_MIN, TEMPERATURE_MAX, PIPELINE_METHOD
)

# Initialize FastAPI app
app = FastAPI(
    title="LLM-PDDL Pipeline API",
    description="API for automated workflow plan generation and evaluation",
    version="1.0.0"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory job storage (in production, use a database)
jobs: Dict[str, Dict] = {}


# ============================================================================
# Request/Response Models
# ============================================================================

class PipelineRequest(BaseModel):
    """Request model for starting a pipeline run"""
    model: str
    temperature: float
    domain: str
    task_id: int
    run_id: str = "run1"


class PipelineResponse(BaseModel):
    """Response model for pipeline submission"""
    job_id: str
    status: str
    message: str


class LogMessage(BaseModel):
    """Structured log message"""
    timestamp: str
    level: str
    message: str


class JobStatus(BaseModel):
    """Job status response model"""
    job_id: str
    status: str
    current_step: Optional[str]
    domain: str
    task_id: int
    plan_num: str
    model: str
    temperature: float
    run_id: str
    progress: int
    logs: List[str]
    messages: List[LogMessage]
    results: Dict
    start_time: Optional[str]
    end_time: Optional[str]
    duration: Optional[float]


class ConfigResponse(BaseModel):
    """Configuration response model"""
    models: List[str]
    domains: List[str]
    domain_tasks: Dict[str, List[int]]
    temperature_min: float
    temperature_max: float
    method: str


# ============================================================================
# Helper Functions
# ============================================================================

def parse_log_messages(logs: List[str]) -> List[Dict]:
    """Parse log strings into structured messages"""
    import re
    messages = []
    
    for log in logs:
        # Parse format: [2026-02-15 10:22:55] [INFO] Message
        match = re.match(r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] \[(\w+)\] (.+)', log)
        if match:
            messages.append({
                "timestamp": match.group(1),
                "level": match.group(2),
                "message": match.group(3)
            })
        else:
            # Fallback for unparseable logs
            messages.append({
                "timestamp": "",
                "level": "INFO",
                "message": log
            })
    
    return messages


def calculate_progress(status: str, current_step: Optional[str]) -> int:
    """Calculate progress percentage based on current step"""
    if status == PipelineStatus.COMPLETED:
        return 100
    if status == PipelineStatus.FAILED:
        return -1
    if status == PipelineStatus.PENDING:
        return 0
    
    # Map steps to progress percentages
    step_progress = {
        "generate_pddl": 20,
        "generate_plan": 40,
        "validate_plan": 60,
        "generate_optimal": 80,
        "calculate_gap": 90
    }
    return step_progress.get(current_step, 0)


async def run_pipeline_async(job_id: str, request: PipelineRequest):
    """Run the pipeline asynchronously in the background"""
    try:
        # Update job status to running
        jobs[job_id]["status"] = PipelineStatus.RUNNING
        jobs[job_id]["start_time"] = datetime.now().isoformat()
        
        # Create pipeline runner
        runner = PipelineRunner(
            model=request.model,
            temperature=request.temperature,
            domain=request.domain,
            task_id=request.task_id,
            run_id=request.run_id
        )
        
        # Store runner reference
        jobs[job_id]["runner"] = runner
        
        # Run the pipeline (this is blocking but runs in background task)
        result = runner.run()
        
        # Update job with results
        jobs[job_id]["status"] = result["status"]
        jobs[job_id]["results"] = result["results"]
        jobs[job_id]["logs"] = result["logs"]
        jobs[job_id]["end_time"] = datetime.now().isoformat()
        jobs[job_id]["duration"] = result["duration"]
        
    except Exception as e:
        jobs[job_id]["status"] = PipelineStatus.FAILED
        jobs[job_id]["logs"].append(f"ERROR: {str(e)}")
        jobs[job_id]["end_time"] = datetime.now().isoformat()


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": "LLM-PDDL Pipeline API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "config": "/api/config",
            "run": "/api/run-pipeline",
            "status": "/api/status/{job_id}",
            "jobs": "/api/jobs"
        }
    }


@app.get("/api/config", response_model=ConfigResponse)
async def get_config():
    """Get available configuration options"""
    return {
        "models": AVAILABLE_MODELS,
        "domains": AVAILABLE_DOMAINS,
        "domain_tasks": DOMAIN_TASK_MAPPING,
        "temperature_min": TEMPERATURE_MIN,
        "temperature_max": TEMPERATURE_MAX,
        "method": PIPELINE_METHOD
    }


@app.post("/api/run-pipeline", response_model=PipelineResponse)
async def run_pipeline(request: PipelineRequest, background_tasks: BackgroundTasks):
    """
    Start a new pipeline run
    
    Args:
        request: Pipeline configuration (model, temperature, domain, task_id)
        background_tasks: FastAPI background tasks
        
    Returns:
        Job ID and status
    """
    # Validate inputs
    if request.model not in AVAILABLE_MODELS:
        raise HTTPException(status_code=400, detail=f"Invalid model: {request.model}")
    
    if request.domain not in AVAILABLE_DOMAINS:
        raise HTTPException(status_code=400, detail=f"Invalid domain: {request.domain}")
    
    if request.task_id not in DOMAIN_TASK_MAPPING[request.domain]:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid task_id {request.task_id} for domain {request.domain}"
        )
    
    if not (TEMPERATURE_MIN <= request.temperature <= TEMPERATURE_MAX):
        raise HTTPException(
            status_code=400,
            detail=f"Temperature must be between {TEMPERATURE_MIN} and {TEMPERATURE_MAX}"
        )
    
    # Generate unique job ID
    job_id = str(uuid.uuid4())
    
    # Initialize job entry
    jobs[job_id] = {
        "job_id": job_id,
        "status": PipelineStatus.PENDING,
        "current_step": None,
        "domain": request.domain,
        "task_id": request.task_id,
        "plan_num": f"p{str(request.task_id + 1).zfill(2)}",
        "model": request.model,
        "temperature": request.temperature,
        "run_id": request.run_id,
        "logs": [],
        "results": {},
        "start_time": None,
        "end_time": None,
        "duration": None,
        "runner": None
    }
    
    # Add pipeline run to background tasks
    background_tasks.add_task(run_pipeline_async, job_id, request)
    
    return {
        "job_id": job_id,
        "status": PipelineStatus.PENDING,
        "message": "Pipeline started successfully"
    }


@app.get("/api/status/{job_id}", response_model=JobStatus)
async def get_status(job_id: str):
    """
    Get the status of a pipeline job
    
    Args:
        job_id: Unique job identifier
        
    Returns:
        Current job status and progress
    """
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    
    # Get current step and logs from runner if available (for real-time updates)
    current_step = None
    logs = job["logs"]
    results = job["results"]
    
    if job["runner"]:
        current_step = job["runner"].current_step
        # Use runner's logs for real-time updates
        logs = job["runner"].logs if job["runner"].logs else job["logs"]
        # Use runner's results for incremental updates
        results = job["runner"].results if job["runner"].results else job["results"]
    
    # Parse logs into structured messages
    messages = parse_log_messages(logs)
    
    return {
        "job_id": job["job_id"],
        "status": job["status"],
        "current_step": current_step,
        "domain": job["domain"],
        "task_id": job["task_id"],
        "plan_num": job["plan_num"],
        "model": job["model"],
        "temperature": job["temperature"],
        "run_id": job["run_id"],
        "progress": calculate_progress(job["status"], current_step),
        "logs": logs,
        "messages": messages,
        "results": results,
        "start_time": job["start_time"],
        "end_time": job["end_time"],
        "duration": job["duration"]
    }


@app.get("/api/jobs")
async def get_all_jobs():
    """Get list of all jobs"""
    return {
        "total": len(jobs),
        "jobs": [
            {
                "job_id": job_id,
                "status": job["status"],
                "domain": job["domain"],
                "task_id": job["task_id"],
                "model": job["model"],
                "temperature": job["temperature"],
                "start_time": job["start_time"]
            }
            for job_id, job in jobs.items()
        ]
    }


@app.delete("/api/jobs/{job_id}")
async def delete_job(job_id: str):
    """Delete a job from history"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    del jobs[job_id]
    return {"message": "Job deleted successfully"}


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_jobs": len([j for j in jobs.values() if j["status"] == PipelineStatus.RUNNING])
    }


# ============================================================================
# Startup/Shutdown Events
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Run on server startup"""
    print("=" * 60)
    print("LLM-PDDL Pipeline API Server Starting...")
    print("=" * 60)
    print(f"Available Models: {AVAILABLE_MODELS}")
    print(f"Available Domains: {AVAILABLE_DOMAINS}")
    print(f"API Docs: http://localhost:8000/docs")
    print("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """Run on server shutdown"""
    print("\nShutting down LLM-PDDL Pipeline API Server...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
