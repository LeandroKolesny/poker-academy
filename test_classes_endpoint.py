#!/usr/bin/env python3
"""
Script para testar endpoint de aulas
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

def test_classes():
    """Testa endpoint de aulas"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Primeiro fazer login para pegar token
        print("📝 Fazendo login...")
        output, _ = execute_command(client, """docker exec poker_backend curl -s -X POST http://localhost:5000/api/auth/login -H 'Content-Type: application/json' -d '{"username":"admin","password":"admin123"}'""")
        
        # Extrair token
        import json
        try:
            response = json.loads(output.split('\n')[0])
            token = response.get('token')
            print(f"✅ Token obtido: {token[:50]}...")
        except:
            print("❌ Erro ao extrair token")
            return
        
        # Testar endpoint de aulas
        print("\n📝 Testando endpoint /api/classes...")
        output, _ = execute_command(client, f"""docker exec poker_backend curl -s -H 'Authorization: Bearer {token}' http://localhost:5000/api/classes""")
        print(output)
        
        if '"id"' in output and '"name"' in output:
            print("\n✅ ENDPOINT DE AULAS FUNCIONANDO!")
        else:
            print("\n❌ ERRO NO ENDPOINT DE AULAS")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_classes()

