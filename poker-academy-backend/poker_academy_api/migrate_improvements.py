#!/usr/bin/env python3
"""
Script para adicionar a coluna improvements na tabela student_leaks
"""

import sys
import os
sys.path.append('/app')

from src.main import app, db

def add_improvements_column():
    """Adiciona a coluna improvements na tabela student_leaks"""
    try:
        with app.app_context():
            # Verificar se a coluna já existe
            result = db.engine.execute("SHOW COLUMNS FROM student_leaks LIKE 'improvements'")
            if result.fetchone():
                print("✅ Coluna 'improvements' já existe!")
                return True
            
            # Adicionar a coluna
            db.engine.execute("ALTER TABLE student_leaks ADD COLUMN improvements TEXT")
            print("✅ Coluna 'improvements' adicionada com sucesso!")
            return True
            
    except Exception as e:
        print(f"❌ Erro ao adicionar coluna: {e}")
        return False

if __name__ == "__main__":
    success = add_improvements_column()
    sys.exit(0 if success else 1)
