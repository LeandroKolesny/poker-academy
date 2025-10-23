#!/usr/bin/env python3
"""
Script para verificar e corrigir arquivos no servidor
"""

import paramiko
import time

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"
SSH_PORT = 22

def execute_command(client, command):
    """Executa um comando via SSH"""
    stdin, stdout, stderr = client.exec_command(command)
    time.sleep(1)
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    return output, error

def check_and_fix():
    """Verifica e corrige"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Arquivo 1: ClassManagement.js
        print("=" * 70)
        print("📋 VERIFICANDO ClassManagement.js")
        print("=" * 70)
        
        file_path = "/root/Dojo_Deploy/poker-academy/poker-academy/src/components/admin/ClassManagement.js"
        
        # Procurar por opções de categoria
        output, error = execute_command(client, f"grep -n 'option value=' {file_path} | grep -E '(preflop|postflop|mental|torneos|cash|iniciantes|icm)'")
        print("\n📋 Opções de categoria encontradas:")
        print(output)
        
        # Corrigir: remover torneos e cash
        print("\n📝 Removendo categorias antigas (torneos, cash)...")
        execute_command(client, f"sed -i '/<option value=\"torneos\"/d' {file_path}")
        execute_command(client, f"sed -i '/<option value=\"cash\"/d' {file_path}")
        print("✅ Removidas!\n")
        
        # Adicionar iniciantes se não existir
        print("📝 Adicionando categoria 'Iniciante'...")
        output, error = execute_command(client, f"grep -c 'iniciantes' {file_path}")
        if output.strip() == "0":
            execute_command(client, f"""sed -i '/<option value=\"preflop\">Pré-Flop<\\/option>/i\\
  <option value=\"iniciantes\">Iniciante</option>' {file_path}""")
            print("✅ Adicionada!\n")
        else:
            print("✅ Já existe!\n")
        
        # Adicionar ICM se não existir
        print("📝 Adicionando categoria 'ICM'...")
        output, error = execute_command(client, f"grep -c 'icm' {file_path}")
        if output.strip() == "0":
            execute_command(client, f"""sed -i '/<option value=\"mental\">Mental Games<\\/option>/a\\
  <option value=\"icm\">ICM</option>' {file_path}""")
            print("✅ Adicionada!\n")
        else:
            print("✅ Já existe!\n")
        
        # Verificar resultado
        print("📋 Verificando resultado final:")
        output, error = execute_command(client, f"grep -n 'option value=' {file_path} | grep -E '(preflop|postflop|mental|iniciantes|icm)'")
        print(output)
        
        # Arquivo 2: Catalog.js
        print("\n" + "=" * 70)
        print("📋 VERIFICANDO Catalog.js")
        print("=" * 70)
        
        file_path = "/root/Dojo_Deploy/poker-academy/poker-academy/src/components/student/Catalog.js"
        
        # Procurar por array de categorias
        output, error = execute_command(client, f"grep -n \"const categories\" {file_path}")
        print("\n📋 Definição de categorias:")
        print(output)
        
        # Corrigir array de categorias
        print("\n📝 Corrigindo array de categorias...")
        execute_command(client, f"""sed -i "s/const categories = \\[.*\\]/const categories = ['all', 'iniciantes', 'preflop', 'postflop', 'mental', 'icm'];/" {file_path}""")
        print("✅ Corrigido!\n")
        
        # Verificar resultado
        output, error = execute_command(client, f"grep -n \"const categories\" {file_path}")
        print("📋 Resultado:")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ VERIFICAÇÃO E CORREÇÃO CONCLUÍDAS!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_and_fix()

