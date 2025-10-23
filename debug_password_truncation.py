#!/usr/bin/env python3
"""
Script para debugar truncação de senha
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

def debug():
    """Debuga"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar coluna
        print("📝 Informações da coluna password_hash:")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SHOW FULL COLUMNS FROM users WHERE Field='password_hash';\"")
        print(output)
        
        # Inserir hash de teste
        test_hash = "pbkdf2:sha256:260000$J4eEjERUmAApf7zW$b5eaf9c5fd42d0b24bbff7dc306236dfe78dd513aaaa3649499d04db060ae49b"
        print(f"\n📝 Hash de teste ({len(test_hash)} caracteres):")
        print(test_hash)
        
        # Inserir direto
        print("\n📝 Inserindo hash de teste...")
        escaped_hash = test_hash.replace("'", "\\'")
        sql = f"UPDATE users SET password_hash = '{escaped_hash}' WHERE username = 'admin' LIMIT 1;"
        cmd = f"docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"{sql}\""
        output, error = execute_command(client, cmd)
        print("✅ Inserido!")
        
        # Verificar o que foi armazenado
        print("\n📝 Verificando o que foi armazenado:")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT username, password_hash FROM users WHERE username='admin';\"")
        print(output)
        
        # Verificar tamanho
        print("\n📝 Verificando tamanho armazenado:")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT username, LENGTH(password_hash) as len, password_hash FROM users WHERE username='admin';\"")
        print(output)
        
        # Tentar com HEX
        print("\n📝 Verificando com HEX:")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT username, HEX(password_hash) FROM users WHERE username='admin';\"")
        print(output)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug()

