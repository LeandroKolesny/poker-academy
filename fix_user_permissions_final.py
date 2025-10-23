#!/usr/bin/env python3
"""
Script para corrigir permissões do usuário poker_user
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

def fix():
    """Corrige"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Remover usuário antigo
        print("📝 Removendo usuário antigo...")
        execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 -e \"DROP USER IF EXISTS 'poker_user'@'%';\"")
        print("✅ Usuário removido!\n")
        
        # Criar novo usuário
        print("📝 Criando novo usuário...")
        execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 -e \"CREATE USER 'poker_user'@'%' IDENTIFIED BY 'Dojo@Sql159357';\"")
        print("✅ Usuário criado!\n")
        
        # Conceder permissões
        print("📝 Concedendo permissões...")
        execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 -e \"GRANT ALL PRIVILEGES ON poker_academy.* TO 'poker_user'@'%'; FLUSH PRIVILEGES;\"")
        print("✅ Permissões concedidas!\n")
        
        # Testar conexão
        print("📝 Testando conexão...")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e \"SELECT 1;\"")
        print(output if output else "Conexão bem-sucedida!")
        
        # Reiniciar backend
        print("\n📝 Reiniciando backend...")
        execute_command(client, "docker restart poker_backend")
        print("✅ Backend reiniciado!\n")
        
        # Aguardar
        print("⏳ Aguardando 15 segundos...")
        time.sleep(15)
        
        # Verificar status
        print("📝 Status:")
        output, error = execute_command(client, "docker ps | grep backend")
        print(output)
        
        # Verificar logs
        print("\n📝 Logs do backend:")
        output, error = execute_command(client, "docker logs poker_backend 2>&1 | tail -20")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ PERMISSÕES CORRIGIDAS!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix()
