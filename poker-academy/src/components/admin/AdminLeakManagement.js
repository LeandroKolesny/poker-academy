import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch, faUpload, faImage, faUsers, faCalendarAlt, faEye, faSave } from '@fortawesome/free-solid-svg-icons';
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
    const [improvements, setImprovements] = useState({});

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
            setPartitions(response.data.partitions || []);
        } catch (error) {
            console.error('❌ Erro ao buscar partições:', error);
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
            const leaks = response.data.leaks || {};
            setStudentLeaks(leaks);
            
            // Carregar melhorias existentes
            const existingImprovements = {};
            Object.keys(leaks).forEach(month => {
                if (leaks[month].improvements) {
                    existingImprovements[month] = leaks[month].improvements;
                }
            });
            setImprovements(existingImprovements);
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
        setImprovements({});
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
            console.log('🔐 Token para upload:', token ? 'PRESENTE' : 'AUSENTE');
            
            const formData = new FormData();
            formData.append('file', file);
            formData.append('month', month);
            formData.append('year', selectedYear);
            formData.append('improvements', improvements[month] || '');

            const response = await fetch(`https://cardroomgrinders.com.br/api/admin/student/${selectedStudent.id}/leaks/upload`, {
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
                alert('Análise de leak enviada com sucesso!');
                fetchStudentLeaks();
            } else {
                const errorData = await response.text();
                console.error('❌ Upload erro:', response.status, errorData);
                alert(`Erro no upload: ${response.status} - ${errorData}`);
            }
        } catch (error) {
            console.error('❌ Erro no upload:', error);
            alert(`Erro ao enviar análise: ${error.message}`);
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

    const handleImprovementChange = (month, value) => {
        setImprovements(prev => ({
            ...prev,
            [month]: value
        }));
    };

    const saveImprovements = async (month) => {
        if (!selectedStudent || !improvements[month]) return;
        
        try {
            const token = localStorage.getItem('token');
            const formData = new FormData();
            formData.append('month', month);
            formData.append('year', selectedYear);
            formData.append('improvements', improvements[month]);

            const response = await fetch(`https://cardroomgrinders.com.br/api/admin/student/${selectedStudent.id}/leaks/improvements`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                body: formData
            });

            if (response.ok) {
                console.log('✅ Melhorias salvas com sucesso');
                alert('Melhorias salvas com sucesso!');
                fetchStudentLeaks();
            } else {
                console.error('❌ Erro ao salvar melhorias:', response.status);
                alert('Erro ao salvar melhorias');
            }
        } catch (error) {
            console.error('❌ Erro ao salvar melhorias:', error);
            alert('Erro ao salvar melhorias');
        }
    };

    if (loading) {
        return <Loading />;
    }

    return (
        <div className="p-6 text-white min-h-screen">
            {/* Header */}
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-semibold text-red-400">Gerenciamento de Caça Leaks</h2>
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

            {/* Análises do Aluno Selecionado */}
            {selectedStudent ? (
                <div className="student-leaks">
                    <div className="flex justify-between items-center mb-4">
                        <div>
                            <h3 className="text-lg font-semibold text-red-400">Análises de {selectedStudent.name}</h3>
                            <p className="text-gray-400 text-sm">{selectedStudent.email}</p>
                        </div>
                    </div>

                    {loadingLeaks ? (
                        <div className="text-center py-8">
                            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-red-400"></div>
                            <p className="text-gray-400 mt-2">Carregando análises...</p>
                        </div>
                    ) : (
                        <div className="bg-gray-700 rounded-lg overflow-x-auto shadow-lg">
                            <table className="w-full min-w-full">
                                <thead className="bg-gray-500">
                                    <tr>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Mês</th>
                                        <th className="px-6 py-3 text-center text-xs font-medium text-white uppercase tracking-wider">Análise</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Melhorias Sugeridas</th>
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
                                                    {studentLeaks[month.key] && (
                                                        <span className="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                                            <FontAwesomeIcon icon={faImage} className="mr-1" />
                                                            Analisado
                                                        </span>
                                                    )}
                                                </div>
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-white">
                                                {studentLeaks[month.key] ? (
                                                    <div className="flex justify-center">
                                                        <img 
                                                            src={`https://cardroomgrinders.com.br${studentLeaks[month.key].image_url}`}
                                                            alt={`Análise ${month.name}`}
                                                            className="h-16 w-auto rounded cursor-pointer hover:opacity-80 transition-opacity"
                                                            onClick={() => window.open(`https://cardroomgrinders.com.br${studentLeaks[month.key].image_url}`, '_blank')}
                                                        />
                                                    </div>
                                                ) : (
                                                    <div className="text-center text-gray-400">
                                                        <FontAwesomeIcon icon={faSearch} className="text-2xl mb-1" />
                                                        <p className="text-xs">Não analisado</p>
                                                    </div>
                                                )}
                                            </td>
                                            <td className="px-6 py-4 text-sm text-white">
                                                <textarea
                                                    className="w-full bg-gray-600 text-white px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-red-400 resize-vertical"
                                                    placeholder="Digite as principais melhorias que o aluno deve focar..."
                                                    value={improvements[month.key] || ''}
                                                    onChange={(e) => handleImprovementChange(month.key, e.target.value)}
                                                    rows="3"
                                                />
                                                <div className="mt-2 flex gap-2">
                                                    <button
                                                        className="px-3 py-1 bg-green-600 hover:bg-green-700 text-white text-xs rounded transition-colors"
                                                        onClick={() => saveImprovements(month.key)}
                                                        disabled={!improvements[month.key]?.trim()}
                                                    >
                                                        <FontAwesomeIcon icon={faSave} className="mr-1" />
                                                        Salvar
                                                    </button>
                                                </div>
                                                {studentLeaks[month.key]?.improvements && (
                                                    <div className="mt-2 p-2 bg-gray-600 rounded">
                                                        <p className="text-xs font-medium text-green-400 mb-1">💾 Salvo:</p>
                                                        <p className="text-xs text-gray-300">{studentLeaks[month.key].improvements}</p>
                                                    </div>
                                                )}
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-center text-sm text-white">
                                                {studentLeaks[month.key] ? (
                                                    <span className="text-gray-300">
                                                        {new Date(studentLeaks[month.key].created_at).toLocaleDateString('pt-BR')}
                                                    </span>
                                                ) : (
                                                    <span className="text-gray-500">-</span>
                                                )}
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-center text-sm font-medium">
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
                                                    className={`px-3 py-2 rounded cursor-pointer transition-colors ${
                                                        studentLeaks[month.key] 
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
                                                            {studentLeaks[month.key] ? 'Substituir' : 'Enviar'}
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
                    <p className="text-gray-500">Escolha um aluno da tabela acima para gerenciar suas análises de leaks</p>
                </div>
            )}
        </div>
    );
};

export default AdminLeakManagement;
