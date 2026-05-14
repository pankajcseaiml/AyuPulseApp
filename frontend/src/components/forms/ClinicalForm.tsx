import React from 'react';

// Ranges for visual indicators
const ranges = {
  sysBP: { min: 90, max: 120, borderMax: 140 },
  diaBP: { min: 60, max: 80, borderMax: 90 },
  totChol: { min: 0, max: 200, borderMax: 240 },
  BMI: { min: 18.5, max: 24.9, borderMax: 29.9 },
  glucose: { min: 70, max: 100, borderMax: 126 },
  heartRate: { min: 60, max: 100 },
};

const getRangeStatus = (param: keyof typeof ranges, value: number) => {
  if (!value || isNaN(value)) return 'neutral';
  const range = ranges[param];
  
  if (param === 'heartRate') {
    return value >= range.min && value <= range.max ? 'success' : 'danger';
  }
  
  if (value < range.min) return 'danger';
  if (value <= range.max) return 'success';
  if ('borderMax' in range && value <= range.borderMax!) return 'warning';
  return 'danger';
};

const StatusIndicator: React.FC<{ status: string }> = ({ status }) => {
  const colors = {
    neutral: 'bg-navy-200',
    success: 'bg-green-500',
    warning: 'bg-amber-500',
    danger: 'bg-red-500',
  };
  return <div className={`w-2 h-2 rounded-full ${colors[status as keyof typeof colors]} ml-2`} />;
};

