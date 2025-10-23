#!/usr/bin/env python3
"""
Script para fazer rebuild completo do frontend
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
        
        # Parar todos os containers
        print("🛑 Parando containers...")
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose down")
        time.sleep(5)
        
        # Remover imagens antigas
        print("\n🧹 Removendo imagens antigas...")
        execute_command(client, "docker rmi poker-academy_frontend:latest 2>/dev/null || true")
        
        # Fazer rebuild
        print("\n🔨 Fazendo rebuild do frontend...")
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose build --no-cache frontend")
        
        # Iniciar todos os containers
        print("\n🚀 Iniciando containers...")
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d")
        time.sleep(20)
        
        # Verificar status
        print("\n📝 Status dos containers:")
        output, _ = execute_command(client, "docker ps | grep poker")
        
        print("\n✅ REBUILD COMPLETO CONCLUÍDO!")
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

