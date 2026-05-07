import { apiFetch } from './base';
import { API_CONFIG } from '../config';

export const adminAPI = {
  getStats: () => apiFetch(API_CONFIG.ENDPOINTS.ADMIN.STATS),
  getUsers: () => apiFetch(API_CONFIG.ENDPOINTS.ADMIN.USERS),
  createUser: (data: any) => apiFetch(API_CONFIG.ENDPOINTS.ADMIN.USERS, {
    method: 'POST',
    body: JSON.stringify(data)
  }),
  toggleActive: (id: string) => apiFetch(API_CONFIG.ENDPOINTS.ADMIN.TOGGLE_ACTIVE.replace('{id}', id), {
    method: 'POST'
  }),
  updateUser: (id: string, data: any) => apiFetch(`${API_CONFIG.ENDPOINTS.ADMIN.USERS}/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data)
  }),
  deleteUser: (id: string) => apiFetch(`${API_CONFIG.ENDPOINTS.ADMIN.USERS}/${id}`, {
    method: 'DELETE'
  }),
};
