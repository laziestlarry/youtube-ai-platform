import * as React from "react";
import React, { useEffect, useState } from "react";
// import api from "../services/api";

interface AdminUser {
  id: string;
  email: string;
}

const AdminUsersPanel: React.FC = () => {
  const [admins, setAdmins] = useState<AdminUser[]>([]);

  useEffect(() => {
    fetch("/internal/admin-users")
      .then((res) => res.json())
      .then((data) => setAdmins(data));
  }, []);

  return (
    <div>
      <h2>Admin Users</h2>
      <ul>
        {admins.map((user: AdminUser) => (
          <li key={user.id}>{user.email}</li>
        ))}
      </ul>
    </div>
  );
};

export default AdminUsersPanel; 