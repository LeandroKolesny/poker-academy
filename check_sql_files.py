#!/usr/bin/env python3
"""
Script para verificar arquivos SQL
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

def check():
    """Verifica"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar create_admin_users.sql
        print("📝 Conteúdo de create_admin_users.sql:")
        output, error = execute_command(client, "cat /root/Dojo_Deploy/poker-academy/create_admin_users.sql")
        print(output)
        
        # Verificar create_test_users.sql
        print("\n📝 Conteúdo de create_test_users.sql:")
        output, error = execute_command(client, "cat /root/Dojo_Deploy/poker-academy/create_test_users.sql")
        print(output)
        
        # Verificar add_real_youtube_videos.sql
        print("\n📝 Conteúdo de add_real_youtube_videos.sql:")
        output, error = execute_command(client, "cat /root/Dojo_Deploy/poker-academy/add_real_youtube_videos.sql")
        print(output)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check()

