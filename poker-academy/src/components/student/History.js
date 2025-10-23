import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSpinner, faPlay, faRedo, faTimes } from '@fortawesome/free-solid-svg-icons';
import { classService } from '../../services/api';
import VideoPlayer from '../shared/VideoPlayer';

const History = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedClass, setSelectedClass] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Buscar histórico de aulas
  const fetchHistory = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await classService.getHistory();
      console.log('📚 History: Dados brutos recebidos:', data);
      console.log('📚 History: Tipo de data:', typeof data);
      console.log('📚 History: data.data:', data?.data);

      // Extrair dados corretos
      // A API retorna um array diretamente, mas apiRequest envolve em { data: [...] }
      let historyData = data?.data || data;

      // Se ainda não for array, tentar extrair de outras formas
      if (!Array.isArray(historyData)) {
        console.warn('📚 History: historyData não é array, tentando extrair...');
        // Se for um objeto com propriedade que é array
        for (let key in historyData) {
          if (Array.isArray(historyData[key])) {
            historyData = historyData[key];
            break;
          }
        }
      }

      console.log('📚 History: Dados extraídos:', historyData);
      console.log('📚 History: É array?', Array.isArray(historyData));

      // Garantir que é um array
      const historyArray = Array.isArray(historyData) ? historyData : [];
      console.log('📚 History: Array final:', historyArray);
      setHistory(historyArray);
    } catch (e) {
      console.error("Erro ao buscar histórico:", e);
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  // Função para continuar assistindo uma aula
  const handleContinueWatching = async (classId) => {
    try {
      const data = await classService.getById(classId);
      setSelectedClass(data);
      setIsModalOpen(true);
    } catch (e) {
      console.error("Erro ao buscar detalhes da aula:", e);
      setError("Não foi possível carregar os detalhes da aula. " + e.message);
    }
  };

  // Função para fechar o modal
  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedClass(null);
  };

  // Função para formatar data
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

  // Função para formatar data
  const formatLastWatched = (dateString) => {
    if (!dateString) return 'Nunca';

    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 1) return 'Ontem';
    if (diffDays <= 7) return `Há ${diffDays} dias`;
    if (diffDays <= 30) return `Há ${Math.ceil(diffDays / 7)} semanas`;
    return `Há ${Math.ceil(diffDays / 30)} meses`;
  };

  // Função para obter cor da categoria
  const getCategoryColor = (category) => {
    const colors = {
      'iniciantes': '#9B59B6',
      'preflop': '#FF6B6B',
      'postflop': '#4ECDC4',
      'mental': '#45B7D1',
      'icm': '#96CEB4'
    };
    return colors[category] || '#6C5CE7';
  };

  if (loading) {
    return (
      <div className="p-6 text-white min-h-screen flex justify-center items-center">
        <FontAwesomeIcon icon={faSpinner} spin size="3x" />
        <span className="ml-4 text-xl">Carregando histórico...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 text-white min-h-screen">
        <h2 className="text-3xl font-bold mb-8 text-red-400">Meu Histórico de Aulas</h2>
        <div className="text-red-500 text-center">
          <p>Erro ao carregar histórico: {error}</p>
          <button
            onClick={fetchHistory}
            className="mt-4 bg-red-400 hover:bg-red-500 text-white py-2 px-4 rounded transition-colors"
          >
            Tentar Novamente
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 text-white min-h-screen">
      <h2 className="text-3xl font-bold mb-8 text-red-400">Meu Histórico de Aulas</h2>

      {!Array.isArray(history) ? (
        <div className="text-center text-red-400 py-12">
          <p className="text-xl">Erro: Dados inválidos recebidos</p>
          <p className="text-sm mt-2">Tipo recebido: {typeof history}</p>
          <p className="text-sm mt-2">Conteúdo: {JSON.stringify(history).substring(0, 100)}</p>
        </div>
      ) : history.length === 0 ? (
        <div className="text-center text-gray-400 py-12">
          <FontAwesomeIcon icon={faPlay} size="3x" className="mb-4 opacity-50" />
          <p className="text-xl">Você ainda não assistiu nenhuma aula.</p>
          <p className="text-sm mt-2">Comece explorando nosso catálogo de aulas!</p>
        </div>
      ) : (
        <div className="space-y-4">
          {history.map(item => (
            <div key={item.id} className="bg-gray-700 p-4 rounded-lg shadow-md flex items-center gap-4 transform hover:bg-gray-600 transition-colors duration-200">
              {/* Thumbnail com cor da categoria */}
              <div
                className="w-32 h-20 rounded flex items-center justify-center text-white font-bold text-sm"
                style={{ backgroundColor: getCategoryColor(item.category) }}
              >
                {item.category?.toUpperCase() || 'AULA'}
              </div>

              <div className="flex-1">
                <h3 className="text-lg font-semibold text-white truncate" title={item.name}>
                  {item.name}
                </h3>
                <p className="text-sm text-gray-400">
                  Instrutor: {item.instructor}
                </p>
                <p className="text-sm text-gray-400">
                  Última vez assistido: {formatLastWatched(item.last_watched)}
                </p>
                <div className="w-full bg-gray-600 rounded-full h-2.5 mt-2">
                  <div
                    className="bg-red-400 h-2.5 rounded-full transition-all duration-300"
                    style={{ width: `${item.progress}%` }}
                    aria-valuenow={item.progress}
                    aria-valuemin="0"
                    aria-valuemax="100"
                  ></div>
                </div>
                <p className="text-xs text-gray-400 mt-1">{item.progress}% completo</p>
              </div>

              <button
                onClick={() => handleContinueWatching(item.id)}
                className="bg-red-400 hover:bg-red-500 text-white py-2 px-4 rounded transition-colors text-sm whitespace-nowrap flex items-center gap-2"
              >
                <FontAwesomeIcon icon={item.progress === 100 ? faRedo : faPlay} />
                {item.progress === 100 ? 'Rever Aula' : 'Continuar'}
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Modal de detalhes da aula */}
      {isModalOpen && selectedClass && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
          <div className="bg-gray-800 p-6 rounded-lg w-full max-w-2xl shadow-xl transform transition-all relative">
            <button
              onClick={closeModal}
              className="absolute top-3 right-3 text-gray-400 hover:text-white transition-colors"
              aria-label="Fechar modal"
            >
              <FontAwesomeIcon icon={faTimes} size="lg" />
            </button>
            <h3 className="text-2xl font-semibold mb-4 text-red-400">{selectedClass.name}</h3>
            <p className="text-gray-300 mb-1"><span className="font-semibold">Instrutor:</span> {selectedClass.instructor}</p>
            <p className="text-gray-300 mb-1"><span className="font-semibold">Categoria:</span> {selectedClass.category}</p>
            <p className="text-gray-300 mb-3"><span className="font-semibold">Data:</span> {formatDateForDisplay(selectedClass.date)}</p>

            {/* Player de vídeo */}
            <VideoPlayer
              classData={selectedClass}
              onViewRegistered={(totalViews) => {
                console.log(`Visualização registrada. Total: ${totalViews}`);
                setSelectedClass(prev => ({
                  ...prev,
                  views: totalViews
                }));
                // Atualizar também no histórico se necessário
                setHistory(prev => prev.map(item =>
                  item.id === selectedClass.id
                    ? { ...item, views: totalViews }
                    : item
                ));
              }}
            />

            <div className="mt-6 flex justify-end">
              <button
                onClick={closeModal}
                className="bg-gray-600 hover:bg-gray-500 text-gray-200 font-bold py-2 px-4 rounded transition-colors duration-150"
              >
                Fechar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default History;
