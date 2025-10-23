#!/usr/bin/env python3
"""
Script para verificar o status do container
"""
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("🔌 Conectando ao servidor...")
client.connect('142.93.206.128', username='root', password='DojoShh159357')
print("✅ Conectado!")

# Verificar status do container
print("\n📊 Status dos containers:")
stdin, stdout, stderr = client.exec_command("docker ps -a | grep poker")
output = stdout.read().decode('utf-8')
print(output)

# Verificar logs do frontend
print("\n📋 Logs do frontend (últimas 20 linhas):")
stdin, stdout, stderr = client.exec_command("docker logs poker_frontend | tail -20")
output = stdout.read().decode('utf-8')
print(output)

# Verificar se o container está rodando
print("\n🔍 Verificando se o container está rodando...")
stdin, stdout, stderr = client.exec_command("docker inspect poker_frontend | grep -A 5 'State'")
output = stdout.read().decode('utf-8')
print(output)

client.close()
print("\n✅ Verificação concluída!")

