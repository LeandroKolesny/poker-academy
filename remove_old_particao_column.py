#!/usr/bin/env python3
"""
Script para remover a coluna antiga 'particao' da tabela users
"""

import mysql.connector
import sys
from mysql.connector import Error

def remove_old_particao_column():
    """Remove a coluna antiga particao da tabela users"""
    
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
        
        # 1. Verificar se a coluna particao existe
        print("Verificando se a coluna 'particao' existe...")
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'poker_academy' 
            AND TABLE_NAME = 'users' 
            AND COLUMN_NAME = 'particao'
        """)
        
        column_exists = cursor.fetchone()[0] > 0
        
        if column_exists:
            print("Coluna 'particao' encontrada. Removendo...")
            
            # 2. Verificar se todos os usuários têm particao_id preenchido
            print("Verificando se todos os usuários têm particao_id...")
            cursor.execute("SELECT COUNT(*) FROM users WHERE particao_id IS NULL")
            users_without_particao_id = cursor.fetchone()[0]
            
            if users_without_particao_id > 0:
                print(f"AVISO: {users_without_particao_id} usuários sem particao_id!")
                print("Preenchendo particao_id com partição 'Dojo' (ID=1)...")
                
                cursor.execute("UPDATE users SET particao_id = 1 WHERE particao_id IS NULL")
                connection.commit()
                print("Usuários atualizados!")
            
            # 3. Tornar particao_id obrigatório
            print("Tornando particao_id obrigatório...")
            cursor.execute("ALTER TABLE users MODIFY COLUMN particao_id INT NOT NULL")
            
            # 4. Remover a coluna antiga
            print("Removendo coluna 'particao'...")
            cursor.execute("ALTER TABLE users DROP COLUMN particao")
            
            connection.commit()
            print("Coluna 'particao' removida com sucesso!")
        else:
            print("Coluna 'particao' não existe. Nada a fazer.")
        
        # 5. Verificar estrutura final
        print("\nVerificando estrutura final da tabela users...")
        cursor.execute("""
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'poker_academy' 
            AND TABLE_NAME = 'users' 
            ORDER BY ORDINAL_POSITION
        """)
        
        columns = cursor.fetchall()
        
        print("\nEstrutura da tabela users:")
        print("-" * 70)
        print(f"{'Coluna':<20} {'Tipo':<15} {'Nulo':<8} {'Padrão':<15}")
        print("-" * 70)
        
        for column in columns:
            column_name, data_type, is_nullable, column_default = column
            nullable = "Sim" if is_nullable == "YES" else "Não"
            default = str(column_default) if column_default else "N/A"
            print(f"{column_name:<20} {data_type:<15} {nullable:<8} {default:<15}")
        
        # 6. Verificar dados dos usuários
        print("\nVerificando dados dos usuários:")
        cursor.execute("""
            SELECT u.id, u.name, u.username, u.email, u.type, u.particao_id, p.nome as particao_nome
            FROM users u
            LEFT JOIN particoes p ON u.particao_id = p.id
            ORDER BY u.id
        """)
        users = cursor.fetchall()
        
        print(f"\nUsuários no sistema ({len(users)}):")
        print("-" * 80)
        print(f"{'ID':<4} {'Nome':<20} {'Username':<15} {'Email':<25} {'Tipo':<8} {'Partição':<10}")
        print("-" * 80)
        
        for user in users:
            user_id, name, username, email, user_type, particao_id, particao_nome = user
            print(f"{user_id:<4} {name[:19]:<20} {username[:14]:<15} {email[:24]:<25} {user_type:<8} {particao_nome or 'N/A':<10}")
        
        print("-" * 80)
        print("Estrutura do banco atualizada com sucesso!")
        
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        if connection and connection.is_connected():
            connection.rollback()
        sys.exit(1)
        
    finally:
        # Fechar conexões
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("Conexão com MySQL fechada.")

if __name__ == "__main__":
    print("REMOCAO DA COLUNA ANTIGA 'particao'")
    print("=" * 40)
    print("Este script irá:")
    print("1. Verificar se todos os usuários têm particao_id")
    print("2. Preencher particao_id faltantes com 'Dojo' (ID=1)")
    print("3. Tornar particao_id obrigatório")
    print("4. Remover coluna 'particao' antiga")
    print()
    
    resposta = input("Deseja continuar? (s/N): ").lower().strip()
    if resposta not in ['s', 'sim', 'y', 'yes']:
        print("Operação cancelada.")
        sys.exit(0)
    
    try:
        remove_old_particao_column()
    except KeyboardInterrupt:
        print("\nOperação cancelada pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro inesperado: {e}")
        sys.exit(1)
