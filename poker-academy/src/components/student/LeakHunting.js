import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch, faImage, faCalendarAlt, faEye } from '@fortawesome/free-solid-svg-icons';
import api from '../../services/api';
import Loading from '../shared/Loading';
import ImageZoomModal from '../shared/ImageZoomModal';
import { MONTHS } from '../../constants';

const LeakHunting = () => {
    const [leaks, setLeaks] = useState({});
    const [loading, setLoading] = useState(true);
    const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());
    const [zoomModal, setZoomModal] = useState({ isOpen: false, imageUrl: '', altText: '' });

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

    const openZoomModal = (imageUrl, altText) => {
        setZoomModal({
            isOpen: true,
            imageUrl: `${api.defaults.baseURL}${imageUrl}`,
            altText
        });
    };

    const closeZoomModal = () => {
        setZoomModal({ isOpen: false, imageUrl: '', altText: '' });
    };

    if (loading) {
        return <Loading />;
    }

    return (
        <div className="p-6 text-white min-h-screen">
            {/* Header */}
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-semibold text-red-400">Minhas Análises de Leaks</h2>
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

            {/* Tabela de Análises */}
            <div className="bg-gray-700 rounded-lg overflow-x-auto shadow-lg">
                <table className="w-full min-w-full">
                    <thead className="bg-gray-500">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Mês</th>
                            <th className="px-6 py-3 text-center text-xs font-medium text-white uppercase tracking-wider">Análise</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Melhorias Sugeridas</th>
                            <th className="px-6 py-3 text-center text-xs font-medium text-white uppercase tracking-wider">Data</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-600">
                        {MONTHS.map(month => (
                            <tr key={month.key} className="hover:bg-gray-600 transition-colors duration-150">
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-white">
                                    <div className="flex items-center">
                                        <span className="font-medium">{month.name}</span>
                                        {leaks[month.key] && (
                                            <span className="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                                <FontAwesomeIcon icon={faImage} className="mr-1" />
                                                Analisado
                                            </span>
                                        )}
                                    </div>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-white">
                                    {leaks[month.key] && leaks[month.key].image_url ? (
                                        <div className="flex justify-center">
                                            <img
                                                src={`${api.defaults.baseURL}${leaks[month.key].image_url}`}
                                                alt={`Análise ${month.name}`}
                                                className="h-16 w-auto rounded cursor-pointer hover:opacity-80 transition-opacity"
                                                onClick={() => openZoomModal(leaks[month.key].image_url, `Análise ${month.name}`)}
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
                                    {leaks[month.key] && leaks[month.key].improvements ? (
                                        <div className="bg-gray-600 rounded p-3">
                                            <p className="text-sm text-gray-300 whitespace-pre-wrap">
                                                {leaks[month.key].improvements}
                                            </p>
                                        </div>
                                    ) : (
                                        <div className="text-center text-gray-400">
                                            <p className="text-xs">Nenhuma melhoria sugerida</p>
                                        </div>
                                    )}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-center text-sm text-white">
                                    {leaks[month.key] ? (
                                        <span className="text-gray-300">
                                            {new Date(leaks[month.key].created_at).toLocaleDateString('pt-BR')}
                                        </span>
                                    ) : (
                                        <span className="text-gray-500">-</span>
                                    )}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {/* Informações */}
            <div className="mt-6 bg-gray-700 rounded-lg p-4">
                <h3 className="text-lg font-semibold text-red-400 mb-2">Sobre as Análises de Leaks</h3>
                <ul className="text-gray-300 text-sm space-y-1">
                    <li>• Aqui você encontra as análises mensais dos seus leaks</li>
                    <li>• As análises são feitas pelos administradores</li>
                    <li>• Clique na imagem para visualizar em tamanho completo</li>
                    <li>• As melhorias sugeridas te ajudarão a evoluir no poker</li>
                    <li>• Foque nas melhorias indicadas para cada mês</li>
                </ul>
            </div>

            {/* Modal de Zoom */}
            <ImageZoomModal
                isOpen={zoomModal.isOpen}
                onClose={closeZoomModal}
                imageUrl={zoomModal.imageUrl}
                altText={zoomModal.altText}
            />
        </div>
    );
};

export default LeakHunting;
