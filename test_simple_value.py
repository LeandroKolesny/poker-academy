#!/usr/bin/env python3
"""
Script para testar com valor simples
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

def test():
    """Testa"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Teste 1: Valor simples
        print("📝 Teste 1: Inserindo valor simples...")
        sql = "UPDATE users SET password_hash = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789' WHERE username = 'admin';"
        cmd = f"docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"{sql}\""
        output, error = execute_command(client, cmd)
        
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT username, LENGTH(password_hash) as len, password_hash FROM users WHERE username='admin';\"")
        print(output)
        
        # Teste 2: Valor com $
        print("\n📝 Teste 2: Inserindo valor com $...")
        sql = "UPDATE users SET password_hash = 'pbkdf2:sha256:260000$J4eEjERUmAApf7zW$b5eaf9c5' WHERE username = 'admin';"
        cmd = f"docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"{sql}\""
        output, error = execute_command(client, cmd)
        
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT username, LENGTH(password_hash) as len, password_hash FROM users WHERE username='admin';\"")
        print(output)
        
        # Teste 3: Valor completo
        print("\n📝 Teste 3: Inserindo valor completo...")
        sql = "UPDATE users SET password_hash = 'pbkdf2:sha256:260000$J4eEjERUmAApf7zW$b5eaf9c5fd42d0b24bbff7dc306236dfe78dd513aaaa3649499d04db060ae49b' WHERE username = 'admin';"
        cmd = f"docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"{sql}\""
        output, error = execute_command(client, cmd)
        
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT username, LENGTH(password_hash) as len, password_hash FROM users WHERE username='admin';\"")
        print(output)
        
        # Teste 4: Verificar se há coluna oculta
        print("\n📝 Teste 4: Verificando estrutura completa...")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SHOW CREATE TABLE users\\G\"")
        print(output)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test()

