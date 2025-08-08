-- Script de inicialização do banco de dados
-- Este arquivo será executado automaticamente quando o container MySQL for criado

USE poker_academy;

-- Criar tabela de partições
CREATE TABLE IF NOT EXISTS particoes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL UNIQUE,
    descricao TEXT,
    ativa BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Criar tabela de usuários
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    type ENUM('admin', 'student') NOT NULL DEFAULT 'student',
    particao_id INT NOT NULL,
    register_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME NULL,
    first_login BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (particao_id) REFERENCES particoes(id)
);

-- Inserir partições padrão
INSERT IGNORE INTO particoes (id, nome, descricao, ativa) VALUES 
(1, 'Dojo', 'Partição principal do Dojo', TRUE),
(2, 'Coco', 'Partição secundária Coco', TRUE);

-- Inserir usuário admin padrão (senha: 123456)
INSERT IGNORE INTO users (id, name, username, email, password_hash, type, particao_id) VALUES 
(1, 'Administrador', 'admin', 'admin@pokeracademy.com', 'pbkdf2:sha256:260000$LrByTYz3Nkjgy0gt$ae9ea8ce44f9b893d93899a8e1d9c759b19da59d584af4455137a1a1bbfeb7fe', 'admin', 1);

-- Criar tabela de gráficos mensais dos alunos
CREATE TABLE IF NOT EXISTS student_graphs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    month ENUM('jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez') NOT NULL,
    year INT NOT NULL,
    image_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_student_month_year (student_id, month, year)
);

-- Criar tabela de análises de leaks dos alunos
CREATE TABLE IF NOT EXISTS student_leaks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    month ENUM('jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez') NOT NULL,
    year INT NOT NULL,
    image_url TEXT NOT NULL,
    uploaded_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (uploaded_by) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_student_leak_month_year (student_id, month, year)
);

-- Criar índices para performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_type ON users(type);
CREATE INDEX IF NOT EXISTS idx_users_particao_id ON users(particao_id);
CREATE INDEX IF NOT EXISTS idx_particoes_ativa ON particoes(ativa);
CREATE INDEX IF NOT EXISTS idx_student_graphs_student_id ON student_graphs(student_id);
CREATE INDEX IF NOT EXISTS idx_student_graphs_year ON student_graphs(year);
CREATE INDEX IF NOT EXISTS idx_student_leaks_student_id ON student_leaks(student_id);
CREATE INDEX IF NOT EXISTS idx_student_leaks_uploaded_by ON student_leaks(uploaded_by);
CREATE INDEX IF NOT EXISTS idx_student_leaks_year ON student_leaks(year);
