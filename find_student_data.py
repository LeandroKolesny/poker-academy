#!/usr/bin/env python3
"""
Script para procurar dados de students
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

def find_students():
    """Procura dados de students"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Procurar por arquivos com "student" no nome
        print("📝 Procurando arquivos com 'student' no nome:")
        output, _ = execute_command(client, "find /root -name '*student*' -type f 2>/dev/null | head -20")
        
        # Procurar por arquivos SQL que contenham INSERT de students
        print("\n📝 Procurando arquivos SQL com INSERT de students:")
        output, _ = execute_command(client, "grep -r \"'student'\" /root/Dojo_Deploy --include='*.sql' 2>/dev/null | head -20")
        
        # Procurar por arquivos de dump
        print("\n📝 Procurando arquivos de dump:")
        output, _ = execute_command(client, "find /root -name '*dump*' -o -name '*backup*' -type f 2>/dev/null | grep -i sql | head -20")
        
        # Verificar conteúdo de users_dump.sql
        print("\n📝 Conteúdo de users_dump.sql:")
        output, _ = execute_command(client, "cat /tmp/users_dump.sql | head -100")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    find_students()

