#!/usr/bin/env python3
"""
Script para verificar o ID do container
"""
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("🔌 Conectando ao servidor...")
client.connect('142.93.206.128', username='root', password='DojoShh159357')
print("✅ Conectado!")

# Verificar o ID do container
print("\n📊 Status do container:")
stdin, stdout, stderr = client.exec_command("docker ps | grep poker_frontend")
output = stdout.read().decode('utf-8')
print(output)

# Verificar a imagem do container
print("\n📊 Imagem do container:")
stdin, stdout, stderr = client.exec_command("docker inspect poker_frontend | grep -A 5 'Image'")
output = stdout.read().decode('utf-8')
print(output)

# Verificar quando o container foi criado
print("\n📊 Data de criação do container:")
stdin, stdout, stderr = client.exec_command("docker inspect poker_frontend | grep -A 2 'Created'")
output = stdout.read().decode('utf-8')
print(output)

client.close()
print("\n✅ Verificação concluída!")

