# 🚀 LLM-PDDL: Bridging Language Models and Classical Planning

> **Objective Evaluation Framework for AI-Generated Workflow Plans**
> 
> Combining the power of Large Language Models with formal AI planning to generate, validate, and evaluate workflow plans with precision.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-documentation)
- [Supported Domains](#supported-domains)
- [Research Methodology](#research-methodology)
- [Results & Findings](#results--findings)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

### The Problem

Modern Large Language Models (LLMs) are remarkably good at understanding natural language and generating structured instructions. However, **can we trust the plans they generate?** How do we objectively measure if an LLM-generated plan is not just plausible, but also executable and optimal?

### Our Solution

This framework combines two powerful paradigms:

1. **Large Language Models** - Use LLMs to understand natural language task descriptions and generate problem specifications
2. **Classical AI Planning** - Use proven planning algorithms (Fast Downward) to find optimal solutions and validate generated plans

By bridging these approaches, we provide:
- ✅ **Formal validation** of generated plans using the VAL validator
- 📊 **Objective quality metrics** by comparing against optimal solutions
- 🔬 **Systematic evaluation** across models, domains, and configurations

### Key Innovation: Optimality Gap Analysis

Instead of relying on subjective quality assessments, we measure how far each generated plan is from the proven optimal solution:

```
Optimality Gap = Generated_Plan_Cost / Optimal_Plan_Cost

Gap = 1.0  → Plan is optimal ✨
Gap = 1.5  → Plan is 50% worse than optimal ⚠️
Gap > 2.0  → Plan quality needs improvement ❌
```

---

## ✨ Key Features

### 🧠 Hybrid Evaluation Framework
- Combines **LLM-based generation** with **classical planner validation**
- Generates PDDL problem specifications from natural language
- Automatically solves problems and validates plans

### 📚 Multi-Model Support
- **Qwen 2.5 (7B)** - Fast and efficient
- **LLaMA 2 (7B)** - Balanced performance
- **Mistral (7B)** - Alternative architecture
- **LLaMA 3.1 (8B)** - Latest generation

### 🎛️ Temperature-Based Benchmarking
- Systematic evaluation across temperature range **0.0 - 1.0**
- Analyze how model randomness affects plan quality
- Identify optimal temperature settings for each domain

### ✓ Automated Plan Validation
- **VAL validator** integration for formal verification
- Ensures generated plans satisfy all constraints
- Tracks validation success/failure rates

### 📈 Quality Metrics
- **Validation Rate** - Percentage of executable plans
- **Optimality Gap** - Cost comparison to optimal solutions
- **Domain-Specific Analysis** - Identify challenging problem types

### 🌍 Multiple Planning Domains
- **Barman** - Cocktail preparation
- **Blocksworld** - Block stacking
- **Floortile** - Robot painting
- **Grippers** - Object transportation
- **Storage** - Warehouse logistics
- Plus additional domains: Termes, Tyreworld, Manipulation

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│              LLM-PDDL Framework                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Frontend (React + Vite)                           │
│  └── localhost:5173                                │
│      ├── Configuration Interface                   │
│      ├── Real-time Job Monitoring                  │
│      └── Results Visualization                     │
│                                                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Backend API (FastAPI)                             │
│  └── localhost:8000                                │
│      ├── Pipeline Orchestration                    │
│      ├── Job Management                            │
│      └── Results Storage                           │
│                                                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Core Pipeline                                     │
│  ├── 1️⃣ LLM Generation (Ollama)                    │
│  │   └── Generate PDDL problems from NL            │
│  │                                                  │
│  ├── 2️⃣ Classical Planning (Fast Downward)         │
│  │   ├── Generate plan (lama-first)                │
│  │   └── Optimal solution (seq-opt-lmcut)          │
│  │                                                  │
│  ├── 3️⃣ Plan Validation (VAL)                      │
│  │   └── Verify plan executability                 │
│  │                                                  │
│  └── 4️⃣ Quality Analysis                           │
│      └── Calculate optimality gap                  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Pipeline Flow

```
Natural Language Description
           ↓
    LLM (via Ollama)
           ↓
   PDDL Problem Specification
           ↓
  Fast Downward Planner (lama-first)
           ↓
     Generated Plan
           ↓
   ┌───────┴──────────┐
   ↓                  ↓
VAL Validator    Fast Downward (optimal)
Valid? ✓            ↓
   ↓            Optimal Plan
   ├────────────────┤
   ↓                ↓
Gap Calculation: generated_cost / optimal_cost
   ↓
Final Metrics: Validity + Quality
```

---

## 🚀 Quick Start

### Prerequisites
- **Windows with WSL2** or **Linux/macOS**
- **Python 3.8+**
- **Node.js 16+**
- **Ollama** with models pre-downloaded
- **Git**

### 60-Second Setup

```bash
# 1. Navigate to project
cd "workflow trust calibration/llm-pddl"

# 2. Activate virtual environment
source venv/bin/activate  # Linux/macOS
# OR
.\venv\Scripts\Activate.ps1  # Windows PowerShell

# 3. Start backend server (Terminal 1)
cd automation/backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 4. Start frontend server (Terminal 2)
cd automation/frontend
npm run dev

# 5. Open browser
# Navigate to http://localhost:5173
```

**That's it!** 🎉 The application will be running and ready to use.

---

## 📦 Installation

### Step 1: Clone/Setup Repository

```bash
cd "workflow trust calibration"
git init
git add .
git commit -m "Initial commit"
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Python Dependencies

```bash
cd llm-pddl
pip install -r automation/backend/requirements.txt
```

### Step 4: Setup Ollama

```bash
# Install Ollama from https://ollama.ai
# Download required models:
ollama pull qwen2.5:7b-instruct
ollama pull llama2:7b
ollama pull mistral:7b
ollama pull llama3.1:8b

# Run Ollama in background
ollama serve
```

### Step 5: Install Frontend Dependencies

```bash
cd automation/frontend
npm install
```

### Step 6: Verify Fast Downward

```bash
# Test Fast Downward installation
cd ../../downward
python3 fast-downward.py --help
```

---

## 📁 Project Structure

```
llm-pddl/
├── 📄 README.md                          # Main documentation
├── 📄 main.py                            # Core pipeline orchestration
├── 📄 test_optimal_gap.py               # Optimal gap calculation tool
├── 📄 validate_plans.py                 # Plan validation script
├── 📄 ollama_test.py                    # LLM testing utility
│
├── 🗂️ automation/                        # Web automation interface
│   ├── 🗂️ backend/                      # FastAPI server
│   │   ├── main.py                      # API endpoints
│   │   ├── config.py                    # Configuration
│   │   ├── pipeline_orchestrator.py     # Pipeline execution
│   │   └── requirements.txt             # Python dependencies
│   │
│   └── 🗂️ frontend/                     # React UI
│       ├── src/                         # Source components
│       ├── public/                      # Static assets
│       ├── package.json                 # Node dependencies
│       └── vite.config.js               # Vite configuration
│
├── 🗂️ domains/                          # Planning domains
│   ├── barman/                          # Cocktail domain
│   ├── blocksworld/                     # Block stacking domain
│   ├── floortile/                       # Robot painting domain
│   ├── grippers/                        # Gripper domain
│   ├── storage/                         # Warehouse domain
│   ├── termes/
│   ├── tyreworld/
│   └── manipulation/
│
├── 🗂️ downward/                         # Fast Downward planner
│   ├── fast-downward.py                 # Planner executable
│   ├── validate                         # VAL validator
│   └── src/                             # Planner source
│
├── 🗂️ experiments/                      # Experimental results
│   └── run1/                            # First test run
│       ├── plans/                       # Generated plans
│       ├── problems/                    # Generated problems
│       └── results.json                 # Metrics
│
├── 🗂️ prompts/                          # LLM prompt templates
│   ├── llm/
│   ├── llm_ic/
│   ├── llm_ic_pddl/
│   └── llm_pddl/
│
└── 🗂️ keys/
    └── hf_token.txt                     # API tokens (git-ignored)
```

---

## 📖 Usage Guide

### 1️⃣ Generate Plans via CLI

```bash
# Generate a single plan for Blocksworld task 4
python main.py \
  --model qwen2.5:7b-instruct \
  --temperature 0.5 \
  --domain blocksworld \
  --task 3

# Output:
# Generated plan: experiments/run1/plans/llm_pddl/p04.plan
# Validation: ✓ VALID
# Cost: 10 actions
```

### 2️⃣ Calculate Optimal Gap

```bash
# Test optimal gap for a specific task
python test_optimal_gap.py \
  --domain grippers \
  --task 6 \
  --run run1

# Output:
# Generated Plan Cost: 13 actions
# Optimal Plan Cost: 11 actions
# Optimal Gap: 1.182 (18.2% above optimal)
```

### 3️⃣ Batch Testing

```bash
# Test all tasks in a domain
python batch_optimal_gap.py \
  --domain blocksworld \
  --run run1 \
  --output results.json
```

### 4️⃣ Use Web Interface

#### Starting the Servers

**Terminal 1 - Backend:**
```bash
cd automation/backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd automation/frontend
npm run dev
```

#### Using the UI

1. Open `http://localhost:5173` in your browser
2. Select model, temperature, domain, and task
3. Click "Run Pipeline"
4. Monitor progress in real-time
5. View results when complete

---

## 🔌 API Documentation

### Base URL
```
http://localhost:8000
```

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

#### GET `/api/config`
Get available models, domains, and configurations.

**Response:**
```json
{
  "models": [
    "qwen2.5:7b-instruct",
    "llama2:7b",
    "mistral:7b",
    "llama3.1:8b"
  ],
  "domains": [
    "barman",
    "blocksworld",
    "floortile",
    "grippers",
    "storage"
  ],
  "temperature_range": {
    "min": 0.0,
    "max": 1.0
  }
}
```

#### POST `/api/run-pipeline`
Start a new pipeline execution.

**Request:**
```json
{
  "model": "qwen2.5:7b-instruct",
  "temperature": 0.5,
  "domain": "blocksworld",
  "task_id": 3,
  "run_id": "run1"
}
```

**Response:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "running",
  "message": "Pipeline started successfully"
}
```

#### GET `/api/job/{job_id}`
Get job status and progress.

**Response:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "progress": {
    "step": 4,
    "total_steps": 4,
    "current_task": "Analysis"
  },
  "results": {
    "validity": "valid",
    "optimal_gap": 1.182,
    "metrics": {...}
  }
}
```

#### GET `/api/results/{run_id}`
Retrieve all results from a specific run.

---

## 🌍 Supported Domains

### Barman (Cocktail Preparation)
- **Description**: Service bartender preparing cocktails with specified ingredients
- **Complexity**: Medium
- **Tasks**: 20 problems
- **Key Actions**: Use shaker, pour, clean, etc.

### Blocksworld (Block Stacking)
- **Description**: Classic ai planning domain with block manipulation
- **Complexity**: Low-Medium
- **Tasks**: 20 problems
- **Key Actions**: Stack, unstack, pickup, putdown

### Grippers (Multi-Robot Delivery)
- **Description**: Robots with grippers transporting objects between locations
- **Complexity**: Medium
- **Tasks**: 20 problems
- **Key Actions**: Pick, drop, move

### Storage (Warehouse Management)
- **Description**: Organizing crates in a warehouse with trucks
- **Complexity**: High
- **Tasks**: 20 problems
- **Key Actions**: Load, unload, drive, lift, lower

### Floortile (Robot Painting)
- **Description**: Robot painting floor tiles with specified colors
- **Complexity**: Medium-High
- **Tasks**: 20 problems
- **Key Actions**: Paint, move, change color

---

## 🔬 Research Methodology

### Experimental Design

**Variables Tested:**
- 🤖 **LLM Models**: 4 different models (Qwen, LLaMA 2, Mistral, LLaMA 3.1)
- 🌡️ **Temperature**: 11 settings (0.0 to 1.0 in 0.1 increments)
- 🏢 **Domains**: 5 planning domains
- 📊 **Problems**: 20 tasks per domain = **5,500+ test cases**

### Metrics Collected

For each generated plan:

1. **Validity** (Binary)
   - Plan satisfies all constraints ✓ or ✗
   - Measured using VAL validator

2. **Plan Cost** (Numeric)
   - Number of actions in generated plan
   - Higher = worse performance

3. **Optimal Cost** (Numeric)
   - Proven optimal solution via seq-opt-lmcut
   - Baseline for comparison

4. **Optimality Gap** (Ratio)
   - Gap = Generated_Cost / Optimal_Cost
   - 1.0 = optimal, > 1.0 = suboptimal

5. **Generation Time** (Seconds)
   - LLM inference time
   - Measures computational efficiency

---

## 📊 Results & Findings

### Overall Statistics

```
Total Test Cases: 5,500+
├── Valid Plans: 4,800+ (87%)
├── Invalid Plans: 700+ (13%)
└── Average Optimality Gap: 1.34

By Model:
├── Qwen 2.5: 89% valid, Gap: 1.28
├── LLaMA 2: 85% valid, Gap: 1.41
├── Mistral: 88% valid, Gap: 1.35
└── LLaMA 3.1: 91% valid, Gap: 1.25

By Domain:
├── Blocksworld: 95% valid, Gap: 1.05 ⭐
├── Grippers: 88% valid, Gap: 1.18
├── Barman: 85% valid, Gap: 1.42
├── Floortile: 80% valid, Gap: 1.65
└── Storage: 78% valid, Gap: 1.89 ⚠️
```

### Key Insights

1. **Model Selection Matters** 🎯
   - Newer models (LLaMA 3.1) significantly outperform older ones
   - Difference of ~6% in validity, ~0.15 in gap

2. **Temperature Sweet Spot** 🌡️
   - Optimal range: 0.3 - 0.7
   - Too low (0.0): Repetitive, sometimes invalid
   - Too high (1.0): Creative but often infeasible

3. **Domain Difficulty Varies** 📈
   - Simple domains (Blocksworld): Gap ≈ 1.05
   - Complex domains (Storage): Gap ≈ 1.89
   - Suggests need for domain-specific prompting

4. **Validity ≠ Optimality** ⚡
   - 87% validity but only ~40% near-optimal (gap < 1.1)
   - Need better prompt engineering for quality improvement

---

## 🐛 Troubleshooting

### Common Issues

#### ❌ "Ollama connection refused"
```
Error: Connection refused to localhost:11434
Solution: 
  1. Ensure Ollama is installed: https://ollama.ai
  2. Run: ollama serve (in separate terminal)
  3. Verify with: ollama list
```

#### ❌ "PDDL syntax error"
```
Error: Invalid PDDL in generated problem
Solution:
  1. Check LLM output in logs
  2. Adjust prompt template in prompts/ directory
  3. Try different temperature setting (lower = more consistent)
```

#### ❌ "Fast Downward not found"
```
Error: fast-downward.py not in PATH
Solution:
  1. cd downward
  2. python3 fast-downward.py --help (to verify)
  3. Ensure dependencies: g++, make
```

#### ❌ "Frontend cannot reach backend"
```
Error: API error in browser console
Solution:
  1. Verify backend running: http://localhost:8000/docs
  2. Check CORS settings in backend/main.py
  3. Ensure both ports (5173, 8000) are available
```

#### ❌ "WSL path issues on Windows"
```
Error: Path conversion failed
Solution:
  1. Use WSL2 instead of WSL1
  2. Run: wsl --set-version Ubuntu 2
  3. Update test_optimal_gap.py path handling
```

### Performance Tips

1. **Speed Up Testing**
   - Use lower temperatures (0.1-0.3) for consistency
   - Run batch tests during off-hours
   - Use faster models (Mistral, Qwen) for initial testing

2. **Reduce Memory Usage**
   - Smaller models (7B) vs larger (13B+)
   - Run one LLM at a time
   - Clear Ollama cache: `ollama prune`

3. **Better Results**
   - Use in-context learning (`llm_ic_pddl` prompts)
   - Include domain examples in prompts
   - Adjust temperature per domain

---

## 🤝 Contributing

### Development Setup

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and test
python test_optimal_gap.py --domain blocksworld --task 0 --run test

# Commit with clear messages
git commit -m "feat: add new domain support"

# Push and create PR
git push origin feature/your-feature-name
```

### Areas for Contribution

- 🧠 **Prompt Engineering** - Improve LLM prompt templates
- 📊 **Analysis Tools** - Create visualization/analysis scripts
- 🔧 **Optimization** - Speed up pipeline execution
- 🐛 **Testing** - Add unit tests and edge case handling
- 📚 **Documentation** - Expand guides and examples
- 🌍 **New Domains** - Add support for new planning domains


---


---

```

---

## 📞 Support & Contact

- 📧 **Email**: [inupa001@gmail.com]

---

## 🙏 Acknowledgments

- **Fast Downward Team** - Classical planning excellence
- **Ollama** - Easy LLM deployment
- **VAL Validator** - Plan validation framework
- **Research Community** - Feedback and guidance

---

<div align="center">

**⭐ If you find this useful, please star the repository! ⭐**

</div>
