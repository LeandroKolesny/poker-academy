#!/usr/bin/env python3
"""
Script para monitorar os logs do backend em tempo real
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
    
    print("\n=== MONITORANDO LOGS DO BACKEND ===")
    print("Aguardando requisições... (Ctrl+C para sair)\n")
    
    last_line_count = 0
    
    while True:
        try:
            stdin, stdout, stderr = ssh.exec_command(
                "docker logs poker_backend 2>&1 | tail -100"
            )
            logs = stdout.read().decode()
            lines = logs.strip().split('\n')
            
            if len(lines) > last_line_count:
                # Mostrar apenas as novas linhas
                new_lines = lines[last_line_count:]
                for line in new_lines:
                    print(line)
                last_line_count = len(lines)
            
            time.sleep(2)
        except KeyboardInterrupt:
            print("\n\nMonitoramento interrompido!")
            break
        except Exception as e:
            print(f"Erro: {e}")
            time.sleep(5)
    
finally:
    ssh.close()

