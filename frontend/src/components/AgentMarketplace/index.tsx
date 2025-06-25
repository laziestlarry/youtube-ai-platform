import React, { useEffect, useState } from 'react';
import { fetchAgents, fetchChannels, fetchTasks, createAgent as apiCreateAgent, createTask as apiCreateTask } from '../../services/api';
 
type Agent = {
  id: number;
  name: string;
  type: string;
  skills: string[];
  endpoint: string;
  is_active: boolean;
  tasks_completed?: number;
  rating?: number;
  earnings?: number;
};

type Channel = {
  id: number;
  name: string;
};

type Task = {
  id: number;
  title: string;
};

const AgentMarketplace: React.FC = () => {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [name, setName] = useState('');
  const [type, setType] = useState('human');
  const [skills, setSkills] = useState('');
  const [endpoint, setEndpoint] = useState('');
  const [isActive, setIsActive] = useState(true);
  const [creating, setCreating] = useState(false);
  const [channels, setChannels] = useState<Channel[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [assigning, setAssigning] = useState(false);
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);
  const [selectedChannel, setSelectedChannel] = useState<number | null>(null);
  const [selectedTask, setSelectedTask] = useState<number | null>(null);

  useEffect(() => {
    fetchAgents().then(data => {
      // Add placeholder performance metrics
      setAgents(data.map((agent: Agent) => ({
        ...agent,
        tasks_completed: Math.floor(Math.random() * 50),
        rating: Math.round((Math.random() * 2 + 3) * 10) / 10, // 3.0-5.0
        earnings: Math.floor(Math.random() * 1000),
      })));
      setLoading(false);
    });
    fetchChannels().then(setChannels);
    fetchTasks().then(setTasks);
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setCreating(true);
    try {
      const newAgent = await apiCreateAgent({
        name, type, skills: skills.split(',').map(s => s.trim()).filter(Boolean), endpoint, is_active: isActive,
      });
      setAgents(agents => [...agents, newAgent]);
    } catch (error) {
      alert('Failed to create agent: ' + (error as Error).message);
    } finally {
      setCreating(false);
    }
    setAgents(agents => [...agents, newAgent]);
    setName('');
    setType('human');
    setSkills('');
    setEndpoint('');
    setIsActive(true);
    setCreating(false);
  }; 

  const handleAssign = async (e: React.FormEvent) => {
    e.preventDefault();
    setAssigning(true);
    try {
      // Find the selected task object
      const taskObj = tasks.find(t => t.id === selectedTask);
      if (!selectedAgent || !selectedChannel || !selectedTask || !taskObj) {
        throw new Error('Missing assignment data');
      }
      // Create a new task assignment in backend
      await apiCreateTask({
        video_id: selectedChannel, // using channel as video_id for now
        assigned_to: selectedAgent.id,
        type: taskObj.title,
        status: 'assigned',
        }),
      });
      if (!res.ok) throw new Error('Failed to assign agent');
      // Optionally, refresh tasks list
      fetchTasks().then(setTasks);
    } catch (err) {
      alert('Assignment failed: ' + (err as Error).message);
    } finally {
    setAssigning(false);
    setSelectedAgent(null);
    setSelectedChannel(null);
    setSelectedTask(null);
    }
  };

  if (loading) return <div>Loading agents...</div>;

  return (
    <div>
      <h2>Agent Marketplace</h2>
      <form onSubmit={handleCreate} style={{ marginBottom: 24 }}>
        <input
          value={name}
          onChange={e => setName(e.target.value)}
          placeholder="Agent name"
          required
        />
        <select value={type} onChange={e => setType(e.target.value)}>
          <option value="human">human</option>
          <option value="ai">ai</option>
          <option value="bot">bot</option>
          <option value="lambda">lambda</option>
        </select>
        <input
          value={skills}
          onChange={e => setSkills(e.target.value)}
          placeholder="Skills (comma separated)"
        />
        <input
          value={endpoint}
          onChange={e => setEndpoint(e.target.value)}
          placeholder="Endpoint (for bot/lambda)"
        />
        <label style={{ marginLeft: 8 }}>
          <input
            type="checkbox"
            checked={isActive}
            onChange={e => setIsActive(e.target.checked)}
          />
          Active
        </label>
        <button type="submit" disabled={creating || !name}>
          {creating ? 'Creating...' : 'Create Agent'}
        </button>
      </form>
      <ul>
        {agents.map(agent => (
          <li key={agent.id} style={{ marginBottom: 16 }}>
            <strong>{agent.name}</strong> ({agent.type})<br />
            Skills: {agent.skills.join(', ')}<br />
            Endpoint: {agent.endpoint}<br />
            Active: {agent.is_active ? 'Yes' : 'No'}<br />
            Tasks Completed: {agent.tasks_completed} | Rating: {agent.rating} | Earnings: ${agent.earnings}<br />
            <button onClick={() => setSelectedAgent(agent)} style={{ marginTop: 4 }}>
              Assign to Channel/Task
            </button>
          </li>
        ))}
      </ul>
      {selectedAgent && (
        <form onSubmit={handleAssign} style={{ marginTop: 24, padding: 16, border: '1px solid #ccc', borderRadius: 8 }}>
          <h3>Assign {selectedAgent.name}</h3>
          <label>
            Channel:
            <select value={selectedChannel ?? ''} onChange={e => setSelectedChannel(Number(e.target.value))} required>
              <option value="" disabled>Select channel</option>
              {channels.map(channel => (
                <option key={channel.id} value={channel.id}>{channel.name}</option>
              ))}
            </select>
          </label>
          <label style={{ marginLeft: 16 }}>
            Task:
            <select value={selectedTask ?? ''} onChange={e => setSelectedTask(Number(e.target.value))} required>
              <option value="" disabled>Select task</option>
              {tasks.map(task => (
                <option key={task.id} value={task.id}>{task.title}</option>
              ))}
            </select>
          </label>
          <button type="submit" disabled={assigning || !selectedChannel || !selectedTask} style={{ marginLeft: 16 }}>
            {assigning ? 'Assigning...' : 'Assign'}
          </button>
          <button type="button" onClick={() => setSelectedAgent(null)} style={{ marginLeft: 8 }}>
            Cancel
          </button>
        </form>
      )}
    </div>
  );
};

export default AgentMarketplace; 