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

        // Validar tamanho do arquivo (máximo 10MB)
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
            } else {
                alert('Erro ao enviar gráfico');
            }
        } catch (error) {
            console.error('Erro no upload:', error);
            alert(`Erro ao enviar gráfico: ${error.response?.data?.error || error.message}`);
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
        <div className="p-6 text-white min-h-screen">
            {/* Header */}
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-semibold text-red-400">Meus Gráficos Mensais</h2>
                <div className="flex items-center gap-4">
                    <label className="text-sm font-medium text-gray-300">Ano:</label>
                    <select 
                        className="bg-gray-700 text-white px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-red-400"
                        value={selectedYear}
                        onChange={(e) => setSelectedYear(parseInt(e.target.value))}
                    >
                        <option value="2024">2024</option>
                        <option value="2025">2025</option>
                        <option value="2026">2026</option>
                    </select>
                </div>
            </div>

            {/* Tabela de Gráficos */}
            <div className="bg-gray-700 rounded-lg overflow-x-auto shadow-lg">
                <table className="w-full min-w-full">
                    <thead className="bg-gray-500">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Mês</th>
                            <th className="px-6 py-3 text-center text-xs font-medium text-white uppercase tracking-wider">Gráfico</th>
                            <th className="px-6 py-3 text-center text-xs font-medium text-white uppercase tracking-wider">Data de Envio</th>
                            <th className="px-6 py-3 text-center text-xs font-medium text-white uppercase tracking-wider">Ações</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-600">
                        {months.map(month => (
                            <tr key={month.key} className="hover:bg-gray-600 transition-colors duration-150">
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-white">
                                    <div className="flex items-center">
                                        <span className="font-medium">{month.name}</span>
                                        {graphs[month.key] && (
                                            <span className="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                                <FontAwesomeIcon icon={faImage} className="mr-1" />
                                                Enviado
                                            </span>
                                        )}
                                    </div>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-white">
                                    {graphs[month.key] ? (
                                        <div className="flex justify-center">
                                            <img 
                                                src={`https://cardroomgrinders.com.br${graphs[month.key].image_url}`}
                                                alt={`Gráfico ${month.name}`}
                                                className="h-16 w-auto rounded cursor-pointer hover:opacity-80 transition-opacity"
                                                onClick={() => window.open(`https://cardroomgrinders.com.br${graphs[month.key].image_url}`, '_blank')}
                                            />
                                        </div>
                                    ) : (
                                        <div className="text-center text-gray-400">
                                            <FontAwesomeIcon icon={faChartLine} className="text-2xl mb-1" />
                                            <p className="text-xs">Não enviado</p>
                                        </div>
                                    )}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-center text-sm text-white">
                                    {graphs[month.key] ? (
                                        <span className="text-gray-300">
                                            {new Date(graphs[month.key].created_at).toLocaleDateString('pt-BR')}
                                        </span>
                                    ) : (
                                        <span className="text-gray-500">-</span>
                                    )}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-center text-sm font-medium">
                                    <input
                                        type="file"
                                        id={`graph-file-${month.key}`}
                                        accept="image/*"
                                        onChange={(e) => handleFileSelect(month.key, e)}
                                        style={{ display: 'none' }}
                                        disabled={uploading}
                                    />
                                    <label 
                                        htmlFor={`graph-file-${month.key}`}
                                        className={`px-3 py-2 rounded cursor-pointer transition-colors ${
                                            graphs[month.key] 
                                                ? 'bg-blue-600 hover:bg-blue-700 text-white' 
                                                : 'bg-red-400 hover:bg-red-500 text-white'
                                        } ${uploading ? 'opacity-50 cursor-not-allowed' : ''}`}
                                    >
                                        {uploadingMonth === month.key ? (
                                            <>
                                                <div className="inline-block animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                                                Enviando...
                                            </>
                                        ) : (
                                            <>
                                                <FontAwesomeIcon icon={faUpload} className="mr-1" />
                                                {graphs[month.key] ? 'Substituir' : 'Enviar'}
                                            </>
                                        )}
                                    </label>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {/* Instruções */}
            <div className="mt-6 bg-gray-700 rounded-lg p-4">
                <h3 className="text-lg font-semibold text-red-400 mb-2">Instruções</h3>
                <ul className="text-gray-300 text-sm space-y-1">
                    <li>• Envie seus gráficos mensais de resultados</li>
                    <li>• Formatos aceitos: PNG, JPG, GIF, WebP</li>
                    <li>• Tamanho máximo: 10MB</li>
                    <li>• Clique na imagem para visualizar em tamanho completo</li>
                    <li>• Você pode substituir gráficos já enviados</li>
                </ul>
            </div>
        </div>
    );
};

export default MonthlyGraphs;
