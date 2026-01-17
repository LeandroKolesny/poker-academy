// src/utils/formatUtils.js
// Funcoes utilitarias para formatacao de valores

/**
 * Formata tamanho de arquivo para exibicao legivel
 * @param {number} bytes - Tamanho em bytes
 * @returns {string} Tamanho formatado (ex: "1.5 MB")
 */
export const formatFileSize = (bytes) => {
    if (!bytes || bytes === 0) return 'N/A';

    const units = ['B', 'KB', 'MB', 'GB', 'TB'];
    let unitIndex = 0;
    let size = bytes;

    while (size >= 1024 && unitIndex < units.length - 1) {
        size /= 1024;
        unitIndex++;
    }

    return `${size.toFixed(2)} ${units[unitIndex]}`;
};

/**
 * Formata duracao em segundos para exibicao (MM:SS ou HH:MM:SS)
 * @param {number} seconds - Duracao em segundos
 * @returns {string} Duracao formatada
 */
export const formatDuration = (seconds) => {
    if (!seconds || seconds === 0) return '00:00';

    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);

    if (hrs > 0) {
        return `${hrs.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
};

/**
 * Formata numero para exibicao com separadores de milhar
 * @param {number} num - Numero a formatar
 * @returns {string} Numero formatado
 */
export const formatNumber = (num) => {
    if (num === null || num === undefined) return '0';
    return num.toLocaleString('pt-BR');
};

/**
 * Formata porcentagem
 * @param {number} value - Valor (0-100 ou 0-1)
 * @param {number} decimals - Casas decimais
 * @returns {string} Porcentagem formatada
 */
export const formatPercentage = (value, decimals = 1) => {
    if (value === null || value === undefined) return '0%';
    const percentage = value > 1 ? value : value * 100;
    return `${percentage.toFixed(decimals)}%`;
};

/**
 * Trunca texto com ellipsis
 * @param {string} text - Texto a truncar
 * @param {number} maxLength - Comprimento maximo
 * @returns {string} Texto truncado
 */
export const truncateText = (text, maxLength = 50) => {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength - 3) + '...';
};

export default {
    formatFileSize,
    formatDuration,
    formatNumber,
    formatPercentage,
    truncateText
};
