function TaskSelector({ tasks, selected, onChange }) {
  return (
    <div className="form-group">
      <label>Task Number:</label>
      <select 
        value={selected !== null ? selected : ''} 
        onChange={(e) => onChange(parseInt(e.target.value))}
      >
        <option value="">Select a task...</option>
        {tasks.map((task) => (
          <option key={task} value={task}>
            Task {task} (Plan: p{String(task + 1).padStart(2, '0')})
          </option>
        ))}
      </select>
    </div>
  )
}

export default TaskSelector
