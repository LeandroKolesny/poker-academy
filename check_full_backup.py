#!/usr/bin/env python3
"""
Script para verificar backup completo
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

def check_backup():
    """Verifica backup"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Descompactar backup
        print("📝 Descompactando backup:")
        output, _ = execute_command(client, "cd /tmp && gunzip -c /root/Dojo_Deploy/poker-academy/full-database-backup-20251016_163317.sql.gz > full-database-backup.sql && echo 'Descompactado'")
        
        # Contar linhas
        print("\n📝 Tamanho do backup:")
        output, _ = execute_command(client, "wc -l /tmp/full-database-backup.sql")
        
        # Contar INSERTs de users
        print("\n📝 Contando INSERTs de users:")
        output, _ = execute_command(client, "grep -c 'INSERT INTO.*users' /tmp/full-database-backup.sql || echo '0'")
        
        # Contar students
        print("\n📝 Contando students:")
        output, _ = execute_command(client, "grep -c \"'student'\" /tmp/full-database-backup.sql || echo '0'")
        
        # Mostrar INSERTs de users
        print("\n📝 Mostrando INSERTs de users:")
        output, _ = execute_command(client, "grep 'INSERT INTO.*users' /tmp/full-database-backup.sql | head -5")
        
        # Contar classes
        print("\n📝 Contando classes:")
        output, _ = execute_command(client, "grep -c 'INSERT INTO.*classes' /tmp/full-database-backup.sql || echo '0'")
        
        # Mostrar INSERTs de classes
        print("\n📝 Mostrando INSERTs de classes:")
        output, _ = execute_command(client, "grep 'INSERT INTO.*classes' /tmp/full-database-backup.sql | head -3")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_backup()

