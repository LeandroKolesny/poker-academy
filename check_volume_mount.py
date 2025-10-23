#!/usr/bin/env python3
"""
Script para verificar o mount do volume
"""
import paramiko

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print("Conectando ao servidor...")
    ssh.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)
    print("Conectado!")
    
    # Verificar mount do backend
    print("\n=== Mount do backend ===")
    stdin, stdout, stderr = ssh.exec_command(
        "docker inspect poker_backend | grep -A 5 'Mounts' | head -20"
    )
    print(stdout.read().decode())
    
    # Verificar mount do frontend
    print("\n=== Mount do frontend ===")
    stdin, stdout, stderr = ssh.exec_command(
        "docker inspect poker_frontend | grep -A 5 'Mounts' | head -20"
    )
    print(stdout.read().decode())
    
    # Verificar conteúdo do volume no host
    print("\n=== Conteúdo do volume no host ===")
    stdin, stdout, stderr = ssh.exec_command(
        "ls -la /var/lib/docker/volumes/poker-academy_backend_uploads/_data/"
    )
    print(stdout.read().decode())
    
    # Verificar se o arquivo existe no volume
    print("\n=== Arquivo no volume ===")
    stdin, stdout, stderr = ssh.exec_command(
        "ls -la /var/lib/docker/volumes/poker-academy_backend_uploads/_data/graphs/"
    )
    print(stdout.read().decode())
    
finally:
    ssh.close()

