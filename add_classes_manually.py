#!/usr/bin/env python3
"""
Script para adicionar aulas manualmente
"""

import paramiko
import time

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"
SSH_PORT = 22

def execute_command(client, command, timeout=60):
    """Executa um comando via SSH"""
    stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
    time.sleep(2)
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    return output, error

def add():
    """Adiciona"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Adicionar aulas
        print("📝 Adicionando aulas...")
        sql = """
        INSERT INTO classes (name, description, category, instructor_id, video_url) VALUES
        ('Fundamentos do Poker - Como Jogar', 'Aprenda os fundamentos básicos do poker', 'iniciantes', 1, 'https://www.youtube.com/watch?v=GAoR9ji8D6A'),
        ('Estratégias Pré-Flop', 'Estratégias essenciais para o pré-flop', 'preflop', 1, 'https://www.youtube.com/watch?v=v3QzLjFLzd4'),
        ('Estratégias Pós-Flop', 'Aprenda a jogar após o flop', 'postflop', 1, 'https://www.youtube.com/watch?v=v3QzLjFLzd4'),
        ('Psicologia no Poker', 'Controle emocional e mentalidade', 'mental', 1, 'https://www.youtube.com/watch?v=8wqw2H5U7Qs'),
        ('ICM - Independent Chip Model', 'Cálculos de torneio com ICM', 'icm', 1, 'https://www.youtube.com/watch?v=ZJJ4PZ3eoNs');
        """
        
        cmd = f"docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"{sql}\""
        output, error = execute_command(client, cmd)
        print(output if output else "Aulas adicionadas!")
        print("✅ Aulas adicionadas!\n")
        
        # Verificar aulas
        print("📝 Aulas cadastradas:")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT id, name, category FROM classes ORDER BY id;\"")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ AULAS ADICIONADAS!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    add()

