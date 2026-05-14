import axios from 'axios';
import { API_CONFIG } from '../config';

const api = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem(API_CONFIG.STORAGE_KEYS.ACCESS_TOKEN);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem(API_CONFIG.STORAGE_KEYS.REFRESH_TOKEN);
        if (!refreshToken) {
          throw new Error('No refresh token available');
        }
        
        const response = await axios.post(`${API_CONFIG.BASE_URL}/auth/refresh`, {
          refresh_token: refreshToken,
        });
        
        const { access_token } = response.data;
        localStorage.setItem(API_CONFIG.STORAGE_KEYS.ACCESS_TOKEN, access_token);
        
        originalRequest.headers.Authorization = `Bearer ${access_token}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh failed, clear storage and redirect to login
        localStorage.removeItem(API_CONFIG.STORAGE_KEYS.ACCESS_TOKEN);
        localStorage.removeItem(API_CONFIG.STORAGE_KEYS.REFRESH_TOKEN);
        localStorage.removeItem(API_CONFIG.STORAGE_KEYS.USER_DATA);
        window.location.href = API_CONFIG.ROUTES.LOGIN;
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  name: string;
  role?: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface UserData {
  id: string;
  username: string;
  email: string;
  full_name: string;
  role: 'admin' | 'doctor' | 'staff' | 'patient';
  is_active: boolean;
  created_at: string;
}

class AuthService {
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);
    
    const response = await api.post<AuthResponse>(
      API_CONFIG.ENDPOINTS.AUTH.LOGIN,
      formData,
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      }
    );
    
    if (response.data.access_token) {
      this.setTokens(response.data);
      await this.fetchUserData();
    }
    
    return response.data;
  }

  async register(userData: RegisterData): Promise<UserData> {
    const response = await api.post<UserData>(
      API_CONFIG.ENDPOINTS.AUTH.REGISTER,
      userData
    );
    return response.data;
  }

  async getCurrentUser(): Promise<UserData> {
    const response = await api.get<UserData>(API_CONFIG.ENDPOINTS.AUTH.ME);
    this.setUserData(response.data);
    return response.data;
  }

  async fetchUserData(): Promise<UserData> {
    try {
      const user = await this.getCurrentUser();
      return user;
    } catch (error) {
      console.error('Failed to fetch user data:', error);
      throw error;
    }
  }

  logout(): void {
    localStorage.removeItem(API_CONFIG.STORAGE_KEYS.ACCESS_TOKEN);
    localStorage.removeItem(API_CONFIG.STORAGE_KEYS.REFRESH_TOKEN);
    localStorage.removeItem(API_CONFIG.STORAGE_KEYS.USER_DATA);
    window.location.href = API_CONFIG.ROUTES.LOGIN;
  }

  setTokens(authData: AuthResponse): void {
    localStorage.setItem(API_CONFIG.STORAGE_KEYS.ACCESS_TOKEN, authData.access_token);
    localStorage.setItem(API_CONFIG.STORAGE_KEYS.REFRESH_TOKEN, authData.refresh_token);
  }

  setUserData(userData: UserData): void {
    localStorage.setItem(API_CONFIG.STORAGE_KEYS.USER_DATA, JSON.stringify(userData));
  }

  getUserData(): UserData | null {
    const userData = localStorage.getItem(API_CONFIG.STORAGE_KEYS.USER_DATA);
    return userData ? JSON.parse(userData) : null;
  }

  getAccessToken(): string | null {
    return localStorage.getItem(API_CONFIG.STORAGE_KEYS.ACCESS_TOKEN);
  }

  isAuthenticated(): boolean {
    return !!this.getAccessToken();
  }

  isAdmin(): boolean {
    const user = this.getUserData();
    return user?.role === 'admin';
  }

  isDoctor(): boolean {
    const user = this.getUserData();
    return user?.role === 'doctor';
  }
}

export const authService = new AuthService();
export default api;