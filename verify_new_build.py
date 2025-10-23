#!/usr/bin/env python3
"""
Script para verificar novo build
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
    """Verifica novo build"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar novo build
        print("📝 Verificando novo build:")
        output, _ = execute_command(client, "ls -lh /root/Dojo_Deploy/poker-academy/poker-academy/build/static/js/main.*.js")
        
        # Verificar se contém a correção
        print("\n📝 Procurando pela correção no build:")
        output, _ = execute_command(client, "grep -o 'includes.*T' /root/Dojo_Deploy/poker-academy/poker-academy/build/static/js/main.*.js | head -1")
        
        if output and "includes" in output:
            print("\n✅ CORREÇÃO ESTÁ NO BUILD!")
        else:
            print("\n⚠️ Verificando conteúdo do arquivo fonte novamente...")
            output, _ = execute_command(client, "grep -A 5 'handleEditClass' /root/Dojo_Deploy/poker-academy/poker-academy/src/components/admin/ClassManagement.js | head -20")
        
        # Verificar status do container
        print("\n📝 Status do container:")
        output, _ = execute_command(client, "docker ps | grep poker_frontend")
        
        print("\n✅ TUDO PRONTO!")
        print("\n📝 Agora teste no navegador:")
        print("1. Limpe o cache (Ctrl+Shift+Delete ou Cmd+Shift+Delete)")
        print("2. Acesse: https://cardroomgrinders.com.br")
        print("3. Faça login com: admin / admin123")
        print("4. Vá para 'Gestão de Aulas'")
        print("5. Clique em editar uma aula")
        print("6. Verifique se o erro de data foi corrigido")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify()

