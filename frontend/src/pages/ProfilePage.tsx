import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { profileAPI } from '../api/profile';
import { patientsAPI } from '../api/patients';
import { useAuth } from '../context/AuthContext';
import { format } from 'date-fns';
import { Link } from 'react-router-dom';

export const ProfilePage: React.FC = () => {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState<'profile' | 'family'>('profile');
  
  // Profile State
  const [profile, setProfile] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<{type: 'success' | 'error', text: string} | null>(null);
  
  // Family State
  const [patients, setPatients] = useState<any[]>([]);

  // Form
  const { register, handleSubmit, reset, watch } = useForm();
  
  useEffect(() => {
    const fetchProfileData = async () => {
      try {
        setLoading(true);
        // Try to get profile
        try {
          const res = await profileAPI.get();
          if (res.data) {
            setProfile(res.data);
            reset(formatProfileForForm(res.data));
          }
        } catch (err: any) {
          if (err.message !== 'Profile not found') {
            console.error(err);
          }
        }
        
        // Get patients
        const pRes = await patientsAPI.getAll();
        setPatients(pRes.data || []);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchProfileData();
  }, [reset]);

  const formatProfileForForm = (data: any) => {
    return {
      ...data,
      date_of_birth: data.date_of_birth ? format(new Date(data.date_of_birth), 'yyyy-MM-dd') : '',
    };
  };

  const calculateBMI = (weight: number, height: number) => {
    if (!weight || !height) return 0;
    const heightInMeters = height / 100;
    return (weight / (heightInMeters * heightInMeters)).toFixed(1);
  };

  const weight = watch('weight_kg');
  const height = watch('height_cm');
  const currentBMI = calculateBMI(weight, height);

  const onSubmitProfile = async (data: any) => {
    setSaving(true);
    setMessage(null);
    try {
      // Clean up data
      const payload = {
        ...data,
        age: 0, // calculated on backend
        height_cm: parseFloat(data.height_cm),
        weight_kg: parseFloat(data.weight_kg),
        lifestyle: {
          smoking: data.lifestyle?.smoking === 'true' || data.lifestyle?.smoking === true,
          alcohol: data.lifestyle?.alcohol === 'true' || data.lifestyle?.alcohol === true,
          exercise_frequency: data.lifestyle?.exercise_frequency || 'Never',
          diet_type: data.lifestyle?.diet_type || 'Vegetarian',
        },
        medical_history: {
          diabetes: data.medical_history?.diabetes === 'true' || data.medical_history?.diabetes === true,
          hypertension: data.medical_history?.hypertension === 'true' || data.medical_history?.hypertension === true,
          previous_heart_disease: data.medical_history?.previous_heart_disease === 'true' || data.medical_history?.previous_heart_disease === true,
          family_heart_history: data.medical_history?.family_heart_history === 'true' || data.medical_history?.family_heart_history === true,
          current_medications: data.medical_history?.current_medications ? data.medical_history.current_medications.split(',').map((s: string) => s.trim()) : [],
        }
      };

      let res;
      if (profile) {
        res = await profileAPI.update(payload);
      } else {
        res = await profileAPI.create(payload);
      }
      
      setProfile(res.data);
      setMessage({ type: 'success', text: 'Profile saved successfully!' });
    } catch (err: any) {
      setMessage({ type: 'error', text: err.message || 'Failed to save profile' });
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex h-[calc(100vh-4rem)] items-center justify-center">
        <div className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in">
      <div className="flex justify-between items-end mb-8">
        <div>
          <h1 className="text-3xl font-heading font-bold text-navy-900 mb-2">Account Settings</h1>
          <p className="text-navy-600">Manage your personal information and family members.</p>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-soft border border-navy-50 overflow-hidden">
        {/* Tabs */}
        <div className="flex border-b border-navy-100 bg-navy-50/50 px-6">
          <button
            className={`py-4 px-6 text-sm font-medium border-b-2 transition-colors ${
              activeTab === 'profile'
                ? 'border-primary text-primary bg-white'
                : 'border-transparent text-navy-500 hover:text-navy-700 hover:border-navy-300'
            }`}
            onClick={() => setActiveTab('profile')}
          >
            My Profile
          </button>
          <button
            className={`py-4 px-6 text-sm font-medium border-b-2 transition-colors ${
              activeTab === 'family'
                ? 'border-primary text-primary bg-white'
                : 'border-transparent text-navy-500 hover:text-navy-700 hover:border-navy-300'
            }`}
            onClick={() => setActiveTab('family')}
          >
            Family Members
          </button>
        </div>

        <div className="p-6 md:p-8">
          {activeTab === 'profile' && (
            <form onSubmit={handleSubmit(onSubmitProfile)} className="space-y-8">
              {message && (
                <div className={`p-4 rounded-lg text-sm ${message.type === 'success' ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'}`}>
                  {message.text}
                </div>
              )}
              
              <section>
                <h3 className="font-heading font-semibold text-lg border-b border-navy-100 pb-2 mb-4">Personal Information</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="label-text">Full Name</label>
                    <input type="text" {...register('full_name', { required: true })} className="input-field" defaultValue={user?.full_name} />
                  </div>
                  <div>
                    <label className="label-text">Date of Birth</label>
                    <input type="date" {...register('date_of_birth', { required: true })} className="input-field" />
                  </div>
                  <div>
                    <label className="label-text">Gender</label>
                    <select {...register('gender')} className="input-field">
                      <option value="Male">Male</option>
                      <option value="Female">Female</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>
                  <div>
                    <label className="label-text">Blood Group</label>
                    <select {...register('blood_group')} className="input-field">
                      <option value="A+">A+</option>
                      <option value="A-">A-</option>
                      <option value="B+">B+</option>
                      <option value="B-">B-</option>
                      <option value="AB+">AB+</option>
                      <option value="AB-">AB-</option>
                      <option value="O+">O+</option>
                      <option value="O-">O-</option>
                    </select>
                  </div>
                  <div>
                    <label className="label-text">Contact Number</label>
                    <input type="text" {...register('contact_number')} className="input-field" />
                  </div>
                  <div>
                    <label className="label-text">Emergency Contact</label>
                    <input type="text" {...register('emergency_contact')} className="input-field" />
                  </div>
                  <div className="md:col-span-2">
                    <label className="label-text">Address</label>
                    <input type="text" {...register('address')} className="input-field" />
                  </div>
                  <div>
                    <label className="label-text">Occupation</label>
                    <input type="text" {...register('occupation')} className="input-field" />
                  </div>
                </div>
              </section>

              <section>
                <h3 className="font-heading font-semibold text-lg border-b border-navy-100 pb-2 mb-4 flex items-center justify-between">
                  Physical Characteristics
                  {Number(currentBMI) > 0 && (
                    <span className="text-sm font-normal bg-navy-100 text-navy-800 px-3 py-1 rounded-full">
                      Calculated BMI: <strong className={Number(currentBMI) > 25 ? 'text-red-600' : 'text-green-600'}>{currentBMI}</strong>
                    </span>
                  )}
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="label-text">Height (cm)</label>
                    <input type="number" {...register('height_cm', { required: true })} className="input-field" step="0.1" />
                  </div>
                  <div>
                    <label className="label-text">Weight (kg)</label>
                    <input type="number" {...register('weight_kg', { required: true })} className="input-field" step="0.1" />
                  </div>
                </div>
              </section>

              <section>
                <h3 className="font-heading font-semibold text-lg border-b border-navy-100 pb-2 mb-4">Lifestyle & Medical History</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="label-text">Exercise Frequency</label>
                    <select {...register('lifestyle.exercise_frequency')} className="input-field">
                      <option value="Never">Never</option>
                      <option value="Rarely">Rarely (1-2 times/month)</option>
                      <option value="Weekly">Weekly (1-3 times/week)</option>
                      <option value="Daily">Daily (4+ times/week)</option>
                    </select>
                  </div>
                  <div>
                    <label className="label-text">Diet Type</label>
                    <select {...register('lifestyle.diet_type')} className="input-field">
                      <option value="Vegetarian">Vegetarian</option>
                      <option value="Non-Vegetarian">Non-Vegetarian</option>
                      <option value="Vegan">Vegan</option>
                    </select>
                  </div>
                  
                  <div className="md:col-span-2 grid grid-cols-2 md:grid-cols-4 gap-4 mt-4">
                   <label className="flex items-center space-x-2">
                     <input type="checkbox" {...register('lifestyle.smoking')} className="rounded text-primary focus:ring-primary" />
                     <span className="text-sm text-navy-800">Smoking</span>
                   </label>
                   <label className="flex items-center space-x-2">
                     <input type="checkbox" {...register('lifestyle.alcohol')} className="rounded text-primary focus:ring-primary" />
                     <span className="text-sm text-navy-800">Alcohol</span>
                   </label>
                   <label className="flex items-center space-x-2">
                     <input type="checkbox" {...register('medical_history.diabetes')} className="rounded text-primary focus:ring-primary" />
                     <span className="text-sm text-navy-800">Diabetes</span>
                   </label>
                   <label className="flex items-center space-x-2">
                     <input type="checkbox" {...register('medical_history.hypertension')} className="rounded text-primary focus:ring-primary" />
                     <span className="text-sm text-navy-800">Hypertension</span>
                   </label>
                   <label className="flex items-center space-x-2">
                     <input type="checkbox" {...register('medical_history.previous_heart_disease')} className="rounded text-primary focus:ring-primary" />
                     <span className="text-sm text-navy-800">Prev. Heart Disease</span>
                   </label>
                   <label className="flex items-center space-x-2">
                     <input type="checkbox" {...register('medical_history.family_heart_history')} className="rounded text-primary focus:ring-primary" />
                     <span className="text-sm text-navy-800">Family History</span>
                   </label>
                 </div>
                  
                  <div className="md:col-span-2 mt-4">
                    <label className="label-text">Current Medications (comma separated)</label>
                    <textarea {...register('medical_history.current_medications')} className="input-field" rows={2} placeholder="e.g. Aspirin, Lisinopril"></textarea>
                  </div>
                </div>
              </section>

              <div className="flex justify-end pt-4">
                <button type="submit" disabled={saving} className="btn-primary flex items-center gap-2">
                  {saving && <svg className="animate-spin h-4 w-4 text-white" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>}
                  {profile ? 'Update Profile' : 'Save Profile'}
                </button>
              </div>
            </form>
          )}

          {activeTab === 'family' && (
            <div>
              <div className="flex justify-between items-center mb-6">
                <h3 className="font-heading font-semibold text-lg">Saved Family Members</h3>
                <Link to="/patients" className="btn-secondary text-sm">Manage Patients Directory</Link>
              </div>
              
              {patients.length === 0 ? (
                <div className="text-center py-12 bg-navy-50 rounded-xl border border-dashed border-navy-200">
                  <svg className="w-12 h-12 text-navy-300 mx-auto mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                  <p className="text-navy-700 font-medium mb-4">No family members added yet.</p>
                  <Link to="/patients" className="btn-primary text-sm inline-flex items-center gap-2">
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" /></svg>
                    Add Family Member
                  </Link>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {patients.map(p => (
                    <div key={p.id} className="border border-navy-100 rounded-xl p-5 hover:border-primary/50 transition-colors bg-white shadow-sm flex flex-col">
                      <div className="flex justify-between items-start mb-3">
                        <div>
                          <h4 className="font-heading font-semibold text-navy-900 text-lg">{p.full_name}</h4>
                          <span className="inline-block px-2.5 py-0.5 rounded-full text-xs font-medium bg-navy-100 text-navy-800 mt-1">
                            {p.relationship}
                          </span>
                        </div>
                        <div className="text-right text-sm text-navy-700">
                          <p>{p.age} years</p>
                          <p>{p.gender}</p>
                        </div>
                      </div>
                      
                      <div className="mt-auto pt-4 flex gap-2">
                        <Link to={`/predictions/new?patient_id=${p.id}`} className="btn-primary flex-1 text-center py-1.5 text-xs">
                          Run Prediction
                        </Link>
                        <Link to={`/patients`} className="btn-secondary py-1.5 px-3 text-xs flex items-center justify-center text-navy-700 hover:text-navy-900 border-navy-200">
                          Edit
                        </Link>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
