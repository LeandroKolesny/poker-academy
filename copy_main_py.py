#!/usr/bin/env python3
"""
Script para copiar main.py para o servidor
"""
import paramiko
import os

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("🔌 Conectando ao servidor...")
client.connect('142.93.206.128', username='root', password='DojoShh159357')
print("✅ Conectado!")

# Copiar arquivo main.py
print("\n📁 Copiando arquivo main.py...")
sftp = client.open_sftp()

local_file = os.path.abspath('poker-academy-backend/poker_academy_api/src/main.py')
remote_file = '/root/Dojo_Deploy/poker-academy/poker-academy-backend/poker_academy_api/src/main.py'

print(f"   Local: {local_file}")
print(f"   Remote: {remote_file}")

sftp.put(local_file, remote_file)
print("✅ main.py copiado!")

sftp.close()

# Reiniciar backend
print("\n🔄 Reiniciando backend...")
stdin, stdout, stderr = client.exec_command("docker restart poker_backend")
output = stdout.read().decode('utf-8')
print(output)

import time
time.sleep(10)

# Verificar se a rota foi registrada
print("\n🔍 Verificando se a rota foi registrada...")
command = """docker exec poker_backend python -c "
from src.main import app
routes = [r.rule for r in app.url_map.iter_rules() if 'database' in r.rule]
if routes:
    print('✅ Rotas de database encontradas:')
    for r in routes:
        print(f'   - {r}')
else:
    print('❌ Nenhuma rota de database encontrada')
" 2>&1"""

stdin, stdout, stderr = client.exec_command(command)
output = stdout.read().decode('utf-8')
print(output)

client.close()
print("\n✅ Cópia concluída!")

