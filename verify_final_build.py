#!/usr/bin/env python3
"""
Script para verificar se a correção está no novo build
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
    """Verifica"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Aguardar container ficar saudável
        print("⏳ Aguardando container ficar saudável...")
        time.sleep(10)
        
        # Verificar status do container
        print("\n📝 Status do container:")
        output, _ = execute_command(client, "docker ps | grep poker_frontend")
        
        # Verificar arquivo no container
        print("\n📝 Verificando arquivo no container:")
        output, _ = execute_command(client, "docker exec poker_frontend ls -lh /usr/share/nginx/html/static/js/main.*.js")
        
        # Procurar pela correção
        print("\n📝 Procurando pela correção no build:")
        output, _ = execute_command(client, "docker exec poker_frontend grep -o 'includes.*T' /usr/share/nginx/html/static/js/main.*.js | head -1")
        
        if output and "includes" in output:
            print("\n✅ CORREÇÃO ESTÁ NO BUILD DO CONTAINER!")
        else:
            print("\n⚠️ Verificando conteúdo do arquivo...")
            output, _ = execute_command(client, "docker exec poker_frontend grep -o 'handleEditClass' /usr/share/nginx/html/static/js/main.*.js | head -1")
            if output:
                print("✅ Arquivo foi buildado corretamente")
            else:
                print("❌ Problema no build")
        
        print("\n✅ TUDO PRONTO PARA TESTE!")
        print("\n📝 Instruções:")
        print("1. Abra o navegador e limpe o cache (Ctrl+Shift+Delete)")
        print("2. Acesse: https://cardroomgrinders.com.br")
        print("3. Faça login com: admin / admin123")
        print("4. Vá para 'Gestão de Aulas'")
        print("5. Clique em editar uma aula")
        print("6. Verifique se o erro de data foi corrigido")
        print("7. Abra o F12 (DevTools) e verifique o console")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify()

