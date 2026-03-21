"""
Test script for the automated pipeline
Tests the complete workflow from API call to result
"""

import requests
import time
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_config():
    """Test the configuration endpoint"""
    print("=" * 60)
    print("TEST 1: Getting Configuration")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/api/config")
    
    if response.status_code == 200:
        config = response.json()
        print("✅ Configuration retrieved successfully")
        print(f"   Models: {config['models']}")
        print(f"   Domains: {config['domains']}")
        print(f"   Method: {config['method']}")
        return config
    else:
        print(f"❌ Failed to get configuration: {response.status_code}")
        return None

def test_pipeline_run():
    """Test running the pipeline"""
    print("\n" + "=" * 60)
    print("TEST 2: Starting Pipeline Run")
    print("=" * 60)
    
    # Configure the pipeline run
    request = {
        "model": "qwen2.5:7b-instruct",
        "temperature": 0.5,
        "domain": "barman",
        "task_id": 0,
        "run_id": "run1"
    }
    
    print(f"Request: {json.dumps(request, indent=2)}")
    
    response = requests.post(
        f"{BASE_URL}/api/run-pipeline",
        json=request
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Pipeline started successfully")
        print(f"   Job ID: {result['job_id']}")
        print(f"   Status: {result['status']}")
        return result['job_id']
    else:
        print(f"❌ Failed to start pipeline: {response.status_code}")
        print(f"   Error: {response.text}")
        return None

def monitor_job(job_id):
    """Monitor the job until completion"""
    print("\n" + "=" * 60)
    print("TEST 3: Monitoring Job Progress")
    print("=" * 60)
    
    completed = False
    iteration = 0
    
    while not completed and iteration < 60:  # Max 2 minutes
        iteration += 1
        time.sleep(2)  # Poll every 2 seconds
        
        response = requests.get(f"{BASE_URL}/api/status/{job_id}")
        
        if response.status_code == 200:
            status = response.json()
            
            print(f"\n[{iteration}] Status: {status['status']}")
            if status.get('current_step'):
                print(f"    Current Step: {status['current_step']}")
            print(f"    Progress: {status.get('progress', 0)}%")
            
            # Show latest log entry
            if status.get('logs') and len(status['logs']) > 0:
                print(f"    Latest: {status['logs'][-1][:80]}")
            
            # Check if completed or failed
            if status['status'] in ['completed', 'failed']:
                completed = True
                print("\n" + "=" * 60)
                print(f"{'✅ JOB COMPLETED' if status['status'] == 'completed' else '❌ JOB FAILED'}")
                print("=" * 60)
                
                if status.get('results'):
                    print("\nResults:")
                    for key, value in status['results'].items():
                        print(f"  {key}: {value}")
                
                if status.get('duration'):
                    print(f"\nDuration: {status['duration']:.2f}s")
                
                return status
        else:
            print(f"❌ Failed to get status: {response.status_code}")
            break
    
    if not completed:
        print("\n⚠️  Job monitoring timeout (2 minutes)")
    
    return None

def test_all_jobs():
    """List all jobs"""
    print("\n" + "=" * 60)
    print("TEST 4: Listing All Jobs")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/api/jobs")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {data['total']} jobs")
        
        for job in data['jobs']:
            print(f"\n  Job ID: {job['job_id'][:8]}...")
            print(f"  Status: {job['status']}")
            print(f"  Domain: {job['domain']}")
            print(f"  Task: {job['task_id']}")
            print(f"  Model: {job['model']}")
    else:
        print(f"❌ Failed to get jobs: {response.status_code}")

def main():
    """Run all tests"""
    print("\n🧪 LLM-PDDL Pipeline API Test Suite")
    print("=" * 60)
    
    try:
        # Test 1: Get configuration
        config = test_config()
        if not config:
            return
        
        # Test 2: Start pipeline
        job_id = test_pipeline_run()
        if not job_id:
            return
        
        # Test 3: Monitor progress
        final_status = monitor_job(job_id)
        
        # Test 4: List all jobs
        test_all_jobs()
        
        print("\n" + "=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to API server")
        print("   Make sure the backend is running on http://localhost:8000")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")

if __name__ == "__main__":
    main()
