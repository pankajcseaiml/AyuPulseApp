import { apiFetch } from './base';
import { API_CONFIG } from '../config';

export const authAPI = {
  login: async (credentials: URLSearchParams) => {
    // login expects form data (OAuth2PasswordRequestForm)
    const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.AUTH.LOGIN}`, {
      method: 'POST',
      body: credentials,
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    
    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.detail || 'Login failed');
    }
    return response.json();
  },
  
  register: (data: any) => 
    apiFetch(API_CONFIG.ENDPOINTS.AUTH.REGISTER, {
      method: 'POST',
      body: JSON.stringify(data),
    }),
    
  getMe: () => 
    apiFetch(API_CONFIG.ENDPOINTS.AUTH.ME),
};
