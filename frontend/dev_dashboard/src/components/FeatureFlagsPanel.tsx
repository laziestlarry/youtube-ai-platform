import React, { useEffect, useState } from "react";
import api from "../services/api";

const FeatureFlagsPanel: React.FC = () => {
  const [flags, setFlags] = useState<any[]>([]);

  useEffect(() => {
    api.get("/internal/feature-flags").then((res) => setFlags(res.data));
  }, []);

  return (
    <div>
      <h2>Feature Flags</h2>
      <ul>
        {flags.map((flag) => (
          <li key={flag.name}>
            {flag.name}: {flag.enabled ? "ON" : "OFF"}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default FeatureFlagsPanel; 