import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';

const ChannelDashboard = () => <div><h2>Channel Dashboard</h2></div>;
const VideoWorkflow = () => <div><h2>Video Workflow</h2></div>;
const UserManagement = () => <div><h2>User Management</h2></div>;
const TaskBoard = () => <div><h2>Task Board</h2></div>;
const AgentMarketplace = () => <div><h2>Agent Marketplace</h2></div>;
const AnalyticsPanel = () => <div><h2>Analytics Panel</h2></div>;

function App() {
  return (
    <Router>
      <nav style={{ display: 'flex', gap: 16, padding: 16, background: '#f0f0f0' }}>
        <Link to="/">Channel Dashboard</Link>
        <Link to="/workflow">Video Workflow</Link>
        <Link to="/users">User Management</Link>
        <Link to="/tasks">Task Board</Link>
        <Link to="/agents">Agent Marketplace</Link>
        <Link to="/analytics">Analytics Panel</Link>
      </nav>
      <Routes>
        <Route path="/" element={<ChannelDashboard />} />
        <Route path="/workflow" element={<VideoWorkflow />} />
        <Route path="/users" element={<UserManagement />} />
        <Route path="/tasks" element={<TaskBoard />} />
        <Route path="/agents" element={<AgentMarketplace />} />
        <Route path="/analytics" element={<AnalyticsPanel />} />
      </Routes>
    </Router>
  );
}

export default App; 