// src/components/admin/AdminPanel.js
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from '../shared/Sidebar';
import StudentManagement from './StudentManagement';
import InstructorManagement from './InstructorManagement';
import ClassManagement from './ClassManagement';
import Analytics from './Analytics';
import AdminStudentGraphs from './AdminStudentGraphs';
import AdminMonthlyDatabase from './AdminMonthlyDatabase';
import AdminLeakManagement from './AdminLeakManagement';
import ChangePassword from '../student/ChangePassword'; // Reutilizar componente do student

const AdminPanel = () => {
  return (
    <div className="flex h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      <Sidebar type="admin" />
      <main className="flex-1 md:ml-64 p-4 md:p-8 overflow-y-auto pt-16 md:pt-8">
        <div className="max-w-7xl mx-auto">
          <Routes>
            {/* Rota padrão para /admin - renderiza Analytics */}
            <Route index element={<Navigate to="/admin/analytics" replace />} />
            <Route path="students" element={<StudentManagement />} />
            <Route path="instructors" element={<InstructorManagement />} />
            <Route path="classes" element={<ClassManagement />} />
            <Route path="analytics" element={<Analytics />} />
            <Route path="student-graphs" element={<AdminStudentGraphs />} />
            <Route path="monthly-database" element={<AdminMonthlyDatabase />} />
            <Route path="leak-management" element={<AdminLeakManagement />} />
            <Route path="change-password" element={<ChangePassword />} />
            {/* Fallback para qualquer outra sub-rota não reconhecida em /admin/* */}
            <Route path="*" element={<Navigate to="/admin/analytics" replace />} />
          </Routes>
        </div>
      </main>
    </div>
  );
};

export default AdminPanel;
