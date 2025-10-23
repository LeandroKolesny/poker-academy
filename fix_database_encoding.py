#!/usr/bin/env python3
"""
Script para corrigir encoding dos dados no banco de dados
"""

import paramiko
import time

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"
SSH_PORT = 22

def execute_command(client, command, timeout=120):
    """Executa um comando via SSH"""
    print(f"\n📝 Executando: {command}")
    stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
    time.sleep(1)

    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')

    if output:
        print(output)

    return output, error

def fix_encoding():
    """Corrige encoding dos dados"""

    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")

        # Corrigir dados com encoding errado
        print("📝 Corrigindo dados com encoding errado...")

        # Estratégias Pré-Flop
        execute_command(client, """docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "UPDATE classes SET name = 'Estratégias Pré-Flop' WHERE id = 2;" """)

        # Estratégias Pós-Flop
        execute_command(client, """docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "UPDATE classes SET name = 'Estratégias Pós-Flop' WHERE id = 3;" """)

        # Corrigir descriptions também
        execute_command(client, """docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "UPDATE classes SET description = 'Estratégias essenciais para o pré-flop' WHERE id = 2;" """)

        execute_command(client, """docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "UPDATE classes SET description = 'Aprenda a jogar após o flop' WHERE id = 3;" """)

        execute_command(client, """docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "UPDATE classes SET description = 'Aprenda os fundamentos básicos do poker' WHERE id = 1;" """)

        execute_command(client, """docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "UPDATE classes SET description = 'Cálculos de torneio com ICM' WHERE id = 5;" """)

        # Verificar dados corrigidos
        print("\n📝 Verificando dados corrigidos:")
        output, _ = execute_command(client, """docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "SELECT id, name FROM classes;" """)
        print(output)

        print("\n✅ DADOS CORRIGIDOS COM SUCESSO!")

        client.close()

    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_encoding()