// src/config/config.local.js
// Configuração específica para desenvolvimento local

const localConfig = {
  API_BASE_URL: 'http://localhost:5000',
  FRONTEND_URL: 'http://localhost:3000',
  WEBSOCKET_URL: 'ws://localhost:5000',
  ENVIRONMENT: 'development',
  
  // Configurações específicas para desenvolvimento
  DEBUG: true,
  ENABLE_LOGS: true,
  MOCK_DATA: false,
  
  // Configurações de desenvolvimento para upload
  UPLOAD: {
    MAX_FILE_SIZE: 500 * 1024 * 1024, // 500MB para desenvolvimento
    ALLOWED_VIDEO_FORMATS: ['mp4', 'avi', 'mov', 'wmv', 'flv', 'webm', 'mkv'],
    CHUNK_SIZE: 1024 * 1024 * 2, // 2MB chunks para desenvolvimento
  },
  
  // Configurações de autenticação para desenvolvimento
  AUTH: {
    TOKEN_REFRESH_INTERVAL: 10 * 60 * 1000, // 10 minutos (mais tempo para debug)
    SESSION_TIMEOUT: 8 * 60 * 60 * 1000, // 8 horas
  },
  
  // Configurações de UI para desenvolvimento
  UI: {
    ITEMS_PER_PAGE: 10, // Menos itens para facilitar testes
    SEARCH_DEBOUNCE: 500, // Mais tempo para debug
    NOTIFICATION_TIMEOUT: 10000, // Notificações mais longas
    SHOW_DEBUG_INFO: true,
  }
};

export default localConfig;
