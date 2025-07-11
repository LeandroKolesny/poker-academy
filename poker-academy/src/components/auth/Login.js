// src/components/auth/Login.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSpinner } from '@fortawesome/free-solid-svg-icons';
import DojoLogo from '../shared/DojoLogo';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { login, loading, error } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    const loginResult = await login(username, password);

    if (loginResult && loginResult.success) {
      console.log('Login bem-sucedido, verificando primeiro login...');

      // Verificar se é primeiro login
      if (loginResult.user && loginResult.user.first_login) {
        console.log('Primeiro login detectado, redirecionando para alteração de senha...');
        // Redirecionar para a área do usuário com a aba de alteração de senha
        if (loginResult.user.type === 'admin') {
          navigate('/admin/change-password');
        } else {
          navigate('/student/change-password');
        }
      } else {
        // Redirecionar para área apropriada baseada no tipo de usuário
        console.log('Login normal, redirecionando...');
        setTimeout(() => {
          if (loginResult.user.type === 'admin') {
            navigate('/admin');
          } else {
            navigate('/student');
          }
        }, 100);
      }
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 flex items-center justify-center p-4">
      <div className="bg-gray-600 p-8 rounded-modern-lg shadow-modern-xl w-full max-w-md border border-gray-500 backdrop-blur-sm">
        {/* Header com Logo e Título */}
        <div className="flex items-center justify-center mb-8 space-x-4">
          <DojoLogo size={56} className="opacity-95" />
          <div className="text-center">
            <h2 className="text-3xl font-bold text-white">Grinders</h2>
            <p className="text-gray-300 text-sm mt-1">Bem-vindos de volta</p>
          </div>
        </div>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="username" className="block text-white font-medium mb-2">
              Username/Email
            </label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full bg-gray-500 border border-gray-400 text-white px-4 py-3 rounded-modern focus:ring-2 focus:ring-primary-red focus:border-primary-red transition-all duration-200 placeholder-gray-300"
              placeholder="Digite seu username ou email"
              required
            />
          </div>
          <div>
            <label htmlFor="password" className="block text-white font-medium mb-2">
              Senha
            </label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-gray-500 border border-gray-400 text-white px-4 py-3 rounded-modern focus:ring-2 focus:ring-primary-red focus:border-primary-red transition-all duration-200 placeholder-gray-300"
              placeholder="Digite sua senha"
              required
            />
          </div>

          {error && (
            <div className="bg-red-900/20 border border-red-500/50 text-red-300 px-4 py-3 rounded-modern text-sm">
              {error}
            </div>
          )}

          <div>
            <button
              type="submit"
              className="w-full bg-primary-red text-white py-3 rounded-modern hover:bg-secondary-red transition-all duration-200 flex items-center justify-center font-medium shadow-modern disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={loading}
            >
              {loading ? (
                <>
                  <FontAwesomeIcon icon={faSpinner} spin className="mr-2" />
                  Processando...
                </>
              ) : 'Entrar'}
            </button>
          </div>

          <div className="text-center">
            <a href="#" className="text-gray-400 hover:text-primary-red transition-colors duration-200 text-sm">
              Esqueceu sua senha?
            </a>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;
