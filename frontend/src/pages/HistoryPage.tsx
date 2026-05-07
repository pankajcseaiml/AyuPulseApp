import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { format } from 'date-fns';
import { predictionsAPI } from '../api/predictions';
import { Badge } from '../components/ui/Badge';

export const HistoryPage: React.FC = () => {
  const [predictions, setPredictions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const loadHistory = async () => {
    try {
      setLoading(true);
      const res = await predictionsAPI.getAll();
      setPredictions(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const handleDelete = async (id: string) => {
    if (confirm('Are you sure you want to delete this prediction?')) {
      try {
        await predictionsAPI.delete(id);
        loadHistory();
      } catch (err) {
        alert('Failed to delete prediction');
      }
    }
  };

  const getRiskBadge = (category: string) => {
    switch (category) {
      case 'Low': return <Badge variant="success">Low Risk</Badge>;
      case 'Medium': return <Badge variant="warning">Medium Risk</Badge>;
      case 'High': return <Badge variant="danger">High Risk</Badge>;
      default: return <Badge>{category}</Badge>;
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-heading font-bold text-navy-900 mb-2">Prediction History</h1>
          <p className="text-navy-800">View and manage all past cardiovascular risk assessments.</p>
        </div>
        <Link to="/predictions/new" className="btn-primary flex items-center gap-2">
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" /></svg>
          New Assessment
        </Link>
      </div>

      <div className="card-base">
        {loading ? (
          <div className="p-12 text-center text-navy-700">Loading history...</div>
        ) : predictions.length === 0 ? (
          <div className="py-16 text-center">
            <svg className="w-16 h-16 text-navy-300 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <h3 className="text-lg font-medium text-navy-900 mb-1">No predictions found</h3>
            <p className="text-navy-700 mb-6">You haven't run any risk assessments yet.</p>
            <Link to="/predictions/new" className="btn-primary">Run First Prediction</Link>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs text-navy-700 uppercase bg-navy-50 border-b border-navy-100">
                <tr>
                  <th className="px-6 py-4">Date</th>
                  <th className="px-6 py-4">Subject</th>
                  <th className="px-6 py-4">Risk Level</th>
                  <th className="px-6 py-4">Score</th>
                  <th className="px-6 py-4">Modalities</th>
                  <th className="px-6 py-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-navy-50">
                {predictions.map((p) => (
                  <tr key={p.id} className="hover:bg-navy-50/50 transition-colors">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="font-medium text-navy-900">{format(new Date(p.created_at), 'MMM d, yyyy')}</div>
                      <div className="text-xs text-navy-700">{format(new Date(p.created_at), 'h:mm a')}</div>
                    </td>
                    <td className="px-6 py-4 font-medium text-navy-900">
                      {p.subject_name}
                    </td>
                    <td className="px-6 py-4">
                      {getRiskBadge(p.risk_category)}
                    </td>
                    <td className="px-6 py-4 font-semibold text-navy-800">
                      {(p.risk_score * 100).toFixed(1)}%
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex gap-1">
                        {p.modalities_used.map((mod: string) => (
                          <span key={mod} className="w-6 h-6 rounded bg-navy-100 flex items-center justify-center text-[10px] font-bold text-navy-800 uppercase tracking-wider" title={mod}>
                            {mod.substring(0, 3)}
                          </span>
                        ))}
                      </div>
                    </td>
                    <td className="px-6 py-4 text-right space-x-3 whitespace-nowrap">
                      <Link to={`/predictions/${p.id}`} className="text-primary hover:text-primary-hover font-medium">
                        View Report
                      </Link>
                      <button onClick={() => handleDelete(p.id)} className="text-red-500 hover:text-red-700 font-medium ml-4">
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};
