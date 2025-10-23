#!/usr/bin/env python3
"""
Script para fazer deploy da correção de partições
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
        print(output[-1500:] if len(output) > 1500 else output)
    
    return output, error

def deploy():
    """Deploy"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Copiar StudentManagement.js
        print("📁 Copiando StudentManagement.js...")
        local_file = os.path.abspath('poker-academy/src/components/admin/StudentManagement.js')
        remote_file = '/root/Dojo_Deploy/poker-academy/poker-academy/src/components/admin/StudentManagement.js'
        
        sftp = client.open_sftp()
        sftp.put(local_file, remote_file)
        sftp.close()
        print("✅ StudentManagement.js copiado!")
        
        # Fazer rebuild do frontend
        print("\n🔨 Fazendo rebuild do frontend...")
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose build --no-cache frontend", timeout=600)
        
        # Parar e iniciar containers
        print("\n🛑 Parando containers...")
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose down")
        time.sleep(5)
        
        print("\n🚀 Iniciando containers...")
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d")
        time.sleep(15)
        
        # Verificar status
        print("\n📝 Status dos containers:")
        execute_command(client, "docker ps")
        
        print("\n✅ DEPLOY COMPLETO!")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    deploy()

