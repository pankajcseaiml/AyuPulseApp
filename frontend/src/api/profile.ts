import { apiFetch } from './base';
import { API_CONFIG } from '../config';

export const profileAPI = {
  create: (data: any) => 
    apiFetch(API_CONFIG.ENDPOINTS.PROFILE.BASE, {
      method: 'POST',
      body: JSON.stringify(data),
    }),
    
  get: () => 
    apiFetch(API_CONFIG.ENDPOINTS.PROFILE.BASE),
    
  update: (data: any) => 
    apiFetch(API_CONFIG.ENDPOINTS.PROFILE.BASE, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),
};
