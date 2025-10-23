#!/usr/bin/env python3
"""
Script para encontrar backups
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

def find():
    """Encontra"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Procurar backups
        print("📝 Procurando backups em /root/Dojo_Deploy/...")
        output, error = execute_command(client, "find /root/Dojo_Deploy -name '*.sql' -type f -exec ls -lh {} \\;")
        print(output)
        
        # Procurar em outros locais
        print("\n📝 Procurando em /root/...")
        output, error = execute_command(client, "find /root -name '*.sql' -type f 2>/dev/null | head -20")
        print(output)
        
        # Verificar volumes do Docker
        print("\n📝 Volumes do Docker:")
        output, error = execute_command(client, "docker volume ls")
        print(output)
        
        # Verificar se há dados no volume
        print("\n📝 Conteúdo do volume backend_uploads:")
        output, error = execute_command(client, "docker run --rm -v backend_uploads:/data alpine ls -lh /data 2>&1 | head -20")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ BUSCA CONCLUÍDA!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    find()

