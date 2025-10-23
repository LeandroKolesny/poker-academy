#!/usr/bin/env python3
"""
Script para listar todas as rotas do Flask
"""
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("🔌 Conectando ao servidor...")
client.connect('142.93.206.128', username='root', password='DojoShh159357')
print("✅ Conectado!")

# Listar todas as rotas
print("\n📋 Listando todas as rotas do Flask...")
command = """docker exec poker_backend python << 'EOF'
from src.main import app
print("\\n🔍 TODAS AS ROTAS REGISTRADAS:")
print("=" * 80)
for rule in sorted(app.url_map.iter_rules(), key=lambda r: r.rule):
    methods = ','.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
    print(f"{rule.rule:50} {methods:20}")
print("=" * 80)
EOF
"""

stdin, stdout, stderr = client.exec_command(command)
output = stdout.read().decode('utf-8')
error = stderr.read().decode('utf-8')

print(output)
if error:
    print(f"Error:\n{error}")

client.close()
print("\n✅ Verificação concluída!")

