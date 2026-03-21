"""
Test to PROVE that model and temperature from frontend are actually used
"""
import requests
import json

API_BASE = 'http://localhost:8000'

def test_model_temperature_usage():
    print("=" * 80)
    print("🔬 MODEL & TEMPERATURE USAGE TEST")
    print("=" * 80)
    
    # Test 1: Use specific model and temperature
    print("\n📝 Test 1: Starting pipeline with SPECIFIC settings")
    config = {
        "model": "qwen2.5:7b-instruct",  # ← Specific choice
        "temperature": 0.3,               # ← Specific choice (low = deterministic)
        "domain": "barman",
        "task_id": 0,
        "run_id": "run1"
    }
    print(f"   Requested: model={config['model']}, temperature={config['temperature']}")
    
    response = requests.post(f'{API_BASE}/api/run-pipeline', json=config)
    job1 = response.json()
    job_id1 = job1['job_id']
    print(f"   Job ID: {job_id1[:16]}...")
    
    # Wait for job to start and check logs
    import time
    time.sleep(3)
    
    status = requests.get(f'{API_BASE}/api/status/{job_id1}').json()
    
    # Check if logs contain the model and temperature
    messages = status.get('messages', [])
    log_text = ' '.join([m['message'] for m in messages])
    
    print(f"\n🔍 Checking execution logs...")
    
    # Look for the command that was executed
    command_log = None
    for msg in messages:
        if 'main.py' in msg['message'] and '--method' in msg['message']:
            command_log = msg['message']
            break
    
    if command_log:
        print(f"   Command executed:")
        print(f"   {command_log}")
        
        has_model = '--model' in command_log and config['model'] in command_log
        has_temp = '--temperature' in command_log and str(config['temperature']) in command_log
        
        print(f"\n   ✅ --model {config['model']} found in command" if has_model else f"   ❌ --model NOT found")
        print(f"   ✅ --temperature {config['temperature']} found in command" if has_temp else f"   ❌ --temperature NOT found")
        
        if has_model and has_temp:
            print(f"\n   🎉 SUCCESS! Frontend values ARE being used!")
        else:
            print(f"\n   ❌ FAILURE! Frontend values are NOT being used!")
    else:
        print("   ⏳ Command not logged yet, check job status...")
    
    # Also check job metadata
    print(f"\n📊 Job Metadata:")
    print(f"   Stored model: {status.get('model')}")
    print(f"   Stored temperature: {status.get('temperature')}")
    print(f"   Match request: {'✅' if status.get('model') == config['model'] else '❌'}")
    
    print("\n" + "=" * 80)
    print("💡 HOW TO VERIFY IN LOGS:")
    print("=" * 80)
    print("Look for this line in the backend terminal:")
    print(f"   [INFO] Using Ollama locally with model={config['model']}, temperature={config['temperature']}...")
    print("\nThis line comes from main.py and proves the values were passed correctly!")
    print("=" * 80)
    
    return job_id1

if __name__ == "__main__":
    try:
        job_id = test_model_temperature_usage()
        print(f"\n✅ Test job created: {job_id}")
        print("\nNow check the backend terminal for the confirmation message!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
