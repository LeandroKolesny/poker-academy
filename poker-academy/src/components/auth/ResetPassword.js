// src/components/auth/ResetPassword.js
import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams, Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSpinner, faLock, faEye, faEyeSlash, faCheckCircle, faArrowLeft } from '@fortawesome/free-solid-svg-icons';
import DojoLogo from '../shared/DojoLogo';
import { apiRequest } from '../../services/api';

const ResetPassword = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const token = searchParams.get('token');

  const [formData, setFormData] = useState({
    password: '',
    confirmPassword: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [validatingToken, setValidatingToken] = useState(true);
  const [tokenValid, setTokenValid] = useState(false);

  // Validar token ao carregar a página
  useEffect(() => {
    const validateToken = async () => {
      if (!token) {
        setError('Token de recuperação não encontrado');
        setValidatingToken(false);
        return;
      }

      try {
        const response = await apiRequest(`/api/auth/validate-reset-token?token=${token}`);
        if (response.valid) {
          setTokenValid(true);
        } else {
          setError('Link de recuperação inválido ou expirado');
        }
      } catch (err) {
        setError('Erro ao validar token de recuperação');
      } finally {
        setValidatingToken(false);
      }
    };

    validateToken();
  }, [token]);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    setError(''); // Limpar erro ao digitar
  };

  const validatePasswords = () => {
    if (formData.password.length < 6) {
      setError('A senha deve ter pelo menos 6 caracteres');
      return false;
    }

    if (formData.password !== formData.confirmPassword) {
      setError('As senhas não coincidem');
      return false;
    }

    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validatePasswords()) {
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await apiRequest('/api/auth/reset-password', {
        method: 'POST',
        body: JSON.stringify({
          token,
          password: formData.password
        }),
      });

      if (response.success) {
        setSuccess(true);
        // Redirecionar para login após 3 segundos
        setTimeout(() => {
          navigate('/login');
        }, 3000);
      } else {
        setError(response.message || 'Erro ao redefinir senha');
      }
    } catch (err) {
      console.error('Erro ao redefinir senha:', err);
      setError('Erro ao conectar com o servidor. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  // Loading do token
  if (validatingToken) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 flex items-center justify-center p-4">
        <div className="bg-gray-600 p-8 rounded-modern-lg shadow-modern-xl w-full max-w-md border border-gray-500 backdrop-blur-sm text-center">
          <FontAwesomeIcon icon={faSpinner} spin className="text-primary-red text-4xl mb-4" />
          <p className="text-white">Validando link de recuperação...</p>
        </div>
      </div>
    );
  }

  // Token inválido
  if (!tokenValid) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 flex items-center justify-center p-4">
        <div className="bg-gray-600 p-8 rounded-modern-lg shadow-modern-xl w-full max-w-md border border-gray-500 backdrop-blur-sm text-center">
          <div className="text-red-500 text-6xl mb-4">❌</div>
          <h3 className="text-xl font-bold text-white mb-4">Link Inválido</h3>
          <p className="text-gray-300 mb-6">{error}</p>
          <Link
            to="/forgot-password"
            className="w-full bg-primary-red text-white py-3 rounded-modern hover:bg-secondary-red transition-all duration-200 flex items-center justify-center font-medium shadow-modern"
          >
            Solicitar Novo Link
          </Link>
        </div>
      </div>
    );
  }

  // Sucesso
  if (success) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 flex items-center justify-center p-4">
        <div className="bg-gray-600 p-8 rounded-modern-lg shadow-modern-xl w-full max-w-md border border-gray-500 backdrop-blur-sm text-center">
          <FontAwesomeIcon icon={faCheckCircle} className="text-green-500 text-6xl mb-4" />
          <h3 className="text-xl font-bold text-white mb-4">Senha Redefinida!</h3>
          <p className="text-gray-300 mb-6">
            Sua senha foi alterada com sucesso. Você será redirecionado para o login em alguns segundos.
          </p>
          <Link
            to="/login"
            className="w-full bg-primary-red text-white py-3 rounded-modern hover:bg-secondary-red transition-all duration-200 flex items-center justify-center font-medium shadow-modern"
          >
            <FontAwesomeIcon icon={faArrowLeft} className="mr-2" />
            Ir para Login
          </Link>
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
            <p className="text-gray-300 text-sm mt-1">Nova Senha</p>
          </div>
        </div>

        {/* Descrição */}
        <div className="text-center mb-6">
          <FontAwesomeIcon icon={faLock} className="text-primary-red text-4xl mb-4" />
          <p className="text-gray-300 text-sm leading-relaxed">
            Digite sua nova senha. Certifique-se de que seja segura e fácil de lembrar.
          </p>
        </div>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          {error && (
            <div className="bg-red-500 bg-opacity-20 border border-red-500 text-red-300 px-4 py-3 rounded-modern text-sm">
              {error}
            </div>
          )}

          <div>
            <label htmlFor="password" className="block text-white font-medium mb-2">
              Nova Senha
            </label>
            <div className="relative">
              <input
                type={showPassword ? 'text' : 'password'}
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                className="w-full bg-gray-500 border border-gray-400 text-white px-4 py-3 pr-12 rounded-modern focus:ring-2 focus:ring-primary-red focus:border-primary-red transition-all duration-200 placeholder-gray-300"
                placeholder="Digite sua nova senha"
                required
                minLength={6}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-white transition-colors"
              >
                <FontAwesomeIcon icon={showPassword ? faEyeSlash : faEye} />
              </button>
            </div>
          </div>

          <div>
            <label htmlFor="confirmPassword" className="block text-white font-medium mb-2">
              Confirmar Nova Senha
            </label>
            <div className="relative">
              <input
                type={showConfirmPassword ? 'text' : 'password'}
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                className="w-full bg-gray-500 border border-gray-400 text-white px-4 py-3 pr-12 rounded-modern focus:ring-2 focus:ring-primary-red focus:border-primary-red transition-all duration-200 placeholder-gray-300"
                placeholder="Confirme sua nova senha"
                required
                minLength={6}
              />
              <button
                type="button"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-white transition-colors"
              >
                <FontAwesomeIcon icon={showConfirmPassword ? faEyeSlash : faEye} />
              </button>
            </div>
          </div>

          {/* Indicador de força da senha */}
          {formData.password && (
            <div className="text-sm">
              <div className="flex items-center space-x-2">
                <span className="text-gray-300">Força da senha:</span>
                <div className={`px-2 py-1 rounded text-xs ${
                  formData.password.length >= 8 ? 'bg-green-500 text-white' :
                  formData.password.length >= 6 ? 'bg-yellow-500 text-black' :
                  'bg-red-500 text-white'
                }`}>
                  {formData.password.length >= 8 ? 'Forte' :
                   formData.password.length >= 6 ? 'Média' : 'Fraca'}
                </div>
              </div>
            </div>
          )}

          <div className="space-y-4">
            <button
              type="submit"
              className="w-full bg-primary-red text-white py-3 rounded-modern hover:bg-secondary-red transition-all duration-200 flex items-center justify-center font-medium shadow-modern disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={loading}
            >
              {loading ? (
                <>
                  <FontAwesomeIcon icon={faSpinner} spin className="mr-2" />
                  Redefinindo...
                </>
              ) : (
                <>
                  <FontAwesomeIcon icon={faLock} className="mr-2" />
                  Redefinir Senha
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

export default ResetPassword;
