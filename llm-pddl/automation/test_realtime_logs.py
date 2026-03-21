"""
Test script to verify real-time log updates and enhanced UI features
"""
import requests
import time
import json

API_BASE = 'http://localhost:8000'

def print_separator():
    print("\n" + "=" * 80 + "\n")

def test_realtime_logs():
    print("🧪 Real-Time Log Updates Test")
    print_separator()
    
    # 1. Start a pipeline job
    print("📝 Starting pipeline job...")
    response = requests.post(f'{API_BASE}/api/run-pipeline', json={
        "model": "qwen2.5:7b-instruct",
        "temperature": 0.5,
        "domain": "barman",
        "task_id": 0,
        "run_id": "run1"
    })
    
    job_data = response.json()
    job_id = job_data['job_id']
    print(f"✅ Job started: {job_id[:8]}...")
    print_separator()
    
    # 2. Monitor the job with real-time updates
    print("👀 Monitoring real-time logs and step progress...\n")
    
    last_log_count = 0
    last_step = None
    
    while True:
        # Get job status
        status_response = requests.get(f'{API_BASE}/api/status/{job_id}')
        status = status_response.json()
        
        # Check if we have new logs
        current_log_count = len(status.get('messages', []))
        
        if current_log_count > last_log_count:
            # Print new logs
            new_messages = status['messages'][last_log_count:]
            for msg in new_messages:
                level_color = {
                    'INFO': '\033[94m',     # Blue
                    'ERROR': '\033[91m',    # Red
                    'WARNING': '\033[93m',  # Yellow
                }.get(msg['level'], '')
                reset = '\033[0m'
                
                print(f"  {msg['timestamp']} {level_color}[{msg['level']}]{reset} {msg['message']}")
            
            last_log_count = current_log_count
        
        # Check if step changed
        if status['current_step'] != last_step and status['current_step']:
            print(f"\n🔄 Current Step: {status['current_step']} (Progress: {status['progress']}%)\n")
            last_step = status['current_step']
        
        # Check if completed
        if status['status'] in ['completed', 'failed']:
            print_separator()
            print(f"🏁 Pipeline {status['status'].upper()}")
            print(f"   Duration: {status.get('duration', 0):.2f}s")
            
            if status['results']:
                print(f"\n📊 Results:")
                for key, value in status['results'].items():
                    print(f"   {key}: {value}")
            
            break
        
        time.sleep(1)  # Poll every second
    
    print_separator()
    print("✅ Real-time log test completed!")
    print(f"   Total logs captured: {last_log_count}")
    print(f"   All 5 steps visible: {'✓' if last_log_count > 15 else '✗'}")

if __name__ == "__main__":
    try:
        test_realtime_logs()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
