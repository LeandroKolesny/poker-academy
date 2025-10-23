#!/usr/bin/env python3
"""
Script para limpeza TOTAL do Docker - versão rápida
"""

import paramiko
import time
from datetime import datetime

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

def cleanup():
    """Limpeza total"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Passo 1: Fazer backup do banco de dados
        print(f"📝 Passo 1: Fazendo backup do banco de dados ({timestamp})...")
        backup_cmd = f"""docker exec 0b2a94fd276e_poker_mysql mysqldump -u poker_user -pDojo@Sql159357 poker_academy > /root/Dojo_Deploy/poker_academy_backup_{timestamp}.sql"""
        execute_command(client, backup_cmd)
        print("✅ Backup do banco de dados feito!\n")
        
        # Passo 2: Parar todos os containers
        print("📝 Passo 2: Parando todos os containers...")
        execute_command(client, "docker stop $(docker ps -q) 2>/dev/null || true")
        print("✅ Containers parados!\n")
        
        # Passo 3: Remover todos os containers
        print("📝 Passo 3: Removendo todos os containers...")
        execute_command(client, "docker rm -f $(docker ps -a -q) 2>/dev/null || true")
        print("✅ Containers removidos!\n")
        
        # Passo 4: Remover todas as imagens
        print("📝 Passo 4: Removendo todas as imagens...")
        execute_command(client, "docker rmi -f $(docker images -q) 2>/dev/null || true")
        print("✅ Imagens removidas!\n")
        
        # Passo 5: Remover todos os volumes
        print("📝 Passo 5: Removendo todos os volumes...")
        execute_command(client, "docker volume rm $(docker volume ls -q) 2>/dev/null || true")
        print("✅ Volumes removidos!\n")
        
        # Passo 6: Limpar sistema Docker
        print("📝 Passo 6: Limpando sistema Docker...")
        execute_command(client, "docker system prune -af --volumes")
        print("✅ Sistema Docker limpo!\n")
        
        # Passo 7: Reconstruir com docker-compose
        print("📝 Passo 7: Reconstruindo com docker-compose...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose build --no-cache", timeout=600)
        print("✅ Build concluído!\n")
        
        # Passo 8: Iniciar containers
        print("📝 Passo 8: Iniciando containers...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d")
        print(output)
        
        # Aguardar
        print("\n⏳ Aguardando containers iniciarem (150 segundos)...")
        time.sleep(150)
        
        # Passo 9: Verificar status
        print("\n📝 Passo 9: Verificando status...")
        output, error = execute_command(client, "docker ps")
        print(output)
        
        # Passo 10: Verificar logs
        print("\n📝 Passo 10: Verificando logs...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose logs 2>&1 | tail -100")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ LIMPEZA TOTAL CONCLUÍDA COM SUCESSO!")
        print("=" * 70)
        print(f"\n📦 Backup criado:")
        print(f"  - Banco de dados: /root/Dojo_Deploy/poker_academy_backup_{timestamp}.sql")
        print("\n🎉 APLICAÇÃO RECONSTRUÍDA!")
        print("  Acesse https://cardroomgrinders.com.br para testar")
        print("\n" + "=" * 70)
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    cleanup()

