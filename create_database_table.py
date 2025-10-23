#!/usr/bin/env python3
"""
Script para criar a tabela student_database no banco de dados
"""
import paramiko
import time

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"

# Credenciais do MySQL
MYSQL_USER = "poker_user"
MYSQL_PASSWORD = "Dojo@Sql159357"
MYSQL_DATABASE = "poker_academy"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print("🔌 Conectando ao servidor...")
    ssh.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)
    print("✅ Conectado!")
    
    # SQL para criar a tabela
    sql_commands = [
        # Criar tabela student_database
        f"""
        CREATE TABLE IF NOT EXISTS student_database (
            id INT PRIMARY KEY AUTO_INCREMENT,
            student_id INT NOT NULL,
            month ENUM('jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez') NOT NULL,
            year INT NOT NULL,
            file_url TEXT NOT NULL,
            file_size INT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE KEY unique_student_db_month_year (student_id, month, year)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,
        # Criar diretório de uploads se não existir
        "mkdir -p /root/Dojo_Deploy/poker-academy/uploads/databases"
    ]
    
    # Executar comando SQL
    print("\n📝 Criando tabela student_database...")
    sql_command = sql_commands[0].replace('\n', ' ').strip()
    
    # Usar docker exec para executar no MySQL
    cmd = f"""docker exec poker_mysql mysql -u {MYSQL_USER} -p{MYSQL_PASSWORD} {MYSQL_DATABASE} -e "{sql_command}" """
    
    stdin, stdout, stderr = ssh.exec_command(cmd)
    output = stdout.read().decode()
    error = stderr.read().decode()
    
    if error and "already exists" not in error:
        print(f"⚠️  Erro: {error}")
    else:
        print("✅ Tabela criada com sucesso!")
    
    if output:
        print(f"📊 Output: {output}")
    
    # Criar diretório de uploads
    print("\n📁 Criando diretório de uploads...")
    stdin, stdout, stderr = ssh.exec_command("mkdir -p /root/Dojo_Deploy/poker-academy/uploads/databases && chmod 777 /root/Dojo_Deploy/poker-academy/uploads/databases")
    print("✅ Diretório criado!")
    
    # Verificar se a tabela foi criada
    print("\n🔍 Verificando tabela...")
    verify_cmd = f"""docker exec poker_mysql mysql -u {MYSQL_USER} -p{MYSQL_PASSWORD} {MYSQL_DATABASE} -e "DESCRIBE student_database;" """
    
    stdin, stdout, stderr = ssh.exec_command(verify_cmd)
    output = stdout.read().decode()
    
    if output:
        print("✅ Tabela verificada com sucesso!")
        print(output)
    else:
        print("⚠️  Não foi possível verificar a tabela")
    
    print("\n✅ Script concluído!")
    
finally:
    ssh.close()

