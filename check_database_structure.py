#!/usr/bin/env python3
"""
Script para verificar a estrutura do banco de dados
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
    
    # Verificar estrutura da tabela student_graphs
    print("\n📊 Estrutura da tabela student_graphs:")
    stdin, stdout, stderr = ssh.exec_command(
        "docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e 'DESCRIBE student_graphs;'"
    )
    print(stdout.read().decode())
    
    # Verificar estrutura da tabela student_leaks
    print("\n📊 Estrutura da tabela student_leaks:")
    stdin, stdout, stderr = ssh.exec_command(
        "docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e 'DESCRIBE student_leaks;'"
    )
    print(stdout.read().decode())
    
    # Verificar dados na tabela student_graphs
    print("\n📊 Dados na tabela student_graphs:")
    stdin, stdout, stderr = ssh.exec_command(
        "docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e 'SELECT * FROM student_graphs LIMIT 5;'"
    )
    print(stdout.read().decode())
    
    # Verificar se há relacionamentos definidos
    print("\n📊 Foreign keys da tabela student_graphs:")
    stdin, stdout, stderr = ssh.exec_command(
        "docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e 'SELECT CONSTRAINT_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_NAME = \"student_graphs\";'"
    )
    print(stdout.read().decode())
    
    print("\n✅ Verificação concluída!")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
finally:
    ssh.close()

