import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChartLine, faUsers, faEye, faCalendarAlt, faImage, faUpload } from '@fortawesome/free-solid-svg-icons';
import api from '../../services/api';
import Loading from '../shared/Loading';

const AdminStudentGraphs = () => {
    const [partitions, setPartitions] = useState([]);
    const [selectedStudent, setSelectedStudent] = useState(null);
    const [studentGraphs, setStudentGraphs] = useState({});
    const [loading, setLoading] = useState(true);
    const [loadingGraphs, setLoadingGraphs] = useState(false);
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
            fetchStudentGraphs();
        }
    }, [selectedStudent, selectedYear]);

    const fetchPartitions = async () => {
        try {
            setLoading(true);
            const response = await api.get('/admin/students-by-partition');
            console.log('📊 Resposta da API:', response.data);
            setPartitions(response.data.partitions || []);
        } catch (error) {
            console.error('❌ Erro ao buscar partições:', error);
            alert(`Erro ao carregar partições: ${error.response?.data?.error || error.message}`);
            setPartitions([]);
        } finally {
            setLoading(false);
        }
    };

    const fetchStudentGraphs = async () => {
        if (!selectedStudent) return;
        
        try {
            setLoadingGraphs(true);
            const response = await api.get(`/admin/student/${selectedStudent.id}/graphs?year=${selectedYear}`);
            const graphs = response.data.graphs || {};
            setStudentGraphs(graphs);
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

    const handleFileUpload = async (month, file) => {
        if (!file || !selectedStudent) return;

        const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/webp'];
        if (!allowedTypes.includes(file.type)) {
            alert('Tipo de arquivo não permitido. Use PNG, JPG, GIF ou WebP.');
            return;
        }

        if (file.size > 10 * 1024 * 1024) {
            alert('Arquivo muito grande. Máximo 10MB.');
            return;
        }

        try {
            setUploading(true);
            setUploadingMonth(month);

            const token = localStorage.getItem('token');
            const formData = new FormData();
            formData.append('file', file);
            formData.append('month', month);
            formData.append('year', selectedYear);

            const response = await fetch(`https://cardroomgrinders.com.br/api/admin/student/${selectedStudent.id}/graphs/upload`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                body: formData
            });

            if (response.ok) {
                const data = await response.json();
                console.log('✅ Upload sucesso:', data);
                alert('Gráfico enviado com sucesso!');
                fetchStudentGraphs();
            } else {
                const errorData = await response.text();
                console.error('❌ Upload erro:', response.status, errorData);
                alert(`Erro no upload: ${response.status} - ${errorData}`);
            }
        } catch (error) {
            console.error('❌ Erro no upload:', error);
            alert(`Erro ao enviar gráfico: ${error.message}`);
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

    if (loading) {
        return <Loading />;
    }

    return (
        <div className="p-6 text-white min-h-screen">
            {/* Header */}
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-semibold text-red-400">Gerenciamento de Gráficos dos Alunos</h2>
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

            {/* Seleção de Aluno */}
            <div className="mb-6">
                <h3 className="text-lg font-semibold text-gray-300 mb-4">Selecionar Aluno</h3>
                <div className="bg-gray-700 rounded-lg overflow-x-auto shadow-lg">
                    <table className="w-full min-w-full">
                        <thead className="bg-gray-500">
                            <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Nome</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Email</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Partição</th>
                                <th className="px-6 py-3 text-center text-xs font-medium text-white uppercase tracking-wider">Ações</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-600">
                            {partitions.map(partition => 
                                partition.students.map(student => (
                                    <tr 
                                        key={student.id} 
                                        className={`hover:bg-gray-600 transition-colors duration-150 ${
                                            selectedStudent?.id === student.id ? 'bg-red-900 bg-opacity-50' : ''
                                        }`}
                                    >
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-white">{student.name}</td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-white">{student.email}</td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-white">{partition.nome}</td>
                                        <td className="px-6 py-4 whitespace-nowrap text-center text-sm font-medium">
                                            <button
                                                className={`px-4 py-2 rounded transition-colors duration-150 ${
                                                    selectedStudent?.id === student.id 
                                                        ? 'bg-green-600 hover:bg-green-700 text-white' 
                                                        : 'bg-red-400 hover:bg-red-500 text-white'
                                                }`}
                                                onClick={() => handleStudentSelect(student)}
                                            >
                                                {selectedStudent?.id === student.id ? 'Selecionado' : 'Selecionar'}
                                            </button>
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            </div>

            {/* Gráficos do Aluno Selecionado */}
            {selectedStudent ? (
                <div className="student-graphs">
                    <div className="flex justify-between items-center mb-4">
                        <div>
                            <h3 className="text-lg font-semibold text-red-400">Gráficos de {selectedStudent.name}</h3>
                            <p className="text-gray-400 text-sm">{selectedStudent.email}</p>
                        </div>
                    </div>

                    {loadingGraphs ? (
                        <div className="text-center py-8">
                            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-red-400"></div>
                            <p className="text-gray-400 mt-2">Carregando gráficos...</p>
                        </div>
                    ) : (
                        <div className="bg-gray-700 rounded-lg overflow-x-auto shadow-lg">
                            <table className="w-full min-w-full">
                                <thead className="bg-gray-500">
                                    <tr>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Mês</th>
                                        <th className="px-6 py-3 text-center text-xs font-medium text-white uppercase tracking-wider">Gráfico</th>
                                        <th className="px-6 py-3 text-center text-xs font-medium text-white uppercase tracking-wider">Data</th>
                                        <th className="px-6 py-3 text-center text-xs font-medium text-white uppercase tracking-wider">Ações</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-gray-600">
                                    {months.map(month => (
                                        <tr key={month.key} className="hover:bg-gray-600 transition-colors duration-150">
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-white">
                                                <div className="flex items-center">
                                                    <span className="font-medium">{month.name}</span>
                                                    {studentGraphs[month.key] && (
                                                        <span className="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                                            <FontAwesomeIcon icon={faImage} className="mr-1" />
                                                            Enviado
                                                        </span>
                                                    )}
                                                </div>
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-white">
                                                {studentGraphs[month.key] ? (
                                                    <div className="flex justify-center">
                                                        <img 
                                                            src={`https://cardroomgrinders.com.br${studentGraphs[month.key].image_url}`}
                                                            alt={`Gráfico ${month.name}`}
                                                            className="h-16 w-auto rounded cursor-pointer hover:opacity-80 transition-opacity"
                                                            onClick={() => window.open(`https://cardroomgrinders.com.br${studentGraphs[month.key].image_url}`, '_blank')}
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
                                                {studentGraphs[month.key] ? (
                                                    <span className="text-gray-300">
                                                        {new Date(studentGraphs[month.key].created_at).toLocaleDateString('pt-BR')}
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
                                                        studentGraphs[month.key] 
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
                                                            {studentGraphs[month.key] ? 'Substituir' : 'Enviar'}
                                                        </>
                                                    )}
                                                </label>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            ) : (
                <div className="text-center py-12">
                    <FontAwesomeIcon icon={faUsers} className="text-6xl text-gray-500 mb-4" />
                    <h3 className="text-xl font-semibold text-gray-400 mb-2">Selecione um aluno</h3>
                    <p className="text-gray-500">Escolha um aluno da tabela acima para gerenciar seus gráficos mensais</p>
                </div>
            )}
        </div>
    );
};

export default AdminStudentGraphs;
