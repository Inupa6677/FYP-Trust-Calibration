"""
Pipeline Orchestrator - Core automation logic for running the complete workflow
Handles execution of all pipeline steps from PDDL generation to optimal gap calculation
"""

import subprocess
import os
import sys
import time
from pathlib import Path
from datetime import datetime
import json

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent))
from config import (
    BASE_DIR, PIPELINE_METHOD, FAST_DOWNWARD_ALIAS_PLAN, 
    FAST_DOWNWARD_ALIAS_OPTIMAL, task_to_plan_number, 
    windows_to_wsl_path, get_experiment_paths, get_ollama_model_name
)


class PipelineStatus:
    """Enum for pipeline execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class PipelineStep:
    """Enum for pipeline steps"""
    GENERATE_PDDL = "generate_pddl"
    GENERATE_PLAN = "generate_plan"
    VALIDATE_PLAN = "validate_plan"
    GENERATE_OPTIMAL = "generate_optimal"
    CALCULATE_GAP = "calculate_gap"


class PipelineRunner:
    """
    Main pipeline orchestrator that runs the complete workflow
    """
    
    def __init__(self, model, temperature, domain, task_id, run_id="run1"):
        self.model = model
        self.temperature = temperature
        self.domain = domain
        self.task_id = task_id
        self.run_id = run_id
        self.plan_num = task_to_plan_number(task_id)
        
        self.status = PipelineStatus.PENDING
        self.current_step = None
        self.logs = []
        self.results = {}
        self.start_time = None
        self.end_time = None
        
        # Get all file paths
        self.paths = get_experiment_paths(run_id, domain, task_id)
        
    def log(self, message, level="INFO"):
        """Add a log message with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.logs.append(log_entry)
        print(log_entry)
        
    def run_command(self, command, use_wsl=False, cwd=None):
        """
        Execute a command and capture output
        
        Args:
            command: List of command arguments
            use_wsl: Whether to run in WSL
            cwd: Working directory
            
        Returns:
            Tuple of (success, output, error)
        """
        if use_wsl:
            command = ['wsl'] + command
            
        self.log(f"Executing: {' '.join(command)}")
        
        try:
            result = subprocess.run(
                command,
                cwd=cwd or BASE_DIR,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )
            
            if result.returncode == 0:
                self.log(f"Command succeeded")
                return True, result.stdout, result.stderr
            else:
                self.log(f"Command failed with code {result.returncode}", "ERROR")
                self.log(f"Error: {result.stderr}", "ERROR")
                return False, result.stdout, result.stderr
                
        except subprocess.TimeoutExpired:
            self.log("Command timeout after 10 minutes", "ERROR")
            return False, "", "Timeout"
        except Exception as e:
            self.log(f"Exception during command execution: {str(e)}", "ERROR")
            return False, "", str(e)
    
    def run_wsl_command(self, command_parts):
        """
        Execute a command in WSL with proper working directory
        
        Args:
            command_parts: List of command parts (without 'wsl')
            
        Returns:
            Tuple of (success, output, error)
        """
        # Convert base directory to WSL path
        wsl_base_dir = windows_to_wsl_path(BASE_DIR)
        
        # Build the full command with cd to project directory
        command_str = ' '.join(command_parts)
        full_command = f"cd '{wsl_base_dir}' && {command_str}"
        
        self.log(f"Executing in WSL: {command_str}")
        self.log(f"WSL working directory: {wsl_base_dir}")
        
        try:
            result = subprocess.run(
                ['wsl', 'bash', '-c', full_command],
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )
            
            if result.returncode == 0:
                self.log(f"WSL command succeeded")
                return True, result.stdout, result.stderr
            else:
                self.log(f"WSL command failed with code {result.returncode}", "ERROR")
                if result.stderr:
                    self.log(f"Error: {result.stderr}", "ERROR")
                if result.stdout:
                    self.log(f"Output: {result.stdout}", "ERROR")
                return False, result.stdout, result.stderr
                
        except subprocess.TimeoutExpired:
            self.log("WSL command timeout after 10 minutes", "ERROR")
            return False, "", "Timeout"
        except Exception as e:
            self.log(f"Exception during WSL command execution: {str(e)}", "ERROR")
            return False, "", str(e)
    
    def step_1_generate_pddl(self):
        """Step 1: Generate PDDL problem using main.py"""
        self.current_step = PipelineStep.GENERATE_PDDL
        self.log(f"Step 1: Generating PDDL problem for {self.domain} task {self.task_id}")
        
        # Extract numeric run ID (e.g., "run1" -> 1)
        run_num = self.run_id.replace('run', '') if 'run' in self.run_id else '1'
        
        # Map frontend model name to actual Ollama model name
        ollama_model = get_ollama_model_name(self.model)
        
        command = [
            'python',
            'main.py',
            '--method', PIPELINE_METHOD,
            '--domain', self.domain,
            '--task', str(self.task_id),
            '--run', run_num,
            '--model', ollama_model,
            '--temperature', str(self.temperature)
        ]
        
        success, stdout, stderr = self.run_command(command, use_wsl=False)
        
        if success and self.paths['problem_pddl'].exists():
            self.log(f"PDDL problem generated successfully: {self.plan_num}.pddl")
            return True
        else:
            self.log("Failed to generate PDDL problem", "ERROR")
            return False
    
    def step_2_generate_plan(self):
        """Step 2: Generate plan using Fast Downward (lama-first)"""
        self.current_step = PipelineStep.GENERATE_PLAN
        self.log(f"Step 2: Generating plan using Fast Downward ({FAST_DOWNWARD_ALIAS_PLAN})")
        
        # Use relative paths within WSL context
        run_num = self.run_id.replace('run', '') if 'run' in self.run_id else '1'
        
        command = [
            'python3',
            'downward/fast-downward.py',
            '--alias', FAST_DOWNWARD_ALIAS_PLAN,
            '--plan-file', f'experiments/run{run_num}/plans/llm_ic_pddl/{self.plan_num}.plan',
            '--sas-file', f'experiments/run{run_num}/plans/llm_ic_pddl/{self.plan_num}.sas',
            f'domains/{self.domain}/domain.pddl',
            f'experiments/run{run_num}/problems/llm_ic_pddl/{self.plan_num}.pddl'
        ]
        
        success, stdout, stderr = self.run_wsl_command(command)
        
        if success and self.paths['plan_file'].exists():
            self.log(f"Plan generated successfully: {self.plan_num}.plan")
            return True
        else:
            self.log("Failed to generate plan", "ERROR")
            return False
    
    def step_3_validate_plan(self):
        """Step 3: Validate the generated plan using VAL"""
        self.current_step = PipelineStep.VALIDATE_PLAN
        self.log(f"Step 3: Validating plan for {self.domain}")
        
        # Use relative paths within WSL context
        run_num = self.run_id.replace('run', '') if 'run' in self.run_id else '1'
        
        command = [
            'python3',
            'validate_plans.py',
            '--domain', self.domain,
            '--run', f'run{run_num}',
            '--verbose'
        ]
        
        success, stdout, stderr = self.run_wsl_command(command)
        
        if success:
            self.log("Plan validation completed")
            # Parse validation results
            self.results['validation'] = self._parse_validation_output(stdout)
            return True
        else:
            self.log("Plan validation failed", "ERROR")
            return False
    
    def step_4_generate_optimal_plan(self):
        """Step 4: Generate optimal plan using Fast Downward (seq-opt-lmcut)"""
        self.current_step = PipelineStep.GENERATE_OPTIMAL
        self.log(f"Step 4: Generating optimal plan using Fast Downward ({FAST_DOWNWARD_ALIAS_OPTIMAL})")
        
        # Use relative paths within WSL context
        run_num = self.run_id.replace('run', '') if 'run' in self.run_id else '1'
        
        command = [
            'python3',
            'downward/fast-downward.py',
            '--alias', FAST_DOWNWARD_ALIAS_OPTIMAL,
            '--plan-file', f'experiments/run{run_num}/plans/llm_ic_pddl/{self.plan_num}_optimal.plan',
            f'domains/{self.domain}/domain.pddl',
            f'experiments/run{run_num}/problems/llm_ic_pddl/{self.plan_num}.pddl'
        ]
        
        success, stdout, stderr = self.run_wsl_command(command)
        
        if success and self.paths['optimal_plan'].exists():
            self.log(f"Optimal plan generated successfully: {self.plan_num}_optimal.plan")
            return True
        else:
            self.log("Failed to generate optimal plan", "ERROR")
            return False
    
    def step_5_calculate_optimal_gap(self):
        """Step 5: Calculate optimal gap"""
        self.current_step = PipelineStep.CALCULATE_GAP
        self.log(f"Step 5: Calculating optimal gap")
        
        command = [
            'python',
            'test_optimal_gap.py',
            '--domain', self.domain,
            '--task', str(self.task_id),
            '--run', self.run_id
        ]
        
        success, stdout, stderr = self.run_command(command, use_wsl=False)
        
        if success:
            self.log("Optimal gap calculated successfully")
            # Parse optimal gap from output
            self.results['optimal_gap'] = self._parse_optimal_gap(stdout)
            return True
        else:
            self.log("Failed to calculate optimal gap", "ERROR")
            return False
    
    def _parse_validation_output(self, output):
        """Parse validation output to determine if plan is valid"""
        if "valid" in output.lower():
            return "valid"
        elif "invalid" in output.lower():
            return "invalid"
        else:
            return "unknown"
    
    def _parse_optimal_gap(self, output):
        """Parse optimal gap value from output"""
        try:
            # Look for pattern like "Optimal Gap: 1.25"
            for line in output.split('\n'):
                if 'gap' in line.lower():
                    parts = line.split(':')
                    if len(parts) > 1:
                        return float(parts[1].strip())
        except:
            pass
        return None
    
    def run(self):
        """
        Execute the complete pipeline
        
        Returns:
            Dictionary with execution results
        """
        self.status = PipelineStatus.RUNNING
        self.start_time = datetime.now()
        self.log(f"Starting pipeline for {self.domain} task {self.task_id} ({self.plan_num})")
        self.log(f"Model: {self.model}, Temperature: {self.temperature}")
        
        steps = [
            self.step_1_generate_pddl,
            self.step_2_generate_plan,
            self.step_3_validate_plan,
            self.step_4_generate_optimal_plan,
            self.step_5_calculate_optimal_gap
        ]
        
        for i, step in enumerate(steps, 1):
            self.log(f"=" * 60)
            try:
                success = step()
                if not success:
                    self.status = PipelineStatus.FAILED
                    self.log(f"Pipeline failed at step {i}", "ERROR")
                    break
            except Exception as e:
                self.log(f"Exception in step {i}: {str(e)}", "ERROR")
                self.status = PipelineStatus.FAILED
                break
        else:
            # All steps completed successfully
            self.status = PipelineStatus.COMPLETED
            self.log("Pipeline completed successfully!")
        
        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()
        self.log(f"Total execution time: {duration:.2f} seconds")
        
        return {
            'status': self.status,
            'domain': self.domain,
            'task_id': self.task_id,
            'plan_num': self.plan_num,
            'model': self.model,
            'temperature': self.temperature,
            'run_id': self.run_id,
            'results': self.results,
            'logs': self.logs,
            'duration': duration
        }


if __name__ == "__main__":
    # Test the pipeline runner
    print("=== Pipeline Orchestrator Test ===\n")
    
    # Example: Run barman task 0 with qwen2.5 at temperature 0.5
    runner = PipelineRunner(
        model="qwen2.5:7b-instruct",
        temperature=0.5,
        domain="barman",
        task_id=0,
        run_id="run1"
    )
    
    print(f"Configured pipeline:")
    print(f"  Domain: {runner.domain}")
    print(f"  Task ID: {runner.task_id}")
    print(f"  Plan Number: {runner.plan_num}")
    print(f"  Model: {runner.model}")
    print(f"  Temperature: {runner.temperature}")
    print(f"\nPaths:")
    for key, path in runner.paths.items():
        print(f"  {key}: {path}")
    
    print("\n" + "=" * 60)
    print("To execute the pipeline, uncomment the line below:")
    print("# result = runner.run()")
    print("=" * 60)
