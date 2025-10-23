#!/usr/bin/env python3
"""
Script para verificar se os arquivos do frontend foram copiados corretamente
"""
import paramiko

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print("🔌 Conectando ao servidor...")
    ssh.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)
    print("✅ Conectado!")
    
    # Verificar se MonthlyDatabase.js existe
    print("\n📁 Verificando MonthlyDatabase.js...")
    cmd = "ls -la /root/Dojo_Deploy/poker-academy/poker-academy/src/components/student/MonthlyDatabase.js"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    output = stdout.read().decode()
    error = stderr.read().decode()
    
    if error:
        print(f"❌ Arquivo não encontrado: {error}")
    else:
        print(f"✅ Arquivo encontrado:\n{output}")
    
    # Verificar se Sidebar.js foi atualizado
    print("\n📁 Verificando Sidebar.js...")
    cmd = "grep -n 'Database Mensal' /root/Dojo_Deploy/poker-academy/poker-academy/src/components/shared/Sidebar.js"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    output = stdout.read().decode()
    
    if output:
        print(f"✅ 'Database Mensal' encontrado em Sidebar.js:\n{output}")
    else:
        print("❌ 'Database Mensal' NÃO encontrado em Sidebar.js")
    
    # Verificar se AdminMonthlyDatabase.js existe
    print("\n📁 Verificando AdminMonthlyDatabase.js...")
    cmd = "ls -la /root/Dojo_Deploy/poker-academy/poker-academy/src/components/admin/AdminMonthlyDatabase.js"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    output = stdout.read().decode()
    error = stderr.read().decode()
    
    if error:
        print(f"❌ Arquivo não encontrado: {error}")
    else:
        print(f"✅ Arquivo encontrado:\n{output}")
    
    # Verificar se AdminPanel.js foi atualizado
    print("\n📁 Verificando AdminPanel.js...")
    cmd = "grep -n 'AdminMonthlyDatabase' /root/Dojo_Deploy/poker-academy/poker-academy/src/components/admin/AdminPanel.js"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    output = stdout.read().decode()
    
    if output:
        print(f"✅ 'AdminMonthlyDatabase' encontrado em AdminPanel.js:\n{output}")
    else:
        print("❌ 'AdminMonthlyDatabase' NÃO encontrado em AdminPanel.js")
    
finally:
    ssh.close()

