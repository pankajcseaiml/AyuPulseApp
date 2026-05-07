import { apiFetch } from './base';
import { API_CONFIG } from '../config';

export const patientsAPI = {
  create: (data: any) => 
    apiFetch(API_CONFIG.ENDPOINTS.PATIENTS.BASE, {
      method: 'POST',
      body: JSON.stringify(data),
    }),
    
  getAll: () => 
    apiFetch(API_CONFIG.ENDPOINTS.PATIENTS.BASE),
    
  getOne: (id: string) => 
    apiFetch(`${API_CONFIG.ENDPOINTS.PATIENTS.BASE}/${id}`),
    
  update: (id: string, data: any) => 
    apiFetch(`${API_CONFIG.ENDPOINTS.PATIENTS.BASE}/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),
    
  delete: (id: string) => 
    apiFetch(`${API_CONFIG.ENDPOINTS.PATIENTS.BASE}/${id}`, {
      method: 'DELETE',
    }),
};
