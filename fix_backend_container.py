#!/usr/bin/env python3
"""
Script para corrigir o container do backend
"""
import paramiko
import time

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print("🔌 Conectando ao servidor...")
    ssh.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)
    print("✅ Conectado!")
    
    # Listar todos os containers
    print("\n📊 Todos os containers:")
    stdin, stdout, stderr = ssh.exec_command("docker ps -a")
    print(stdout.read().decode())
    
    # Remover container antigo
    print("\n🗑️  Removendo container antigo...")
    stdin, stdout, stderr = ssh.exec_command("docker rm -f 5e3896b40432_poker_backend 2>/dev/null || true")
    print(stdout.read().decode())
    
    # Fazer down e up
    print("\n⬇️  Fazendo docker-compose down...")
    stdin, stdout, stderr = ssh.exec_command("cd /root/Dojo_Deploy/poker-academy && docker-compose down")
    print(stdout.read().decode())
    
    time.sleep(3)
    
    print("\n⬆️  Fazendo docker-compose up -d...")
    stdin, stdout, stderr = ssh.exec_command("cd /root/Dojo_Deploy/poker-academy && docker-compose up -d")
    print(stdout.read().decode())
    
    time.sleep(10)
    
    # Verificar status
    print("\n📊 Status dos containers:")
    stdin, stdout, stderr = ssh.exec_command("cd /root/Dojo_Deploy/poker-academy && docker-compose ps")
    print(stdout.read().decode())
    
    print("\n✅ Containers corrigidos!")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
finally:
    ssh.close()

