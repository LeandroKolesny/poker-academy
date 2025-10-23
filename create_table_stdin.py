#!/usr/bin/env python3
"""
Script para criar a tabela user_progress usando stdin
"""

import paramiko
import time

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"
SSH_PORT = 22

def execute_command_with_stdin(client, command, stdin_data, timeout=120):
    """Executa um comando via SSH com stdin"""
    print(f"\n📝 Executando: {command}")
    stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
    
    # Enviar dados para stdin
    stdin.write(stdin_data)
    stdin.close()
    
    time.sleep(2)
    
    output = stdout.read().decode('utf-8', errors='replace')
    error = stderr.read().decode('utf-8', errors='replace')
    
    if output:
        print(output)
    if error and 'Warning' not in error:
        print(f"ERRO: {error}")
    
    return output, error

def create():
    """Create"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # SQL para criar a tabela
        sql = """SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS user_progress (
    user_id INT NOT NULL,
    class_id INT NOT NULL,
    progress INT NOT NULL DEFAULT 0,
    watched BOOLEAN NOT NULL DEFAULT FALSE,
    last_watched DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    video_time FLOAT NOT NULL DEFAULT 0.0,
    completed_at DATETIME NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, class_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
SHOW TABLES LIKE 'user_progress';
DESCRIBE user_progress;
"""
        
        # Passo 1: Criar tabela
        print("1️⃣ Criando tabela user_progress...")
        cmd = "docker exec -i poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy"
        execute_command_with_stdin(client, cmd, sql)
        
        # Passo 2: Verificar se foi criada
        print("\n2️⃣ Verificando se a tabela foi criada...")
        cmd = "docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e 'SHOW TABLES;'"
        stdin, stdout, stderr = client.exec_command(cmd, timeout=120)
        time.sleep(2)
        output = stdout.read().decode('utf-8', errors='replace')
        print(output)
        
        print("\n✅ CONCLUÍDO!")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create()

