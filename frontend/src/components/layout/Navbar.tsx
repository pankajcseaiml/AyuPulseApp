import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

export const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  const location = useLocation();

  const isPublicPage = ['/', '/login', '/register'].includes(location.pathname);

  return (
    <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-navy-100 no-print">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <div className="flex items-center gap-2">
            <svg className="w-8 h-8 text-primary" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
            </svg>
            <Link to="/" className="font-heading font-bold text-xl text-navy-900 tracking-tight">
              AyuPulse
            </Link>
          </div>

          <div className="hidden md:flex items-center space-x-8">
            {isPublicPage ? (
              <>
                <a href="#features" className="text-navy-900 hover:text-primary transition-colors font-medium">Features</a>
                <a href="#how-it-works" className="text-navy-900 hover:text-primary transition-colors font-medium">How it Works</a>
                <a href="#about" className="text-navy-900 hover:text-primary transition-colors font-medium">About</a>
              </>
            ) : null}
          </div>

          <div className="flex items-center space-x-4">
            {user ? (
              <div className="flex items-center gap-4">
                <span className="text-sm font-medium text-navy-900 hidden sm:block">
                  Hello, {user.full_name}
                </span>
                {!isPublicPage ? null : (
                  <Link to="/dashboard" className="btn-secondary text-sm">Dashboard</Link>
                )}
                <button onClick={logout} className="text-sm text-navy-900 hover:text-primary font-medium">
                  Logout
                </button>
              </div>
            ) : (
              <>
                <Link to="/login" className="text-navy-900 hover:text-primary font-medium transition-colors">
                  Log in
                </Link>
                <Link to="/register" className="btn-primary">
                  Get Started
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};
