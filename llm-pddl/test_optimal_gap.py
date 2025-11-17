import argparse
from pathlib import Path
import subprocess
from main import (
    DOMAINS,
    Barman, Blocksworld, Floortile, Grippers, Storage, Termes, Tyreworld, Manipulation
)

# Create domain mapping
DOMAIN_MAP = {
    "barman": Barman,
    "blocksworld": Blocksworld,
    "floortile": Floortile,
    "grippers": Grippers,
    "storage": Storage,
    "termes": Termes,
    "tyreworld": Tyreworld,
    "manipulation": Manipulation,
}

def get_plan_cost(plan_file):
    """
    Extract the cost of a plan from its .plan file
    """
    try:
        with open(plan_file, 'r') as f:
            lines = f.readlines()
            # Fast-downward plans have a '; cost = X' line at the end
            for line in reversed(lines):
                if '; cost =' in line:
                    cost_str = line.split('=')[1].strip()
                    # Handle unit cost format (e.g., "45 (unit cost)")
                    if '(unit cost)' in cost_str:
                        return float(cost_str.split()[0])
                    return float(cost_str)
        # If no cost found, count the number of actions
        return len([l for l in lines if l.strip() and not l.startswith(';')])
    except Exception as e:
        print(f"Error reading plan cost: {e}")
        return None

def get_optimal_plan(domain_file, problem_file, output_file):
    """
    Generate optimal plan using Fast Downward with optimal settings
    """
    # Use WSL python3 command
    # Convert paths for WSL
    wsl_output = convert_to_wsl_path(output_file)
    wsl_domain = convert_to_wsl_path(domain_file)
    wsl_problem = convert_to_wsl_path(problem_file)
    
    cmd = [
        "wsl",
        "python3",
        "./downward/fast-downward.py",
        "--alias",
        "seq-opt-lmcut",  # Use optimal planning configuration with landmark-cut heuristic
        "--plan-file",
        wsl_output,
        wsl_domain,
        wsl_problem
    ]
    
    try:
        # Add a timeout to prevent hanging
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)  # 5 minute timeout
        if result.returncode == 0:
            return True
        else:
            print(f"Error generating optimal plan: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("Planner timed out after 5 minutes")
        return False
    except Exception as e:
        print(f"Error running planner: {e}")
        return False

def convert_to_wsl_path(windows_path):
    """Convert Windows path to WSL compatible path"""
    # Handle relative paths
    if windows_path.startswith('./'):
        return windows_path
        
    # Convert absolute paths
    path = str(Path(windows_path).resolve())
    path = path.replace('\\', '/')
    drive = path[0].lower()
    return f"/mnt/{drive}/{path[3:]}"

def calculate_optimal_gap(generated_plan_file, domain_file, problem_file):
    """
    Calculate the optimal gap ratio:
    optimal_gap = cost_of_generated_plan / cost_of_optimal_plan
    """
    # Ensure directories exist
    Path(generated_plan_file).parent.mkdir(parents=True, exist_ok=True)
    # Get cost of generated plan
    generated_cost = get_plan_cost(generated_plan_file)
    if generated_cost is None:
        return None
    
    # Generate optimal plan with unique filename (based on generated plan)
    plan_stem = Path(generated_plan_file).stem  # e.g., "p08"
    optimal_plan_file = str(Path(generated_plan_file).parent / f"{plan_stem}_optimal.plan")
    if not get_optimal_plan(domain_file, problem_file, optimal_plan_file):
        return None
    
    # Get cost of optimal plan
    optimal_cost = get_plan_cost(optimal_plan_file)
    if optimal_cost is None:
        return None
        
    # Calculate gap
    if optimal_cost == 0:
        print("Warning: Optimal plan has zero cost!")
        return None
        
    optimal_gap = generated_cost / optimal_cost
    return optimal_gap

def main():
    parser = argparse.ArgumentParser(description="Test Optimal Gap Calculator")
    parser.add_argument('--domain', type=str, choices=DOMAINS, required=True)
    parser.add_argument('--run', type=str, default="run1")
    parser.add_argument('--task', type=int, default=0)
    args = parser.parse_args()

    # Setup paths
    domain_cls = DOMAIN_MAP[args.domain]
    domain = domain_cls()
    domain_file = domain.get_domain_pddl_file()
    
    # Get paths for the specific task
    task_suffix = domain.get_task_suffix(args.task)
    problem_file = f"experiments/{args.run}/problems/llm_ic_pddl/{Path(task_suffix).name}"
    generated_plan = f"experiments/{args.run}/plans/llm_ic_pddl/{Path(task_suffix).stem}.plan"

    # Calculate optimal gap
    gap = calculate_optimal_gap(generated_plan, domain_file, problem_file)
    if gap is not None:
        print(f"Optimal Gap for {args.domain} task {args.task}: {gap:.3f}")
    else:
        print("Failed to calculate optimal gap")

if __name__ == "__main__":
    main()