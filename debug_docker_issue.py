#!/usr/bin/env python3
"""
Script para debugar problema do Docker
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

def debug():
    """Debug"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar se Docker está rodando
        print("📝 Verificando se Docker está rodando...")
        output, error = execute_command(client, "systemctl status docker")
        print(output)
        
        # Verificar log do docker-compose start
        print("\n📝 Verificando log do docker-compose start...")
        output, error = execute_command(client, "cat /tmp/docker_start.log 2>/dev/null || echo 'Log não encontrado'")
        print(output)
        
        # Tentar iniciar manualmente
        print("\n📝 Tentando iniciar manualmente...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d 2>&1")
        print(output)
        print(error)
        
        # Aguardar
        print("\n⏳ Aguardando 60 segundos...")
        time.sleep(60)
        
        # Verificar status
        print("\n📝 Status dos containers...")
        output, error = execute_command(client, "docker ps -a")
        print(output)
        
        # Verificar logs
        print("\n📝 Logs dos containers...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose logs 2>&1 | tail -200")
        print(output)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug()

