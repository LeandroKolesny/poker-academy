// src/components/student/Catalog.js
import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTimes, faHeart, faPlus } from '@fortawesome/free-solid-svg-icons';
import { classService, favoritesService } from '../../services/api';
import VideoPlayer from '../shared/VideoPlayer';

const Catalog = () => {
  const [classes, setClasses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedClass, setSelectedClass] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [favorites, setFavorites] = useState(new Set());
  const [searchTerm, setSearchTerm] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('all');

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        // Buscar aulas e favoritos em paralelo
        const [classesResponse, favoritesResponse] = await Promise.all([
          classService.getAll(),
          favoritesService.getAll().catch(() => []) // Se falhar, retorna array vazio
        ]);

        const classesData = classesResponse.data || classesResponse;
        const favoritesData = favoritesResponse.data || favoritesResponse;

        setClasses(Array.isArray(classesData) ? classesData : []);

        // Criar Set com IDs dos favoritos para busca rápida
        const favoriteIds = new Set(Array.isArray(favoritesData) ? favoritesData.map(fav => fav.id) : []);
        setFavorites(favoriteIds);

      } catch (e) {
        console.error("Erro ao buscar dados:", e);
        setError(e.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleViewDetails = async (classId) => {
    try {
      const data = await classService.getById(classId);
      setSelectedClass(data);
      setIsModalOpen(true);
    } catch (e) {
      console.error("Erro ao buscar detalhes da aula:", e);
      setError("Não foi possível carregar os detalhes da aula. " + e.message);
      setSelectedClass(null);
      setIsModalOpen(false);
    }
  };

  const handleToggleFavorite = async (classId) => {
    try {
      if (favorites.has(classId)) {
        await favoritesService.remove(classId);
        setFavorites(prev => {
          const newSet = new Set(prev);
          newSet.delete(classId);
          return newSet;
        });
      } else {
        await favoritesService.add(classId);
        setFavorites(prev => new Set([...prev, classId]));
      }
    } catch (e) {
      console.error("Erro ao atualizar favoritos:", e);
      setError("Erro ao atualizar favoritos: " + e.message);
    }
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedClass(null);
  };

  // Filtrar aulas baseado na busca e categoria
  const filteredClasses = classes.filter(cls => {
    const matchesSearch = cls.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         cls.instructor.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = categoryFilter === 'all' || cls.category === categoryFilter;
    return matchesSearch && matchesCategory;
  });

  const categories = ['all', 'preflop', 'postflop', 'mental', 'icm'];

  const getCategoryDisplayName = (category) => {
    const categoryNames = {
      'all': 'Todas as Categorias',
      'preflop': 'Pré-Flop',
      'postflop': 'Pós-Flop',
      'mental': 'Mental Game',
      'icm': 'ICM'
    };
    return categoryNames[category] || category;
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
    return <div className="p-6 text-white">Carregando catálogo de aulas...</div>;
  }

  // Exibe erro principal se houver, ou erro específico de modal se aplicável
  if (error && !isModalOpen) { // Só mostra erro principal se o modal não estiver tentando exibir algo
    return <div className="p-6 text-red-500">Erro ao carregar aulas: {error}</div>;
  }

  return (
    <div className="p-4 md:p-6 text-white min-h-screen">
      <h2 className="text-2xl md:text-3xl font-bold mb-6 md:mb-8 text-red-400">Catálogo de Aulas</h2>

      {/* Filtros */}
      <div className="mb-6 space-y-4">
        <div className="flex flex-col md:flex-row gap-4">
          <input
            type="text"
            placeholder="Buscar por nome da aula ou instrutor..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="flex-1 bg-gray-500 text-white px-4 py-3 md:py-2 rounded focus:outline-none focus:ring-2 focus:ring-red-300 placeholder-gray-300 text-base"
          />
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="bg-gray-500 text-white px-4 py-3 md:py-2 rounded focus:outline-none focus:ring-2 focus:ring-red-300 text-base"
          >
            {categories.map(category => (
              <option key={category} value={category}>
                {getCategoryDisplayName(category)}
              </option>
            ))}
          </select>
        </div>
      </div>

      {filteredClasses.length === 0 && !loading ? (
        <p className="text-gray-400">
          {searchTerm || categoryFilter !== 'all'
            ? 'Nenhuma aula encontrada com os filtros aplicados.'
            : 'Nenhuma aula disponível no momento.'}
        </p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">
          {filteredClasses.map(cls => (
            <div key={cls.id} className="bg-gray-700 p-4 md:p-4 rounded-lg shadow-md transform hover:bg-gray-600 transition-all duration-200 md:hover:scale-105 flex flex-col justify-between">
              <div>
                <div className="flex justify-between items-start mb-3">
                  <h3 className="text-lg md:text-xl font-semibold text-white flex-1 pr-2 leading-tight" title={cls.name}>
                    {cls.name}
                  </h3>
                  <button
                    onClick={() => handleToggleFavorite(cls.id)}
                    className={`p-2 rounded transition-colors ${
                      favorites.has(cls.id)
                        ? 'text-red-500 hover:text-red-400'
                        : 'text-gray-400 hover:text-red-500'
                    }`}
                    title={favorites.has(cls.id) ? 'Remover dos favoritos' : 'Adicionar aos favoritos'}
                  >
                    <FontAwesomeIcon icon={faHeart} className="text-lg" />
                  </button>
                </div>
                <div className="space-y-1 mb-4">
                  <p className="text-sm text-gray-400">Instrutor: {cls.instructor}</p>
                  <p className="text-sm text-gray-400">Categoria: {getCategoryDisplayName(cls.category)}</p>
                  <p className="text-sm text-gray-400">Data: {formatDateForDisplay(cls.date)}</p>
                </div>
              </div>
              <button
                onClick={() => handleViewDetails(cls.id)}
                className="w-full bg-red-400 hover:bg-red-500 text-white py-3 md:py-2 px-4 rounded transition-colors mt-2 font-medium"
              >
                Ver Detalhes
              </button>
            </div>
          ))}
        </div>
      )}

      {isModalOpen && selectedClass && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-0 md:p-4">
          <div className="bg-gray-800 w-full h-full md:w-full md:max-w-4xl md:h-auto md:rounded-lg shadow-xl transform transition-all relative overflow-y-auto">
            <div className="sticky top-0 bg-gray-800 p-4 border-b border-gray-700 flex justify-between items-center">
              <h3 className="text-xl md:text-2xl font-semibold text-red-400 truncate pr-4">{selectedClass.name}</h3>
              <button
                onClick={closeModal}
                className="text-gray-400 hover:text-white transition-colors p-2"
                aria-label="Fechar modal"
              >
                <FontAwesomeIcon icon={faTimes} size="lg" />
              </button>
            </div>

            <div className="p-4 md:p-6">
              <div className="mb-4 space-y-2">
                <p className="text-gray-300 text-sm md:text-base"><span className="font-semibold">Instrutor:</span> {selectedClass.instructor}</p>
                <p className="text-gray-300 text-sm md:text-base"><span className="font-semibold">Categoria:</span> {getCategoryDisplayName(selectedClass.category)}</p>
                <p className="text-gray-300 text-sm md:text-base"><span className="font-semibold">Data:</span> {formatDateForDisplay(selectedClass.date)}</p>
              </div>

              {/* Player de vídeo com registro de visualização */}
              <VideoPlayer
                classData={selectedClass}
                onViewRegistered={(totalViews) => {
                  console.log(`Visualização registrada. Total: ${totalViews}`);
                  // Atualizar contador de views localmente
                  setSelectedClass(prev => ({
                    ...prev,
                    views: totalViews
                  }));
                  // Atualizar também na lista principal
                  setClasses(prev => prev.map(cls =>
                    cls.id === selectedClass.id
                      ? { ...cls, views: totalViews }
                      : cls
                  ));
                }}
              />

              {/* Adicionar mais detalhes da aula aqui se necessário, como descrição, etc. */}

              <div className="mt-6 flex justify-center md:justify-end">
                <button
                  onClick={closeModal}
                  className="w-full md:w-auto bg-gray-600 hover:bg-gray-500 text-gray-200 font-bold py-3 px-6 rounded transition-colors duration-150"
                >
                  Fechar
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
      {/* Exibe erro específico do modal, se houver, e o modal estiver fechado */}
      {error && selectedClass === null && !isModalOpen && (
         <div className="p-6 text-red-500">Erro ao carregar detalhes da aula: {error}</div>
      )}
    </div>
  );
};

export default Catalog;

