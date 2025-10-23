#!/usr/bin/env python3
"""
Script para verificar se o NGINX consegue acessar os uploads
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
    
    # Verificar se o NGINX consegue acessar os uploads
    print("\n=== Verificando acesso do NGINX aos uploads ===")
    stdin, stdout, stderr = ssh.exec_command(
        "docker exec poker_frontend ls -la /app/uploads/graphs/ 2>/dev/null || echo 'Diretório não acessível'"
    )
    print(stdout.read().decode())
    
    # Verificar logs do NGINX
    print("\n=== Logs do NGINX (últimas 30 linhas) ===")
    stdin, stdout, stderr = ssh.exec_command(
        "docker logs poker_frontend 2>&1 | tail -30"
    )
    print(stdout.read().decode())
    
    # Testar acesso direto ao arquivo via curl
    print("\n=== Testando acesso ao arquivo via curl ===")
    stdin, stdout, stderr = ssh.exec_command(
        "curl -s -I https://cardroomgrinders.com.br/api/uploads/graphs/graph_26_fev_2025_8894168d.png 2>&1 | head -20"
    )
    print(stdout.read().decode())
    
finally:
    ssh.close()

