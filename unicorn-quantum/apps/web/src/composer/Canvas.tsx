import React from 'react';
// Visual circuit editor canvas — renders qubit lanes and gate operations.
export const Canvas: React.FC<{ numQubits: number }> = ({ numQubits }) => {
  return (
    <div className="circuit-canvas" data-testid="circuit-canvas">
      {Array.from({ length: numQubits }).map((_, i) => (
        <div key={i} className="qubit-lane" data-qubit={i}>
          <span className="qubit-label">q[{i}]</span>
          <div className="wire" />
        </div>
      ))}
    </div>
  );
};
export default Canvas;
