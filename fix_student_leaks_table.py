#!/usr/bin/env python3
"""
Script para adicionar a coluna 'improvements' à tabela student_leaks
"""
import paramiko

def fix_student_leaks_table():
    """Adiciona a coluna improvements à tabela student_leaks"""
    
    # Conectar ao servidor
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    print("🔌 Conectando ao servidor...")
    client.connect('142.93.206.128', username='root', password='DojoShh159357')
    print("✅ Conectado!")
    
    # SQL para adicionar a coluna
    sql_commands = [
        "USE poker_academy;",
        "SHOW COLUMNS FROM student_leaks;",
        "ALTER TABLE student_leaks ADD COLUMN improvements TEXT NULL AFTER image_url;",
        "SHOW COLUMNS FROM student_leaks;",
    ]
    
    sql_script = "\n".join(sql_commands)
    
    print("\n📝 Executando comandos SQL...")
    print("="*80)
    
    # Executar via mysql
    command = f"mysql -h mysql -u poker_user -pDojo@Sql159357 -e \"{sql_script}\""
    
    # Usar docker exec para executar dentro do container
    docker_command = f"cd /root/Dojo_Deploy/poker-academy && docker-compose exec -T mysql mysql -u poker_user -pDojo@Sql159357 -e \"{sql_script}\""
    
    stdin, stdout, stderr = client.exec_command(docker_command)
    output = stdout.read().decode('utf-8', errors='replace')
    error = stderr.read().decode('utf-8', errors='replace')
    
    print("OUTPUT:")
    print(output)
    
    if error:
        print("\nERROR:")
        print(error)
    
    print("="*80)
    
    client.close()
    print("\n✅ Comando executado!")

if __name__ == '__main__':
    fix_student_leaks_table()

