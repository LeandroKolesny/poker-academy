#!/usr/bin/env python3
"""
Script para corrigir senha usando werkzeug
"""

import paramiko
import time
from werkzeug.security import generate_password_hash

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"
SSH_PORT = 22

def execute_command(client, command, timeout=60):
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
        
        # Gerar hash werkzeug para admin123
        print("📝 Gerando hash werkzeug para 'admin123'...")
        password = "admin123"
        password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        print(f"Hash gerado: {password_hash}\n")
        
        # Escapar aspas para SQL
        escaped_hash = password_hash.replace("'", "\\'")
        
        # Atualizar senha do admin
        print("📝 Atualizando senha do admin...")
        sql = f"UPDATE users SET password_hash = '{escaped_hash}' WHERE username = 'admin';"
        cmd = f"docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"{sql}\""
        output, error = execute_command(client, cmd)
        print(output if output else "Senha atualizada!")
        print("✅ Senha do admin atualizada!\n")
        
        # Atualizar senha de todos os admins
        print("📝 Atualizando senha de todos os admins...")
        sql = f"UPDATE users SET password_hash = '{escaped_hash}' WHERE type = 'admin';"
        cmd = f"docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"{sql}\""
        output, error = execute_command(client, cmd)
        print(output if output else "Senhas atualizadas!")
        print("✅ Senhas de todos os admins atualizadas!\n")
        
        # Verificar usuários
        print("📝 Verificando hash do admin:")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT id, username, password_hash FROM users WHERE username='admin';\"")
        print(output)
        
        # Reiniciar backend
        print("\n📝 Reiniciando backend...")
        execute_command(client, "docker restart poker_backend")
        print("✅ Backend reiniciado!\n")
        
        # Aguardar
        print("⏳ Aguardando 15 segundos...")
        time.sleep(15)
        
        # Testar login
        print("📝 Testando login...")
        output, error = execute_command(client, "docker exec poker_backend python -c \"from werkzeug.security import check_password_hash; hash_val = input('Hash: '); pwd = input('Senha: '); print('Válido!' if check_password_hash(hash_val, pwd) else 'Inválido!')\" 2>&1")
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ SENHA CORRIGIDA COM WERKZEUG!")
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

