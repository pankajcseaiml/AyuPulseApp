import React, { useState } from 'react';
import { API_CONFIG } from '../../config';

interface GradCamViewerProps {
  title: string;
  originalPath?: string | null;
  gradcamPath?: string | null;
}

export const GradCamViewer: React.FC<GradCamViewerProps> = ({ title, originalPath, gradcamPath }) => {
  const [showGradCam, setShowGradCam] = useState(true);
  
  if (!originalPath) {
    return (
      <div className="flex flex-col items-center justify-center bg-navy-50 rounded-xl p-8 border border-dashed border-navy-200 h-64">
        <svg className="w-12 h-12 text-navy-300 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        <p className="text-navy-500 font-medium">No {title} uploaded</p>
      </div>
    );
  }

  // Handle paths that might be absolute from backend
  const getImageUrl = (path: string) => {
    if (path.startsWith('http')) return path;
    // Assuming backend serves uploads at /static/uploads or similar, but the prompt says files are in uploads/
    // Since we didn't setup static file serving in backend yet, we'll need to fetch via an endpoint or assume the dev server proxies it.
    // For now, assume API_CONFIG.BASE_URL/path works if we strip leading slash.
    // We will add static file serving in backend main.py shortly.
    const cleanPath = path.replace(/\\/g, '/'); // fix windows paths
    return `${API_CONFIG.BASE_URL}/${cleanPath}`;
  };

  return (
    <div className="flex flex-col border border-navy-100 rounded-xl overflow-hidden bg-white shadow-sm print-break-inside-avoid">
      <div className="flex justify-between items-center px-4 py-3 border-b border-navy-100 bg-navy-50">
        <h4 className="font-heading font-semibold text-navy-800">{title}</h4>
        {gradcamPath && (
          <div className="flex bg-white rounded-lg p-0.5 border border-navy-200 no-print">
            <button 
              className={`px-3 py-1 text-xs font-medium rounded-md transition-colors ${!showGradCam ? 'bg-navy-100 text-navy-900' : 'text-navy-500 hover:text-navy-700'}`}
              onClick={() => setShowGradCam(false)}
            >
              Original
            </button>
            <button 
              className={`px-3 py-1 text-xs font-medium rounded-md transition-colors ${showGradCam ? 'bg-primary/10 text-primary' : 'text-navy-500 hover:text-navy-700'}`}
              onClick={() => setShowGradCam(true)}
            >
              Highlighted
            </button>
          </div>
        )}
      </div>
      
      <div className="relative aspect-square w-full bg-black overflow-hidden flex items-center justify-center">
        <img 
          src={getImageUrl(originalPath)} 
          alt={`Original ${title}`}
          className="absolute inset-0 w-full h-full object-contain"
        />
        {gradcamPath && (
          <img 
            src={getImageUrl(gradcamPath)} 
            alt={`GradCAM ${title}`}
            className={`absolute inset-0 w-full h-full object-contain transition-opacity duration-500 ${showGradCam ? 'opacity-100' : 'opacity-0'}`}
          />
        )}
      </div>
      
      {gradcamPath && (
        <div className="p-3 bg-navy-50 text-xs text-navy-600">
          <p>Areas highlighted in red indicate regions the AI focused on for this prediction.</p>
        </div>
      )}
    </div>
  );
};
