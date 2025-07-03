// src/context/AuthContext.js
import React, { createContext, useState, useContext, useEffect } from 'react';
import { setApiToken, getToken } from '../services/api';
import appConfig from '../config/config';

// Criando o contexto de autenticação
export const AuthContext = createContext();

// Hook personalizado para usar o contexto de autenticação
export const useAuth = () => useContext(AuthContext);

// Provedor do contexto de autenticação
export const AuthProvider = ({ children }) => {
  // Estado para armazenar informações do usuário e status de autenticação
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true); // Iniciar como true para verificar token salvo
  const [error, setError] = useState('');

  // Verificar se há token salvo ao inicializar
  useEffect(() => {
    const checkSavedToken = async () => {
      const savedToken = getToken();

      if (savedToken) {
        try {
          // Verificar se o token ainda é válido
          const response = await fetch(`${appConfig.API_BASE_URL}${appConfig.API_ENDPOINTS.VERIFY}`, {
            headers: {
              'Authorization': `Bearer ${savedToken}`,
            },
          });

          if (response.ok) {
            const data = await response.json();
            setUser(data.user);
            setIsAuthenticated(true);
            setApiToken(savedToken); // Garantir que está definido
            console.log('✅ Token válido encontrado, usuário autenticado:', data.user);
          } else {
            // Token inválido, limpar
            console.log('❌ Token inválido encontrado, limpando...');
            setApiToken(null);
            setUser(null);
            setIsAuthenticated(false);
          }
        } catch (error) {
          console.error('❌ Erro ao verificar token salvo:', error);
          setApiToken(null);
          setUser(null);
          setIsAuthenticated(false);
        }
      }

      setLoading(false);
    };

    checkSavedToken();
  }, []);

  // Verificar token periodicamente (a cada 5 minutos)
  useEffect(() => {
    if (!isAuthenticated) return;

    const tokenCheckInterval = setInterval(async () => {
      const currentToken = getToken();

      if (currentToken) {
        try {
          const response = await fetch(`${appConfig.API_BASE_URL}${appConfig.API_ENDPOINTS.VERIFY}`, {
            headers: {
              'Authorization': `Bearer ${currentToken}`,
            },
          });

          if (!response.ok) {
            console.log('🔄 Token expirado durante verificação periódica');
            setApiToken(null);
            setUser(null);
            setIsAuthenticated(false);
            setError('Sessão expirada. Faça login novamente.');
          }
        } catch (error) {
          console.error('❌ Erro na verificação periódica do token:', error);
        }
      }
    }, 5 * 60 * 1000); // 5 minutos

    return () => clearInterval(tokenCheckInterval);
  }, [isAuthenticated]);



  // Função para realizar login
  const login = async (username, password) => {
    setLoading(true);
    setError('');

    try {
      console.log('🔄 Tentando login para:', username);
      console.log('🌐 URL da API:', `${appConfig.API_BASE_URL}${appConfig.API_ENDPOINTS.LOGIN}`);

      const response = await fetch(`${appConfig.API_BASE_URL}${appConfig.API_ENDPOINTS.LOGIN}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: username, password }), // Enviar como 'email' para compatibilidade
      });

      console.log('📡 Resposta recebida:', response.status, response.statusText);

      const data = await response.json();

      if (response.ok) {
        // Definir o token para uso nas requisições da API
        console.log('Token recebido no login:', data.token);
        setApiToken(data.token);
        console.log('Token definido, verificando:', getToken());
        console.log('Login realizado com sucesso:', data);
        setUser(data.user);
        setIsAuthenticated(true);
        return true;
      } else {
        setError(data.error || 'Erro ao fazer login');
        return false;
      }
    } catch (err) {
      console.error('❌ Erro no login:', err);
      console.error('❌ Tipo do erro:', err.name);
      console.error('❌ Mensagem:', err.message);
      setError(`Erro ao conectar com o servidor: ${err.message}`);
      return false;
    } finally {
      setLoading(false);
    }
  };

  // Função para realizar logout
  const logout = () => {
    // Limpar o token da API
    setApiToken(null);
    setUser(null);
    setIsAuthenticated(false);
  };

  // Função para alterar senha
  const changePassword = async (currentPassword, newPassword) => {
    setLoading(true);
    setError('');

    try {
      const token = getToken();
      if (!token) {
        setError('Token não encontrado');
        return false;
      }

      const response = await fetch(`${appConfig.API_BASE_URL}${appConfig.API_ENDPOINTS.CHANGE_PASSWORD}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          current_password: currentPassword,
          new_password: newPassword
        })
      });

      const data = await response.json();

      if (response.ok) {
        return true;
      } else {
        setError(data.error || 'Erro ao alterar senha');
        return false;
      }
    } catch (err) {
      console.error('❌ Erro ao alterar senha:', err);
      setError(`Erro ao conectar com o servidor: ${err.message}`);
      return false;
    } finally {
      setLoading(false);
    }
  };

  // Valores e funções expostos pelo contexto
  const value = {
    user,
    isAuthenticated,
    loading,
    error,
    setError,
    login,
    logout,
    changePassword
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
