import React, { useEffect, useState } from "react";
import api from "../services/api";

const AdminUsersPanel: React.FC = () => {
  const [admins, setAdmins] = useState<any[]>([]);

  useEffect(() => {
    api.get("/internal/admin-users").then((res) => setAdmins(res.data));
  }, []);

  return (
    <div>
      <h2>Admin Users</h2>
      <ul>
        {admins.map((user) => (
          <li key={user.id}>{user.email}</li>
        ))}
      </ul>
    </div>
  );
};

export default AdminUsersPanel; 