import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { patientsAPI } from '../api/patients';
import { format } from 'date-fns';

export const PatientsPage: React.FC = () => {
  const [patients, setPatients] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [editingPatient, setEditingPatient] = useState<any>(null);
  const [showForm, setShowForm] = useState(false);
  
  const { register, handleSubmit, reset } = useForm();

  const loadPatients = async () => {
    try {
      setLoading(true);
      const res = await patientsAPI.getAll();
      setPatients(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPatients();
  }, []);

  const handleEdit = (patient: any) => {
    setEditingPatient(patient);
    reset({
      ...patient,
      date_of_birth: format(new Date(patient.date_of_birth), 'yyyy-MM-dd'),
      medical_history: {
        ...patient.medical_history,
        current_medications: patient.medical_history?.current_medications?.join(', ') || ''
      }
    });
    setShowForm(true);
  };

  const handleDelete = async (id: string) => {
    if (confirm('Are you sure you want to delete this patient? This will not delete their prediction history.')) {
      try {
        await patientsAPI.delete(id);
        loadPatients();
      } catch (err) {
        console.error(err);
        alert('Failed to delete patient');
      }
    }
  };

  const onSubmit = async (data: any) => {
    try {
      const payload = {
        ...data,
        age: 0,
        height_cm: parseFloat(data.height_cm),
        weight_kg: parseFloat(data.weight_kg),
        medical_history: {
          diabetes: data.medical_history?.diabetes === 'true' || data.medical_history?.diabetes === true,
          hypertension: data.medical_history?.hypertension === 'true' || data.medical_history?.hypertension === true,
          previous_heart_disease: data.medical_history?.previous_heart_disease === 'true' || data.medical_history?.previous_heart_disease === true,
          family_heart_history: data.medical_history?.family_heart_history === 'true' || data.medical_history?.family_heart_history === true,
          current_medications: data.medical_history?.current_medications ? data.medical_history.current_medications.split(',').map((s: string) => s.trim()) : [],
        }
      };

      if (editingPatient) {
        await patientsAPI.update(editingPatient.id, payload);
      } else {
        await patientsAPI.create(payload);
      }
      
      setShowForm(false);
      setEditingPatient(null);
      reset();
      loadPatients();
    } catch (err: any) {
      alert(err.message || 'Failed to save patient');
    }
  };

  if (loading) return <div className="p-8 text-center">Loading...</div>;

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-heading font-bold text-navy-900 mb-2">Patients Directory</h1>
          <p className="text-navy-600">Manage family members and dependents.</p>
        </div>
        {!showForm && (
          <button 
            onClick={() => {
              setEditingPatient(null);
              reset({});
              setShowForm(true);
            }} 
            className="btn-primary flex items-center gap-2"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" /></svg>
            Add Patient
          </button>
        )}
      </div>

      {showForm ? (
        <div className="bg-white rounded-xl shadow-soft border border-navy-50 p-6 md:p-8 mb-8">
          <div className="flex justify-between items-center border-b border-navy-100 pb-4 mb-6">
            <h2 className="text-xl font-heading font-semibold text-navy-900">
              {editingPatient ? 'Edit Patient' : 'Add New Patient'}
            </h2>
            <button onClick={() => setShowForm(false)} className="text-navy-400 hover:text-navy-700">
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
            </button>
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="label-text">Full Name</label>
                <input type="text" {...register('full_name', { required: true })} className="input-field" />
              </div>
              <div>
                <label className="label-text">Relationship</label>
                <input type="text" {...register('relationship', { required: true })} className="input-field" placeholder="e.g. Father, Mother, Spouse" />
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
                <label className="label-text">Height (cm)</label>
                <input type="number" {...register('height_cm')} className="input-field" step="0.1" />
              </div>
              <div>
                <label className="label-text">Weight (kg)</label>
                <input type="number" {...register('weight_kg')} className="input-field" step="0.1" />
              </div>
              <div>
                <label className="label-text">Blood Group</label>
                <select {...register('blood_group')} className="input-field">
                  <option value="">Unknown</option>
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
            </div>

            <div className="flex justify-end gap-3 pt-6 border-t border-navy-100">
              <button type="button" onClick={() => setShowForm(false)} className="btn-secondary">Cancel</button>
              <button type="submit" className="btn-primary">{editingPatient ? 'Save Changes' : 'Add Patient'}</button>
            </div>
          </form>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {patients.map(p => (
            <div key={p.id} className="card-base hover:shadow-md transition-shadow relative group">
              <div className="absolute top-4 right-4 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                <button onClick={() => handleEdit(p)} className="p-1.5 text-navy-400 hover:text-primary bg-navy-50 rounded-md">
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                </button>
                <button onClick={() => handleDelete(p.id)} className="p-1.5 text-navy-400 hover:text-red-500 bg-navy-50 rounded-md">
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                </button>
              </div>
              
              <div className="w-12 h-12 bg-primary/10 text-primary rounded-full flex items-center justify-center font-bold text-xl mb-4">
                {p.full_name.charAt(0)}
              </div>
              <h3 className="text-xl font-heading font-semibold text-navy-900">{p.full_name}</h3>
              <p className="text-sm font-medium text-navy-500 mb-4">{p.relationship}</p>
              
              <div className="grid grid-cols-2 gap-y-2 text-sm text-navy-600 border-t border-navy-100 pt-4">
                <div><span className="text-navy-400 block text-xs">Age</span>{p.age}</div>
                <div><span className="text-navy-400 block text-xs">Gender</span>{p.gender}</div>
                <div><span className="text-navy-400 block text-xs">Blood Group</span>{p.blood_group || '-'}</div>
                <div><span className="text-navy-400 block text-xs">Added On</span>{format(new Date(p.created_at), 'MMM yyyy')}</div>
              </div>
            </div>
          ))}
          
          {patients.length === 0 && !showForm && (
            <div className="col-span-full py-12 text-center text-navy-500 bg-white rounded-xl border border-dashed border-navy-200">
              No patients found. Add a patient to get started.
            </div>
          )}
        </div>
      )}
    </div>
  );
};
