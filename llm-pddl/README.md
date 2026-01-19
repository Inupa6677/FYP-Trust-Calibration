# LLM-PDDL: Trust Calibration in LLM-Assisted Workflow Planning

## Overview

This repository contains the experimental framework developed for research on **Trust Calibration in LLM-Assisted Workflow Planning**. The system evaluates Large Language Models (LLMs) in generating PDDL (Planning Domain Definition Language) plans, providing a comprehensive pipeline for plan generation, validation, and quality assessment.

### Research Objectives

1. **RQ1**: How effectively can LLMs generate valid and optimal PDDL plans across different planning domains?
2. **RQ2**: How do domain experts perceive and evaluate LLM-generated plans? (Human-centric trust calibration)

### Key Contributions

- **Local LLM Inference**: Utilizes Ollama for privacy-preserving, local model deployment
- **Multi-Model Evaluation**: Supports multiple open-source models (Qwen 2.5, LLaMA 2, Mistral)
- **Temperature Benchmarking**: Systematic evaluation across temperature range (0.0-1.0)
- **Automated Plan Validation**: Integration with VAL validator for correctness verification
- **Optimal Gap Analysis**: Plan quality assessment against classical planner baselines
- **Natural Language Conversion**: Human-readable plan generation for expert evaluation

---

## Features

- **Multiple Planning Methods**: Support for various prompting strategies (LLM, LLM+PDDL, LLM+IC, LLM+IC+PDDL)
- **Temperature Benchmarking**: Systematic evaluation across temperature range 0.0-1.0
- **Plan Validation**: Automated validation using VAL validator
- **Optimal Gap Analysis**: Comparison against optimal plans using Fast Downward
- **Natural Language Conversion**: Convert PDDL plans to human-readable descriptions
- **Multi-Model Support**: Test with different LLM models via Ollama

## Supported Planning Domains

| Domain | Description |
|--------|-------------|
| **Barman** | Cocktail preparation with ingredients, shakers, and glasses |
| **Blocksworld** | Classic block stacking and manipulation |
| **Floortile** | Robot floor painting with color patterns |
| **Grippers** | Multi-gripper object transportation |
| **Storage** | Warehouse crate organization |
| **Termes** | 3D block structure construction |
| **Tyreworld** | Vehicle tyre changing operations |
| **Manipulation** | Object manipulation tasks |

---

## Prerequisites

### System Requirements

- **Python 3.8+**
- **WSL (Windows Subsystem for Linux)** - Required for Windows users
- **Git**

### Required Software

1. **Ollama** - Local LLM inference platform
2. **Fast Downward** - Classical PDDL planner
3. **VAL** - Plan validator

---

## Installation & Setup

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd llm-pddl
```

### Step 2: Install Python Dependencies

```bash
pip install ollama backoff
```

### Step 3: Install and Configure Ollama

#### Install Ollama
Download and install from: https://ollama.ai/download

#### Start Ollama Service
```bash
ollama serve
```

#### Pull Required Models
```bash
# Pull the models you want to test
ollama pull qwen2.5:7b-instruct
ollama pull llama2:7b
ollama pull mistral:7b

# Verify models are installed
ollama list
```

### Step 4: Build Fast Downward (WSL Required for Windows)

```bash
# Open WSL terminal
wsl

# Navigate to the downward directory
cd /mnt/c/Users/<your-username>/Desktop/workflow\ trust\ calibration/llm-pddl/downward

# Fix line endings (required on Windows)
sudo apt install dos2unix
dos2unix build.py
dos2unix fast-downward.py

# Install build dependencies
sudo apt update
sudo apt install cmake g++ python3

# Build Fast Downward
python3 build.py release
```

### Step 5: Verify VAL Installation

VAL validator is included in the `downward/VAL/` directory:

```bash
# In WSL - ensure execute permissions
chmod +x downward/VAL/validate

# Test VAL
./downward/VAL/validate --help
```

---

## Project Structure

```
llm-pddl/
├── main.py                      # Main pipeline orchestration
├── validate_plans.py            # Plan validation using VAL
├── test_optimal_gap.py          # Optimal gap calculation
├── convert_plan_to_language.py  # Plan to natural language conversion
├── run.sh                       # Batch execution script
├── domains/                     # Planning domains
│   ├── barman/
│   │   ├── domain.pddl          # Domain definition
│   │   ├── domain.nl            # Natural language domain description
│   │   ├── p_example.pddl       # Example problem (for few-shot)
│   │   ├── p_example.nl         # Example natural language
│   │   ├── p_example.sol        # Example solution
│   │   ├── p01.pddl - p20.pddl  # Test problems
│   │   └── p01.nl - p20.nl      # Test problem descriptions
│   ├── blocksworld/
│   ├── floortile/
│   ├── grippers/
│   ├── storage/
│   ├── termes/
│   ├── tyreworld/
│   └── manipulation/
├── downward/                    # Fast Downward planner
│   ├── fast-downward.py         # Main planner script
│   ├── builds/                  # Compiled binaries
│   └── VAL/                     # Plan validator
├── experiments/                 # Generated experiment results
│   └── run1/
│       └── llm_ic_pddl/
│           └── blocksworld/
│               ├── *.plan       # Generated plans
│               └── *.nl         # Natural language descriptions
├── prompts/                     # Prompt templates
│   ├── llm/                     # Basic LLM prompts
│   ├── llm_pddl/                # LLM + PDDL prompts
│   ├── llm_ic/                  # LLM + In-Context prompts
│   └── llm_ic_pddl/             # LLM + IC + PDDL prompts
└── keys/                        # Configuration files
```

---

## Usage

### Running the Main Pipeline

#### Basic Command Structure
```bash
python main.py --domain DOMAIN --method METHOD --run RUN_ID [OPTIONS]
```

#### Command Line Arguments

| Argument | Description | Options |
|----------|-------------|---------|
| `--domain` | Planning domain | `barman`, `blocksworld`, `floortile`, `grippers`, `storage`, `termes`, `tyreworld`, `manipulation` |
| `--method` | Planning method | `llm`, `llm_pddl`, `llm_ic`, `llm_ic_pddl` |
| `--run` | Experiment run identifier | Any string (e.g., `run1`, `run2`) |
| `--pnum` | Problem numbers | Comma-separated (e.g., `1,2,3,4,5`) |
| `--temp` | Temperature values | Comma-separated (e.g., `0.0,0.2,0.4`) |

#### Example Commands

```bash
# Run single domain with default settings
python main.py --domain blocksworld --method llm_ic_pddl --run run1

