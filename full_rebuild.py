#!/usr/bin/env python3
"""
Script para fazer rebuild completo
"""
import paramiko
import time

def execute_command(client, command, timeout=120):
    """Executa um comando via SSH"""
    print(f"\n📝 Executando: {command}")
    stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
    output = stdout.read().decode('utf-8', errors='replace')
    error = stderr.read().decode('utf-8', errors='replace')
    return output, error

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("🔌 Conectando ao servidor...")
client.connect('142.93.206.128', username='root', password='DojoShh159357')
print("✅ Conectado!")

# Parar containers
print("\n🛑 Parando containers...")
output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose down")
print(output)

time.sleep(3)

# Remover imagens
print("\n🗑️  Removendo imagens...")
output, error = execute_command(client, "docker rmi poker-academy_backend:latest 2>/dev/null || true")
print(output)

# Rebuild
print("\n🔨 Rebuilding containers...")
output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d --build", timeout=300)
print(output)

if error:
    print("\n⚠️  Stderr:")
    print(error)

# Aguardar containers iniciarem
print("\n⏳ Aguardando containers iniciarem...")
time.sleep(10)

# Verificar status
print("\n📊 Status dos containers:")
output, error = execute_command(client, "docker ps -a")
print(output)

# Verificar logs do backend
print("\n📝 Logs do backend (últimas 30 linhas):")
output, error = execute_command(client, "docker logs poker_backend 2>&1 | tail -30")
print(output)

client.close()
print("\n✅ Rebuild concluído!")

