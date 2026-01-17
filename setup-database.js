// Script para criar as tabelas no Supabase
const { Client } = require('pg');

const DATABASE_URL = 'postgresql://postgres:Grinders15935!@db.hwizxjbufsiviuxelahh.supabase.co:5432/postgres';

const schema = `
-- Tabela de Particoes
CREATE TABLE IF NOT EXISTS particoes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    descricao TEXT,
    ativa BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tabela de Usuarios
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    type VARCHAR(20) DEFAULT 'student' CHECK (type IN ('admin', 'student')),
    particao_id INTEGER REFERENCES particoes(id),
    first_login BOOLEAN DEFAULT TRUE,
    register_date TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);

-- Tabela de Aulas
CREATE TABLE IF NOT EXISTS classes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    instructor_id INTEGER REFERENCES users(id),
    date DATE NOT NULL,
    category VARCHAR(20) CHECK (category IN ('iniciantes', 'preflop', 'postflop', 'mental', 'icm')),
    video_url TEXT,
    video_duration INTEGER,
    priority INTEGER DEFAULT 5,
    views INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabela de Progresso
CREATE TABLE IF NOT EXISTS user_progress (
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    class_id INTEGER REFERENCES classes(id) ON DELETE CASCADE,
    progress INTEGER DEFAULT 0,
    watched BOOLEAN DEFAULT FALSE,
    video_time FLOAT DEFAULT 0,
    last_watched TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (user_id, class_id)
);

-- Tabela de Favoritos
CREATE TABLE IF NOT EXISTS favorites (
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    class_id INTEGER REFERENCES classes(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (user_id, class_id)
);

-- Tabela de Visualizacoes
CREATE TABLE IF NOT EXISTS class_views (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    class_id INTEGER REFERENCES classes(id) ON DELETE CASCADE,
    viewed_at TIMESTAMP DEFAULT NOW(),
    ip_address VARCHAR(45),
    user_agent TEXT
);

-- Tabela de Playlists
CREATE TABLE IF NOT EXISTS playlists (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabela de Aulas nas Playlists
CREATE TABLE IF NOT EXISTS playlist_classes (
    playlist_id INTEGER REFERENCES playlists(id) ON DELETE CASCADE,
    class_id INTEGER REFERENCES classes(id) ON DELETE CASCADE,
    PRIMARY KEY (playlist_id, class_id)
);

-- Tabela de Graficos
CREATE TABLE IF NOT EXISTS student_graphs (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    month VARCHAR(3) CHECK (month IN ('jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez')),
    year INTEGER NOT NULL,
    image_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(student_id, month, year)
);

-- Tabela de Leaks
CREATE TABLE IF NOT EXISTS student_leaks (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    month VARCHAR(3) CHECK (month IN ('jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez')),
    year INTEGER NOT NULL,
    image_url TEXT,
    improvements TEXT,
    uploaded_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(student_id, month, year)
);

-- Indices
CREATE INDEX IF NOT EXISTS idx_classes_category ON classes(category);
CREATE INDEX IF NOT EXISTS idx_classes_date ON classes(date);
CREATE INDEX IF NOT EXISTS idx_user_progress_user ON user_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_class_views_class ON class_views(class_id);
CREATE INDEX IF NOT EXISTS idx_users_type ON users(type);
CREATE INDEX IF NOT EXISTS idx_users_particao ON users(particao_id);
`;

const seedData = `
-- Particao padrao
INSERT INTO particoes (nome, descricao)
VALUES ('Principal', 'Particao principal do time')
ON CONFLICT (nome) DO NOTHING;

-- Admin padrao (senha: admin123)
INSERT INTO users (name, username, email, password_hash, type, particao_id, first_login)
VALUES (
    'Administrador',
    'admin',
    'admin@cardroomgrinders.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTtYr/EKsHsHWK',
    'admin',
    1,
    TRUE
)
ON CONFLICT (username) DO NOTHING;
`;

async function setupDatabase() {
    const client = new Client({ connectionString: DATABASE_URL, ssl: { rejectUnauthorized: false } });

    try {
        console.log('Conectando ao Supabase...');
        await client.connect();
        console.log('Conectado!');

        console.log('Criando tabelas...');
        await client.query(schema);
        console.log('Tabelas criadas!');

        console.log('Inserindo dados iniciais...');
        await client.query(seedData);
        console.log('Dados inseridos!');

        // Verificar tabelas
        const result = await client.query(`
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name
        `);

        console.log('\\nTabelas criadas:');
        result.rows.forEach(row => console.log('  - ' + row.table_name));

        console.log('\\n✅ Setup concluido com sucesso!');
        console.log('\\nAdmin criado:');
        console.log('  Usuario: admin');
        console.log('  Senha: admin123');
        console.log('  (Troque a senha apos o primeiro login!)');

    } catch (err) {
        console.error('Erro:', err.message);
    } finally {
        await client.end();
    }
}

setupDatabase();
