#!/usr/bin/env python3
"""
Script para reconstruir após corrigir Dockerfile
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

def rebuild():
    """Reconstrói"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Passo 1: Pull do GitHub
        print("📝 Passo 1: Fazendo pull do GitHub...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && git pull origin main")
        print(output)
        
        # Passo 2: Parar containers
        print("\n📝 Passo 2: Parando containers...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose down")
        print("✅ Containers parados!\n")
        
        # Passo 3: Remover imagens
        print("📝 Passo 3: Removendo imagens antigas...")
        output, error = execute_command(client, "docker rmi -f poker-academy_frontend:latest poker-academy_backend:latest 2>/dev/null || true")
        print("✅ Imagens removidas!\n")
        
        # Passo 4: Reconstruir
        print("📝 Passo 4: Reconstruindo com docker-compose...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose build --no-cache", timeout=600)
        print("✅ Build concluído!\n")
        
        # Passo 5: Iniciar
        print("📝 Passo 5: Iniciando containers...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d")
        print(output)
        
        # Aguardar
        print("\n⏳ Aguardando containers iniciarem (60 segundos)...")
        time.sleep(60)
        
        # Passo 6: Verificar status
        print("\n📝 Passo 6: Verificando status...")
        output, error = execute_command(client, "docker ps")
        print(output)
        
        # Passo 7: Verificar logs
        print("\n📝 Passo 7: Verificando logs...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose logs 2>&1 | tail -50")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("🎉 RECONSTRUÇÃO CONCLUÍDA!")
        print("=" * 70)
        print("\nPróximos passos:")
        print("  1. Aguarde 60 segundos para a aplicação iniciar completamente")
        print("  2. Acesse http://cardroomgrinders.com.br")
        print("  3. Faça login com admin/admin123")
        print("  4. Vá para 'Gestão de Aulas'")
        print("  5. Tente editar uma aula existente")
        print("  6. Verifique se as categorias aparecem no dropdown:")
        print("     - Iniciante")
        print("     - Pré-Flop")
        print("     - Pós-Flop")
        print("     - Mental Games")
        print("     - ICM")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("Reconstrução após Corrigir Dockerfile")
    print("=" * 70)
    print(f"\nServidor: {SSH_HOST}")
    print("\nEste script irá:")
    print("  1. Fazer pull do GitHub")
    print("  2. Parar containers")
    print("  3. Remover imagens antigas")
    print("  4. Reconstruir com docker-compose")
    print("  5. Iniciar containers")
    print("  6. Verificar status")
    print("\n" + "=" * 70)
    
    input("\nPressione ENTER para continuar...")
    
    success = rebuild()
    
    if not success:
        print("\n❌ Processo falhou!")

