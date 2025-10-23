#!/usr/bin/env python3
"""
Script para criar um aluno de teste
"""
import paramiko
import hashlib

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"

MYSQL_USER = "poker_user"
MYSQL_PASSWORD = "Dojo@Sql159357"
MYSQL_DATABASE = "poker_academy"

# Dados do aluno de teste
TEST_STUDENT_NAME = "Aluno Teste"
TEST_STUDENT_USERNAME = "aluno_teste"
TEST_STUDENT_EMAIL = "aluno@teste.com"
TEST_STUDENT_PASSWORD = "123456"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print("🔌 Conectando ao servidor...")
    ssh.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)
    print("✅ Conectado!")
    
    # Hash da senha (bcrypt)
    # Para simplificar, vou usar um hash pré-calculado
    # Você pode gerar com: python -c "import bcrypt; print(bcrypt.hashpw(b'123456', bcrypt.gensalt()).decode())"
    password_hash = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5YmMxSUmGEJiq"  # hash de "123456"
    
    # Inserir aluno
    print("\n👤 Criando aluno de teste...")
    sql = f"""
    INSERT INTO users (name, username, email, password_hash, type, created_at, updated_at)
    VALUES ('{TEST_STUDENT_NAME}', '{TEST_STUDENT_USERNAME}', '{TEST_STUDENT_EMAIL}', '{password_hash}', 'student', NOW(), NOW());
    """
    
    cmd = f"""docker exec poker_mysql mysql -u {MYSQL_USER} -p{MYSQL_PASSWORD} {MYSQL_DATABASE} -e "{sql}" """
    
    stdin, stdout, stderr = ssh.exec_command(cmd)
    output = stdout.read().decode()
    error = stderr.read().decode()
    
    if error and "duplicate" not in error.lower():
        print(f"⚠️  Erro: {error}")
    else:
        print("✅ Aluno criado com sucesso!")
    
    # Verificar aluno criado
    print("\n📋 Verificando aluno criado:")
    verify_cmd = f"""docker exec poker_mysql mysql -u {MYSQL_USER} -p{MYSQL_PASSWORD} {MYSQL_DATABASE} -e "SELECT id, name, username, type FROM users WHERE username='{TEST_STUDENT_USERNAME}';" """
    
    stdin, stdout, stderr = ssh.exec_command(verify_cmd)
    output = stdout.read().decode()
    
    print(output)
    
    print(f"\n✅ Credenciais de teste:")
    print(f"   Username: {TEST_STUDENT_USERNAME}")
    print(f"   Password: {TEST_STUDENT_PASSWORD}")
    
finally:
    ssh.close()

