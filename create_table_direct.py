#!/usr/bin/env python3
"""
Script para criar a tabela user_progress diretamente
"""

import paramiko
import time

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"
SSH_PORT = 22

def execute_command(client, command, timeout=120):
    """Executa um comando via SSH"""
    print(f"\n📝 Executando: {command}")
    stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
    time.sleep(2)
    
    output = stdout.read().decode('utf-8', errors='replace')
    error = stderr.read().decode('utf-8', errors='replace')
    
    if output:
        print(output)
    if error:
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
        
        # Criar a tabela diretamente
        print("1️⃣ Criando tabela user_progress...")
        sql_commands = [
            "SET NAMES utf8mb4;",
            "SET CHARACTER SET utf8mb4;",
            """CREATE TABLE IF NOT EXISTS user_progress (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;""",
            "SHOW TABLES LIKE 'user_progress';",
            "DESCRIBE user_progress;"
        ]
        
        # Juntar todos os comandos SQL
        sql_script = "\n".join(sql_commands)

        # Criar arquivo temporário
        local_file = 'create_table.sql'
        with open(local_file, 'w', encoding='utf-8') as f:
            f.write(sql_script)

        # Copiar arquivo para servidor
        print("2️⃣ Copiando arquivo SQL para servidor...")
        sftp = client.open_sftp()
        sftp.put(local_file, '/tmp/create_table.sql')
        sftp.close()
        
        # Executar arquivo SQL
        print("3️⃣ Executando arquivo SQL...")
        cmd = """docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy < /tmp/create_table.sql"""
        execute_command(client, cmd)
        
        print("\n✅ TABELA CRIADA COM SUCESSO!")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create()

