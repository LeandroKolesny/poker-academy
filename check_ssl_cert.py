#!/usr/bin/env python3
"""
Script para verificar certificado SSL
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

def check():
    """Verifica"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar se o diretório letsencrypt existe
        print("1️⃣ Verificando /etc/letsencrypt...")
        cmd1 = "ls -la /etc/letsencrypt/ 2>&1 || echo 'Diretório não existe'"
        execute_command(client, cmd1)
        
        # Verificar se o certificado existe
        print("\n2️⃣ Verificando certificado...")
        cmd2 = "ls -la /etc/letsencrypt/live/cardroomgrinders.com.br/ 2>&1 || echo 'Certificado não existe'"
        execute_command(client, cmd2)
        
        # Verificar nginx.conf
        print("\n3️⃣ Verificando nginx.conf...")
        cmd3 = "cat /root/Dojo_Deploy/poker-academy/nginx.conf | head -50"
        execute_command(client, cmd3)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check()

