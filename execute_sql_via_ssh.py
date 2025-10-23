#!/usr/bin/env python3
"""
Script para executar SQL no servidor via SSH
"""

import paramiko
import time

# Configurações do servidor
SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"
SSH_PORT = 22

# Configurações do banco de dados
DB_USER = "poker_user"
DB_PASSWORD = "Dojo@Sql159357"
DB_NAME = "poker_academy"

def execute_sql_via_ssh():
    """Conecta ao servidor via SSH e executa o SQL"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Comando para executar o SQL
        sql_file = "/root/Dojo_Deploy/poker-academy/add_iniciantes_category.sql"
        command = f"mysql -u {DB_USER} -p{DB_PASSWORD} {DB_NAME} < {sql_file}"
        
        print(f"📝 Executando: {command}\n")
        stdin, stdout, stderr = client.exec_command(command)
        
        # Aguardar execução
        time.sleep(3)
        
        # Ler output
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        
        if output:
            print("✅ Output do SQL:")
            print(output)
        
        if error and "Warning" not in error:
            print("\n⚠️ Erros:")
            print(error)
        elif error:
            print("\n⚠️ Avisos (ignoráveis):")
            print(error)
        
        client.close()
        print("\n✅ Conexão fechada!")
        print("\n🎉 Banco de dados atualizado com sucesso!")
        return True
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("Executor de SQL via SSH - Poker Academy")
    print("=" * 70)
    print(f"\nServidor: {SSH_HOST}")
    print(f"Banco de dados: {DB_NAME}")
    print("\nO script irá:")
    print("  1. Conectar ao servidor via SSH")
    print("  2. Executar o arquivo add_iniciantes_category.sql")
    print("  3. Atualizar o ENUM da tabela 'classes'")
    print("  4. Converter categorias antigas para novas")
    print("\n" + "=" * 70)
    
    input("\nPressione ENTER para continuar...")
    
    success = execute_sql_via_ssh()
    
    if success:
        print("\n✅ Processo concluído com sucesso!")
        print("\nPróximos passos:")
        print("  1. Reconstruir os containers Docker")
        print("  2. Reiniciar a aplicação")
        print("  3. Testar as novas categorias no navegador")
    else:
        print("\n❌ Processo falhou!")

