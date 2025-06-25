import React, { useEffect, useState } from "react";
import api from "../services/api";

const SystemHealthPanel: React.FC = () => {
  const [health, setHealth] = useState<any>(null);

  useEffect(() => {
    api.get("/internal/health").then((res) => setHealth(res.data));
  }, []);

  return (
    <div>
      <h2>System Health</h2>
      <pre>{JSON.stringify(health, null, 2)}</pre>
    </div>
  );
};

export default SystemHealthPanel; 