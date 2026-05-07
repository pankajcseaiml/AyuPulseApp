import React from 'react';

type BadgeVariant = 'success' | 'warning' | 'danger' | 'neutral' | 'primary';

interface BadgeProps {
  children: React.ReactNode;
  variant?: BadgeVariant;
  className?: string;
}

export const Badge: React.FC<BadgeProps> = ({ children, variant = 'neutral', className = '' }) => {
  const baseClasses = "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium";
  
  const variantClasses = {
    success: "bg-green-100 text-navy-900",
    warning: "bg-amber-100 text-navy-900",
    danger: "bg-red-100 text-navy-900",
    neutral: "bg-navy-100 text-navy-900",
    primary: "bg-primary-50 text-primary",
  };
  
  return (
    <span className={`${baseClasses} ${variantClasses[variant]} ${className}`}>
      {children}
    </span>
  );
};
