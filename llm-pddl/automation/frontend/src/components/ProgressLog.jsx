function ProgressLog({ jobStatus, jobId }) {
  if (!jobStatus) {
    return (
      <div className="progress-log">
        <h2>Pipeline Status</h2>
        <p className="no-job">No pipeline running. Configure and click "Run Pipeline" to start.</p>
      </div>
    )
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return '#22c55e'
      case 'failed':
        return '#ef4444'
      case 'running':
        return '#3b82f6'
      case 'pending':
        return '#f59e0b'
      default:
        return '#64748b'
    }
  }

  const getStepName = (step) => {
    const stepNames = {
      'generate_pddl': 'Generate PDDL Problem',
      'generate_plan': 'Generate Plan (Fast Downward)',
      'validate_plan': 'Validate Plan (VAL)',
      'generate_optimal': 'Generate Optimal Plan',
      'calculate_gap': 'Calculate Optimal Gap'
    }
    return stepNames[step] || step
  }

  const getStepIcon = (step) => {
    const icons = {
      'generate_pddl': '1',
      'generate_plan': '2',
      'validate_plan': '3',
      'generate_optimal': '4',
      'calculate_gap': '5'
    }
    return icons[step] || '·'
  }

  const allSteps = ['generate_pddl', 'generate_plan', 'validate_plan', 'generate_optimal', 'calculate_gap']
  
  const getStepStatus = (step) => {
    const stepIndex = allSteps.indexOf(step)
    const currentIndex = allSteps.indexOf(jobStatus.current_step)
    
    if (jobStatus.status === 'completed') {
      return 'completed'
    }
    if (jobStatus.status === 'failed') {
      if (stepIndex < currentIndex) return 'completed'
      if (stepIndex === currentIndex) return 'failed'
      return 'pending'
    }
    if (stepIndex < currentIndex) return 'completed'
    if (stepIndex === currentIndex) return 'running'
    return 'pending'
  }

  const getLevelColor = (level) => {
    switch (level) {
      case 'ERROR':
        return '#ef4444'
      case 'WARNING':
        return '#f59e0b'
      case 'INFO':
        return '#3b82f6'
      default:
        return '#64748b'
    }
  }

  return (
    <div className="progress-log">
      <h2>Pipeline Status</h2>
      
      <div className="status-header">
        <div className="status-badge" style={{ backgroundColor: getStatusColor(jobStatus.status) }}>
          {jobStatus.status.toUpperCase()}
        </div>
        {jobId && <div className="job-id">Job ID: {jobId.substring(0, 8)}...</div>}
      </div>

      {/* Step Indicators */}
      <div className="step-indicators">
        {allSteps.map((step, index) => {
          const stepStatus = getStepStatus(step)
          return (
            <div key={step} className={`step-indicator step-${stepStatus}`}>
              <div className="step-icon">{getStepIcon(step)}</div>
              <div className="step-name">{getStepName(step)}</div>
              <div className="step-status-icon">
                {stepStatus === 'completed' && '✓'}
                {stepStatus === 'running' && '●'}
                {stepStatus === 'failed' && '✕'}
              </div>
            </div>
          )
        })}
      </div>

      {jobStatus.progress !== undefined && jobStatus.progress >= 0 && (
        <div className="progress-bar-container">
          <div className="progress-bar" style={{ width: `${jobStatus.progress}%` }}>
            {jobStatus.progress}%
          </div>
        </div>
      )}

      {jobStatus.results && Object.keys(jobStatus.results).length > 0 && (
        <div className="results">
          <h3>Results:</h3>
          {jobStatus.results.validation && (
            <div className="result-item">
              <strong>Validation:</strong> 
              <span className={`validation-${jobStatus.results.validation}`}>
                {jobStatus.results.validation}
              </span>
            </div>
          )}
          {jobStatus.results.optimal_gap !== undefined && (
            <div className="result-item">
              <strong>Optimal Gap:</strong> {jobStatus.results.optimal_gap.toFixed(2)}
            </div>
          )}
        </div>
      )}

      <div className="logs">
        <h3>Logs ({jobStatus.messages?.length || jobStatus.logs?.length || 0}):</h3>
        <div className="log-content">
          {jobStatus.messages && jobStatus.messages.length > 0 ? (
            jobStatus.messages.map((msg, index) => (
              <div key={index} className="log-entry">
                <span className="log-timestamp">{msg.timestamp}</span>
                <span className="log-level" style={{ color: getLevelColor(msg.level) }}>
                  [{msg.level}]
                </span>
                <span className="log-message">{msg.message}</span>
              </div>
            ))
          ) : jobStatus.logs && jobStatus.logs.length > 0 ? (
            jobStatus.logs.map((log, index) => (
              <div key={index} className="log-entry">{log}</div>
            ))
          ) : (
            <div className="log-entry">Waiting for logs...</div>
          )}
        </div>
      </div>

      {jobStatus.duration && (
        <div className="duration">
          <strong>Duration:</strong> {jobStatus.duration.toFixed(2)}s
        </div>
      )}
    </div>
  )
}

export default ProgressLog
