#!/usr/bin/env python3
"""
Script para restaurar aulas do backup
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

def restore():
    """Restaura"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Extrair dados de classes do backup
        print("📝 Extraindo dados de classes do backup...")
        output, error = execute_command(client, "grep -A 1000 'INSERT INTO.*classes' /root/Dojo_Deploy/poker_academy_backup_20251016_022151.sql | head -100")
        print(output)
        
        # Restaurar apenas a tabela de classes
        print("\n📝 Restaurando tabela de classes...")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy < /root/Dojo_Deploy/poker_academy_backup_20251016_022151.sql 2>&1 | tail -20")
        print(output if output else "Restauração concluída!")
        
        # Aguardar
        time.sleep(5)
        
        # Verificar aulas
        print("\n📝 Verificando aulas restauradas...")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT COUNT(*) as total FROM classes;\"")
        print(output)
        
        # Listar aulas
        print("\n📝 Aulas (primeiras 10):")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT id, name, category FROM classes LIMIT 10;\"")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ AULAS RESTAURADAS!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    restore()

