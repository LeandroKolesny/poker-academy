// Configuração para domínio personalizado - cardroomgrinders.com.br
const domainConfig = {
  // URLs Base
  API_BASE_URL: 'https://cardroomgrinders.com.br/api',
  FRONTEND_URL: 'https://cardroomgrinders.com.br',
  WEBSOCKET_URL: 'wss://cardroomgrinders.com.br/ws',
  
  // Upload Configuration
  MAX_FILE_SIZE: 1024 * 1024 * 1024, // 1GB para produção
  ALLOWED_VIDEO_FORMATS: ['mp4', 'avi', 'mov', 'wmv', 'flv', 'webm', 'mkv'],
  CHUNK_SIZE: 5 * 1024 * 1024, // 5MB chunks para produção
  
  // Authentication
  TOKEN_REFRESH_INTERVAL: 5 * 60 * 1000, // 5 minutos
  SESSION_TIMEOUT: 24 * 60 * 60 * 1000, // 24 horas
  
  // UI Configuration
  ITEMS_PER_PAGE: 20,
  SEARCH_DEBOUNCE: 300,
  NOTIFICATION_TIMEOUT: 5000,
  
  // API Endpoints
  API_ENDPOINTS: {
    // Authentication
    LOGIN: '/auth/login',
    REGISTER: '/auth/register',
    VERIFY_TOKEN: '/auth/verify-token',
    CHANGE_PASSWORD: '/auth/change-password',
    
    // Classes
    CLASSES: '/classes',
    CLASS_BY_ID: '/classes',
    UPLOAD_VIDEO: '/classes/upload-video',
    UPLOAD_COMPLETE: '/classes/upload-complete',
    UPLOAD_PROGRESS: '/classes/upload-progress',
    
    // Users
    USERS: '/users',
    USER_BY_ID: '/users',
    
    // Favorites
    FAVORITES: '/favorites',
    ADD_FAVORITE: '/favorites',
    REMOVE_FAVORITE: '/favorites',
    
    // Playlists
    PLAYLISTS: '/playlists',
    PLAYLIST_BY_ID: '/playlists',
    
    // Analytics
    ANALYTICS: '/analytics',
    USER_PROGRESS: '/analytics/user-progress',
    
    // Instructors
    INSTRUCTORS: '/instructors',
    
    // Partições
    PARTICOES: '/particoes'
  },
  
  // Environment
  ENVIRONMENT: 'domain',
  DEBUG: false,
  
  // CORS
  CORS_ORIGINS: [
    'https://cardroomgrinders.com.br',
    'https://www.cardroomgrinders.com.br'
  ],
  
  // SSL/HTTPS
  FORCE_HTTPS: true,
  SECURE_COOKIES: true,
  
  // CDN/Static Files
  STATIC_URL: 'https://cardroomgrinders.com.br/static',
  MEDIA_URL: 'https://cardroomgrinders.com.br/media',
  
  // Database (para referência do backend)
  DATABASE_CONFIG: {
    HOST: 'localhost',
    PORT: 3306,
    NAME: 'poker_academy',
    // Credenciais devem estar no .env do servidor
  }
};

export default domainConfig;
