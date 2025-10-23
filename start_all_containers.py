#!/usr/bin/env python3
"""
Script para iniciar todos os containers
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
    
    # Iniciar todos os containers
    print("\n▶️  Iniciando todos os containers...")
    stdin, stdout, stderr = ssh.exec_command("cd /root/Dojo_Deploy/poker-academy && docker-compose up -d")
    output = stdout.read().decode()
    print(output)
    
    # Esperar containers ficarem prontos
    print("\n⏳ Aguardando containers ficarem prontos...")
    time.sleep(10)
    
    # Verificar status
    print("\n📊 Status dos containers:")
    stdin, stdout, stderr = ssh.exec_command("cd /root/Dojo_Deploy/poker-academy && docker-compose ps")
    print(stdout.read().decode())
    
    print("\n✅ Containers iniciados!")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
finally:
    ssh.close()

