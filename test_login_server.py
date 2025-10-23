#!/usr/bin/env python3
"""
Script para testar login no servidor
"""

import paramiko
import time
import json

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"
SSH_PORT = 22

def execute_command(client, command, timeout=120):
    """Executa um comando via SSH"""
    print(f"\n📝 Executando: {command}")
    stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
    time.sleep(2)
    
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    
    if output:
        print(output)
    
    return output, error

def test_login():
    """Testa login"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar status do backend
        print("📝 Status do backend:")
        output, _ = execute_command(client, "docker ps | grep poker_backend")
        print(output)
        
        # Verificar logs
        print("\n📝 Últimos logs do backend:")
        output, _ = execute_command(client, "docker logs poker_backend 2>&1 | tail -20")
        print(output)
        
        # Testar health check
        print("\n📝 Testando health check:")
        output, _ = execute_command(client, "docker exec poker_backend curl -s http://localhost:5000/api/health")
        print(output)
        
        # Testar login
        print("\n📝 Testando login com admin/admin123:")
        output, _ = execute_command(client, """docker exec poker_backend curl -s -X POST http://localhost:5000/api/auth/login -H 'Content-Type: application/json' -d '{"username":"admin","password":"admin123"}'""")
        print(output)
        
        # Verificar se tem token
        if '"token"' in output:
            print("\n✅ LOGIN BEM-SUCEDIDO!")
        else:
            print("\n❌ LOGIN FALHOU!")
            
            # Verificar senha no banco
            print("\n📝 Verificando senha no banco:")
            output, _ = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT username, password_hash FROM users WHERE username='admin' LIMIT 1;\"")
            print(output)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_login()

