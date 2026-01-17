#!/usr/bin/env python3
"""
Script para criar a tabela password_reset_tokens
"""
import os
import sys

# Adicionar o diretorio src ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import app, db
from src.password_reset_model import PasswordResetToken

def create_table():
    """Cria a tabela password_reset_tokens"""
    with app.app_context():
        print("[INFO] Conectando ao banco de dados...")

        try:
            # Testar conexao
            connection = db.engine.connect()
            print("[OK] Conexao estabelecida!")
            connection.close()

            print("[INFO] Criando tabela password_reset_tokens...")

            # Criar a tabela especifica
            PasswordResetToken.__table__.create(db.engine, checkfirst=True)

            # Verificar se a tabela foi criada
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()

            if 'password_reset_tokens' in tables:
                print("[OK] Tabela password_reset_tokens criada com sucesso!")
            else:
                print("[ERRO] Tabela nao foi criada")

            print(f"[INFO] Tabelas disponiveis: {tables}")
            print("[OK] Processo concluido!")

        except Exception as e:
            print(f"[ERRO] {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    create_table()
