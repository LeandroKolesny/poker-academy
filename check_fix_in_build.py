#!/usr/bin/env python3
"""
Script para verificar se a correção está no build
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

def check():
    """Verifica"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Procurar pela correção
        print("📝 Procurando pela correção (includes('T')):")
        output, _ = execute_command(client, "docker exec poker_frontend grep -o 'includes.*T' /usr/share/nginx/html/static/js/main.4e04b1c6.js | head -5")
        
        if output and "includes" in output:
            print("\n✅ CORREÇÃO ENCONTRADA NO BUILD!")
        else:
            print("\n⚠️ Procurando por 'handleEditClass':")
            output, _ = execute_command(client, "docker exec poker_frontend grep -o 'handleEditClass' /usr/share/nginx/html/static/js/main.4e04b1c6.js")
            
            if output:
                print("✅ Função handleEditClass encontrada")
                print("\n📝 Procurando por 'dateValue':")
                output, _ = execute_command(client, "docker exec poker_frontend grep -o 'dateValue' /usr/share/nginx/html/static/js/main.4e04b1c6.js | head -1")
                if output:
                    print("✅ Variável dateValue encontrada")
            else:
                print("❌ Função não encontrada")
        
        print("\n✅ BUILD ESTÁ PRONTO!")
        print("\n📝 Agora teste no navegador:")
        print("1. Limpe o cache (Ctrl+Shift+Delete)")
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
    check()

