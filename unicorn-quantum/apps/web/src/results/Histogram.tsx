import React from 'react';
// Counts/probability histogram for measurement results.
export const Histogram: React.FC<{ counts: Record<string, number> }> = ({ counts }) => {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="histogram" data-testid="histogram">
      {Object.entries(counts).map(([label, count]) => (
        <div key={label} className="hist-bar">
          <span className="hist-label">{label}</span>
          <div className="hist-fill" style={{ height: `${(count / total) * 100}%` }} />
          <span className="hist-value">{(count / total).toFixed(3)}</span>
        </div>
      ))}
    </div>
  );
};
export default Histogram;
