#!/usr/bin/env python3
"""
Script para criar tabelas faltantes
"""

import paramiko
import time

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"
SSH_PORT = 22

def execute_command(client, command, timeout=60):
    """Executa um comando via SSH"""
    stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
    time.sleep(2)
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    return output, error

def create():
    """Cria"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Criar tabela de classes
        print("📝 Criando tabela de classes...")
        sql = """
        CREATE TABLE IF NOT EXISTS classes (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            category ENUM('iniciantes','preflop','postflop','mental','icm') DEFAULT 'preflop',
            video_url VARCHAR(500),
            instructor_id INT,
            date DATETIME DEFAULT CURRENT_TIMESTAMP,
            views INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
        """
        
        cmd = f"docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"{sql}\""
        output, error = execute_command(client, cmd)
        print(output if output else "Tabela criada!")
        print("✅ Tabela de classes criada!\n")
        
        # Verificar tabelas
        print("📝 Verificando tabelas...")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SHOW TABLES;\"")
        print(output)
        
        # Verificar categorias
        print("\n📝 Verificando categorias...")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SHOW COLUMNS FROM classes WHERE Field='category';\"")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ TABELAS CRIADAS!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create()

