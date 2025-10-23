#!/usr/bin/env python3
"""
Script para verificar o conteúdo do main.js
"""
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("🔌 Conectando ao servidor...")
client.connect('142.93.206.128', username='root', password='DojoShh159357')
print("✅ Conectado!")

# Verificar o tamanho do arquivo main.js
print("\n📁 Verificando tamanho do main.js...")
stdin, stdout, stderr = client.exec_command("docker exec poker_frontend ls -lh /usr/share/nginx/html/static/js/main.*.js")
output = stdout.read().decode('utf-8')
print(output)

# Procurar por 'monthly-database' no arquivo
print("\n🔍 Procurando por 'monthly-database'...")
stdin, stdout, stderr = client.exec_command("docker exec poker_frontend grep -c 'monthly-database' /usr/share/nginx/html/static/js/main.*.js 2>/dev/null || echo '0'")
output = stdout.read().decode('utf-8')
print(f"Resultado: {output}")

# Procurar por 'monthly' (mais genérico)
print("\n🔍 Procurando por 'monthly'...")
stdin, stdout, stderr = client.exec_command("docker exec poker_frontend grep -o 'monthly' /usr/share/nginx/html/static/js/main.*.js | wc -l")
output = stdout.read().decode('utf-8')
print(f"Ocorrências de 'monthly': {output}")

# Procurar por 'MonthlyDatabase'
print("\n🔍 Procurando por 'MonthlyDatabase'...")
stdin, stdout, stderr = client.exec_command("docker exec poker_frontend grep -o 'MonthlyDatabase' /usr/share/nginx/html/static/js/main.*.js | wc -l")
output = stdout.read().decode('utf-8')
print(f"Ocorrências de 'MonthlyDatabase': {output}")

# Procurar por '/student/catalog'
print("\n🔍 Procurando por '/student/catalog'...")
stdin, stdout, stderr = client.exec_command("docker exec poker_frontend grep -o '/student/catalog' /usr/share/nginx/html/static/js/main.*.js | wc -l")
output = stdout.read().decode('utf-8')
print(f"Ocorrências de '/student/catalog': {output}")

client.close()
print("\n✅ Verificação concluída!")

