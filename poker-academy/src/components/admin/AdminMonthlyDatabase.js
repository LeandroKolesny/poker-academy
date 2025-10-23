import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faDownload, faDatabase, faCalendarAlt, faFile, faUser, faBuilding } from '@fortawesome/free-solid-svg-icons';
import api from '../../services/api';
import Loading from '../shared/Loading';

const AdminMonthlyDatabase = () => {
    const [databases, setDatabases] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());
    const [selectedParticao, setSelectedParticao] = useState('');
    const [studentFilter, setStudentFilter] = useState('');
    const [students, setStudents] = useState([]);
    const [particoes, setParticoes] = useState([]);

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
        fetchDatabases();
        fetchStudents();
        fetchParticoes();
    }, [selectedYear, selectedParticao]);

    const fetchDatabases = async () => {
        try {
            setLoading(true);
            let url = `/student/database?year=${selectedYear}`;
            if (selectedParticao) {
                url += `&particao_id=${selectedParticao}`;
            }
            const response = await api.get(url);

            // O backend retorna { data: [...] }, então acessar response.data.data
            const databasesList = response.data?.data || [];
            if (Array.isArray(databasesList)) {
                setDatabases(databasesList);
            }
            console.log('📊 Databases carregados (admin):', databasesList);
        } catch (error) {
            console.error('Erro ao buscar databases:', error);
            alert('Erro ao carregar databases');
        } finally {
            setLoading(false);
        }
    };

    const fetchStudents = async () => {
        try {
            const response = await api.get('/users?type=student');
            if (response.data && Array.isArray(response.data)) {
                setStudents(response.data);
            }
        } catch (error) {
            console.error('Erro ao buscar alunos:', error);
        }
    };

    const fetchParticoes = async () => {
        try {
            const response = await api.get('/particoes');
            const particoesList = response.data?.data || [];
            if (Array.isArray(particoesList)) {
                setParticoes(particoesList);
            }
        } catch (error) {
            console.error('Erro ao buscar partições:', error);
        }
    };

    const formatFileSize = (bytes) => {
        if (!bytes) return 'N/A';
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
        return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
    };

    const getStudentName = (studentId) => {
        const student = students.find(s => s.id === studentId);
        return student ? student.name : `Aluno #${studentId}`;
    };

    const handleDownload = async (filename) => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(
                `https://cardroomgrinders.com.br/api/student/database/download/${filename}`,
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

    const filteredDatabases = studentFilter
        ? databases.filter(db => db.student_id === parseInt(studentFilter))
        : databases;

    if (loading) {
        return <Loading />;
    }

    return (
        <div className="p-6 text-white min-h-screen">
            {/* Header */}
            <div className="flex justify-between items-center mb-6 flex-wrap gap-4">
                <h2 className="text-2xl font-semibold text-red-400">Database Mensal - Todos os Alunos</h2>
                <div className="flex items-center gap-4 flex-wrap">
                    <div>
                        <label className="text-sm font-medium text-gray-300 block mb-1">Partição:</label>
                        <select
                            className="bg-gray-700 text-white px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-red-400"
                            value={selectedParticao}
                            onChange={(e) => setSelectedParticao(e.target.value)}
                        >
                            <option value="">Todas as partições</option>
                            {particoes.map(particao => (
                                <option key={particao.id} value={particao.id}>
                                    {particao.nome}
                                </option>
                            ))}
                        </select>
                    </div>
                    <div>
                        <label className="text-sm font-medium text-gray-300 block mb-1">Ano:</label>
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
                    <div>
                        <label className="text-sm font-medium text-gray-300 block mb-1">Filtrar Aluno:</label>
                        <select
                            className="bg-gray-700 text-white px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-red-400"
                            value={studentFilter}
                            onChange={(e) => setStudentFilter(e.target.value)}
                        >
                            <option value="">Todos os alunos</option>
                            {students.map(student => (
                                <option key={student.id} value={student.id}>
                                    {student.name}
                                </option>
                            ))}
                        </select>
                    </div>
                </div>
            </div>

            {/* Tabela de Databases */}
            <div className="bg-gray-700 rounded-lg overflow-x-auto shadow-lg">
                <table className="w-full min-w-full">
                    <thead className="bg-gray-500">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Aluno</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Mês</th>
                            <th className="px-6 py-3 text-center text-xs font-medium text-white uppercase tracking-wider">Tamanho</th>
                            <th className="px-6 py-3 text-center text-xs font-medium text-white uppercase tracking-wider">Data de Envio</th>
                            <th className="px-6 py-3 text-center text-xs font-medium text-white uppercase tracking-wider">Status</th>
                            <th className="px-6 py-3 text-center text-xs font-medium text-white uppercase tracking-wider">Ações</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-600">
                        {filteredDatabases.length > 0 ? (
                            filteredDatabases.map((db, index) => (
                                <tr key={index} className="hover:bg-gray-600 transition-colors duration-150">
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-white">
                                        <div className="flex items-center">
                                            <FontAwesomeIcon icon={faUser} className="mr-2 text-gray-400" />
                                            <span className="font-medium">{getStudentName(db.student_id)}</span>
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-white">
                                        <div className="flex items-center">
                                            <FontAwesomeIcon icon={faCalendarAlt} className="mr-2 text-gray-400" />
                                            <span>{months.find(m => m.key === db.month)?.name || db.month}</span>
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-center text-sm text-white">
                                        <span className="text-gray-300">
                                            {formatFileSize(db.file_size)}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-center text-sm text-white">
                                        <span className="text-gray-300">
                                            {new Date(db.created_at).toLocaleDateString('pt-BR')}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-center text-sm font-medium">
                                        {db.status === 'ativo' ? (
                                            <span className="inline-block px-3 py-1 rounded bg-green-600 text-white text-xs font-semibold">
                                                ✓ Disponível
                                            </span>
                                        ) : (
                                            <span className="inline-block px-3 py-1 rounded bg-red-600 text-white text-xs font-semibold">
                                                ✗ Deletado
                                            </span>
                                        )}
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-center text-sm font-medium">
                                        <button
                                            onClick={() => handleDownload(db.file_url.split('/').pop())}
                                            disabled={db.status === 'deletado'}
                                            className={`inline-block px-3 py-2 rounded text-white transition-colors ${
                                                db.status === 'deletado'
                                                    ? 'bg-gray-600 cursor-not-allowed opacity-50'
                                                    : 'bg-green-600 hover:bg-green-700'
                                            }`}
                                        >
                                            <FontAwesomeIcon icon={faDownload} className="mr-1" />
                                            Baixar
                                        </button>
                                    </td>
                                </tr>
                            ))
                        ) : (
                            <tr>
                                <td colSpan="6" className="px-6 py-4 text-center text-gray-400">
                                    Nenhum database encontrado para o filtro selecionado
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>

            {/* Resumo */}
            <div className="mt-6 bg-gray-700 rounded-lg p-4">
                <h3 className="text-lg font-semibold text-red-400 mb-2">Resumo</h3>
                <ul className="text-gray-300 text-sm space-y-1">
                    <li>• Total de databases: <span className="font-semibold text-white">{filteredDatabases.length}</span></li>
                    <li>• Tamanho total: <span className="font-semibold text-white">{formatFileSize(filteredDatabases.reduce((sum, db) => sum + (db.file_size || 0), 0))}</span></li>
                    <li>• Você pode baixar qualquer database de aluno para análise</li>
                </ul>
            </div>
        </div>
    );
};

export default AdminMonthlyDatabase;

