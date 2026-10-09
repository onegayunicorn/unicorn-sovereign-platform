import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Dashboard from '../routes/Dashboard';
import Workbench from '../routes/Workbench';
import NpcSandbox from '../routes/NpcSandbox';
import Security from '../routes/Security';
import OfflineIndicator from '../components/OfflineIndicator';

const App: React.FC = () => (
  <BrowserRouter>
    <div className="app-shell">
      <nav className="sidebar">
        <h1>Matrix OS</h1>
        <Link to="/">Dashboard</Link>
        <Link to="/workbench">Circuit Workbench</Link>
        <Link to="/npc">NPC Sandbox</Link>
        <Link to="/security">Security & Audit</Link>
      </nav>
      <main className="content">
        <OfflineIndicator />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/workbench" element={<Workbench />} />
          <Route path="/npc" element={<NpcSandbox />} />
          <Route path="/security" element={<Security />} />
        </Routes>
      </main>
    </div>
  </BrowserRouter>
);
export default App;
