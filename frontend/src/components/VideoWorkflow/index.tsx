import React, { useEffect, useState } from 'react';
import { fetchVideos, createVideo as apiCreateVideo } from '../../services/api';
 
type Video = {
  id: number;
  channel_id: number;
  creator_id: number;
  title: string;
  description: string;
  status: string;
};

const VideoWorkflow: React.FC = () => {
  const [videos, setVideos] = useState<Video[]>([]);
  const [loading, setLoading] = useState(true);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [status, setStatus] = useState('draft');
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    fetchVideos().then(data => {
      setVideos(data);
      setLoading(false);
    });
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setCreating(true);
    try {
      const newVideo = await apiCreateVideo({ channel_id: 1, creator_id: 1, title, description, status });
      setVideos(videos => [...videos, newVideo]);
      setTitle('');
      setDescription('');
      setStatus('draft');
    } catch (error) {
      alert('Failed to create video: ' + (error as Error).message);
    } finally { setCreating(false); }
  };

  if (loading) return <div>Loading videos...</div>;

  return (
    <div>
      <h2>Video Workflow</h2>
      <form onSubmit={handleCreate} style={{ marginBottom: 24 }}>
        <input
          value={title}
          onChange={e => setTitle(e.target.value)}
          placeholder="Video title"
          required
        />
        <input
          value={description}
          onChange={e => setDescription(e.target.value)}
          placeholder="Description"
        />
        <select value={status} onChange={e => setStatus(e.target.value)}>
          <option value="draft">draft</option>
          <option value="published">published</option>
        </select>
        <button type="submit" disabled={creating || !title}>
          {creating ? 'Creating...' : 'Create Video'}
        </button>
      </form>
      <ul>
        {videos.map(video => (
          <li key={video.id}>
            <strong>{video.title}</strong> (Channel: {video.channel_id}, Creator: {video.creator_id})<br />
            Status: {video.status}<br />
            <span>{video.description}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default VideoWorkflow; 