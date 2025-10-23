#!/usr/bin/env python3
"""
Script para copiar arquivos corrigidos e fazer rebuild
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

# Fazer rebuild do frontend
print("\n🔨 Fazendo rebuild do frontend...")
stdin, stdout, stderr = client.exec_command("cd /root/Dojo_Deploy/poker-academy && docker-compose build frontend")
output = stdout.read().decode('utf-8')
print(output)

# Reiniciar frontend
print("\n🚀 Reiniciando frontend...")
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

