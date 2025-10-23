#!/usr/bin/env python3
"""
Script para reconstruir e testar
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
        
        # Passo 1: Parar containers
        print("📝 Passo 1: Parando containers...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose down")
        print("✅ Containers parados!\n")
        
        # Passo 2: Remover imagens
        print("📝 Passo 2: Removendo imagens antigas...")
        output, error = execute_command(client, "docker rmi -f poker-academy_frontend:latest poker-academy_backend:latest 2>/dev/null || true")
        print("✅ Imagens removidas!\n")
        
        # Passo 3: Reconstruir
        print("📝 Passo 3: Reconstruindo com docker-compose...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose build --no-cache", timeout=600)
        print("✅ Build concluído!\n")
        
        # Passo 4: Iniciar
        print("📝 Passo 4: Iniciando containers...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d")
        print(output)
        
        # Aguardar
        print("\n⏳ Aguardando containers iniciarem (120 segundos)...")
        time.sleep(120)
        
        # Passo 5: Verificar status
        print("\n📝 Passo 5: Verificando status...")
        output, error = execute_command(client, "docker ps")
        print(output)
        
        # Passo 6: Verificar logs
        print("\n📝 Passo 6: Verificando logs...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose logs 2>&1 | tail -100")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ RECONSTRUÇÃO CONCLUÍDA!")
        print("=" * 70)
        print("\n🎉 PRÓXIMOS PASSOS:")
        print("  1. Aguarde 120 segundos para a aplicação iniciar completamente")
        print("  2. Acesse https://cardroomgrinders.com.br")
        print("  3. Faça login com admin/admin123")
        print("  4. Vá para 'Gestão de Aulas'")
        print("  5. Tente editar uma aula existente")
        print("  6. Verifique se as categorias aparecem no dropdown:")
        print("     ✓ Iniciante")
        print("     ✓ Pré-Flop")
        print("     ✓ Pós-Flop")
        print("     ✓ Mental Games")
        print("     ✓ ICM")
        print("\n" + "=" * 70)
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=" * 70)
    print("Reconstrução e Teste Final")
    print("=" * 70)
    print(f"\nServidor: {SSH_HOST}")
    print("\nEste script irá:")
    print("  1. Parar containers")
    print("  2. Remover imagens antigas")
    print("  3. Reconstruir com docker-compose")
    print("  4. Iniciar containers")
    print("  5. Verificar status")
    print("\n" + "=" * 70)
    
    input("\nPressione ENTER para continuar...")
    
    rebuild()

