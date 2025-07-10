// src/services/api.js
import appConfig from '../config/config';

// Variável global para armazenar o token temporariamente
let currentToken = null;

// Função para definir o token
export const setApiToken = (token) => {
  currentToken = token;
  // Usar localStorage para consistência com AuthContext
  if (token) {
    localStorage.setItem('token', token);
  } else {
    localStorage.removeItem('token');
  }
};

// Função para obter o token
export const getToken = () => {
  // Se não temos token na memória, tentar recuperar do localStorage
  if (!currentToken) {
    currentToken = localStorage.getItem('token');
  }
  return currentToken;
};

// Função para fazer requisições autenticadas
const apiRequest = async (endpoint, options = {}) => {
  const token = getToken();
  const url = `${appConfig.API_BASE_URL}${endpoint}`;

  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options.headers,
    },
    ...options,
  };

  try {
    const response = await fetch(url, config);

    // Se token expirou, tentar renovar automaticamente
    if (response.status === 401 && token) {
      console.log('🔄 Token expirado, tentando renovar...');

      // Verificar se o token realmente expirou
      const verifyResponse = await fetch(`${appConfig.API_BASE_URL}${appConfig.API_ENDPOINTS.VERIFY}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (verifyResponse.status === 401) {
        console.log('❌ Token inválido, redirecionando para login...');
        // Limpar token inválido
        setApiToken(null);
        // Redirecionar para login
        window.location.href = '/login';
        throw new Error('Sessão expirada. Faça login novamente.');
      }
    }

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Erro na requisição');
    }

    return data;
  } catch (error) {
    console.error('Erro na API:', error);
    throw error;
  }
};

// Serviços de Classes
export const classService = {
  // Listar todas as aulas
  getAll: () => apiRequest(appConfig.API_ENDPOINTS.CLASSES),

  // Obter detalhes de uma aula
  getById: (id) => apiRequest(appConfig.API_ENDPOINTS.CLASS_BY_ID(id)),

  // Criar nova aula (admin)
  create: (classData) => apiRequest(appConfig.API_ENDPOINTS.CLASSES, {
    method: 'POST',
    body: JSON.stringify(classData),
  }),

  // Atualizar aula (admin)
  update: (id, classData) => apiRequest(appConfig.API_ENDPOINTS.CLASS_BY_ID(id), {
    method: 'PUT',
    body: JSON.stringify(classData),
  }),

  // Deletar aula (admin)
  delete: (id) => apiRequest(appConfig.API_ENDPOINTS.CLASS_BY_ID(id), {
    method: 'DELETE',
  }),
  
  // Obter progresso da aula
  getProgress: (id) => apiRequest(appConfig.API_ENDPOINTS.CLASS_PROGRESS(id)),

  // Atualizar progresso da aula
  updateProgress: (id, progressData) => apiRequest(appConfig.API_ENDPOINTS.CLASS_PROGRESS(id), {
    method: 'POST',
    body: JSON.stringify(progressData),
  }),

  // Registrar visualização da aula
  registerView: (id) => apiRequest(appConfig.API_ENDPOINTS.CLASS_VIEW(id), {
    method: 'POST',
  }),

  // Obter estatísticas de visualizações (admin)
  getViewStats: (id) => apiRequest(appConfig.API_ENDPOINTS.CLASS_VIEWS(id)),

  // Obter histórico de aulas assistidas
  getHistory: () => apiRequest(appConfig.API_ENDPOINTS.CLASSES_HISTORY),

  // Obter lista de instrutores (admins)
  getInstructors: () => apiRequest(appConfig.API_ENDPOINTS.INSTRUCTORS),

  // Obter categorias disponíveis
  getCategories: () => apiRequest(appConfig.API_ENDPOINTS.CATEGORIES),
};

// Serviços de Analytics
export const analyticsService = {
  // Obter estatísticas do painel (admin)
  getStats: () => apiRequest(appConfig.API_ENDPOINTS.ANALYTICS_STATS),
};

// Serviços de Usuários
export const userService = {
  // Listar todos os usuários (admin)
  getAll: () => apiRequest(appConfig.API_ENDPOINTS.USERS),

  // Criar novo usuário (admin)
  create: (userData) => apiRequest(appConfig.API_ENDPOINTS.USERS, {
    method: 'POST',
    body: JSON.stringify(userData),
  }),

  // Atualizar usuário (admin)
  update: (id, userData) => apiRequest(appConfig.API_ENDPOINTS.USER_BY_ID(id), {
    method: 'PUT',
    body: JSON.stringify(userData),
  }),

  // Deletar usuário (admin)
  delete: (id) => apiRequest(appConfig.API_ENDPOINTS.USER_BY_ID(id), {
    method: 'DELETE',
  }),
};

// Serviços de Favoritos
export const favoritesService = {
  // Listar favoritos do usuário
  getAll: () => apiRequest(appConfig.API_ENDPOINTS.FAVORITES),

  // Adicionar aos favoritos
  add: (classId) => apiRequest(appConfig.API_ENDPOINTS.FAVORITE_BY_ID(classId), {
    method: 'POST',
  }),

  // Remover dos favoritos
  remove: (classId) => apiRequest(appConfig.API_ENDPOINTS.FAVORITE_BY_ID(classId), {
    method: 'DELETE',
  }),

  // Verificar se está nos favoritos
  check: (classId) => apiRequest(appConfig.API_ENDPOINTS.FAVORITE_CHECK(classId)),
};

// Serviços de Playlists
export const playlistService = {
  // Listar playlists do usuário
  getAll: () => apiRequest(appConfig.API_ENDPOINTS.PLAYLISTS),

  // Obter detalhes de uma playlist
  getById: (id) => apiRequest(appConfig.API_ENDPOINTS.PLAYLIST_BY_ID(id)),

  // Criar nova playlist
  create: (playlistData) => apiRequest(appConfig.API_ENDPOINTS.PLAYLISTS, {
    method: 'POST',
    body: JSON.stringify(playlistData),
  }),

  // Deletar playlist
  delete: (id) => apiRequest(appConfig.API_ENDPOINTS.PLAYLIST_BY_ID(id), {
    method: 'DELETE',
  }),

  // Adicionar aula à playlist
  addClass: (playlistId, classId) => apiRequest(appConfig.API_ENDPOINTS.PLAYLIST_ADD_CLASS(playlistId, classId), {
    method: 'POST',
  }),

  // Remover aula da playlist
  removeClass: (playlistId, classId) => apiRequest(appConfig.API_ENDPOINTS.PLAYLIST_ADD_CLASS(playlistId, classId), {
    method: 'DELETE',
  }),
};

// Serviços de Autenticação
export const authService = {
  // Login
  login: (email, password) => apiRequest(appConfig.API_ENDPOINTS.LOGIN, {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  }),

  // Registro
  register: (userData) => apiRequest(appConfig.API_ENDPOINTS.REGISTER, {
    method: 'POST',
    body: JSON.stringify(userData),
  }),

  // Verificar token
  verify: () => apiRequest(appConfig.API_ENDPOINTS.VERIFY),

  // Logout
  logout: () => apiRequest(appConfig.API_ENDPOINTS.LOGOUT, {
    method: 'POST',
  }),

  // Alterar senha
  changePassword: (currentPassword, newPassword) => apiRequest(appConfig.API_ENDPOINTS.CHANGE_PASSWORD, {
    method: 'POST',
    body: JSON.stringify({
      current_password: currentPassword,
      new_password: newPassword
    }),
  }),
};

export default {
  classService,
  userService,
  favoritesService,
  playlistService,
  authService,
  analyticsService,
};
