import React from 'react';
import CapabilityBadge from '../components/CapabilityBadge';

const Dashboard: React.FC = () => (
  <div className="dashboard">
    <h2>System Dashboard</h2>
    <div className="capability-grid">
      <CapabilityBadge module="Quantum" level="Simulated" />
      <CapabilityBadge module="AI Orchestration" level="Implemented" />
      <CapabilityBadge module="NPC Sandbox" level="Implemented" />
      <CapabilityBadge module="File Transfer" level="Implemented" />
      <CapabilityBadge module="Edge Runtime" level="Implemented" />
      <CapabilityBadge module="Emulation" level="Implemented" />
    </div>
  </div>
);
export default Dashboard;
