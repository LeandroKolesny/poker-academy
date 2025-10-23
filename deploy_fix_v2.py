#!/usr/bin/env python3
"""
Script para copiar arquivos corrigidos e fazer rebuild v2
"""
import paramiko
import os
import time

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("🔌 Conectando ao servidor...")
client.connect('142.93.206.128', username='root', password='DojoShh159357')
print("✅ Conectado!")

# Copiar arquivos
print("\n📁 Copiando arquivos corrigidos...")
sftp = client.open_sftp()

files_to_copy = [
    ('poker-academy/src/components/student/StudentPanel.js', '/root/Dojo_Deploy/poker-academy/poker-academy/src/components/student/StudentPanel.js'),
    ('poker-academy/src/components/admin/AdminPanel.js', '/root/Dojo_Deploy/poker-academy/poker-academy/src/components/admin/AdminPanel.js'),
]

for local_file, remote_file in files_to_copy:
    local_path = os.path.abspath(local_file)
    print(f"   Copiando {local_file}...")
    sftp.put(local_path, remote_file)
    print(f"   ✅ {local_file} copiado!")

sftp.close()

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

client.close()
print("\n✅ Deploy concluído!")

