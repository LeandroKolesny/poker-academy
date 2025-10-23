#!/usr/bin/env python3
"""
Script para restaurar DB e iniciar todos os containers
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
        
        # Aguardar MySQL estar pronto
        print("⏳ Aguardando 30 segundos para MySQL estar pronto...")
        time.sleep(30)
        
        # Restaurar backup
        print("\n📝 Restaurando backup do banco de dados...")
        execute_command(client, "mysql -u poker_user -pDojo@Sql159357 poker_academy < /root/Dojo_Deploy/poker_academy_backup_20251016_022151.sql", timeout=120)
        print("✅ Backup restaurado!\n")
        
        # Iniciar todos os containers
        print("📝 Iniciando todos os containers...")
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d")
        print("✅ Comando enviado!\n")
        
        # Aguardar
        print("⏳ Aguardando 180 segundos...")
        time.sleep(180)
        
        # Verificar status
        print("\n📝 Status dos containers:")
        output, error = execute_command(client, "docker ps")
        print(output)
        
        # Verificar logs
        print("\n📝 Logs dos containers:")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose logs 2>&1 | tail -100")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ PROCESSO CONCLUÍDO!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    restore()

