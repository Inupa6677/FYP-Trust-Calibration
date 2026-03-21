function RunButton({ onClick, disabled, isRunning }) {
  return (
    <button
      className={`run-button ${isRunning ? 'running' : ''}`}
      onClick={onClick}
      disabled={disabled}
    >
      {isRunning ? '⏳ Running Pipeline...' : '🚀 Run Pipeline'}
    </button>
  )
}

export default RunButton
