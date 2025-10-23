#!/usr/bin/env python3
"""
Script para testar a aplicação
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
        
        # Verificar status dos containers
        print("📝 Status dos containers:")
        output, error = execute_command(client, "docker ps")
        print(output)
        
        # Testar backend
        print("\n📝 Testando backend...")
        output, error = execute_command(client, "curl -s http://localhost:5000/api/health || echo 'Erro'")
        print(output)
        
        # Testar frontend
        print("\n📝 Testando frontend...")
        output, error = execute_command(client, "curl -s http://localhost:80/ | head -20")
        print(output)
        
        # Verificar banco de dados
        print("\n📝 Verificando categorias no banco de dados...")
        output, error = execute_command(client, "mysql -u poker_user -pDojo@Sql159357 poker_academy -e \"SHOW COLUMNS FROM classes LIKE 'category';\"")
        print(output)
        
        # Verificar aulas
        print("\n📝 Verificando aulas no banco de dados...")
        output, error = execute_command(client, "mysql -u poker_user -pDojo@Sql159357 poker_academy -e \"SELECT id, name, category FROM classes LIMIT 5;\"")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ TESTES CONCLUÍDOS!")
        print("=" * 70)
        print("\n🌐 Acesse a aplicação em: https://cardroomgrinders.com.br")
        print("👤 Usuário: admin")
        print("🔑 Senha: admin123")
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test()

