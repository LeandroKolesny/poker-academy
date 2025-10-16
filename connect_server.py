#!/usr/bin/env python3
import paramiko
import sys

# Configurações do servidor
HOST = '142.93.206.128'
USER = 'root'
PASSWORD = 'DojoShh159357'
PORT = 22

def connect_and_execute(commands):
    """Conecta ao servidor e executa comandos"""
    try:
        # Criar cliente SSH
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Conectar ao servidor
        print(f"Conectando ao servidor {HOST}...")
        client.connect(HOST, port=PORT, username=USER, password=PASSWORD, timeout=10)
        print("✓ Conectado com sucesso!")
        
        # Executar cada comando
        for cmd in commands:
            print(f"\n→ Executando: {cmd}")
            stdin, stdout, stderr = client.exec_command(cmd)
            output = stdout.read().decode()
            error = stderr.read().decode()
            
            if output:
                print(output)
            if error:
                print(f"Erro: {error}")
        
        client.close()
        print("\n✓ Desconectado do servidor")
        
    except Exception as e:
        print(f"✗ Erro ao conectar: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Comandos para subir o servidor
    commands = [
        "cd /root/Dojo_Deploy && docker-compose up -d",
        "sleep 5",
        "docker-compose ps",
        "docker logs poker-academy-backend 2>&1 | tail -20"
    ]
    
    connect_and_execute(commands)

