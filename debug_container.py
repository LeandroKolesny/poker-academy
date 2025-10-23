#!/usr/bin/env python3
"""
Script para debugar o container
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

def debug():
    """Debug"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Listar arquivos no container
        print("📁 Arquivos em /usr/share/nginx/html/:")
        output, _ = execute_command(client, "docker exec poker_frontend ls -la /usr/share/nginx/html/")
        
        # Listar arquivos em static
        print("\n📁 Arquivos em /usr/share/nginx/html/static/:")
        output, _ = execute_command(client, "docker exec poker_frontend ls -la /usr/share/nginx/html/static/")
        
        # Listar arquivos em js
        print("\n📁 Arquivos em /usr/share/nginx/html/static/js/:")
        output, _ = execute_command(client, "docker exec poker_frontend ls -la /usr/share/nginx/html/static/js/")
        
        # Verificar tamanho do arquivo
        print("\n📝 Tamanho do arquivo main:")
        output, _ = execute_command(client, "docker exec poker_frontend du -sh /usr/share/nginx/html/static/js/main.*.js")
        
        # Verificar conteúdo do arquivo (primeiras linhas)
        print("\n📝 Primeiras linhas do arquivo main:")
        output, _ = execute_command(client, "docker exec poker_frontend head -c 500 /usr/share/nginx/html/static/js/main.*.js")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug()

