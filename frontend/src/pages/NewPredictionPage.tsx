import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { ClinicalForm } from '../components/forms/ClinicalForm';
import { ImageUpload } from '../components/forms/ImageUpload';
import { predictionsAPI } from '../api/predictions';
import { patientsAPI } from '../api/patients';
import { profileAPI } from '../api/profile';

export const NewPredictionPage: React.FC = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const defaultPatientId = searchParams.get('patient_id');
  
  const [patients, setPatients] = useState<any[]>([]);
  const [selectedSubject, setSelectedSubject] = useState<string>(defaultPatientId || 'self');
  
  const [loading, setLoading] = useState(false);
  const [fetchingProfile, setFetchingProfile] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Form State
  const [clinicalData, setClinicalData] = useState({
    gender: '', age: '', sysBP: '', diaBP: '', totChol: '',
    height_cm: '', weight_kg: '',
    BMI: 0, heartRate: '', glucose: '', cigsPerDay: 0,
    currentSmoker: 0, BPMeds: 0, prevalentStroke: 0,
    prevalentHyp: 0, diabetes: 0, CP: '0'
  });
  
  const [xrayFile, setXrayFile] = useState<File | null>(null);
  const [ecgFile, setEcgFile] = useState<File | null>(null);
  const [errors, setErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    const loadSubjects = async () => {
      try {
        const [patientsRes, profileRes] = await Promise.all([
          patientsAPI.getAll().catch(() => ({ data: [] })),
          profileAPI.get().catch(() => ({ data: null }))
        ]);
        
        setPatients(patientsRes.data || []);
        
        // If subject is selected, pre-fill data
        const targetId = defaultPatientId || 'self';
        let sourceData = null;
        
        if (targetId === 'self' && profileRes.data) {
          sourceData = profileRes.data;
        } else if (targetId !== 'self') {
          const patient = patientsRes.data?.find((p: any) => p.id === targetId);
          if (patient) sourceData = patient;
        }
        
        if (sourceData) {
          // Pre-fill logic based on profile/patient model
          setClinicalData(prev => ({
            ...prev,
            gender: sourceData.gender === 'Female' ? '0' : '1',
            age: sourceData.age?.toString() || '',
            sysBP: '', diaBP: '', totChol: '', heartRate: '', glucose: '', // Leave lab values blank
            height_cm: sourceData.height_cm?.toString() || '',
            weight_kg: sourceData.weight_kg?.toString() || '',
            BMI: sourceData.height_cm && sourceData.weight_kg ?
                 parseFloat((sourceData.weight_kg / Math.pow(sourceData.height_cm/100, 2)).toFixed(1)) : 0,
            cigsPerDay: 0,
            currentSmoker: sourceData.lifestyle?.smoking ? 1 : 0,
            BPMeds: 0,
            prevalentStroke: sourceData.medical_history?.previous_heart_disease ? 1 : 0,
            prevalentHyp: sourceData.medical_history?.hypertension ? 1 : 0,
            diabetes: sourceData.medical_history?.diabetes ? 1 : 0,
          }));
        }
      } catch (err) {
        console.error("Error loading subjects", err);
      } finally {
        setFetchingProfile(false);
      }
    };
    
    loadSubjects();
  }, [defaultPatientId]);

  const handleSubjectChange = async (e: React.ChangeEvent<HTMLSelectElement>) => {
    const val = e.target.value;
    setSelectedSubject(val);
    
    // Attempt to pre-fill again
    try {
      let sourceData = null;
      if (val === 'self') {
        const res = await profileAPI.get();
        sourceData = res.data;
      } else {
        const res = await patientsAPI.getOne(val);
        sourceData = res.data;
      }
      
      if (sourceData) {
        setClinicalData(prev => ({
          ...prev,
          gender: sourceData.gender === 'Female' ? '0' : '1',
          age: sourceData.age?.toString() || '',
          height_cm: sourceData.height_cm?.toString() || prev.height_cm,
          weight_kg: sourceData.weight_kg?.toString() || prev.weight_kg,
          BMI: sourceData.height_cm && sourceData.weight_kg ?
               parseFloat((sourceData.weight_kg / Math.pow(sourceData.height_cm/100, 2)).toFixed(1)) : prev.BMI,
          currentSmoker: sourceData.lifestyle?.smoking ? 1 : 0,
          prevalentStroke: sourceData.medical_history?.previous_heart_disease ? 1 : 0,
          prevalentHyp: sourceData.medical_history?.hypertension ? 1 : 0,
          diabetes: sourceData.medical_history?.diabetes ? 1 : 0,
        }));
      }
    } catch(err) {
      // ignore
    }
  };

  const handleClinicalChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    
    setClinicalData(prev => {
      let val = value;
      if (type === 'number' && value !== '') {
        val = parseFloat(value) as any;
      }
      const next = { ...prev, [name]: val };
      
      if (name === 'height_cm' || name === 'weight_kg') {
        const h = parseFloat(next.height_cm);
        const w = parseFloat(next.weight_kg);
        if (h && w && h > 0 && w > 0) {
          next.BMI = parseFloat((w / Math.pow(h / 100, 2)).toFixed(1));
        } else {
          next.BMI = 0;
        }
      }
      
      return next;
    });
    
    // Clear error for this field
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validateForm = () => {
    const newErrors: Record<string, string> = {};
    const requiredStr = ['gender', 'age', 'sysBP', 'diaBP', 'totChol', 'heartRate', 'glucose'];
    
    requiredStr.forEach(field => {
      if (clinicalData[field as keyof typeof clinicalData] === '') {
        newErrors[field] = 'This field is required';
      }
    });
    
    // Special validation for BMI (it's a number, not string)
    if (clinicalData.BMI === 0) {
      newErrors.BMI = 'BMI must be calculated (enter height and weight)';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    
    if (!validateForm()) {
      window.scrollTo({ top: 0, behavior: 'smooth' });
      return;
    }
    
    setLoading(true);
    try {
      const formData = new FormData();
      
      // Convert all clinical data values to numbers where necessary
      const formattedClinicalData = {
        ...clinicalData,
        gender: parseInt(clinicalData.gender as string),
        age: parseInt(clinicalData.age as string),
        sysBP: parseFloat(clinicalData.sysBP as string),
        diaBP: parseFloat(clinicalData.diaBP as string),
        totChol: parseFloat(clinicalData.totChol as string),
        BMI: clinicalData.BMI,
        heartRate: parseFloat(clinicalData.heartRate as string),
        glucose: parseFloat(clinicalData.glucose as string),
        CP: parseInt(clinicalData.CP as string),
      };
      
      formData.append('clinical_data', JSON.stringify(formattedClinicalData));
      
      if (selectedSubject !== 'self') {
        formData.append('patient_id', selectedSubject);
      }
      
      if (xrayFile) formData.append('xray_file', xrayFile);
      if (ecgFile) formData.append('ecg_file', ecgFile);
      
      const res = await predictionsAPI.create(formData);
      navigate(`/predictions/${res.data.id}`);
      
    } catch (err: any) {
      setError(err.message || 'Failed to run prediction. Please try again.');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } finally {
      setLoading(false);
    }
  };

  if (fetchingProfile) return <div className="p-8 text-center">Loading...</div>;

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in">
      <div className="mb-8">
        <h1 className="text-3xl font-heading font-bold text-navy-900 mb-2">New Prediction</h1>
        <p className="text-navy-600">Enter clinical parameters and upload images to calculate cardiovascular risk.</p>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-800 rounded-xl p-4 mb-8">
          <p className="font-medium">Error</p>
          <p className="text-sm">{error}</p>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-8">
        <div className="card-base p-6 md:p-8">
          <div className="mb-8 border-b border-navy-100 pb-6">
            <label className="label-text text-base font-semibold">Subject</label>
            <p className="text-sm text-navy-700 mb-3">Who is this prediction for?</p>
            <select
              value={selectedSubject}
              onChange={handleSubjectChange}
              className="input-field max-w-md"
            >
              <option value="self">My Profile</option>
              {patients.map(p => (
                <option key={p.id} value={p.id}>{p.full_name} ({p.relationship})</option>
              ))}
            </select>
            <p className="text-xs text-navy-600 mt-2">Selecting a profile will pre-fill known values.</p>
          </div>

          <ClinicalForm 
            data={clinicalData} 
            onChange={handleClinicalChange} 
            errors={errors} 
          />
        </div>

        <div className="card-base p-6 md:p-8">
          <div className="mb-6">
            <h3 className="font-heading font-semibold text-lg border-b border-navy-100 pb-2">E. Medical Imaging (Optional)</h3>
            <p className="text-sm text-navy-700 mt-2">Upload images to enable multi-modal analysis for higher accuracy.</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <ImageUpload 
              label="Chest X-Ray" 
              accept="image/jpeg,image/png,image/bmp" 
              onUpload={setXrayFile} 
            />
            <ImageUpload 
              label="ECG (Electrocardiogram)" 
              accept="image/jpeg,image/png,image/bmp" 
              onUpload={setEcgFile} 
            />
          </div>
        </div>

        <div className="flex justify-end pt-4 pb-12">
          <button 
            type="submit" 
            disabled={loading} 
            className="btn-primary text-lg px-8 py-3 w-full md:w-auto flex justify-center items-center gap-2"
          >
            {loading ? (
              <>
                <svg className="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                Processing AI Models...
              </>
            ) : (
              'Run Prediction'
            )}
          </button>
        </div>
      </form>
    </div>
  );
};
