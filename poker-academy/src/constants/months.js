// src/constants/months.js
// Array de meses centralizado para uso em todo o sistema

export const MONTHS = [
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

// Helper para obter nome do mes pela key
export const getMonthName = (key) => {
    const month = MONTHS.find(m => m.key === key);
    return month ? month.name : key;
};

// Helper para obter key do mes pelo indice (0-11)
export const getMonthKeyByIndex = (index) => {
    return MONTHS[index]?.key || null;
};

export default MONTHS;
