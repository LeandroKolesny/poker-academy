#!/usr/bin/env python3
"""
Script para verificar se os arquivos foram atualizados no servidor
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
    
    # Verificar se o arquivo models.py foi atualizado
    print("\n=== Verificando models.py no servidor ===")
    stdin, stdout, stderr = ssh.exec_command(
        "docker exec poker_backend grep -n 'AttributeError em StudentGraphs' /app/src/models.py"
    )
    result = stdout.read().decode()
    if result:
        print("✅ models.py foi atualizado com o try/except")
        print(result)
    else:
        print("❌ models.py NÃO foi atualizado!")
    
    # Verificar se o arquivo graphs_routes.py foi atualizado
    print("\n=== Verificando graphs_routes.py no servidor ===")
    stdin, stdout, stderr = ssh.exec_command(
        "docker exec poker_backend grep -n 'StudentGraphs.__mapper__.relationships' /app/src/routes/graphs_routes.py"
    )
    result = stdout.read().decode()
    if result:
        print("✅ graphs_routes.py foi atualizado com os logs")
        print(result)
    else:
        print("❌ graphs_routes.py NÃO foi atualizado!")
    
    # Verificar o conteúdo do to_dict
    print("\n=== Conteúdo do to_dict em models.py ===")
    stdin, stdout, stderr = ssh.exec_command(
        "docker exec poker_backend sed -n '190,205p' /app/src/models.py"
    )
    result = stdout.read().decode()
    print(result)
    
finally:
    ssh.close()

