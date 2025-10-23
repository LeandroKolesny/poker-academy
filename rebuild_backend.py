#!/usr/bin/env python3
"""
Script para fazer rebuild do backend
"""

import paramiko
import time

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"
SSH_PORT = 22

def execute_command(client, command, timeout=300):
    """Executa um comando via SSH"""
    print(f"\n📝 Executando: {command}")
    stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
    time.sleep(2)

    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')

    if output:
        print(output)
    if error:
        print(f"❌ Erro: {error}")

    return output, error

def rebuild():
    """Faz rebuild do backend"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Parar container
        print("🛑 Parando container do backend...")
        execute_command(client, "docker stop poker_backend")
        time.sleep(2)
        
        # Remover container
        print("🗑️  Removendo container do backend...")
        execute_command(client, "docker rm poker_backend")
        time.sleep(2)
        
        # Rebuild imagem
        print("🔨 Fazendo rebuild da imagem...")
        execute_command(client, "cd /root/Dojo_Deploy && docker build -t poker_backend_image ./poker-academy-backend", timeout=600)
        time.sleep(2)
        
        # Iniciar novo container
        print("🚀 Iniciando novo container...")
        execute_command(client, """docker run -d \\
            --name poker_backend \\
            --network poker_network \\
            -e FLASK_ENV=production \\
            -e DATABASE_URL='mysql+pymysql://poker_user:Dojo@Sql159357@poker_mysql:3306/poker_academy' \\
            -p 5000:5000 \\
            poker_backend_image""")
        time.sleep(5)
        
        # Verificar status
        print("\n📝 Verificando status do container...")
        output, _ = execute_command(client, "docker ps | grep poker_backend")
        print(output)
        
        # Testar endpoint
        print("\n📝 Testando endpoint /api/classes...")
        output, _ = execute_command(client, "docker exec poker_backend curl -s http://localhost:5000/api/test")
        print(output)
        
        # Verificar logs
        print("\n📝 Logs do backend (últimas 30 linhas):")
        output, _ = execute_command(client, "docker logs poker_backend 2>&1 | tail -30")
        print(output)
        
        client.close()
        print("\n✅ Rebuild concluído!")
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    rebuild()

