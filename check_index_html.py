#!/usr/bin/env python3
"""
Script para verificar o index.html no servidor
"""
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("🔌 Conectando ao servidor...")
client.connect('142.93.206.128', username='root', password='DojoShh159357')
print("✅ Conectado!")

# Verificar o conteúdo do index.html
print("\n📁 Verificando index.html...")
stdin, stdout, stderr = client.exec_command("docker exec poker_frontend cat /usr/share/nginx/html/index.html")
output = stdout.read().decode('utf-8')
print(output[:1000])

# Procurar por 'monthly-database' no index.html
print("\n🔍 Procurando por 'monthly-database' no index.html...")
stdin, stdout, stderr = client.exec_command("docker exec poker_frontend grep -c 'monthly-database' /usr/share/nginx/html/index.html")
output = stdout.read().decode('utf-8')
print(f"Resultado: {output}")

# Procurar por 'main.' no index.html
print("\n🔍 Procurando por 'main.' no index.html...")
stdin, stdout, stderr = client.exec_command("docker exec poker_frontend grep 'main\\.' /usr/share/nginx/html/index.html")
output = stdout.read().decode('utf-8')
print(output)

client.close()
print("\n✅ Verificação concluída!")

