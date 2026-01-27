import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChartLine, faImage, faUpload } from '@fortawesome/free-solid-svg-icons';
import api from '../../services/api';
import PartitionStudentLayout from './PartitionStudentLayout';
import ImageZoomModal from '../shared/ImageZoomModal';
import { MONTHS } from '../../constants';

// Helper para construir URL de imagem (suporta URLs absolutas do R2 e relativas)
const getImageUrl = (imageUrl) => {
    if (!imageUrl) return '';
    // URL absoluta correta
    if (imageUrl.startsWith('http://') || imageUrl.startsWith('https://')) {
        return imageUrl;
    }
    // URL com protocolo malformado (sem dois pontos, ex: https//...)
    if (imageUrl.startsWith('https//')) {
        return imageUrl.replace('https//', 'https://');
    }
    if (imageUrl.startsWith('http//')) {
        return imageUrl.replace('http//', 'http://');
    }
    // URL relativa - concatenar com base
    return `${api.defaults.baseURL}${imageUrl}`;
};

// Componente de conteudo do modal para graficos
const GraphsModalContent = ({ student, year }) => {
    const [studentGraphs, setStudentGraphs] = useState({});
    const [loading, setLoading] = useState(true);
    const [uploading, setUploading] = useState(false);
    const [uploadingMonth, setUploadingMonth] = useState(null);
    const [zoomModal, setZoomModal] = useState({ isOpen: false, imageUrl: '', altText: '' });

    useEffect(() => {
        fetchStudentGraphs();
    }, [student.id, year]);

    const fetchStudentGraphs = async () => {
        try {
            setLoading(true);
            const response = await api.get(`/api/admin/student/${student.id}/graphs?year=${year}`);
            const graphs = response.data.graphs || {};
            setStudentGraphs(graphs);
        } catch (error) {
            console.error('Erro ao buscar graficos do aluno:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleFileUpload = async (month, file) => {
        if (!file) return;

        const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/webp'];
        if (!allowedTypes.includes(file.type)) {
            alert('Tipo de arquivo nao permitido. Use PNG, JPG, GIF ou WebP.');
            return;
        }

        if (file.size > 10 * 1024 * 1024) {
            alert('Arquivo muito grande. Maximo 10MB.');
            return;
        }

        try {
            setUploading(true);
            setUploadingMonth(month);

            const token = localStorage.getItem('token');
            const formData = new FormData();
            formData.append('file', file);
            formData.append('month', month);
            formData.append('year', year);

            const response = await fetch(`${api.defaults.baseURL}/api/admin/student/${student.id}/graphs/upload`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                body: formData
            });

            if (response.ok) {
                alert('Grafico enviado com sucesso!');
                fetchStudentGraphs();
            } else {
                const errorData = await response.text();
                alert(`Erro no upload: ${response.status} - ${errorData}`);
            }
        } catch (error) {
            alert(`Erro ao enviar grafico: ${error.message}`);
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

    const openZoomModal = (imageUrl, altText) => {
        setZoomModal({
            isOpen: true,
            imageUrl: getImageUrl(imageUrl),
            altText
        });
    };

    const closeZoomModal = () => {
        setZoomModal({ isOpen: false, imageUrl: '', altText: '' });
    };

    if (loading) {
        return (
            <div className="text-center py-8">
                <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-red-400"></div>
                <p className="text-gray-400 mt-2">Carregando graficos...</p>
            </div>
        );
    }

    return (
        <>
            <div className="bg-gray-700 rounded-lg overflow-x-auto shadow-lg">
                <table className="w-full min-w-full">
                    <thead className="bg-gray-600">
                        <tr>
                            <th className="px-4 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Mes</th>
                            <th className="px-4 py-3 text-center text-xs font-medium text-white uppercase tracking-wider">Grafico</th>
                            <th className="px-4 py-3 text-center text-xs font-medium text-white uppercase tracking-wider">Data</th>
                            <th className="px-4 py-3 text-center text-xs font-medium text-white uppercase tracking-wider">Acoes</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-600">
                        {MONTHS.map(month => (
                            <tr key={month.key} className="hover:bg-gray-600 transition-colors duration-150">
                                <td className="px-4 py-3 whitespace-nowrap text-sm text-white">
                                    <div className="flex items-center">
                                        <span className="font-medium">{month.name}</span>
                                        {studentGraphs[month.key] && (
                                            <span className="ml-2 inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                                <FontAwesomeIcon icon={faImage} className="mr-1" />
                                                Enviado
                                            </span>
                                        )}
                                    </div>
                                </td>
                                <td className="px-4 py-3 whitespace-nowrap text-sm text-white">
                                    {studentGraphs[month.key] ? (
                                        <div className="flex justify-center">
                                            <img
                                                src={getImageUrl(studentGraphs[month.key].image_url)}
                                                alt={`Grafico ${month.name}`}
                                                className="h-14 w-auto rounded cursor-pointer hover:opacity-80 transition-opacity"
                                                onClick={() => openZoomModal(studentGraphs[month.key].image_url, `Grafico ${month.name}`)}
                                            />
                                        </div>
                                    ) : (
                                        <div className="text-center text-gray-400">
                                            <FontAwesomeIcon icon={faChartLine} className="text-xl" />
                                            <p className="text-xs">Nao enviado</p>
                                        </div>
                                    )}
                                </td>
                                <td className="px-4 py-3 whitespace-nowrap text-center text-sm text-white">
                                    {studentGraphs[month.key] ? (
                                        <span className="text-gray-300">
                                            {new Date(studentGraphs[month.key].created_at).toLocaleDateString('pt-BR')}
                                        </span>
                                    ) : (
                                        <span className="text-gray-500">-</span>
                                    )}
                                </td>
                                <td className="px-4 py-3 whitespace-nowrap text-center text-sm font-medium">
                                    <input
                                        type="file"
                                        id={`graph-file-${student.id}-${month.key}`}
                                        accept="image/*"
                                        onChange={(e) => handleFileSelect(month.key, e)}
                                        style={{ display: 'none' }}
                                        disabled={uploading}
                                    />
                                    <label
                                        htmlFor={`graph-file-${student.id}-${month.key}`}
                                        className={`inline-block px-3 py-1.5 rounded cursor-pointer transition-colors text-sm ${
                                            studentGraphs[month.key]
                                                ? 'bg-blue-600 hover:bg-blue-700 text-white'
                                                : 'bg-red-500 hover:bg-red-600 text-white'
                                        } ${uploading ? 'opacity-50 cursor-not-allowed' : ''}`}
                                    >
                                        {uploadingMonth === month.key ? (
                                            <>
                                                <div className="inline-block animate-spin rounded-full h-3 w-3 border-b-2 border-white mr-1"></div>
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

            {/* Modal de Zoom */}
            <ImageZoomModal
                isOpen={zoomModal.isOpen}
                onClose={closeZoomModal}
                imageUrl={zoomModal.imageUrl}
                altText={zoomModal.altText}
            />
        </>
    );
};

// Componente principal
const AdminStudentGraphs = () => {
    return (
        <PartitionStudentLayout
            title="Gerenciamento de Graficos dos Alunos"
            renderModalContent={({ student, year }) => (
                <GraphsModalContent student={student} year={year} />
            )}
        />
    );
};

export default AdminStudentGraphs;
