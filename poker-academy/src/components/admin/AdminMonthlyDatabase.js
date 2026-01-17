import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faDownload, faDatabase, faFile } from '@fortawesome/free-solid-svg-icons';
import api from '../../services/api';
import PartitionStudentLayout from './PartitionStudentLayout';
import { MONTHS } from '../../constants';
import { formatFileSize } from '../../utils';

// Componente de conteudo do modal para databases
const DatabaseModalContent = ({ student, year }) => {
    const [databases, setDatabases] = useState({});
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchStudentDatabases();
    }, [student.id, year]);

    const fetchStudentDatabases = async () => {
        try {
            setLoading(true);
            // Buscar todos os databases e filtrar pelo student_id
            const response = await api.get(`/api/student/database?year=${year}`);
            const databasesList = response.data?.data || [];

            // Filtrar pelo student_id e converter para objeto por mes
            const studentDbs = databasesList.filter(db => db.student_id === student.id);
            const dbByMonth = {};
            studentDbs.forEach(db => {
                dbByMonth[db.month] = db;
            });

            setDatabases(dbByMonth);
        } catch (error) {
            console.error('Erro ao buscar databases do aluno:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleDownload = async (filename) => {
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
        return (
            <div className="text-center py-8">
                <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-red-400"></div>
                <p className="text-gray-400 mt-2">Carregando databases...</p>
            </div>
        );
    }

    return (
        <div className="bg-gray-700 rounded-lg overflow-x-auto shadow-lg">
            <table className="w-full min-w-full">
                <thead className="bg-gray-600">
                    <tr>
                        <th className="px-4 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Mes</th>
                        <th className="px-4 py-3 text-center text-xs font-medium text-white uppercase tracking-wider">Status</th>
                        <th className="px-4 py-3 text-center text-xs font-medium text-white uppercase tracking-wider">Tamanho</th>
                        <th className="px-4 py-3 text-center text-xs font-medium text-white uppercase tracking-wider">Data Envio</th>
                        <th className="px-4 py-3 text-center text-xs font-medium text-white uppercase tracking-wider">Acoes</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-gray-600">
                    {MONTHS.map(month => (
                        <tr key={month.key} className="hover:bg-gray-600 transition-colors duration-150">
                            <td className="px-4 py-3 whitespace-nowrap text-sm text-white">
                                <div className="flex items-center">
                                    <span className="font-medium">{month.name}</span>
                                    {databases[month.key] && (
                                        <span className="ml-2 inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                            <FontAwesomeIcon icon={faFile} className="mr-1" />
                                            Enviado
                                        </span>
                                    )}
                                </div>
                            </td>
                            <td className="px-4 py-3 whitespace-nowrap text-center text-sm">
                                {databases[month.key] ? (
                                    databases[month.key].status === 'ativo' ? (
                                        <span className="inline-block px-2 py-1 rounded bg-green-600 text-white text-xs font-semibold">
                                            Disponivel
                                        </span>
                                    ) : (
                                        <span className="inline-block px-2 py-1 rounded bg-red-600 text-white text-xs font-semibold">
                                            Deletado
                                        </span>
                                    )
                                ) : (
                                    <span className="text-gray-500">-</span>
                                )}
                            </td>
                            <td className="px-4 py-3 whitespace-nowrap text-center text-sm text-white">
                                {databases[month.key] ? (
                                    <span className="text-gray-300">
                                        {formatFileSize(databases[month.key].file_size)}
                                    </span>
                                ) : (
                                    <span className="text-gray-500">-</span>
                                )}
                            </td>
                            <td className="px-4 py-3 whitespace-nowrap text-center text-sm text-white">
                                {databases[month.key] ? (
                                    <span className="text-gray-300">
                                        {new Date(databases[month.key].created_at).toLocaleDateString('pt-BR')}
                                    </span>
                                ) : (
                                    <span className="text-gray-500">-</span>
                                )}
                            </td>
                            <td className="px-4 py-3 whitespace-nowrap text-center text-sm font-medium">
                                {databases[month.key] ? (
                                    <button
                                        onClick={() => handleDownload(databases[month.key].file_url.split('/').pop())}
                                        disabled={databases[month.key].status === 'deletado'}
                                        className={`inline-block px-3 py-1.5 rounded text-white transition-colors text-sm ${
                                            databases[month.key].status === 'deletado'
                                                ? 'bg-gray-600 cursor-not-allowed opacity-50'
                                                : 'bg-green-600 hover:bg-green-700'
                                        }`}
                                    >
                                        <FontAwesomeIcon icon={faDownload} className="mr-1" />
                                        Baixar
                                    </button>
                                ) : (
                                    <span className="text-gray-500 text-xs">Nao enviado</span>
                                )}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

// Componente principal
const AdminMonthlyDatabase = () => {
    return (
        <PartitionStudentLayout
            title="Database Mensal - Todos os Alunos"
            renderModalContent={({ student, year }) => (
                <DatabaseModalContent student={student} year={year} />
            )}
        />
    );
};

export default AdminMonthlyDatabase;
