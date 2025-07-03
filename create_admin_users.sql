-- =====================================================
-- SCRIPT PARA CRIAR USUÁRIOS ADMIN
-- =====================================================
-- Senha padrão para todos: admin123
-- Hash bcrypt da senha: $2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C
-- Partição ID: 1
-- =====================================================

USE poker_academy;

-- Verificar partições disponíveis
SELECT 'PARTIÇÕES DISPONÍVEIS:' as info;
SELECT * FROM particoes;

-- Verificar usuários existentes antes
SELECT 'USUÁRIOS ANTES:' as info;
SELECT id, name, username, email, type FROM users WHERE type = 'admin';

-- =====================================================
-- INSERIR NOVOS USUÁRIOS ADMIN
-- =====================================================

-- Cademito
INSERT INTO users (name, username, email, password_hash, type, particao_id, register_date) 
VALUES ('Cademito', 'Cademito', 'Cademito@gmail.com', '$2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C', 'admin', 1, NOW());

-- Carlos.rox
INSERT INTO users (name, username, email, password_hash, type, particao_id, register_date) 
VALUES ('Carlos.rox', 'Carlos.rox', 'Carlos.rox@gmail.com', '$2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C', 'admin', 1, NOW());

-- Eiji
INSERT INTO users (name, username, email, password_hash, type, particao_id, register_date) 
VALUES ('Eiji', 'Eiji', 'Eiji@gmail.com', '$2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C', 'admin', 1, NOW());

-- Jonas
INSERT INTO users (name, username, email, password_hash, type, particao_id, register_date) 
VALUES ('Jonas', 'Jonas', 'Jonas@gmail.com', '$2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C', 'admin', 1, NOW());

-- Harnefer
INSERT INTO users (name, username, email, password_hash, type, particao_id, register_date) 
VALUES ('Harnefer', 'Harnefer', 'Harnefer@gmail.com', '$2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C', 'admin', 1, NOW());

-- Pseudo Fruto
INSERT INTO users (name, username, email, password_hash, type, particao_id, register_date) 
VALUES ('Pseudo Fruto', 'Pseudo Fruto', 'Pseudo.Fruto@gmail.com', '$2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C', 'admin', 1, NOW());

-- LeoFranco
INSERT INTO users (name, username, email, password_hash, type, particao_id, register_date) 
VALUES ('LeoFranco', 'LeoFranco', 'LeoFranco@gmail.com', '$2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C', 'admin', 1, NOW());

-- Badinha
INSERT INTO users (name, username, email, password_hash, type, particao_id, register_date) 
VALUES ('Badinha', 'Badinha', 'Badinha@gmail.com', '$2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C', 'admin', 1, NOW());

-- Jose Lucas
INSERT INTO users (name, username, email, password_hash, type, particao_id, register_date) 
VALUES ('Jose Lucas', 'Jose Lucas', 'Jose.Lucas@gmail.com', '$2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C', 'admin', 1, NOW());

-- Nanatopai
INSERT INTO users (name, username, email, password_hash, type, particao_id, register_date) 
VALUES ('Nanatopai', 'Nanatopai', 'Nanatopai@gmail.com', '$2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C', 'admin', 1, NOW());

-- Luandods
INSERT INTO users (name, username, email, password_hash, type, particao_id, register_date) 
VALUES ('Luandods', 'Luandods', 'Luandods@gmail.com', '$2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C', 'admin', 1, NOW());

-- Lenon318
INSERT INTO users (name, username, email, password_hash, type, particao_id, register_date) 
VALUES ('Lenon318', 'Lenon318', 'Lenon318@gmail.com', '$2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C', 'admin', 1, NOW());

-- Danton
INSERT INTO users (name, username, email, password_hash, type, particao_id, register_date) 
VALUES ('Danton', 'Danton', 'Danton@gmail.com', '$2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C', 'admin', 1, NOW());

-- Jwolter
INSERT INTO users (name, username, email, password_hash, type, particao_id, register_date) 
VALUES ('Jwolter', 'Jwolter', 'Jwolter@gmail.com', '$2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C', 'admin', 1, NOW());

-- Gabriel
INSERT INTO users (name, username, email, password_hash, type, particao_id, register_date) 
VALUES ('Gabriel', 'Gabriel', 'Gabriel@gmail.com', '$2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C', 'admin', 1, NOW());

-- Ruan Bispo
INSERT INTO users (name, username, email, password_hash, type, particao_id, register_date) 
VALUES ('Ruan Bispo', 'Ruan Bispo', 'Ruan.Bispo@gmail.com', '$2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C', 'admin', 1, NOW());

-- Morfeu90
INSERT INTO users (name, username, email, password_hash, type, particao_id, register_date) 
VALUES ('Morfeu90', 'Morfeu90', 'Morfeu90@gmail.com', '$2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C', 'admin', 1, NOW());

-- Biguethi
INSERT INTO users (name, username, email, password_hash, type, particao_id, register_date) 
VALUES ('Biguethi', 'Biguethi', 'Biguethi@gmail.com', '$2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C', 'admin', 1, NOW());

-- Tgrinder
INSERT INTO users (name, username, email, password_hash, type, particao_id, register_date) 
VALUES ('Tgrinder', 'Tgrinder', 'Tgrinder@gmail.com', '$2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C', 'admin', 1, NOW());

-- Quadskilla
INSERT INTO users (name, username, email, password_hash, type, particao_id, register_date) 
VALUES ('Quadskilla', 'Quadskilla', 'Quadskilla@gmail.com', '$2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C', 'admin', 1, NOW());

-- Kapirov
INSERT INTO users (name, username, email, password_hash, type, particao_id, register_date) 
VALUES ('Kapirov', 'Kapirov', 'Kapirov@gmail.com', '$2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C', 'admin', 1, NOW());

-- =====================================================
-- VERIFICAR RESULTADO
-- =====================================================

-- Ver todos os usuários admin criados
SELECT 'USUÁRIOS ADMIN CRIADOS:' as info;
SELECT id, name, username, email, type, particao_id, register_date FROM users WHERE type = 'admin' ORDER BY id;

-- Contar total de admins
SELECT 'TOTAL DE ADMINS:' as info, COUNT(*) as total FROM users WHERE type = 'admin';

-- =====================================================
-- CREDENCIAIS DE LOGIN
-- =====================================================
-- TODOS OS USUÁRIOS ADMIN TÊM:
-- Senha: admin123
-- Username: igual ao nome
-- Email: nome@gmail.com
-- =====================================================
