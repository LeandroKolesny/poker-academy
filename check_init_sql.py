#!/usr/bin/env python3
"""
Script para verificar arquivo de inicialização SQL
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
        print(output[-3000:] if len(output) > 3000 else output)
    
    return output, error

def check_init():
    """Verifica arquivo de inicialização"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Procurar arquivo de inicialização
        print("📝 Procurando arquivo de inicialização SQL:")
        output, _ = execute_command(client, "find /root/Dojo_Deploy -name '*.sql' -type f | grep -i init")
        
        # Verificar conteúdo do arquivo de inicialização
        print("\n📝 Verificando conteúdo do arquivo de inicialização:")
        output, _ = execute_command(client, "cat /root/Dojo_Deploy/poker-academy/poker-academy-deploy/mysql/init/01-create-tables.sql | head -100")
        
        # Procurar por INSERT de students
        print("\n📝 Procurando INSERT de students:")
        output, _ = execute_command(client, "grep -n \"'student'\" /root/Dojo_Deploy/poker-academy/poker-academy-deploy/mysql/init/01-create-tables.sql | head -20")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_init()

