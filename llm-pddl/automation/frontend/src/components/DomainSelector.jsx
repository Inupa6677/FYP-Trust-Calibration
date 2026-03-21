function DomainSelector({ domains, selected, onChange }) {
  return (
    <div className="form-group">
      <label>Planning Domain:</label>
      <select value={selected} onChange={(e) => onChange(e.target.value)}>
        {domains.map((domain) => (
          <option key={domain} value={domain}>
            {domain.charAt(0).toUpperCase() + domain.slice(1)}
          </option>
        ))}
      </select>
    </div>
  )
}

export default DomainSelector
