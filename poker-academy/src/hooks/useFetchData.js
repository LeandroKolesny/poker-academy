// src/hooks/useFetchData.js
// Hook reutilizavel para busca de dados com loading e error states

import { useState, useEffect, useCallback } from 'react';

/**
 * Hook para buscar dados com gerenciamento automatico de loading/error
 * @param {Function} fetchFn - Funcao async que retorna os dados
 * @param {Array} dependencies - Array de dependencias para re-fetch
 * @param {Object} options - Opcoes adicionais
 * @returns {Object} { data, loading, error, refetch }
 */
export const useFetchData = (fetchFn, dependencies = [], options = {}) => {
    const {
        initialData = null,
        onSuccess = null,
        onError = null,
        enabled = true
    } = options;

    const [data, setData] = useState(initialData);
    const [loading, setLoading] = useState(enabled);
    const [error, setError] = useState(null);

    const fetch = useCallback(async () => {
        if (!enabled) return;

        setLoading(true);
        setError(null);

        try {
            const result = await fetchFn();
            setData(result);
            if (onSuccess) onSuccess(result);
        } catch (e) {
            const errorMessage = e.response?.data?.error || e.message || 'Erro ao carregar dados';
            setError(errorMessage);
            if (onError) onError(e);
            console.error('useFetchData error:', e);
        } finally {
            setLoading(false);
        }
    }, [fetchFn, enabled, onSuccess, onError]);

    useEffect(() => {
        fetch();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [...dependencies, enabled]);

    const refetch = useCallback(() => {
        fetch();
    }, [fetch]);

    return { data, loading, error, refetch, setData };
};

/**
 * Hook simplificado para buscar lista de dados
 * @param {Function} fetchFn - Funcao async que retorna array
 * @param {Array} dependencies - Dependencias
 * @returns {Object} { items, loading, error, refetch }
 */
export const useFetchList = (fetchFn, dependencies = []) => {
    const { data, loading, error, refetch, setData } = useFetchData(
        fetchFn,
        dependencies,
        { initialData: [] }
    );

    return {
        items: Array.isArray(data) ? data : [],
        loading,
        error,
        refetch,
        setItems: setData
    };
};

export default useFetchData;
