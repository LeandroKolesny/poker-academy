// src/App.js
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Login from './components/auth/Login';
import ForgotPassword from './components/auth/ForgotPassword';
import ResetPassword from './components/auth/ResetPassword';
import AdminPanel from './components/admin/AdminPanel';
import StudentPanel from './components/student/StudentPanel';
import Loading from './components/shared/Loading';
import SessionAlert from './components/common/SessionAlert';

// Componente para rotas protegidas
const ProtectedRoute = ({ children, requiredRole = null }) => {
  const { isAuthenticated, user, loading } = useAuth();
  
  // Mostrar loading enquanto verifica autenticação
  if (loading) {
    return <Loading show={true} />;
  }
  
  // Verificar autenticação
  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }
  
  // Verificar papel/tipo de usuário se necessário
  if (requiredRole && user.type !== requiredRole) {
    return <Navigate to={`/${user.type}`} />;
  }
  
  return children;
};

// Componente para redirecionar usuários autenticados
const AuthenticatedRedirect = () => {
  const { isAuthenticated, user, loading } = useAuth();

  if (loading) {
    return <Loading show={true} />;
  }

  if (isAuthenticated && user) {
    return <Navigate to={`/${user.type}`} />;
  }

  return <Navigate to="/login" />;
};

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <SessionAlert />
        <Routes>
          {/* Rotas de autenticação */}
          <Route path="/login" element={<Login />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route path="/reset-password" element={<ResetPassword />} />

          {/* Rotas do administrador */}
          <Route path="/admin/*" element={
            <ProtectedRoute requiredRole="admin">
              <AdminPanel />
            </ProtectedRoute>
          } />

          {/* Rotas do aluno */}
          <Route path="/student/*" element={
            <ProtectedRoute requiredRole="student">
              <StudentPanel />
            </ProtectedRoute>
          } />

          {/* Redirecionamento da raiz */}
          <Route path="/" element={<AuthenticatedRedirect />} />

          {/* Rota para qualquer outro caminho */}
          <Route path="*" element={<Navigate to="/login" />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
