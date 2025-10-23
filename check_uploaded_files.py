#!/usr/bin/env python3
"""
Script para verificar se os arquivos de upload estão sendo salvos
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
    
    # Verificar se o diretório de uploads existe
    print("\n=== Verificando diretório de uploads ===")
    stdin, stdout, stderr = ssh.exec_command(
        "docker exec poker_backend ls -la /app/uploads/ 2>/dev/null || echo 'Diretório não existe'"
    )
    print(stdout.read().decode())
    
    # Verificar se há subdiretório graphs
    print("\n=== Verificando diretório de gráficos ===")
    stdin, stdout, stderr = ssh.exec_command(
        "docker exec poker_backend ls -la /app/uploads/graphs/ 2>/dev/null || echo 'Diretório não existe'"
    )
    print(stdout.read().decode())
    
    # Verificar volume do Docker
    print("\n=== Verificando volumes do Docker ===")
    stdin, stdout, stderr = ssh.exec_command(
        "docker inspect poker_backend | grep -A 20 'Mounts'"
    )
    print(stdout.read().decode())
    
    # Verificar se há arquivos no volume
    print("\n=== Verificando arquivos no volume ===")
    stdin, stdout, stderr = ssh.exec_command(
        "docker volume inspect poker-academy_backend_uploads"
    )
    print(stdout.read().decode())
    
finally:
    ssh.close()

