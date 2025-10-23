#!/usr/bin/env python3
"""
Script para corrigir conectividade de rede
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

def fix():
    """Corrige"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar redes
        print("📝 Redes disponíveis:")
        output, error = execute_command(client, "docker network ls")
        print(output)
        
        # Verificar containers conectados à rede
        print("\n📝 Containers na rede poker_network:")
        output, error = execute_command(client, "docker network inspect poker_network 2>/dev/null | grep -A20 'Containers' || echo 'Rede não encontrada'")
        print(output)
        
        # Remover backend
        print("\n📝 Removendo backend...")
        execute_command(client, "docker rm -f poker_backend")
        print("✅ Removido!\n")
        
        # Remover rede
        print("📝 Removendo rede...")
        execute_command(client, "docker network rm poker_network 2>/dev/null || echo 'Rede não encontrada'")
        print("✅ Removida!\n")
        
        # Usar docker-compose para criar tudo corretamente
        print("📝 Usando docker-compose para criar containers...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose down 2>&1 | tail -10")
        print(output)
        
        print("\n⏳ Aguardando 5 segundos...")
        time.sleep(5)
        
        print("\n📝 Iniciando com docker-compose...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d 2>&1 | tail -20")
        print(output)
        
        print("\n⏳ Aguardando 30 segundos...")
        time.sleep(30)
        
        # Verificar status
        print("\n📝 Status dos containers:")
        output, error = execute_command(client, "docker ps")
        print(output)
        
        # Verificar logs do backend
        print("\n📝 Logs do backend:")
        output, error = execute_command(client, "docker logs poker_backend 2>&1 | tail -20")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ REDE CORRIGIDA!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix()

