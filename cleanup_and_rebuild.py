#!/usr/bin/env python3
"""
Script para limpar e fazer rebuild do backend
"""

import paramiko
import time

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"
SSH_PORT = 22

def execute_command(client, command, timeout=300):
    """Executa um comando via SSH"""
    print(f"\n📝 Executando: {command}")
    stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
    time.sleep(2)
    
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    
    if output:
        print(output)
    
    return output, error

def cleanup_and_rebuild():
    """Limpa e faz rebuild"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Remover container antigo
        print("🗑️  Removendo container antigo...")
        execute_command(client, "docker rm -f poker_backend 2>/dev/null || true")
        time.sleep(2)
        
        # Ir para diretório
        print("📂 Entrando no diretório /root/Dojo_Deploy/poker-academy...")
        
        # Parar e remover containers
        print("🛑 Parando containers...")
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose down")
        time.sleep(3)
        
        # Rebuild
        print("🔨 Fazendo rebuild...")
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose build --no-cache backend", timeout=600)
        time.sleep(2)
        
        # Iniciar
        print("🚀 Iniciando containers...")
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d")
        time.sleep(10)
        
        # Verificar status
        print("\n📝 Status dos containers:")
        output, _ = execute_command(client, "docker ps --format 'table {{.Names}}\\t{{.Status}}'")
        
        # Testar endpoint
        print("\n📝 Testando endpoint /api/test...")
        time.sleep(5)
        output, _ = execute_command(client, "docker exec poker_backend curl -s http://localhost:5000/api/test")
        print(output)
        
        # Testar endpoint de aulas
        print("\n📝 Testando endpoint /api/classes...")
        output, _ = execute_command(client, "docker exec poker_backend curl -s -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VyX3R5cGUiOiJhZG1pbiIsImV4cCI6MTc2MDcxNDQwMSwiaWF0IjoxNzYwNjI4MDAxfQ.5_5jeBrG76mnE3gCoDteEPJVMM4lifg1-ZqINfW6gu4' http://localhost:5000/api/classes")
        print(output)
        
        # Verificar logs
        print("\n📝 Logs do backend (últimas 50 linhas):")
        output, _ = execute_command(client, "docker logs poker_backend 2>&1 | tail -50")
        print(output)
        
        client.close()
        print("\n✅ Rebuild concluído!")
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    cleanup_and_rebuild()

