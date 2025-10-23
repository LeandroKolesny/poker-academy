#!/usr/bin/env python3
"""
Script para verificar volumes do Docker
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

def check_volumes():
    """Verifica volumes do Docker"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Listar volumes
        print("📝 Volumes do Docker:")
        output, _ = execute_command(client, "docker volume ls")
        
        # Inspecionar volume do MySQL
        print("\n📝 Inspecionando volume poker-academy_mysql_data:")
        output, _ = execute_command(client, "docker volume inspect poker-academy_mysql_data")
        
        # Verificar conteúdo do volume
        print("\n📝 Conteúdo do volume:")
        output, _ = execute_command(client, "ls -la /var/lib/docker/volumes/poker-academy_mysql_data/_data/poker_academy/")
        
        # Fazer dump do banco atual
        print("\n📝 Fazendo dump do banco atual:")
        output, _ = execute_command(client, "docker exec poker_mysql mysqldump -u poker_user -pDojo@Sql159357 poker_academy > /tmp/poker_academy_current.sql 2>&1 && echo 'Dump criado com sucesso' || echo 'Erro ao criar dump'")
        
        # Verificar tamanho do dump
        print("\n📝 Verificando tamanho do dump:")
        output, _ = execute_command(client, "ls -lh /tmp/poker_academy_current.sql")
        
        # Copiar dump para um local acessível
        print("\n📝 Copiando dump para /root/Dojo_Deploy:")
        output, _ = execute_command(client, "cp /tmp/poker_academy_current.sql /root/Dojo_Deploy/poker_academy_current.sql && echo 'Dump copiado'")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_volumes()

