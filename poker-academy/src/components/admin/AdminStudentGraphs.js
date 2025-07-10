import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChartLine, faUsers, faEye, faCalendarAlt, faImage } from '@fortawesome/free-solid-svg-icons';
import api from '../../services/api';
import Loading from '../shared/Loading';

const AdminStudentGraphs = () => {
    const [partitions, setPartitions] = useState([]);
    const [selectedStudent, setSelectedStudent] = useState(null);
    const [studentGraphs, setStudentGraphs] = useState({});
    const [loading, setLoading] = useState(true);
    const [loadingGraphs, setLoadingGraphs] = useState(false);
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
            fetchStudentGraphs();
        }
    }, [selectedStudent, selectedYear]);

    const fetchPartitions = async () => {
        try {
            setLoading(true);
            const response = await api.get('/admin/students-by-partition');
            setPartitions(response.data.partitions || []);
        } catch (error) {
            console.error('Erro ao buscar partições:', error);
            alert('Erro ao carregar partições');
        } finally {
            setLoading(false);
        }
    };

    const fetchStudentGraphs = async () => {
        if (!selectedStudent) return;
        
        try {
            setLoadingGraphs(true);
            const response = await api.get(`/admin/student/${selectedStudent.id}/graphs?year=${selectedYear}`);
            setStudentGraphs(response.data.graphs || {});
        } catch (error) {
            console.error('Erro ao buscar gráficos do aluno:', error);
            alert('Erro ao carregar gráficos do aluno');
        } finally {
            setLoadingGraphs(false);
        }
    };

    const handleStudentSelect = (student) => {
        setSelectedStudent(student);
        setStudentGraphs({});
    };

    if (loading) {
        return <Loading />;
    }

    return (
        <div className="admin-student-graphs">
            <div className="page-header">
                <h2>
                    <FontAwesomeIcon icon={faChartLine} className="me-2" />
                    Gráficos dos Alunos
                </h2>
                <p className="text-muted">
                    Visualize os gráficos mensais enviados pelos alunos organizados por partição
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

                {/* Gráficos do Aluno Selecionado */}
                <div className="col-md-8">
                    {selectedStudent ? (
                        <div className="student-graphs">
                            <div className="card">
                                <div className="card-header">
                                    <div className="d-flex justify-content-between align-items-center">
                                        <div>
                                            <h6 className="mb-0">Gráficos de {selectedStudent.name}</h6>
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
                                    {loadingGraphs ? (
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
                                                                {studentGraphs[month.key] && (
                                                                    <span className="badge bg-success">
                                                                        <FontAwesomeIcon icon={faImage} />
                                                                    </span>
                                                                )}
                                                            </div>
                                                        </div>
                                                        <div className="card-body p-2">
                                                            {studentGraphs[month.key] ? (
                                                                <div className="graph-preview">
                                                                    <img 
                                                                        src={`${process.env.REACT_APP_API_URL || 'http://localhost:5000'}/api${studentGraphs[month.key].image_url}`}
                                                                        alt={`Gráfico ${month.name}`}
                                                                        className="img-fluid rounded"
                                                                        style={{ maxHeight: '120px', width: '100%', objectFit: 'contain' }}
                                                                    />
                                                                    <small className="text-muted d-block mt-1">
                                                                        {new Date(studentGraphs[month.key].created_at).toLocaleDateString('pt-BR')}
                                                                    </small>
                                                                </div>
                                                            ) : (
                                                                <div className="no-graph text-center py-3">
                                                                    <FontAwesomeIcon 
                                                                        icon={faImage} 
                                                                        className="text-muted mb-2" 
                                                                    />
                                                                    <small className="text-muted d-block">
                                                                        Não enviado
                                                                    </small>
                                                                </div>
                                                            )}
                                                        </div>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            </div>

                            {/* Estatísticas */}
                            {Object.keys(studentGraphs).length > 0 && (
                                <div className="card mt-3">
                                    <div className="card-header">
                                        <h6 className="mb-0">📊 Estatísticas {selectedYear}</h6>
                                    </div>
                                    <div className="card-body">
                                        <div className="row text-center">
                                            <div className="col-md-4">
                                                <h5 className="text-success">{Object.keys(studentGraphs).length}</h5>
                                                <small className="text-muted">Gráficos Enviados</small>
                                            </div>
                                            <div className="col-md-4">
                                                <h5 className="text-warning">{12 - Object.keys(studentGraphs).length}</h5>
                                                <small className="text-muted">Pendentes</small>
                                            </div>
                                            <div className="col-md-4">
                                                <h5 className="text-info">
                                                    {Math.round((Object.keys(studentGraphs).length / 12) * 100)}%
                                                </h5>
                                                <small className="text-muted">Progresso</small>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    ) : (
                        <div className="card">
                            <div className="card-body text-center py-5">
                                <FontAwesomeIcon icon={faUsers} size="3x" className="text-muted mb-3" />
                                <h5 className="text-muted">Selecione um aluno</h5>
                                <p className="text-muted">
                                    Escolha um aluno da lista ao lado para visualizar seus gráficos mensais
                                </p>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default AdminStudentGraphs;
