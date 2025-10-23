#!/usr/bin/env python3
"""
Script para fazer deploy da correção do backend (UTF-8 encoding)
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
        print(output[-1500:] if len(output) > 1500 else output)
    
    return output, error

def deploy():
    """Faz deploy da correção"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Copiar arquivo atualizado
        print("📁 Copiando main.py via SFTP...")
        sftp = client.open_sftp()
        sftp.put(
            r"C:\Users\Usuario\Desktop\site_Dojo_Final\poker-academy-backend\poker_academy_api\src\main.py",
            "/root/Dojo_Deploy/poker-academy/poker-academy-backend/poker_academy_api/src/main.py"
        )
        print("✅ main.py copiado!")
        sftp.close()
        
        # Fazer rebuild
        print("\n🔨 Fazendo rebuild do backend...")
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose down poker_backend")
        time.sleep(5)
        
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose build --no-cache backend")
        time.sleep(60)
        
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d poker_backend")
        time.sleep(15)
        
        # Verificar status
        print("\n📝 Status do backend:")
        output, _ = execute_command(client, "docker ps | grep poker_backend")
        print(output)
        
        # Testar acesso
        print("\n📝 Testando acesso ao backend...")
        output, _ = execute_command(client, "curl -s -o /dev/null -w 'Status: %{http_code}\\n' http://localhost:5000/api/health")
        print(output)
        
        if "200" in output:
            print("\n✅ BACKEND ATUALIZADO COM SUCESSO!")
            print("\n📝 Mudanças aplicadas:")
            print("  - Configurado JSON_AS_ASCII = False")
            print("  - Caracteres UTF-8 agora aparecem corretamente no JSON")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    deploy()

