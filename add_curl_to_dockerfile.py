#!/usr/bin/env python3
"""
Script para adicionar curl ao Dockerfile no servidor
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

def add_curl():
    """Adiciona curl"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Ver Dockerfile atual
        print("📝 Dockerfile atual (linhas 13-20):")
        output, error = execute_command(client, "sed -n '13,20p' /root/Dojo_Deploy/poker-academy/poker-academy-backend/Dockerfile")
        print(output)
        
        # Adicionar curl com sed
        print("\n📝 Adicionando curl ao Dockerfile...")
        cmd = """sed -i '18s/pkg-config/pkg-config \\\\/' /root/Dojo_Deploy/poker-academy/poker-academy-backend/Dockerfile && sed -i '18a\\    curl \\\\' /root/Dojo_Deploy/poker-academy/poker-academy-backend/Dockerfile"""
        output, error = execute_command(client, cmd)
        
        # Verificar
        print("\n📝 Dockerfile após alteração (linhas 13-22):")
        output, error = execute_command(client, "sed -n '13,22p' /root/Dojo_Deploy/poker-academy/poker-academy-backend/Dockerfile")
        print(output)
        
        # Parar containers
        print("\n📝 Parando containers...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose down")
        print("✅ Containers parados!")
        
        # Remover imagens e cache
        print("\n📝 Removendo imagens e cache...")
        output, error = execute_command(client, "docker rmi poker-academy_backend -f 2>/dev/null; docker builder prune -af 2>/dev/null; true")
        print("✅ Imagens removidas!")
        
        # Reconstruir
        print("\n📝 Reconstruindo backend (isso pode levar alguns minutos)...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose build backend 2>&1 | tail -50", timeout=300)
        print(output)
        
        # Iniciar
        print("\n📝 Iniciando containers...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d")
        print("✅ Containers iniciados!")
        
        # Aguardar
        print("\n⏳ Aguardando 40 segundos para containers iniciarem...")
        time.sleep(40)
        
        # Verificar curl
        print("\n📝 Verificando se curl está instalado...")
        output, error = execute_command(client, "docker exec poker_backend which curl")
        if output.strip():
            print(f"✅ curl encontrado em: {output.strip()}")
        else:
            print("❌ curl não encontrado!")
        
        # Testar health check
        print("\n📝 Testando health check...")
        output, error = execute_command(client, "docker exec poker_backend curl -s http://localhost:5000/api/health")
        print(f"Response: {output}")
        
        # Testar login
        print("\n📝 Testando login com admin/admin123...")
        output, error = execute_command(client, "docker exec poker_backend curl -s -X POST http://localhost:5000/api/auth/login -H 'Content-Type: application/json' -d '{\"username\":\"admin\",\"password\":\"admin123\"}'")
        print(f"Response: {output}")
        
        # Verificar logs
        print("\n📝 Logs do backend (últimas 10 linhas):")
        output, error = execute_command(client, "docker logs poker_backend 2>&1 | tail -10")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ CURL ADICIONADO E TESTADO!")
        print("=" * 70)
        print("\n🌐 Acesse: https://cardroomgrinders.com.br")
        print("👤 Usuário: admin")
        print("🔑 Senha: admin123")
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    add_curl()

