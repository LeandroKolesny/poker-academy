#!/usr/bin/env python3
"""
Script para testar login final
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
        
        # Testar health check
        print("📝 Testando health check...")
        output, error = execute_command(client, "docker exec poker_backend curl -s http://localhost:5000/api/health")
        print(f"Response: {output}\n")
        
        # Testar login
        print("📝 Testando login com admin/admin123...")
        output, error = execute_command(client, "docker exec poker_backend curl -s -X POST http://localhost:5000/api/auth/login -H 'Content-Type: application/json' -d '{\"username\":\"admin\",\"password\":\"admin123\"}'")
        print(f"Response: {output}\n")
        
        # Verificar logs
        print("📝 Logs do backend (últimas 15 linhas):")
        output, error = execute_command(client, "docker logs poker_backend 2>&1 | tail -15")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ TESTE FINAL CONCLUÍDO!")
        print("=" * 70)
        print("\n🌐 Acesse: https://cardroomgrinders.com.br")
        print("👤 Usuário: admin")
        print("🔑 Senha: admin123")
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test()

