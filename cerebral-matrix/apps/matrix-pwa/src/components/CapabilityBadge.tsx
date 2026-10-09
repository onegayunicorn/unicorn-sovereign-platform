import React from 'react';
// Capability label badge — Demonstrated/Prototype/Simulated/Reported/Proposed/Implemented.
const COLORS: Record<string, string> = {
  Demonstrated: '#22c55e', Prototype: '#eab308', Simulated: '#3b82f6',
  Reported: '#a855f7', Proposed: '#64748b', Implemented: '#06b6d4',
};
const CapabilityBadge: React.FC<{ module: string; level: string }> = ({ module, level }) => (
  <div className="capability-badge" style={{ borderColor: COLORS[level] || '#64748b' }}>
    <span className="module-name">{module}</span>
    <span className="level" style={{ color: COLORS[level] || '#64748b' }}>{level}</span>
  </div>
);
export default CapabilityBadge;
