#!/usr/bin/env python3
"""
Script para verificar triggers e corrigir
"""

import paramiko
import time

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"
SSH_PORT = 22

def execute_command(client, command, timeout=120):
    """Executa um comando via SSH"""
    stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
    time.sleep(2)
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    return output, error

def check():
    """Verifica"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar triggers
        print("📝 Verificando triggers na tabela users:")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SHOW TRIGGERS WHERE `Table` = 'users';\"")
        print(output if output else "Nenhum trigger encontrado")
        
        # Verificar constraints
        print("\n📝 Verificando constraints:")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT CONSTRAINT_NAME, CONSTRAINT_TYPE FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS WHERE TABLE_NAME='users';\"")
        print(output)
        
        # Verificar se há coluna com mesmo nome
        print("\n📝 Verificando todas as colunas da tabela users:")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SHOW COLUMNS FROM users;\"")
        print(output)
        
        # Tentar com INSERT novo
        print("\n📝 Testando INSERT com novo usuário...")
        test_hash = "pbkdf2:sha256:260000$J4eEjERUmAApf7zW$b5eaf9c5fd42d0b24bbff7dc306236dfe78dd513aaaa3649499d04db060ae49b"
        sql = f"""INSERT INTO users (name, username, email, password_hash, type, particao_id) 
VALUES ('Test User', 'testuser123', 'test@test.com', '{test_hash}', 'admin', 1);
SELECT username, LENGTH(password_hash) as len, password_hash FROM users WHERE username='testuser123';"""
        
        cmd = f"docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"{sql}\""
        output, error = execute_command(client, cmd)
        print(output)
        
        # Verificar se o problema é com UPDATE
        print("\n📝 Testando UPDATE com CAST...")
        sql = f"UPDATE users SET password_hash = CAST('{test_hash}' AS CHAR(500)) WHERE username = 'admin';"
        cmd = f"docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"{sql}\""
        output, error = execute_command(client, cmd)
        
        # Verificar resultado
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT username, LENGTH(password_hash) as len, password_hash FROM users WHERE username='admin';\"")
        print(output)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check()

