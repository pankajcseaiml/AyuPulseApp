import { API_CONFIG } from '../config';

const getHeaders = () => {
  const token = localStorage.getItem(API_CONFIG.STORAGE_KEYS.ACCESS_TOKEN);
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
};

const handleResponse = async (response: Response) => {
  const data = await response.json();
  if (!response.ok) {
    if (response.status === 401) {
      localStorage.removeItem(API_CONFIG.STORAGE_KEYS.ACCESS_TOKEN);
      localStorage.removeItem(API_CONFIG.STORAGE_KEYS.USER_DATA);
      window.location.href = API_CONFIG.ROUTES.LOGIN;
    }
    // Try to extract error message from various possible fields
    const errorMessage = data.detail || data.error || data.message || 'Something went wrong';
    throw new Error(errorMessage);
  }
  return data;
};

export const apiFetch = async (endpoint: string, options: RequestInit = {}) => {
  const response = await fetch(`${API_CONFIG.BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      ...getHeaders(),
      ...options.headers,
    },
  });
  return handleResponse(response);
};

export const apiFetchMultipart = async (endpoint: string, formData: FormData) => {
  const token = localStorage.getItem(API_CONFIG.STORAGE_KEYS.ACCESS_TOKEN);
  const response = await fetch(`${API_CONFIG.BASE_URL}${endpoint}`, {
    method: 'POST',
    body: formData,
    headers: {
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      // DO NOT set Content-Type to multipart/form-data here, browser does it with boundary
    },
  });
  return handleResponse(response);
};
