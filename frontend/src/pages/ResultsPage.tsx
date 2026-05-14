import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { format } from 'date-fns';
import { predictionsAPI } from '../api/predictions';
import { RiskMeter } from '../components/ui/RiskMeter';
import { ShapChart } from '../components/ui/ShapChart';
import { GradCamViewer } from '../components/ui/GradCamViewer';
import { Badge } from '../components/ui/Badge';

export const ResultsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [prediction, setPrediction] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPrediction = async () => {
      try {
        const res = await predictionsAPI.getOne(id!);
        setPrediction(res.data);
      } catch (err: any) {
        // Use the actual error message from the API if available
        const errorMessage = err.message || 'Failed to load prediction results.';
        setError(errorMessage);
      } finally {
        setLoading(false);
      }
    };
    if (id) fetchPrediction();
  }, [id]);

  if (loading) return <div className="p-12 text-center text-navy-700">Loading results...</div>;
  if (error || !prediction) return (
    <div className="p-12 text-center">
      <div className="max-w-md mx-auto">
        <div className="text-red-500 text-lg font-semibold mb-2">Error</div>
        <div className="text-navy-800 mb-4">{error || 'Prediction not found'}</div>
        <Link to="/history" className="text-primary hover:text-primary-dark font-medium">
          ← Back to Prediction History
        </Link>
      </div>
    </div>
  );

  const handlePrint = () => {
    window.print();
  };

  const getRiskColor = (category: string) => {
    switch (category) {
      case 'Low': return 'text-risk-low';
      case 'Medium': return 'text-risk-medium';
      case 'High': return 'text-risk-high';
      default: return 'text-navy-900';
    }
  };

  const getRiskBgColor = (category: string) => {
    switch (category) {
      case 'Low': return 'bg-green-50 border-green-200';
      case 'Medium': return 'bg-amber-50 border-amber-200';
      case 'High': return 'bg-red-50 border-red-200';
      default: return 'bg-navy-50 border-navy-200';
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in">
      <div className="flex justify-between items-center mb-6 no-print">
        <Link to="/history" className="text-navy-700 hover:text-navy-900 flex items-center gap-1 text-sm font-medium">
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" /></svg>
          Back to History
        </Link>
        <button onClick={handlePrint} className="btn-secondary text-sm flex items-center gap-2">
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" /></svg>
          Print Report
        </button>
      </div>

      <div className="print-only hidden mb-8 text-center border-b border-navy-200 pb-6">
        <h1 className="text-3xl font-heading font-bold text-navy-900 mb-2">AyuPulse Medical Report</h1>
        <p className="text-navy-700">Cardiovascular Risk Assessment</p>
      </div>

      {/* Main Results Section */}
      <div className={`card-base p-8 mb-8 border-2 ${getRiskBgColor(prediction.risk_category)}`}>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
          <div>
            <div className="mb-2">
              <span className="text-sm font-medium text-navy-700 uppercase tracking-wider">Patient</span>
              <h2 className="text-2xl font-heading font-bold text-navy-900">{prediction.subject_name}</h2>
              <p className="text-sm text-navy-700 mt-1">Date: {format(new Date(prediction.created_at), 'MMMM do, yyyy h:mm a')}</p>
            </div>
            
            <div className="mt-8">
              <h3 className="text-lg font-heading font-semibold mb-2">Overall Risk Category</h3>
              <div className="flex items-end gap-3 mb-4">
                <span className={`text-4xl font-bold ${getRiskColor(prediction.risk_category)}`}>
                  {prediction.risk_category}
                </span>
                <span className="text-xl text-navy-700 mb-1">Risk</span>
              </div>
              <p className="text-navy-800 leading-relaxed">
                {prediction.explanation_text}
              </p>
            </div>
            
            <div className="mt-6 flex flex-wrap gap-4">
              <div className="bg-white/60 px-4 py-2 rounded-lg border border-white/40">
                <p className="text-xs text-navy-700 mb-1">Model Confidence</p>
                <p className="font-semibold text-navy-900">{(prediction.confidence * 100).toFixed(1)}%</p>
              </div>
              <div className="bg-white/60 px-4 py-2 rounded-lg border border-white/40">
                <p className="text-xs text-navy-700 mb-1">Modalities Used</p>
                <div className="flex gap-1 mt-0.5">
                  {prediction.modalities_used.map((m: string) => (
                    <Badge key={m} variant="primary" className="text-[10px]">{m}</Badge>
                  ))}
                </div>
              </div>
            </div>
          </div>
          
          <div className="flex justify-center border-l border-navy-200/50 pl-8">
            <div className="text-center">
              <p className="font-heading font-semibold text-navy-900 mb-4">Risk Score</p>
              <RiskMeter score={prediction.risk_score} size="lg" />
              <p className="text-3xl font-bold mt-4 text-navy-900">
                {(prediction.risk_score * 100).toFixed(1)}<span className="text-lg text-navy-700">%</span>
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        {/* SHAP Values Chart */}
        <div className="card-base">
          <h3 className="font-heading font-semibold text-lg border-b border-navy-100 pb-4 mb-4">Key Risk Factors</h3>
          <p className="text-sm text-navy-700 mb-6">
            The following clinical parameters had the most significant impact on your risk score.
            Features increasing risk push to the right, those decreasing risk push to the left.
          </p>
          <ShapChart features={prediction.shap_features} />
        </div>

        {/* Clinical Inputs Table */}
        <div className="card-base print-break-inside-avoid">
          <h3 className="font-heading font-semibold text-lg border-b border-navy-100 pb-4 mb-4">Clinical Parameters</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs text-navy-700 bg-navy-50">
                <tr>
                  <th className="px-3 py-2 rounded-tl-lg">Parameter</th>
                  <th className="px-3 py-2">Value</th>
                  <th className="px-3 py-2">Reference</th>
                  <th className="px-3 py-2 rounded-tr-lg">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-navy-50">
                {prediction.clinical_reference_ranges.map((ref: any, idx: number) => {
                  let statusBadge;
                  if (ref.status === 'Normal') statusBadge = <Badge variant="success">Normal</Badge>;
                  else if (ref.status === 'Borderline') statusBadge = <Badge variant="warning">Borderline</Badge>;
                  else statusBadge = <Badge variant="danger">{ref.status}</Badge>;
                  
                  return (
                    <tr key={idx}>
                      <td className="px-3 py-2.5 font-medium text-navy-900">{ref.parameter}</td>
                      <td className="px-3 py-2.5">{ref.value} {ref.unit}</td>
                      <td className="px-3 py-2.5 text-navy-700">{ref.reference_range}</td>
                      <td className="px-3 py-2.5">{statusBadge}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Recommendations */}
      <div className="card-base mb-8 bg-primary/5 border-primary/20 print-break-inside-avoid">
        <h3 className="font-heading font-semibold text-lg text-navy-900 mb-4 flex items-center gap-2">
          <svg className="w-5 h-5 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          Clinical Recommendations
        </h3>
        <ul className="space-y-3">
          {prediction.recommendations.map((rec: string, idx: number) => (
            <li key={idx} className="flex items-start gap-3 text-navy-900 text-sm">
              <div className="w-1.5 h-1.5 rounded-full bg-primary mt-1.5 flex-shrink-0"></div>
              {rec}
            </li>
          ))}
        </ul>
        <div className="mt-6 p-4 bg-white rounded-lg border border-navy-100 text-xs text-navy-700 italic">
          Disclaimer: This AI-generated report is for informational purposes only and does not constitute medical advice, diagnosis, or treatment. Always consult with a qualified healthcare provider regarding your health and before making any changes to your treatment or lifestyle.
        </div>
      </div>

      {/* Imaging Section */}
      {(prediction.xray_original_path || prediction.ecg_original_path) && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
          {prediction.xray_original_path && (
            <div className="flex flex-col gap-3">
              <GradCamViewer 
                title="Chest X-Ray Analysis" 
                originalPath={prediction.xray_original_path}
                gradcamPath={prediction.xray_gradcam_path}
              />
              {prediction.xray_analysis && (
                <div className="p-4 bg-navy-50 rounded-xl border border-navy-100 text-sm text-navy-800 shadow-sm">
                  <p className="font-heading font-semibold text-navy-900 mb-1">Model Conclusion</p>
                  <p>{prediction.xray_analysis}</p>
                </div>
              )}
            </div>
          )}
          {prediction.ecg_original_path && (
            <div className="flex flex-col gap-3">
              <GradCamViewer 
                title="ECG Analysis" 
                originalPath={prediction.ecg_original_path}
                gradcamPath={prediction.ecg_gradcam_path}
              />
              {prediction.ecg_analysis && (
                <div className="p-4 bg-navy-50 rounded-xl border border-navy-100 text-sm text-navy-800 shadow-sm">
                  <p className="font-heading font-semibold text-navy-900 mb-1">Model Conclusion</p>
                  <p>{prediction.ecg_analysis}</p>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
