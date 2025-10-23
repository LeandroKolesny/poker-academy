#!/usr/bin/env python3
"""
Script para verificar main.py no servidor
"""
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("🔌 Conectando ao servidor...")
client.connect('142.93.206.128', username='root', password='DojoShh159357')
print("✅ Conectado!")

# Verificar conteúdo do main.py
print("\n📝 Conteúdo do main.py no servidor (linhas 1-80):")
command = "head -80 /root/Dojo_Deploy/poker-academy/poker-academy-backend/poker_academy_api/src/main.py"

stdin, stdout, stderr = client.exec_command(command)
output = stdout.read().decode('utf-8')

print(output)

# Procurar por database_bp
print("\n🔍 Procurando por 'database_bp' no main.py:")
command = "grep -n 'database' /root/Dojo_Deploy/poker-academy/poker-academy-backend/poker_academy_api/src/main.py"

stdin, stdout, stderr = client.exec_command(command)
output = stdout.read().decode('utf-8')

print(output)

client.close()
print("\n✅ Verificação concluída!")

