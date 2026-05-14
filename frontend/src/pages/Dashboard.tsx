import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { format } from 'date-fns';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { useAuth } from '../context/AuthContext';
import { predictionsAPI } from '../api/predictions';
import { MetricCard } from '../components/ui/MetricCard';
import { Badge } from '../components/ui/Badge';

export const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState<any>(null);
  const [predictions, setPredictions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsRes, predsRes] = await Promise.all([
          predictionsAPI.getStatsSummary(),
          predictionsAPI.getAll(),
        ]);
        setStats(statsRes.data);
        setPredictions(predsRes.data.slice(0, 5)); // Last 5 for recent table
      } catch (err) {
        console.error('Failed to load dashboard data', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex h-full items-center justify-center">
        <div className="animate-pulse-slow flex flex-col items-center">
          <div className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin mb-4"></div>
          <p className="text-navy-700 font-medium">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  const getRiskBadge = (category: string) => {
    switch (category) {
      case 'Low': return <Badge variant="success">Low Risk</Badge>;
      case 'Medium': return <Badge variant="warning">Medium Risk</Badge>;
      case 'High': return <Badge variant="danger">High Risk</Badge>;
      default: return <Badge>{category}</Badge>;
    }
  };

  // Format history for chart (reverse to chronological order)
  const chartData = [...(stats?.history || [])].reverse().map(item => ({
    ...item,
    dateLabel: format(new Date(item.date), 'MMM d'),
  }));

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in">
      {/* Welcome Banner */}
      <div className="bg-navy-900 rounded-2xl p-8 text-white mb-8 bg-grain relative overflow-hidden">
        <div className="relative z-10">
          <h1 className="text-3xl font-heading font-bold mb-2">
            Good morning, {user?.full_name || user?.username || 'User'}.
          </h1>
          <p className="text-white/80">
            {stats?.total_predictions > 0
              ? `Your last prediction was on ${format(new Date(stats.history[0]?.date || new Date()), 'MMMM do, yyyy')}.`
              : "Welcome to AyuPulse. Run your first prediction to get started."}
          </p>
          <div className="mt-6">
            <Link to="/predictions/new" className="btn-primary inline-flex items-center gap-2">
              New Prediction
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
              </svg>
            </Link>
          </div>
        </div>
        <div className="absolute right-0 bottom-0 opacity-10 pointer-events-none">
          <svg width="300" height="300" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
          </svg>
        </div>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <MetricCard 
          title="Total Predictions" 
          value={stats?.total_predictions || 0}
          icon={<svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>}
        />
        <MetricCard 
          title="High Risk Alerts" 
          value={stats?.high_risk_alerts || 0}
          icon={<svg className="w-6 h-6 text-risk-high" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>}
        />
        <MetricCard 
          title="Last Risk Score" 
          value={`${stats?.last_risk_score ? Math.round(stats.last_risk_score) : 0}%`}
          subtitle="From latest prediction"
          icon={<svg className="w-6 h-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>}
        />
        <MetricCard 
          title="Days Since Last Check" 
          value={stats?.days_since_last || 0}
          icon={<svg className="w-6 h-6 text-navy-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Recent Predictions Table */}
        <div className="lg:col-span-2 card-base">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-lg font-heading font-semibold">Recent Predictions</h2>
            <Link to="/history" className="text-sm font-medium text-primary hover:text-primary-hover">View all</Link>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs text-navy-700 uppercase bg-navy-50 rounded-t-lg">
                <tr>
                  <th className="px-4 py-3 rounded-tl-lg">Date</th>
                  <th className="px-4 py-3">Subject</th>
                  <th className="px-4 py-3">Risk Level</th>
                  <th className="px-4 py-3">Modalities</th>
                  <th className="px-4 py-3 rounded-tr-lg"></th>
                </tr>
              </thead>
              <tbody>
                {predictions.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="px-4 py-8 text-center text-navy-700">
                      No predictions found.
                    </td>
                  </tr>
                ) : (
                  predictions.map((p) => (
                    <tr key={p.id} className="border-b border-navy-50 hover:bg-navy-50/50 transition-colors">
                      <td className="px-4 py-4 whitespace-nowrap text-navy-700">
                        {format(new Date(p.created_at), 'MMM d, yyyy')}
                      </td>
                      <td className="px-4 py-4 font-medium text-navy-900">
                        {p.subject_name}
                      </td>
                      <td className="px-4 py-4">
                        {getRiskBadge(p.risk_category)}
                      </td>
                      <td className="px-4 py-4">
                        <div className="flex gap-1">
                          {p.modalities_used.map((mod: string) => (
                            <span key={mod} className="w-6 h-6 rounded bg-navy-100 flex items-center justify-center text-xs font-bold text-navy-700" title={mod}>
                              {mod[0].toUpperCase()}
                            </span>
                          ))}
                        </div>
                      </td>
                      <td className="px-4 py-4 text-right">
                        <Link to={`/predictions/${p.id}`} className="text-primary hover:text-primary-hover font-medium text-sm">
                          View Report &rarr;
                        </Link>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Risk Trend Chart */}
        <div className="card-base flex flex-col">
          <h2 className="text-lg font-heading font-semibold mb-6">Risk Trend</h2>
          <div className="flex-grow min-h-[250px] relative w-full">
            {chartData.length < 2 ? (
              <div className="absolute inset-0 flex items-center justify-center flex-col text-center px-4">
                <svg className="w-12 h-12 text-navy-400 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
                </svg>
                <p className="text-sm text-navy-700">Not enough data to show a trend. Complete at least 2 predictions.</p>
              </div>
            ) : (
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={chartData} margin={{ top: 5, right: 10, left: -20, bottom: 5 }}>
                  <XAxis 
                    dataKey="dateLabel" 
                    axisLine={false} 
                    tickLine={false} 
                    tick={{ fill: '#64748b', fontSize: 12 }} 
                    dy={10}
                  />
                  <YAxis 
                    domain={[0, 100]} 
                    axisLine={false} 
                    tickLine={false} 
                    tick={{ fill: '#64748b', fontSize: 12 }}
                  />
                  <Tooltip 
                    contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}
                    formatter={(value: number) => [`${value.toFixed(1)}%`, 'Risk Score']}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="score" 
                    stroke="#E24B4A" 
                    strokeWidth={3} 
                    dot={{ fill: '#E24B4A', strokeWidth: 2, r: 4, stroke: 'white' }} 
                    activeDot={{ r: 6 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};