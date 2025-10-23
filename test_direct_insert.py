#!/usr/bin/env python3
"""
Script para testar INSERT direto
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

def test():
    """Testa"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Criar arquivo SQL
        test_hash = "pbkdf2:sha256:260000$J4eEjERUmAApf7zW$b5eaf9c5fd42d0b24bbff7dc306236dfe78dd513aaaa3649499d04db060ae49b"
        
        print(f"📝 Hash de teste ({len(test_hash)} caracteres):")
        print(test_hash)
        
        # Tentar com arquivo SQL
        print("\n📝 Criando arquivo SQL...")
        sql_content = f"""UPDATE users SET password_hash = '{test_hash}' WHERE username = 'admin';
SELECT username, LENGTH(password_hash) as len, password_hash FROM users WHERE username='admin';"""
        
        # Copiar arquivo para servidor
        sftp = client.open_sftp()
        with sftp.file('/tmp/update_password.sql', 'w') as f:
            f.write(sql_content)
        sftp.close()
        print("✅ Arquivo criado!")
        
        # Executar arquivo
        print("\n📝 Executando arquivo SQL...")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy < /tmp/update_password.sql")
        print(output)
        
        # Verificar
        print("\n📝 Verificando resultado:")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT username, LENGTH(password_hash) as len, password_hash FROM users WHERE username='admin';\"")
        print(output)
        
        # Tentar com prepared statement
        print("\n📝 Tentando com prepared statement...")
        cmd = f"""docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy << 'EOF'
SET @hash = '{test_hash}';
UPDATE users SET password_hash = @hash WHERE username = 'admin';
SELECT username, LENGTH(password_hash) as len, password_hash FROM users WHERE username='admin';
EOF
"""
        output, error = execute_command(client, cmd)
        print(output)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test()

