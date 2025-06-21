#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar e corrigir a senha do aluno no servidor
"""

import pymysql
import bcrypt
import os
from werkzeug.security import generate_password_hash

# Configurações do banco de dados
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Dojo@Sql159357"
DB_NAME = "poker_academy"

def hash_password(password):
    """Gera hash da senha usando o mesmo método do Flask"""
    return generate_password_hash(password)

def verify_password(password, password_hash):
    """Verifica se a senha confere com o hash"""
    try:
        from werkzeug.security import check_password_hash
        return check_password_hash(password_hash, password)
    except:
        return False

def main():
    print("🔍 VERIFICANDO E CORRIGINDO SENHA DO ALUNO...")
    print("=" * 50)
    
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
        
        # Verificar usuários existentes
        print("📋 USUÁRIOS NO BANCO:")
        cursor.execute("SELECT id, name, email, type FROM users")
        users = cursor.fetchall()
        
        for user in users:
            print(f"   ID: {user[0]} | Nome: {user[1]} | Email: {user[2]} | Tipo: {user[3]}")
        
        print("\n" + "=" * 50)
        
        # Verificar aluno específico
        cursor.execute("SELECT id, name, email, password_hash, type FROM users WHERE email = %s", ("aluno@pokeracademy.com",))
        student = cursor.fetchone()
        
        if not student:
            print("❌ ALUNO NÃO ENCONTRADO!")
            print("🔧 Criando aluno...")
            
            # Criar aluno
            password_hash = hash_password("aluno123")
            cursor.execute("""
                INSERT INTO users (name, email, password_hash, type, register_date) 
                VALUES (%s, %s, %s, %s, NOW())
            """, ("aluno", "aluno@pokeracademy.com", password_hash, "student"))
            
            connection.commit()
            print("✅ ALUNO CRIADO COM SUCESSO!")
            
        else:
            print(f"✅ ALUNO ENCONTRADO:")
            print(f"   ID: {student[0]}")
            print(f"   Nome: {student[1]}")
            print(f"   Email: {student[2]}")
            print(f"   Tipo: {student[4]}")
            print(f"   Hash atual: {student[3][:50]}...")
            
            # Testar senha atual
            current_hash = student[3]
            test_passwords = ["aluno123", "admin123", "123456", "student123"]
            
            print(f"\n🔍 TESTANDO SENHAS POSSÍVEIS:")
            password_works = False
            
            for test_pass in test_passwords:
                if verify_password(test_pass, current_hash):
                    print(f"   ✅ SENHA '{test_pass}' FUNCIONA!")
                    password_works = True
                    break
                else:
                    print(f"   ❌ SENHA '{test_pass}' não funciona")
            
            if not password_works:
                print(f"\n🔧 NENHUMA SENHA TESTADA FUNCIONA. ATUALIZANDO PARA 'aluno123'...")
                
                # Gerar novo hash
                new_hash = hash_password("aluno123")
                
                # Atualizar no banco
                cursor.execute("""
                    UPDATE users 
                    SET password_hash = %s 
                    WHERE email = %s
                """, (new_hash, "aluno@pokeracademy.com"))
                
                connection.commit()
                
                print("✅ SENHA ATUALIZADA COM SUCESSO!")
                print(f"   Novo hash: {new_hash[:50]}...")
                
                # Verificar se funcionou
                if verify_password("aluno123", new_hash):
                    print("✅ VERIFICAÇÃO: Nova senha 'aluno123' funciona!")
                else:
                    print("❌ ERRO: Nova senha não funciona!")
            
        print("\n" + "=" * 50)
        print("📋 CREDENCIAIS FINAIS:")
        print("   Email: aluno@pokeracademy.com")
        print("   Senha: aluno123")
        print("=" * 50)
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ ERRO: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    main()
