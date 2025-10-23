#!/usr/bin/env python3
"""
Script para verificar e corrigir Dockerfile final
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
    """Verifica e corrige"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar Dockerfile
        print("📝 Verificando Dockerfile...")
        output, error = execute_command(client, "cat /root/Dojo_Deploy/poker-academy-backend/Dockerfile")
        print(output)
        
        # Procurar pela linha mkdir
        if "mkdir -p uploads/videos logs" in output:
            print("\n❌ DOCKERFILE AINDA TEM O COMANDO ANTIGO!")
            print("Corrigindo...")
            
            # Usar sed para corrigir
            execute_command(client, "sed -i 's/mkdir -p uploads\\/videos logs/mkdir -p logs/g' /root/Dojo_Deploy/poker-academy-backend/Dockerfile")
            
            # Verificar resultado
            output, error = execute_command(client, "cat /root/Dojo_Deploy/poker-academy-backend/Dockerfile | grep -A 2 'mkdir'")
            print("\n✅ Dockerfile corrigido:")
            print(output)
        else:
            print("\n✅ Dockerfile OK")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix()

