// src/services/api.js
const API_BASE_URL = 'http://localhost:5000';

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
  const url = `${API_BASE_URL}${endpoint}`;

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
      const verifyResponse = await fetch(`${API_BASE_URL}/api/auth/verify`, {
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
  getAll: () => apiRequest('/api/classes'),
  
  // Obter detalhes de uma aula
  getById: (id) => apiRequest(`/api/classes/${id}`),
  
  // Criar nova aula (admin)
  create: (classData) => apiRequest('/api/classes', {
    method: 'POST',
    body: JSON.stringify(classData),
  }),
  
  // Atualizar aula (admin)
  update: (id, classData) => apiRequest(`/api/classes/${id}`, {
    method: 'PUT',
    body: JSON.stringify(classData),
  }),
  
  // Deletar aula (admin)
  delete: (id) => apiRequest(`/api/classes/${id}`, {
    method: 'DELETE',
  }),
  
  // Obter progresso da aula
  getProgress: (id) => apiRequest(`/api/classes/${id}/progress`),

  // Atualizar progresso da aula
  updateProgress: (id, progressData) => apiRequest(`/api/classes/${id}/progress`, {
    method: 'POST',
    body: JSON.stringify(progressData),
  }),

  // Registrar visualização da aula
  registerView: (id) => apiRequest(`/api/classes/${id}/view`, {
    method: 'POST',
  }),

  // Obter estatísticas de visualizações (admin)
  getViewStats: (id) => apiRequest(`/api/classes/${id}/views`),

  // Obter histórico de aulas assistidas
  getHistory: () => apiRequest('/api/classes/history'),

  // Obter lista de instrutores (admins)
  getInstructors: () => apiRequest('/api/instructors'),
};

// Serviços de Analytics
export const analyticsService = {
  // Obter estatísticas do painel (admin)
  getStats: () => apiRequest('/api/analytics/stats'),
};

// Serviços de Usuários
export const userService = {
  // Listar todos os usuários (admin)
  getAll: () => apiRequest('/api/users'),
  
  // Criar novo usuário (admin)
  create: (userData) => apiRequest('/api/users', {
    method: 'POST',
    body: JSON.stringify(userData),
  }),
  
  // Atualizar usuário (admin)
  update: (id, userData) => apiRequest(`/api/users/${id}`, {
    method: 'PUT',
    body: JSON.stringify(userData),
  }),
  
  // Deletar usuário (admin)
  delete: (id) => apiRequest(`/api/users/${id}`, {
    method: 'DELETE',
  }),
};

// Serviços de Favoritos
export const favoritesService = {
  // Listar favoritos do usuário
  getAll: () => apiRequest('/api/favorites'),
  
  // Adicionar aos favoritos
  add: (classId) => apiRequest(`/api/favorites/${classId}`, {
    method: 'POST',
  }),
  
  // Remover dos favoritos
  remove: (classId) => apiRequest(`/api/favorites/${classId}`, {
    method: 'DELETE',
  }),
  
  // Verificar se está nos favoritos
  check: (classId) => apiRequest(`/api/favorites/${classId}/check`),
};

// Serviços de Playlists
export const playlistService = {
  // Listar playlists do usuário
  getAll: () => apiRequest('/api/playlists'),
  
  // Obter detalhes de uma playlist
  getById: (id) => apiRequest(`/api/playlists/${id}`),
  
  // Criar nova playlist
  create: (playlistData) => apiRequest('/api/playlists', {
    method: 'POST',
    body: JSON.stringify(playlistData),
  }),
  
  // Deletar playlist
  delete: (id) => apiRequest(`/api/playlists/${id}`, {
    method: 'DELETE',
  }),
  
  // Adicionar aula à playlist
  addClass: (playlistId, classId) => apiRequest(`/api/playlists/${playlistId}/classes/${classId}`, {
    method: 'POST',
  }),
  
  // Remover aula da playlist
  removeClass: (playlistId, classId) => apiRequest(`/api/playlists/${playlistId}/classes/${classId}`, {
    method: 'DELETE',
  }),
};

// Serviços de Autenticação
export const authService = {
  // Login
  login: (email, password) => apiRequest('/api/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  }),
  
  // Registro
  register: (userData) => apiRequest('/api/auth/register', {
    method: 'POST',
    body: JSON.stringify(userData),
  }),
  
  // Verificar token
  verify: () => apiRequest('/api/auth/verify'),
  
  // Logout
  logout: () => apiRequest('/api/auth/logout', {
    method: 'POST',
  }),

  // Alterar senha
  changePassword: (currentPassword, newPassword) => apiRequest('/api/auth/change-password', {
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
