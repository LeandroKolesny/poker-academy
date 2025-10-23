#!/usr/bin/env python3
"""
Script para testar rotas diretamente no container
"""
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("🔌 Conectando ao servidor...")
client.connect('142.93.206.128', username='root', password='DojoShh159357')
print("✅ Conectado!")

# Testar health
print("\n🧪 Testando rota /api/health...")
command = "curl -s http://poker_backend:5000/api/health"

stdin, stdout, stderr = client.exec_command(command)
output = stdout.read().decode('utf-8')

print(f"Health response:\n{output}")

# Listar rotas com grep
print("\n🔍 Procurando por rotas com 'database'...")
command = "docker exec poker_backend python -c \"from src.main import app; routes = [r.rule for r in app.url_map.iter_rules()]; print('\\n'.join([r for r in routes if 'database' in r]))\" 2>&1"

stdin, stdout, stderr = client.exec_command(command)
output = stdout.read().decode('utf-8')
error = stderr.read().decode('utf-8')

print(f"Output:\n{output}")
if error:
    print(f"Error:\n{error}")

# Listar TODAS as rotas
print("\n🔍 TODAS AS ROTAS:")
command = "docker exec poker_backend python -c \"from src.main import app; routes = sorted([r.rule for r in app.url_map.iter_rules()]); print('\\n'.join(routes))\" 2>&1"

stdin, stdout, stderr = client.exec_command(command)
output = stdout.read().decode('utf-8')
error = stderr.read().decode('utf-8')

print(f"Output:\n{output}")
if error:
    print(f"Error:\n{error}")

client.close()
print("\n✅ Teste concluído!")

