#!/usr/bin/env python3
"""
Script para corrigir os dados das partições no banco de dados
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

def fix():
    """Fix"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Corrigir dados das partições
        print("1️⃣ Corrigindo dados das partições...")
        
        # Comando para corrigir a partição Dojo
        cmd1 = """docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "UPDATE particoes SET descricao = 'Partição principal do Dojo' WHERE id = 1;" """
        execute_command(client, cmd1)
        
        # Comando para corrigir a partição Coco
        cmd2 = """docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "UPDATE particoes SET descricao = 'Partição secundária Coco' WHERE id = 2;" """
        execute_command(client, cmd2)
        
        # Verificar dados
        print("\n2️⃣ Verificando dados...")
        cmd3 = """docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "SELECT id, nome, descricao FROM particoes;" """
        execute_command(client, cmd3)
        
        print("\n✅ FIX COMPLETO!")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix()

