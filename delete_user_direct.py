#!/usr/bin/env python3
"""
Script para deletar usuário diretamente do banco de dados
Bypassa completamente o SQLAlchemy e Flask
"""

import pymysql
import sys

def delete_user_direct(user_id):
    """Deleta usuário diretamente do banco de dados"""
    try:
        # Conectar diretamente ao MySQL
        connection = pymysql.connect(
            host='172.18.0.2',
            user='root',
            password='Dojo@Sql159357',
            database='poker_academy',
            charset='utf8mb4',
            autocommit=False
        )
        
        cursor = connection.cursor()
        
        try:
            # Verificar se usuário existe
            cursor.execute("SELECT id, name, email FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            if not user:
                print(f"❌ Usuário {user_id} não encontrado")
                return False
            
            print(f"👤 Usuário encontrado: {user[1]} ({user[2]})")
            
            # Iniciar transação
            cursor.execute("START TRANSACTION")
            print("🔄 Transação iniciada")
            
            # Desabilitar foreign key checks
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            print("🔓 Foreign key checks desabilitados")
            
            # Deletar registros relacionados em ordem
            tables_to_clean = [
                ("user_progress", "user_id"),
                ("student_graphs", "student_id"),
                ("student_leaks", "student_id"),
                ("student_leaks", "uploaded_by"),
                ("favorites", "user_id"),
                ("playlists", "user_id")
            ]
            
            for table, column in tables_to_clean:
                cursor.execute(f"DELETE FROM {table} WHERE {column} = %s", (user_id,))
                deleted_count = cursor.rowcount
                if deleted_count > 0:
                    print(f"🗑️  Deletados {deleted_count} registros de {table}")
            
            # Deletar o usuário
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            print(f"👤 Usuário {user_id} deletado")
            
            # Reabilitar foreign key checks
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            print("🔒 Foreign key checks reabilitados")
            
            # Commit da transação
            cursor.execute("COMMIT")
            print("✅ Transação commitada com sucesso")
            
            print(f"🎉 Usuário {user[1]} ({user[2]}) excluído com sucesso!")
            return True
            
        except Exception as e:
            # Rollback em caso de erro
            cursor.execute("ROLLBACK")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            print(f"❌ Erro durante exclusão: {e}")
            print("🔄 Rollback executado")
            return False
            
        finally:
            cursor.close()
            connection.close()
            print("🔌 Conexão fechada")
            
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("❌ Uso: python delete_user_direct.py <user_id>")
        sys.exit(1)
    
    try:
        user_id = int(sys.argv[1])
        success = delete_user_direct(user_id)
        sys.exit(0 if success else 1)
    except ValueError:
        print("❌ ID do usuário deve ser um número")
        sys.exit(1)
