const API_BASE = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';

export async function fetchChannels() {
  const res = await fetch(`${API_BASE}/channels/`);
  return res.json();
}

export async function fetchUsers() {
  const res = await fetch(`${API_BASE}/users/`);
  return res.json();
}

export async function fetchVideos() {
  const res = await fetch(`${API_BASE}/videos/`);
  return res.json();
}

export async function fetchTasks() {
  const res = await fetch(`${API_BASE}/tasks/`);
  return res.json();
}

export async function fetchAgents() {
  const res = await fetch(`${API_BASE}/agents/`);
  return res.json();
}

export async function fetchAnalyticsSummary() {
  const res = await fetch(`${API_BASE}/analytics/summary`);
  return res.json();
}

export async function createAgent(agentData: any) {
  const res = await fetch(`${API_BASE}/agents/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(agentData),
  });
  if (!res.ok) {
    const errorData = await res.json();
    throw new Error(errorData.detail || 'Failed to create agent');
  }
  return res.json();
}

export async function createTask(taskData: any) {
  const res = await fetch(`${API_BASE}/tasks/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(taskData),
  });
  if (!res.ok) {
    const errorData = await res.json();
    throw new Error(errorData.detail || 'Failed to create task');
  }
  return res.json();
}

export async function createChannel(channelData: any) {
  const res = await fetch(`${API_BASE}/channels/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(channelData),
  });
  if (!res.ok) {
    const errorData = await res.json();
    throw new Error(errorData.detail || 'Failed to create channel');
  }
  return res.json();
}

export async function createUser(userData: any) {
  const res = await fetch(`${API_BASE}/users/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userData),
  });
  if (!res.ok) {
    const errorData = await res.json();
    throw new Error(errorData.detail || 'Failed to create user');
  }
  return res.json();
}

export async function createVideo(videoData: any) {
  const res = await fetch(`${API_BASE}/videos/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(videoData),
  });
  if (!res.ok) {
    const errorData = await res.json();
    throw new Error(errorData.detail || 'Failed to create video');
  }
  return res.json();
}

// Analytics specific fetches (moved from AnalyticsPanel)
export async function fetchRevenueData() {
  const res = await fetch(`${API_BASE}/analytics/revenue`);
  return res.json();
}
export async function fetchGrowthData() {
  const res = await fetch(`${API_BASE}/analytics/growth`);
  return res.json();
}
export async function fetchEngagementData() {
  const res = await fetch(`${API_BASE}/analytics/engagement`);
  return res.json();
}
} 