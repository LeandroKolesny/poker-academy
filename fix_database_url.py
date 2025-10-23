#!/usr/bin/env python3
"""
Script para corrigir DATABASE_URL
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

def fix():
    """Corrige"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar arquivo .env
        print("📝 Arquivo .env atual:")
        output, error = execute_command(client, "cat /root/Dojo_Deploy/poker-academy/poker-academy-backend/poker_academy_api/.env")
        print(output)
        
        # Corrigir DATABASE_URL
        print("\n📝 Corrigindo DATABASE_URL...")
        execute_command(client, "sed -i 's|DATABASE_URL=mysql+pymysql://poker_user:Dojo%40Sql159357@localhost:3306/poker_academy|DATABASE_URL=mysql+pymysql://poker_user:Dojo%40Sql159357@mysql:3306/poker_academy|g' /root/Dojo_Deploy/poker-academy/poker-academy-backend/poker_academy_api/.env")
        print("✅ Corrigido!\n")
        
        # Verificar arquivo .env após correção
        print("📝 Arquivo .env após correção:")
        output, error = execute_command(client, "cat /root/Dojo_Deploy/poker-academy/poker-academy-backend/poker_academy_api/.env")
        print(output)
        
        # Reiniciar backend
        print("\n📝 Reiniciando backend...")
        execute_command(client, "docker restart poker_backend")
        print("✅ Backend reiniciado!\n")
        
        # Aguardar
        print("⏳ Aguardando 15 segundos...")
        time.sleep(15)
        
        # Verificar status
        print("📝 Status:")
        output, error = execute_command(client, "docker ps | grep backend")
        print(output)
        
        # Verificar logs
        print("\n📝 Logs do backend:")
        output, error = execute_command(client, "docker logs poker_backend 2>&1 | tail -20")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ DATABASE_URL CORRIGIDO!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix()

