#!/usr/bin/env python3
"""
Script para verificar erro das aulas
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

def check():
    """Verifica"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Testar endpoint de aulas
        print("📝 Testando endpoint /api/classes...")
        output, error = execute_command(client, "docker exec poker_backend curl -s -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VyX3R5cGUiOiJhZG1pbiIsImV4cCI6MTc2MDcxNDQwMSwiaWF0IjoxNzYwNjI4MDAxfQ.5_5jeBrG76mnE3gCoDteEPJVMM4lifg1-ZqINfW6gu4' http://localhost:5000/api/classes")
        print(f"Response: {output}")
        
        # Verificar logs
        print("\n📝 Logs do backend (últimas 50 linhas):")
        output, error = execute_command(client, "docker logs poker_backend 2>&1 | tail -50")
        print(output)
        
        # Verificar se a tabela classes existe
        print("\n📝 Verificando tabela classes:")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"DESCRIBE classes;\"")
        print(output)
        
        # Verificar dados
        print("\n📝 Dados na tabela classes:")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT * FROM classes;\"")
        print(output)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check()

