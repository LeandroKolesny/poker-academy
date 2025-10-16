-- Script para atualizar as categorias de aulas no banco de dados
-- Categorias: Iniciante, Pré-Flop, Pós-Flop, Mental Games, ICM

USE poker_academy;

-- 1. Verificar o ENUM atual
SELECT COLUMN_TYPE FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'classes' AND COLUMN_NAME = 'category';

-- 2. Converter aulas existentes com categorias antigas
-- Converter "torneos" para "icm"
UPDATE classes SET category = 'icm' WHERE category = 'torneos';

-- Converter "cash" para "preflop"
UPDATE classes SET category = 'preflop' WHERE category = 'cash';

-- 3. Alterar o ENUM da tabela para as novas categorias
ALTER TABLE classes 
MODIFY COLUMN category ENUM('iniciantes', 'preflop', 'postflop', 'mental', 'icm') 
NOT NULL DEFAULT 'preflop';

-- 4. Verificar se a alteração foi bem-sucedida
SELECT COLUMN_TYPE FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'classes' AND COLUMN_NAME = 'category';

-- 5. Verificar as categorias atuais nas aulas
SELECT DISTINCT category FROM classes ORDER BY category;

-- 6. Contar aulas por categoria
SELECT category, COUNT(*) as total FROM classes GROUP BY category ORDER BY category;

-- 7. Confirmar que a tabela foi atualizada
SHOW CREATE TABLE classes;

