// src/components/student/Favorites.js
import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTimes, faHeart } from '@fortawesome/free-solid-svg-icons';
import { favoritesService, classService } from '../../services/api';
import VideoPlayer from '../shared/VideoPlayer';

const Favorites = () => {
  const [favorites, setFavorites] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedClass, setSelectedClass] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    const fetchFavorites = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await favoritesService.getAll();
        const data = response.data || response;

        // Garantir que data é um array e ordenar por data mais recente
        const favoritesArray = Array.isArray(data) ? data : [];
        const sortedFavorites = favoritesArray.sort((a, b) => {
          const dateA = a.date ? new Date(a.date).getTime() : 0;
          const dateB = b.date ? new Date(b.date).getTime() : 0;
          return dateB - dateA; // Ordem decrescente (mais recente primeiro)
        });

        setFavorites(sortedFavorites);
      } catch (e) {
        console.error("Erro ao buscar favoritos:", e);
        setError(e.message);
        setFavorites([]); // Garantir que favorites seja sempre um array
      } finally {
        setLoading(false);
      }
    };

    fetchFavorites();
  }, []);

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

  const handleViewDetails = async (classId) => {
    try {
      const data = await classService.getById(classId);
      setSelectedClass(data);
      setIsModalOpen(true);
    } catch (e) {
      console.error("Erro ao buscar detalhes da aula:", e);
      setError("Não foi possível carregar os detalhes da aula. " + e.message);
    }
  };

  const handleRemoveFavorite = async (classId) => {
    try {
      await favoritesService.remove(classId);
      setFavorites(prev => prev.filter(fav => fav.id !== classId));
    } catch (e) {
      console.error("Erro ao remover favorito:", e);
      setError("Erro ao remover dos favoritos: " + e.message);
    }
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedClass(null);
  };

  if (loading) {
    return <div className="p-6 text-white">Carregando favoritos...</div>;
  }

  if (error) {
    return <div className="p-6 text-red-500">Erro ao carregar favoritos: {error}</div>;
  }

  return (
    <div className="p-6 text-white min-h-screen">
      <h2 className="text-3xl font-bold mb-8 text-red-400">Favoritos</h2>

      {favorites.length === 0 ? (
        <p className="text-gray-400">Você ainda não tem aulas favoritas. Adicione algumas aulas aos favoritos no catálogo!</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {favorites.map(cls => (
            <div key={cls.id} className="bg-gray-700 p-4 rounded-lg shadow-md transform hover:bg-gray-600 transition-all duration-200 hover:scale-105 flex flex-col justify-between">
              <div>
                <div className="flex justify-between items-start mb-2">
                  <h3 className="text-xl font-semibold text-white truncate flex-1" title={cls.name}>{cls.name}</h3>
                  <button
                    onClick={() => handleRemoveFavorite(cls.id)}
                    className="ml-2 p-1 rounded transition-colors text-red-500 hover:text-red-400"
                    title="Remover dos favoritos"
                  >
                    <FontAwesomeIcon icon={faHeart} />
                  </button>
                </div>
                <p className="text-sm text-gray-400 mb-1">Instrutor: {cls.instructor}</p>
                <p className="text-sm text-gray-400 mb-1">Categoria: {cls.category}</p>
                <p className="text-sm text-gray-400 mb-3">Data: {formatDateForDisplay(cls.date)}</p>
              </div>
              <button
                onClick={() => handleViewDetails(cls.id)}
                className="w-full bg-red-400 hover:bg-red-500 text-white py-2 px-4 rounded transition-colors mt-2"
              >
                Ver Detalhes
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Modal de detalhes da aula */}
      {isModalOpen && selectedClass && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-0 md:p-4">
          <div className="bg-gray-800 w-full h-full md:w-full md:max-w-4xl md:max-h-[95vh] md:rounded-lg shadow-xl transform transition-all flex flex-col">
            {/* Header fixo com botão de fechar sempre visível */}
            <div className="flex-shrink-0 bg-gray-800 p-4 border-b border-gray-700 flex justify-between items-start md:rounded-t-lg">
              <div className="flex-1 pr-4">
                <h3 className="text-xl md:text-2xl font-semibold text-red-400 leading-tight">{selectedClass.name}</h3>
                <div className="mt-2 space-y-1 text-sm text-gray-400">
                  <p><span className="text-gray-300 font-semibold">Instrutor:</span> {selectedClass.instructor}</p>
                  <p><span className="text-gray-300 font-semibold">Categoria:</span> {selectedClass.category}</p>
                  <p><span className="text-gray-300 font-semibold">Data:</span> {formatDateForDisplay(selectedClass.date)}</p>
                </div>
              </div>
              <button
                onClick={closeModal}
                className="flex-shrink-0 bg-red-600 hover:bg-red-700 text-white transition-colors p-2 rounded-lg shadow-lg"
                aria-label="Fechar modal"
                title="Fechar"
              >
                <FontAwesomeIcon icon={faTimes} size="xl" />
              </button>
            </div>

            {/* Área de conteúdo scrollável */}
            <div className="flex-1 overflow-y-auto p-4 md:p-6">
              {/* Player de vídeo */}
              <VideoPlayer
                classData={selectedClass}
                onViewRegistered={(totalViews) => {
                  console.log(`Visualização registrada. Total: ${totalViews}`);
                  setSelectedClass(prev => ({
                    ...prev,
                    views: totalViews
                  }));
                }}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Favorites;
