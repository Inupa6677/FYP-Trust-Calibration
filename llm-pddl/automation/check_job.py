import requests
import sys

job_id = sys.argv[1] if len(sys.argv) > 1 else "01004b49-3391-4ef9-aa0a-90b9606d5e6f"
response = requests.get(f'http://localhost:8000/api/status/{job_id}')
data = response.json()

print(f"\n{'='*60}")
print(f"Job ID: {job_id}")
print(f"Status: {data.get('status')}")
print(f"Domain: {data.get('domain')}, Task: {data.get('task_id')}")
print(f"{'='*60}\n")

for msg in data.get('messages', []):
    print(f"[{msg['timestamp']}] [{msg['level']}] {msg['message']}")
