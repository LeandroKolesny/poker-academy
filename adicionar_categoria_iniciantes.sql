-- Script para adicionar a categoria "iniciantes" ao banco de dados
-- Data: 16 de Outubro de 2025

USE poker_academy;

-- =====================================================
-- PASSO 1: Verificar categorias atuais
-- =====================================================
SELECT DISTINCT category FROM classes;

-- =====================================================
-- PASSO 2: Alterar o ENUM da tabela classes
-- =====================================================
-- Adicionar "iniciantes" ao ENUM de categorias
ALTER TABLE classes MODIFY COLUMN category ENUM('preflop', 'postflop', 'mental', 'torneos', 'cash', 'iniciantes') NOT NULL;

-- =====================================================
-- PASSO 3: Verificar se a alteração foi bem-sucedida
-- =====================================================
SHOW COLUMNS FROM classes LIKE 'category';

-- =====================================================
-- PASSO 4: Verificar categorias após alteração
-- =====================================================
SELECT DISTINCT category FROM classes;

-- =====================================================
-- RESULTADO ESPERADO:
-- - Coluna category agora aceita: preflop, postflop, mental, torneos, cash, iniciantes
-- - Todas as aulas existentes mantêm suas categorias
-- - Novas aulas podem ser criadas com a categoria "iniciantes"
-- =====================================================

