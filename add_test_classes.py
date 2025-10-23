#!/usr/bin/env python3
"""
Script para adicionar aulas de teste
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
        
        # Adicionar aulas de teste
        print("📝 Adicionando aulas de teste...")
        sql = """
        INSERT INTO classes (name, description, category, instructor_id) VALUES
        ('Iniciante - Conceitos Básicos', 'Aula para iniciantes', 'iniciantes', 1),
        ('Pré-Flop - Posições', 'Estratégia pré-flop', 'preflop', 1),
        ('Pós-Flop - Continuação', 'Estratégia pós-flop', 'postflop', 1),
        ('Mental Games - Controle Emocional', 'Psicologia do poker', 'mental', 1),
        ('ICM - Cálculos de Torneio', 'Independent Chip Model', 'icm', 1);
        """
        
        cmd = f"docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"{sql}\""
        output, error = execute_command(client, cmd)
        print(output if output else "Aulas adicionadas!")
        print("✅ Aulas adicionadas!\n")
        
        # Verificar aulas
        print("📝 Verificando aulas...")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT id, name, category FROM classes;\"")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ AULAS DE TESTE ADICIONADAS!")
        print("=" * 70)
        print("\n🌐 Acesse: https://cardroomgrinders.com.br")
        print("👤 Usuário: admin")
        print("🔑 Senha: admin123")
        print("\n📝 Teste:")
        print("1. Vá para 'Gestão de Aulas'")
        print("2. Clique em editar uma aula")
        print("3. Verifique se as categorias aparecem no dropdown")
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    add()

