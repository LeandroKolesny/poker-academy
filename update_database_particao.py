#!/usr/bin/env python3
"""
Script para adicionar campo 'particao' na tabela users do banco poker_academy
Execute este script para atualizar o banco de dados MySQL
"""

import mysql.connector
import sys
from mysql.connector import Error

def update_database():
    """Adiciona campo particao na tabela users"""
    
    # Configurações do banco de dados
    config = {
        'host': 'localhost',
        'database': 'poker_academy',
        'user': 'root',
        'password': '',  # Senha vazia para XAMPP padrão
        'port': 3306
    }
    
    connection = None
    cursor = None
    
    try:
        # Conectar ao MySQL
        print("Conectando ao MySQL...")
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        print("Conectado com sucesso!")

        # Verificar se a coluna já existe
        print("Verificando se a coluna 'particao' já existe...")
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'poker_academy' 
            AND TABLE_NAME = 'users' 
            AND COLUMN_NAME = 'particao'
        """)
        
        column_exists = cursor.fetchone()[0] > 0
        
        if column_exists:
            print("⚠️  A coluna 'particao' já existe na tabela users.")
            
            # Verificar se há registros sem partição
            cursor.execute("SELECT COUNT(*) FROM users WHERE particao IS NULL OR particao = ''")
            empty_particao = cursor.fetchone()[0]
            
            if empty_particao > 0:
                print(f"🔄 Atualizando {empty_particao} registros sem partição...")
                cursor.execute("UPDATE users SET particao = 'Dojo' WHERE particao IS NULL OR particao = ''")
                connection.commit()
                print("✅ Registros atualizados com sucesso!")
            else:
                print("✅ Todos os registros já possuem partição definida.")
        else:
            print("➕ Adicionando coluna 'particao' na tabela users...")
            cursor.execute("ALTER TABLE users ADD COLUMN particao VARCHAR(100) NOT NULL DEFAULT 'Dojo'")
            
            print("🔄 Atualizando registros existentes...")
            cursor.execute("UPDATE users SET particao = 'Dojo' WHERE particao IS NULL OR particao = ''")
            
            connection.commit()
            print("✅ Coluna adicionada e registros atualizados com sucesso!")
        
        # Verificar resultado final
        print("\n📊 Verificando resultado final...")
        cursor.execute("SELECT id, name, username, email, type, particao FROM users")
        users = cursor.fetchall()
        
        print(f"\n👥 Total de usuários: {len(users)}")
        print("\n📋 Lista de usuários:")
        print("-" * 80)
        print(f"{'ID':<4} {'Nome':<20} {'Username':<15} {'Email':<25} {'Tipo':<8} {'Partição':<10}")
        print("-" * 80)
        
        for user in users:
            user_id, name, username, email, user_type, particao = user
            print(f"{user_id:<4} {name[:19]:<20} {username[:14]:<15} {email[:24]:<25} {user_type:<8} {particao:<10}")
        
        print("-" * 80)
        print("✅ Atualização do banco de dados concluída com sucesso!")
        
    except Error as e:
        print(f"❌ Erro ao conectar ao MySQL: {e}")
        if connection and connection.is_connected():
            connection.rollback()
        sys.exit(1)
        
    finally:
        # Fechar conexões
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("🔌 Conexão com MySQL fechada.")

if __name__ == "__main__":
    print("🚀 Iniciando atualização do banco de dados...")
    print("📋 Este script irá:")
    print("   1. Adicionar campo 'particao' na tabela users (se não existir)")
    print("   2. Definir 'Dojo' como valor padrão")
    print("   3. Atualizar registros existentes")
    print()
    
    try:
        update_database()
    except KeyboardInterrupt:
        print("\n⚠️  Operação cancelada pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        sys.exit(1)
