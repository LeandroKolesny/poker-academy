#!/usr/bin/env python3
"""
Script para teste final
"""

import paramiko
import time

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

def test():
    """Testa"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar dados
        print("📝 Total de aulas:")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT COUNT(*) as total FROM classes;\"")
        print(output)
        
        # Verificar categorias
        print("\n📝 Verificando categorias no banco de dados:")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SHOW COLUMNS FROM classes WHERE Field='category';\"")
        print(output)
        
        # Verificar aulas com categorias
        print("\n📝 Aulas com categorias:")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT id, name, category FROM classes LIMIT 15;\"")
        print(output)
        
        # Verificar usuários
        print("\n📝 Usuários:")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT id, username, type FROM users LIMIT 10;\"")
        print(output)
        
        # Verificar status dos containers
        print("\n📝 Status dos containers:")
        output, error = execute_command(client, "docker ps")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ TESTE FINAL CONCLUÍDO!")
        print("=" * 70)
        print("\n🌐 Acesse a aplicação em: https://cardroomgrinders.com.br")
        print("👤 Usuário: admin")
        print("🔑 Senha: admin123")
        print("\n📝 Ou acesse via IP: http://142.93.206.128")
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test()