interface ClinicalFormProps {
  data: any;
  onChange: (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => void;
  errors: Record<string, string>;
}

export const ClinicalForm: React.FC<ClinicalFormProps> = ({ data, onChange, errors }) => {
  return (
    <div className="space-y-8">
      {/* Group A: Demographics */}
      <section>
        <h3 className="font-heading font-semibold text-lg border-b border-navy-100 pb-2 mb-4">A. Demographics</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="label-text">Gender</label>
            <select name="gender" value={data.gender} onChange={onChange} className="input-field">
              <option value="">Select Gender</option>
              <option value="1">Male</option>
              <option value="0">Female</option>
            </select>
            {errors.gender && <p className="text-red-500 text-xs mt-1">{errors.gender}</p>}
          </div>
          <div>
            <label className="label-text">Age</label>
            <input type="number" name="age" value={data.age} onChange={onChange} min="1" max="120" className="input-field" placeholder="Years" />
            {errors.age && <p className="text-red-500 text-xs mt-1">{errors.age}</p>}
          </div>
        </div>
      </section>

      {/* Group B: Cardiovascular */}
      <section>
        <h3 className="font-heading font-semibold text-lg border-b border-navy-100 pb-2 mb-4">B. Cardiovascular</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="label-text flex items-center">
              Systolic BP (mmHg) <span className="text-navy-400 font-normal ml-2 text-xs">Normal: 90-120</span>
              <StatusIndicator status={getRangeStatus('sysBP', data.sysBP)} />
            </label>
            <input type="number" name="sysBP" value={data.sysBP} onChange={onChange} className="input-field" />
            {errors.sysBP && <p className="text-red-500 text-xs mt-1">{errors.sysBP}</p>}
          </div>
          <div>
            <label className="label-text flex items-center">
              Diastolic BP (mmHg) <span className="text-navy-400 font-normal ml-2 text-xs">Normal: 60-80</span>
              <StatusIndicator status={getRangeStatus('diaBP', data.diaBP)} />
            </label>
            <input type="number" name="diaBP" value={data.diaBP} onChange={onChange} className="input-field" />
            {errors.diaBP && <p className="text-red-500 text-xs mt-1">{errors.diaBP}</p>}
          </div>
          <div>
            <label className="label-text flex items-center">
              Heart Rate (bpm) <span className="text-navy-400 font-normal ml-2 text-xs">Normal: 60-100</span>
              <StatusIndicator status={getRangeStatus('heartRate', data.heartRate)} />
            </label>
            <input type="number" name="heartRate" value={data.heartRate} onChange={onChange} className="input-field" />
            {errors.heartRate && <p className="text-red-500 text-xs mt-1">{errors.heartRate}</p>}
          </div>
          <div>
            <label className="label-text">Chest Pain Type</label>
            <select name="CP" value={data.CP} onChange={onChange} className="input-field">
              <option value="0">0 - No pain</option>
              <option value="1">1 - Typical angina</option>
              <option value="2">2 - Atypical angina</option>
              <option value="3">3 - Non-anginal</option>
            </select>
          </div>
          <div className="flex items-center mt-6">
            <input type="checkbox" id="BPMeds" name="BPMeds" checked={data.BPMeds === 1} onChange={(e) => onChange({ target: { name: 'BPMeds', value: e.target.checked ? 1 : 0 } } as any)} className="w-4 h-4 text-primary rounded border-navy-300 focus:ring-primary" />
            <label htmlFor="BPMeds" className="ml-2 text-sm text-navy-700">Currently taking BP Medication</label>
          </div>
          <div className="flex items-center mt-6">
            <input type="checkbox" id="prevalentHyp" name="prevalentHyp" checked={data.prevalentHyp === 1} onChange={(e) => onChange({ target: { name: 'prevalentHyp', value: e.target.checked ? 1 : 0 } } as any)} className="w-4 h-4 text-primary rounded border-navy-300 focus:ring-primary" />
            <label htmlFor="prevalentHyp" className="ml-2 text-sm text-navy-700">History of Hypertension</label>
          </div>
          <div className="flex items-center">
            <input type="checkbox" id="prevalentStroke" name="prevalentStroke" checked={data.prevalentStroke === 1} onChange={(e) => onChange({ target: { name: 'prevalentStroke', value: e.target.checked ? 1 : 0 } } as any)} className="w-4 h-4 text-primary rounded border-navy-300 focus:ring-primary" />
            <label htmlFor="prevalentStroke" className="ml-2 text-sm text-navy-700">History of Stroke</label>
          </div>
        </div>
      </section>

      {/* Group C: Metabolic */}
      <section>
        <h3 className="font-heading font-semibold text-lg border-b border-navy-100 pb-2 mb-4">C. Metabolic</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="label-text flex items-center">
              Total Cholesterol (mg/dL) <span className="text-navy-400 font-normal ml-2 text-xs">Normal: &lt;200</span>
              <StatusIndicator status={getRangeStatus('totChol', data.totChol)} />
            </label>
            <input type="number" name="totChol" value={data.totChol} onChange={onChange} className="input-field" />
            {errors.totChol && <p className="text-red-500 text-xs mt-1">{errors.totChol}</p>}
          </div>
          <div>
            <label className="label-text flex items-center">
              Blood Glucose (mg/dL) <span className="text-navy-400 font-normal ml-2 text-xs">Normal: 70-100</span>
              <StatusIndicator status={getRangeStatus('glucose', data.glucose)} />
            </label>
            <input type="number" name="glucose" value={data.glucose} onChange={onChange} className="input-field" />
            {errors.glucose && <p className="text-red-500 text-xs mt-1">{errors.glucose}</p>}
          </div>
          <div>
            <label className="label-text">Height (cm)</label>
            <input type="number" name="height_cm" value={data.height_cm} onChange={onChange} className="input-field" step="0.1" />
          </div>
          <div>
            <label className="label-text">Weight (kg)</label>
            <input type="number" name="weight_kg" value={data.weight_kg} onChange={onChange} className="input-field" step="0.1" />
          </div>
          <div>
            <label className="label-text flex items-center">
              BMI (kg/m²) <span className="text-navy-400 font-normal ml-2 text-xs">Normal: 18.5-24.9</span>
              <StatusIndicator status={getRangeStatus('BMI', parseFloat(data.BMI))} />
            </label>
            <input type="number" name="BMI" value={data.BMI} readOnly className="input-field bg-navy-50" step="0.1" />
            {errors.BMI && <p className="text-red-500 text-xs mt-1">{errors.BMI}</p>}
          </div>
          <div className="flex items-center mt-6">
            <input type="checkbox" id="diabetes" name="diabetes" checked={data.diabetes === 1} onChange={(e) => onChange({ target: { name: 'diabetes', value: e.target.checked ? 1 : 0 } } as any)} className="w-4 h-4 text-primary rounded border-navy-300 focus:ring-primary" />
            <label htmlFor="diabetes" className="ml-2 text-sm text-navy-700">Has Diabetes</label>
          </div>
        </div>
      </section>

      {/* Group D: Lifestyle */}
      <section>
        <h3 className="font-heading font-semibold text-lg border-b border-navy-100 pb-2 mb-4">D. Lifestyle</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="flex items-center">
            <input type="checkbox" id="currentSmoker" name="currentSmoker" checked={data.currentSmoker === 1} onChange={(e) => {
              onChange({ target: { name: 'currentSmoker', value: e.target.checked ? 1 : 0 } } as any);
              if (!e.target.checked) onChange({ target: { name: 'cigsPerDay', value: 0 } } as any);
            }} className="w-4 h-4 text-primary rounded border-navy-300 focus:ring-primary" />
            <label htmlFor="currentSmoker" className="ml-2 text-sm text-navy-700">Current Smoker</label>
          </div>
          
          {data.currentSmoker === 1 && (
            <div>
              <label className="label-text">Cigarettes per Day</label>
              <input type="number" name="cigsPerDay" value={data.cigsPerDay} onChange={onChange} className="input-field" min="1" />
              {errors.cigsPerDay && <p className="text-red-500 text-xs mt-1">{errors.cigsPerDay}</p>}
            </div>
          )}
        </div>
      </section>
    </div>
  );
};
