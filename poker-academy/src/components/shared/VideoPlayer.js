import React, { useState, useRef, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlay } from '@fortawesome/free-solid-svg-icons';
import { classService } from '../../services/api';
import { getToken } from '../../services/api';
import appConfig from '../../config/config';
import './VideoPlayer.css';

const VideoPlayer = ({ classData, onViewRegistered }) => {
  console.log('🎬 VideoPlayer: Iniciando com classData:', classData);

  // Extrair dados corretos - verificar se está aninhado em .data
  const actualClassData = classData?.data || classData;
  console.log('🎬 VideoPlayer: classData original:', classData);
  console.log('🎬 VideoPlayer: actualClassData:', actualClassData);
  console.log('🎬 VideoPlayer: actualClassData.instructor:', actualClassData?.instructor);
  console.log('🎬 VideoPlayer: actualClassData.category:', actualClassData?.category);
  console.log('🎬 VideoPlayer: actualClassData.date:', actualClassData?.date);
  console.log('🎬 VideoPlayer: actualClassData.date:', actualClassData?.date);

  const [isWatching, setIsWatching] = useState(false);
  const [viewRegistered, setViewRegistered] = useState(false);
  const [progress, setProgress] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isMobile, setIsMobile] = useState(false);
  const videoRef = useRef(null);
  const hasResumedRef = useRef(false); // Flag para evitar retomar múltiplas vezes
  const lastSaveTimeRef = useRef(0); // Controlar quando foi o último save

  // Detectar se é mobile
  useEffect(() => {
    const checkIsMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };

    checkIsMobile();
    window.addEventListener('resize', checkIsMobile);

    return () => window.removeEventListener('resize', checkIsMobile);
  }, []);

  // Carregar progresso da aula ao montar o componente
  useEffect(() => {
    console.log('🎬 VideoPlayer: useEffect loadProgress iniciado');
    console.log('🎬 VideoPlayer: actualClassData.id:', actualClassData?.id);

    // Resetar flags quando a aula muda
    hasResumedRef.current = false;
    lastSaveTimeRef.current = 0;

    const loadProgress = async () => {
      try {
        console.log('🎬 VideoPlayer: Carregando progresso para aula ID:', actualClassData.id);
        const progressData = await classService.getProgress(actualClassData.id);
        console.log('🎬 VideoPlayer: Progresso carregado (raw):', progressData);

        // Extrair dados corretos - a API retorna { data: {...} }
        const actualProgress = progressData?.data || progressData;
        console.log('🎬 VideoPlayer: Progresso extraído:', actualProgress);
        console.log('🎬 VideoPlayer: current_time:', actualProgress?.current_time);

        setProgress(actualProgress);
      } catch (error) {
        console.error('🎬 VideoPlayer: Erro ao carregar progresso:', error);
        setProgress({ progress: 0, watched: false, last_watched: null, current_time: 0 });
      } finally {
        console.log('🎬 VideoPlayer: Finalizando loading');
        setLoading(false);
      }
    };

    if (actualClassData?.id) {
      console.log('🎬 VideoPlayer: Iniciando loadProgress');
      loadProgress();
    } else {
      console.log('🎬 VideoPlayer: actualClassData.id não encontrado, finalizando loading');
      setLoading(false);
    }
  }, [actualClassData?.id]);

  // Quando o progresso é carregado, tentar retomar o vídeo
  useEffect(() => {
    console.log('🎬 VideoPlayer: useEffect progress mudou:', progress);

    if (videoRef.current && progress && progress.current_time && progress.current_time > 0 && !hasResumedRef.current) {
      console.log(`🎬 VideoPlayer: Tentando retomar de ${progress.current_time}s (progress effect)`);

      // Se o vídeo já está pronto, retomar imediatamente
      if (videoRef.current.readyState >= 2) { // HAVE_CURRENT_DATA ou superior
        videoRef.current.currentTime = progress.current_time;
        hasResumedRef.current = true;
        console.log(`✅ Retomado imediatamente em ${progress.current_time}s`);
      }
    }
  }, [progress]);

  // Função para registrar visualização
  const registerView = async () => {
    if (viewRegistered) return; // Evitar registrar múltiplas vezes

    try {
      console.log('🎬 VideoPlayer: Registrando view para ID:', actualClassData?.id);
      const response = await classService.registerView(actualClassData.id);
      setViewRegistered(true);

      if (onViewRegistered) {
        onViewRegistered(response.total_views);
      }

      console.log('🎬 VideoPlayer: Visualização registrada:', response);
    } catch (error) {
      console.error('🎬 VideoPlayer: Erro ao registrar visualização:', error);
    }
  };

  // Função para salvar progresso do vídeo
  const saveProgress = async (currentTime, duration) => {
    if (!duration || duration === 0) return;

    const progressPercent = Math.round((currentTime / duration) * 100);
    const watched = progressPercent >= 90; // Considera assistido se passou de 90%

    try {
      console.log('🎬 VideoPlayer: Salvando progresso para ID:', actualClassData?.id);
      await classService.updateProgress(actualClassData.id, {
        progress: progressPercent,
        watched: watched,
        current_time: currentTime
      });

      setProgress(prev => ({
        ...prev,
        progress: progressPercent,
        watched: watched,
        current_time: currentTime
      }));

      console.log(`Progresso salvo: ${progressPercent}% (${currentTime}s)`);
    } catch (error) {
      console.error('Erro ao salvar progresso:', error);
    }
  };

  // Função para iniciar assistir
  const handleStartWatching = () => {
    console.log('🎬 VideoPlayer: handleStartWatching chamado');
    console.log('🎬 VideoPlayer: actualClassData.video_path:', actualClassData?.video_path);
    setIsWatching(true);
    registerView();
  };

  // Função para quando o vídeo carrega
  const handleVideoLoaded = () => {
    // Evitar retomar múltiplas vezes
    if (hasResumedRef.current) {
      console.log(`🎬 VideoPlayer: handleVideoLoaded - já foi retomado, ignorando`);
      return;
    }

    console.log(`🎬 VideoPlayer: handleVideoLoaded chamado`);
    console.log(`🎬 VideoPlayer: progress:`, progress);
    console.log(`🎬 VideoPlayer: progress?.current_time:`, progress?.current_time);

    if (videoRef.current && progress && progress.current_time && progress.current_time > 0) {
      // Retomar de onde parou
      console.log(`🎬 VideoPlayer: Tentando retomar de ${progress.current_time}s`);
      console.log(`🎬 VideoPlayer: videoRef.current.duration: ${videoRef.current.duration}`);

      // Usar setTimeout para garantir que o vídeo está pronto
      setTimeout(() => {
        if (videoRef.current && !hasResumedRef.current) {
          videoRef.current.currentTime = progress.current_time;
          hasResumedRef.current = true; // Marcar como já retomado
          console.log(`✅ Retomando vídeo em ${progress.current_time}s (${progress.progress}%)`);
        }
      }, 100);
    } else {
      console.log(`🎬 VideoPlayer: Não há progresso para retomar`);
      hasResumedRef.current = true; // Marcar como já processado mesmo sem retomar
    }
  };

  // Função para salvar progresso periodicamente
  const handleTimeUpdate = () => {
    if (videoRef.current) {
      const currentTime = videoRef.current.currentTime;
      const duration = videoRef.current.duration;
      const now = Date.now();

      // Salvar progresso apenas a cada 5 segundos (5000ms) para evitar muitas requisições
      if (now - lastSaveTimeRef.current >= 5000) {
        saveProgress(currentTime, duration);
        lastSaveTimeRef.current = now;
      }
    }
  };

  // Função para salvar progresso quando pausar
  const handlePause = () => {
    if (videoRef.current) {
      const currentTime = videoRef.current.currentTime;
      const duration = videoRef.current.duration;
      saveProgress(currentTime, duration);
    }
  };

  // Renderizar player para vídeos locais
  if (!isWatching) {
    if (loading) {
      console.log('🎬 VideoPlayer: Renderizando loading...');
      return (
        <div className="my-4">
          <div className={`bg-gray-800 rounded-lg text-center ${isMobile ? 'p-4' : 'p-8'}`}>
            <div className={`animate-spin rounded-full border-b-2 border-poker-red mx-auto mb-4 loading-spinner ${isMobile ? 'h-10 w-10' : 'h-12 w-12'}`}></div>
            <p className={`text-gray-400 ${isMobile ? 'text-sm' : ''}`}>Carregando...</p>
          </div>
        </div>
      );
    }

    console.log('🎬 VideoPlayer: Renderizando botão de play');

    return (
      <div className="my-4">
        <div className={`bg-gray-800 rounded-lg text-center ${isMobile ? 'p-4' : 'p-6'}`}>
          {/* Barra de progresso se existir */}
          {progress && progress.progress > 0 && (
            <div className="mb-4">
              <div className="flex justify-between text-xs sm:text-sm text-gray-400 mb-2">
                <span>Progresso da aula</span>
                <span className="font-medium">{progress.progress}%</span>
              </div>
              <div className={`w-full bg-gray-700 rounded-full ${isMobile ? 'progress-bar-mobile' : 'h-2 sm:h-3'}`}>
                <div
                  className={`bg-poker-red rounded-full transition-all duration-300 ${isMobile ? 'progress-bar-mobile' : 'h-2 sm:h-3'}`}
                  style={{ width: `${progress.progress}%` }}
                ></div>
              </div>
            </div>
          )}

          {/* Botão principal - único elemento clicável */}
          <button
            onClick={handleStartWatching}
            className={`bg-poker-red hover:bg-red-700 text-white font-bold rounded-lg transition-colors shadow-lg ${
              isMobile
                ? 'py-4 px-6 text-base w-full'
                : 'py-4 px-8 text-lg w-full sm:w-auto'
            }`}
          >
            <FontAwesomeIcon icon={faPlay} className="mr-3 text-xl" />
            {progress && progress.progress > 0 ? 'Continuar Aula' : 'Assistir Aula'}
          </button>

          {/* Informação adicional - apenas visual */}
          {progress && progress.progress > 0 && (
            <p className="text-gray-400 text-xs sm:text-sm mt-3">
              Você parou em {progress.progress}% da aula
            </p>
          )}
        </div>
      </div>
    );
  }

  // Player para vídeos locais
  if (actualClassData?.video_path) {
    console.log('🎬 VideoPlayer: Renderizando player para vídeo local');
    console.log('🎬 VideoPlayer: video_path:', actualClassData.video_path);
    console.log('🎬 VideoPlayer: isWatching:', isWatching);

    // Usar rota com token para autenticação
    const token = getToken();
    const videoUrl = `${appConfig.API_BASE_URL}/videos/${actualClassData.video_path}?token=${token}`;
    console.log('🎬 VideoPlayer: URL do vídeo:', videoUrl);

    return (
      <div className="my-4">
        <div className={`bg-gray-900 rounded-lg video-player-container ${isMobile ? 'p-2' : 'p-3 md:p-4'}`}>
          <div className="mb-3 md:mb-4">
            <h4 className={`font-semibold text-white mb-2 leading-tight ${isMobile ? 'video-title-mobile' : 'text-sm sm:text-base md:text-lg'}`}>
              {actualClassData.name}
            </h4>
          </div>

          {/* Container responsivo para vídeo */}
          {isMobile ? (
            // Layout específico para mobile
            <div className="mb-3 md:mb-4">
              <div className="w-full bg-black rounded overflow-hidden" style={{ aspectRatio: '16/9' }}>
                <video
                  ref={videoRef}
                  controls
                  className="w-full h-full object-contain"
                  preload="metadata"
                  playsInline // Importante para iOS
                  webkit-playsinline="true" // Para compatibilidade com iOS mais antigos
                  controlsList="nodownload" // Remover opção de download no mobile
                  onCanPlay={handleVideoLoaded}
                  onTimeUpdate={handleTimeUpdate}
                  onPause={handlePause}
                  onEnded={() => saveProgress(videoRef.current?.duration || 0, videoRef.current?.duration || 0)}
                  style={{
                    maxHeight: '70vh',
                    width: '100%',
                    height: 'auto'
                  }}
                >
                  <source src={videoUrl} type="video/mp4" />
                  <source src={videoUrl} type="video/webm" />
                  <source src={videoUrl} type="video/ogg" />
                  Seu navegador não suporta o elemento de vídeo.
                </video>
              </div>
            </div>
          ) : (
            // Layout para desktop
            <div className="mb-3 md:mb-4">
              <div className="video-container">
                <div className="video-aspect-ratio">
                  <video
                    ref={videoRef}
                    controls
                    className="video-element video-transition"
                    preload="metadata"
                    onCanPlay={handleVideoLoaded}
                    onTimeUpdate={handleTimeUpdate}
                    onPause={handlePause}
                    onEnded={() => saveProgress(videoRef.current?.duration || 0, videoRef.current?.duration || 0)}
                  >
                    <source src={videoUrl} type="video/mp4" />
                    <source src={videoUrl} type="video/webm" />
                    <source src={videoUrl} type="video/ogg" />
                    Seu navegador não suporta o elemento de vídeo.
                  </video>
                </div>
              </div>
            </div>
          )}

          {/* Barra de progresso visual - responsiva */}
          {progress && progress.progress > 0 && (
            <div className="mb-3 md:mb-4">
              <div className="flex justify-between text-xs sm:text-sm text-gray-400 mb-1">
                <span>Progresso da aula</span>
                <span className="font-medium">{progress.progress}%</span>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-2 sm:h-3">
                <div
                  className="bg-poker-red h-2 sm:h-3 rounded-full transition-all duration-300"
                  style={{ width: `${progress.progress}%` }}
                ></div>
              </div>
            </div>
          )}

          {viewRegistered && (
            <div className="text-center bg-green-900 bg-opacity-50 p-2 sm:p-3 rounded">
              <p className="text-green-400 text-xs sm:text-sm">✓ Visualização registrada com sucesso!</p>
            </div>
          )}
        </div>
      </div>
    );
  }

  // Fallback se nenhum vídeo for encontrado
  console.log('🎬 VideoPlayer: Renderizando fallback - nenhum vídeo encontrado');
  console.log('🎬 VideoPlayer: classData completo:', classData);
  console.log('🎬 VideoPlayer: actualClassData completo:', actualClassData);

  return (
    <div className="my-4">
      <div className={`error-message ${isMobile ? 'p-4' : 'p-8'}`}>
        <p className={`text-gray-400 ${isMobile ? 'text-sm' : ''}`}>Nenhum vídeo disponível para esta aula</p>
        <p className={`text-gray-500 mt-2 ${isMobile ? 'text-xs' : 'text-sm'}`}>Entre em contato com o administrador</p>
      </div>
    </div>
  );
};

export default VideoPlayer;
