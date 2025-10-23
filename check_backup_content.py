#!/usr/bin/env python3
"""
Script para verificar conteúdo dos backups
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

def check_backups():
    """Verifica backups"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        backups = [
            "/root/Dojo_Deploy/poker_academy_backup_20251016_022151.sql",
            "/root/Dojo_Deploy/poker_academy_backup_20251016_021922.sql",
            "/root/Dojo_Deploy/poker_academy_backup_20251016_021447.sql"
        ]
        
        for backup in backups:
            print(f"\n{'='*60}")
            print(f"📝 Verificando: {backup}")
            print(f"{'='*60}")
            
            # Contar linhas
            output, _ = execute_command(client, f"wc -l {backup}")
            
            # Procurar INSERT de students
            output, _ = execute_command(client, f"grep -c \"INSERT INTO.*users\" {backup} || echo '0'")
            
            # Mostrar alguns INSERTs
            output, _ = execute_command(client, f"grep \"INSERT INTO.*users\" {backup} | head -3")
            
            # Contar quantos students tem
            output, _ = execute_command(client, f"grep \"'student'\" {backup} | wc -l")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_backups()

