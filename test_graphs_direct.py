#!/usr/bin/env python3
"""
Script para testar o endpoint de gráficos diretamente
"""
import paramiko
import time

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print("Conectando ao servidor...")
    ssh.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)
    print("Conectado!")
    
    # Fazer uma requisição ao endpoint
    print("\nFazendo requisição ao endpoint /api/student/graphs...")
    stdin, stdout, stderr = ssh.exec_command(
        "curl -s -X GET 'http://localhost:5000/api/student/graphs?year=2025' -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyNiwidXNlcl90eXBlIjoic3R1ZGVudCIsImV4cCI6MTc2MDc0MjI0MSwiaWF0IjoxNzYwNjU1ODQxfQ.bgezp4eN5jBLdvVYvdKSKSQPua_wstc9i1mSXzUEY1E' 2>&1"
    )
    response = stdout.read().decode()
    print("Response:", response)
    
    # Aguardar um pouco
    time.sleep(2)
    
    # Verificar logs do backend
    print("\n=== LOGS DO BACKEND (últimas 50 linhas) ===\n")
    stdin, stdout, stderr = ssh.exec_command(
        "docker logs poker_backend 2>&1 | tail -50"
    )
    logs = stdout.read().decode()
    print(logs)
    
finally:
    ssh.close()

