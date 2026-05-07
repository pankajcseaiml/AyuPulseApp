import React from 'react';
import RegisterForm from '../components/auth/RegisterForm';
import { Navbar } from '../components/layout/Navbar';
import { Footer } from '../components/layout/Footer';

export const RegisterPage: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col bg-navy-50">
      <Navbar />
      <main className="flex-grow flex items-center justify-center p-4">
        <RegisterForm />
      </main>
      <Footer />
    </div>
  );
};
