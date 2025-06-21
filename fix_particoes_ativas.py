#!/usr/bin/env python3
"""
Script para ativar as partições no banco de dados
"""

import mysql.connector
import sys
from mysql.connector import Error

def fix_particoes():
    """Ativa as partições no banco"""
    
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
        
        # Ativar todas as partições
        print("Ativando partições...")
        cursor.execute("UPDATE particoes SET ativa = TRUE")
        connection.commit()
        
        # Verificar resultado
        cursor.execute("SELECT id, nome, descricao, ativa FROM particoes ORDER BY id")
        particoes = cursor.fetchall()
        
        print(f"\nPartições ativas ({len(particoes)}):")
        print("-" * 60)
        print(f"{'ID':<4} {'Nome':<15} {'Descrição':<30} {'Ativa':<6}")
        print("-" * 60)
        
        for particao in particoes:
            particao_id, nome, descricao, ativa = particao
            descricao_short = (descricao[:27] + '...') if descricao and len(descricao) > 30 else (descricao or '')
            ativa_str = 'Sim' if ativa else 'Não'
            print(f"{particao_id:<4} {nome:<15} {descricao_short:<30} {ativa_str:<6}")
        
        print("-" * 60)
        print("Partições ativadas com sucesso!")
        
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
    print("ATIVANDO PARTICOES")
    print("=" * 30)
    
    try:
        fix_particoes()
    except KeyboardInterrupt:
        print("\nOperação cancelada pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro inesperado: {e}")
        sys.exit(1)
