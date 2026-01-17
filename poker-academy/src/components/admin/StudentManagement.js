// src/components/admin/StudentManagement.js
import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlus, faEdit, faTrash, faSpinner, faTimes } from '@fortawesome/free-solid-svg-icons';
import { userService } from '../../services/api';
import appConfig from '../../config/config';

const StudentManagement = () => {
  const [students, setStudents] = useState([]);
  const [particoes, setParticoes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [formError, setFormError] = useState(null);

  const [showForm, setShowForm] = useState(false);
  const [currentStudent, setCurrentStudent] = useState(null); // Para identificar se é edição
  const [searchTerm, setSearchTerm] = useState('');

  // Estado inicial do formulário
  const initialFormData = {
    name: '', // Nome real do usuário
    username: '', // Nome de usuário único
    email: '',
    password: '',
    particao_id: '', // ID da partição selecionada
  };
  const [formData, setFormData] = useState(initialFormData);

  // Buscar alunos da API
  const fetchStudents = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await userService.getAll();
      const data = response.data || response; // Compatibilidade com nova estrutura
      console.log("📊 Dados dos alunos:", data); // Debug
      setStudents(Array.isArray(data) ? data : []);
    } catch (e) {
      console.error("Erro ao buscar alunos:", e);
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  // Buscar partições da API
  const fetchParticoes = async () => {
    try {
      const response = await fetch(`${appConfig.API_BASE_URL}${appConfig.API_ENDPOINTS.PARTICOES}`);
      if (response.ok) {
        const data = await response.json();
        console.log("Partições carregadas:", data); // Debug
        setParticoes(data);

        // Se não há partição selecionada e há partições disponíveis, selecionar a primeira
        if (data.length > 0 && !formData.particao_id) {
          console.log("Selecionando partição padrão:", data[0].id); // Debug
          setFormData(prev => ({ ...prev, particao_id: data[0].id.toString() }));
        }
      } else {
        console.error("Erro ao buscar partições - Status:", response.status);
      }
    } catch (e) {
      console.error("Erro ao buscar partições:", e);
    }
  };

  useEffect(() => {
    fetchStudents();
    fetchParticoes();
  }, []);

  // Filtrar alunos com base no termo de busca
  const filteredStudents = students.filter(student =>
    (student.name && student.name.toLowerCase().includes(searchTerm.toLowerCase())) ||
    (student.username && student.username.toLowerCase().includes(searchTerm.toLowerCase())) ||
    (student.email && student.email.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  // Função para formatar data sem problemas de timezone
  const formatDateForDisplay = (dateString) => {
    if (!dateString) return 'N/A';

    // Se a data está no formato YYYY-MM-DD, criar Date com timezone local
    if (typeof dateString === 'string' && dateString.match(/^\d{4}-\d{2}-\d{2}$/)) {
      const [year, month, day] = dateString.split('-');
      const date = new Date(parseInt(year), parseInt(month) - 1, parseInt(day));
      return date.toLocaleDateString('pt-BR');
    }

    // Fallback para outros formatos
    return new Date(dateString).toLocaleDateString('pt-BR');
  };

  // Manipular mudanças no formulário
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  // Abrir formulário para adicionar novo aluno
  const handleAddStudent = () => {
    setCurrentStudent(null);
    setFormData(initialFormData);
    setShowForm(true);
    setFormError(null);
  };

  // Abrir formulário para editar aluno existente
  const handleEditStudent = (student) => {
    setCurrentStudent(student);
    setFormData({
      name: student.name || '',
      username: student.username || '',
      email: student.email || '',
      password: '', // Senha não é pré-preenchida por segurança
      particao_id: student.particao_id ? student.particao_id.toString() : (particoes.length > 0 ? particoes[0].id.toString() : ''), // Preencher partição existente
    });
    setShowForm(true);
    setFormError(null);
  };

  // Salvar aluno (novo ou editado) via API
  const handleSaveStudent = async (e) => {
    e.preventDefault();
    setFormError(null);

    console.log("Dados do formulário:", formData); // Debug

    if (!formData.name || !formData.username || !formData.email || !formData.particao_id) {
      setFormError("Nome, Username, Email e Partição são obrigatórios.");
      console.log("Validação falhou - campos obrigatórios:", {
        name: !!formData.name,
        username: !!formData.username,
        email: !!formData.email,
        particao_id: !!formData.particao_id
      });
      return;
    }
    if (!currentStudent && !formData.password) { // Senha obrigatória apenas para novos alunos
        setFormError("Senha é obrigatória para novos alunos.");
        return;
    }

    const studentData = {
      name: formData.name,
      username: formData.username,
      email: formData.email,
      type: 'student', // Corrigido: usar 'type' em vez de 'role'
      particao_id: formData.particao_id ? parseInt(formData.particao_id) : null, // Incluir ID da partição
    };

    if (formData.password) {
      studentData.password = formData.password;
    }

    console.log("Dados que serão enviados:", studentData); // Debug

    try {
      if (currentStudent && currentStudent.id) {
        // Editar aluno existente
        await userService.update(currentStudent.id, studentData);
      } else {
        // Criar novo aluno
        await userService.create(studentData);
      }

      fetchStudents(); // Recarrega a lista de alunos
      setShowForm(false);
      setCurrentStudent(null); // Limpa o estado de edição
    } catch (err) {
      console.error("Erro ao salvar aluno:", err);
      setFormError(err.message);
    }
  };

  // Excluir aluno via API
  const handleDeleteStudent = async (id) => {
    if (window.confirm('Tem certeza que deseja excluir este aluno? Esta ação não pode ser desfeita.')) {
      try {
        await userService.delete(id);
        fetchStudents(); // Recarrega a lista de alunos
      } catch (err) {
        console.error("Erro ao excluir aluno:", err);
        setError(err.message);
      }
    }
  };

  if (loading) {
    return (
      <div className="p-6 text-white flex justify-center items-center min-h-[300px]">
        <FontAwesomeIcon icon={faSpinner} spin size="3x" />
        <span className="ml-4 text-xl">Carregando alunos...</span>
      </div>
    );
  }

  if (error) {
    return <div className="p-6 text-red-500">Erro ao carregar alunos: {error}. Tente recarregar a página.</div>;
  }

  return (
    <div className="p-4 md:p-6 text-white min-h-screen">
      <div className="flex flex-col md:flex-row md:justify-between md:items-center mb-6 space-y-4 md:space-y-0">
        <h2 className="text-xl md:text-2xl font-semibold text-red-400">Gestão de Alunos</h2>
        <button
          className="bg-red-400 hover:bg-red-500 text-white font-bold py-3 md:py-2 px-4 rounded transition-colors duration-150 w-full md:w-auto"
          onClick={handleAddStudent}
        >
          <FontAwesomeIcon icon={faPlus} className="mr-2" /> Novo Aluno
        </button>
      </div>

      <div className="mb-6">
        <input
          type="text"
          placeholder="Buscar aluno por nome, username ou email..."
          className="w-full bg-gray-500 text-white px-4 py-3 md:py-2 rounded focus:outline-none focus:ring-2 focus:ring-red-300 placeholder-gray-300 text-base"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      {filteredStudents.length === 0 && !loading && (
        <p className="text-gray-400 text-center py-4">Nenhum aluno encontrado.</p>
      )}

      {filteredStudents.length > 0 && (
        <>
          {/* Tabela para Desktop */}
          <div className="hidden md:block bg-gray-700 rounded-lg overflow-x-auto shadow-lg">
            <table className="w-full min-w-full">
              <thead className="bg-gray-500">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Nome</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Username</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Email</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Partição</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Data de Cadastro</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Último Login</th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-white uppercase tracking-wider">Ações</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-600">
                {filteredStudents.map(student => (
                  <tr key={student.id} className="hover:bg-gray-600 transition-colors duration-150">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-white">{student.name}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-white">{student.username}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-white">{student.email}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-white">{student.particao_nome || 'N/A'}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-white">{student.register_date ? formatDateForDisplay(student.register_date) : 'N/A'}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-white">{student.last_login ? new Date(student.last_login).toLocaleString() : 'Nunca'}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <button
                        className="text-blue-400 hover:text-blue-300 mr-3 transition-colors duration-150"
                        onClick={() => handleEditStudent(student)}
                        title="Editar Aluno"
                      >
                        <FontAwesomeIcon icon={faEdit} />
                      </button>
                      <button
                        className="text-red-400 hover:text-red-300 transition-colors duration-150"
                        onClick={() => handleDeleteStudent(student.id)}
                        title="Excluir Aluno"
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
          <div className="md:hidden space-y-4">
            {filteredStudents.map(student => (
              <div key={student.id} className="bg-gray-700 rounded-lg p-4 shadow-lg">
                <div className="flex justify-between items-start mb-3">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-white mb-1">{student.name}</h3>
                    <p className="text-gray-300 text-sm">@{student.username}</p>
                  </div>
                  <div className="flex space-x-3">
                    <button
                      className="text-blue-400 hover:text-blue-300 p-2 transition-colors duration-150"
                      onClick={() => handleEditStudent(student)}
                      title="Editar Aluno"
                    >
                      <FontAwesomeIcon icon={faEdit} className="text-lg" />
                    </button>
                    <button
                      className="text-red-400 hover:text-red-300 p-2 transition-colors duration-150"
                      onClick={() => handleDeleteStudent(student.id)}
                      title="Excluir Aluno"
                    >
                      <FontAwesomeIcon icon={faTrash} className="text-lg" />
                    </button>
                  </div>
                </div>

                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-400">Email:</span>
                    <span className="text-white text-right">{student.email}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Partição:</span>
                    <span className="text-white">{student.particao_nome || 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Cadastro:</span>
                    <span className="text-white">{student.register_date ? formatDateForDisplay(student.register_date) : 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Último Login:</span>
                    <span className="text-white text-right">{student.last_login ? new Date(student.last_login).toLocaleString() : 'Nunca'}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </>
      )}

      {/* Formulário de Aluno Modal */}
      {showForm && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-0 md:p-4">
          <div className="bg-gray-800 w-full h-full md:w-full md:max-w-lg md:h-auto md:max-h-[90vh] md:rounded-lg shadow-xl transform transition-all flex flex-col">
            {/* Header fixo com botão de fechar sempre visível */}
            <div className="flex-shrink-0 bg-gray-800 p-4 md:p-6 border-b border-gray-700 md:rounded-t-lg flex justify-between items-center">
              <h3 className="text-lg md:text-xl font-semibold text-red-400">
                {currentStudent ? 'Editar Aluno' : 'Adicionar Novo Aluno'}
              </h3>
              <button
                type="button"
                onClick={() => { setShowForm(false); setCurrentStudent(null); }}
                className="flex-shrink-0 bg-red-600 hover:bg-red-700 text-white transition-colors p-2 rounded-lg shadow-lg"
                aria-label="Fechar modal"
                title="Fechar"
              >
                <FontAwesomeIcon icon={faTimes} size="lg" />
              </button>
            </div>
            {/* Área de conteúdo scrollável */}
            <div className="flex-1 overflow-y-auto p-4 md:p-6 md:pt-4">
            
            <form onSubmit={handleSaveStudent}>
              {formError && <p className="text-red-500 mb-4 bg-red-900 bg-opacity-50 p-3 rounded">{formError}</p>}
              <div className="mb-4">
                <label htmlFor="name" className="block mb-2 text-sm font-medium text-gray-300">Nome Real</label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  className="w-full bg-gray-700 text-white px-4 py-3 md:py-2 rounded focus:outline-none focus:ring-2 focus:ring-red-400 text-base"
                  required
                />
              </div>

              <div className="mb-4">
                <label htmlFor="username" className="block mb-2 text-sm font-medium text-gray-300">Username</label>
                <input
                  type="text"
                  id="username"
                  name="username"
                  value={formData.username}
                  onChange={handleChange}
                  placeholder="Nome de usuário único (ex: joao_silva)"
                  className="w-full bg-gray-700 text-white px-4 py-3 md:py-2 rounded focus:outline-none focus:ring-2 focus:ring-red-400 text-base"
                  required
                />
              </div>

              <div className="mb-4">
                <label htmlFor="email" className="block mb-2 text-sm font-medium text-gray-300">Email</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="w-full bg-gray-700 text-white px-4 py-3 md:py-2 rounded focus:outline-none focus:ring-2 focus:ring-red-400 text-base"
                  required
                />
              </div>

              <div className="mb-4">
                <label htmlFor="particao_id" className="block mb-1 text-sm font-medium text-gray-300">Partição</label>
                <select
                  id="particao_id"
                  name="particao_id"
                  value={formData.particao_id}
                  onChange={handleChange}
                  className="w-full bg-gray-700 text-white px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-poker-red"
                  required
                >
                  <option value="">Selecione uma partição</option>
                  {particoes.map(particao => (
                    <option key={particao.id} value={particao.id.toString()}>
                      {particao.nome} {particao.descricao ? `- ${particao.descricao}` : ''}
                    </option>
                  ))}
                </select>
                <small className="text-gray-400 block mt-1">Campo obrigatório que identifica a partição do aluno.</small>
              </div>
              
              {/* Campo senha apenas para novos alunos */}
              {!currentStudent && (
                <div className="mb-6">
                  <label htmlFor="password" className="block mb-1 text-sm font-medium text-gray-300">Senha *</label>
                  <input
                    type="password"
                    id="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    placeholder="Senha obrigatória para novo aluno"
                    className="w-full bg-gray-700 text-white px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-poker-red"
                    required
                  />
                  <small className="text-gray-400 block mt-1">A senha será usada pelo aluno para fazer login.</small>
                </div>
              )}

              {/* Aviso para edição de aluno existente */}
              {currentStudent && (
                <div className="mb-6 p-4 bg-blue-900 bg-opacity-30 border border-blue-500 rounded">
                  <p className="text-blue-300 text-sm">
                    <i className="fas fa-info-circle mr-2"></i>
                    <strong>Editando aluno existente:</strong> Para alterar a senha, o aluno deve usar a opção "Alterar Senha" no sistema.
                  </p>
                </div>
              )}
              
              <div className="flex flex-col md:flex-row md:justify-end pt-4 border-t border-gray-700 space-y-3 md:space-y-0 md:space-x-2">
                <button
                  type="button"
                  className="w-full md:w-auto bg-gray-600 hover:bg-gray-500 text-gray-200 font-bold py-3 md:py-2 px-4 rounded transition-colors duration-150 order-2 md:order-1"
                  onClick={() => { setShowForm(false); setCurrentStudent(null); }}
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="w-full md:w-auto bg-red-400 hover:bg-red-500 text-white font-bold py-3 md:py-2 px-4 rounded transition-colors duration-150 order-1 md:order-2"
                >
                  {currentStudent ? 'Salvar Alterações' : 'Adicionar Aluno'}
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

export default StudentManagement;

