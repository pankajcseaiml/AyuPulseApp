import { apiFetch, apiFetchMultipart } from './base';
import { API_CONFIG } from '../config';

export const predictionsAPI = {
  create: (formData: FormData) => 
    apiFetchMultipart(API_CONFIG.ENDPOINTS.PREDICTIONS.BASE, formData),
    
  getAll: () => 
    apiFetch(API_CONFIG.ENDPOINTS.PREDICTIONS.BASE),
    
  getOne: (id: string) => 
    apiFetch(`${API_CONFIG.ENDPOINTS.PREDICTIONS.BASE}/${id}`),
    
  getByPatient: (patientId: string) => 
    apiFetch(`${API_CONFIG.ENDPOINTS.PREDICTIONS.PATIENT}/${patientId}`),
    
  getStatsSummary: () => 
    apiFetch(API_CONFIG.ENDPOINTS.PREDICTIONS.STATS),
    
  delete: (id: string) => 
    apiFetch(`${API_CONFIG.ENDPOINTS.PREDICTIONS.BASE}/${id}`, {
      method: 'DELETE',
    }),
};
