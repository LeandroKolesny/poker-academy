#!/usr/bin/env python3
"""
Script para verificar e reconstruir
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

def verify():
    """Verifica e reconstrói"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar Dockerfile
        print("📋 Verificando Dockerfile:")
        output, error = execute_command(client, "cat /root/Dojo_Deploy/poker-academy-backend/Dockerfile | tail -20")
        print(output)
        
        # Limpar cache do Docker
        print("\n📝 Limpando cache do Docker...")
        output, error = execute_command(client, "docker system prune -af")
        print("✅ Cache limpo!\n")
        
        # Parar containers
        print("📝 Parando containers...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose down")
        print("✅ Containers parados!\n")
        
        # Remover imagens
        print("📝 Removendo imagens...")
        output, error = execute_command(client, "docker rmi -f $(docker images -q) 2>/dev/null || true")
        print("✅ Imagens removidas!\n")
        
        # Reconstruir
        print("📝 Reconstruindo...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose build --no-cache --force-rm", timeout=600)
        print("✅ Build concluído!\n")
        
        # Iniciar
        print("📝 Iniciando containers...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d")
        print(output)
        
        # Aguardar
        print("\n⏳ Aguardando containers iniciarem (90 segundos)...")
        time.sleep(90)
        
        # Verificar status
        print("\n📝 Verificando status...")
        output, error = execute_command(client, "docker ps")
        print(output)
        
        # Verificar logs
        print("\n📝 Verificando logs...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose logs 2>&1 | tail -50")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ PROCESSO CONCLUÍDO!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=" * 70)
    print("Verificação e Reconstrução")
    print("=" * 70)
    
    input("\nPressione ENTER para continuar...")
    
    verify()

