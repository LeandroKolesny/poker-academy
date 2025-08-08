// src/components/shared/Sidebar.js
import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faUsers, faVideo, faChartBar, faBook,
  faHeart, faList, faHistory, faSignOutAlt, faKey,
  faChartLine, faSearch, faImage
} from '@fortawesome/free-solid-svg-icons';
import { useAuth } from '../../context/AuthContext';
import DojoLogo from './DojoLogo';

const Sidebar = ({ type }) => {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  
  const handleLogout = () => {
    logout();
    navigate('/login');
  };
  
  const isActive = (path) => {
    return location.pathname === path;
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
    <div className="bg-gray-600 w-64 h-screen flex flex-col shadow-modern-lg">
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
  );
};

export default Sidebar;
