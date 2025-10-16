-- Script para adicionar a categoria "iniciantes" ao ENUM da tabela classes
-- Este script modifica a coluna 'category' da tabela 'classes' para incluir 'iniciantes'

USE poker_academy;

-- Verificar o ENUM atual
SELECT COLUMN_TYPE FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'classes' AND COLUMN_NAME = 'category';

-- Modificar a coluna category para adicionar 'iniciantes' como primeira opção
ALTER TABLE classes 
MODIFY COLUMN category ENUM('iniciantes', 'preflop', 'postflop', 'mental', 'torneos', 'cash') NOT NULL DEFAULT 'preflop';

-- Verificar se a alteração foi bem-sucedida
SELECT COLUMN_TYPE FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'classes' AND COLUMN_NAME = 'category';

-- Confirmar que a tabela foi atualizada
SHOW CREATE TABLE classes;

