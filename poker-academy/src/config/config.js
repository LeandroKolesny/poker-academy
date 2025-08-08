// src/config/config.js
// Configuração centralizada para URLs e constantes da aplicação

// Detectar ambiente automaticamente
const isDevelopment = process.env.NODE_ENV === 'development' || window.location.hostname === 'localhost';
const isProduction = process.env.NODE_ENV === 'production';

// Configurações por ambiente
const environments = {
  development: {
    API_BASE_URL: 'http://localhost:5000',
    FRONTEND_URL: 'http://localhost:3000',
    WEBSOCKET_URL: 'ws://localhost:5000',
    ENVIRONMENT: 'development'
  },
  production: {
    API_BASE_URL: '/api',
    FRONTEND_URL: 'http://142.93.206.128',
    WEBSOCKET_URL: 'ws://142.93.206.128:5000',
    ENVIRONMENT: 'production'
  },
  server: {
    API_BASE_URL: '/api',
    FRONTEND_URL: 'https://grinders.com.br',
    WEBSOCKET_URL: 'wss://grinders.com.br',
    ENVIRONMENT: 'server'
  },
  domain: {
    API_BASE_URL: '/api',
    FRONTEND_URL: 'https://cardroomgrinders.com.br',
    WEBSOCKET_URL: 'wss://cardroomgrinders.com.br',
    ENVIRONMENT: 'domain'
  }
};

// Função para detectar ambiente atual
const getCurrentEnvironment = () => {
  // Verificar se há configuração manual via variável de ambiente
  if (process.env.REACT_APP_ENV) {
    return process.env.REACT_APP_ENV;
  }
  
  // Detectar baseado no hostname
  const hostname = window.location.hostname;
  
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    return 'development';
  } else if (hostname === 'cardroomgrinders.com.br' || hostname.includes('cardroomgrinders')) {
    return 'domain';
  } else if (hostname === 'grinders.com.br' || hostname.includes('grinders')) {
    return 'server';
  } else if (hostname === '142.93.206.128') {
    return 'production';
  }
  
  // Fallback para development
  return 'development';
};

// Obter configuração do ambiente atual
const currentEnv = getCurrentEnvironment();
const config = environments[currentEnv] || environments.development;

// Configurações adicionais
const appConfig = {
  ...config,
  
  // Configurações de upload
  UPLOAD: {
    MAX_FILE_SIZE: 1024 * 1024 * 1024, // 1GB
    ALLOWED_VIDEO_FORMATS: ['mp4', 'avi', 'mov', 'wmv', 'flv', 'webm', 'mkv'],
    CHUNK_SIZE: 1024 * 1024 * 5, // 5MB chunks para upload
  },
  
  // Configurações de autenticação
  AUTH: {
    TOKEN_REFRESH_INTERVAL: 5 * 60 * 1000, // 5 minutos
    SESSION_TIMEOUT: 24 * 60 * 60 * 1000, // 24 horas
  },
  
  // Configurações de vídeo
  VIDEO: {
    DEFAULT_CATEGORY: 'preflop',
    SUPPORTED_FORMATS: ['mp4', 'webm', 'ogg'],
    PRELOAD: 'metadata',
  },
  
  // Configurações de UI
  UI: {
    ITEMS_PER_PAGE: 20,
    SEARCH_DEBOUNCE: 300,
    NOTIFICATION_TIMEOUT: 5000,
  },
  
  // URLs de API construídas dinamicamente
  API_ENDPOINTS: {
    // Autenticação
    LOGIN: '/auth/login',
    REGISTER: '/auth/register',
    VERIFY: '/auth/verify',
    LOGOUT: '/auth/logout',
    CHANGE_PASSWORD: '/auth/change-password',
    FORGOT_PASSWORD: '/auth/forgot-password',
    RESET_PASSWORD: '/auth/reset-password',
    VALIDATE_RESET_TOKEN: '/auth/validate-reset-token',
    
    // Classes
    CLASSES: '/classes',
    CLASS_BY_ID: (id) => `/classes/${id}`,
    CLASS_PROGRESS: (id) => `/classes/${id}/progress`,
    CLASS_VIEW: (id) => `/classes/${id}/view`,
    CLASS_VIEWS: (id) => `/classes/${id}/views`,
    CLASSES_HISTORY: '/classes/history',
    UPLOAD_VIDEO: '/classes/upload-video',
    UPLOAD_COMPLETE: '/classes/upload-complete',
    CATEGORIES: '/classes/categories',

    // Usuários
    USERS: '/users',
    USER_BY_ID: (id) => `/users/${id}`,

    // Favoritos
    FAVORITES: '/favorites',
    FAVORITE_BY_ID: (id) => `/favorites/${id}`,
    FAVORITE_CHECK: (id) => `/favorites/${id}/check`,

    // Playlists
    PLAYLISTS: '/playlists',
    PLAYLIST_BY_ID: (id) => `/playlists/${id}`,
    PLAYLIST_ADD_CLASS: (playlistId, classId) => `/playlists/${playlistId}/classes/${classId}`,

    // Analytics
    ANALYTICS_STATS: '/analytics/stats',

    // Instrutores
    INSTRUCTORS: '/instructors',

    // Partições
    PARTICOES: '/particoes',

    // Vídeos
    VIDEO_STREAM: (videoPath, token) => `/videos/${videoPath}?token=${token}`,
  }
};

// Função helper para construir URLs completas
export const buildApiUrl = (endpoint) => {
  return `${appConfig.API_BASE_URL}${endpoint}`;
};

// Função helper para construir URL de vídeo
export const buildVideoUrl = (videoPath, token) => {
  return buildApiUrl(appConfig.API_ENDPOINTS.VIDEO_STREAM(videoPath, token));
};

// Função para debug - mostrar configuração atual
export const debugConfig = () => {
  console.log('🔧 Configuração atual:', {
    environment: currentEnv,
    config: appConfig,
    hostname: window.location.hostname,
    isDevelopment,
    isProduction
  });
};

// Log da configuração em desenvolvimento
if (isDevelopment) {
  console.log('🔧 Poker Academy - Configuração carregada:', currentEnv);
  console.log('📡 API Base URL:', appConfig.API_BASE_URL);
}

export default appConfig;
