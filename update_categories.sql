-- Script para atualizar categorias de aulas
-- Remove "torneos" e "cash", adiciona "icm"

USE poker_academy;

-- Primeiro, atualizar aulas existentes com categorias que serão removidas
-- Converter "torneos" para "icm" (ICM é mais relevante para torneios)
UPDATE classes SET category = 'icm' WHERE category = 'torneos';

-- Converter "cash" para "preflop" (ou outra categoria apropriada)
UPDATE classes SET category = 'preflop' WHERE category = 'cash';

-- Alterar o ENUM da tabela para remover categorias antigas e adicionar ICM
ALTER TABLE classes MODIFY COLUMN category ENUM('preflop', 'postflop', 'mental', 'icm') NOT NULL;

-- Verificar as mudanças
SELECT DISTINCT category FROM classes;

-- Mostrar estrutura da tabela atualizada
SHOW COLUMNS FROM classes LIKE 'category';
