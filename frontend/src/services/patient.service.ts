import api from './auth.service';
import { API_CONFIG } from '../config';

export interface Patient {
  id: string;
  first_name: string;
  last_name: string;
  age: number;
  gender: 'male' | 'female' | 'other';
  email?: string;
  phone?: string;
  address?: string;
  medical_history?: string;
  blood_pressure?: string;
  cholesterol?: string;
  bmi?: number;
  smoking_status?: boolean;
  diabetes_status?: boolean;
  family_history?: boolean;
  created_at: string;
  updated_at: string;
  created_by: string;
}

export interface CreatePatientRequest {
  first_name: string;
  last_name: string;
  age: number;
  gender: 'male' | 'female' | 'other';
  email?: string;
  phone?: string;
  address?: string;
  medical_history?: string;
  blood_pressure?: string;
  cholesterol?: string;
  bmi?: number;
  smoking_status?: boolean;
  diabetes_status?: boolean;
  family_history?: boolean;
}

export type UpdatePatientRequest = Partial<CreatePatientRequest>;

export interface PatientStats {
  total_patients: number;
  male_count: number;
  female_count: number;
  average_age: number;
  high_risk_count: number;
  recent_patients: number;
}

export interface SearchParams {
  query?: string;
  gender?: string;
  min_age?: number;
  max_age?: number;
  page?: number;
  limit?: number;
}

// Backend patient interface (what the API actually returns)
interface BackendPatient {
  id: string;
  name: string;
  age: number;
  gender: string;
  contact?: string;
  medical_history?: string;
  doctor_id?: string;
  created_at: string;
  updated_at: string;
  // Clinical fields
  currentSmoker?: number;
  cigsPerDay?: number;
  BPMeds?: number;
  prevalentStroke?: number;
  prevalentHyp?: number;
  diabetes?: number;
  totChol?: number;
  sysBP?: number;
  diaBP?: number;
  BMI?: number;
  heartRate?: number;
  glucose?: number;
  CP?: number;
}

// Backend patient create/update request
interface BackendPatientRequest {
  name: string;
  age: number;
  gender: string;
  contact?: string;
  medical_history?: string;
  // Clinical fields
  currentSmoker?: number;
  cigsPerDay?: number;
  BPMeds?: number;
  prevalentStroke?: number;
  prevalentHyp?: number;
  diabetes?: number;
  totChol?: number;
  sysBP?: number;
  diaBP?: number;
  BMI?: number;
  heartRate?: number;
  glucose?: number;
  CP?: number;
}

class PatientService {
  // Transform backend patient to frontend patient
  private transformBackendToFrontend(backendPatient: BackendPatient): Patient {
    // Parse name into first and last name
    const nameParts = backendPatient.name.split(' ');
    const first_name = nameParts[0] || '';
    const last_name = nameParts.slice(1).join(' ') || '';
    
    // Parse contact info (backend uses single contact field, frontend has email/phone/address)
    let email = '';
    let phone = '';
    let address = '';
    if (backendPatient.contact) {
      // Simple parsing - in a real app, you'd have more sophisticated parsing
      if (backendPatient.contact.includes('@')) {
        email = backendPatient.contact;
      } else if (/^\d+$/.test(backendPatient.contact.replace(/\D/g, ''))) {
        phone = backendPatient.contact;
      } else {
        address = backendPatient.contact;
      }
    }
    
    // Parse blood pressure from sysBP and diaBP
    let blood_pressure = '';
    if (backendPatient.sysBP !== undefined && backendPatient.diaBP !== undefined) {
      blood_pressure = `${backendPatient.sysBP}/${backendPatient.diaBP}`;
    }
    
    // Transform clinical fields
    const smoking_status = backendPatient.currentSmoker === 1;
    const diabetes_status = backendPatient.diabetes === 1;
    // family_history maps to prevalentHyp (hypertension) or prevalentStroke
    const family_history = (backendPatient.prevalentHyp === 1) || (backendPatient.prevalentStroke === 1);
    
    return {
      id: backendPatient.id,
      first_name,
      last_name,
      age: backendPatient.age,
      gender: backendPatient.gender as 'male' | 'female' | 'other',
      email: email || undefined,
      phone: phone || undefined,
      address: address || undefined,
      medical_history: backendPatient.medical_history,
      blood_pressure: blood_pressure || undefined,
      cholesterol: backendPatient.totChol?.toString() || undefined,
      bmi: backendPatient.BMI,
      smoking_status,
      diabetes_status,
      family_history,
      created_at: backendPatient.created_at,
      updated_at: backendPatient.updated_at,
      created_by: backendPatient.doctor_id || '',
    };
  }
  
