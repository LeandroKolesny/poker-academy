#!/usr/bin/env python3
"""
Script para reconstruir frontend corretamente
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

def rebuild():
    """Reconstrói"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Reconstruir frontend
        print("📝 Reconstruindo frontend...")
        client.exec_command("cd /root/Dojo_Deploy/poker-academy && docker-compose build --no-cache frontend > /tmp/frontend_build.log 2>&1 &")
        print("✅ Build iniciado em background!\n")
        
        # Aguardar
        print("⏳ Aguardando 300 segundos...")
        time.sleep(300)
        
        # Verificar log
        print("\n📝 Verificando log...")
        output, error = execute_command(client, "tail -100 /tmp/frontend_build.log")
        print(output)
        
        # Iniciar frontend
        print("\n📝 Iniciando frontend...")
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d frontend")
        print("✅ Comando enviado!\n")
        
        # Aguardar
        print("⏳ Aguardando 60 segundos...")
        time.sleep(60)
        
        # Verificar status
        print("\n📝 Status:")
        output, error = execute_command(client, "docker ps")
        print(output)
        
        # Verificar logs
        print("\n📝 Logs do frontend:")
        output, error = execute_command(client, "docker logs poker_frontend 2>&1 | tail -50")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ PROCESSO CONCLUÍDO!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    rebuild()
