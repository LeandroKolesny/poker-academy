#!/usr/bin/env python3
"""
Script para restaurar banco de dados completo
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
    time.sleep(3)
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    return output, error

def restore():
    """Restaura"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Listar backups disponíveis
        print("📝 Backups disponíveis:")
        output, error = execute_command(client, "ls -lh /root/Dojo_Deploy/poker_academy_backup*.sql")
        print(output)
        
        # Restaurar backup completo
        print("\n📝 Restaurando banco de dados completo...")
        output, error = execute_command(client, "docker exec -i poker_mysql mysql -u root -ppoker_academy_2025 < /root/Dojo_Deploy/poker_academy_backup_20251016_022151.sql", timeout=180)
        print("✅ Banco restaurado!\n")
        
        # Aguardar
        print("⏳ Aguardando 10 segundos...")
        time.sleep(10)
        
        # Verificar tabelas
        print("📝 Tabelas no banco:")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SHOW TABLES;\"")
        print(output)
        
        # Verificar aulas
        print("\n📝 Total de aulas:")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT COUNT(*) as total FROM classes;\"")
        print(output)
        
        # Verificar alunos
        print("\n📝 Total de usuários:")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT COUNT(*) as total FROM users;\"")
        print(output)
        
        # Listar usuários
        print("\n📝 Usuários cadastrados:")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT id, name, username, type FROM users;\"")
        print(output)
        
        # Listar aulas
        print("\n📝 Aulas cadastradas (primeiras 10):")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT id, name, category FROM classes LIMIT 10;\"")
        print(output)
        
        # Reiniciar backend
        print("\n📝 Reiniciando backend...")
        execute_command(client, "docker restart poker_backend")
        print("✅ Backend reiniciado!\n")
        
        # Aguardar
        print("⏳ Aguardando 15 segundos...")
        time.sleep(15)
        
        # Verificar status
        print("📝 Status dos containers:")
        output, error = execute_command(client, "docker ps")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ BANCO DE DADOS RESTAURADO COM SUCESSO!")
        print("=" * 70)
        print("\n🌐 Acesse: https://cardroomgrinders.com.br")
        print("👤 Usuário: admin")
        print("🔑 Senha: admin123")
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    restore()

