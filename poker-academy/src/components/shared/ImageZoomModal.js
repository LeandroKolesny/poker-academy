import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearchPlus, faSearchMinus, faTimes, faExpand, faCompress } from '@fortawesome/free-solid-svg-icons';

const ImageZoomModal = ({ isOpen, onClose, imageUrl, altText }) => {
    const [zoom, setZoom] = useState(1);
    const [position, setPosition] = useState({ x: 0, y: 0 });
    const [isDragging, setIsDragging] = useState(false);
    const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
    const [isFullscreen, setIsFullscreen] = useState(false);

    // Reset zoom e posição quando modal abre/fecha
    useEffect(() => {
        if (isOpen) {
            setZoom(1);
            setPosition({ x: 0, y: 0 });
            setIsFullscreen(false);
        }
    }, [isOpen]);

    // Fechar modal com ESC
    useEffect(() => {
        const handleKeyDown = (e) => {
            if (e.key === 'Escape') {
                onClose();
            }
        };

        if (isOpen) {
            document.addEventListener('keydown', handleKeyDown);
            document.body.style.overflow = 'hidden';
        }

        return () => {
            document.removeEventListener('keydown', handleKeyDown);
            document.body.style.overflow = 'unset';
        };
    }, [isOpen, onClose]);

    const handleZoomIn = () => {
        setZoom(prev => Math.min(prev + 0.25, 5));
    };

    const handleZoomOut = () => {
        setZoom(prev => Math.max(prev - 0.25, 0.25));
    };

    const handleResetZoom = () => {
        setZoom(1);
        setPosition({ x: 0, y: 0 });
    };

    const handleMouseDown = (e) => {
        if (zoom > 1) {
            setIsDragging(true);
            setDragStart({
                x: e.clientX - position.x,
                y: e.clientY - position.y
            });
        }
    };

    const handleMouseMove = (e) => {
        if (isDragging && zoom > 1) {
            setPosition({
                x: e.clientX - dragStart.x,
                y: e.clientY - dragStart.y
            });
        }
    };

    const handleMouseUp = () => {
        setIsDragging(false);
    };

    const toggleFullscreen = () => {
        setIsFullscreen(!isFullscreen);
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-90">
            {/* Overlay para fechar */}
            <div 
                className="absolute inset-0 cursor-pointer"
                onClick={onClose}
            />
            
            {/* Container do modal */}
            <div className={`relative ${isFullscreen ? 'w-full h-full' : 'max-w-[90vw] max-h-[90vh]'} flex flex-col`}>
                {/* Barra de ferramentas */}
                <div className="absolute top-4 left-4 right-4 z-10 flex justify-between items-center">
                    <div className="flex gap-2">
                        {/* Botões de zoom */}
                        <button
                            onClick={handleZoomIn}
                            className="bg-gray-800 bg-opacity-80 text-white p-2 rounded hover:bg-opacity-100 transition-all"
                            title="Zoom In"
                        >
                            <FontAwesomeIcon icon={faSearchPlus} />
                        </button>
                        <button
                            onClick={handleZoomOut}
                            className="bg-gray-800 bg-opacity-80 text-white p-2 rounded hover:bg-opacity-100 transition-all"
                            title="Zoom Out"
                        >
                            <FontAwesomeIcon icon={faSearchMinus} />
                        </button>
                        <button
                            onClick={handleResetZoom}
                            className="bg-gray-800 bg-opacity-80 text-white px-3 py-2 rounded hover:bg-opacity-100 transition-all text-sm"
                            title="Reset Zoom"
                        >
                            {Math.round(zoom * 100)}%
                        </button>
                        <button
                            onClick={toggleFullscreen}
                            className="bg-gray-800 bg-opacity-80 text-white p-2 rounded hover:bg-opacity-100 transition-all"
                            title={isFullscreen ? "Sair do Fullscreen" : "Fullscreen"}
                        >
                            <FontAwesomeIcon icon={isFullscreen ? faCompress : faExpand} />
                        </button>
                    </div>
                    
                    {/* Botão fechar */}
                    <button
                        onClick={onClose}
                        className="bg-red-600 bg-opacity-80 text-white p-2 rounded hover:bg-opacity-100 transition-all"
                        title="Fechar"
                    >
                        <FontAwesomeIcon icon={faTimes} />
                    </button>
                </div>

                {/* Container da imagem */}
                <div 
                    className={`flex-1 flex items-center justify-center overflow-hidden ${
                        zoom > 1 ? 'cursor-move' : 'cursor-default'
                    }`}
                    onMouseDown={handleMouseDown}
                    onMouseMove={handleMouseMove}
                    onMouseUp={handleMouseUp}
                    onMouseLeave={handleMouseUp}
                >
                    <img
                        src={imageUrl}
                        alt={altText}
                        className="max-w-none transition-transform duration-200 select-none"
                        style={{
                            transform: `scale(${zoom}) translate(${position.x / zoom}px, ${position.y / zoom}px)`,
                            transformOrigin: 'center center'
                        }}
                        draggable={false}
                    />
                </div>

                {/* Instruções */}
                <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 bg-gray-800 bg-opacity-80 text-white px-4 py-2 rounded text-sm">
                    {zoom > 1 ? 'Arraste para mover • ' : ''}ESC para fechar • Scroll para zoom
                </div>
            </div>
        </div>
    );
};

export default ImageZoomModal;
