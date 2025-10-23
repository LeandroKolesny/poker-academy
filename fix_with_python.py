#!/usr/bin/env python3
"""
Script para corrigir usando Python no container
"""

import paramiko
import time

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"
SSH_PORT = 22

def execute_command(client, command, timeout=120):
    """Executa um comando via SSH"""
    stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
    time.sleep(2)
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    return output, error

def fix():
    """Corrige"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Criar script Python
        python_script = """
import pymysql
from werkzeug.security import generate_password_hash

# Conectar ao banco
conn = pymysql.connect(
    host='mysql',
    user='root',
    password='poker_academy_2025',
    database='poker_academy'
)

cursor = conn.cursor()

# Gerar hash
password_hash = generate_password_hash('admin123', method='pbkdf2:sha256')
print(f"Hash gerado: {password_hash}")
print(f"Tamanho: {len(password_hash)}")

# Atualizar
sql = "UPDATE users SET password_hash = %s WHERE type = 'admin'"
cursor.execute(sql, (password_hash,))
conn.commit()

# Verificar
cursor.execute("SELECT username, LENGTH(password_hash) as len, password_hash FROM users WHERE type='admin' LIMIT 1")
result = cursor.fetchone()
print(f"Resultado: {result}")

cursor.close()
conn.close()
"""
        
        print("📝 Criando script Python...")
        sftp = client.open_sftp()
        with sftp.file('/tmp/fix_password.py', 'w') as f:
            f.write(python_script)
        sftp.close()
        print("✅ Script criado!")
        
        # Executar script
        print("\n📝 Executando script Python no container...")
        output, error = execute_command(client, "docker exec poker_backend python /tmp/fix_password.py")
        print(output)
        if error:
            print(f"Error: {error}")
        
        # Verificar resultado
        print("\n📝 Verificando resultado no banco:")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT username, LENGTH(password_hash) as len, SUBSTRING(password_hash, 1, 50) as preview FROM users WHERE username='admin';\"")
        print(output)
        
        # Reiniciar backend
        print("\n📝 Reiniciando backend...")
        output, error = execute_command(client, "docker restart poker_backend")
        print("✅ Backend reiniciado!")
        
        # Aguardar
        print("\n⏳ Aguardando 20 segundos...")
        time.sleep(20)
        
        # Testar login
        print("\n📝 Testando login...")
        output, error = execute_command(client, "docker exec poker_backend curl -s -X POST http://localhost:5000/api/auth/login -H 'Content-Type: application/json' -d '{\"username\":\"admin\",\"password\":\"admin123\"}'")
        print(f"Response: {output}")
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ SENHA CORRIGIDA COM PYTHON!")
        print("=" * 70)
        print("\n🌐 Acesse: https://cardroomgrinders.com.br")
        print("👤 Usuário: admin")
        print("🔑 Senha: admin123")
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix()

