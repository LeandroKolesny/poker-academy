#!/usr/bin/env python3
"""
Script para verificar o conteúdo do main.js no container
"""
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("🔌 Conectando ao servidor...")
client.connect('142.93.206.128', username='root', password='DojoShh159357')
print("✅ Conectado!")

# Procurar por 'monthly-database' no arquivo main.js
print("\n🔍 Procurando por 'monthly-database'...")
stdin, stdout, stderr = client.exec_command("docker exec poker_frontend grep -o 'monthly-database' /usr/share/nginx/html/static/js/main.e1ab1fef.js | wc -l")
output = stdout.read().decode('utf-8')
print(f"Ocorrências: {output.strip()}")

# Procurar por '/student/catalog'
print("\n🔍 Procurando por '/student/catalog'...")
stdin, stdout, stderr = client.exec_command("docker exec poker_frontend grep -o '/student/catalog' /usr/share/nginx/html/static/js/main.e1ab1fef.js | wc -l")
output = stdout.read().decode('utf-8')
print(f"Ocorrências: {output.strip()}")

# Procurar por 'to="catalog"'
print("\n🔍 Procurando por 'to=\"catalog\"'...")
stdin, stdout, stderr = client.exec_command("docker exec poker_frontend grep -o 'to=\"catalog\"' /usr/share/nginx/html/static/js/main.e1ab1fef.js | wc -l")
output = stdout.read().decode('utf-8')
print(f"Ocorrências: {output.strip()}")

# Verificar tamanho do arquivo
print("\n📊 Tamanho do arquivo:")
stdin, stdout, stderr = client.exec_command("docker exec poker_frontend ls -lh /usr/share/nginx/html/static/js/main.e1ab1fef.js")
output = stdout.read().decode('utf-8')
print(output)

client.close()
print("\n✅ Verificação concluída!")

