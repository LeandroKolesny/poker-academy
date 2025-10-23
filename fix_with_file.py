#!/usr/bin/env python3
"""
Script para corrigir usando arquivo SQL
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
        
        # Hash de teste
        test_hash = "pbkdf2:sha256:260000$J4eEjERUmAApf7zW$b5eaf9c5fd42d0b24bbff7dc306236dfe78dd513aaaa3649499d04db060ae49b"
        
        print(f"📝 Hash ({len(test_hash)} caracteres):")
        print(test_hash)
        
        # Criar arquivo SQL
        sql_content = f"""UPDATE users SET password_hash = '{test_hash}' WHERE type = 'admin';
SELECT username, LENGTH(password_hash) as len, SUBSTRING(password_hash, 1, 50) as preview FROM users WHERE type = 'admin' LIMIT 3;"""
        
        print("\n📝 Criando arquivo SQL no servidor...")
        sftp = client.open_sftp()
        with sftp.file('/tmp/fix_password.sql', 'w') as f:
            f.write(sql_content)
        sftp.close()
        print("✅ Arquivo criado!")
        
        # Executar arquivo
        print("\n📝 Executando arquivo SQL...")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy < /tmp/fix_password.sql")
        print(output)
        if error:
            print(f"Error: {error}")
        
        # Verificar resultado
        print("\n📝 Verificando resultado:")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT username, LENGTH(password_hash) as len, password_hash FROM users WHERE username='admin';\"")
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
        print("✅ SENHA CORRIGIDA COM ARQUIVO SQL!")
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

