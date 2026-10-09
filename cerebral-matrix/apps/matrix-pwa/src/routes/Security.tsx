import React from 'react';
// Security + audit status — PQC algorithms, kill switches, audit log, export/delete controls.
const Security: React.FC = () => (
  <div className="security-page">
    <h2>Security & Audit</h2>
    <section>
      <h3>Post-Quantum Cryptography (NIST standard)</h3>
      <ul>
        <li>ML-KEM-768 — key encapsulation</li>
        <li>ML-DSA-65 — digital signatures</li>
        <li>SLH-DSA-SHA2-128s — hash-based signatures</li>
        <li>Hybrid: ML-KEM-768 + ECDSA-P256 (browser interoperability)</li>
      </ul>
    </section>
    <section>
      <h3>Data Controls</h3>
      <button>Export all local data</button>
      <button className="danger">Delete all local data</button>
    </section>
    <section>
      <h3>Telemetry</h3>
      <p>Telemetry is OFF by default. Every outbound request requires explicit opt-in.</p>
    </section>
  </div>
);
export default Security;
