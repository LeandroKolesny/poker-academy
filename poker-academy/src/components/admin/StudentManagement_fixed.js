// src/components/admin/StudentManagement.js
import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlus, faEdit, faTrash, faSpinner, faSort, faSortUp, faSortDown } from '@fortawesome/free-solid-svg-icons';
import { userService } from '../../services/api';
import appConfig from '../../config/config';

const StudentManagement = () => {
  const [students, setStudents] = useState([]);
  const [particoes, setParticoes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [formError, setFormError] = useState(null);

  const [showForm, setShowForm] = useState(false);
  const [currentStudent, setCurrentStudent] = useState(null); // Para identificar se é edição
  const [searchTerm, setSearchTerm] = useState('');

  // Estado para ordenação
  const [sortField, setSortField] = useState(null);
  const [sortDirection, setSortDirection] = useState('asc'); // 'asc' ou 'desc'

  // Estado inicial do formulário
  const initialFormData = {
    name: '', // Nome real do usuário
    username: '', // Nome de usuário único
    email: '',
    password: '',
    particao_id: '', // ID da partição selecionada
  };
  const [formData, setFormData] = useState(initialFormData);

  // Buscar alunos da API
  const fetchStudents = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await userService.getAll();
      const data = response.data || response; // Compatibilidade com nova estrutura
      console.log("📊 Dados dos alunos:", data); // Debug
      setStudents(Array.isArray(data) ? data : []);
    } catch (e) {
      console.error("Erro ao buscar alunos:", e);
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  // Buscar partições da API
  const fetchParticoes = async () => {
    try {
      const response = await fetch(`${appConfig.API_BASE_URL}${appConfig.API_ENDPOINTS.PARTICOES}`);
      if (response.ok) {
        const data = await response.json();
        console.log("Partições carregadas:", data); // Debug
        setParticoes(data);

        // Se não há partição selecionada e há partições disponíveis, selecionar a primeira
        if (data.length > 0 && !formData.particao_id) {
          console.log("Selecionando partição padrão:", data[0].id); // Debug
          setFormData(prev => ({ ...prev, particao_id: data[0].id.toString() }));
        }
      } else {
        console.error("Erro ao buscar partições - Status:", response.status);
      }
    } catch (e) {
      console.error("Erro ao buscar partições:", e);
    }
  };

  useEffect(() => {
    fetchStudents();
    fetchParticoes();
  }, []);

