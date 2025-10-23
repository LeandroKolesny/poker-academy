#!/usr/bin/env python3
"""
Script para testar login de verdade
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

def test():
    """Testa"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Aguardar backend ficar healthy
        print("⏳ Aguardando backend ficar healthy...")
        for i in range(30):
            output, error = execute_command(client, "docker ps | grep backend | grep healthy")
            if output:
                print(f"✅ Backend está healthy!\n")
                break
            print(f"  Tentativa {i+1}/30...")
            time.sleep(2)
        
        # Testar login via API
        print("📝 Testando login via API...")
        cmd = """docker exec poker_backend python << 'EOF'
import requests
import json

try:
    response = requests.post(
        'http://localhost:5000/api/auth/login',
        json={'username': 'admin', 'password': 'admin123'},
        timeout=5
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Erro: {str(e)}")
EOF
"""
        output, error = execute_command(client, cmd)
        print(output)
        
        # Verificar logs
        print("\n📝 Logs do backend (últimas 20 linhas):")
        output, error = execute_command(client, "docker logs poker_backend 2>&1 | tail -20")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ TESTE DE LOGIN CONCLUÍDO!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test()

