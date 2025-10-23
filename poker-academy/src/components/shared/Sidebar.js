// src/components/shared/Sidebar.js
import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faUsers, faVideo, faChartBar, faBook,
  faHeart, faList, faHistory, faSignOutAlt, faKey,
  faChartLine, faSearch, faImage, faBars, faTimes, faChalkboardTeacher, faDatabase
} from '@fortawesome/free-solid-svg-icons';
import { useAuth } from '../../context/AuthContext';
import DojoLogo from './DojoLogo';

const Sidebar = ({ type }) => {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isMobile, setIsMobile] = useState(false);

  // Detectar se é mobile
  useEffect(() => {
    const checkIsMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };

    checkIsMobile();
    window.addEventListener('resize', checkIsMobile);

    return () => window.removeEventListener('resize', checkIsMobile);
  }, []);

  // Fechar menu mobile quando navegar
  useEffect(() => {
    setIsMobileMenuOpen(false);
  }, [location.pathname]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const isActive = (path) => {
    return location.pathname === path;
  };

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };
  
  // Renderiza a sidebar do administrador
  const renderAdminSidebar = () => (
    <>
      <div className="header bg-gradient-to-b from-black to-gray-800 py-6 px-6">
        <div className="flex items-center space-x-3">
          <DojoLogo size={36} className="opacity-95" />
          <div>
            <h3 className="text-white font-bold text-lg">Painel Admin</h3>
            <p className="text-gray-300 text-xs">Gestão Completa</p>
          </div>
        </div>
      </div>
      <div className="px-4 py-2">
        <div
          className={`flex items-center px-4 py-3 rounded-modern cursor-pointer transition-all duration-200 ${
            isActive('/admin/students')
              ? 'bg-red-100 text-primary-red border-l-4 border-primary-red'
              : 'text-white hover:bg-gray-500 hover:text-red-200'
          }`}
          onClick={() => navigate('/admin/students')}
        >
          <FontAwesomeIcon icon={faUsers} className="mr-3 w-5 h-5" />
          <span className="font-medium">Gestão de Alunos</span>
        </div>
        <div
          className={`flex items-center px-4 py-3 rounded-modern cursor-pointer transition-all duration-200 ${
            isActive('/admin/instructors')
              ? 'bg-red-100 text-primary-red border-l-4 border-primary-red'
              : 'text-white hover:bg-gray-500 hover:text-red-200'
          }`}
          onClick={() => navigate('/admin/instructors')}
        >
          <FontAwesomeIcon icon={faChalkboardTeacher} className="mr-3 w-5 h-5" />
          <span className="font-medium">Gestão de Instrutores</span>
        </div>
        <div
          className={`flex items-center px-4 py-3 rounded-modern cursor-pointer transition-all duration-200 ${
            isActive('/admin/classes')
              ? 'bg-red-100 text-primary-red border-l-4 border-primary-red'
              : 'text-white hover:bg-gray-500 hover:text-red-200'
          }`}
          onClick={() => navigate('/admin/classes')}
        >
          <FontAwesomeIcon icon={faVideo} className="mr-3 w-5 h-5" />
          <span className="font-medium">Gestão de Aulas</span>
        </div>
        <div
          className={`flex items-center px-4 py-3 rounded-modern cursor-pointer transition-all duration-200 ${
            isActive('/admin/analytics')
              ? 'bg-red-100 text-primary-red border-l-4 border-primary-red'
              : 'text-white hover:bg-gray-500 hover:text-red-200'
          }`}
          onClick={() => navigate('/admin/analytics')}
        >
          <FontAwesomeIcon icon={faChartBar} className="mr-3 w-5 h-5" />
          <span className="font-medium">Analytics</span>
        </div>
        <div
          className={`flex items-center px-4 py-3 rounded-modern cursor-pointer transition-all duration-200 ${
            isActive('/admin/student-graphs')
              ? 'bg-red-100 text-primary-red border-l-4 border-primary-red'
              : 'text-white hover:bg-gray-500 hover:text-red-200'
          }`}
          onClick={() => navigate('/admin/student-graphs')}
        >
          <FontAwesomeIcon icon={faChartLine} className="mr-3 w-5 h-5" />
          <span className="font-medium">Gráficos dos Alunos</span>
        </div>
        <div
          className={`flex items-center px-4 py-3 rounded-modern cursor-pointer transition-all duration-200 ${
            isActive('/admin/monthly-database')
              ? 'bg-red-100 text-primary-red border-l-4 border-primary-red'
              : 'text-white hover:bg-gray-500 hover:text-red-200'
          }`}
          onClick={() => navigate('/admin/monthly-database')}
        >
          <FontAwesomeIcon icon={faDatabase} className="mr-3 w-5 h-5" />
          <span className="font-medium">Database Mensal</span>
        </div>
        <div
          className={`flex items-center px-4 py-3 rounded-modern cursor-pointer transition-all duration-200 ${
            isActive('/admin/leak-management')
              ? 'bg-red-100 text-primary-red border-l-4 border-primary-red'
              : 'text-white hover:bg-gray-500 hover:text-red-200'
          }`}
          onClick={() => navigate('/admin/leak-management')}
        >
          <FontAwesomeIcon icon={faSearch} className="mr-3 w-5 h-5" />
          <span className="font-medium">Caça Leaks</span>
        </div>
      </div>
    </>
  );
  
  // Renderiza a sidebar do aluno
  const renderStudentSidebar = () => (
    <>
      <div className="header bg-gradient-to-b from-black to-gray-800 py-6 px-6">
        <div className="flex items-center space-x-3">
          <DojoLogo size={36} className="opacity-95" />
          <div>
            <h3 className="text-white font-bold text-lg">Poker Academy</h3>
            <p className="text-gray-300 text-xs">Portal do Aluno</p>
          </div>
        </div>
      </div>
      <div className="px-4 py-2">
        <div
          className={`flex items-center px-4 py-3 rounded-modern cursor-pointer transition-all duration-200 ${
            isActive('/student/catalog')
              ? 'bg-red-100 text-primary-red border-l-4 border-primary-red'
              : 'text-white hover:bg-gray-500 hover:text-red-200'
          }`}
          onClick={() => navigate('/student/catalog')}
        >
          <FontAwesomeIcon icon={faBook} className="mr-3 w-5 h-5" />
          <span className="font-medium">Catálogo de Aulas</span>
        </div>
        <div
          className={`flex items-center px-4 py-3 rounded-modern cursor-pointer transition-all duration-200 ${
            isActive('/student/favorites')
              ? 'bg-red-100 text-primary-red border-l-4 border-primary-red'
              : 'text-white hover:bg-gray-500 hover:text-red-200'
          }`}
          onClick={() => navigate('/student/favorites')}
        >
          <FontAwesomeIcon icon={faHeart} className="mr-3 w-5 h-5" />
          <span className="font-medium">Favoritos</span>
        </div>
        {/* Playlists temporariamente oculto */}
        {/* <div
          className={`flex items-center px-4 py-3 rounded-modern cursor-pointer transition-all duration-200 ${
            isActive('/student/playlists')
              ? 'bg-sidebar-active text-primary-red border-l-4 border-primary-red'
              : 'text-gray-700 hover:bg-sidebar-hover hover:text-primary-red'
          }`}
          onClick={() => navigate('/student/playlists')}
        >
          <FontAwesomeIcon icon={faList} className="mr-3 w-5 h-5" />
          <span className="font-medium">Playlists</span>
        </div> */}
        <div
          className={`flex items-center px-4 py-3 rounded-modern cursor-pointer transition-all duration-200 ${
            isActive('/student/history')
              ? 'bg-red-100 text-primary-red border-l-4 border-primary-red'
              : 'text-white hover:bg-gray-500 hover:text-red-200'
          }`}
          onClick={() => navigate('/student/history')}
        >
          <FontAwesomeIcon icon={faHistory} className="mr-3 w-5 h-5" />
          <span className="font-medium">Histórico</span>
        </div>
        <div
          className={`flex items-center px-4 py-3 rounded-modern cursor-pointer transition-all duration-200 ${
            isActive('/student/monthly-graphs')
              ? 'bg-red-100 text-primary-red border-l-4 border-primary-red'
              : 'text-white hover:bg-gray-500 hover:text-red-200'
          }`}
          onClick={() => navigate('/student/monthly-graphs')}
        >
          <FontAwesomeIcon icon={faChartLine} className="mr-3 w-5 h-5" />
          <span className="font-medium">Gráficos Mensais</span>
        </div>
        <div
          className={`flex items-center px-4 py-3 rounded-modern cursor-pointer transition-all duration-200 ${
            isActive('/student/monthly-database')
              ? 'bg-red-100 text-primary-red border-l-4 border-primary-red'
              : 'text-white hover:bg-gray-500 hover:text-red-200'
          }`}
          onClick={() => navigate('/student/monthly-database')}
        >
          <FontAwesomeIcon icon={faDatabase} className="mr-3 w-5 h-5" />
          <span className="font-medium">Database Mensal</span>
        </div>
        <div
          className={`flex items-center px-4 py-3 rounded-modern cursor-pointer transition-all duration-200 ${
            isActive('/student/leak-hunting')
              ? 'bg-red-100 text-primary-red border-l-4 border-primary-red'
              : 'text-white hover:bg-gray-500 hover:text-red-200'
          }`}
          onClick={() => navigate('/student/leak-hunting')}
        >
          <FontAwesomeIcon icon={faSearch} className="mr-3 w-5 h-5" />
          <span className="font-medium">Caça Leaks</span>
        </div>
        <div
          className={`flex items-center px-4 py-3 rounded-modern cursor-pointer transition-all duration-200 ${
            isActive('/student/change-password')
              ? 'bg-red-100 text-primary-red border-l-4 border-primary-red'
              : 'text-white hover:bg-gray-500 hover:text-red-200'
          }`}
          onClick={() => navigate('/student/change-password')}
        >
          <FontAwesomeIcon icon={faKey} className="mr-3 w-5 h-5" />
          <span className="font-medium">Alterar Senha</span>
        </div>
      </div>
    </>
  );
  
  return (
    <>
      {/* Botão Hambúrguer Mobile */}
      {isMobile && (
        <button
          onClick={toggleMobileMenu}
          className="fixed top-4 left-4 z-50 bg-gray-600 text-white p-3 rounded-modern shadow-lg md:hidden"
        >
          <FontAwesomeIcon
            icon={isMobileMenuOpen ? faTimes : faBars}
            className="w-5 h-5"
          />
        </button>
      )}

      {/* Overlay para mobile */}
      {isMobile && isMobileMenuOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden"
          onClick={() => setIsMobileMenuOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div className={`
        bg-gray-600 h-screen flex flex-col shadow-modern-lg transition-transform duration-300 ease-in-out
        ${isMobile
          ? `fixed top-0 left-0 z-50 w-80 ${isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full'}`
          : 'w-64 relative'
        }
      `}>
        {type === 'admin' ? renderAdminSidebar() : renderStudentSidebar()}

        {/* Botão de logout (comum para ambos os tipos) */}
        <div className="mt-auto p-4">
          <div
            className="flex items-center px-4 py-3 rounded-modern cursor-pointer transition-all duration-200 text-white hover:bg-red-100 hover:text-primary-red border border-gray-500 hover:border-primary-red"
            onClick={handleLogout}
          >
            <FontAwesomeIcon icon={faSignOutAlt} className="mr-3 w-5 h-5" />
            <span className="font-medium">Sair</span>
          </div>
        </div>
      </div>
    </>
  );
};

export default Sidebar;
