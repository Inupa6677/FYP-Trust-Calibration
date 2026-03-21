const API_BASE_URL = 'http://localhost:8000'

export async function getConfig() {
  const response = await fetch(`${API_BASE_URL}/api/config`)
  if (!response.ok) {
    throw new Error('Failed to fetch configuration')
  }
  return response.json()
}

export async function runPipeline(request) {
  const response = await fetch(`${API_BASE_URL}/api/run-pipeline`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  })
  
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Failed to start pipeline')
  }
  
  return response.json()
}

export async function getJobStatus(jobId) {
  const response = await fetch(`${API_BASE_URL}/api/status/${jobId}`)
  if (!response.ok) {
    throw new Error('Failed to fetch job status')
  }
  return response.json()
}

export async function getAllJobs() {
  const response = await fetch(`${API_BASE_URL}/api/jobs`)
  if (!response.ok) {
    throw new Error('Failed to fetch jobs')
  }
  return response.json()
}
