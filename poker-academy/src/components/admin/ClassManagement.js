/* eslint-disable no-unused-vars */
// src/components/admin/ClassManagement.js
import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlus, faEdit, faTrash, faSpinner } from '@fortawesome/free-solid-svg-icons';
import { classService, getToken } from '../../services/api';

const ClassManagement = () => {
  const [classes, setClasses] = useState([]);
  const [instructors, setInstructors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [formError, setFormError] = useState(null);

  const [showForm, setShowForm] = useState(false);
  const [currentClass, setCurrentClass] = useState(null); // Para identificar se é edição
  const [searchTerm, setSearchTerm] = useState('');

  const initialFormData = {
    name: '',
    instructor: '',
    category: 'preflop',
    date: new Date().toISOString().split('T')[0],
    priority: 5,
    video_path: '',
    video_type: 'local',
  };
  const [formData, setFormData] = useState(initialFormData);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  const fetchClasses = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await classService.getAll();
      setClasses(data);
    } catch (e) {
      console.error("Erro ao buscar aulas:", e);
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchInstructors = async () => {
    try {
      const data = await classService.getInstructors();
      setInstructors(data);
    } catch (e) {
      console.error("Erro ao buscar instrutores:", e);
    }
  };

  useEffect(() => {
    fetchClasses();
    fetchInstructors();
  }, []);

  const filteredClasses = classes.filter(cls =>
    (cls.name && cls.name.toLowerCase().includes(searchTerm.toLowerCase())) ||
    (cls.instructor && cls.instructor.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  const handleChange = (e) => {
    const { name, value } = e.target;



    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleAddClass = () => {
    setCurrentClass(null); // Garante que não estamos em modo de edição
    setFormData(initialFormData);
    setShowForm(true);
    setFormError(null);
  };

  const handleEditClass = (cls) => {
    setCurrentClass(cls); // Define a aula atual para edição

    // Corrigir problema de timezone na data
    let dateValue = new Date().toISOString().split('T')[0];
    if (cls.date) {
      // A data vem do backend como string YYYY-MM-DD, usar diretamente
      dateValue = cls.date;
    }

    setFormData({
      name: cls.name || '',
      instructor: cls.instructor || '',
      category: cls.category || 'preflop',
      date: dateValue,
      priority: cls.priority || 5,
      video_path: cls.video_path || '',
      video_type: 'local',
    });
    setShowForm(true);
    setFormError(null);
    setSelectedFile(null);
    setUploadProgress(0);
  };

  // Validar formato e tamanho do arquivo
  const validateFile = (file) => {
    const allowedFormats = ['mp4', 'avi', 'mov', 'wmv', 'flv', 'webm', 'mkv'];
    const maxSize = 500 * 1024 * 1024; // 500MB em bytes

    if (!file) return { valid: false, error: 'Nenhum arquivo selecionado' };

    const fileExtension = file.name.split('.').pop().toLowerCase();
    if (!allowedFormats.includes(fileExtension)) {
      return {
        valid: false,
        error: `Formato não suportado. Use: ${allowedFormats.join(', ').toUpperCase()}`
      };
    }

    if (file.size > maxSize) {
      return {
        valid: false,
        error: `Arquivo muito grande. Máximo: 500MB (atual: ${(file.size / 1024 / 1024).toFixed(1)}MB)`
      };
    }

    return { valid: true };
  };

  // Função para upload de vídeo com barra de progresso
  const handleFileUpload = async () => {
    if (!selectedFile) {
      console.error('Nenhum arquivo selecionado para upload');
      return null;
    }

    // Validar arquivo antes do upload
    const validation = validateFile(selectedFile);
    if (!validation.valid) {
      setFormError(validation.error);
      return null;
    }

    console.log('Iniciando upload do arquivo:', selectedFile.name, 'Tamanho:', selectedFile.size);
    setUploading(true);
    setUploadProgress(0);

    const formDataUpload = new FormData();
    formDataUpload.append('video', selectedFile);

    try {
      // Usar o token do sistema de API
      const token = getToken();
      console.log('Token para upload:', token ? 'Presente' : 'Ausente');

      if (!token) {
        throw new Error('Token de autenticação não encontrado. Faça login novamente.');
      }

      // Criar XMLHttpRequest para monitorar progresso
      const xhr = new XMLHttpRequest();

      return new Promise((resolve, reject) => {
        // Monitorar progresso do upload
        xhr.upload.addEventListener('progress', (e) => {
          if (e.lengthComputable) {
            const percentComplete = Math.round((e.loaded / e.total) * 100);
            setUploadProgress(percentComplete);
            console.log(`Upload progress: ${percentComplete}%`);
          }
        });

        // Configurar resposta
        xhr.addEventListener('load', () => {
          if (xhr.status === 200) {
            try {
              const result = JSON.parse(xhr.responseText);
              console.log('Upload bem-sucedido, filename:', result.filename);
              setUploadProgress(100);

              // Manter a barra visível por 1 segundo antes de resolver
              setTimeout(() => {
                setUploading(false);
                setUploadProgress(0);
                resolve(result.filename);
              }, 1000);
            } catch (e) {
              setUploading(false);
              setUploadProgress(0);
              reject(new Error('Erro ao processar resposta do servidor'));
            }
          } else {
            try {
              const errorResult = JSON.parse(xhr.responseText);
              setUploading(false);
              setUploadProgress(0);
              reject(new Error(errorResult.error || 'Erro no upload'));
            } catch (e) {
              setUploading(false);
              setUploadProgress(0);
              reject(new Error(`Erro no upload: ${xhr.status} ${xhr.statusText}`));
            }
          }
        });

        xhr.addEventListener('error', () => {
          setUploading(false);
          setUploadProgress(0);
          reject(new Error('Erro de conexão durante o upload'));
        });

        xhr.addEventListener('abort', () => {
          setUploading(false);
          setUploadProgress(0);
          reject(new Error('Upload cancelado'));
        });

        // Configurar e enviar requisição
        xhr.open('POST', 'http://localhost:5000/api/classes/upload-video');
        xhr.setRequestHeader('Authorization', `Bearer ${token}`);
        xhr.send(formDataUpload);
      });

    } catch (error) {
      console.error('Erro no upload:', error);
      setFormError(`Erro no upload: ${error.message}`);
      setUploading(false);
      setUploadProgress(0);
      return null;
    }
  };

  const handleSaveClass = async (e) => {
    e.preventDefault();
    setFormError(null);

    if (!formData.name || !formData.instructor || !formData.date || !formData.category) {
      setFormError("Por favor, preencha todos os campos obrigatórios.");
      return;
    }

    // Upload de vídeo obrigatório para novas aulas
    let uploadedFilename = null;
    if (selectedFile) {
      console.log('Fazendo upload do arquivo:', selectedFile.name);
      uploadedFilename = await handleFileUpload();
      if (!uploadedFilename) {
        console.error('Falha no upload do arquivo');
        return; // Erro no upload, não continuar
      }
      console.log('Upload concluído:', uploadedFilename);
    } else if (!currentClass || !currentClass.video_path) {
      setFormError("Por favor, selecione um arquivo de vídeo.");
      return;
    }

    // Verificar se temos um video_path válido
    const finalVideoPath = uploadedFilename || formData.video_path;
    if (!finalVideoPath) {
      setFormError("É necessário fazer upload de um vídeo.");
      return;
    }

    // Garantir que a data seja enviada no formato correto
    const dateToSend = formData.date;

    const classData = {
      name: formData.name,
      instructor: formData.instructor,
      date: dateToSend, // Enviar a data exatamente como está no input
      category: formData.category,
      video_type: 'local',
      video_path: finalVideoPath,
      priority: parseInt(formData.priority, 10) || 5,
    };

    console.log('Dados sendo enviados:', classData);

    // Definir views para novas aulas
    if (!currentClass || !currentClass.id) {
      classData.views = 0;
    }

    try {
      if (currentClass && currentClass.id) {
        // Editar aula existente
        await classService.update(currentClass.id, classData);
      } else {
        // Criar nova aula
        await classService.create(classData);
      }

      fetchClasses();
      setShowForm(false);
      setCurrentClass(null); // Limpa o estado de edição
    } catch (err) {
      console.error("Erro ao salvar aula:", err);
      setFormError(err.message);
    }
  };

  const handleDeleteClass = async (id) => {
    if (window.confirm('Tem certeza que deseja excluir esta aula?')) {
      try {
        await classService.delete(id);
        fetchClasses(); // Recarrega as aulas
      } catch (err) {
        console.error("Erro ao excluir aula:", err);
        setError(err.message);
      }
    }
  };
  
  const getCategoryName = (category) => {
    const categories = {
      'preflop': 'Pré-Flop',
      'postflop': 'Pós-Flop',
      'mental': 'Mental Game',
      'torneos': 'Torneios',
      'cash': 'Cash Game'
    };
    return categories[category] || category;
  };

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

  if (loading) {
    return (
      <div className="p-6 text-white flex justify-center items-center min-h-[300px]">
        <FontAwesomeIcon icon={faSpinner} spin size="3x" />
        <span className="ml-4 text-xl">Carregando aulas...</span>
      </div>
    );
  }

  if (error) {
    return <div className="p-6 text-red-500">Erro ao carregar aulas: {error}. Tente recarregar a página.</div>;
  }

  return (
    <div className="p-6 text-white min-h-screen">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-semibold text-red-400">Gestão de Aulas</h2>
        <button
          className="bg-red-400 hover:bg-red-500 text-white font-bold py-2 px-4 rounded transition-colors duration-150"
          onClick={handleAddClass}
        >
          <FontAwesomeIcon icon={faPlus} className="mr-2" /> Nova Aula
        </button>
      </div>

      <div className="mb-6">
        <input
          type="text"
          placeholder="Buscar aula por nome ou instrutor..."
          className="w-full bg-gray-500 text-white px-4 py-2 rounded focus:outline-none focus:ring-2 focus:ring-red-300 placeholder-gray-300"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      {filteredClasses.length === 0 && !loading && (
        <p className="text-gray-400 text-center py-4">Nenhuma aula encontrada.</p>
      )}

      {filteredClasses.length > 0 && (
        <div className="bg-gray-700 rounded-lg overflow-x-auto shadow-lg">
          <table className="w-full min-w-full">
            <thead className="bg-gray-500">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Nome</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Instrutor</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Categoria</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Data</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Visualizações</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-white uppercase tracking-wider">Ações</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-600">
              {filteredClasses.map(cls => (
                <tr key={cls.id} className="hover:bg-gray-600 transition-colors duration-150">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-white">{cls.name}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-white">{cls.instructor}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-white">{getCategoryName(cls.category)}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-white">{formatDateForDisplay(cls.date)}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-white">
                    <span className="bg-red-100 text-black px-2 py-1 rounded-full text-xs">
                      {cls.views || 0} views
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button
                      className="text-blue-400 hover:text-blue-300 mr-3 transition-colors duration-150"
                      onClick={() => handleEditClass(cls)}
                      title="Editar Aula"
                    >
                      <FontAwesomeIcon icon={faEdit} />
                    </button>
                    <button
                      className="text-red-400 hover:text-red-300 transition-colors duration-150"
                      onClick={() => handleDeleteClass(cls.id)}
                      title="Excluir Aula"
                    >
                      <FontAwesomeIcon icon={faTrash} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {showForm && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
          <div className="bg-gray-800 p-6 rounded-lg w-full max-w-lg shadow-xl transform transition-all">
            <h3 className="text-xl font-semibold mb-6 text-poker-red">
              {currentClass ? 'Editar Aula' : 'Adicionar Nova Aula'}
            </h3>
            
            <form onSubmit={handleSaveClass}>
              {formError && <p className="text-red-500 mb-4 bg-red-900 bg-opacity-50 p-3 rounded">{formError}</p>}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div>
                  <label htmlFor="name" className="block mb-1 text-sm font-medium text-gray-300">Nome da Aula *</label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    className="w-full bg-gray-700 text-white px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-poker-red"
                    required
                    placeholder="Digite o nome da aula"
                  />
                </div>
                <div>
                  <label htmlFor="instructor" className="block mb-1 text-sm font-medium text-gray-300">Instrutor *</label>
                  <select
                    id="instructor"
                    name="instructor"
                    value={formData.instructor}
                    onChange={handleChange}
                    className="w-full bg-gray-700 text-white px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-poker-red"
                    required
                  >
                    <option value="">Selecione um instrutor</option>
                    {instructors.map(instructor => (
                      <option key={instructor.id} value={instructor.name}>
                        {instructor.name}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div>
                  <label htmlFor="date" className="block mb-1 text-sm font-medium text-gray-300">Data</label>
                  <input 
                    type="date" 
                    id="date" 
                    name="date"
                    value={formData.date}
                    onChange={handleChange}
                    className="w-full bg-gray-700 text-white px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-poker-red calendar-dark" 
                    required 
                  />
                </div>
                <div>
                  <label htmlFor="category" className="block mb-1 text-sm font-medium text-gray-300">Categoria</label>
                  <select 
                    id="category" 
                    name="category"
                    value={formData.category}
                    onChange={handleChange}
                    className="w-full bg-gray-700 text-white px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-poker-red" 
                    required
                  >
                    <option value="preflop">Pré-Flop</option>
                    <option value="postflop">Pós-Flop</option>
                    <option value="mental">Mental Game</option>
                    <option value="torneos">Torneios</option>
                    <option value="cash">Cash Game</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div>
                  <label htmlFor="priority" className="block mb-1 text-sm font-medium text-gray-300">Prioridade (1-10)</label>
                  <input 
                    type="number" 
                    id="priority" 
                    name="priority"
                    min="1" 
                    max="10" 
                    value={formData.priority}
                    onChange={handleChange}
                    className="w-full bg-gray-700 text-white px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-poker-red"
                  />
                </div>
                <div>
                  <label className="block mb-1 text-sm font-medium text-gray-300">Tipo de Vídeo</label>
                  <div className="w-full bg-gray-700 text-white px-3 py-2 rounded">
                    Vídeo Local (Upload)
                  </div>
                </div>
              </div>
              
              <div className="mb-6">
                <label htmlFor="video_file" className="block mb-1 text-sm font-medium text-gray-300">
                  Upload de Vídeo *
                </label>
                <input
                  type="file"
                  id="video_file"
                  accept=".mp4,.avi,.mov,.wmv,.flv,.webm,.mkv"
                  onChange={(e) => {
                    const file = e.target.files[0];
                    if (file) {
                      const validation = validateFile(file);
                      if (validation.valid) {
                        setSelectedFile(file);
                        setFormError(null);
                      } else {
                        setFormError(validation.error);
                        e.target.value = ''; // Limpar input
                        setSelectedFile(null);
                      }
                    }
                  }}
                  disabled={uploading}
                  className="w-full bg-gray-700 text-white px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-poker-red file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-poker-red file:text-white hover:file:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed"
                />

                {/* Informações do arquivo selecionado */}
                {selectedFile && !uploading && (
                  <div className="mt-3 p-3 bg-green-900 bg-opacity-30 border border-green-500 rounded">
                    <p className="text-green-400 text-sm">
                      <i className="fas fa-check-circle mr-2"></i>
                      <strong>Arquivo válido:</strong> {selectedFile.name}
                    </p>
                    <p className="text-green-300 text-xs mt-1">
                      Tamanho: {(selectedFile.size / 1024 / 1024).toFixed(1)}MB
                    </p>
                  </div>
                )}

                {/* Barra de progresso durante upload */}
                {uploading && (
                  <div className="mt-3 p-4 bg-blue-900 bg-opacity-30 border border-blue-500 rounded">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-blue-300 text-sm font-medium">
                        <i className="fas fa-cloud-upload-alt mr-2"></i>
                        Fazendo upload...
                      </span>
                      <span className="text-blue-300 text-sm font-bold">
                        {uploadProgress}%
                      </span>
                    </div>

                    {/* Barra de progresso */}
                    <div className="w-full bg-gray-700 rounded-full h-3 overflow-hidden">
                      <div
                        className="bg-gradient-to-r from-blue-500 to-blue-600 h-full rounded-full transition-all duration-300 ease-out"
                        style={{ width: `${uploadProgress}%` }}
                      ></div>
                    </div>

                    <p className="text-blue-200 text-xs mt-2">
                      {selectedFile ? `Enviando: ${selectedFile.name}` : 'Processando...'}
                    </p>
                  </div>
                )}

                {/* Vídeo atual (para edição) */}
                {formData.video_path && !selectedFile && !uploading && (
                  <div className="mt-3 p-3 bg-blue-900 bg-opacity-30 border border-blue-500 rounded">
                    <p className="text-blue-400 text-sm">
                      <i className="fas fa-video mr-2"></i>
                      <strong>Vídeo atual:</strong> {formData.video_path}
                    </p>
                    <p className="text-blue-300 text-xs mt-1">
                      Selecione um novo arquivo para substituir
                    </p>
                  </div>
                )}

                {/* Instruções de formato */}
                <div className="mt-2 p-2 bg-gray-800 rounded">
                  <p className="text-gray-400 text-xs">
                    <i className="fas fa-info-circle mr-1"></i>
                    <strong>Formatos aceitos:</strong> MP4, AVI, MOV, WMV, FLV, WEBM, MKV
                  </p>
                  <p className="text-gray-400 text-xs">
                    <i className="fas fa-weight-hanging mr-1"></i>
                    <strong>Tamanho máximo:</strong> 500MB
                  </p>
                </div>
              </div>
              
              <div className="flex justify-end pt-2 border-t border-gray-700">
                <button 
                  type="button" 
                  className="bg-gray-600 hover:bg-gray-500 text-gray-200 font-bold py-2 px-4 rounded mr-2 transition-colors duration-150"
                  onClick={() => { setShowForm(false); setCurrentClass(null); }}
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={uploading}
                  className="bg-poker-red hover:bg-red-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-bold py-2 px-4 rounded transition-colors duration-150 flex items-center"
                >
                  {uploading ? (
                    <>
                      <i className="fas fa-spinner fa-spin mr-2"></i>
                      Fazendo Upload... ({uploadProgress}%)
                    </>
                  ) : (
                    <>
                      <i className={`fas ${currentClass ? 'fa-save' : 'fa-plus'} mr-2`}></i>
                      {currentClass ? 'Salvar Alterações' : 'Salvar Nova Aula'}
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default ClassManagement;

