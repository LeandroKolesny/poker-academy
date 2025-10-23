#!/usr/bin/env python3
"""
Script para reiniciar backend
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

def restart():
    """Reinicia"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Parar backend
        print("📝 Parando backend...")
        execute_command(client, "docker stop poker_backend")
        print("✅ Backend parado!\n")
        
        # Aguardar
        print("⏳ Aguardando 5 segundos...")
        time.sleep(5)
        
        # Iniciar backend
        print("📝 Iniciando backend...")
        output, error = execute_command(client, "docker start poker_backend")
        print(output)
        print("✅ Backend iniciado!\n")
        
        # Aguardar
        print("⏳ Aguardando 15 segundos...")
        time.sleep(15)
        
        # Verificar status
        print("📝 Status:")
        output, error = execute_command(client, "docker ps | grep backend")
        print(output)
        
        # Verificar logs
        print("\n📝 Logs do backend:")
        output, error = execute_command(client, "docker logs poker_backend 2>&1 | tail -30")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ BACKEND REINICIADO!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    restart()

