#!/usr/bin/env python3
"""
Script para criar tabela de partições e atualizar estrutura do banco
"""

import mysql.connector
import sys
from mysql.connector import Error

def update_database_structure():
    """Cria tabela particoes e atualiza estrutura"""
    
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
        
        # 1. Verificar se a tabela particoes já existe
        print("Verificando se a tabela 'particoes' já existe...")
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = 'poker_academy' 
            AND TABLE_NAME = 'particoes'
        """)
        
        table_exists = cursor.fetchone()[0] > 0
        
        if not table_exists:
            print("Criando tabela 'particoes'...")
            cursor.execute("""
                CREATE TABLE particoes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL UNIQUE,
                    descricao TEXT,
                    ativa BOOLEAN NOT NULL DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            print("Tabela 'particoes' criada com sucesso!")
        else:
            print("Tabela 'particoes' já existe.")
        
        # 2. Inserir partições padrão
        print("Inserindo partições padrão...")
        particoes_padrao = [
            ('Dojo', 'Partição principal do Dojo Poker'),
            ('Coco', 'Partição de teste Coco')
        ]
        
        for nome, descricao in particoes_padrao:
            cursor.execute("""
                INSERT IGNORE INTO particoes (nome, descricao) 
                VALUES (%s, %s)
            """, (nome, descricao))
        
        connection.commit()
        print("Partições inseridas com sucesso!")
        
        # 3. Verificar estrutura atual da tabela users
        print("Verificando estrutura atual da tabela users...")
        cursor.execute("""
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'poker_academy' 
            AND TABLE_NAME = 'users' 
            AND COLUMN_NAME = 'particao'
        """)
        
        current_column = cursor.fetchone()
        
        if current_column:
            print("Coluna 'particao' atual encontrada:", current_column)
            
            # 4. Criar nova coluna particao_id
            print("Verificando se coluna 'particao_id' já existe...")
            cursor.execute("""
                SELECT COUNT(*) 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = 'poker_academy' 
                AND TABLE_NAME = 'users' 
                AND COLUMN_NAME = 'particao_id'
            """)
            
            particao_id_exists = cursor.fetchone()[0] > 0
            
            if not particao_id_exists:
                print("Adicionando coluna 'particao_id'...")
                cursor.execute("""
                    ALTER TABLE users 
                    ADD COLUMN particao_id INT,
                    ADD FOREIGN KEY (particao_id) REFERENCES particoes(id)
                """)
                print("Coluna 'particao_id' adicionada com sucesso!")
            else:
                print("Coluna 'particao_id' já existe.")
            
            # 5. Migrar dados da coluna particao para particao_id
            print("Migrando dados da coluna 'particao' para 'particao_id'...")
            
            # Buscar ID da partição "Dojo"
            cursor.execute("SELECT id FROM particoes WHERE nome = 'Dojo'")
            dojo_id = cursor.fetchone()
            
            if dojo_id:
                dojo_id = dojo_id[0]
                print(f"ID da partição Dojo: {dojo_id}")
                
                # Atualizar todos os usuários que têm particao = 'Dojo'
                cursor.execute("""
                    UPDATE users 
                    SET particao_id = %s 
                    WHERE particao = 'Dojo' AND particao_id IS NULL
                """, (dojo_id,))
                
                # Atualizar usuários com outras partições ou NULL
                cursor.execute("""
                    UPDATE users 
                    SET particao_id = %s 
                    WHERE (particao IS NULL OR particao = '' OR particao_id IS NULL)
                """, (dojo_id,))
                
                connection.commit()
                print("Dados migrados com sucesso!")
            
            # 6. Remover coluna antiga 'particao' (opcional - comentado por segurança)
            print("AVISO: Coluna 'particao' antiga mantida por segurança.")
            print("Após confirmar que tudo funciona, você pode removê-la manualmente.")
            # cursor.execute("ALTER TABLE users DROP COLUMN particao")
        
        # 7. Verificar resultado final
        print("\nVerificando resultado final...")
        
        # Listar partições
        cursor.execute("SELECT id, nome, descricao, ativa FROM particoes ORDER BY id")
        particoes = cursor.fetchall()
        
        print(f"\nPartições cadastradas ({len(particoes)}):")
        print("-" * 60)
        print(f"{'ID':<4} {'Nome':<15} {'Descrição':<30} {'Ativa':<6}")
        print("-" * 60)
        
        for particao in particoes:
            particao_id, nome, descricao, ativa = particao
            descricao_short = (descricao[:27] + '...') if descricao and len(descricao) > 30 else (descricao or '')
            ativa_str = 'Sim' if ativa else 'Não'
            print(f"{particao_id:<4} {nome:<15} {descricao_short:<30} {ativa_str:<6}")
        
        # Listar usuários com suas partições
        cursor.execute("""
            SELECT u.id, u.name, u.username, u.email, u.type, p.nome as particao_nome
            FROM users u
            LEFT JOIN particoes p ON u.particao_id = p.id
            ORDER BY u.id
        """)
        users = cursor.fetchall()
        
        print(f"\nUsuários com partições ({len(users)}):")
        print("-" * 80)
        print(f"{'ID':<4} {'Nome':<20} {'Username':<15} {'Email':<25} {'Tipo':<8} {'Partição':<10}")
        print("-" * 80)
        
        for user in users:
            user_id, name, username, email, user_type, particao_nome = user
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
    print("ATUALIZACAO DA ESTRUTURA DO BANCO - PARTICOES")
    print("=" * 50)
    print("Este script irá:")
    print("1. Criar tabela 'particoes'")
    print("2. Inserir partições 'Dojo' e 'Coco'")
    print("3. Adicionar coluna 'particao_id' na tabela users")
    print("4. Migrar dados existentes")
    print("5. Manter coluna 'particao' antiga por segurança")
    print()
    
    try:
        update_database_structure()
    except KeyboardInterrupt:
        print("\nOperação cancelada pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro inesperado: {e}")
        sys.exit(1)
