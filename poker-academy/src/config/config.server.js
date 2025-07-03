// src/config/config.server.js
// Configuração específica para servidor de produção

const serverConfig = {
  API_BASE_URL: 'http://142.93.206.128:5000',
  FRONTEND_URL: 'http://142.93.206.128',
  WEBSOCKET_URL: 'ws://142.93.206.128:5000',
  ENVIRONMENT: 'production',
  
  // Configurações específicas para produção
  DEBUG: false,
  ENABLE_LOGS: false,
  MOCK_DATA: false,
  
  // Configurações de produção para upload
  UPLOAD: {
    MAX_FILE_SIZE: 1024 * 1024 * 1024, // 1GB para produção
    ALLOWED_VIDEO_FORMATS: ['mp4', 'avi', 'mov', 'wmv', 'flv', 'webm', 'mkv'],
    CHUNK_SIZE: 1024 * 1024 * 5, // 5MB chunks para produção
  },
  
  // Configurações de autenticação para produção
  AUTH: {
    TOKEN_REFRESH_INTERVAL: 5 * 60 * 1000, // 5 minutos
    SESSION_TIMEOUT: 24 * 60 * 60 * 1000, // 24 horas
  },
  
  // Configurações de UI para produção
  UI: {
    ITEMS_PER_PAGE: 20,
    SEARCH_DEBOUNCE: 300,
    NOTIFICATION_TIMEOUT: 5000,
    SHOW_DEBUG_INFO: false,
  }
};

export default serverConfig;
