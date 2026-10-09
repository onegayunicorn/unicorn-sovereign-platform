// N02 Cognitive Hive mock — agent twin statuses.
export interface AgentTwinStatus {
  agentId: string;
  status: 'idle' | 'running' | 'blocked' | 'killed';
  lastHeartbeat: number;
}

export function mockAgentStatuses(): AgentTwinStatus[] {
  const now = Date.now();
  return [
    { agentId: 'architect', status: 'idle', lastHeartbeat: now },
    { agentId: 'integrator', status: 'running', lastHeartbeat: now - 2000 },
    { agentId: 'security', status: 'idle', lastHeartbeat: now - 5000 },
    { agentId: 'quantum-hpc', status: 'idle', lastHeartbeat: now - 1000 },
    { agentId: 'photonics', status: 'blocked', lastHeartbeat: now - 60000 },
    { agentId: 'repository', status: 'idle', lastHeartbeat: now },
  ];
}
