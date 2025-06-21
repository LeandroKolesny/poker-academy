import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';

const SessionAlert = () => {
  const { error, setError } = useAuth();
  const [showAlert, setShowAlert] = useState(false);

  useEffect(() => {
    if (error && error.includes('expirada')) {
      setShowAlert(true);
      
      // Auto-hide após 5 segundos
      const timer = setTimeout(() => {
        setShowAlert(false);
        setError('');
      }, 5000);

      return () => clearTimeout(timer);
    }
  }, [error, setError]);

  if (!showAlert || !error) return null;

  return (
    <div className="fixed top-4 right-4 z-50 max-w-sm">
      <div className="bg-red-500 text-white px-4 py-3 rounded-lg shadow-lg flex items-center justify-between">
        <div className="flex items-center">
          <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
          <span className="text-sm font-medium">{error}</span>
        </div>
        <button
          onClick={() => {
            setShowAlert(false);
            setError('');
          }}
          className="ml-2 text-white hover:text-gray-200"
        >
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
          </svg>
        </button>
      </div>
    </div>
  );
};

export default SessionAlert;
