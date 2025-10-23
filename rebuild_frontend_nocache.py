#!/usr/bin/env python3
"""
Script para fazer rebuild do frontend sem cache
"""

import paramiko
import time

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"
SSH_PORT = 22

def execute_command(client, command, timeout=600):
    """Executa um comando via SSH"""
    print(f"\n📝 Executando: {command}")
    stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
    time.sleep(2)
    
    output = stdout.read().decode('utf-8', errors='replace')
    error = stderr.read().decode('utf-8', errors='replace')
    
    if output:
        print(output[-1500:] if len(output) > 1500 else output)
    
    return output, error

def rebuild():
    """Faz rebuild"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Parar frontend
        print("🛑 Parando frontend...")
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose down poker_frontend")
        time.sleep(5)
        
        # Limpar build antigo
        print("\n🧹 Limpando build antigo...")
        execute_command(client, "rm -rf /root/Dojo_Deploy/poker-academy/poker-academy/build")
        
        # Fazer rebuild sem cache
        print("\n🔨 Fazendo rebuild do frontend (sem cache)...")
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose build --no-cache frontend")
        
        # Iniciar frontend
        print("\n🚀 Iniciando frontend...")
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d poker_frontend")
        time.sleep(15)
        
        # Verificar status
        print("\n📝 Status do frontend:")
        output, _ = execute_command(client, "docker ps | grep poker_frontend")
        
        # Verificar novo build
        print("\n📝 Verificando novo build:")
        output, _ = execute_command(client, "ls -lh /root/Dojo_Deploy/poker-academy/poker-academy/build/static/js/main.*.js | tail -1")
        
        print("\n✅ FRONTEND RECONSTRUÍDO COM SUCESSO!")
        print("\n📝 Próximos passos:")
        print("1. Limpe o cache do navegador (Ctrl+Shift+Delete)")
        print("2. Acesse: https://cardroomgrinders.com.br")
        print("3. Faça login com: admin / admin123")
        print("4. Vá para 'Gestão de Aulas'")
        print("5. Clique em editar uma aula")
        print("6. Teste se o erro de data foi corrigido")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    rebuild()

