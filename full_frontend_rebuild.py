#!/usr/bin/env python3
"""
Script para fazer rebuild completo do frontend
"""
import paramiko
import time

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("🔌 Conectando ao servidor...")
client.connect('142.93.206.128', username='root', password='DojoShh159357')
print("✅ Conectado!")

# Parar o frontend
print("\n🛑 Parando frontend...")
stdin, stdout, stderr = client.exec_command("cd /root/Dojo_Deploy/poker-academy && docker-compose down poker_frontend")
output = stdout.read().decode('utf-8')
print(output)

time.sleep(3)

# Remover imagem e build
print("\n🗑️  Removendo imagem e build antigos...")
stdin, stdout, stderr = client.exec_command("docker rmi poker-academy_frontend:latest 2>/dev/null; rm -rf /root/Dojo_Deploy/poker-academy/poker-academy/build")
output = stdout.read().decode('utf-8')
print(output)

# Fazer rebuild sem cache
print("\n🔨 Fazendo rebuild sem cache...")
stdin, stdout, stderr = client.exec_command("cd /root/Dojo_Deploy/poker-academy && docker-compose build --no-cache frontend")
output = stdout.read().decode('utf-8')
print(output)

# Iniciar frontend
print("\n🚀 Iniciando frontend...")
stdin, stdout, stderr = client.exec_command("cd /root/Dojo_Deploy/poker-academy && docker-compose up -d poker_frontend")
output = stdout.read().decode('utf-8')
print(output)

time.sleep(15)

# Verificar status
print("\n📊 Status do frontend:")
stdin, stdout, stderr = client.exec_command("docker ps | grep poker_frontend")
output = stdout.read().decode('utf-8')
print(output)

# Verificar se o build contém 'monthly-database'
print("\n🔍 Verificando se build foi atualizado...")
stdin, stdout, stderr = client.exec_command("docker exec poker_frontend grep -o 'monthly-database' /usr/share/nginx/html/static/js/main.*.js | wc -l")
output = stdout.read().decode('utf-8')
count = output.strip()
print(f"Ocorrências de 'monthly-database': {count}")

if int(count) > 0:
    print("✅ Build foi atualizado com sucesso!")
else:
    print("❌ Build pode não ter sido atualizado")

client.close()
print("\n✅ Rebuild concluído!")

