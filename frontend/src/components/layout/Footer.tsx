import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-navy-900 text-white py-12 no-print">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center gap-2 mb-4">
              <svg className="w-8 h-8 text-primary" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
              </svg>
              <span className="font-heading font-bold text-xl tracking-tight">
                AyuPulse
              </span>
            </div>
            <p className="text-navy-300 text-sm mb-4 max-w-sm">
              AI-powered early detection combining clinical data, chest X-ray, and ECG analysis — with full explainability for every prediction.
            </p>
            <p className="text-xs text-navy-400 font-medium">
              Disclaimer: For screening purposes only. Not a diagnostic tool. Always consult a healthcare professional.
            </p>
          </div>
          
          <div>
            <h4 className="font-heading font-semibold mb-4 text-white">Product</h4>
            <ul className="space-y-2 text-sm text-navy-300">
              <li><a href="#features" className="hover:text-primary transition-colors">Features</a></li>
              <li><a href="#how-it-works" className="hover:text-primary transition-colors">How it Works</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">Pricing</a></li>
            </ul>
          </div>
          
          <div>
            <h4 className="font-heading font-semibold mb-4 text-white">Company</h4>
            <ul className="space-y-2 text-sm text-navy-300">
              <li><a href="#about" className="hover:text-primary transition-colors">About Us</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">Contact</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">Privacy Policy</a></li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-navy-800 mt-12 pt-8 flex flex-col md:flex-row justify-between items-center">
          <p className="text-sm text-navy-400">
            &copy; {new Date().getFullYear()} AyuPulse. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};
