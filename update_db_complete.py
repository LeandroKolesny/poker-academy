#!/usr/bin/env python3
"""
Script completo para atualizar categorias no servidor
1. Conecta via SSH
2. Envia o arquivo SQL
3. Executa o SQL
4. Reconstrói os containers Docker
5. Reinicia a aplicação
"""

import paramiko
import time
import os

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
SQL_CONTENT = """-- Script para adicionar a categoria "iniciantes" ao ENUM da tabela classes
USE poker_academy;

-- Verificar o ENUM atual
SELECT COLUMN_TYPE FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'classes' AND COLUMN_NAME = 'category';

-- Modificar a coluna category para adicionar 'iniciantes' como primeira opção
ALTER TABLE classes
MODIFY COLUMN category ENUM('iniciantes', 'preflop', 'postflop', 'mental', 'icm') NOT NULL DEFAULT 'preflop';

-- Verificar se a alteração foi bem-sucedida
SELECT COLUMN_TYPE FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'classes' AND COLUMN_NAME = 'category';

-- Contar aulas por categoria
SELECT category, COUNT(*) as total FROM classes GROUP BY category ORDER BY category;

-- Confirmar que a tabela foi atualizada
SHOW CREATE TABLE classes;
"""

def execute_command_ssh(client, command):
    """Executa um comando via SSH e retorna o output"""
    stdin, stdout, stderr = client.exec_command(command)
    time.sleep(1)
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    return output, error

def update_database():
    """Executa todo o processo de atualização"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Passo 1: Criar arquivo SQL no servidor
        print("📝 Passo 1: Criando arquivo SQL no servidor...")
        sql_file_path = "/tmp/update_categories.sql"
        
        # Usar SFTP para enviar o arquivo
        sftp = client.open_sftp()
        with sftp.file(sql_file_path, 'w') as f:
            f.write(SQL_CONTENT)
        sftp.close()
        print(f"✅ Arquivo SQL criado em {sql_file_path}\n")
        
        # Passo 2: Executar o SQL
        print("📝 Passo 2: Executando SQL no banco de dados...")
        command = f"mysql -u {DB_USER} -p{DB_PASSWORD} {DB_NAME} < {sql_file_path}"
        output, error = execute_command_ssh(client, command)
        
        if output:
            print("✅ Output do SQL:")
            print(output)
        
        if error and "Warning" not in error:
            print("⚠️ Erros:")
            print(error)
        
        print()
        
        # Passo 3: Verificar se a atualização foi bem-sucedida
        print("📝 Passo 3: Verificando se as categorias foram atualizadas...")
        verify_command = f"mysql -u {DB_USER} -p{DB_PASSWORD} {DB_NAME} -e \"SELECT COLUMN_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'classes' AND COLUMN_NAME = 'category';\""
        output, error = execute_command_ssh(client, verify_command)
        
        if "iniciantes" in output and "icm" in output:
            print("✅ Categorias atualizadas com sucesso no banco de dados!")
            print(output)
        else:
            print("❌ Erro ao atualizar categorias!")
            print(output)
            return False
        
        print()
        
        # Passo 4: Reconstruir containers Docker
        print("📝 Passo 4: Reconstruindo containers Docker...")
        docker_commands = [
            "cd /root/Dojo_Deploy && docker-compose build",
            "cd /root/Dojo_Deploy && docker-compose up -d",
            "sleep 5",
            "docker-compose ps"
        ]
        
        for cmd in docker_commands:
            print(f"  Executando: {cmd}")
            output, error = execute_command_ssh(client, cmd)
            if output:
                print(f"  {output[:200]}...")
            if error and "Warning" not in error:
                print(f"  ⚠️ {error[:200]}...")
        
        print("✅ Containers reconstruídos e reiniciados!\n")
        
        # Passo 5: Verificar status dos containers
        print("📝 Passo 5: Verificando status dos containers...")
        output, error = execute_command_ssh(client, "docker-compose -f /root/Dojo_Deploy/docker-compose.yml ps")
        print(output)
        
        client.close()
        print("\n✅ Conexão fechada!")
        print("\n" + "=" * 70)
        print("🎉 PROCESSO CONCLUÍDO COM SUCESSO!")
        print("=" * 70)
        print("\nO que foi feito:")
        print("  ✅ Banco de dados atualizado com novas categorias")
        print("  ✅ Containers Docker reconstruídos")
        print("  ✅ Aplicação reiniciada")
        print("\nPróximos passos:")
        print("  1. Aguarde 30 segundos para a aplicação iniciar")
        print("  2. Acesse http://grinders.com.br")
        print("  3. Teste as novas categorias (Iniciante, Pré-Flop, Pós-Flop, Mental Games, ICM)")
        print("  4. Tente editar uma aula existente para verificar se as categorias aparecem")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("Atualizador Completo de Categorias - Poker Academy")
    print("=" * 70)
    print(f"\nServidor: {SSH_HOST}")
    print(f"Banco de dados: {DB_NAME}")
    print("\nEste script irá:")
    print("  1. Conectar ao servidor via SSH")
    print("  2. Enviar arquivo SQL")
    print("  3. Executar SQL para atualizar categorias")
    print("  4. Reconstruir containers Docker")
    print("  5. Reiniciar a aplicação")
    print("\nNovas categorias:")
    print("  - Iniciante (iniciantes)")
    print("  - Pré-Flop (preflop)")
    print("  - Pós-Flop (postflop)")
    print("  - Mental Games (mental)")
    print("  - ICM (icm)")
    print("\n" + "=" * 70)
    
    input("\nPressione ENTER para continuar...")
    
    success = update_database()
    
    if not success:
        print("\n❌ Processo falhou!")

