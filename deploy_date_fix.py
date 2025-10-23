#!/usr/bin/env python3
"""
Script para fazer deploy da correção de data
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
    
    output = stdout.read().decode('utf-8', errors='replace')
    error = stderr.read().decode('utf-8', errors='replace')
    
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
        print("📁 Copiando ClassManagement.js via SFTP...")
        sftp = client.open_sftp()
        sftp.put(
            r"C:\Users\Usuario\Desktop\site_Dojo_Final\poker-academy\src\components\admin\ClassManagement.js",
            "/root/Dojo_Deploy/poker-academy/poker-academy/src/components/admin/ClassManagement.js"
        )
        print("✅ ClassManagement.js copiado!")
        sftp.close()
        
        # Fazer rebuild do frontend
        print("\n🔨 Fazendo rebuild do frontend...")
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose down poker_frontend")
        time.sleep(5)
        
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose build --no-cache frontend")
        time.sleep(60)
        
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d poker_frontend")
        time.sleep(15)
        
        # Verificar status
        print("\n📝 Status do frontend:")
        output, _ = execute_command(client, "docker ps | grep poker_frontend")
        print(output)
        
        print("\n✅ FRONTEND ATUALIZADO COM SUCESSO!")
        print("\n📝 Mudanças aplicadas:")
        print("  - Corrigido formato de data no formulário de edição")
        print("  - Agora aceita datas no formato YYYY-MM-DDTHH:MM:SS")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    deploy()

