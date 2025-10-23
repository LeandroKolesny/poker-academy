#!/usr/bin/env python3
"""
Script para copiar models.py e class_routes.py e reiniciar backend
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
        
        # Copiar models.py
        print("📁 Copiando models.py...")
        local_models = os.path.abspath('poker-academy-backend/poker_academy_api/src/models.py')
        remote_models = '/root/Dojo_Deploy/poker-academy/poker-academy-backend/poker_academy_api/src/models.py'
        
        sftp = client.open_sftp()
        sftp.put(local_models, remote_models)
        sftp.close()
        print("✅ models.py copiado!")
        
        # Copiar class_routes.py
        print("\n📁 Copiando class_routes.py...")
        local_routes = os.path.abspath('poker-academy-backend/poker_academy_api/src/routes/class_routes.py')
        remote_routes = '/root/Dojo_Deploy/poker-academy/poker-academy-backend/poker_academy_api/src/routes/class_routes.py'
        
        sftp = client.open_sftp()
        sftp.put(local_routes, remote_routes)
        sftp.close()
        print("✅ class_routes.py copiado!")
        
        # Remover container antigo
        print("\n🗑️  Removendo container antigo...")
        execute_command(client, "docker rm -f poker_backend")
        
        # Iniciar
        print("\n🚀 Iniciando containers...")
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d")
        time.sleep(15)
        
        # Verificar status
        print("\n📝 Status dos containers:")
        execute_command(client, "docker ps")
        
        # Verificar logs do backend
        print("\n📝 Logs do backend:")
        execute_command(client, "docker logs poker_backend --tail 50")
        
        print("\n✅ BACKEND REINICIADO COM SUCESSO!")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    deploy()

