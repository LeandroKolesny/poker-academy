#!/usr/bin/env python3
"""
Script para reconstruir e aguardar
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
        
        # Reconstruir (sem aguardar resposta)
        print("📝 Iniciando rebuild...")
        client.exec_command("cd /root/Dojo_Deploy/poker-academy && docker-compose build --no-cache > /tmp/docker_build.log 2>&1 &")
        print("✅ Rebuild iniciado em background!\n")
        
        # Aguardar 5 minutos
        print("⏳ Aguardando 300 segundos para o build completar...")
        time.sleep(300)
        
        # Verificar log
        print("\n📝 Verificando log do build...")
        output, error = execute_command(client, "tail -100 /tmp/docker_build.log")
        print(output)
        
        # Iniciar containers
        print("\n📝 Iniciando containers...")
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d")
        print("✅ Comando enviado!\n")
        
        # Aguardar
        print("⏳ Aguardando 180 segundos...")
        time.sleep(180)
        
        # Verificar status
        print("\n📝 Status dos containers:")
        output, error = execute_command(client, "docker ps")
        print(output)
        
        # Verificar logs
        print("\n📝 Logs dos containers:")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose logs 2>&1 | tail -100")
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

