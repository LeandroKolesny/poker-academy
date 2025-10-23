#!/usr/bin/env python3
"""
Script para restaurar dados dos arquivos SQL
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

def restore():
    """Restaura"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Restaurar usuários admin
        print("📝 Restaurando usuários admin...")
        execute_command(client, "docker exec -i poker_mysql mysql -u root -ppoker_academy_2025 < /root/Dojo_Deploy/poker-academy/create_admin_users.sql")
        print("✅ Usuários admin restaurados!\n")
        
        # Restaurar usuários de teste
        print("📝 Restaurando usuários de teste...")
        execute_command(client, "docker exec -i poker_mysql mysql -u root -ppoker_academy_2025 < /root/Dojo_Deploy/poker-academy/create_test_users.sql")
        print("✅ Usuários de teste restaurados!\n")
        
        # Restaurar aulas
        print("📝 Restaurando aulas...")
        execute_command(client, "docker exec -i poker_mysql mysql -u root -ppoker_academy_2025 < /root/Dojo_Deploy/poker-academy/add_real_youtube_videos.sql")
        print("✅ Aulas restauradas!\n")
        
        # Aguardar
        time.sleep(5)
        
        # Verificar usuários
        print("📝 Usuários cadastrados:")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT id, name, username, type FROM users ORDER BY id;\"")
        print(output)
        
        # Verificar aulas
        print("\n📝 Aulas cadastradas:")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT id, name, category FROM classes ORDER BY id;\"")
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
        print("✅ DADOS RESTAURADOS COM SUCESSO!")
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

