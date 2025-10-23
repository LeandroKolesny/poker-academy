#!/usr/bin/env python3
"""
Script para editar Dockerfile com sed
"""

import paramiko
import time

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"
SSH_PORT = 22

def execute_command(client, command):
    """Executa um comando via SSH"""
    stdin, stdout, stderr = client.exec_command(command)
    time.sleep(1)
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    return output, error

def edit():
    """Edita"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Fazer backup
        print("📝 Fazendo backup do Dockerfile...")
        output, error = execute_command(client, "cp /root/Dojo_Deploy/poker-academy-backend/Dockerfile /root/Dojo_Deploy/poker-academy-backend/Dockerfile.bak")
        print("✅ Backup feito!\n")
        
        # Editar com sed
        print("📝 Editando Dockerfile...")
        output, error = execute_command(client, "sed -i 's/mkdir -p uploads\\/videos logs/mkdir -p logs/g' /root/Dojo_Deploy/poker-academy-backend/Dockerfile")
        print("✅ Dockerfile editado!\n")
        
        # Verificar
        print("📋 Verificando Dockerfile:")
        output, error = execute_command(client, "cat /root/Dojo_Deploy/poker-academy-backend/Dockerfile | grep -A 5 'Criar diretórios'")
        print(output)
        
        client.close()
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    edit()

