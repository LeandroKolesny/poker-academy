#!/usr/bin/env python3
"""
Script para verificar logs do backend e debug
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

def check_logs():
    """Verifica os logs"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar containers
        print("📋 Status dos containers:")
        output, error = execute_command(client, "cd /root/Dojo_Deploy && docker-compose ps")
        print(output)
        
        # Verificar logs do backend
        print("\n📋 Últimos 50 linhas dos logs do backend:")
        output, error = execute_command(client, "cd /root/Dojo_Deploy && docker-compose logs poker-academy-backend | tail -50")
        print(output)
        
        # Verificar se o arquivo models.py tem o enum correto
        print("\n📋 Verificando ClassCategory enum no models.py:")
        output, error = execute_command(client, "grep -A 10 'class ClassCategory' /root/Dojo_Deploy/poker-academy/poker-academy-backend/poker_academy_api/src/models.py")
        print(output)
        
        # Verificar se o arquivo class_routes.py tem a normalização correta
        print("\n📋 Verificando normalize_category no class_routes.py:")
        output, error = execute_command(client, "grep -A 20 'def normalize_category' /root/Dojo_Deploy/poker-academy/poker-academy-backend/poker_academy_api/src/routes/class_routes.py")
        print(output)
        
        # Verificar o endpoint de categorias
        print("\n📋 Testando endpoint de categorias:")
        output, error = execute_command(client, "curl -s http://localhost:5000/api/classes/categories 2>&1 | head -20")
        print(output)
        
        # Verificar se há erro ao conectar no banco
        print("\n📋 Testando conexão com banco de dados:")
        output, error = execute_command(client, "mysql -h 127.0.0.1 -u poker_user -pDojo@Sql159357 poker_academy -e 'SELECT COLUMN_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = \"classes\" AND COLUMN_NAME = \"category\";'")
        print(output)
        
        client.close()
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_logs()

