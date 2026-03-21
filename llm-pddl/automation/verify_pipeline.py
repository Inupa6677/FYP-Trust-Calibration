"""
Pipeline Verification Script
Proves that the automation system works correctly
"""
import requests
import time
import os
from pathlib import Path

API_BASE = 'http://localhost:8000'
PROJECT_ROOT = Path(__file__).parent.parent

def verify_pipeline():
    print("=" * 80)
    print("🔬 PIPELINE VERIFICATION TEST")
    print("=" * 80)
    
    # 1. Start a pipeline
    print("\n1️⃣  Starting pipeline job...")
    config = {
        "model": "qwen2.5:7b-instruct",
        "temperature": 0.7,
        "domain": "barman",
        "task_id": 0,
        "run_id": "run1"
    }
    print(f"   Config: {config}")
    
    response = requests.post(f'{API_BASE}/api/run-pipeline', json=config)
    job = response.json()
    job_id = job['job_id']
    print(f"   ✅ Job started: {job_id[:16]}...")
    
    # 2. Monitor until completion
    print("\n2️⃣  Monitoring execution...")
    step_completed = {}
    
    while True:
        status = requests.get(f'{API_BASE}/api/status/{job_id}').json()
        
        current_step = status.get('current_step')
        if current_step and current_step not in step_completed:
            print(f"   📍 Step: {current_step} ({status['progress']}%)")
            step_completed[current_step] = True
        
        if status['status'] in ['completed', 'failed']:
            print(f"\n   Status: {status['status'].upper()}")
            break
        
        time.sleep(1)
    
    # 3. Verify files were created
    print("\n3️⃣  Verifying files created...")
    run_num = config['run_id'].replace('run', '')
    plan_num = f"p{str(config['task_id'] + 1).zfill(2)}"
    
    files_to_check = {
        "PDDL Problem": PROJECT_ROOT / f"experiments/run{run_num}/problems/llm_ic_pddl/{plan_num}.pddl",
        "Generated Plan": PROJECT_ROOT / f"experiments/run{run_num}/plans/llm_ic_pddl/{plan_num}.plan",
        "SAS File": PROJECT_ROOT / f"experiments/run{run_num}/plans/llm_ic_pddl/{plan_num}.sas",
        "Optimal Plan": PROJECT_ROOT / f"experiments/run{run_num}/plans/llm_ic_pddl/{plan_num}_optimal.plan",
    }
    
    all_exist = True
    for name, path in files_to_check.items():
        exists = path.exists()
        symbol = "✅" if exists else "❌"
        print(f"   {symbol} {name}: {path.name}")
        if exists:
            size = path.stat().st_size
            print(f"      Size: {size} bytes")
        all_exist = all_exist and exists
    
    # 4. Verify content
    print("\n4️⃣  Verifying file contents...")
    
    pddl_file = files_to_check["PDDL Problem"]
    if pddl_file.exists():
        with open(pddl_file, 'r') as f:
            content = f.read()
            has_define = content.startswith("(define")
            has_goal = ":goal" in content
            no_explanation = "Note:" not in content and "Explanation:" not in content
            
            print(f"   PDDL Problem:")
            print(f"      ✅ Starts with (define)" if has_define else "      ❌ Missing (define)")
            print(f"      ✅ Has :goal section" if has_goal else "      ❌ Missing :goal")
            print(f"      ✅ No explanatory text" if no_explanation else "      ❌ Has explanatory text")
    
    plan_file = files_to_check["Generated Plan"]
    if plan_file.exists():
        with open(plan_file, 'r') as f:
            lines = f.readlines()
            # Remove cost line if present
            actions = [l for l in lines if not l.startswith(';')]
            plan_length = len(actions)
            print(f"   Generated Plan:")
            print(f"      Plan length: {plan_length} actions")
    
    optimal_file = files_to_check["Optimal Plan"]
    if optimal_file.exists():
        with open(optimal_file, 'r') as f:
            lines = f.readlines()
            actions = [l for l in lines if not l.startswith(';')]
            optimal_length = len(actions)
            print(f"   Optimal Plan:")
            print(f"      Plan length: {optimal_length} actions")
    
    # 5. Verify results
    print("\n5️⃣  Verifying results...")
    if 'results' in status:
        results = status['results']
        print(f"   Validation: {results.get('validation', 'N/A')}")
        print(f"   Optimal Gap: {results.get('optimal_gap', 'N/A')}")
        
        if 'optimal_gap' in results:
            calculated_gap = plan_length / optimal_length
            matches = abs(calculated_gap - results['optimal_gap']) < 0.01
            print(f"   Manual calculation: {plan_length}/{optimal_length} = {calculated_gap:.2f}")
            print(f"   {'✅' if matches else '❌'} Gap matches: {matches}")
    
    # 6. Verify command execution via logs
    print("\n6️⃣  Verifying command execution...")
    messages = status.get('messages', [])
    
    commands_found = {
        "Step 1 - PDDL Generation": any("python main.py --method llm_ic_pddl_planner" in m['message'] for m in messages),
        "Step 2 - Plan Generation": any("fast-downward.py" in m['message'] and "lama-first" in m['message'] for m in messages),
        "Step 3 - Validation": any("validate_plans.py" in m['message'] for m in messages),
        "Step 4 - Optimal Plan": any("fast-downward.py" in m['message'] and "seq-opt-lmcut" in m['message'] for m in messages),
        "Step 5 - Gap Calculation": any("test_optimal_gap.py" in m['message'] for m in messages),
    }
    
    for step, found in commands_found.items():
        symbol = "✅" if found else "❌"
        print(f"   {symbol} {step}")
    
    # 7. Model & Temperature verification
    print("\n7️⃣  Verifying model & temperature settings...")
    print(f"   Model used: {status.get('model', 'N/A')}")
    print(f"   Temperature: {status.get('temperature', 'N/A')}")
    print(f"   ✅ Matches request" if status.get('model') == config['model'] else "   ❌ Mismatch")
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 80)
    print(f"Pipeline Status: {status['status'].upper()}")
    print(f"All Files Created: {'YES ✅' if all_exist else 'NO ❌'}")
    print(f"All Steps Executed: {'YES ✅' if all(commands_found.values()) else 'NO ❌'}")
    print(f"Results Available: {'YES ✅' if status.get('results') else 'NO ❌'}")
    print(f"Total Duration: {status.get('duration', 0):.2f}s")
    print(f"Total Logs: {len(messages)}")
    print("=" * 80)

if __name__ == "__main__":
    try:
        verify_pipeline()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
