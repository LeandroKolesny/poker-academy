// src/utils/dateUtils.js
// Funcoes utilitarias para formatacao de datas

/**
 * Formata uma data para exibicao no formato brasileiro (DD/MM/YYYY)
 * @param {string|Date} dateString - Data a ser formatada
 * @returns {string} Data formatada ou 'N/A' se invalida
 */
export const formatDateForDisplay = (dateString) => {
    if (!dateString) return 'N/A';

    // Se for string no formato YYYY-MM-DD
    if (typeof dateString === 'string' && dateString.match(/^\d{4}-\d{2}-\d{2}$/)) {
        const [year, month, day] = dateString.split('-');
        const date = new Date(parseInt(year), parseInt(month) - 1, parseInt(day));
        return date.toLocaleDateString('pt-BR');
    }

    // Tenta criar uma data e formatar
    try {
        const date = new Date(dateString);
        if (isNaN(date.getTime())) return 'N/A';
        return date.toLocaleDateString('pt-BR');
    } catch {
        return 'N/A';
    }
};

/**
 * Formata a data da ultima visualizacao como tempo relativo
 * @param {string|Date} dateString - Data a ser formatada
 * @returns {string} Tempo relativo (ex: "Ha 3 dias") ou 'Nunca'
 */
export const formatLastWatched = (dateString) => {
    if (!dateString) return 'Nunca';

    try {
        const date = new Date(dateString);
        if (isNaN(date.getTime())) return 'Nunca';

        const now = new Date();
        const diffTime = Math.abs(now - date);
        const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

        if (diffDays === 0) return 'Hoje';
        if (diffDays === 1) return 'Ontem';
        if (diffDays < 7) return `Ha ${diffDays} dias`;
        if (diffDays < 30) return `Ha ${Math.floor(diffDays / 7)} semanas`;
        if (diffDays < 365) return `Ha ${Math.floor(diffDays / 30)} meses`;
        return `Ha ${Math.floor(diffDays / 365)} anos`;
    } catch {
        return 'Nunca';
    }
};

/**
 * Formata data e hora para exibicao
 * @param {string|Date} dateString - Data a ser formatada
 * @returns {string} Data e hora formatadas
 */
export const formatDateTime = (dateString) => {
    if (!dateString) return 'N/A';

    try {
        const date = new Date(dateString);
        if (isNaN(date.getTime())) return 'N/A';
        return date.toLocaleString('pt-BR');
    } catch {
        return 'N/A';
    }
};

/**
 * Retorna o ano atual
 * @returns {number} Ano atual
 */
export const getCurrentYear = () => new Date().getFullYear();

/**
 * Retorna o mes atual (0-11)
 * @returns {number} Mes atual
 */
export const getCurrentMonth = () => new Date().getMonth();

export default {
    formatDateForDisplay,
    formatLastWatched,
    formatDateTime,
    getCurrentYear,
    getCurrentMonth
};
