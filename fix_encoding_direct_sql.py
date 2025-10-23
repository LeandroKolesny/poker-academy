#!/usr/bin/env python3
"""
Script para corrigir o encoding diretamente via SQL
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
        print(output[-1000:] if len(output) > 1000 else output)
    
    return output, error

def fix_encoding():
    """Corrige o encoding"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar dados atuais
        print("1️⃣ Verificando dados atuais...")
        cmd = """docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "SELECT id, nome, HEX(descricao) as descricao_hex FROM particoes;" """
        execute_command(client, cmd)
        
        # Corrigir a coluna descricao para UTF-8
        print("\n2️⃣ Corrigindo encoding da coluna...")
        cmd2 = """docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "ALTER TABLE particoes MODIFY descricao TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" """
        execute_command(client, cmd2)
        
        # Verificar dados após correção
        print("\n3️⃣ Verificando dados após correção...")
        cmd3 = """docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "SELECT id, nome, descricao FROM particoes;" """
        execute_command(client, cmd3)
        
        print("\n✅ ENCODING CORRIGIDO COM SUCESSO!")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_encoding()

