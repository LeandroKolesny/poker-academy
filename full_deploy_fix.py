#!/usr/bin/env python3
"""
Script para fazer deploy completo com fix de charset
"""

import paramiko
import time
import os

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
        print(output[-1000:] if len(output) > 1000 else output)
    
    return output, error

def deploy():
    """Deploy"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Copiar arquivo main.py
        print("📁 Copiando main.py...")
        local_file = os.path.abspath('poker-academy-backend/poker_academy_api/src/main.py')
        remote_file = '/root/Dojo_Deploy/poker-academy/poker-academy-backend/poker_academy_api/src/main.py'
        
        sftp = client.open_sftp()
        sftp.put(local_file, remote_file)
        sftp.close()
        print("✅ main.py copiado!")
        
        # Parar todos os containers
        print("\n🛑 Parando todos os containers...")
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose down")
        time.sleep(5)
        
        # Remover imagens
        print("\n🗑️ Removendo imagens...")
        execute_command(client, "docker rmi poker-academy_backend:latest poker-academy_frontend:latest 2>&1 || echo 'Imagens não encontradas'")
        time.sleep(2)
        
        # Iniciar containers
        print("\n🚀 Iniciando containers...")
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d")
        time.sleep(30)
        
        # Verificar status
        print("\n📊 Status dos containers...")
        execute_command(client, "docker ps | grep poker")
        
        print("\n✅ DEPLOY COMPLETO!")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    deploy()

