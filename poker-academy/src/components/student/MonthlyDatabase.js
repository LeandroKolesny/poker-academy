import React, { useState, useEffect, useContext } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUpload, faDownload, faDatabase, faCalendarAlt, faFile } from '@fortawesome/free-solid-svg-icons';
import api from '../../services/api';
import Loading from '../shared/Loading';
import { AuthContext } from '../../context/AuthContext';
import { MONTHS } from '../../constants';
import { formatFileSize } from '../../utils';

const MonthlyDatabase = () => {
    console.log('🔍 MonthlyDatabase component renderizado!');
    const { user } = useContext(AuthContext);
    const [databases, setDatabases] = useState([]);
    const [loading, setLoading] = useState(true);
    const [uploading, setUploading] = useState(false);
    const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());
    const [uploadingMonth, setUploadingMonth] = useState(null);

    useEffect(() => {
        fetchDatabases();
    }, [selectedYear]);

    const fetchDatabases = async () => {
        try {
            setLoading(true);
            const response = await api.get(`/api/student/database?year=${selectedYear}`);

            // Converter array em objeto indexado por mês
            const dbByMonth = {};
            // O backend retorna { data: [...] }, então acessar response.data.data
            const databasesList = response.data?.data || [];
            if (Array.isArray(databasesList)) {
                databasesList.forEach(db => {
                    dbByMonth[db.month] = db;
                });
            }
            console.log('📊 Databases carregados:', dbByMonth);
            setDatabases(dbByMonth);
        } catch (error) {
            console.error('Erro ao buscar databases:', error);
            alert('Erro ao carregar databases');
        } finally {
            setLoading(false);
        }
    };

    const handleFileUpload = async (month, file) => {
        if (!file) return;

        // Validar tipo de arquivo
        if (file.type !== 'application/zip' && !file.name.endsWith('.zip')) {
            alert('Apenas arquivos .zip são permitidos.');
            return;
        }

        // Validar tamanho do arquivo (máximo 500MB)
        if (file.size > 500 * 1024 * 1024) {
            alert('Arquivo muito grande. Máximo 500MB.');
            return;
        }

        try {
            setUploading(true);
            setUploadingMonth(month);

            const token = localStorage.getItem('token');
            console.log('🔐 Token para upload:', token ? 'PRESENTE' : 'AUSENTE');

            const formData = new FormData();
            formData.append('file', file);
            formData.append('month', month);
            formData.append('year', selectedYear);

            const response = await fetch(`${api.defaults.baseURL}/api/student/database/upload`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                body: formData
            });

            console.log('📤 Response status:', response.status);

            if (response.ok) {
                const data = await response.json();
                console.log('✅ Upload sucesso:', data);
                alert('Database enviado com sucesso!');
                fetchDatabases();
            } else {
                const errorData = await response.text();
                console.error('❌ Upload erro:', response.status, errorData);
                alert(`Erro no upload: ${response.status} - ${errorData}`);
            }
        } catch (error) {
            console.error('❌ Erro no upload:', error);
            alert(`Erro ao enviar database: ${error.message}`);
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
        event.target.value = '';
    };

    const handleDownload = async (month, filename) => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(
                `${api.defaults.baseURL}/api/student/database/download/${filename}`,
                {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                }
            );

            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
            } else {
                alert('Erro ao baixar arquivo');
            }
        } catch (error) {
            console.error('Erro ao baixar:', error);
            alert('Erro ao baixar arquivo');
        }
    };

    if (loading) {
        return <Loading />;
    }

    return (
        <div className="p-6 text-white min-h-screen">
            {/* Header */}
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-semibold text-red-400">Database Mensal</h2>
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

            {/* Tabela de Databases */}
            <div className="bg-gray-700 rounded-lg overflow-x-auto shadow-lg">
                <table className="w-full min-w-full">
                    <thead className="bg-gray-500">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Mês</th>
                            <th className="px-6 py-3 text-center text-xs font-medium text-white uppercase tracking-wider">Status</th>
                            <th className="px-6 py-3 text-center text-xs font-medium text-white uppercase tracking-wider">Tamanho</th>
                            <th className="px-6 py-3 text-center text-xs font-medium text-white uppercase tracking-wider">Data de Envio</th>
                            <th className="px-6 py-3 text-center text-xs font-medium text-white uppercase tracking-wider">Ações</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-600">
                        {MONTHS.map(month => (
                            <tr key={month.key} className="hover:bg-gray-600 transition-colors duration-150">
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-white">
                                    <div className="flex items-center">
                                        <span className="font-medium">{month.name}</span>
                                        {databases[month.key] && (
                                            <span className="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                                <FontAwesomeIcon icon={faFile} className="mr-1" />
                                                Enviado
                                            </span>
                                        )}
                                    </div>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-center text-sm text-white">
                                    {databases[month.key] ? (
                                        databases[month.key].status === 'ativo' ? (
                                            <div className="flex justify-center items-center">
                                                <span className="inline-block px-3 py-1 rounded bg-green-600 text-white text-xs font-semibold">
                                                    ✓ Disponível
                                                </span>
                                            </div>
                                        ) : (
                                            <div className="flex justify-center items-center">
                                                <span className="inline-block px-3 py-1 rounded bg-red-600 text-white text-xs font-semibold">
                                                    ✗ Deletado
                                                </span>
                                            </div>
                                        )
                                    ) : (
                                        <div className="text-center text-gray-400">
                                            <span>Não enviado</span>
                                        </div>
                                    )}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-center text-sm text-white">
                                    {databases[month.key] ? (
                                        <span className="text-gray-300">
                                            {formatFileSize(databases[month.key].file_size)}
                                        </span>
                                    ) : (
                                        <span className="text-gray-500">-</span>
                                    )}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-center text-sm text-white">
                                    {databases[month.key] ? (
                                        <span className="text-gray-300">
                                            {new Date(databases[month.key].created_at).toLocaleDateString('pt-BR')}
                                        </span>
                                    ) : (
                                        <span className="text-gray-500">-</span>
                                    )}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-center text-sm font-medium space-x-2">
                                    {/* Upload Button */}
                                    <input
                                        type="file"
                                        id={`db-file-${month.key}`}
                                        accept=".zip"
                                        onChange={(e) => handleFileSelect(month.key, e)}
                                        style={{ display: 'none' }}
                                        disabled={uploading || (databases[month.key]?.status === 'deletado')}
                                    />
                                    <label
                                        htmlFor={`db-file-${month.key}`}
                                        className={`inline-block px-3 py-2 rounded cursor-pointer transition-colors ${
                                            databases[month.key]?.status === 'deletado'
                                                ? 'bg-gray-600 cursor-not-allowed opacity-50 text-white'
                                                : databases[month.key]
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
                                                {databases[month.key] && databases[month.key]?.status !== 'deletado' ? 'Substituir' : 'Enviar'}
                                            </>
                                        )}
                                    </label>

                                    {/* Download Button */}
                                    {databases[month.key] && (
                                        <button
                                            onClick={() => handleDownload(month.key, databases[month.key].file_url.split('/').pop())}
                                            disabled={databases[month.key].status === 'deletado'}
                                            className={`inline-block px-3 py-2 rounded text-white transition-colors ${
                                                databases[month.key].status === 'deletado'
                                                    ? 'bg-gray-600 cursor-not-allowed opacity-50'
                                                    : 'bg-green-600 hover:bg-green-700'
                                            }`}
                                        >
                                            <FontAwesomeIcon icon={faDownload} className="mr-1" />
                                            Baixar
                                        </button>
                                    )}
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
                    <li>• Envie seus databases mensais com os dados das mãos jogadas</li>
                    <li>• Formato aceito: .zip</li>
                    <li>• Tamanho máximo: 500MB</li>
                    <li>• Você pode substituir databases já enviados</li>
                    <li>• Clique em "Baixar" para recuperar seus arquivos</li>
                </ul>
            </div>
        </div>
    );
};

export default MonthlyDatabase;

