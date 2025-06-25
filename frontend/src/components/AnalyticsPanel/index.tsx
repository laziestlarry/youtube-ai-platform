import React, { useEffect, useState } from 'react';
import {
  fetchAnalyticsSummary, fetchRevenueData, fetchGrowthData, fetchEngagementData
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar
} from 'recharts';

type AnalyticsSummary = {
  channels: number;
  users: number;
  videos: number;
  tasks: number;
  agents: number;
};

const AnalyticsPanel: React.FC = () => {
  const [summary, setSummary] = useState<AnalyticsSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [revenueData, setRevenueData] = useState<Array<{month: string; revenue: number}>>([]);
  const [growthData, setGrowthData] = useState<Array<{month: string; users: number}>>([]);
  const [engagementData, setEngagementData] = useState<Array<{month: string; engagement: number}>>([]);
  const [chartsLoading, setChartsLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    fetchAnalyticsSummary().then(data => {
      setSummary(data);
      setLoading(false);
    });
    setChartsLoading(true);
    Promise.all([
      fetchRevenueData(),
      fetchGrowthData(),
      fetchEngagementData()
    ]).then(([revenue, growth, engagement]) => {
      setRevenueData(revenue);
      setGrowthData(growth);
      setEngagementData(engagement);
      setChartsLoading(false);
    });
  }, []);

  if (loading || chartsLoading) return <div>Loading analytics...</div>;
  if (!summary) return <div>No analytics data available.</div>;

  return (
    <div>
      <h2>Analytics Panel</h2>
      <ul>
        <li>Channels: {summary.channels}</li>
        <li>Users: {summary.users}</li>
        <li>Videos: {summary.videos}</li>
        <li>Tasks: {summary.tasks}</li>
        <li>Agents: {summary.agents}</li>
      </ul>
      <div style={{ display: 'flex', gap: 32, flexWrap: 'wrap', marginTop: 32 }}>
        <div style={{ flex: 1, minWidth: 320 }}>
          <h3>Revenue (Monthly)</h3>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={revenueData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="revenue" stroke="#8884d8" />
            </LineChart>
          </ResponsiveContainer>
        </div>
        <div style={{ flex: 1, minWidth: 320 }}>
          <h3>User Growth</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={growthData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="users" fill="#82ca9d" />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div style={{ flex: 1, minWidth: 320 }}>
          <h3>Engagement</h3>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={engagementData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="engagement" stroke="#ff7300" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsPanel; 