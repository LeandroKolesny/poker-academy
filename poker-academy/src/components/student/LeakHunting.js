import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch, faImage, faCalendarAlt, faEye } from '@fortawesome/free-solid-svg-icons';
import api from '../../services/api';
import Loading from '../shared/Loading';

const LeakHunting = () => {
    const [leaks, setLeaks] = useState({});
    const [loading, setLoading] = useState(true);
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
        fetchLeaks();
    }, [selectedYear]);

    const fetchLeaks = async () => {
        try {
            setLoading(true);
            const response = await api.get(`/api/student/leaks?year=${selectedYear}`);
            setLeaks(response.data.leaks || {});
        } catch (error) {
            console.error('Erro ao buscar análises de leaks:', error);
            alert('Erro ao carregar análises de leaks');
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return <Loading />;
    }

    return (
        <div className="leak-hunting">
            <div className="page-header">
                <h2>
                    <FontAwesomeIcon icon={faSearch} className="me-2" />
                    Caça Leaks
                </h2>
                <p className="text-muted">
                    Visualize as análises mensais dos seus leaks feitas pelos instrutores
                </p>
            </div>

            {/* Seletor de Ano */}
            <div className="year-selector mb-4">
                <label className="form-label">
                    <FontAwesomeIcon icon={faCalendarAlt} className="me-2" />
                    Ano:
                </label>
                <select 
                    className="form-select w-auto d-inline-block ms-2"
                    value={selectedYear}
                    onChange={(e) => setSelectedYear(parseInt(e.target.value))}
                >
                    {[2024, 2025, 2026].map(year => (
                        <option key={year} value={year}>{year}</option>
                    ))}
                </select>
            </div>

            {/* Grid de Meses */}
            <div className="row">
                {months.map(month => (
                    <div key={month.key} className="col-md-6 col-lg-4 mb-4">
                        <div className="card h-100">
                            <div className="card-header d-flex justify-content-between align-items-center">
                                <h6 className="mb-0">{month.name} {selectedYear}</h6>
                                {leaks[month.key] ? (
                                    <span className="badge bg-success">
                                        <FontAwesomeIcon icon={faEye} className="me-1" />
                                        Disponível
                                    </span>
                                ) : (
                                    <span className="badge bg-secondary">
                                        Aguardando
                                    </span>
                                )}
                            </div>
                            <div className="card-body">
                                {leaks[month.key] ? (
                                    <div className="leak-analysis">
                                        <img 
                                            src={`${process.env.REACT_APP_API_URL || 'http://localhost:5000'}/api${leaks[month.key].image_url}`}
                                            alt={`Análise de Leaks ${month.name}`}
                                            className="img-fluid rounded mb-3"
                                            style={{ maxHeight: '200px', width: '100%', objectFit: 'contain' }}
                                        />
                                        <div className="analysis-info">
                                            <small className="text-muted d-block">
                                                <strong>Analisado por:</strong> {leaks[month.key].uploaded_by_name}
                                            </small>
                                            <small className="text-muted d-block">
                                                <strong>Data:</strong> {new Date(leaks[month.key].created_at).toLocaleDateString('pt-BR')}
                                            </small>
                                        </div>
                                    </div>
                                ) : (
                                    <div className="no-analysis text-center py-4">
                                        <FontAwesomeIcon 
                                            icon={faSearch} 
                                            size="3x" 
                                            className="text-muted mb-3" 
                                        />
                                        <p className="text-muted mb-0">
                                            Análise ainda não disponível
                                        </p>
                                        <small className="text-muted">
                                            Aguarde o instrutor fazer a análise dos seus leaks
                                        </small>
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {/* Informações */}
            <div className="alert alert-info mt-4">
                <h6>🔍 Sobre o Caça Leaks:</h6>
                <ul className="mb-0">
                    <li>As análises são feitas mensalmente pelos instrutores</li>
                    <li>Cada análise contém stats e observações sobre seu jogo</li>
                    <li>Use essas informações para identificar pontos de melhoria</li>
                    <li>As análises ficam disponíveis permanentemente para consulta</li>
                </ul>
            </div>

            {/* Estatísticas */}
            {Object.keys(leaks).length > 0 && (
                <div className="stats-summary mt-4">
                    <div className="card">
                        <div className="card-header">
                            <h6 className="mb-0">📊 Resumo do Ano {selectedYear}</h6>
                        </div>
                        <div className="card-body">
                            <div className="row text-center">
                                <div className="col-md-4">
                                    <div className="stat-item">
                                        <h4 className="text-success">{Object.keys(leaks).length}</h4>
                                        <small className="text-muted">Análises Recebidas</small>
                                    </div>
                                </div>
                                <div className="col-md-4">
                                    <div className="stat-item">
                                        <h4 className="text-primary">{12 - Object.keys(leaks).length}</h4>
                                        <small className="text-muted">Análises Pendentes</small>
                                    </div>
                                </div>
                                <div className="col-md-4">
                                    <div className="stat-item">
                                        <h4 className="text-info">
                                            {Math.round((Object.keys(leaks).length / 12) * 100)}%
                                        </h4>
                                        <small className="text-muted">Progresso Anual</small>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default LeakHunting;
