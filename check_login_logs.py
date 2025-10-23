#!/usr/bin/env python3
"""
Script para verificar logs de login
"""

import paramiko
import time

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"
SSH_PORT = 22

def execute_command(client, command, timeout=60):
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
        
        # Verificar logs do backend
        print("📝 Logs do backend (últimas 50 linhas):")
        output, error = execute_command(client, "docker logs poker_backend 2>&1 | tail -50")
        print(output)
        
        # Verificar status do backend
        print("\n📝 Status do backend:")
        output, error = execute_command(client, "docker ps | grep backend")
        print(output)
        
        # Testar endpoint de login
        print("\n📝 Testando endpoint de login...")
        output, error = execute_command(client, "docker exec poker_backend python -c \"import requests; r = requests.post('http://localhost:5000/api/login', json={'username': 'admin', 'password': 'admin123'}); print(r.status_code, r.text)\" 2>&1")
        print(output)
        
        # Verificar usuário no banco
        print("\n📝 Verificando usuário admin no banco:")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT id, username, type, password_hash FROM users WHERE username='admin';\"")
        print(output)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check()

