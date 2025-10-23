#!/usr/bin/env python3
"""
Script para verificar o status do servidor e dos containers
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

def check_server():
    """Verifica o status do servidor"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar status dos containers
        print("📋 Status dos containers Docker:")
        output, error = execute_command(client, "cd /root/Dojo_Deploy && docker-compose ps")
        print(output)
        
        # Verificar logs do MySQL
        print("\n📋 Últimos logs do MySQL:")
        output, error = execute_command(client, "docker logs poker-academy-mysql 2>&1 | tail -20")
        print(output)
        
        # Verificar se MySQL está rodando
        print("\n📋 Verificando se MySQL está rodando:")
        output, error = execute_command(client, "docker ps | grep mysql")
        print(output if output else "❌ MySQL não está rodando")
        
        # Tentar conectar ao MySQL
        print("\n📋 Tentando conectar ao MySQL:")
        output, error = execute_command(client, "mysql -h 127.0.0.1 -u poker_user -pDojo@Sql159357 poker_academy -e 'SELECT 1;'")
        if output:
            print("✅ Conexão bem-sucedida!")
            print(output)
        else:
            print("❌ Erro ao conectar:")
            print(error)
        
        client.close()
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

if __name__ == "__main__":
    check_server()

