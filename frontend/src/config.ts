export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  ENDPOINTS: {
    AUTH: {
      LOGIN: '/auth/login',
      REGISTER: '/auth/register',
      ME: '/auth/me',
      REFRESH: '/auth/refresh',
    },
    PROFILE: {
      BASE: '/profile',
    },
    PATIENTS: {
      BASE: '/patients',
      SEARCH: '/patients/search',
      STATS: '/patients/stats/summary',
    },
    PREDICTIONS: {
      BASE: '/predictions',
      STATS: '/predictions/stats/summary',
      PATIENT: '/predictions/patient',
    },
    ADMIN: {
      USERS: '/admin/users',
      STATS: '/admin/stats',
      TOGGLE_ACTIVE: '/admin/users/{id}/toggle-active',
    },
    HEALTH: '/health',
  },
  STORAGE_KEYS: {
    ACCESS_TOKEN: 'ayu_access_token',
    REFRESH_TOKEN: 'ayu_refresh_token',
    USER_DATA: 'ayu_user_data',
  },
  ROUTES: {
    LOGIN: '/login',
    REGISTER: '/register',
    DASHBOARD: '/dashboard',
    PATIENTS: '/patients',
    PREDICTIONS: '/predictions',
    ADMIN: '/admin',
    PROFILE: '/profile',
  },
} as const;

export const APP_CONFIG = {
  APP_NAME: 'AyuPulse',
  APP_DESCRIPTION: 'Early Heart Disease Risk Prediction System',
  VERSION: '1.0.0',
  DEFAULT_PAGE_SIZE: 10,
  MAX_FILE_SIZE: 10 * 1024 * 1024, // 10MB
  ALLOWED_FILE_TYPES: ['image/jpeg', 'image/png', 'image/jpg', 'image/bmp'],
} as const;