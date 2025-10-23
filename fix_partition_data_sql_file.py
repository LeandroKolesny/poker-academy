#!/usr/bin/env python3
"""
Script para corrigir os dados das partições usando arquivo SQL
"""

import paramiko
import time
import os

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
        
        # Criar arquivo SQL
        print("1️⃣ Criando arquivo SQL...")
        sql_content = """SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
DELETE FROM particoes WHERE id IN (1, 2);
INSERT INTO particoes (id, nome, descricao, ativa, created_at, updated_at) VALUES 
(1, 'Dojo', 'Partição principal do Dojo', 1, NOW(), NOW()),
(2, 'Coco', 'Partição secundária Coco', 1, NOW(), NOW());
SELECT id, nome, descricao FROM particoes;
"""
        
        # Salvar arquivo localmente
        with open('fix_partition.sql', 'w', encoding='utf-8') as f:
            f.write(sql_content)
        
        # Copiar arquivo para servidor
        print("2️⃣ Copiando arquivo SQL para servidor...")
        sftp = client.open_sftp()
        sftp.put('fix_partition.sql', '/tmp/fix_partition.sql')
        sftp.close()
        
        # Executar arquivo SQL
        print("3️⃣ Executando arquivo SQL...")
        cmd = """docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy < /tmp/fix_partition.sql"""
        execute_command(client, cmd)
        
        print("\n✅ FIX COMPLETO!")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix()

