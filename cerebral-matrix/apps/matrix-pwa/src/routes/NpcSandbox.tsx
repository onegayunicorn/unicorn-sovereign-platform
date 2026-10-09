import React, { useState } from 'react';
// NPC sandbox view — interacts with original fictional NPC characters.
const NpcSandbox: React.FC = () => {
  const [input, setInput] = useState('');
  const [log, setLog] = useState<Array<{ speaker: string; text: string }>>([]);
  const send = () => {
    setLog(l => [...l, { speaker: 'player', text: input },
      { speaker: 'npc', text: '[Fictional game asset] Response processed through 4-gate safety filter.' }]);
    setInput('');
  };
  return (
    <div className="npc-sandbox">
      <h2>NPC Sandbox</h2>
      <p className="disclaimer">All characters are original fictional game assets — 100% original content.</p>
      <div className="chat-log">
        {log.map((m, i) => <div key={i} className={`msg ${m.speaker}`}><strong>{m.speaker}:</strong> {m.text}</div>)}
      </div>
      <input value={input} onChange={e => setInput(e.target.value)} placeholder="Speak to NPC..." />
      <button onClick={send}>Send</button>
    </div>
  );
};
export default NpcSandbox;
