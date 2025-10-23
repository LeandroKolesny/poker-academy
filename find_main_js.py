#!/usr/bin/env python3
"""
Script para encontrar o arquivo main.js
"""
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("🔌 Conectando ao servidor...")
client.connect('142.93.206.128', username='root', password='DojoShh159357')
print("✅ Conectado!")

# Procurar por main.js em vários locais
locations = [
    "/root/Dojo_Deploy/poker-academy/poker-academy/build/static/js/",
    "/root/Dojo_Deploy/poker-academy/build/static/js/",
    "/root/Dojo_Deploy/build/static/js/",
]

for location in locations:
    print(f"\n🔍 Procurando em {location}...")
    stdin, stdout, stderr = client.exec_command(f"ls -la {location}main.*.js 2>/dev/null || echo 'Não encontrado'")
    output = stdout.read().decode('utf-8')
    print(output)

# Procurar no container
print("\n🔍 Procurando no container...")
stdin, stdout, stderr = client.exec_command("docker exec poker_frontend ls -la /usr/share/nginx/html/static/js/main.*.js")
output = stdout.read().decode('utf-8')
print(output)

client.close()
print("\n✅ Busca concluída!")