# Run with specific temperatures
python main.py --domain barman --method llm_ic_pddl --run run1 --temp 0.0,0.2,0.4,0.6,0.8,1.0

# Run specific problems only
python main.py --domain blocksworld --method llm_ic_pddl --run run1 --pnum 1,2,3

# Full benchmark run (5 problems × 11 temperatures)
python main.py --domain blocksworld --method llm_ic_pddl --run run1 --pnum 1,2,3,4,5 --temp 0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0
```

### Validating Generated Plans

After generating plans, validate them using:

```bash
python validate_plans.py --domain blocksworld --run run1 --verbose
```

**Output**: Creates `validation.txt` in the experiment directory with:
- Valid/Invalid status for each plan
- Error messages for invalid plans
- Summary statistics

### Calculating Optimal Gap

Compare generated plans against optimal solutions:

```bash
python test_optimal_gap.py --domain blocksworld --run run1
```

**Optimal Gap Formula**: `Generated Plan Cost / Optimal Plan Cost`
- Value of **1.0** = Optimal plan
- Value of **1.5** = Plan is 50% longer than optimal

### Converting Plans to Natural Language

Generate human-readable plan descriptions:

```bash
python convert_plan_to_language.py --domain blocksworld --run run1
```

---

## Planning Methods Explained

| Method | Prompt Components | Description |
|--------|-------------------|-------------|
| `llm` | NL problem only | Direct natural language prompting |
| `llm_pddl` | NL + Domain PDDL + Problem PDDL | PDDL context provided |
| `llm_ic` | NL + Example problem + Example solution | Few-shot learning |
| `llm_ic_pddl` | NL + PDDL + Example (full context) | **Best performance** |

### Recommended Method

For research purposes, use **`llm_ic_pddl`** as it provides the LLM with:
1. Domain knowledge (PDDL)
2. Problem specification (NL + PDDL)
3. Learning examples (few-shot)

---

## Configuration

### Changing the LLM Model

Edit `main.py` and modify the model name in the `Planner` class:

```python
response = ollama.chat(
    model='qwen2.5:7b-instruct',  # Change to desired model
    messages=[{"role": "user", "content": prompt}],
    options={"temperature": self.temperature}
)
```

**Available Models**:
- `qwen2.5:7b-instruct` (Recommended)
- `llama2:7b`
- `mistral:7b`
- `codellama:7b`
- Any Ollama-supported model

### Changing the Planner Algorithm

Edit the `FAST_DOWNWARD_ALIAS` in `main.py`:

```python
# For satisficing plans (faster, good quality)
FAST_DOWNWARD_ALIAS = "lama-first"

# For optimal plans (slower, guaranteed optimal)
FAST_DOWNWARD_ALIAS = "seq-opt-lmcut"
```

---

## Troubleshooting

### Fast Downward Build Errors (Windows/WSL)

**Problem**: Line ending errors
```
/usr/bin/env: 'python3\r': No such file or directory
```

**Solution**:
```bash
dos2unix build.py
dos2unix fast-downward.py
python3 build.py release
```

### Ollama Connection Errors

**Problem**: Cannot connect to Ollama

**Solution**:
1. Start Ollama service: `ollama serve`
2. Verify models: `ollama list`
3. Pull missing model: `ollama pull qwen2.5:7b-instruct`

### Plan Validation Fails

**Problem**: All plans marked as invalid

**Solution**:
1. Check domain/problem PDDL syntax
2. Ensure VAL has execute permissions: `chmod +x downward/VAL/validate`
3. Verify WSL paths are correct for Windows

### Memory Issues

**Problem**: Out of memory during plan generation

**Solution**:
1. Use smaller models (7B instead of 13B)
2. Reduce batch size
3. Close other applications

---

## Output Files

### Generated File Types

| Extension | Description |
|-----------|-------------|
| `.plan` | PDDL action sequence |
| `.nl` | Natural language plan description |
| `_prompt.txt` | Full prompt sent to LLM |
| `_response.txt` | Raw LLM response |
| `validation.txt` | Validation results |
| `optimal_gap.txt` | Plan quality metrics |

### Example Output Structure

```
experiments/run1/llm_ic_pddl/blocksworld/
├── p01_t0.0.plan           # Plan at temperature 0.0
├── p01_t0.0.nl             # Natural language version
├── p01_t0.0_prompt.txt     # Prompt used
├── p01_t0.5.plan           # Plan at temperature 0.5
├── p01_t1.0.plan           # Plan at temperature 1.0
├── validation.txt          # All validation results
└── optimal_gap.txt         # Quality metrics
```


## License

This project is developed for academic research purposes.

**Third-Party Components**:
- Fast Downward: GPL-3.0 License
- VAL Validator: Included with attribution

---

## Acknowledgments

This research was conducted as part of a Final Year Project on Trust Calibration in LLM-Assisted Workflow Planning.

---

## Contact

For questions or issues, please open a GitHub issue or contact the repository maintainers.
