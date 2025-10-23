#!/usr/bin/env python3
"""
Script para reconstrução final v2
"""

import paramiko
import time

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"
SSH_PORT = 22

def execute_command(client, command, timeout=60):
    """Executa um comando via SSH"""
    stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
    time.sleep(2)
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    return output, error

def rebuild():
    """Reconstrói"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Passo 1: Pull do GitHub
        print("📝 Passo 1: Fazendo pull do GitHub...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && git pull origin main")
        print(output)
        
        # Passo 2: Copiar Dockerfile atualizado
        print("\n📝 Passo 2: Copiando Dockerfile atualizado...")
        output, error = execute_command(client, "cp /root/Dojo_Deploy/poker-academy/poker-academy-backend/Dockerfile /root/Dojo_Deploy/poker-academy-backend/Dockerfile")
        print("✅ Dockerfile copiado!\n")
        
        # Passo 3: Parar containers
        print("📝 Passo 3: Parando containers...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose down")
        print("✅ Containers parados!\n")
        
        # Passo 4: Remover imagens
        print("📝 Passo 4: Removendo imagens...")
        output, error = execute_command(client, "docker rmi -f poker-academy_frontend:latest poker-academy_backend:latest 2>/dev/null || true")
        print("✅ Imagens removidas!\n")
        
        # Passo 5: Reconstruir
        print("📝 Passo 5: Reconstruindo...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose build --no-cache --force-rm", timeout=600)
        print("✅ Build concluído!\n")
        
        # Passo 6: Iniciar
        print("📝 Passo 6: Iniciando containers...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d")
        print(output)
        
        # Aguardar
        print("\n⏳ Aguardando containers iniciarem (90 segundos)...")
        time.sleep(90)
        
        # Passo 7: Verificar status
        print("\n📝 Passo 7: Verificando status...")
        output, error = execute_command(client, "docker ps")
        print(output)
        
        # Passo 8: Verificar logs
        print("\n📝 Passo 8: Verificando logs...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose logs 2>&1 | tail -50")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ RECONSTRUÇÃO CONCLUÍDA!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=" * 70)
    print("Reconstrução Final v2")
    print("=" * 70)
    
    input("\nPressione ENTER para continuar...")
    
    rebuild()

