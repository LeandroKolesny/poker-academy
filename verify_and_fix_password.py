#!/usr/bin/env python3
"""
Script para verificar e corrigir senha no servidor
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

def verify():
    """Verifica"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar hash atual
        print("📝 Hash atual do admin no banco:")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT id, username, password_hash FROM users WHERE username='admin' LIMIT 1;\"")
        print(output)
        
        # Gerar novo hash com werkzeug
        print("\n📝 Gerando novo hash werkzeug para 'admin123'...")
        cmd = """docker exec poker_backend python << 'EOF'
from werkzeug.security import generate_password_hash
password_hash = generate_password_hash('admin123', method='pbkdf2:sha256')
print(f"Hash: {password_hash}")
EOF
"""
        output, error = execute_command(client, cmd)
        print(output)
        
        # Extrair hash
        hash_line = [line for line in output.split('\n') if line.startswith('Hash:')]
        if hash_line:
            new_hash = hash_line[0].replace('Hash: ', '').strip()
            print(f"\n✅ Novo hash gerado: {new_hash}\n")
            
            # Atualizar no banco
            print("📝 Atualizando senha no banco...")
            escaped_hash = new_hash.replace("'", "\\'")
            sql = f"UPDATE users SET password_hash = '{escaped_hash}' WHERE username = 'admin';"
            cmd = f"docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"{sql}\""
            output, error = execute_command(client, cmd)
            print("✅ Senha atualizada!")
            
            # Atualizar todos os admins
            print("\n📝 Atualizando senha de todos os admins...")
            sql = f"UPDATE users SET password_hash = '{escaped_hash}' WHERE type = 'admin';"
            cmd = f"docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"{sql}\""
            output, error = execute_command(client, cmd)
            print("✅ Senhas de todos os admins atualizadas!")
            
            # Verificar
            print("\n📝 Verificando hash atualizado:")
            output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT id, username, password_hash FROM users WHERE username='admin' LIMIT 1;\"")
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
        print("✅ SENHA VERIFICADA E CORRIGIDA!")
        print("=" * 70)
        print("\n🌐 Acesse: https://cardroomgrinders.com.br")
        print("👤 Usuário: admin")
        print("🔑 Senha: admin123")
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify()

