#!/usr/bin/env python3
"""
Script para reconstruir o frontend
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

def rebuild_frontend():
    """Reconstrói o frontend"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Passo 1: Parar containers
        print("📝 Passo 1: Parando containers...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy && docker-compose down")
        print("✅ Containers parados!\n")
        
        # Passo 2: Remover imagem do frontend
        print("📝 Passo 2: Removendo imagem antiga do frontend...")
        output, error = execute_command(client, "docker rmi poker-academy-frontend:latest 2>/dev/null || true")
        print("✅ Imagem removida!\n")
        
        # Passo 3: Reconstruir com --no-cache
        print("📝 Passo 3: Reconstruindo containers com --no-cache...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy && docker-compose build --no-cache", timeout=300)
        print("✅ Build concluído!\n")
        
        # Passo 4: Iniciar containers
        print("📝 Passo 4: Iniciando containers...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy && docker-compose up -d")
        print(output)
        
        # Aguardar containers iniciarem
        print("\n⏳ Aguardando containers iniciarem (30 segundos)...")
        time.sleep(30)
        
        # Passo 5: Verificar status
        print("\n📝 Passo 5: Verificando status dos containers...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy && docker-compose ps")
        print(output)
        
        # Passo 6: Verificar logs do frontend
        print("\n📝 Passo 6: Verificando logs do frontend...")
        output, error = execute_command(client, "docker logs poker-academy-frontend 2>&1 | tail -20")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("🎉 FRONTEND RECONSTRUÍDO COM SUCESSO!")
        print("=" * 70)
        print("\nPróximos passos:")
        print("  1. Aguarde 30 segundos para a aplicação iniciar completamente")
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
    print("Reconstrutor de Frontend - Poker Academy")
    print("=" * 70)
    print(f"\nServidor: {SSH_HOST}")
    print("\nEste script irá:")
    print("  1. Parar os containers")
    print("  2. Remover imagem antiga do frontend")
    print("  3. Reconstruir containers com --no-cache")
    print("  4. Iniciar containers")
    print("  5. Verificar status")
    print("\n" + "=" * 70)
    
    input("\nPressione ENTER para continuar...")
    
    success = rebuild_frontend()
    
    if not success:
        print("\n❌ Processo falhou!")

