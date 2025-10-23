#!/usr/bin/env python3
"""
Script para verificar se o arquivo database_routes.py foi copiado corretamente
"""
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("🔌 Conectando ao servidor...")
client.connect('142.93.206.128', username='root', password='DojoShh159357')
print("✅ Conectado!")

# Verificar se o arquivo existe
print("\n📋 Verificando arquivo database_routes.py...")
command = "ls -la /root/Dojo_Deploy/poker-academy/poker-academy-backend/poker_academy_api/src/routes/database_routes.py"

stdin, stdout, stderr = client.exec_command(command)
output = stdout.read().decode('utf-8')
error = stderr.read().decode('utf-8')

print(f"Output:\n{output}")
if error:
    print(f"Error:\n{error}")

# Verificar conteúdo do arquivo (primeiras 50 linhas)
print("\n📝 Primeiras 50 linhas do arquivo:")
command = "head -50 /root/Dojo_Deploy/poker-academy/poker-academy-backend/poker_academy_api/src/routes/database_routes.py"

stdin, stdout, stderr = client.exec_command(command)
output = stdout.read().decode('utf-8')

print(output)

# Verificar se há erro de importação
print("\n🔍 Verificando se há erro de importação no backend...")
command = "docker exec poker_backend python -c 'from src.routes.database_routes import database_bp; print(\"✅ Importação bem-sucedida\")' 2>&1"

stdin, stdout, stderr = client.exec_command(command)
output = stdout.read().decode('utf-8')
error = stderr.read().decode('utf-8')

print(f"Output:\n{output}")
if error:
    print(f"Error:\n{error}")

client.close()
print("\n✅ Verificação concluída!")

