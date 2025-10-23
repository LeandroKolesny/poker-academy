#!/usr/bin/env python3
"""
Script para testar importação
"""
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("🔌 Conectando ao servidor...")
client.connect('142.93.206.128', username='root', password='DojoShh159357')
print("✅ Conectado!")

# Testar importação
print("\n🧪 Testando importação de database_routes...")
command = """docker exec poker_backend python << 'EOF'
try:
    from src.routes.database_routes import database_bp
    print("✅ database_bp importado com sucesso")
    print(f"   Blueprint name: {database_bp.name}")
    print(f"   Blueprint url_prefix: {database_bp.url_prefix}")
    print(f"   Rotas no blueprint:")
    for rule in database_bp.deferred_functions:
        print(f"     - {rule}")
except Exception as e:
    print(f"❌ Erro ao importar: {e}")
    import traceback
    traceback.print_exc()
EOF
"""

stdin, stdout, stderr = client.exec_command(command)
output = stdout.read().decode('utf-8')
error = stderr.read().decode('utf-8')

print(output)
if error:
    print(f"Error:\n{error}")

# Testar se o blueprint foi registrado
print("\n🧪 Testando se o blueprint foi registrado...")
command = """docker exec poker_backend python << 'EOF'
try:
    from src.main import app
    print("✅ app importado com sucesso")
    print(f"   Blueprints registrados: {list(app.blueprints.keys())}")
    
    # Procurar por database
    if 'database' in app.blueprints:
        print("✅ Blueprint 'database' está registrado!")
    else:
        print("❌ Blueprint 'database' NÃO está registrado!")
        
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
EOF
"""

stdin, stdout, stderr = client.exec_command(command)
output = stdout.read().decode('utf-8')
error = stderr.read().decode('utf-8')

print(output)
if error:
    print(f"Error:\n{error}")

client.close()
print("\n✅ Teste concluído!")

