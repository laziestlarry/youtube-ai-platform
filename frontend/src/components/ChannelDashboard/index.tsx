import React, { useEffect, useState } from 'react';
import { fetchChannels, createChannel as apiCreateChannel } from '../../services/api';
 
type Channel = {
  id: number;
  name: string;
  description: string;
  owner_id: number;
};

const ChannelDashboard: React.FC = () => {
  const [channels, setChannels] = useState<Channel[]>([]);
  const [loading, setLoading] = useState(true);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    fetchChannels().then(data => {
      setChannels(data);
      setLoading(false);
    });
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setCreating(true);
    try {
      const newChannel = await apiCreateChannel({ name, description, owner_id: 1 });
      setChannels(channels => [...channels, newChannel]);
      setName('');
      setDescription('');
    } catch (error) {
      alert('Failed to create channel: ' + (error as Error).message);
    } finally { setCreating(false); }
  };

  if (loading) return <div>Loading channels...</div>;

  return (
    <div>
      <h2>Channel Dashboard</h2>
      <form onSubmit={handleCreate} style={{ marginBottom: 24 }}>
        <input
          value={name}
          onChange={e => setName(e.target.value)}
          placeholder="Channel name"
          required
        />
        <input
          value={description}
          onChange={e => setDescription(e.target.value)}
          placeholder="Description"
        />
        <button type="submit" disabled={creating || !name}>
          {creating ? 'Creating...' : 'Create Channel'}
        </button>
      </form>
      <ul>
        {channels.map(channel => (
          <li key={channel.id}>
            <strong>{channel.name}</strong> (Owner: {channel.owner_id})<br />
            <span>{channel.description}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ChannelDashboard; 