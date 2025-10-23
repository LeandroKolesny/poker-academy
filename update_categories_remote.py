#!/usr/bin/env python3
"""
Script para atualizar as categorias no banco de dados remoto via SSH
"""

import paramiko
import time

# Configurações do servidor
SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"
SSH_PORT = 22

# Configurações do banco de dados
DB_USER = "poker_user"
DB_PASSWORD = "Dojo@Sql159357"
DB_NAME = "poker_academy"

# SQL para atualizar as categorias
SQL_COMMANDS = """
USE poker_academy;

-- Verificar o ENUM atual
SELECT COLUMN_TYPE FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'classes' AND COLUMN_NAME = 'category';

-- Converter aulas existentes com categorias antigas
UPDATE classes SET category = 'icm' WHERE category = 'torneos';
UPDATE classes SET category = 'preflop' WHERE category = 'cash';

-- Alterar o ENUM da tabela para as novas categorias
ALTER TABLE classes 
MODIFY COLUMN category ENUM('iniciantes', 'preflop', 'postflop', 'mental', 'icm') 
NOT NULL DEFAULT 'preflop';

-- Verificar se a alteração foi bem-sucedida
SELECT COLUMN_TYPE FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'classes' AND COLUMN_NAME = 'category';

-- Contar aulas por categoria
SELECT category, COUNT(*) as total FROM classes GROUP BY category ORDER BY category;
"""

def execute_remote_sql():
    """Conecta ao servidor remoto e executa os comandos SQL"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD)
        print("✅ Conectado ao servidor SSH!")
        
        # Criar comando MySQL
        mysql_command = f"mysql -u {DB_USER} -p{DB_PASSWORD} {DB_NAME}"
        
        print("\n📝 Executando comandos SQL...")
        stdin, stdout, stderr = client.exec_command(f"echo \"{SQL_COMMANDS}\" | {mysql_command}")
        
        # Aguardar execução
        time.sleep(2)
        
        # Ler output
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        
        if output:
            print("\n✅ Output do SQL:")
            print(output)
        
        if error:
            print("\n⚠️ Erros/Avisos:")
            print(error)
        
        client.close()
        print("\n✅ Conexão fechada!")
        print("\n🎉 Categorias atualizadas com sucesso!")
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("Atualizador de Categorias - Poker Academy")
    print("=" * 60)
    print(f"\nServidor: {SSH_HOST}")
    print(f"Banco de dados: {DB_NAME}")
    print("\nCategorias a serem atualizadas:")
    print("  - Iniciante (iniciantes)")
    print("  - Pré-Flop (preflop)")
    print("  - Pós-Flop (postflop)")
    print("  - Mental Games (mental)")
    print("  - ICM (icm)")
    print("\n" + "=" * 60)
    
    input("\nPressione ENTER para continuar...")
    
    success = execute_remote_sql()
    
    if success:
        print("\n✅ Processo concluído com sucesso!")
    else:
        print("\n❌ Processo falhou!")

