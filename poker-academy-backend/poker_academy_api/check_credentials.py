#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar credenciais no banco MySQL
"""

import pymysql
from werkzeug.security import check_password_hash

def check_database_credentials():
    """Verificar credenciais no banco"""
    print("🔍 VERIFICANDO CREDENCIAIS NO BANCO MYSQL")
    print("=" * 60)
    
    try:
        # Conectar ao banco
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',  # Senha do MySQL (geralmente vazia no XAMPP)
            database='poker_academy',
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # Buscar todos os usuários
        cursor.execute("SELECT id, name, email, password_hash, type FROM users ORDER BY id")
        users = cursor.fetchall()
        
        if users:
            print(f"📋 USUÁRIOS ENCONTRADOS ({len(users)}):")
            print("-" * 60)
            for user in users:
                user_id, name, email, password_hash, user_type = user
                print(f"   ID: {user_id}")
                print(f"   Nome: {name}")
                print(f"   Email: {email}")
                print(f"   Tipo: {user_type}")
                print(f"   Hash: {password_hash[:50]}...")
                print("-" * 60)
        else:
            print("❌ NENHUM USUÁRIO ENCONTRADO!")
        
        # Testar senhas específicas
        print(f"\n🔐 TESTANDO SENHAS PARA USUÁRIOS:")
        print("-" * 60)
        
        test_passwords = ['student', 'admin123', 'password', '123456', 'admin']
        
        for user in users:
            user_id, name, email, password_hash, user_type = user
            print(f"\n👤 {name} ({email}):")
            
            for test_password in test_passwords:
                try:
                    if check_password_hash(password_hash, test_password):
                        print(f"   ✅ SENHA CORRETA: '{test_password}'")
                        break
                except Exception as e:
                    continue
            else:
                print(f"   ❌ Nenhuma senha testada funcionou")
        
        cursor.close()
        connection.close()
        
        print(f"\n🎯 CREDENCIAIS VÁLIDAS ENCONTRADAS:")
        print("=" * 60)
        
        # Reconectar para testar login específico
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='poker_academy',
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # Buscar usuário student@pokeracademy.com
        cursor.execute("SELECT id, name, email, password_hash, type FROM users WHERE email = %s", 
                      ('student@pokeracademy.com',))
        student = cursor.fetchone()
        
        if student:
            user_id, name, email, password_hash, user_type = student
            print(f"📧 USUÁRIO: {email}")
            print(f"🔐 TESTANDO SENHAS COMUNS:")
            
            common_passwords = ['student', 'password', '123456', 'admin', 'test', 'student123']
            
            for pwd in common_passwords:
                if check_password_hash(password_hash, pwd):
                    print(f"   ✅ SENHA CORRETA: '{pwd}'")
                    print(f"   📋 USE ESTAS CREDENCIAIS:")
                    print(f"      Email: {email}")
                    print(f"      Senha: {pwd}")
                    break
            else:
                print("   ❌ Nenhuma senha comum funcionou")
                print("   🔧 Vou resetar a senha para 'student'...")
                
                # Resetar senha
                from werkzeug.security import generate_password_hash
                new_hash = generate_password_hash('student')
                cursor.execute("UPDATE users SET password_hash = %s WHERE id = %s", 
                              (new_hash, user_id))
                connection.commit()
                print("   ✅ Senha resetada para 'student'!")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ ERRO AO CONECTAR COM O BANCO: {e}")
        print("\n🔧 POSSÍVEIS SOLUÇÕES:")
        print("1. Verifique se o XAMPP está rodando")
        print("2. Verifique se o MySQL está ativo")
        print("3. Verifique se o banco 'poker_academy' existe")

if __name__ == "__main__":
    check_database_credentials()
