#!/usr/bin/env python3
"""
Script para atualizar banco MySQL local existente com novas tabelas V1.1
"""
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'poker_academy_api', 'src'))

from main import app, db
from models import Users, Particoes, Classes, StudentGraphs, StudentLeaks
import pymysql

def update_database():
    """Atualiza o banco de dados local com novas tabelas"""
    with app.app_context():
        print("🔧 Conectando ao banco MySQL local...")
        
        try:
            # Testar conexão
            connection = db.engine.connect()
            print("✅ Conexão com MySQL estabelecida!")
            connection.close()
            
            print("📊 Criando/atualizando tabelas...")
            
            # Criar todas as tabelas (só cria se não existir)
            db.create_all()
            
            print("✅ Estrutura do banco atualizada!")
            
            # Verificar se existem as novas tabelas
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"📋 Tabelas disponíveis: {tables}")
            
            if 'student_graphs' in tables:
                print("✅ Tabela student_graphs criada")
            else:
                print("❌ Tabela student_graphs não foi criada")
                
            if 'student_leaks' in tables:
                print("✅ Tabela student_leaks criada")
            else:
                print("❌ Tabela student_leaks não foi criada")
            
            # Verificar se há usuários
            user_count = Users.query.count()
            print(f"👥 Usuários no banco: {user_count}")
            
            if user_count == 0:
                print("⚠️ Nenhum usuário encontrado. Você pode criar usuários pelo painel admin.")
            
            print("🎉 Banco atualizado com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao conectar/atualizar banco: {e}")
            print("💡 Verifique se:")
            print("   - MySQL está rodando")
            print("   - Banco 'poker_academy' existe")
            print("   - Usuário 'root' tem acesso")
            print("   - Senha está correta (vazia por padrão)")

if __name__ == "__main__":
    update_database()
