#!/usr/bin/env python3
"""
Script para verificar e corrigir problema de timezone no MySQL
"""

import pymysql
from datetime import datetime, date

# Configurações do banco
DB_USERNAME = "root"
DB_PASSWORD = "Dojo@Sql159357"
DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "poker_academy"

def check_and_fix_timezone():
    try:
        print("🔍 Conectando ao MySQL...")
        # Conectar ao banco
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        print("📋 Verificando configurações de timezone...")
        
        # Verificar timezone atual
        cursor.execute("SELECT @@global.time_zone, @@session.time_zone, NOW(), UTC_TIMESTAMP();")
        result = cursor.fetchone()
        print(f"Global timezone: {result[0]}")
        print(f"Session timezone: {result[1]}")
        print(f"NOW(): {result[2]}")
        print(f"UTC_TIMESTAMP(): {result[3]}")
        
        print("\n🔍 Verificando dados da tabela classes...")
        
        # Verificar algumas aulas para ver o problema
        cursor.execute("SELECT id, name, date FROM classes ORDER BY id DESC LIMIT 5;")
        classes = cursor.fetchall()
        
        print("📋 Últimas 5 aulas:")
        for cls in classes:
            print(f"ID: {cls[0]}, Nome: {cls[1]}, Data: {cls[2]}")
        
        print("\n🔧 Testando conversão de data...")
        
        # Testar conversão de data
        test_date_str = "2025-06-17"  # Data que você colocou
        test_date_obj = datetime.strptime(test_date_str, "%Y-%m-%d").date()
        
        print(f"String original: {test_date_str}")
        print(f"Objeto date Python: {test_date_obj}")
        
        # Inserir uma aula de teste para ver o que acontece
        print("\n🧪 Inserindo aula de teste...")
        
        cursor.execute("""
            INSERT INTO classes (name, instructor, date, category, video_type, video_path, priority, views)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            "TESTE TIMEZONE",
            "leandro", 
            test_date_obj,
            "preflop",
            "local",
            "teste.mp4",
            5,
            0
        ))
        
        # Buscar a aula que acabamos de inserir
        cursor.execute("SELECT id, name, date FROM classes WHERE name = 'TESTE TIMEZONE' ORDER BY id DESC LIMIT 1;")
        test_result = cursor.fetchone()
        
        if test_result:
            print(f"✅ Aula inserida - ID: {test_result[0]}, Data salva: {test_result[2]}")
            
            # Comparar as datas
            if str(test_result[2]) == test_date_str:
                print("✅ Data está correta!")
            else:
                print(f"❌ PROBLEMA: Data esperada {test_date_str}, mas salva como {test_result[2]}")
                
                # Tentar corrigir definindo timezone da sessão
                print("🔧 Tentando corrigir timezone da sessão...")
                cursor.execute("SET time_zone = '+00:00';")
                
                # Inserir outra aula de teste
                cursor.execute("""
                    INSERT INTO classes (name, instructor, date, category, video_type, video_path, priority, views)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    "TESTE TIMEZONE 2",
                    "leandro", 
                    test_date_obj,
                    "preflop",
                    "local",
                    "teste2.mp4",
                    5,
                    0
                ))
                
                cursor.execute("SELECT id, name, date FROM classes WHERE name = 'TESTE TIMEZONE 2' ORDER BY id DESC LIMIT 1;")
                test_result2 = cursor.fetchone()
                
                if test_result2:
                    print(f"🔧 Teste com timezone UTC - Data salva: {test_result2[2]}")
        
        # Limpar aulas de teste
        print("\n🧹 Limpando aulas de teste...")
        cursor.execute("DELETE FROM classes WHERE name LIKE 'TESTE TIMEZONE%';")
        
        connection.commit()
        connection.close()
        
        print("✅ Verificação concluída!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    check_and_fix_timezone()
