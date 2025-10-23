#!/usr/bin/env python3
"""
Script para verificar se 'monthly-database' está no main.js
"""
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("🔌 Conectando ao servidor...")
client.connect('142.93.206.128', username='root', password='DojoShh159357')
print("✅ Conectado!")

# Procurar por 'monthly-database' no arquivo main.e1ab1fef.js
print("\n🔍 Procurando por 'monthly-database' em main.e1ab1fef.js...")
stdin, stdout, stderr = client.exec_command("docker exec poker_frontend grep -c 'monthly-database' /usr/share/nginx/html/static/js/main.e1ab1fef.js")
output = stdout.read().decode('utf-8')
print(f"Resultado: {output}")

# Procurar por 'monthly' (mais genérico)
print("\n🔍 Procurando por 'monthly' em main.e1ab1fef.js...")
stdin, stdout, stderr = client.exec_command("docker exec poker_frontend grep -o 'monthly' /usr/share/nginx/html/static/js/main.e1ab1fef.js | wc -l")
output = stdout.read().decode('utf-8')
print(f"Ocorrências de 'monthly': {output}")

# Procurar por '/student/catalog'
print("\n🔍 Procurando por '/student/catalog' em main.e1ab1fef.js...")
stdin, stdout, stderr = client.exec_command("docker exec poker_frontend grep -o '/student/catalog' /usr/share/nginx/html/static/js/main.e1ab1fef.js | wc -l")
output = stdout.read().decode('utf-8')
print(f"Ocorrências de '/student/catalog': {output}")

# Procurar por 'catalog' (relativo)
print("\n🔍 Procurando por 'catalog' (relativo) em main.e1ab1fef.js...")
stdin, stdout, stderr = client.exec_command("docker exec poker_frontend grep -o 'to=\"catalog\"' /usr/share/nginx/html/static/js/main.e1ab1fef.js | wc -l")
output = stdout.read().decode('utf-8')
print(f"Ocorrências de 'to=\"catalog\"': {output}")

client.close()
print("\n✅ Verificação concluída!")

