#!/usr/bin/env python3
"""
Script para limpar e reconstruir tudo
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

def clean_and_rebuild():
    """Limpa e reconstrói"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Passo 1: Parar todos os containers
        print("📝 Passo 1: Parando todos os containers...")
        output, error = execute_command(client, "docker stop $(docker ps -q) 2>/dev/null || true")
        print("✅ Containers parados!\n")
        
        # Passo 2: Remover containers problemáticos
        print("📝 Passo 2: Removendo containers...")
        output, error = execute_command(client, "docker rm -f $(docker ps -a -q) 2>/dev/null || true")
        print("✅ Containers removidos!\n")
        
        # Passo 3: Remover imagens antigas
        print("📝 Passo 3: Removendo imagens antigas...")
        output, error = execute_command(client, "docker rmi -f poker-academy_frontend:latest poker-academy_backend:latest 2>/dev/null || true")
        print("✅ Imagens removidas!\n")
        
        # Passo 4: Limpar volumes
        print("📝 Passo 4: Limpando volumes...")
        output, error = execute_command(client, "docker volume prune -f 2>/dev/null || true")
        print("✅ Volumes limpos!\n")
        
        # Passo 5: Reconstruir com docker-compose
        print("📝 Passo 5: Reconstruindo com docker-compose...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose build --no-cache", timeout=600)
        print("✅ Build concluído!\n")
        
        # Passo 6: Iniciar containers
        print("📝 Passo 6: Iniciando containers...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d")
        print(output)
        
        # Aguardar containers iniciarem
        print("\n⏳ Aguardando containers iniciarem (60 segundos)...")
        time.sleep(60)
        
        # Passo 7: Verificar status
        print("\n📝 Passo 7: Verificando status dos containers...")
        output, error = execute_command(client, "docker ps")
        print(output)
        
        # Passo 8: Verificar logs
        print("\n📝 Passo 8: Verificando logs...")
        output, error = execute_command(client, "docker logs poker_frontend 2>&1 | tail -30")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("🎉 LIMPEZA E RECONSTRUÇÃO CONCLUÍDAS!")
        print("=" * 70)
        print("\nPróximos passos:")
        print("  1. Aguarde 60 segundos para a aplicação iniciar completamente")
        print("  2. Acesse http://cardroomgrinders.com.br")
        print("  3. Faça login com admin/admin123")
        print("  4. Vá para 'Gestão de Aulas'")
        print("  5. Tente editar uma aula existente")
        print("  6. Verifique se as categorias aparecem no dropdown")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("Limpeza e Reconstrução - Poker Academy")
    print("=" * 70)
    print(f"\nServidor: {SSH_HOST}")
    print("\nEste script irá:")
    print("  1. Parar todos os containers")
    print("  2. Remover containers")
    print("  3. Remover imagens antigas")
    print("  4. Limpar volumes")
    print("  5. Reconstruir com docker-compose")
    print("  6. Iniciar containers")
    print("  7. Verificar status")
    print("\n⚠️  AVISO: Isto vai remover TODOS os containers e imagens!")
    print("\n" + "=" * 70)
    
    response = input("\nTem certeza? Digite 'SIM' para continuar: ")
    
    if response.upper() == "SIM":
        success = clean_and_rebuild()
        if not success:
            print("\n❌ Processo falhou!")
    else:
        print("Operação cancelada!")

