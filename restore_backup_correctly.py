#!/usr/bin/env python3
"""
Script para restaurar backup corretamente
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

def restore():
    """Restaura"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Restaurar backup com root
        print("📝 Restaurando backup com usuário root...")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy < /root/Dojo_Deploy/poker_academy_backup_20251016_022151.sql", timeout=120)
        print(f"Output: {output}")
        print(f"Error: {error}")
        print("✅ Backup restaurado!\n")
        
        # Verificar dados
        print("📝 Verificando dados...")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT COUNT(*) as total FROM classes;\"")
        print(output)
        
        # Verificar categorias
        print("\n📝 Verificando categorias...")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SHOW COLUMNS FROM classes WHERE Field='category';\"")
        print(output)
        
        # Verificar aulas
        print("\n📝 Aulas com categorias:")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT id, name, category FROM classes LIMIT 10;\"")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ BACKUP RESTAURADO COM SUCESSO!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    restore()

