#!/usr/bin/env python3
"""
Script para procurar backups do banco de dados
"""

import paramiko
import time

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"
SSH_PORT = 22

def execute_command(client, command, timeout=120):
    """Executa um comando via SSH"""
    print(f"\n📝 Executando: {command}")
    stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
    time.sleep(1)
    
    output = stdout.read().decode('utf-8', errors='replace')
    error = stderr.read().decode('utf-8', errors='replace')
    
    if output:
        print(output)
    
    return output, error

def search_backups():
    """Procura backups"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Procurar arquivos SQL
        print("📝 Procurando arquivos SQL no servidor:")
        output, _ = execute_command(client, "find /root -name '*.sql' -type f 2>/dev/null | head -20")
        
        # Procurar backups em diretórios comuns
        print("\n📝 Procurando em diretórios de backup:")
        output, _ = execute_command(client, "ls -la /root/backups/ 2>/dev/null || echo 'Nenhum backup em /root/backups'")
        
        output, _ = execute_command(client, "ls -la /var/backups/ 2>/dev/null | grep -i poker || echo 'Nenhum backup em /var/backups'")
        
        # Verificar volume do Docker
        print("\n📝 Verificando volumes do Docker:")
        output, _ = execute_command(client, "docker volume ls | grep -i poker")
        
        # Verificar se há dump do MySQL
        print("\n📝 Procurando dumps do MySQL:")
        output, _ = execute_command(client, "find /var/lib/mysql -name '*.ibd' -o -name '*.frm' 2>/dev/null | head -10")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    search_backups()

