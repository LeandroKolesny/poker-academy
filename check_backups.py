#!/usr/bin/env python3
"""
Script para verificar backups disponíveis
"""

import paramiko
import time

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"
SSH_PORT = 22

def execute_command(client, command):
    """Executa um comando via SSH"""
    stdin, stdout, stderr = client.exec_command(command)
    time.sleep(1)
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    return output, error

def check():
    """Verifica backups"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Procurar backups
        print("📋 Procurando backups em /root/Dojo_Deploy...")
        output, error = execute_command(client, "ls -lh /root/Dojo_Deploy/*.tar.gz 2>/dev/null")
        print(output if output else "Nenhum backup .tar.gz encontrado")
        
        # Procurar backups em /root
        print("\n📋 Procurando backups em /root...")
        output, error = execute_command(client, "ls -lh /root/*.tar.gz 2>/dev/null")
        print(output if output else "Nenhum backup .tar.gz encontrado")
        
        # Verificar volumes do Docker
        print("\n📋 Volumes do Docker:")
        output, error = execute_command(client, "docker volume ls")
        print(output)
        
        # Verificar dados do MySQL
        print("\n📋 Verificando dados do MySQL...")
        output, error = execute_command(client, "ls -lh /var/lib/docker/volumes/ 2>/dev/null | head -20")
        print(output if output else "Não foi possível acessar volumes")
        
        # Verificar uploads
        print("\n📋 Verificando uploads...")
        output, error = execute_command(client, "du -sh /root/Dojo_Deploy/poker-academy-backend/poker_academy_api/uploads/ 2>/dev/null")
        print(output if output else "Diretório não encontrado")
        
        output, error = execute_command(client, "ls -lh /root/Dojo_Deploy/poker-academy-backend/poker_academy_api/uploads/ 2>/dev/null | head -10")
        print(output if output else "Diretório vazio ou não encontrado")
        
        # Verificar banco de dados
        print("\n📋 Verificando banco de dados...")
        output, error = execute_command(client, "docker exec 0b2a94fd276e_poker_mysql mysql -u poker_user -pDojo@Sql159357 -e 'SELECT COUNT(*) as total_classes FROM poker_academy.classes;' 2>/dev/null")
        print(output if output else "Não foi possível conectar ao banco")
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ VERIFICAÇÃO DE BACKUPS CONCLUÍDA!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check()