  // Transform frontend patient request to backend request
  private transformFrontendToBackend(patientData: CreatePatientRequest | UpdatePatientRequest): BackendPatientRequest {
    // Combine first and last name (handle undefined for update)
    const firstName = patientData.first_name || '';
    const lastName = patientData.last_name || '';
    const name = `${firstName} ${lastName}`.trim();
    
    // Combine contact info (prioritize email, then phone, then address)
    let contact = '';
    if (patientData.email) {
      contact = patientData.email;
    } else if (patientData.phone) {
      contact = patientData.phone;
    } else if (patientData.address) {
      contact = patientData.address;
    }
    
    // Parse blood pressure string into sysBP and diaBP
    let sysBP: number | undefined;
    let diaBP: number | undefined;
    if (patientData.blood_pressure) {
      const bpParts = patientData.blood_pressure.split('/').map(Number);
      if (bpParts.length >= 2 && !isNaN(bpParts[0]) && !isNaN(bpParts[1])) {
        sysBP = bpParts[0];
        diaBP = bpParts[1];
      }
    }
    
    // Transform clinical fields (handle undefined for update)
    const currentSmoker = patientData.smoking_status ? 1 : 0;
    const diabetes = patientData.diabetes_status ? 1 : 0;
    // For family_history, we set prevalentHyp (hypertension) as a proxy
    const prevalentHyp = patientData.family_history ? 1 : 0;
    
    // Build result object, only including fields that are defined
    const result: BackendPatientRequest = {
      name,
      age: patientData.age || 0, // Default to 0 if undefined
      gender: patientData.gender || 'other', // Default if undefined
    };
    
    // Add optional fields only if they have values
    if (contact) result.contact = contact;
    if (patientData.medical_history !== undefined) result.medical_history = patientData.medical_history;
    
    // Clinical fields
    result.currentSmoker = currentSmoker;
    result.cigsPerDay = patientData.smoking_status ? 10 : 0;
    result.BPMeds = 0;
    result.prevalentStroke = 0;
    result.prevalentHyp = prevalentHyp;
    result.diabetes = diabetes;
    
    if (patientData.cholesterol) {
      result.totChol = parseFloat(patientData.cholesterol);
    }
    
    if (sysBP !== undefined) result.sysBP = sysBP;
    if (diaBP !== undefined) result.diaBP = diaBP;
    if (patientData.bmi !== undefined) result.BMI = patientData.bmi;
    
    result.heartRate = 75;
    result.glucose = 85;
    result.CP = 1;
    
    return result;
  }
  
  async getPatients(page = 1, limit = 10): Promise<Patient[]> {
    const response = await api.get<BackendPatient[]>(API_CONFIG.ENDPOINTS.PATIENTS.BASE, {
      params: { page, limit },
    });
    // Transform each backend patient to frontend format
    return response.data.map(patient => this.transformBackendToFrontend(patient));
  }

  async getPatient(id: string): Promise<Patient> {
    const response = await api.get<BackendPatient>(`${API_CONFIG.ENDPOINTS.PATIENTS.BASE}/${id}`);
    return this.transformBackendToFrontend(response.data);
  }

