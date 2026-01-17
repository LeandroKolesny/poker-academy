// src/components/auth/ChangePassword.js
import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEye, faEyeSlash, faSpinner, faCheck, faKey } from '@fortawesome/free-solid-svg-icons';
import { useAuth } from '../../context/AuthContext';
import PageHeader from '../shared/PageHeader';
import api from '../../services/api';

const ChangePassword = () => {
  const [formData, setFormData] = useState({
    current_password: '',
    new_password: '',
    confirm_password: ''
  });
  const [showPasswords, setShowPasswords] = useState({
    current: false,
    new: false,
    confirm: false
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [validations, setValidations] = useState({
    length: false,
    match: false
  });

  const { user } = useAuth();

  // Validar senha em tempo real
  const validatePassword = (password, confirmPassword) => {
    setValidations({
      length: password.length >= 6,
      match: password === confirmPassword && password.length > 0
    });
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    // Validar em tempo real
    if (name === 'new_password' || name === 'confirm_password') {
      const newPassword = name === 'new_password' ? value : formData.new_password;
      const confirmPassword = name === 'confirm_password' ? value : formData.confirm_password;
      validatePassword(newPassword, confirmPassword);
    }

    // Limpar mensagens ao digitar
    if (error) setError('');
    if (success) setSuccess(false);
  };

  const togglePasswordVisibility = (field) => {
    setShowPasswords(prev => ({
      ...prev,
      [field]: !prev[field]
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validações
    if (!formData.current_password || !formData.new_password || !formData.confirm_password) {
      setError('Todos os campos são obrigatórios');
      return;
    }

    if (formData.new_password.length < 6) {
      setError('A nova senha deve ter pelo menos 6 caracteres');
      return;
    }

    if (formData.new_password !== formData.confirm_password) {
      setError('As senhas não coincidem');
      return;
    }

    if (formData.current_password === formData.new_password) {
      setError('A nova senha deve ser diferente da senha atual');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await api.put('/api/auth/change-password', {
        current_password: formData.current_password,
        new_password: formData.new_password
      });

      if (response.status === 200) {
        setSuccess(true);
        setFormData({
          current_password: '',
          new_password: '',
          confirm_password: ''
        });
        setValidations({ length: false, match: false });
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Erro ao conectar com o servidor');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <PageHeader 
        title="Alterar Senha" 
        subtitle="Mantenha sua conta segura atualizando sua senha regularmente"
        icon={faKey}
      />

      <div className="max-w-md mx-auto">
        <div className="bg-gray-600 p-8 rounded-modern-lg shadow-modern-xl border border-gray-500">
          {/* Informações do usuário */}
          <div className="mb-6 p-4 bg-gray-700 rounded-modern border border-gray-500">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-primary-red rounded-full flex items-center justify-center">
                <span className="text-white font-bold text-lg">
                  {user?.name?.charAt(0).toUpperCase()}
                </span>
              </div>
              <div>
                <p className="text-white font-medium">{user?.name}</p>
                <p className="text-gray-300 text-sm">{user?.email}</p>
              </div>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Senha Atual */}
            <div>
              <label className="block text-white font-medium mb-2">
                Senha Atual
              </label>
              <div className="relative">
                <input
                  type={showPasswords.current ? 'text' : 'password'}
                  name="current_password"
                  value={formData.current_password}
                  onChange={handleInputChange}
                  className="w-full bg-gray-500 border border-gray-400 text-white px-4 py-3 pr-12 rounded-modern focus:ring-2 focus:ring-primary-red focus:border-primary-red transition-all duration-200"
                  placeholder="Digite sua senha atual"
                  required
                />
                <button
                  type="button"
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-300 hover:text-white"
                  onClick={() => togglePasswordVisibility('current')}
                >
                  <FontAwesomeIcon icon={showPasswords.current ? faEyeSlash : faEye} />
                </button>
              </div>
            </div>

            {/* Nova Senha */}
            <div>
              <label className="block text-white font-medium mb-2">
                Nova Senha
              </label>
              <div className="relative">
                <input
                  type={showPasswords.new ? 'text' : 'password'}
                  name="new_password"
                  value={formData.new_password}
                  onChange={handleInputChange}
                  className="w-full bg-gray-500 border border-gray-400 text-white px-4 py-3 pr-12 rounded-modern focus:ring-2 focus:ring-primary-red focus:border-primary-red transition-all duration-200"
                  placeholder="Digite sua nova senha"
                  required
                />
                <button
                  type="button"
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-300 hover:text-white"
                  onClick={() => togglePasswordVisibility('new')}
                >
                  <FontAwesomeIcon icon={showPasswords.new ? faEyeSlash : faEye} />
                </button>
              </div>
            </div>

            {/* Confirmar Nova Senha */}
            <div>
              <label className="block text-white font-medium mb-2">
                Confirmar Nova Senha
              </label>
              <div className="relative">
                <input
                  type={showPasswords.confirm ? 'text' : 'password'}
                  name="confirm_password"
                  value={formData.confirm_password}
                  onChange={handleInputChange}
                  className="w-full bg-gray-500 border border-gray-400 text-white px-4 py-3 pr-12 rounded-modern focus:ring-2 focus:ring-primary-red focus:border-primary-red transition-all duration-200"
                  placeholder="Confirme sua nova senha"
                  required
                />
                <button
                  type="button"
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-300 hover:text-white"
                  onClick={() => togglePasswordVisibility('confirm')}
                >
                  <FontAwesomeIcon icon={showPasswords.confirm ? faEyeSlash : faEye} />
                </button>
              </div>
            </div>

            {/* Validações visuais */}
            {formData.new_password && (
              <div className="space-y-2">
                <div className={`flex items-center space-x-2 text-sm ${validations.length ? 'text-green-400' : 'text-gray-400'}`}>
                  <FontAwesomeIcon icon={faCheck} className={validations.length ? 'opacity-100' : 'opacity-30'} />
                  <span>Pelo menos 6 caracteres</span>
                </div>
                <div className={`flex items-center space-x-2 text-sm ${validations.match ? 'text-green-400' : 'text-gray-400'}`}>
                  <FontAwesomeIcon icon={faCheck} className={validations.match ? 'opacity-100' : 'opacity-30'} />
                  <span>Senhas coincidem</span>
                </div>
              </div>
            )}

            {/* Mensagens */}
            {error && (
              <div className="bg-red-900/20 border border-red-500/50 text-red-300 px-4 py-3 rounded-modern text-sm">
                {error}
              </div>
            )}

            {success && (
              <div className="bg-green-900/20 border border-green-500/50 text-green-300 px-4 py-3 rounded-modern text-sm">
                Senha alterada com sucesso!
              </div>
            )}

            {/* Botão */}
            <button
              type="submit"
              disabled={loading || !validations.length || !validations.match}
              className="w-full bg-primary-red text-white py-3 rounded-modern hover:bg-secondary-red transition-all duration-200 flex items-center justify-center font-medium shadow-modern disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <>
                  <FontAwesomeIcon icon={faSpinner} spin className="mr-2" />
                  Alterando...
                </>
              ) : (
                'Alterar Senha'
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ChangePassword;
