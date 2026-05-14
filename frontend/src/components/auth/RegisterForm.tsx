import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { UserPlus, Mail, Lock, User, Eye, EyeOff, AlertCircle, CheckCircle } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { API_CONFIG } from '../../config';

const registerSchema = z.object({
  name: z.string().min(2, 'Full name must be at least 2 characters'),
  username: z.string().min(3, 'Username must be at least 3 characters'),
  email: z.string().email('Please enter a valid email address'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
    .regex(/[a-z]/, 'Password must contain at least one lowercase letter')
    .regex(/[0-9]/, 'Password must contain at least one number')
    .regex(/[^A-Za-z0-9]/, 'Password must contain at least one special character'),
  confirmPassword: z.string(),
  agreeToTerms: z.boolean().refine(val => val === true, {
    message: 'You must agree to the terms and conditions',
  }),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
});

type RegisterFormData = z.infer<typeof registerSchema>;

const RegisterForm: React.FC = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate();
  const { register: registerUser } = useAuth();

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      name: '',
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      agreeToTerms: false,
    },
  });

  const password = watch('password'); // eslint-disable-line react-hooks/incompatible-library

  const onSubmit = async (data: RegisterFormData) => {
    setError(null);
    setSuccess(null);
    setIsSubmitting(true);

    try {
      const { confirmPassword, agreeToTerms, ...userData } = data; // eslint-disable-line @typescript-eslint/no-unused-vars
      // Hardcode role as "patient" for all public registrations
      const userDataWithRole = { ...userData, role: 'patient' };
      await registerUser(userDataWithRole);
      setSuccess('Registration successful! Redirecting to dashboard...');
      setTimeout(() => {
        navigate(API_CONFIG.ROUTES.DASHBOARD);
      }, 2000);
    } catch (err: any) { // eslint-disable-line @typescript-eslint/no-explicit-any
      setError(
        err.response?.data?.detail ||
        err.message ||
        'Registration failed. Please try again.'
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  const passwordStrength = (pass: string): { score: number; label: string; color: string } => {
    if (!pass) return { score: 0, label: 'Empty', color: 'gray' };
    
    let score = 0;
    if (pass.length >= 8) score++;
    if (/[A-Z]/.test(pass)) score++;
    if (/[a-z]/.test(pass)) score++;
    if (/[0-9]/.test(pass)) score++;
    if (/[^A-Za-z0-9]/.test(pass)) score++;
    
    const strengths = [
      { score: 1, label: 'Very Weak', color: 'red' },
      { score: 2, label: 'Weak', color: 'orange' },
      { score: 3, label: 'Fair', color: 'yellow' },
      { score: 4, label: 'Good', color: 'lime' },
      { score: 5, label: 'Strong', color: 'green' },
    ];
    
    return strengths[Math.min(score - 1, 4)];
  };

  const strength = passwordStrength(password);

  return (
    <div className="w-full max-w-4xl mx-auto py-8 px-4">
      <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
        <div className="md:flex">
          {/* Left Side - Form */}
          <div className="md:w-1/2 p-8">
            <div className="text-center mb-8">
              <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary/10 mb-4">
                <UserPlus className="w-8 h-8 text-primary" />
              </div>
              <h1 className="text-3xl font-bold text-navy-900">Create Account</h1>
              <p className="text-navy-600 mt-2">Join AyuPulse to start predicting heart disease risks</p>
            </div>

            {/* Error Message */}
            {error && (
              <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start">
                <AlertCircle className="w-5 h-5 text-red-500 mr-2 mt-0.5 flex-shrink-0" />
                <p className="text-red-700 text-sm">{error}</p>
              </div>
            )}

            {/* Success Message */}
            {success && (
              <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg flex items-start">
                <CheckCircle className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                <p className="text-green-700 text-sm">{success}</p>
              </div>
            )}

            {/* Registration Form */}
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                <div>
                  <label htmlFor="name" className="form-label">
                    <User className="w-4 h-4 inline mr-2" />
                    Name
                  </label>
                  <input
                    id="name"
                    type="text"
                    {...register('name')}
                    className={`form-input ${errors.name ? 'border-red-300 focus:border-red-500 focus:ring-red-200' : ''}`}
                    placeholder="Enter your name"
                    disabled={isSubmitting}
                  />
                  {errors.name && (
                    <p className="form-error">{errors.name.message}</p>
                  )}
                </div>

                <div>
                  <label htmlFor="username" className="form-label">
                    <User className="w-4 h-4 inline mr-2" />
                    Username
                  </label>
                  <input
                    id="username"
                    type="text"
                    {...register('username')}
                    className={`form-input ${errors.username ? 'border-red-300 focus:border-red-500 focus:ring-red-200' : ''}`}
                    placeholder="Choose a username"
                    disabled={isSubmitting}
                  />
                  {errors.username && (
                    <p className="form-error">{errors.username.message}</p>
                  )}
                </div>
              </div>

              <div>
                <label htmlFor="email" className="form-label">
                  <Mail className="w-4 h-4 inline mr-2" />
                  Email Address
                </label>
                <input
                  id="email"
                  type="email"
                  {...register('email')}
                  className={`form-input ${errors.email ? 'border-red-300 focus:border-red-500 focus:ring-red-200' : ''}`}
                  placeholder="Enter your email address"
                  disabled={isSubmitting}
                />
                {errors.email && (
                  <p className="form-error">{errors.email.message}</p>
                )}
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                <div>
                  <label htmlFor="password" className="form-label">
                    <Lock className="w-4 h-4 inline mr-2" />
                    Password
                  </label>
                  <div className="relative">
                    <input
                      id="password"
                      type={showPassword ? 'text' : 'password'}
                      {...register('password')}
                      className={`form-input pr-10 ${errors.password ? 'border-red-300 focus:border-red-500 focus:ring-red-200' : ''}`}
                      placeholder="Create a strong password"
                      disabled={isSubmitting}
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3 top-1/2 transform -translate-y-1/2 text-navy-500 hover:text-navy-700"
                      disabled={isSubmitting}
                    >
                      {showPassword ? (
                        <EyeOff className="w-5 h-5" />
                      ) : (
                        <Eye className="w-5 h-5" />
                      )}
                    </button>
                  </div>
                  {errors.password && (
                    <p className="form-error">{errors.password.message}</p>
                  )}
                  
                  {/* Password Strength Meter */}
                  {password && (
                    <div className="mt-2">
                      <div className="flex justify-between text-xs mb-1">
                        <span className="text-navy-600">Password strength:</span>
                        <span className={`font-medium ${strength.color === 'red' ? 'text-red-600' : strength.color === 'orange' ? 'text-orange-600' : strength.color === 'yellow' ? 'text-yellow-600' : strength.color === 'lime' ? 'text-lime-600' : 'text-green-600'}`}>
                          {strength.label}
                        </span>
                      </div>
                      <div className="h-1.5 bg-navy-200 rounded-full overflow-hidden">
                        <div
                          className={`h-full ${strength.color === 'red' ? 'bg-red-500' : strength.color === 'orange' ? 'bg-orange-500' : strength.color === 'yellow' ? 'bg-yellow-500' : strength.color === 'lime' ? 'bg-lime-500' : 'bg-green-500'} transition-all duration-300`}
                          style={{ width: `${(passwordStrength(password).score / 5) * 100}%` }}
                        ></div>
                      </div>
                    </div>
                  )}
                </div>

                <div>
                  <label htmlFor="confirmPassword" className="form-label">
                    <Lock className="w-4 h-4 inline mr-2" />
                    Confirm Password
                  </label>
                  <div className="relative">
                    <input
                      id="confirmPassword"
                      type={showConfirmPassword ? 'text' : 'password'}
                      {...register('confirmPassword')}
                      className={`form-input pr-10 ${errors.confirmPassword ? 'border-red-300 focus:border-red-500 focus:ring-red-200' : ''}`}
                      placeholder="Confirm your password"
                      disabled={isSubmitting}
                    />
                    <button
                      type="button"
                      onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                      className="absolute right-3 top-1/2 transform -translate-y-1/2 text-navy-500 hover:text-navy-700"
                      disabled={isSubmitting}
                    >
                      {showConfirmPassword ? (
                        <EyeOff className="w-5 h-5" />
                      ) : (
                        <Eye className="w-5 h-5" />
                      )}
                    </button>
                  </div>
                  {errors.confirmPassword && (
                    <p className="form-error">{errors.confirmPassword.message}</p>
                  )}
                </div>
              </div>

              <div className="flex items-start">
                <input
                  id="agreeToTerms"
                  type="checkbox"
                  {...register('agreeToTerms')}
                  className="h-4 w-4 text-primary focus:ring-primary border-navy-300 rounded mt-1"
                  disabled={isSubmitting}
                />
                <label htmlFor="agreeToTerms" className="ml-2 block text-sm text-navy-700">
                  I agree to the{' '}
                  <a href="#" className="text-primary font-medium hover:underline">
                    Terms of Service
                  </a>{' '}
                  and{' '}
                  <a href="#" className="text-primary font-medium hover:underline">
                    Privacy Policy
                  </a>
                  . I understand that this is a medical application and I will use it responsibly.
                </label>
              </div>
              {errors.agreeToTerms && (
                <p className="form-error">{errors.agreeToTerms.message}</p>
              )}

              <button
                type="submit"
                disabled={isSubmitting}
                className="w-full py-3.5 bg-primary text-white font-semibold rounded-lg hover:bg-primary/90 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
              >
                {isSubmitting ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-2 border-white/30 border-t-white mr-2"></div>
                    Creating Account...
                  </>
                ) : (
                  <>
                    <UserPlus className="w-5 h-5 mr-2" />
                    Create Account
                  </>
                )}
              </button>
            </form>

            {/* Sign In Link */}
            <div className="mt-8 text-center">
              <p className="text-navy-600">
                Already have an account?{' '}
                <Link
                  to="/login"
                  className="text-primary font-semibold hover:text-primary/80"
                >
                  Sign in here
                </Link>
              </p>
            </div>
          </div>

          {/* Right Side - Info */}
          <div className="md:w-1/2 bg-gradient-to-br from-primary to-secondary p-8 text-white flex flex-col justify-center">
            <div className="mb-8">
              <h2 className="text-2xl font-bold mb-4">Why Join AyuPulse?</h2>
              <ul className="space-y-4">
                <li className="flex items-start">
                  <CheckCircle className="w-5 h-5 mr-3 mt-0.5 flex-shrink-0" />
                  <span>Early detection of heart disease risks using AI</span>
                </li>
                <li className="flex items-start">
                  <CheckCircle className="w-5 h-5 mr-3 mt-0.5 flex-shrink-0" />
                  <span>Multi-modal analysis (clinical, X-ray, ECG data)</span>
                </li>
                <li className="flex items-start">
                  <CheckCircle className="w-5 h-5 mr-3 mt-0.5 flex-shrink-0" />
                  <span>Comprehensive patient management system</span>
                </li>
                <li className="flex items-start">
                  <CheckCircle className="w-5 h-5 mr-3 mt-0.5 flex-shrink-0" />
                  <span>Secure, HIPAA-compliant data handling</span>
                </li>
                <li className="flex items-start">
                  <CheckCircle className="w-5 h-5 mr-3 mt-0.5 flex-shrink-0" />
                  <span>Real-time risk visualization and reporting</span>
                </li>
              </ul>
            </div>

            <div className="bg-white/10 rounded-xl p-6">
              <h3 className="font-bold mb-3">Patient-First Approach</h3>
              <p className="text-sm opacity-90">
                AyuPulse empowers patients to take control of their heart health
                through AI-driven risk assessments, early detection, and
                personalized health insights.
              </p>
            </div>

            <div className="mt-8 pt-6 border-t border-white/20">
              <p className="text-sm opacity-80">
                <strong>Note:</strong> This account gives you patient-level access.
                Healthcare professionals should contact an administrator
                for doctor or staff accounts.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="mt-6 text-center">
        <p className="text-xs text-navy-500">
          By creating an account, you agree to AyuPulse's Terms of Service and Privacy Policy.
          All medical data is encrypted and stored securely.
          <br />
          © {new Date().getFullYear()} AyuPulse. All rights reserved.
        </p>
      </div>
    </div>
  );
};

export default RegisterForm;