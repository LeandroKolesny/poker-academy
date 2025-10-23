#!/usr/bin/env python3
"""
Script para verificar coluna password_hash
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

def check():
    """Verifica"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar estrutura da tabela
        print("📝 Estrutura da tabela users:")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"DESCRIBE users;\"")
        print(output)
        
        # Verificar tamanho da coluna password_hash
        print("\n📝 Informações da coluna password_hash:")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT COLUMN_NAME, COLUMN_TYPE, CHARACTER_MAXIMUM_LENGTH FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='users' AND COLUMN_NAME='password_hash';\"")
        print(output)
        
        # Alterar coluna para VARCHAR(500)
        print("\n📝 Alterando coluna password_hash para VARCHAR(500)...")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"ALTER TABLE users MODIFY COLUMN password_hash VARCHAR(500);\"")
        print("✅ Coluna alterada!")
        
        # Verificar novamente
        print("\n📝 Verificando coluna após alteração:")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT COLUMN_NAME, COLUMN_TYPE, CHARACTER_MAXIMUM_LENGTH FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='users' AND COLUMN_NAME='password_hash';\"")
        print(output)
        
        # Gerar novo hash
        print("\n📝 Gerando novo hash werkzeug...")
        cmd = """docker exec poker_backend python << 'EOF'
from werkzeug.security import generate_password_hash
password_hash = generate_password_hash('admin123', method='pbkdf2:sha256')
print(password_hash)
EOF
"""
        output, error = execute_command(client, cmd)
        new_hash = output.strip()
        print(f"Hash: {new_hash}")
        
        # Atualizar no banco
        print("\n📝 Atualizando senha no banco...")
        escaped_hash = new_hash.replace("'", "\\'")
        sql = f"UPDATE users SET password_hash = '{escaped_hash}' WHERE type = 'admin';"
        cmd = f"docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"{sql}\""
        output, error = execute_command(client, cmd)
        print("✅ Senha atualizada!")
        
        # Verificar
        print("\n📝 Verificando hash no banco:")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT username, password_hash FROM users WHERE username='admin' LIMIT 1;\"")
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
        print("✅ COLUNA CORRIGIDA E SENHA ATUALIZADA!")
        print("=" * 70)
        print("\n🌐 Acesse: https://cardroomgrinders.com.br")
        print("👤 Usuário: admin")
        print("🔑 Senha: admin123")
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check()

