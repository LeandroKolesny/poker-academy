// src/components/admin/AdminPanel.js
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from '../shared/Sidebar';
import StudentManagement from './StudentManagement';
import ClassManagement from './ClassManagement';
import Analytics from './Analytics';

const AdminPanel = () => {
  return (
    <div className="flex h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      <Sidebar type="admin" />
      <main className="flex-1 ml-64 p-8 overflow-y-auto">
        <div className="max-w-7xl mx-auto">
          <Routes>
            {/* Rota padrão para /admin - renderiza Analytics */}
            <Route index element={<Navigate to="analytics" replace />} />
            <Route path="students" element={<StudentManagement />} />
            <Route path="classes" element={<ClassManagement />} />
            <Route path="analytics" element={<Analytics />} />
            {/* Fallback para qualquer outra sub-rota não reconhecida em /admin/* */}
            <Route path="*" element={<Navigate to="analytics" replace />} />
          </Routes>
        </div>
      </main>
    </div>
  );
};

export default AdminPanel;
