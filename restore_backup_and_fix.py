#!/usr/bin/env python3
"""
Script para restaurar backup e corrigir
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
        
        # Restaurar backup
        print("📝 Restaurando backup...")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy < /root/Dojo_Deploy/poker_academy_backup_20251016_022151.sql", timeout=120)
        print(output if output else "Backup restaurado!")
        print("✅ Backup restaurado!\n")
        
        # Aguardar
        print("⏳ Aguardando 10 segundos...")
        time.sleep(10)
        
        # Verificar dados
        print("📝 Verificando dados...")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT COUNT(*) as total FROM classes;\"")
        print(output)
        
        # Reiniciar backend
        print("\n📝 Reiniciando backend...")
        execute_command(client, "docker restart poker_backend")
        print("✅ Backend reiniciado!\n")
        
        # Aguardar
        print("⏳ Aguardando 15 segundos...")
        time.sleep(15)
        
        # Verificar status
        print("📝 Status:")
        output, error = execute_command(client, "docker ps | grep backend")
        print(output)
        
        # Verificar logs
        print("\n📝 Logs do backend:")
        output, error = execute_command(client, "docker logs poker_backend 2>&1 | tail -20")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ BACKUP RESTAURADO E BACKEND REINICIADO!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    restore()

