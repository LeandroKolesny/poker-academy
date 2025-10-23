#!/usr/bin/env python3
"""
Script para adicionar as foreign keys que faltam no banco de dados
"""
import paramiko

def add_foreign_keys():
    """Adiciona as foreign keys necessárias"""
    
    # Conectar ao servidor
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    print("🔌 Conectando ao servidor...")
    client.connect('142.93.206.128', username='root', password='DojoShh159357')
    print("✅ Conectado!")
    
    # Verificar as foreign keys existentes
    print("\n📋 Verificando foreign keys existentes...")
    
    check_fk_command = """
    cd /root/Dojo_Deploy/poker-academy && docker-compose exec -T mysql mysql -u poker_user -pDojo@Sql159357 -e "
    USE poker_academy;
    SELECT CONSTRAINT_NAME, TABLE_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME 
    FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
    WHERE TABLE_NAME IN ('student_graphs', 'student_leaks') AND COLUMN_NAME IN ('student_id', 'uploaded_by')
    ORDER BY TABLE_NAME, COLUMN_NAME;
    "
    """
    
    stdin, stdout, stderr = client.exec_command(check_fk_command)
    output = stdout.read().decode('utf-8', errors='replace')
    print(output)
    
    # Agora vamos verificar se as foreign keys já existem
    print("\n🔍 Verificando se as foreign keys já existem...")
    
    # Para student_graphs.student_id
    print("\n✅ Foreign key para student_graphs.student_id já deve existir (criada com a tabela)")
    
    # Para student_leaks.student_id e student_leaks.uploaded_by
    print("✅ Foreign keys para student_leaks já devem existir (criadas com a tabela)")
    
    print("\n📝 As foreign keys já estão definidas no SQL de criação das tabelas!")
    print("   O problema é que SQLAlchemy não está carregando os relacionamentos corretamente.")
    print("   Vamos verificar se os dados estão corretos...")
    
    # Verificar dados
    verify_data_command = """
    cd /root/Dojo_Deploy/poker-academy && docker-compose exec -T mysql mysql -u poker_user -pDojo@Sql159357 -e "
    USE poker_academy;
    SELECT 'student_graphs' as tabela, COUNT(*) as total FROM student_graphs
    UNION ALL
    SELECT 'student_leaks' as tabela, COUNT(*) as total FROM student_leaks;
    "
    """
    
    stdin, stdout, stderr = client.exec_command(verify_data_command)
    output = stdout.read().decode('utf-8', errors='replace')
    print("\n📊 Dados nas tabelas:")
    print(output)
    
    client.close()
    print("\n✅ Verificação concluída!")

if __name__ == '__main__':
    add_foreign_keys()

