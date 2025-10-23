#!/usr/bin/env python3
"""
Script para verificar se o build foi atualizado
"""
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("🔌 Conectando ao servidor...")
client.connect('142.93.206.128', username='root', password='DojoShh159357')
print("✅ Conectado!")

# Verificar se o arquivo StudentPanel.js foi atualizado
print("\n📁 Verificando arquivos no container...")
stdin, stdout, stderr = client.exec_command("docker exec poker_frontend ls -la /usr/share/nginx/html/static/js/ | head -20")
output = stdout.read().decode('utf-8')
print(output)

# Verificar o conteúdo do arquivo main.js
print("\n🔍 Verificando se 'monthly-database' está no build...")
stdin, stdout, stderr = client.exec_command("docker exec poker_frontend grep -o 'monthly-database' /usr/share/nginx/html/static/js/main.*.js | wc -l")
output = stdout.read().decode('utf-8')
count = output.strip()
print(f"Ocorrências de 'monthly-database': {count}")

if int(count) > 0:
    print("✅ Build foi atualizado com sucesso!")
else:
    print("❌ Build pode não ter sido atualizado")

# Verificar se '/student/catalog' está no build
print("\n🔍 Verificando se '/student/catalog' está no build...")
stdin, stdout, stderr = client.exec_command("docker exec poker_frontend grep -o '/student/catalog' /usr/share/nginx/html/static/js/main.*.js | wc -l")
output = stdout.read().decode('utf-8')
count = output.strip()
print(f"Ocorrências de '/student/catalog': {count}")

if int(count) > 0:
    print("✅ Caminhos absolutos foram adicionados!")
else:
    print("⚠️  Caminhos absolutos podem não estar presentes")

client.close()
print("\n✅ Verificação concluída!")

