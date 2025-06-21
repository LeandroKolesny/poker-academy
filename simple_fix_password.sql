-- =====================================================
-- SCRIPT PARA VERIFICAR E CORRIGIR SENHA DO ALUNO
-- =====================================================

USE poker_academy;

-- Ver usuários existentes
SELECT 'USUÁRIOS ATUAIS:' as info;
SELECT id, name, email, type, LEFT(password_hash, 20) as hash_preview FROM users;

-- Ver estrutura da tabela
SELECT 'ESTRUTURA DA TABELA:' as info;
DESCRIBE users;

-- Verificar aluno específico
SELECT 'DADOS DO ALUNO:' as info;
SELECT * FROM users WHERE email = 'aluno@pokeracademy.com';

-- Atualizar senha do aluno para 'aluno123'
-- Hash gerado: $2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C
UPDATE users 
SET password_hash = '$2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C'
WHERE email = 'aluno@pokeracademy.com';

-- Verificar se foi atualizado
SELECT 'APÓS ATUALIZAÇÃO:' as info;
SELECT id, name, email, type, LEFT(password_hash, 30) as hash_preview FROM users WHERE email = 'aluno@pokeracademy.com';

-- =====================================================
-- CREDENCIAIS FINAIS:
-- Email: aluno@pokeracademy.com
-- Senha: aluno123
-- =====================================================
