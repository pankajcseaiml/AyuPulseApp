import React from 'react';
import LoginForm from '../components/auth/LoginForm';
import { Navbar } from '../components/layout/Navbar';
import { Footer } from '../components/layout/Footer';

export const LoginPage: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col bg-navy-50">
      <Navbar />
      <main className="flex-grow flex items-center justify-center p-4">
        <LoginForm />
      </main>
      <Footer />
    </div>
  );
};
