import React from 'react';

interface RiskMeterProps {
  score: number; // 0 to 1
  size?: 'sm' | 'md' | 'lg';
}

export const RiskMeter: React.FC<RiskMeterProps> = ({ score, size = 'md' }) => {
  // Normalize score between 0 and 1
  const normalizedScore = Math.max(0, Math.min(1, score));
  
  // Angle for the needle (0 to 180 degrees)
  const angle = normalizedScore * 180;
  
  const dimensions = {
    sm: { width: 120, height: 60, stroke: 10, cx: 60, cy: 55, r: 45 },
    md: { width: 200, height: 100, stroke: 16, cx: 100, cy: 90, r: 75 },
    lg: { width: 300, height: 150, stroke: 24, cx: 150, cy: 135, r: 110 },
  };
  
  const dim = dimensions[size];
  
  // Calculate dash array for arc
  const arcLength = Math.PI * dim.r;
  const dashArray = `${arcLength} ${arcLength}`;
  
  // We'll create three colored segments: Green (0-0.3), Amber (0.3-0.7), Red (0.7-1.0)
  // We can just use a gradient for a smoother look
  return (
    <div className="flex flex-col items-center justify-center relative">
      <svg 
        width={dim.width} 
        height={dim.height} 
        viewBox={`0 0 ${dim.width} ${dim.height}`}
        className="overflow-visible"
      >
        <defs>
          <linearGradient id={`riskGradient-${size}`} x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#22c55e" />   {/* Green */}
            <stop offset="30%" stopColor="#22c55e" />
            <stop offset="50%" stopColor="#f59e0b" />  {/* Amber */}
            <stop offset="70%" stopColor="#f59e0b" />
            <stop offset="85%" stopColor="#E24B4A" />  {/* Red */}
            <stop offset="100%" stopColor="#E24B4A" />
          </linearGradient>
        </defs>
        
        {/* Background track */}
        <path
          d={`M ${dim.cx - dim.r} ${dim.cy} A ${dim.r} ${dim.r} 0 0 1 ${dim.cx + dim.r} ${dim.cy}`}
          fill="none"
          stroke="#e2e8f0"
          strokeWidth={dim.stroke}
          strokeLinecap="round"
        />
        
        {/* Colored arc */}
        <path
          d={`M ${dim.cx - dim.r} ${dim.cy} A ${dim.r} ${dim.r} 0 0 1 ${dim.cx + dim.r} ${dim.cy}`}
          fill="none"
          stroke={`url(#riskGradient-${size})`}
          strokeWidth={dim.stroke}
          strokeLinecap="round"
          strokeDasharray={dashArray}
          strokeDashoffset="0"
        />
        
        {/* Needle group */}
        <g 
          transform={`translate(${dim.cx}, ${dim.cy}) rotate(${angle - 90})`}
          style={{ transition: 'transform 1s cubic-bezier(0.34, 1.56, 0.64, 1)' }}
        >
          {/* Needle path */}
          <path d={`M -${dim.stroke/4} 0 L 0 -${dim.r - dim.stroke/2} L ${dim.stroke/4} 0 Z`} fill="#1e293b" />
          {/* Needle center */}
          <circle cx="0" cy="0" r={dim.stroke/2} fill="#1e293b" />
          <circle cx="0" cy="0" r={dim.stroke/4} fill="white" />
        </g>
      </svg>
      
      {size === 'lg' && (
        <div className="absolute bottom-0 translate-y-full pt-2 flex justify-between w-full text-xs font-medium text-navy-500 px-6">
          <span>Low</span>
          <span>Medium</span>
          <span>High</span>
        </div>
      )}
    </div>
  );
};
