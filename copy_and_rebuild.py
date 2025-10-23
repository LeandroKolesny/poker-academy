#!/usr/bin/env python3
"""
Script para copiar arquivos e fazer rebuild
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
    
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    
    if output:
        print(output)
    
    return output, error

def copy_and_rebuild():
    """Copia arquivos e faz rebuild"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Copiar arquivos via SFTP
        print("📁 Copiando arquivos via SFTP...")
        sftp = client.open_sftp()
        
        # Copiar models.py
        print("📝 Copiando models.py...")
        sftp.put(
            r"C:\Users\Usuario\Desktop\site_Dojo_Final\poker-academy-backend\poker_academy_api\src\models.py",
            "/root/Dojo_Deploy/poker-academy-backend/poker_academy_api/src/models.py"
        )
        print("✅ models.py copiado!")
        
        # Copiar class_routes.py
        print("📝 Copiando class_routes.py...")
        sftp.put(
            r"C:\Users\Usuario\Desktop\site_Dojo_Final\poker-academy-backend\poker_academy_api\src\routes\class_routes.py",
            "/root/Dojo_Deploy/poker-academy-backend/poker_academy_api/src/routes/class_routes.py"
        )
        print("✅ class_routes.py copiado!")
        
        sftp.close()
        
        # Fazer rebuild
        print("\n🔨 Fazendo rebuild...")
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose down")
        time.sleep(5)
        
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose build --no-cache backend")
        time.sleep(30)
        
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d")
        time.sleep(15)
        
        # Testar login
        print("\n📝 Testando login...")
        output, _ = execute_command(client, """docker exec poker_backend curl -s -X POST http://localhost:5000/api/auth/login -H 'Content-Type: application/json' -d '{"username":"admin","password":"admin123"}'""")
        print(output)
        
        if '"token"' in output:
            print("\n✅ LOGIN BEM-SUCEDIDO!")
        else:
            print("\n❌ LOGIN FALHOU")
            print("\n📝 Últimos logs:")
            output, _ = execute_command(client, "docker logs poker_backend 2>&1 | tail -30")
            print(output)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    copy_and_rebuild()

