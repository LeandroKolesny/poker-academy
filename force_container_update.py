#!/usr/bin/env python3
"""
Script para forçar a atualização do container
"""
import paramiko
import time

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("🔌 Conectando ao servidor...")
client.connect('142.93.206.128', username='root', password='DojoShh159357')
print("✅ Conectado!")

# Parar o container
print("\n🛑 Parando container...")
stdin, stdout, stderr = client.exec_command("docker stop poker_frontend")
output = stdout.read().decode('utf-8')
print(output)

time.sleep(3)

# Remover o container
print("\n🗑️  Removendo container...")
stdin, stdout, stderr = client.exec_command("docker rm poker_frontend")
output = stdout.read().decode('utf-8')
print(output)

time.sleep(3)

# Iniciar novo container
print("\n🚀 Iniciando novo container...")
stdin, stdout, stderr = client.exec_command("cd /root/Dojo_Deploy/poker-academy && docker-compose up -d poker_frontend")
output = stdout.read().decode('utf-8')
print(output)

time.sleep(15)

# Verificar status
print("\n📊 Status do container:")
stdin, stdout, stderr = client.exec_command("docker ps | grep poker_frontend")
output = stdout.read().decode('utf-8')
print(output)

# Verificar qual arquivo main.js está sendo usado
print("\n📁 Verificando arquivo main.js...")
stdin, stdout, stderr = client.exec_command("docker exec poker_frontend ls -la /usr/share/nginx/html/static/js/main.*.js")
output = stdout.read().decode('utf-8')
print(output)

# Verificar o index.html
print("\n📁 Verificando index.html...")
stdin, stdout, stderr = client.exec_command("docker exec poker_frontend cat /usr/share/nginx/html/index.html | grep 'main\\.'")
output = stdout.read().decode('utf-8')
print(output)

client.close()
print("\n✅ Atualização concluída!")

