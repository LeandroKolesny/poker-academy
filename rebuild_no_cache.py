#!/usr/bin/env python3
"""
Script para fazer rebuild sem cache
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
    
    # Rebuild sem cache
    print("\n🔨 Rebuilding backend sem cache...")
    stdin, stdout, stderr = ssh.exec_command("cd /root/Dojo_Deploy/poker-academy && docker-compose build --no-cache backend 2>&1")
    
    # Ler output em tempo real
    for line in iter(stdout.readline, ''):
        if line:
            print(line.rstrip())
    
    # Iniciar containers
    print("\n▶️  Iniciando containers...")
    stdin, stdout, stderr = ssh.exec_command("cd /root/Dojo_Deploy/poker-academy && docker-compose up -d")
    print(stdout.read().decode())
    
    # Esperar containers ficarem prontos
    print("\n⏳ Aguardando containers ficarem prontos...")
    time.sleep(10)
    
    # Verificar status
    print("\n📊 Status dos containers:")
    stdin, stdout, stderr = ssh.exec_command("cd /root/Dojo_Deploy/poker-academy && docker-compose ps")
    print(stdout.read().decode())
    
    print("\n✅ Rebuild concluído!")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
finally:
    ssh.close()

