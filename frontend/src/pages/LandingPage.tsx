import React from 'react';
import { Link } from 'react-router-dom';
import { Navbar } from '../components/layout/Navbar';
import { Footer } from '../components/layout/Footer';
import { RiskMeter } from '../components/ui/RiskMeter';

export const LandingPage: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col bg-white">
      <Navbar />
      
      <main className="flex-grow">
        {/* Hero Section */}
        <section className="relative pt-20 pb-32 overflow-hidden bg-navy-900">
          <div className="absolute inset-0 bg-gradient-to-br from-navy-900 via-navy-950 to-navy-900 opacity-90"></div>
          
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
              <div className="text-white">
                <h1 className="text-5xl md:text-6xl font-heading font-bold leading-tight mb-6 animate-fade-in text-white">
                  Know Your Heart Risk Before It Knows You
                </h1>
                <p className="text-lg md:text-xl text-white/90 mb-8 max-w-xl animate-slide-up" style={{ animationDelay: '0.1s' }}>
                  AI-powered early detection combining clinical data, chest X-ray, and ECG analysis — with full explainability for every prediction.
                </p>
                
                <div className="flex flex-wrap gap-4 animate-slide-up" style={{ animationDelay: '0.2s' }}>
                  <Link to="/register" className="btn-primary text-lg px-8 py-3 bg-primary hover:bg-primary-hover shadow-lg shadow-primary/30">
                    Get Started Free
                  </Link>
                  <a href="#how-it-works" className="btn-secondary text-lg px-8 py-3 bg-white/10 text-white border-white/20 hover:bg-white/20">
                    See How It Works
                  </a>
                </div>
                
                <div className="mt-12 flex flex-wrap gap-6 text-sm font-medium text-white/80 animate-fade-in" style={{ animationDelay: '0.4s' }}>
                  <div className="flex items-center gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-primary"></div>
                    15 Clinical Parameters
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-primary"></div>
                    3 AI Models
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-primary"></div>
                    Full Explainability
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-primary"></div>
                    Instant Results
                  </div>
                </div>
              </div>
              
              <div className="hidden lg:flex justify-center animate-fade-in" style={{ animationDelay: '0.3s' }}>
                <div className="bg-white rounded-2xl p-8 shadow-2xl relative w-full max-w-md transform rotate-1 hover:rotate-0 transition-transform duration-500">
                  <div className="absolute -top-4 -right-4 bg-primary text-white text-xs font-bold px-3 py-1 rounded-full shadow-lg">
                    Live Demo
                  </div>
                  <h3 className="font-heading font-semibold text-center text-navy-900 mb-6">Risk Assessment Model</h3>
                  <div className="flex justify-center mb-8">
                    <RiskMeter score={0.65} size="md" />
                  </div>
                  <div className="space-y-4">
                    <div className="h-2 bg-navy-100 rounded-full overflow-hidden">
                      <div className="h-full bg-primary w-[65%] animate-progress-fill"></div>
                    </div>
                    <div className="flex justify-between text-xs font-medium text-navy-700">
                      <span>Clinical Data Analyzed</span>
                      <span className="text-primary">Complete</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section id="features" className="py-24 bg-navy-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-3xl mx-auto mb-16">
              <h2 className="text-3xl md:text-4xl font-heading font-bold text-navy-900 mb-4">Comprehensive Analysis</h2>
              <p className="text-lg text-navy-700">Our platform goes beyond simple questionnaires, integrating multiple data modalities for a more accurate assessment.</p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {[
                { title: 'Multi-Modal Analysis', desc: 'Combines clinical data, chest X-rays, and ECGs into a single cohesive risk score using advanced fusion neural networks.', icon: 'M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10' },
                { title: 'Explainable AI', desc: 'Understand exactly why a prediction was made with SHAP values for clinical data and GradCAM heatmaps for images.', icon: 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z' },
                { title: 'Family Profiles', desc: 'Manage cardiovascular health for your entire family from a single dashboard. Track individual trends over time.', icon: 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z' },
                { title: 'Full Medical Report', desc: 'Receive a detailed report with your values compared against standard medical reference ranges (e.g. JNC8, ATP III).', icon: 'M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' },
                { title: 'Prediction History', desc: 'Longitudinal trend tracking visualizes how your risk changes as you modify lifestyle factors or start new treatments.', icon: 'M13 7h8m0 0v8m0-8l-8 8-4-4-6 6' },
                { title: 'Doctor-Ready', desc: 'Easily export or print your risk assessment to share with your healthcare provider during your next checkup.', icon: 'M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4' },
              ].map((feature, i) => (
                <div key={i} className="card-base hover:border-primary/30 transition-colors group">
                  <div className="w-12 h-12 rounded-lg bg-navy-100 flex items-center justify-center text-primary mb-6 group-hover:bg-primary group-hover:text-white transition-colors">
                    <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d={feature.icon} />
                    </svg>
                  </div>
                  <h3 className="text-xl font-heading font-semibold text-navy-900 mb-3">{feature.title}</h3>
                  <p className="text-navy-700 text-sm leading-relaxed">{feature.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* How It Works */}
        <section id="how-it-works" className="py-24 bg-white relative overflow-hidden">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-3xl mx-auto mb-20">
              <h2 className="text-3xl md:text-4xl font-heading font-bold text-navy-900 mb-4">How It Works</h2>
              <p className="text-lg text-navy-700">A simple, seamless process to understand your cardiovascular health.</p>
            </div>
            
            <div className="relative">
              {/* Connecting line */}
              <div className="hidden md:block absolute top-1/2 left-0 w-full h-0.5 bg-navy-100 -translate-y-1/2 z-0"></div>
              
              <div className="grid grid-cols-1 md:grid-cols-4 gap-8 relative z-10">
                {[
                  { step: '1', title: 'Create Profile', desc: 'Register and enter your basic clinical parameters like BP, cholesterol, and BMI.' },
                  { step: '2', title: 'Upload Images', desc: 'Optionally upload an ECG or chest X-ray for a more comprehensive analysis.' },
                  { step: '3', title: 'AI Analysis', desc: 'Our multi-modal ML pipeline analyzes all your data in seconds.' },
                  { step: '4', title: 'Get Results', desc: 'Receive a detailed risk report with AI explanations and actionable insights.' },
                ].map((item, i) => (
                  <div key={i} className="flex flex-col items-center text-center">
                    <div className="w-16 h-16 rounded-full bg-white border-4 border-primary flex items-center justify-center text-2xl font-bold text-primary mb-6 shadow-soft">
                      {item.step}
                    </div>
                    <h3 className="text-xl font-heading font-semibold text-navy-900 mb-2">{item.title}</h3>
                    <p className="text-navy-700 text-sm">{item.desc}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* About Section */}
        <section id="about" className="py-24 bg-navy-900 text-white relative bg-grain">
          <div className="max-w-4xl mx-auto px-4 text-center">
            <h2 className="text-3xl md:text-4xl font-heading font-bold mb-8 text-white">Why AyuPulse?</h2>
            <p className="text-lg text-white/90 leading-relaxed mb-12">
              Early detection is the most effective defense against cardiovascular disease. 
              AyuPulse was built to bridge the gap between advanced machine learning capabilities and accessible patient care. 
              By providing transparent, explainable AI, we empower patients to understand their risk factors and facilitate better conversations with their doctors.
            </p>
          </div>
        </section>

        {/* Contact Section */}
        <section id="contact" className="py-24 bg-white">
          <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-heading font-bold text-navy-900 mb-4">Get in Touch</h2>
              <p className="text-navy-700">Have questions? We'd love to hear from you.</p>
            </div>
            
            <form className="space-y-6" onSubmit={(e) => e.preventDefault()}>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="label-text">Name</label>
                  <input type="text" className="input-field" placeholder="John Doe" />
                </div>
                <div>
                  <label className="label-text">Email</label>
                  <input type="email" className="input-field" placeholder="john@example.com" />
                </div>
              </div>
              <div>
                <label className="label-text">Message</label>
                <textarea className="input-field" rows={4} placeholder="How can we help?"></textarea>
              </div>
              <div className="text-center">
                <button type="submit" className="btn-primary w-full md:w-auto px-12">Send Message</button>
              </div>
            </form>
          </div>
        </section>
      </main>
      
      <Footer />
    </div>
  );
};
