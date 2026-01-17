import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChevronDown, faChevronRight, faUser, faEye, faTimes } from '@fortawesome/free-solid-svg-icons';
import api from '../../services/api';
import Loading from '../shared/Loading';

const PartitionStudentLayout = ({ title, renderModalContent, yearFilter = true }) => {
    const [partitions, setPartitions] = useState([]);
    const [expandedPartitions, setExpandedPartitions] = useState({});
    const [loading, setLoading] = useState(true);
    const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());
    const [selectedStudent, setSelectedStudent] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);

    useEffect(() => {
        fetchPartitions();
    }, []);

    // Expandir primeira partição quando carregar
    useEffect(() => {
        if (partitions.length > 0 && Object.keys(expandedPartitions).length === 0) {
            setExpandedPartitions({ [partitions[0].id]: true });
        }
    }, [partitions]);

    const fetchPartitions = async () => {
        try {
            setLoading(true);
            const response = await api.get('/api/admin/students-by-partition');
            console.log('Particoes carregadas:', response.data);
            setPartitions(response.data.partitions || []);
        } catch (error) {
            console.error('Erro ao buscar particoes:', error);
            alert('Erro ao carregar particoes');
            setPartitions([]);
        } finally {
            setLoading(false);
        }
    };

    const togglePartition = (partitionId) => {
        setExpandedPartitions(prev => ({
            ...prev,
            [partitionId]: !prev[partitionId]
        }));
    };

    const openStudentModal = (student) => {
        setSelectedStudent(student);
        setIsModalOpen(true);
    };

    const closeModal = () => {
        setIsModalOpen(false);
        setSelectedStudent(null);
    };

    if (loading) {
        return <Loading />;
    }

    return (
        <div className="p-6 text-white min-h-screen">
            {/* Header */}
            <div className="flex flex-col md:flex-row md:justify-between md:items-center mb-6 gap-4">
                <h2 className="text-2xl font-semibold text-red-400">{title}</h2>
                {yearFilter && (
                    <div className="flex items-center gap-2">
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
                )}
            </div>

            {/* Partitions */}
            <div className="space-y-4">
                {partitions.length === 0 ? (
                    <div className="bg-gray-700 rounded-lg p-8 text-center">
                        <p className="text-gray-400">Nenhuma particao encontrada</p>
                    </div>
                ) : (
                    partitions.map(partition => (
                        <div key={partition.id} className="bg-gray-700 rounded-lg overflow-hidden shadow-lg">
                            {/* Partition Header - Clickable */}
                            <button
                                onClick={() => togglePartition(partition.id)}
                                className="w-full px-4 py-3 bg-gray-600 hover:bg-gray-500 transition-colors flex items-center justify-between"
                            >
                                <div className="flex items-center gap-3">
                                    <FontAwesomeIcon
                                        icon={expandedPartitions[partition.id] ? faChevronDown : faChevronRight}
                                        className="text-red-400"
                                    />
                                    <span className="font-semibold text-white text-lg">
                                        {partition.nome}
                                    </span>
                                    <span className="text-gray-300 text-sm">
                                        ({partition.students?.length || 0} alunos)
                                    </span>
                                </div>
                            </button>

                            {/* Partition Content - Students Grid */}
                            {expandedPartitions[partition.id] && (
                                <div className="p-4">
                                    {partition.students?.length === 0 ? (
                                        <p className="text-gray-400 text-center py-4">
                                            Nenhum aluno nesta particao
                                        </p>
                                    ) : (
                                        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
                                            {partition.students?.map(student => (
                                                <div
                                                    key={student.id}
                                                    className="bg-gray-800 rounded-lg p-4 flex flex-col items-center text-center hover:bg-gray-750 transition-colors"
                                                >
                                                    <div className="w-12 h-12 bg-gray-600 rounded-full flex items-center justify-center mb-3">
                                                        <FontAwesomeIcon icon={faUser} className="text-gray-300 text-xl" />
                                                    </div>
                                                    <h4 className="font-medium text-white text-sm mb-1 truncate w-full">
                                                        {student.name}
                                                    </h4>
                                                    <button
                                                        onClick={() => openStudentModal(student)}
                                                        className="mt-2 px-4 py-1.5 bg-red-500 hover:bg-red-600 text-white text-sm rounded transition-colors flex items-center gap-2"
                                                    >
                                                        <FontAwesomeIcon icon={faEye} />
                                                        Ver
                                                    </button>
                                                </div>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            )}
                        </div>
                    ))
                )}
            </div>

            {/* Modal */}
            {isModalOpen && selectedStudent && (
                <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-0 md:p-4">
                    <div className="bg-gray-800 w-full h-full md:w-full md:max-w-4xl md:max-h-[95vh] md:rounded-lg shadow-xl flex flex-col">
                        {/* Modal Header */}
                        <div className="flex-shrink-0 bg-gray-800 p-4 border-b border-gray-700 flex justify-between items-start md:rounded-t-lg">
                            <div className="flex-1 pr-4">
                                <h3 className="text-xl md:text-2xl font-semibold text-red-400">
                                    {selectedStudent.name}
                                </h3>
                                <p className="text-gray-400 text-sm mt-1">{selectedStudent.email}</p>
                            </div>
                            <button
                                onClick={closeModal}
                                className="flex-shrink-0 bg-red-600 hover:bg-red-700 text-white transition-colors p-2 rounded-lg shadow-lg"
                                aria-label="Fechar modal"
                                title="Fechar"
                            >
                                <FontAwesomeIcon icon={faTimes} size="lg" />
                            </button>
                        </div>

                        {/* Modal Content */}
                        <div className="flex-1 overflow-y-auto p-4 md:p-6">
                            {renderModalContent && renderModalContent({
                                student: selectedStudent,
                                year: selectedYear,
                                onClose: closeModal
                            })}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default PartitionStudentLayout;
