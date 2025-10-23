#!/usr/bin/env python3
"""
Script para verificar se o arquivo foi atualizado
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
        print(output[-2000:] if len(output) > 2000 else output)
    
    return output, error

def verify():
    """Verifica arquivo"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar se o arquivo contém a correção
        print("📝 Procurando pela correção no arquivo:")
        output, _ = execute_command(client, "grep -n 'includes.*T' /root/Dojo_Deploy/poker-academy/poker-academy/src/components/admin/ClassManagement.js")
        
        if not output or "includes" not in output:
            print("\n❌ ARQUIVO NÃO FOI ATUALIZADO!")
            print("\n📝 Verificando conteúdo atual (linhas 96-110):")
            output, _ = execute_command(client, "sed -n '96,110p' /root/Dojo_Deploy/poker-academy/poker-academy/src/components/admin/ClassManagement.js")
        else:
            print("\n✅ Arquivo foi atualizado corretamente!")
        
        # Verificar data do arquivo
        print("\n📝 Data de modificação do arquivo:")
        output, _ = execute_command(client, "ls -lh /root/Dojo_Deploy/poker-academy/poker-academy/src/components/admin/ClassManagement.js")
        
        # Verificar se o build foi feito
        print("\n📝 Verificando se o build foi feito:")
        output, _ = execute_command(client, "ls -lh /root/Dojo_Deploy/poker-academy/poker-academy/build/static/js/main.*.js | tail -1")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify()

