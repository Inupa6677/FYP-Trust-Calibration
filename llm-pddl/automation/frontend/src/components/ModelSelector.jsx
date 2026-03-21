function ModelSelector({ models, selected, onChange }) {
  return (
    <div className="form-group">
      <label>LLM Model:</label>
      <select value={selected} onChange={(e) => onChange(e.target.value)}>
        {models.map((model) => (
          <option key={model} value={model}>
            {model}
          </option>
        ))}
      </select>
    </div>
  )
}

export default ModelSelector
