"""
Configuration file for the automated pipeline
Contains domain-task mappings and system settings
"""

import os
from pathlib import Path

# Base directory (parent of automation folder)
BASE_DIR = Path(__file__).parent.parent.parent.absolute()

# Domain to task ID mappings (actual task IDs used in commands)
DOMAIN_TASK_MAPPING = {
    "barman": [0, 5, 2, 3, 4],
    "blocksworld": [17, 12, 11, 7, 4],
    "floortile": [7, 4, 3, 6, 5],
    "grippers": [7, 1, 2, 3, 6],
    "storage": [6, 5, 2, 3, 4]
}

# Available LLM models (display name -> actual Ollama model name)
MODEL_MAPPING = {
    "qwen2.5:7b-instruct": "qwen2.5:7b-instruct",
    "llama2:7b": "llama2:7b",
    "mistral:7b": "mistral:latest",
    "llama3.1:8b": "llama3.1:8b"
}

# Available models for frontend (display names)
AVAILABLE_MODELS = list(MODEL_MAPPING.keys())

# Available domains
AVAILABLE_DOMAINS = ["barman", "blocksworld", "floortile", "grippers", "storage"]

# Temperature range
TEMPERATURE_MIN = 0.0
TEMPERATURE_MAX = 1.0
TEMPERATURE_STEP = 0.1

# Pipeline method (fixed for this research)
PIPELINE_METHOD = "llm_ic_pddl_planner"

# Fast Downward aliases
FAST_DOWNWARD_ALIAS_PLAN = "lama-first"
FAST_DOWNWARD_ALIAS_OPTIMAL = "seq-opt-lmcut"


def get_ollama_model_name(display_name):
    """
    Map frontend display name to actual Ollama model name
    Example: "mistral:7b" -> "mistral:latest"
    """
    return MODEL_MAPPING.get(display_name, display_name)


def task_to_plan_number(task_id):
    """
    Convert task ID to plan number format
    Example: task 0 -> p01, task 6 -> p07, task 17 -> p18
    """
    return f"p{str(task_id + 1).zfill(2)}"


def plan_number_to_task(plan_num):
    """
    Convert plan number to task ID
    Example: p01 -> 0, p07 -> 6, p18 -> 17
    """
    return int(plan_num.replace('p', '')) - 1


def windows_to_wsl_path(win_path):
    """
    Convert Windows path to WSL path
    Example: C:/Users/... -> /mnt/c/Users/...
    """
    win_path_str = str(win_path)
    # Convert backslashes to forward slashes
    wsl_path = win_path_str.replace('\\', '/')
    # Replace drive letter
    if ':' in wsl_path:
        drive = wsl_path[0].lower()
        wsl_path = f"/mnt/{drive}{wsl_path[2:]}"
    return wsl_path


def get_experiment_paths(run_id, domain, task_id):
    """
    Get all relevant file paths for a given experiment
    """
    plan_num = task_to_plan_number(task_id)
    
    paths = {
        'domain_pddl': BASE_DIR / 'domains' / domain / 'domain.pddl',
        'problem_pddl': BASE_DIR / 'experiments' / run_id / 'problems' / 'llm_ic_pddl' / f'{plan_num}.pddl',
        'plan_file': BASE_DIR / 'experiments' / run_id / 'plans' / 'llm_ic_pddl' / f'{plan_num}.plan',
        'sas_file': BASE_DIR / 'experiments' / run_id / 'plans' / 'llm_ic_pddl' / f'{plan_num}.sas',
        'optimal_plan': BASE_DIR / 'experiments' / run_id / 'plans' / 'llm_ic_pddl' / f'{plan_num}_optimal.plan',
        'validation_output': BASE_DIR / 'experiments' / run_id / 'plans' / 'llm_ic_pddl' / 'validation.txt',
    }
    
    return paths


if __name__ == "__main__":
    # Test the configuration
    print("=== Pipeline Configuration ===")
    print(f"Base Directory: {BASE_DIR}")
    print(f"\nAvailable Models: {AVAILABLE_MODELS}")
    print(f"\nAvailable Domains: {AVAILABLE_DOMAINS}")
    print(f"\nDomain-Task Mappings:")
    for domain, tasks in DOMAIN_TASK_MAPPING.items():
        print(f"  {domain}: {tasks}")
    
    print("\n=== Path Conversion Tests ===")
    print(f"Task 0 -> {task_to_plan_number(0)}")
    print(f"Task 6 -> {task_to_plan_number(6)}")
    print(f"Task 17 -> {task_to_plan_number(17)}")
    
    test_path = "C:/Users/inupa/Desktop/workflow trust calibration/llm-pddl"
    print(f"\nWindows path: {test_path}")
    print(f"WSL path: {windows_to_wsl_path(test_path)}")
