// src/components/admin/InstructorManagement.js
import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlus, faEdit, faTrash, faSpinner, faChalkboardTeacher } from '@fortawesome/free-solid-svg-icons';
import { instructorService } from '../../services/api';

const InstructorManagement = () => {
  const [instructors, setInstructors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [formError, setFormError] = useState(null);

  const [showForm, setShowForm] = useState(false);
  const [currentInstructor, setCurrentInstructor] = useState(null); // Para identificar se é edição
  const [searchTerm, setSearchTerm] = useState('');

  // Estado inicial do formulário
  const initialFormData = {
    name: '', // Nome real do instrutor
    username: '', // Nome de usuário único
    email: '',
    password: '',
  };
  const [formData, setFormData] = useState(initialFormData);

  // Buscar instrutores da API
  const fetchInstructors = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await instructorService.getAll();
      const data = response.data || response; // Compatibilidade com nova estrutura
      console.log("📊 Dados dos instrutores:", data); // Debug
      setInstructors(Array.isArray(data) ? data : []);
    } catch (e) {
      console.error("Erro ao buscar instrutores:", e);
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInstructors();
  }, []);

  // Função para formatar data para exibição
  const formatDateForDisplay = (dateString) => {
    if (!dateString) return 'N/A';
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('pt-BR');
    } catch (error) {
      return 'Data inválida';
    }
  };

  // Filtrar instrutores baseado na busca
  const filteredInstructors = instructors.filter(instructor => {
    const searchLower = searchTerm.toLowerCase();
    return instructor.name.toLowerCase().includes(searchLower) ||
           instructor.username.toLowerCase().includes(searchLower) ||
           instructor.email.toLowerCase().includes(searchLower);
  });

  // Abrir formulário para adicionar novo instrutor
  const handleAddInstructor = () => {
    setCurrentInstructor(null);
    setFormData(initialFormData);
    setShowForm(true);
    setFormError(null);
  };

  // Abrir formulário para editar instrutor existente
  const handleEditInstructor = (instructor) => {
    setCurrentInstructor(instructor);
    setFormData({
      name: instructor.name || '',
      username: instructor.username || '',
      email: instructor.email || '',
      password: '', // Senha não é pré-preenchida por segurança
    });
    setShowForm(true);
    setFormError(null);
  };

  // Salvar instrutor (novo ou editado) via API
  const handleSaveInstructor = async (e) => {
    e.preventDefault();
    setFormError(null);

    console.log("Dados do formulário:", formData); // Debug

    if (!formData.name || !formData.username || !formData.email) {
      setFormError("Nome, Username e Email são obrigatórios.");
      console.log("Validação falhou - campos obrigatórios:", {
        name: !!formData.name,
        username: !!formData.username,
        email: !!formData.email
      });
      return;
    }
    if (!currentInstructor && !formData.password) { // Senha obrigatória apenas para novos instrutores
        setFormError("Senha é obrigatória para novos instrutores.");
        return;
    }

    // Preparar dados para envio
    const instructorData = {
      name: formData.name,
      username: formData.username,
      email: formData.email,
      type: 'admin' // Sempre criar como admin/instrutor
    };

    // Incluir senha apenas se fornecida
    if (formData.password) {
      instructorData.password = formData.password;
    }

    console.log("Dados que serão enviados:", instructorData); // Debug

    try {
      if (currentInstructor && currentInstructor.id) {
        // Editar instrutor existente
        await instructorService.update(currentInstructor.id, instructorData);
      } else {
        // Criar novo instrutor
        await instructorService.create(instructorData);
      }

      fetchInstructors(); // Recarrega a lista de instrutores
      setShowForm(false);
      setCurrentInstructor(null); // Limpa o estado de edição
    } catch (err) {
      console.error("Erro ao salvar instrutor:", err);
      setFormError(err.message);
    }
  };

  // Excluir instrutor via API
  const handleDeleteInstructor = async (id) => {
    if (window.confirm('Tem certeza que deseja excluir este instrutor? Esta ação não pode ser desfeita.')) {
      try {
        await instructorService.delete(id);
        fetchInstructors(); // Recarrega a lista de instrutores
      } catch (err) {
        console.error("Erro ao excluir instrutor:", err);
        setError(err.message);
      }
    }
  };

  if (loading) {
    return (
      <div className="p-6 text-white flex justify-center items-center min-h-[300px]">
        <FontAwesomeIcon icon={faSpinner} spin size="3x" />
        <span className="ml-4 text-xl">Carregando instrutores...</span>
      </div>
    );
  }

  if (error) {
    return <div className="p-6 text-red-500">Erro ao carregar instrutores: {error}. Tente recarregar a página.</div>;
  }

  return (
    <div className="p-4 md:p-6 text-white min-h-screen">
      <div className="flex flex-col md:flex-row md:justify-between md:items-center mb-6 space-y-4 md:space-y-0">
        <h2 className="text-xl md:text-2xl font-semibold text-red-400">Gestão de Instrutores</h2>
        <button
          className="bg-red-400 hover:bg-red-500 text-white font-bold py-3 md:py-2 px-4 rounded transition-colors duration-150 w-full md:w-auto"
          onClick={handleAddInstructor}
        >
          <FontAwesomeIcon icon={faPlus} className="mr-2" /> Novo Instrutor
        </button>
      </div>

      {/* Campo de busca */}
      <div className="mb-6">
        <input
          type="text"
          placeholder="Buscar por nome, username ou email..."
          className="w-full p-3 bg-gray-700 text-white rounded-lg border border-gray-600 focus:border-red-400 focus:outline-none"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      {/* Lista de instrutores */}
      <div className="bg-gray-800 rounded-lg shadow-lg overflow-hidden">
        {filteredInstructors.length === 0 ? (
          <div className="p-8 text-center text-gray-400">
            <FontAwesomeIcon icon={faChalkboardTeacher} size="3x" className="mb-4 opacity-50" />
            <p className="text-lg">Nenhum instrutor encontrado</p>
            <p className="text-sm mt-2">
              {searchTerm ? 'Tente ajustar sua busca' : 'Clique em "Novo Instrutor" para adicionar o primeiro'}
            </p>
          </div>
        ) : (
          <>
            {/* Tabela para Desktop */}
            <div className="hidden md:block overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-700">
                <thead className="bg-gray-700">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Nome</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Username</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Email</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Data Registro</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Último Login</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-300 uppercase tracking-wider">Ações</th>
                  </tr>
                </thead>
                <tbody className="bg-gray-800 divide-y divide-gray-700">
                  {filteredInstructors.map(instructor => (
                    <tr key={instructor.id} className="hover:bg-gray-700 transition-colors duration-150">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-white">{instructor.name}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">@{instructor.username}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">{instructor.email}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-white">{instructor.register_date ? formatDateForDisplay(instructor.register_date) : 'N/A'}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-white">{instructor.last_login ? new Date(instructor.last_login).toLocaleString() : 'Nunca'}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <button
                          className="text-blue-400 hover:text-blue-300 mr-3 transition-colors duration-150"
                          onClick={() => handleEditInstructor(instructor)}
                          title="Editar Instrutor"
                        >
                          <FontAwesomeIcon icon={faEdit} />
                        </button>
                        <button
                          className="text-red-400 hover:text-red-300 transition-colors duration-150"
                          onClick={() => handleDeleteInstructor(instructor.id)}
                          title="Excluir Instrutor"
                        >
                          <FontAwesomeIcon icon={faTrash} />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Cards para Mobile */}
            <div className="md:hidden space-y-4 p-4">
              {filteredInstructors.map(instructor => (
                <div key={instructor.id} className="bg-gray-700 rounded-lg p-4 shadow-lg">
                  <div className="flex justify-between items-start mb-3">
                    <div className="flex-1">
                      <h3 className="text-lg font-semibold text-white mb-1">{instructor.name}</h3>
                      <p className="text-gray-300 text-sm">@{instructor.username}</p>
                    </div>
                    <div className="flex space-x-3">
                      <button
                        className="text-blue-400 hover:text-blue-300 p-2 transition-colors duration-150"
                        onClick={() => handleEditInstructor(instructor)}
                        title="Editar Instrutor"
                      >
                        <FontAwesomeIcon icon={faEdit} className="text-lg" />
                      </button>
                      <button
                        className="text-red-400 hover:text-red-300 p-2 transition-colors duration-150"
                        onClick={() => handleDeleteInstructor(instructor.id)}
                        title="Excluir Instrutor"
                      >
                        <FontAwesomeIcon icon={faTrash} className="text-lg" />
                      </button>
                    </div>
                  </div>
                  <div className="space-y-2 text-sm">
                    <p className="text-gray-300">
                      <span className="font-medium text-white">Email:</span> {instructor.email}
                    </p>
                    <p className="text-gray-300">
                      <span className="font-medium text-white">Registro:</span> {instructor.register_date ? formatDateForDisplay(instructor.register_date) : 'N/A'}
                    </p>
                    <p className="text-gray-300">
                      <span className="font-medium text-white">Último Login:</span> {instructor.last_login ? new Date(instructor.last_login).toLocaleString() : 'Nunca'}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </>
        )}
      </div>

      {/* Modal do formulário */}
      {showForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-gray-800 rounded-lg shadow-xl w-full max-w-md max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <h3 className="text-lg font-semibold text-white mb-4">
                {currentInstructor ? 'Editar Instrutor' : 'Novo Instrutor'}
              </h3>

              {formError && (
                <div className="mb-4 p-3 bg-red-900 border border-red-700 rounded text-red-200 text-sm">
                  {formError}
                </div>
              )}

              <form onSubmit={handleSaveInstructor} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Nome Completo *
                  </label>
                  <input
                    type="text"
                    className="w-full p-3 bg-gray-700 text-white rounded border border-gray-600 focus:border-red-400 focus:outline-none"
                    value={formData.name}
                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                    placeholder="Nome completo do instrutor"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Username *
                  </label>
                  <input
                    type="text"
                    className="w-full p-3 bg-gray-700 text-white rounded border border-gray-600 focus:border-red-400 focus:outline-none"
                    value={formData.username}
                    onChange={(e) => setFormData({...formData, username: e.target.value})}
                    placeholder="Nome de usuário único"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Email *
                  </label>
                  <input
                    type="email"
                    className="w-full p-3 bg-gray-700 text-white rounded border border-gray-600 focus:border-red-400 focus:outline-none"
                    value={formData.email}
                    onChange={(e) => setFormData({...formData, email: e.target.value})}
                    placeholder="email@exemplo.com"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Senha {!currentInstructor && '*'}
                  </label>
                  <input
                    type="password"
                    className="w-full p-3 bg-gray-700 text-white rounded border border-gray-600 focus:border-red-400 focus:outline-none"
                    value={formData.password}
                    onChange={(e) => setFormData({...formData, password: e.target.value})}
                    placeholder={currentInstructor ? "Deixe em branco para manter a senha atual" : "Senha do instrutor"}
                    required={!currentInstructor}
                  />
                  {currentInstructor && (
                    <p className="text-xs text-gray-400 mt-1">
                      Deixe em branco para manter a senha atual
                    </p>
                  )}
                </div>

                <div className="flex flex-col md:flex-row md:justify-end pt-4 border-t border-gray-700 space-y-3 md:space-y-0 md:space-x-2">
                  <button
                    type="button"
                    className="w-full md:w-auto bg-gray-600 hover:bg-gray-500 text-gray-200 font-bold py-3 md:py-2 px-4 rounded transition-colors duration-150 order-2 md:order-1"
                    onClick={() => { setShowForm(false); setCurrentInstructor(null); }}
                  >
                    Cancelar
                  </button>
                  <button
                    type="submit"
                    className="w-full md:w-auto bg-red-400 hover:bg-red-500 text-white font-bold py-3 md:py-2 px-4 rounded transition-colors duration-150 order-1 md:order-2"
                  >
                    {currentInstructor ? 'Salvar Alterações' : 'Adicionar Instrutor'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default InstructorManagement;
