// src/constants/categories.js
// Categorias e cores centralizadas para uso em todo o sistema

export const CATEGORIES = [
    'iniciantes',
    'preflop',
    'postflop',
    'mental',
    'icm'
];

export const DEFAULT_CATEGORY = 'preflop';

export const CATEGORY_COLORS = {
    iniciantes: '#9B59B6',
    preflop: '#FF6B6B',
    postflop: '#4ECDC4',
    mental: '#45B7D1',
    icm: '#96CEB4'
};

// Mapa de normalizacao para categorias (aceita variações)
const CATEGORY_NORMALIZATION = {
    // Iniciantes
    'iniciantes': 'iniciantes',
    'iniciante': 'iniciantes',
    'beginner': 'iniciantes',
    'beginners': 'iniciantes',

    // Preflop
    'preflop': 'preflop',
    'pre-flop': 'preflop',
    'pre flop': 'preflop',

    // Postflop
    'postflop': 'postflop',
    'post-flop': 'postflop',
    'post flop': 'postflop',
    'posflop': 'postflop',

    // Mental
    'mental': 'mental',
    'mindset': 'mental',
    'psicologia': 'mental',

    // ICM
    'icm': 'icm',
    'torneio': 'icm',
    'torneios': 'icm',
    'tournament': 'icm'
};

// Normaliza uma categoria para o formato padrao
export const normalizeCategory = (category) => {
    if (!category) return DEFAULT_CATEGORY;
    const normalized = category.toLowerCase().trim();
    return CATEGORY_NORMALIZATION[normalized] || DEFAULT_CATEGORY;
};

// Obtem a cor de uma categoria
export const getCategoryColor = (category) => {
    const normalized = normalizeCategory(category);
    return CATEGORY_COLORS[normalized] || CATEGORY_COLORS[DEFAULT_CATEGORY];
};

// Verifica se uma categoria e valida
export const isValidCategory = (category) => {
    return CATEGORIES.includes(normalizeCategory(category));
};

export default CATEGORIES;
