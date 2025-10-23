#!/usr/bin/env python3
"""
Script para criar a tabela class_views no servidor
"""
import paramiko
import time

def execute_command(client, command):
    """Executa um comando via SSH"""
    stdin, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode('utf-8', errors='replace')
    error = stderr.read().decode('utf-8', errors='replace')
    return output, error

def create_class_views_table():
    """Cria a tabela class_views no banco de dados"""
    
    # Conectar ao servidor
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    print("🔌 Conectando ao servidor...")
    client.connect('142.93.206.128', username='root', password='DojoShh159357')
    print("✅ Conectado!")
    
    # SQL para criar a tabela
    sql_commands = """
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

CREATE TABLE IF NOT EXISTS class_views (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    class_id INT NOT NULL,
    viewed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45) NULL,
    user_agent TEXT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE,
    INDEX idx_user_class (user_id, class_id),
    INDEX idx_class_views (class_id),
    INDEX idx_viewed_at (viewed_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SHOW TABLES LIKE 'class_views';
"""
    
    # Executar via docker exec
    print("\n📝 Criando tabela class_views...")
    
    # Usar docker exec com stdin
    command = f"""docker exec -i poker_mysql mysql -u poker_user -p'Dojo@Sql159357' poker_academy << 'EOF'
{sql_commands}
EOF
"""
    
    output, error = execute_command(client, command)
    
    print("\n📤 Output:")
    print(output)
    
    if error:
        print("\n⚠️  Stderr:")
        print(error)
    
    # Verificar se a tabela foi criada
    print("\n✅ Verificando se a tabela foi criada...")
    check_command = "docker exec poker_mysql mysql -u poker_user -p'Dojo@Sql159357' poker_academy -e 'DESCRIBE class_views;'"
    output, error = execute_command(client, check_command)
    
    print("\n📋 Estrutura da tabela:")
    print(output)
    
    if error:
        print("\n❌ Erro:")
        print(error)
    
    client.close()
    print("\n✅ Concluído!")

if __name__ == "__main__":
    create_class_views_table()

