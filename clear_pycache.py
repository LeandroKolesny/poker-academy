#!/usr/bin/env python3
"""
Script para limpar cache Python no servidor
"""
import paramiko

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print("🔌 Conectando ao servidor...")
    ssh.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)
    print("✅ Conectado!")
    
    # Limpar cache Python no container
    print("\n🗑️  Limpando cache Python no container...")
    stdin, stdout, stderr = ssh.exec_command("cd /root/Dojo_Deploy/poker-academy && docker exec poker_backend find /app -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true")
    print(stdout.read().decode())
    
    # Limpar cache Python no servidor
    print("\n🗑️  Limpando cache Python no servidor...")
    stdin, stdout, stderr = ssh.exec_command("find /root/Dojo_Deploy/poker-academy -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true")
    print(stdout.read().decode())
    
    # Reiniciar backend
    print("\n▶️  Reiniciando backend...")
    stdin, stdout, stderr = ssh.exec_command("cd /root/Dojo_Deploy/poker-academy && docker-compose restart poker_backend")
    print(stdout.read().decode())
    
    print("\n✅ Cache limpo e backend reiniciado!")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
finally:
    ssh.close()

