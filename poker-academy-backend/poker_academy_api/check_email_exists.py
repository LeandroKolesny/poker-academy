#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar se um email específico existe no banco
"""

import pymysql
import sys

# Configurações do banco de dados
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""  # Senha vazia conforme .env
DB_NAME = "poker_academy"

def check_email_exists(email):
    print(f"🔍 VERIFICANDO EMAIL: {email}")
    print("=" * 60)
    
    try:
        # Conectar ao banco
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # Buscar email exato
        print("1. BUSCA EXATA:")
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        exact_match = cursor.fetchall()
        
        if exact_match:
            print(f"   ✅ ENCONTRADO: {len(exact_match)} registro(s)")
            for user in exact_match:
                print(f"   ID: {user[0]} | Nome: {user[1]} | Email: {user[3]} | Tipo: {user[5]}")
        else:
            print("   ❌ NÃO ENCONTRADO")
        
        # Buscar email case-insensitive
        print("\n2. BUSCA CASE-INSENSITIVE:")
        cursor.execute("SELECT * FROM users WHERE LOWER(email) = LOWER(%s)", (email,))
        case_insensitive = cursor.fetchall()
        
        if case_insensitive:
            print(f"   ✅ ENCONTRADO: {len(case_insensitive)} registro(s)")
            for user in case_insensitive:
                print(f"   ID: {user[0]} | Nome: {user[1]} | Email: {user[3]} | Tipo: {user[5]}")
        else:
            print("   ❌ NÃO ENCONTRADO")
        
        # Buscar emails similares
        print("\n3. BUSCA SIMILAR (LIKE):")
        cursor.execute("SELECT * FROM users WHERE email LIKE %s", (f"%{email.split('@')[0]}%",))
        similar = cursor.fetchall()
        
        if similar:
            print(f"   ✅ ENCONTRADO: {len(similar)} registro(s) similares")
            for user in similar:
                print(f"   ID: {user[0]} | Nome: {user[1]} | Email: {user[3]} | Tipo: {user[5]}")
        else:
            print("   ❌ NÃO ENCONTRADO")
        
        # Mostrar todos os emails
        print("\n4. TODOS OS EMAILS NO BANCO:")
        cursor.execute("SELECT id, name, email, type FROM users ORDER BY id")
        all_users = cursor.fetchall()
        
        for user in all_users:
            print(f"   ID: {user[0]} | Nome: {user[1]} | Email: {user[2]} | Tipo: {user[3]}")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ ERRO: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    email_to_check = "lekolesny@hotmail.com"
    if len(sys.argv) > 1:
        email_to_check = sys.argv[1]
    
    check_email_exists(email_to_check)