  async createPatient(patientData: CreatePatientRequest): Promise<Patient> {
    const backendData = this.transformFrontendToBackend(patientData);
    const response = await api.post<BackendPatient>(API_CONFIG.ENDPOINTS.PATIENTS.BASE, backendData);
    return this.transformBackendToFrontend(response.data);
  }

  async updatePatient(id: string, patientData: UpdatePatientRequest): Promise<Patient> {
    const backendData = this.transformFrontendToBackend(patientData);
    const response = await api.put<BackendPatient>(`${API_CONFIG.ENDPOINTS.PATIENTS.BASE}/${id}`, backendData);
    return this.transformBackendToFrontend(response.data);
  }

  async deletePatient(id: string): Promise<{ message: string }> {
    const response = await api.delete<{ message: string }>(`${API_CONFIG.ENDPOINTS.PATIENTS.BASE}/${id}`);
    return response.data;
  }

  async searchPatients(params: SearchParams): Promise<Patient[]> {
    const response = await api.get<BackendPatient[]>(API_CONFIG.ENDPOINTS.PATIENTS.SEARCH, {
      params,
    });
    return response.data.map(patient => this.transformBackendToFrontend(patient));
  }

  async getPatientStats(): Promise<PatientStats> {
    const response = await api.get<PatientStats>(API_CONFIG.ENDPOINTS.PATIENTS.STATS);
    return response.data;
  }

  // Helper methods
  getFullName(patient: Patient): string {
    return `${patient.first_name} ${patient.last_name}`;
  }

  getAgeGroup(age: number): string {
    if (age < 18) return 'Child';
    if (age < 40) return 'Young Adult';
    if (age < 60) return 'Middle Aged';
    return 'Senior';
  }

  calculateRiskScore(patient: Patient): number {
    let score = 0;
    
    // Age factor
    if (patient.age >= 50) score += 30;
    else if (patient.age >= 40) score += 20;
    else if (patient.age >= 30) score += 10;
    
    // Gender factor (males have higher risk)
    if (patient.gender === 'male') score += 10;
    
    // BMI factor
    if (patient.bmi) {
      if (patient.bmi >= 30) score += 25;
      else if (patient.bmi >= 25) score += 15;
    }
    
    // Medical history factors
    if (patient.smoking_status) score += 20;
    if (patient.diabetes_status) score += 15;
    if (patient.family_history) score += 10;
    
    // Blood pressure (simplified)
    if (patient.blood_pressure) {
      const bp = patient.blood_pressure.split('/').map(Number);
      if (bp[0] >= 140 || bp[1] >= 90) score += 15;
    }
    
    return Math.min(score, 100);
  }

  getRiskLevel(score: number): { level: string; color: string; description: string } {
    if (score >= 70) {
      return {
        level: 'High',
        color: 'red',
        description: 'High risk - Immediate attention recommended',
      };
    } else if (score >= 40) {
      return {
        level: 'Medium',
        color: 'yellow',
        description: 'Moderate risk - Regular monitoring needed',
      };
    } else {
      return {
        level: 'Low',
        color: 'green',
        description: 'Low risk - Continue healthy lifestyle',
      };
    }
  }

  formatPatientForForm(patient?: Patient): Partial<CreatePatientRequest> {
    if (!patient) {
      return {
        first_name: '',
        last_name: '',
        age: 30,
        gender: 'male',
        email: '',
        phone: '',
        address: '',
        medical_history: '',
        blood_pressure: '',
        cholesterol: '',
        bmi: undefined,
        smoking_status: false,
        diabetes_status: false,
        family_history: false,
      };
    }

    return {
      first_name: patient.first_name,
      last_name: patient.last_name,
      age: patient.age,
      gender: patient.gender,
      email: patient.email,
      phone: patient.phone,
      address: patient.address,
      medical_history: patient.medical_history,
      blood_pressure: patient.blood_pressure,
      cholesterol: patient.cholesterol,
      bmi: patient.bmi,
      smoking_status: patient.smoking_status,
      diabetes_status: patient.diabetes_status,
      family_history: patient.family_history,
    };
  }
}

export const patientService = new PatientService();