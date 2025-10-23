#!/usr/bin/env python3
"""
Script para executar SQL no servidor via SSH
"""

import paramiko
import time

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"
SSH_PORT = 22

DB_USER = "poker_user"
DB_PASSWORD = "Dojo@Sql159357"
DB_NAME = "poker_academy"

def execute_command(client, command):
    """Executa um comando via SSH"""
    stdin, stdout, stderr = client.exec_command(command)
    time.sleep(2)
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    return output, error

def update_database():
    """Atualiza o banco de dados"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Passo 1: Verificar ENUM atual
        print("📝 Passo 1: Verificando ENUM atual...")
        cmd = f"mysql -h 127.0.0.1 -u {DB_USER} -p{DB_PASSWORD} {DB_NAME} -e \"SELECT COLUMN_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'classes' AND COLUMN_NAME = 'category';\""
        output, error = execute_command(client, cmd)
        print(output)
        
        # Passo 2: Alterar o ENUM
        print("\n📝 Passo 2: Alterando ENUM da tabela classes...")
        cmd = f"mysql -h 127.0.0.1 -u {DB_USER} -p{DB_PASSWORD} {DB_NAME} -e \"ALTER TABLE classes MODIFY COLUMN category ENUM('iniciantes', 'preflop', 'postflop', 'mental', 'icm') NOT NULL DEFAULT 'preflop';\""
        output, error = execute_command(client, cmd)
        if error and "Warning" not in error:
            print(f"❌ Erro: {error}")
        else:
            print("✅ ENUM alterado com sucesso!")
        
        # Passo 3: Verificar novo ENUM
        print("\n📝 Passo 3: Verificando novo ENUM...")
        cmd = f"mysql -h 127.0.0.1 -u {DB_USER} -p{DB_PASSWORD} {DB_NAME} -e \"SELECT COLUMN_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'classes' AND COLUMN_NAME = 'category';\""
        output, error = execute_command(client, cmd)
        print(output)
        
        if "iniciantes" in output and "icm" in output:
            print("✅ Categorias atualizadas com sucesso!")
        else:
            print("❌ Erro ao atualizar categorias!")
            return False
        
        # Passo 4: Contar aulas por categoria
        print("\n📝 Passo 4: Contando aulas por categoria...")
        cmd = f"mysql -h 127.0.0.1 -u {DB_USER} -p{DB_PASSWORD} {DB_NAME} -e \"SELECT category, COUNT(*) as total FROM classes GROUP BY category ORDER BY category;\""
        output, error = execute_command(client, cmd)
        print(output)
        
        # Passo 5: Reconstruir containers
        print("\n📝 Passo 5: Reconstruindo containers Docker...")
        cmd = "cd /root/Dojo_Deploy && docker-compose build --no-cache"
        print("  Executando: docker-compose build --no-cache")
        output, error = execute_command(client, cmd)
        print("  ✅ Build concluído!")
        
        # Passo 6: Reiniciar containers
        print("\n📝 Passo 6: Reiniciando containers...")
        cmd = "cd /root/Dojo_Deploy && docker-compose up -d"
        print("  Executando: docker-compose up -d")
        output, error = execute_command(client, cmd)
        print(output)
        
        # Aguardar containers iniciarem
        print("\n⏳ Aguardando containers iniciarem...")
        time.sleep(10)
        
        # Passo 7: Verificar status
        print("\n📝 Passo 7: Verificando status dos containers...")
        cmd = "cd /root/Dojo_Deploy && docker-compose ps"
        output, error = execute_command(client, cmd)
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("🎉 PROCESSO CONCLUÍDO COM SUCESSO!")
        print("=" * 70)
        print("\nO que foi feito:")
        print("  ✅ Banco de dados atualizado com novas categorias")
        print("  ✅ Containers Docker reconstruídos")
        print("  ✅ Aplicação reiniciada")
        print("\nPróximos passos:")
        print("  1. Aguarde 30 segundos para a aplicação iniciar completamente")
        print("  2. Acesse http://grinders.com.br")
        print("  3. Teste as novas categorias:")
        print("     - Iniciante")
        print("     - Pré-Flop")
        print("     - Pós-Flop")
        print("     - Mental Games")
        print("     - ICM")
        print("  4. Tente editar uma aula existente para verificar se as categorias aparecem")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("Executor de SQL - Poker Academy")
    print("=" * 70)
    print(f"\nServidor: {SSH_HOST}")
    print(f"Banco de dados: {DB_NAME}")
    print("\nEste script irá:")
    print("  1. Conectar ao servidor via SSH")
    print("  2. Atualizar o ENUM da tabela classes")
    print("  3. Reconstruir containers Docker")
    print("  4. Reiniciar a aplicação")
    print("\n" + "=" * 70)
    
    input("\nPressione ENTER para continuar...")
    
    success = update_database()
    
    if not success:
        print("\n❌ Processo falhou!")

