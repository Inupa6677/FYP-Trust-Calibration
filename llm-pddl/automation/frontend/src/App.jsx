import { useState, useEffect } from 'react'
import './App.css'
import ModelSelector from './components/ModelSelector'
import DomainSelector from './components/DomainSelector'
import TaskSelector from './components/TaskSelector'
import TemperatureSlider from './components/TemperatureSlider'
import RunButton from './components/RunButton'
import ProgressLog from './components/ProgressLog'
import { getConfig, runPipeline, getJobStatus } from './api/pipeline'

function App() {
  const [config, setConfig] = useState(null)
  const [loading, setLoading] = useState(true)
  
  // Form state
  const [selectedModel, setSelectedModel] = useState('')
  const [selectedDomain, setSelectedDomain] = useState('')
  const [selectedTask, setSelectedTask] = useState(null)
  const [temperature, setTemperature] = useState(0.5)
  const [runId, setRunId] = useState('run1')
  
  // Job state
  const [currentJob, setCurrentJob] = useState(null)
  const [jobStatus, setJobStatus] = useState(null)
  const [polling, setPolling] = useState(false)

  // Load configuration on mount
  useEffect(() => {
    loadConfig()
  }, [])

  // Poll for job status
  useEffect(() => {
    if (polling && currentJob) {
      const interval = setInterval(async () => {
        try {
          const status = await getJobStatus(currentJob)
          setJobStatus(status)
          
          // Stop polling if job is complete or failed
          if (status.status === 'completed' || status.status === 'failed') {
            setPolling(false)
          }
        } catch (error) {
          console.error('Error fetching job status:', error)
        }
      }, 2000) // Poll every 2 seconds

      return () => clearInterval(interval)
    }
  }, [polling, currentJob])

  const loadConfig = async () => {
    try {
      const data = await getConfig()
      setConfig(data)
      // Set default values
      if (data.models.length > 0) setSelectedModel(data.models[0])
      if (data.domains.length > 0) setSelectedDomain(data.domains[0])
      setLoading(false)
    } catch (error) {
      console.error('Error loading config:', error)
      setLoading(false)
    }
  }

  const handleRunPipeline = async () => {
    if (!selectedModel || !selectedDomain || selectedTask === null) {
      alert('Please select all required fields')
      return
    }

    try {
      const response = await runPipeline({
        model: selectedModel,
        temperature: temperature,
        domain: selectedDomain,
        task_id: selectedTask,
        run_id: runId
      })

      setCurrentJob(response.job_id)
      setJobStatus({
        status: 'pending',
        logs: ['Pipeline started...'],
        progress: 0
      })
      setPolling(true)
    } catch (error) {
      console.error('Error starting pipeline:', error)
      alert('Failed to start pipeline: ' + error.message)
    }
  }

  if (loading) {
    return (
      <div className="app">
        <div className="loading">Loading configuration...</div>
      </div>
    )
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-container">
          <div className="header-content">
            <h1>LLM-PDDL Pipeline</h1>
            <p>Automated Classical Planning with Large Language Models</p>
          </div>
        </div>
      </header>

      <div className="app-content">
        <div className="config-panel">
          <h2>Configuration</h2>
          
          <ModelSelector
            models={config?.models || []}
            selected={selectedModel}
            onChange={setSelectedModel}
          />
          
          <TemperatureSlider
            value={temperature}
            onChange={setTemperature}
            min={config?.temperature_min || 0.0}
            max={config?.temperature_max || 1.0}
          />
          
          <DomainSelector
            domains={config?.domains || []}
            selected={selectedDomain}
            onChange={(domain) => {
              setSelectedDomain(domain)
              setSelectedTask(null) // Reset task when domain changes
            }}
          />
          
          {selectedDomain && (
            <TaskSelector
              tasks={config?.domain_tasks[selectedDomain] || []}
              selected={selectedTask}
              onChange={setSelectedTask}
            />
          )}
          
          <div className="form-group">
            <label>Run ID:</label>
            <input
              type="text"
              value={runId}
              onChange={(e) => setRunId(e.target.value)}
              placeholder="run1"
            />
          </div>
          
          <RunButton
            onClick={handleRunPipeline}
            disabled={!selectedModel || !selectedDomain || selectedTask === null || polling}
            isRunning={polling}
          />
        </div>

        <div className="results-panel">
          <ProgressLog
            jobStatus={jobStatus}
            jobId={currentJob}
          />
        </div>
      </div>
    </div>
  )
}

export default App
