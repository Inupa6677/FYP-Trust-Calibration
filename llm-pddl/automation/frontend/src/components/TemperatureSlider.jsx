function TemperatureSlider({ value, onChange, min, max }) {
  return (
    <div className="form-group">
      <label>
        Temperature: <span className="value">{value.toFixed(1)}</span>
      </label>
      <input
        type="range"
        min={min}
        max={max}
        step={0.1}
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        className="temperature-slider"
      />
      <div className="range-labels">
        <span>Deterministic ({min})</span>
        <span>Creative ({max})</span>
      </div>
    </div>
  )
}

export default TemperatureSlider
