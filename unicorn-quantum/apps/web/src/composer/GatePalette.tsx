import React from 'react';
// Gate drag-and-drop palette — available gates for circuit composition.
const GATES = ['H', 'X', 'Y', 'Z', 'CX', 'CZ', 'Measure'];
export const GatePalette: React.FC<{ onDragStart?: (gate: string) => void }> = ({ onDragStart }) => {
  return (
    <div className="gate-palette" data-testid="gate-palette">
      {GATES.map(g => (
        <div key={g} className="gate-chip" draggable onDragStart={() => onDragStart?.(g)}>
          {g}
        </div>
      ))}
    </div>
  );
};
export default GatePalette;
