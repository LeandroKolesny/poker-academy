#!/usr/bin/env python3
"""
Script para verificar conteúdo dos backups tar.gz
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
        print(output[-2000:] if len(output) > 2000 else output)
    
    return output, error

def check_backups():
    """Verifica backups"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar tamanho dos backups
        print("📝 Tamanho dos backups:")
        output, _ = execute_command(client, "ls -lh /root/Dojo_Deploy/poker-academy-backup.tar.gz /root/Dojo_Deploy/poker-academy/poker-academy-backend-backup-20251016_022417.tar.gz")
        
        # Listar conteúdo do backup
        print("\n📝 Conteúdo do poker-academy-backup.tar.gz:")
        output, _ = execute_command(client, "tar -tzf /root/Dojo_Deploy/poker-academy-backup.tar.gz | head -30")
        
        # Procurar por arquivos SQL dentro do tar
        print("\n📝 Procurando arquivos SQL no backup:")
        output, _ = execute_command(client, "tar -tzf /root/Dojo_Deploy/poker-academy-backup.tar.gz | grep -i '\\.sql$'")
        
        # Procurar por arquivos de banco de dados
        print("\n📝 Procurando arquivos de banco no backup:")
        output, _ = execute_command(client, "tar -tzf /root/Dojo_Deploy/poker-academy-backup.tar.gz | grep -i 'poker_academy\\|mysql\\|database' | head -20")
        
        # Extrair e verificar
        print("\n📝 Extraindo backup para verificação:")
        output, _ = execute_command(client, "cd /tmp && tar -xzf /root/Dojo_Deploy/poker-academy-backup.tar.gz 2>&1 | head -20 && echo 'Extração concluída'")
        
        # Procurar por arquivos SQL extraídos
        print("\n📝 Procurando arquivos SQL extraídos:")
        output, _ = execute_command(client, "find /tmp -name '*.sql' -type f 2>/dev/null | head -20")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_backups()

