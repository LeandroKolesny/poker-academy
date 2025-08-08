// src/components/auth/ForgotPassword.js
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSpinner, faEnvelope, faArrowLeft, faCheckCircle } from '@fortawesome/free-solid-svg-icons';
import DojoLogo from '../shared/DojoLogo';
import { apiRequest } from '../../services/api';

const ForgotPassword = () => {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await apiRequest('/auth/forgot-password', {
        method: 'POST',
        body: JSON.stringify({ email }),
      });

      if (response.success) {
        setSuccess(true);
      } else {
        setError(response.message || 'Erro ao enviar email de recuperação');
      }
    } catch (err) {
      console.error('Erro ao solicitar reset de senha:', err);
      setError('Erro ao conectar com o servidor. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 flex items-center justify-center p-4">
        <div className="bg-gray-600 p-8 rounded-modern-lg shadow-modern-xl w-full max-w-md border border-gray-500 backdrop-blur-sm">
          {/* Header com Logo e Título */}
          <div className="flex items-center justify-center mb-8 space-x-4">
            <DojoLogo size={56} className="opacity-95" />
            <div className="text-center">
              <h2 className="text-3xl font-bold text-white">Grinders</h2>
              <p className="text-gray-300 text-sm mt-1">Email Enviado</p>
            </div>
          </div>

          {/* Sucesso */}
          <div className="text-center">
            <div className="mb-6">
              <FontAwesomeIcon 
                icon={faCheckCircle} 
                className="text-green-500 text-6xl mb-4" 
              />
            </div>
            
            <h3 className="text-xl font-bold text-white mb-4">
              Email Enviado com Sucesso!
            </h3>
            
            <p className="text-gray-300 mb-6 leading-relaxed">
              Enviamos um link de recuperação para <strong className="text-white">{email}</strong>.
              <br /><br />
              Verifique sua caixa de entrada e clique no link para redefinir sua senha.
              <br /><br />
              <span className="text-yellow-400">⏰ O link expira em 1 hora.</span>
            </p>

            <div className="space-y-4">
              <Link
                to="/login"
                className="w-full bg-primary-red text-white py-3 rounded-modern hover:bg-secondary-red transition-all duration-200 flex items-center justify-center font-medium shadow-modern"
              >
                <FontAwesomeIcon icon={faArrowLeft} className="mr-2" />
                Voltar ao Login
              </Link>
              
              <button
                onClick={() => {
                  setSuccess(false);
                  setEmail('');
                }}
                className="w-full bg-gray-500 text-white py-3 rounded-modern hover:bg-gray-400 transition-all duration-200 font-medium"
              >
                Enviar Novamente
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 flex items-center justify-center p-4">
      <div className="bg-gray-600 p-8 rounded-modern-lg shadow-modern-xl w-full max-w-md border border-gray-500 backdrop-blur-sm">
        {/* Header com Logo e Título */}
        <div className="flex items-center justify-center mb-8 space-x-4">
          <DojoLogo size={56} className="opacity-95" />
          <div className="text-center">
            <h2 className="text-3xl font-bold text-white">Grinders</h2>
            <p className="text-gray-300 text-sm mt-1">Recuperar Senha</p>
          </div>
        </div>

        {/* Descrição */}
        <div className="text-center mb-6">
          <FontAwesomeIcon icon={faEnvelope} className="text-primary-red text-4xl mb-4" />
          <p className="text-gray-300 text-sm leading-relaxed">
            Digite seu email para receber um link de recuperação de senha.
          </p>
        </div>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          {error && (
            <div className="bg-red-500 bg-opacity-20 border border-red-500 text-red-300 px-4 py-3 rounded-modern text-sm">
              {error}
            </div>
          )}

          <div>
            <label htmlFor="email" className="block text-white font-medium mb-2">
              Email
            </label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full bg-gray-500 border border-gray-400 text-white px-4 py-3 rounded-modern focus:ring-2 focus:ring-primary-red focus:border-primary-red transition-all duration-200 placeholder-gray-300"
              placeholder="Digite seu email"
              required
            />
          </div>

          <div className="space-y-4">
            <button
              type="submit"
              className="w-full bg-primary-red text-white py-3 rounded-modern hover:bg-secondary-red transition-all duration-200 flex items-center justify-center font-medium shadow-modern disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={loading}
            >
              {loading ? (
                <>
                  <FontAwesomeIcon icon={faSpinner} spin className="mr-2" />
                  Enviando...
                </>
              ) : (
                <>
                  <FontAwesomeIcon icon={faEnvelope} className="mr-2" />
                  Enviar Link de Recuperação
                </>
              )}
            </button>

            <Link
              to="/login"
              className="w-full bg-gray-500 text-white py-3 rounded-modern hover:bg-gray-400 transition-all duration-200 flex items-center justify-center font-medium"
            >
              <FontAwesomeIcon icon={faArrowLeft} className="mr-2" />
              Voltar ao Login
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ForgotPassword;
