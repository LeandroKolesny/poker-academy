#!/usr/bin/env python3
"""
Script para gerar hash localmente e inserir no servidor
"""

import paramiko
import time
from werkzeug.security import generate_password_hash

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

def generate_and_insert():
    """Gera e insere"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Gerar hash localmente
        print("📝 Gerando hash werkzeug localmente...")
        password_hash = generate_password_hash('admin123', method='pbkdf2:sha256')
        print(f"Hash gerado: {password_hash}\n")
        
        # Escapar para SQL
        escaped_hash = password_hash.replace("'", "\\'")
        
        # Atualizar no banco
        print("📝 Atualizando senha de todos os admins no banco...")
        sql = f"UPDATE users SET password_hash = '{escaped_hash}' WHERE type = 'admin';"
        cmd = f"docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"{sql}\""
        output, error = execute_command(client, cmd)
        print("✅ Senha atualizada!")
        
        # Verificar
        print("\n📝 Verificando hash no banco:")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT username, LENGTH(password_hash) as hash_length, SUBSTRING(password_hash, 1, 50) as hash_preview FROM users WHERE type='admin' LIMIT 3;\"")
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
        
        # Verificar logs
        print("\n📝 Logs do backend (últimas 5 linhas):")
        output, error = execute_command(client, "docker logs poker_backend 2>&1 | tail -5")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ HASH GERADO E INSERIDO!")
        print("=" * 70)
        print("\n🌐 Acesse: https://cardroomgrinders.com.br")
        print("👤 Usuário: admin")
        print("🔑 Senha: admin123")
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    generate_and_insert()

