#!/usr/bin/env python3
"""
Script para criar rede e iniciar backend
"""

import paramiko
import time

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"
SSH_PORT = 22

def execute_command(client, command, timeout=120):
    """Executa um comando via SSH"""
    stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
    time.sleep(2)
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    return output, error

def start():
    """Inicia"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Criar rede
        print("📝 Criando rede poker_network...")
        execute_command(client, "docker network create poker_network 2>/dev/null || echo 'Rede já existe'")
        print("✅ Rede criada!\n")
        
        # Remover container antigo
        print("📝 Removendo container antigo...")
        execute_command(client, "docker rm -f poker_backend")
        print("✅ Removido!\n")
        
        # Iniciar backend com docker run
        print("📝 Iniciando backend com docker run...")
        cmd = """docker run -d \
  --name poker_backend \
  --network poker_network \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  -e DB_HOST=mysql \
  -e DB_USERNAME=poker_user \
  -e DB_PASSWORD=Dojo@Sql159357 \
  -e DB_NAME=poker_academy \
  -e DB_PORT=3306 \
  -v backend_uploads:/app/uploads \
  -v backend_logs:/app/logs \
  poker-academy_backend:latest"""
        
        output, error = execute_command(client, cmd, timeout=30)
        print(output)
        print("✅ Backend iniciado!\n")
        
        # Aguardar
        print("⏳ Aguardando 15 segundos...")
        time.sleep(15)
        
        # Verificar status
        print("📝 Status:")
        output, error = execute_command(client, "docker ps | grep backend")
        print(output)
        
        # Verificar logs
        print("\n📝 Logs do backend:")
        output, error = execute_command(client, "docker logs poker_backend 2>&1 | tail -30")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ BACKEND INICIADO!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    start()

