import React from 'react';

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon?: React.ReactNode;
  trend?: {
    value: number;
    isPositive: boolean;
  };
}

export const MetricCard: React.FC<MetricCardProps> = ({ title, value, subtitle, icon, trend }) => {
  return (
    <div className="bg-white rounded-xl shadow-soft border border-navy-50 p-6 flex flex-col">
      <div className="flex justify-between items-start mb-4">
        <h3 className="text-sm font-medium text-navy-500">{title}</h3>
        {icon && <div className="text-navy-400">{icon}</div>}
      </div>
      
      <div className="flex items-end gap-3 mt-auto">
        <p className="text-3xl font-heading font-bold text-navy-900">{value}</p>
        
        {trend && (
          <div className={`flex items-center text-sm font-medium mb-1 ${trend.isPositive ? 'text-risk-low' : 'text-risk-high'}`}>
            <svg className={`w-4 h-4 mr-1 ${trend.isPositive ? '' : 'transform rotate-180'}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
            </svg>
            {Math.abs(trend.value)}%
          </div>
        )}
      </div>
      
      {subtitle && <p className="text-xs text-navy-400 mt-2">{subtitle}</p>}
    </div>
  );
};
