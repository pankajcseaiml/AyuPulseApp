import React from 'react';

interface ShapFeature {
  name: string;
  display_name: string;
  value: any;
  shap_value: number;
  contribution_pct: number;
  direction: string;
}

interface ShapChartProps {
  features: ShapFeature[];
}

export const ShapChart: React.FC<ShapChartProps> = ({ features }) => {
  if (!features || features.length === 0) return <div>No data available</div>;

  // Find max absolute shap value to scale bars properly
  const maxShap = Math.max(...features.map(f => Math.abs(f.shap_value)));
  
  return (
    <div className="w-full flex flex-col gap-3 print-break-inside-avoid">
      <div className="flex text-xs font-medium text-navy-500 mb-2 border-b border-navy-100 pb-2">
        <div className="w-1/3">Feature</div>
        <div className="w-2/3 flex justify-between">
          <span className="text-risk-low">&larr; Decreases Risk</span>
          <span className="text-risk-high">Increases Risk &rarr;</span>
        </div>
      </div>
      
      {features.map((feature, idx) => {
        // Calculate width percentage relative to max absolute shap value (scale to max 45% so they meet in middle)
        const widthPct = (Math.abs(feature.shap_value) / maxShap) * 45;
        const isPositive = feature.direction === 'positive';
        
        return (
          <div key={idx} className="flex items-center text-sm">
            {/* Label Column */}
            <div className="w-1/3 pr-4 flex flex-col justify-center">
              <span className="font-medium text-navy-800 truncate" title={feature.display_name}>
                {feature.display_name}
              </span>
              <span className="text-xs text-navy-500 truncate">
                Value: {feature.value}
              </span>
            </div>
            
            {/* Bar Column */}
            <div className="w-2/3 flex items-center relative h-6 bg-navy-50 rounded">
              {/* Zero line */}
              <div className="absolute left-1/2 top-0 bottom-0 w-px bg-navy-300 z-10"></div>
              
              {/* Negative bar (Left side) */}
              {!isPositive && (
                <div 
                  className="absolute right-1/2 h-4 bg-risk-low/80 rounded-l transition-all duration-1000 ease-out"
                  style={{ width: `${widthPct}%` }}
                ></div>
              )}
              
              {/* Positive bar (Right side) */}
              {isPositive && (
                <div 
                  className="absolute left-1/2 h-4 bg-risk-high/80 rounded-r transition-all duration-1000 ease-out"
                  style={{ width: `${widthPct}%` }}
                ></div>
              )}
              
              {/* Tooltip/Value display */}
              <div className={`absolute text-[10px] font-medium px-1 ${isPositive ? 'left-[calc(50%+4px)] text-risk-high' : 'right-[calc(50%+4px)] text-risk-low'}`}>
                {feature.contribution_pct.toFixed(1)}%
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};
