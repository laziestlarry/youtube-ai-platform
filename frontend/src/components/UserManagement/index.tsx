import React, { useEffect, useState } from 'react';
import { fetchUsers, createUser as apiCreateUser } from '../../services/api';
 
type User = {
  id: number; // This should match the UserOut model from the backend
  email: string;
  username: string;
  role: string;
};

const UserManagement: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('creator');
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    fetchUsers().then(data => {
      setUsers(data);
      setLoading(false);
    });
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setCreating(true);
    try {
      const newUser = await apiCreateUser({ email, username, password, role });
      setUsers(users => [...users, newUser]);
      setEmail('');
      setUsername('');
      setPassword('');
      setRole('creator');
    } catch (error) {
      alert('Failed to create user: ' + (error as Error).message);
    } finally { setCreating(false); }
  };

  if (loading) return <div>Loading users...</div>;

  return (
    <div>
      <h2>User Management</h2>
      <form onSubmit={handleCreate} style={{ marginBottom: 24 }}>
        <input
          value={email}
          onChange={e => setEmail(e.target.value)}
          placeholder="Email"
          required
        />
        <input
          value={username}
          onChange={e => setUsername(e.target.value)}
          placeholder="Username"
          required
        />
        <input
          value={password}
          onChange={e => setPassword(e.target.value)}
          placeholder="Password"
          type="password"
          required
        />
        <select value={role} onChange={e => setRole(e.target.value)}>
          <option value="creator">creator</option>
          <option value="editor">editor</option>
          <option value="admin">admin</option>
        </select>
        <button type="submit" disabled={creating || !email || !username || !password}>
          {creating ? 'Creating...' : 'Create User'}
        </button>
      </form>
      <ul>
        {users.map(user => (
          <li key={user.id}>
            <strong>{user.username}</strong> ({user.email})<br />
            Role: {user.role}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default UserManagement; 