-- Script para adicionar campo 'particao' na tabela users
-- Execute este script no MySQL/phpMyAdmin

USE poker_academy;

-- Adicionar coluna particao na tabela users
ALTER TABLE users ADD COLUMN particao VARCHAR(100) NOT NULL DEFAULT 'Dojo';

-- Atualizar todos os registros existentes com 'Dojo'
UPDATE users SET particao = 'Dojo' WHERE particao IS NULL OR particao = '';

-- Verificar se a alteração foi aplicada
SELECT id, name, username, email, type, particao FROM users;
