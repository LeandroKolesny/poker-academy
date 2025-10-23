#!/usr/bin/env python3
"""
Script para forçar rebuild do backend
"""

import paramiko
import time

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"
SSH_PORT = 22

def execute_command(client, command, timeout=120):
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
        
        # Verificar Dockerfile no servidor
        print("📝 Verificando Dockerfile no servidor...")
        output, error = execute_command(client, "cat /root/Dojo_Deploy/poker-academy-backend/Dockerfile | grep -A 5 'Instalar dependências'")
        print(output)
        
        # Parar containers
        print("\n📝 Parando containers...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy && docker-compose down")
        print("✅ Containers parados!")
        
        # Remover imagens
        print("\n📝 Removendo imagens antigas...")
        output, error = execute_command(client, "docker rmi poker-academy_backend -f")
        print("✅ Imagens removidas!")
        
        # Copiar Dockerfile atualizado via SSH
        print("\n📝 Copiando Dockerfile atualizado...")
        sftp = client.open_sftp()
        sftp.put('C:\\Users\\Usuario\\Desktop\\site_Dojo_Final\\poker-academy-backend\\Dockerfile', 
                 '/root/Dojo_Deploy/poker-academy-backend/Dockerfile')
        sftp.close()
        print("✅ Dockerfile copiado!")
        
        # Verificar se foi copiado
        print("\n📝 Verificando Dockerfile copiado...")
        output, error = execute_command(client, "cat /root/Dojo_Deploy/poker-academy-backend/Dockerfile | grep -A 5 'Instalar dependências'")
        print(output)
        
        # Reconstruir com --no-cache
        print("\n📝 Reconstruindo backend com --no-cache...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy && docker-compose build --no-cache backend", timeout=300)
        print(output[-1000:] if len(output) > 1000 else output)
        
        # Iniciar
        print("\n📝 Iniciando containers...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy && docker-compose up -d")
        print("✅ Containers iniciados!")
        
        # Aguardar
        print("\n⏳ Aguardando 30 segundos...")
        time.sleep(30)
        
        # Verificar status
        print("\n📝 Status do backend:")
        output, error = execute_command(client, "docker ps | grep backend")
        print(output)
        
        # Verificar se curl está instalado
        print("\n📝 Verificando se curl está instalado...")
        output, error = execute_command(client, "docker exec poker_backend which curl")
        print(f"Response: {output}")
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ REBUILD FORÇADO CONCLUÍDO!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    rebuild()

