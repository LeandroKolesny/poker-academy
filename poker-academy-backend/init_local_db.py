#!/usr/bin/env python3
"""
Script para inicializar banco SQLite local para teste
"""
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'poker_academy_api', 'src'))

from main import app, db
from models import Users, Particoes, Classes, StudentGraphs, StudentLeaks
from werkzeug.security import generate_password_hash
from datetime import datetime

def init_database():
    """Inicializa o banco de dados SQLite local"""
    with app.app_context():
        print("🔧 Criando tabelas...")
        db.create_all()
        
        # Verificar se já existem dados
        if Users.query.first():
            print("✅ Banco já inicializado!")
            return
        
        print("📊 Criando dados iniciais...")
        
        # Criar partição padrão
        particao = Particoes(
            nome="Turma Teste",
            descricao="Turma para testes locais",
            ativa=True
        )
        db.session.add(particao)
        db.session.flush()  # Para obter o ID
        
        # Criar usuário admin
        admin = Users(
            name="Admin Teste",
            email="admin@test.com",
            username="admin",
            password_hash=generate_password_hash("admin123"),
            type="admin",
            particao_id=particao.id,
            first_login=False
        )
        db.session.add(admin)
        
        # Criar usuário aluno
        aluno = Users(
            name="Aluno Teste",
            email="aluno@test.com", 
            username="aluno",
            password_hash=generate_password_hash("aluno123"),
            type="student",
            particao_id=particao.id,
            first_login=False
        )
        db.session.add(aluno)
        
        db.session.commit()
        
        print("✅ Banco inicializado com sucesso!")
        print("👤 Admin: admin@test.com / admin123")
        print("🎓 Aluno: aluno@test.com / aluno123")

if __name__ == "__main__":
    init_database()
