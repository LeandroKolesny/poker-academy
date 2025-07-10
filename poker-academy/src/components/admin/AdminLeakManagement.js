import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch, faUsers, faUpload, faCalendarAlt, faImage, faEye } from '@fortawesome/free-solid-svg-icons';
import api from '../../services/api';
import Loading from '../shared/Loading';

const AdminLeakManagement = () => {
    const [partitions, setPartitions] = useState([]);
    const [selectedStudent, setSelectedStudent] = useState(null);
    const [studentLeaks, setStudentLeaks] = useState({});
    const [loading, setLoading] = useState(true);
    const [loadingLeaks, setLoadingLeaks] = useState(false);
    const [uploading, setUploading] = useState(false);
    const [uploadingMonth, setUploadingMonth] = useState(null);
    const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());

    const months = [
        { key: 'jan', name: 'Janeiro' },
        { key: 'fev', name: 'Fevereiro' },
        { key: 'mar', name: 'Março' },
        { key: 'abr', name: 'Abril' },
        { key: 'mai', name: 'Maio' },
        { key: 'jun', name: 'Junho' },
        { key: 'jul', name: 'Julho' },
        { key: 'ago', name: 'Agosto' },
        { key: 'set', name: 'Setembro' },
        { key: 'out', name: 'Outubro' },
        { key: 'nov', name: 'Novembro' },
        { key: 'dez', name: 'Dezembro' }
    ];

    useEffect(() => {
        fetchPartitions();
    }, []);

    useEffect(() => {
        if (selectedStudent) {
            fetchStudentLeaks();
        }
    }, [selectedStudent, selectedYear]);

    const fetchPartitions = async () => {
        try {
            setLoading(true);
            const response = await api.get('/admin/students-by-partition');
            console.log('📊 Resposta da API:', response.data);

            if (response.data.success && response.data.partitions) {
                setPartitions(response.data.partitions);
            } else if (response.data.error) {
                console.error('❌ Erro da API:', response.data.error);
                alert(`Erro: ${response.data.error}`);
                setPartitions([]);
            } else {
                console.error('❌ Resposta inesperada:', response.data);
                alert('Resposta inesperada da API');
                setPartitions([]);
            }
        } catch (error) {
            console.error('❌ Erro ao buscar partições:', error);
            console.error('❌ Detalhes do erro:', error.response?.data);
            alert(`Erro ao carregar partições: ${error.response?.data?.error || error.message}`);
            setPartitions([]);
        } finally {
            setLoading(false);
        }
    };

    const fetchStudentLeaks = async () => {
        if (!selectedStudent) return;
        
        try {
            setLoadingLeaks(true);
            const response = await api.get(`/admin/student/${selectedStudent.id}/leaks?year=${selectedYear}`);
            setStudentLeaks(response.data.leaks || {});
        } catch (error) {
            console.error('Erro ao buscar leaks do aluno:', error);
            alert('Erro ao carregar análises do aluno');
        } finally {
            setLoadingLeaks(false);
        }
    };

    const handleStudentSelect = (student) => {
        setSelectedStudent(student);
        setStudentLeaks({});
    };

    const handleFileUpload = async (month, file) => {
        if (!file || !selectedStudent) return;

        // Validar tipo de arquivo
        const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/webp'];
        if (!allowedTypes.includes(file.type)) {
            alert('Tipo de arquivo não permitido. Use PNG, JPG, GIF ou WebP.');
            return;
        }

        // Validar tamanho (10MB)
        if (file.size > 10 * 1024 * 1024) {
            alert('Arquivo muito grande. Máximo 10MB.');
            return;
        }

        try {
            setUploading(true);
            setUploadingMonth(month);

            const formData = new FormData();
            formData.append('file', file);
            formData.append('month', month);
            formData.append('year', selectedYear);

            const response = await api.post(`/admin/student/${selectedStudent.id}/leaks/upload`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });

            if (response.data.success) {
                alert('Análise de leak enviada com sucesso!');
                fetchStudentLeaks(); // Recarregar análises
            }
        } catch (error) {
            console.error('Erro no upload:', error);
            alert(error.response?.data?.error || 'Erro ao enviar análise');
        } finally {
            setUploading(false);
            setUploadingMonth(null);
        }
    };

    const handleFileSelect = (month, event) => {
        const file = event.target.files[0];
        if (file) {
            handleFileUpload(month, file);
        }
        // Limpar o input para permitir reenvio do mesmo arquivo
        event.target.value = '';
    };

    if (loading) {
        return <Loading />;
    }

    return (
        <div className="admin-leak-management">
            <div className="page-header">
                <h2>
                    <FontAwesomeIcon icon={faSearch} className="me-2" />
                    Gerenciar Caça Leaks
                </h2>
                <p className="text-muted">
                    Faça upload das análises mensais de leaks para os alunos
                </p>
            </div>

            <div className="row">
                {/* Lista de Partições e Alunos */}
                <div className="col-md-4">
                    <div className="card">
                        <div className="card-header">
                            <h6 className="mb-0">
                                <FontAwesomeIcon icon={faUsers} className="me-2" />
                                Alunos por Partição
                            </h6>
                        </div>
                        <div className="card-body p-0">
                            {partitions.map(partition => (
                                <div key={partition.id} className="partition-group">
                                    <div className="partition-header p-3 bg-light border-bottom">
                                        <h6 className="mb-0 text-primary">{partition.nome}</h6>
                                        <small className="text-muted">{partition.students.length} alunos</small>
                                    </div>
                                    <div className="students-list">
                                        {partition.students.map(student => (
                                            <button
                                                key={student.id}
                                                className={`btn btn-link text-start w-100 p-3 border-bottom ${
                                                    selectedStudent?.id === student.id ? 'bg-primary text-white' : ''
                                                }`}
                                                onClick={() => handleStudentSelect(student)}
                                            >
                                                <div className="d-flex justify-content-between align-items-center">
                                                    <div>
                                                        <div className="fw-bold">{student.name}</div>
                                                        <small className={selectedStudent?.id === student.id ? 'text-white-50' : 'text-muted'}>
                                                            {student.email}
                                                        </small>
                                                    </div>
                                                    <FontAwesomeIcon icon={faEye} />
                                                </div>
                                            </button>
                                        ))}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Análises do Aluno Selecionado */}
                <div className="col-md-8">
                    {selectedStudent ? (
                        <div className="student-leaks">
                            <div className="card">
                                <div className="card-header">
                                    <div className="d-flex justify-content-between align-items-center">
                                        <div>
                                            <h6 className="mb-0">Análises de {selectedStudent.name}</h6>
                                            <small className="text-muted">{selectedStudent.email}</small>
                                        </div>
                                        <div className="year-selector">
                                            <label className="form-label me-2">
                                                <FontAwesomeIcon icon={faCalendarAlt} className="me-1" />
                                                Ano:
                                            </label>
                                            <select 
                                                className="form-select w-auto d-inline-block"
                                                value={selectedYear}
                                                onChange={(e) => setSelectedYear(parseInt(e.target.value))}
                                            >
                                                {[2024, 2025, 2026].map(year => (
                                                    <option key={year} value={year}>{year}</option>
                                                ))}
                                            </select>
                                        </div>
                                    </div>
                                </div>
                                <div className="card-body">
                                    {loadingLeaks ? (
                                        <div className="text-center py-4">
                                            <div className="spinner-border" role="status">
                                                <span className="visually-hidden">Carregando...</span>
                                            </div>
                                        </div>
                                    ) : (
                                        <div className="row">
                                            {months.map(month => (
                                                <div key={month.key} className="col-md-6 col-lg-4 mb-3">
                                                    <div className="card h-100">
                                                        <div className="card-header py-2">
                                                            <div className="d-flex justify-content-between align-items-center">
                                                                <small className="fw-bold">{month.name}</small>
                                                                {studentLeaks[month.key] && (
                                                                    <span className="badge bg-success">
                                                                        <FontAwesomeIcon icon={faImage} />
                                                                    </span>
                                                                )}
                                                            </div>
                                                        </div>
                                                        <div className="card-body p-2">
                                                            {studentLeaks[month.key] ? (
                                                                <div className="leak-preview">
                                                                    <img 
                                                                        src={`${process.env.REACT_APP_API_URL || 'http://localhost:5000'}${studentLeaks[month.key].image_url}`}
                                                                        alt={`Análise ${month.name}`}
                                                                        className="img-fluid rounded mb-2"
                                                                        style={{ maxHeight: '100px', width: '100%', objectFit: 'contain' }}
                                                                    />
                                                                    <small className="text-muted d-block">
                                                                        {new Date(studentLeaks[month.key].created_at).toLocaleDateString('pt-BR')}
                                                                    </small>
                                                                </div>
                                                            ) : (
                                                                <div className="no-leak text-center py-2">
                                                                    <FontAwesomeIcon 
                                                                        icon={faSearch} 
                                                                        className="text-muted mb-2" 
                                                                    />
                                                                    <small className="text-muted d-block mb-2">
                                                                        Não analisado
                                                                    </small>
                                                                </div>
                                                            )}
                                                            
                                                            {/* Botão de Upload */}
                                                            <div className="upload-button mt-2">
                                                                <input
                                                                    type="file"
                                                                    id={`leak-file-${month.key}`}
                                                                    accept="image/*"
                                                                    onChange={(e) => handleFileSelect(month.key, e)}
                                                                    style={{ display: 'none' }}
                                                                    disabled={uploading}
                                                                />
                                                                <label 
                                                                    htmlFor={`leak-file-${month.key}`}
                                                                    className={`btn btn-sm ${studentLeaks[month.key] ? 'btn-outline-primary' : 'btn-primary'} w-100 ${uploading ? 'disabled' : ''}`}
                                                                >
                                                                    {uploadingMonth === month.key ? (
                                                                        <>
                                                                            <div className="spinner-border spinner-border-sm me-1" role="status">
                                                                                <span className="visually-hidden">Enviando...</span>
                                                                            </div>
                                                                            Enviando...
                                                                        </>
                                                                    ) : (
                                                                        <>
                                                                            <FontAwesomeIcon icon={faUpload} className="me-1" />
                                                                            {studentLeaks[month.key] ? 'Substituir' : 'Enviar'}
                                                                        </>
                                                                    )}
                                                                </label>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            </div>

                            {/* Estatísticas */}
                            <div className="card mt-3">
                                <div className="card-header">
                                    <h6 className="mb-0">📊 Progresso das Análises {selectedYear}</h6>
                                </div>
                                <div className="card-body">
                                    <div className="row text-center">
                                        <div className="col-md-4">
                                            <h5 className="text-success">{Object.keys(studentLeaks).length}</h5>
                                            <small className="text-muted">Análises Feitas</small>
                                        </div>
                                        <div className="col-md-4">
                                            <h5 className="text-warning">{12 - Object.keys(studentLeaks).length}</h5>
                                            <small className="text-muted">Pendentes</small>
                                        </div>
                                        <div className="col-md-4">
                                            <h5 className="text-info">
                                                {Math.round((Object.keys(studentLeaks).length / 12) * 100)}%
                                            </h5>
                                            <small className="text-muted">Completo</small>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    ) : (
                        <div className="card">
                            <div className="card-body text-center py-5">
                                <FontAwesomeIcon icon={faUsers} size="3x" className="text-muted mb-3" />
                                <h5 className="text-muted">Selecione um aluno</h5>
                                <p className="text-muted">
                                    Escolha um aluno da lista ao lado para gerenciar suas análises de leaks
                                </p>
                            </div>
                        </div>
                    )}
                </div>
            </div>

            {/* Informações */}
            <div className="alert alert-info mt-4">
                <h6>📋 Instruções para Análises:</h6>
                <ul className="mb-0">
                    <li>Formatos aceitos: PNG, JPG, GIF, WebP</li>
                    <li>Tamanho máximo: 10MB por arquivo</li>
                    <li>Inclua stats, observações e pontos de melhoria</li>
                    <li>As análises ficam disponíveis imediatamente para o aluno</li>
                </ul>
            </div>
        </div>
    );
};

export default AdminLeakManagement;
