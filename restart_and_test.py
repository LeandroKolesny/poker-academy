#!/usr/bin/env python3
"""
Script para reiniciar backend e testar login
"""

import paramiko
import time

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"
SSH_PORT = 22

def execute_command(client, command, timeout=120):
    """Executa um comando via SSH"""
    print(f"\n📝 Executando: {command}")
    stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
    time.sleep(1)
    
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    
    if output:
        print(output)
    
    return output, error

def test_login():
    """Testa login no servidor"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Reiniciar backend
        print("🔄 Reiniciando backend...")
        execute_command(client, "docker restart poker_backend")
        time.sleep(15)
        
        # Verificar status
        print("\n📝 Status do backend:")
        output, _ = execute_command(client, "docker ps | grep poker_backend")
        print(output)
        
        # Testar endpoint de teste
        print("\n📝 Testando endpoint /api/test...")
        output, _ = execute_command(client, "docker exec poker_backend curl -s http://localhost:5000/api/test")
        print(output)
        
        # Testar login
        print("\n📝 Testando login...")
        output, _ = execute_command(client, """docker exec poker_backend curl -s -X POST http://localhost:5000/api/auth/login -H 'Content-Type: application/json' -d '{"username":"admin","password":"admin123"}'""")
        print(output)
        
        if '"token"' in output:
            print("\n✅ LOGIN BEM-SUCEDIDO!")
        else:
            print("\n❌ LOGIN FALHOU")
            print("\n📝 Últimos logs:")
            output, _ = execute_command(client, "docker logs poker_backend 2>&1 | tail -50")
            print(output)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_login()

