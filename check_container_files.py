#!/usr/bin/env python3
"""
Script para verificar arquivos dentro do container
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

def check():
    """Verifica"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar arquivo dentro do container
        print("📝 Verificando arquivo dentro do container:")
        output, _ = execute_command(client, "docker exec poker_frontend ls -lh /usr/share/nginx/html/static/js/main.*.js")
        
        # Verificar se contém a correção
        print("\n📝 Procurando pela correção no arquivo do container:")
        output, _ = execute_command(client, "docker exec poker_frontend grep -o 'includes.*T' /usr/share/nginx/html/static/js/main.*.js | head -1")
        
        if output and "includes" in output:
            print("\n✅ CORREÇÃO ESTÁ NO CONTAINER!")
        else:
            print("\n❌ Correção NÃO está no container")
            print("\n📝 Verificando arquivo fonte no container:")
            output, _ = execute_command(client, "docker exec poker_frontend grep -A 3 'handleEditClass' /app/src/components/admin/ClassManagement.js | head -10")
        
        # Verificar data do arquivo
        print("\n📝 Data do arquivo no container:")
        output, _ = execute_command(client, "docker exec poker_frontend ls -lh /app/src/components/admin/ClassManagement.js")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check()

