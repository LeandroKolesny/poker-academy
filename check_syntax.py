#!/usr/bin/env python3
"""
Script para verificar sintaxe do arquivo
"""
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("🔌 Conectando ao servidor...")
client.connect('142.93.206.128', username='root', password='DojoShh159357')
print("✅ Conectado!")

# Verificar sintaxe
print("\n🧪 Verificando sintaxe do arquivo database_routes.py...")
command = "docker exec poker_backend python -m py_compile /app/src/routes/database_routes.py 2>&1"

stdin, stdout, stderr = client.exec_command(command)
output = stdout.read().decode('utf-8')
error = stderr.read().decode('utf-8')

print(f"Output:\n{output}")
if error:
    print(f"Error:\n{error}")

# Tentar importar com mais detalhes
print("\n🧪 Tentando importar com detalhes...")
command = """docker exec poker_backend python -c "
import sys
sys.path.insert(0, '/app')
try:
    print('Importando database_routes...')
    from src.routes.database_routes import database_bp
    print('✅ Sucesso!')
except Exception as e:
    print(f'❌ Erro: {e}')
    import traceback
    traceback.print_exc()
" 2>&1"""

stdin, stdout, stderr = client.exec_command(command)
output = stdout.read().decode('utf-8')

print(output)

client.close()
print("\n✅ Verificação concluída!")

