#!/usr/bin/env python3
"""
Script para verificar qual é o arquivo main.js atual
"""
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("🔌 Conectando ao servidor...")
client.connect('142.93.206.128', username='root', password='DojoShh159357')
print("✅ Conectado!")

# Verificar qual é o arquivo main.js atual
print("\n📁 Verificando arquivo main.js atual...")
stdin, stdout, stderr = client.exec_command("docker exec poker_frontend ls -la /usr/share/nginx/html/static/js/main.*.js")
output = stdout.read().decode('utf-8')
print(output)

# Verificar o index.html
print("\n📁 Verificando index.html...")
stdin, stdout, stderr = client.exec_command("docker exec poker_frontend cat /usr/share/nginx/html/index.html | grep 'main\\.'")
output = stdout.read().decode('utf-8')
print(output)

# Verificar logs do container
print("\n📋 Logs do container (últimas 10 linhas):")
stdin, stdout, stderr = client.exec_command("docker logs poker_frontend | tail -10")
output = stdout.read().decode('utf-8')
print(output)

client.close()
print("\n✅ Verificação concluída!")

