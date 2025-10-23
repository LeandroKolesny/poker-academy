#!/usr/bin/env python3
"""
Script para adicionar colunas faltantes no banco
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
    time.sleep(1)
    
    output = stdout.read().decode('utf-8', errors='replace')
    error = stderr.read().decode('utf-8', errors='replace')
    
    if output:
        print(output[-2000:] if len(output) > 2000 else output)
    
    return output, error

def add_columns():
    """Add columns"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Adicionar colunas
        print("📝 Adicionando colunas faltantes...")
        sql_commands = [
            "ALTER TABLE classes ADD COLUMN video_path VARCHAR(255) NULL;",
            "ALTER TABLE classes ADD COLUMN video_type ENUM('youtube', 'local') DEFAULT 'local';",
            "ALTER TABLE classes ADD COLUMN priority INT DEFAULT 5;"
        ]
        
        for sql in sql_commands:
            cmd = f"docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e \"{sql}\""
            print(f"\n📝 Executando: {sql}")
            output, _ = execute_command(client, cmd)
        
        # Verificar estrutura
        print("\n📝 Verificando estrutura da tabela:")
        execute_command(client, "docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e \"DESCRIBE classes;\"")
        
        print("\n✅ COLUNAS ADICIONADAS!")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    add_columns()

