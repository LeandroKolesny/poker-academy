#!/usr/bin/env python3
"""
Script para verificar volumes antigos
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
        print(output)
    
    return output, error

def check_old_volumes():
    """Verifica volumes antigos"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Procurar volumes antigos
        print("📝 Procurando volumes antigos:")
        output, _ = execute_command(client, "ls -la /var/lib/docker/volumes/ | grep -i poker")
        
        # Procurar backups de volumes
        print("\n📝 Procurando backups de volumes:")
        output, _ = execute_command(client, "find /var/lib/docker/volumes -name '*mysql*' -o -name '*poker*' 2>/dev/null | head -20")
        
        # Verificar histórico de arquivos
        print("\n📝 Verificando arquivos recentes no /var/lib/mysql:")
        output, _ = execute_command(client, "find /var/lib/mysql/poker_academy -type f -mtime -1 2>/dev/null")
        
        # Procurar por arquivos deletados
        print("\n📝 Procurando por arquivos em /tmp:")
        output, _ = execute_command(client, "ls -la /tmp/ | grep -i poker")
        
        # Verificar se há backup em outro lugar
        print("\n📝 Procurando backups em /root:")
        output, _ = execute_command(client, "find /root -name '*poker*' -type f 2>/dev/null | grep -i backup")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_old_volumes()

