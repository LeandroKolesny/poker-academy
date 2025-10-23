#!/usr/bin/env python3
"""
Script para atualizar as categorias no banco de dados remoto via conexão direta
"""

import mysql.connector
from mysql.connector import Error

# Configurações do banco de dados
DB_HOST = "142.93.206.128"
DB_USER = "poker_user"
DB_PASSWORD = "Dojo@Sql159357"
DB_NAME = "poker_academy"
DB_PORT = 3306

# SQL para atualizar as categorias
SQL_COMMANDS = [
    "USE poker_academy;",
    
    # Verificar o ENUM atual
    "SELECT COLUMN_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'classes' AND COLUMN_NAME = 'category';",
    
    # Converter aulas existentes com categorias antigas
    "UPDATE classes SET category = 'icm' WHERE category = 'torneos';",
    "UPDATE classes SET category = 'preflop' WHERE category = 'cash';",
    
    # Alterar o ENUM da tabela para as novas categorias
    "ALTER TABLE classes MODIFY COLUMN category ENUM('iniciantes', 'preflop', 'postflop', 'mental', 'icm') NOT NULL DEFAULT 'preflop';",
    
    # Verificar se a alteração foi bem-sucedida
    "SELECT COLUMN_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'classes' AND COLUMN_NAME = 'category';",
    
    # Contar aulas por categoria
    "SELECT category, COUNT(*) as total FROM classes GROUP BY category ORDER BY category;",
]

def update_database():
    """Conecta ao banco de dados e executa os comandos SQL"""
    
    connection = None
    cursor = None
    
    try:
        print("🔌 Conectando ao banco de dados...")
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
        
        if connection.is_connected():
            print("✅ Conectado ao banco de dados!")
            cursor = connection.cursor()
            
            print("\n📝 Executando comandos SQL...\n")
            
            for i, command in enumerate(SQL_COMMANDS, 1):
                if command.strip():
                    print(f"[{i}/{len(SQL_COMMANDS)}] Executando: {command[:60]}...")
                    try:
                        cursor.execute(command)
                        
                        # Se for um SELECT, mostrar resultados
                        if command.strip().upper().startswith('SELECT'):
                            results = cursor.fetchall()
                            if results:
                                print(f"     Resultado:")
                                for row in results:
                                    print(f"       {row}")
                        else:
                            # Para UPDATE/ALTER, mostrar linhas afetadas
                            if cursor.rowcount > 0:
                                print(f"     ✅ {cursor.rowcount} linhas afetadas")
                            else:
                                print(f"     ✅ Comando executado")
                        
                        connection.commit()
                        print()
                    
                    except Error as err:
                        print(f"     ❌ Erro: {err}\n")
                        connection.rollback()
            
            print("\n" + "=" * 60)
            print("✅ Todas as categorias foram atualizadas com sucesso!")
            print("=" * 60)
            
    except Error as err:
        print(f"\n❌ Erro de conexão: {err}")
        return False
    
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("\n✅ Conexão fechada!")
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("Atualizador de Categorias - Poker Academy")
    print("=" * 60)
    print(f"\nServidor: {DB_HOST}:{DB_PORT}")
    print(f"Banco de dados: {DB_NAME}")
    print(f"Usuário: {DB_USER}")
    print("\nCategorias a serem atualizadas:")
    print("  - Iniciante (iniciantes)")
    print("  - Pré-Flop (preflop)")
    print("  - Pós-Flop (postflop)")
    print("  - Mental Games (mental)")
    print("  - ICM (icm)")
    print("\n" + "=" * 60)
    
    input("\nPressione ENTER para continuar...")
    
    success = update_database()
    
    if success:
        print("\n✅ Processo concluído com sucesso!")
    else:
        print("\n❌ Processo falhou!")

