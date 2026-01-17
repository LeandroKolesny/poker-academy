// src/constants/storage.js
// Chaves de localStorage centralizadas

export const STORAGE_KEYS = {
    TOKEN: 'token',
    REMEMBERED_CREDENTIALS: 'rememberedCredentials',
    USER_TYPE: 'userType',
    USER_DATA: 'userData',
    THEME: 'theme',
    LAST_ROUTE: 'lastRoute'
};

// Helpers para localStorage
export const storage = {
    get: (key) => {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : null;
        } catch {
            return localStorage.getItem(key);
        }
    },

    set: (key, value) => {
        try {
            const item = typeof value === 'string' ? value : JSON.stringify(value);
            localStorage.setItem(key, item);
        } catch (error) {
            console.error('Error saving to localStorage:', error);
        }
    },

    remove: (key) => {
        localStorage.removeItem(key);
    },

    clear: () => {
        localStorage.clear();
    }
};

export default STORAGE_KEYS;
