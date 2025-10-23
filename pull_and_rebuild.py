#!/usr/bin/env python3
"""
Script para fazer pull e reconstruir
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

def rebuild():
    """Reconstrói"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Parar containers
        print("📝 Parando containers...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose down")
        print("✅ Containers parados!")
        
        # Fazer pull
        print("\n📝 Fazendo pull do GitHub...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && git pull origin main")
        print(output if output else "Pull concluído!")
        
        # Verificar Dockerfile
        print("\n📝 Verificando Dockerfile...")
        output, error = execute_command(client, "cat /root/Dojo_Deploy/poker-academy/poker-academy-backend/Dockerfile | grep -A 5 'Instalar dependências'")
        print(output)
        
        # Remover imagens
        print("\n📝 Removendo imagens antigas...")
        output, error = execute_command(client, "docker rmi poker-academy_backend -f 2>/dev/null; true")
        print("✅ Imagens removidas!")
        
        # Reconstruir
        print("\n📝 Reconstruindo backend...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose build backend 2>&1 | tail -30", timeout=300)
        print(output)
        
        # Iniciar
        print("\n📝 Iniciando containers...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d")
        print("✅ Containers iniciados!")
        
        # Aguardar
        print("\n⏳ Aguardando 30 segundos...")
        time.sleep(30)
        
        # Verificar curl
        print("\n📝 Verificando curl...")
        output, error = execute_command(client, "docker exec poker_backend which curl")
        print(f"curl path: {output}")
        
        # Testar health check
        print("\n📝 Testando health check...")
        output, error = execute_command(client, "docker exec poker_backend curl -s http://localhost:5000/api/health")
        print(f"Response: {output}")
        
        # Testar login
        print("\n📝 Testando login...")
        output, error = execute_command(client, "docker exec poker_backend curl -s -X POST http://localhost:5000/api/auth/login -H 'Content-Type: application/json' -d '{\"username\":\"admin\",\"password\":\"admin123\"}'")
        print(f"Response: {output}")
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ PULL E REBUILD CONCLUÍDO!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    rebuild()

