import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUpload, faImage, faCalendarAlt, faChartLine } from '@fortawesome/free-solid-svg-icons';
import api from '../../services/api';
import Loading from '../shared/Loading';

const MonthlyGraphs = () => {
    const [graphs, setGraphs] = useState({});
    const [loading, setLoading] = useState(true);
    const [uploading, setUploading] = useState(false);
    const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());
    const [uploadingMonth, setUploadingMonth] = useState(null);

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
        fetchGraphs();
    }, [selectedYear]);

    const fetchGraphs = async () => {
        try {
            setLoading(true);
            const response = await api.get(`/student/graphs?year=${selectedYear}`);
            setGraphs(response.data.graphs || {});
        } catch (error) {
            console.error('Erro ao buscar gráficos:', error);
            alert('Erro ao carregar gráficos');
        } finally {
            setLoading(false);
        }
    };

    const handleFileUpload = async (month, file) => {
        if (!file) return;

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

            const response = await api.post('/student/graphs/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });

            if (response.data.success) {
                alert('Gráfico enviado com sucesso!');
                fetchGraphs(); // Recarregar gráficos
            }
        } catch (error) {
            console.error('Erro no upload:', error);
            alert(error.response?.data?.error || 'Erro ao enviar gráfico');
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
        <div className="monthly-graphs">
            <div className="page-header">
                <h2>
                    <FontAwesomeIcon icon={faChartLine} className="me-2" />
                    Gráficos Mensais
                </h2>
                <p className="text-muted">
                    Faça upload dos seus gráficos de resultados mensais para acompanhar sua evolução
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
                                {graphs[month.key] && (
                                    <span className="badge bg-success">
                                        <FontAwesomeIcon icon={faImage} className="me-1" />
                                        Enviado
                                    </span>
                                )}
                            </div>
                            <div className="card-body">
                                {graphs[month.key] ? (
                                    <div className="graph-preview">
                                        <img 
                                            src={`${process.env.REACT_APP_API_URL || 'http://localhost:5000'}/api${graphs[month.key].image_url}`}
                                            alt={`Gráfico ${month.name}`}
                                            className="img-fluid rounded mb-3"
                                            style={{ maxHeight: '200px', width: '100%', objectFit: 'contain' }}
                                        />
                                        <small className="text-muted">
                                            Enviado em: {new Date(graphs[month.key].created_at).toLocaleDateString('pt-BR')}
                                        </small>
                                    </div>
                                ) : (
                                    <div className="upload-area text-center py-4">
                                        <FontAwesomeIcon 
                                            icon={faImage} 
                                            size="3x" 
                                            className="text-muted mb-3" 
                                        />
                                        <p className="text-muted mb-3">
                                            Nenhum gráfico enviado para este mês
                                        </p>
                                    </div>
                                )}
                                
                                {/* Botão de Upload */}
                                <div className="upload-button">
                                    <input
                                        type="file"
                                        id={`file-${month.key}`}
                                        accept="image/*"
                                        onChange={(e) => handleFileSelect(month.key, e)}
                                        style={{ display: 'none' }}
                                        disabled={uploading}
                                    />
                                    <label 
                                        htmlFor={`file-${month.key}`}
                                        className={`btn ${graphs[month.key] ? 'btn-outline-primary' : 'btn-primary'} w-100 ${uploading ? 'disabled' : ''}`}
                                    >
                                        {uploadingMonth === month.key ? (
                                            <>
                                                <div className="spinner-border spinner-border-sm me-2" role="status">
                                                    <span className="visually-hidden">Enviando...</span>
                                                </div>
                                                Enviando...
                                            </>
                                        ) : (
                                            <>
                                                <FontAwesomeIcon icon={faUpload} className="me-2" />
                                                {graphs[month.key] ? 'Substituir Gráfico' : 'Enviar Gráfico'}
                                            </>
                                        )}
                                    </label>
                                </div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {/* Informações */}
            <div className="alert alert-info mt-4">
                <h6>📋 Instruções:</h6>
                <ul className="mb-0">
                    <li>Formatos aceitos: PNG, JPG, GIF, WebP</li>
                    <li>Tamanho máximo: 10MB por arquivo</li>
                    <li>Você pode substituir gráficos já enviados</li>
                    <li>Os gráficos ficam organizados por mês e ano</li>
                </ul>
            </div>
        </div>
    );
};

export default MonthlyGraphs;
