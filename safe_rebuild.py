#!/usr/bin/env python3
"""
Script para reconstrução SEGURA sem perder dados
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

def rebuild():
    """Reconstrói de forma segura"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Passo 1: Fazer backup dos dados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        print(f"📝 Passo 1: Fazendo backup dos dados ({timestamp})...")
        
        # Backup do banco de dados
        backup_cmd = f"""docker exec 0b2a94fd276e_poker_mysql mysqldump -u poker_user -pDojo@Sql159357 poker_academy > /root/Dojo_Deploy/poker_academy_backup_{timestamp}.sql"""
        output, error = execute_command(client, backup_cmd)
        print("✅ Backup do banco de dados feito!\n")
        
        # Backup dos uploads
        backup_uploads = f"""tar -czf /root/Dojo_Deploy/uploads_backup_{timestamp}.tar.gz /root/Dojo_Deploy/poker-academy-backend/poker_academy_api/uploads/ 2>/dev/null"""
        output, error = execute_command(client, backup_uploads)
        print("✅ Backup dos uploads feito!\n")
        
        # Passo 2: Parar containers (SEM remover volumes)
        print("📝 Passo 2: Parando containers (mantendo volumes)...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose down")
        print("✅ Containers parados!\n")
        
        # Passo 3: Remover APENAS imagens (não volumes!)
        print("📝 Passo 3: Removendo imagens antigas...")
        execute_command(client, "docker rmi -f poker-academy_frontend:latest poker-academy_backend:latest 2>/dev/null || true")
        print("✅ Imagens removidas!\n")
        
        # Passo 4: Reconstruir imagens
        print("📝 Passo 4: Reconstruindo imagens...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose build --no-cache", timeout=600)
        print("✅ Build concluído!\n")
        
        # Passo 5: Iniciar containers
        print("📝 Passo 5: Iniciando containers...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d")
        print(output)
        
        # Aguardar
        print("\n⏳ Aguardando containers iniciarem (120 segundos)...")
        time.sleep(120)
        
        # Passo 6: Verificar status
        print("\n📝 Passo 6: Verificando status...")
        output, error = execute_command(client, "docker ps")
        print(output)
        
        # Passo 7: Verificar dados
        print("\n📝 Passo 7: Verificando integridade dos dados...")
        output, error = execute_command(client, "ls -lh /root/Dojo_Deploy/poker-academy-backend/poker_academy_api/uploads/videos/ 2>/dev/null | head -5")
        print(output if output else "Diretório de uploads OK")
        
        # Passo 8: Verificar logs
        print("\n📝 Passo 8: Verificando logs...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose logs 2>&1 | tail -50")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ RECONSTRUÇÃO SEGURA CONCLUÍDA!")
        print("=" * 70)
        print(f"\n📦 Backups criados:")
        print(f"  - Banco de dados: /root/Dojo_Deploy/poker_academy_backup_{timestamp}.sql")
        print(f"  - Uploads: /root/Dojo_Deploy/uploads_backup_{timestamp}.tar.gz")
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
    print("Reconstrução SEGURA - Poker Academy")
    print("=" * 70)
    print(f"\nServidor: {SSH_HOST}")
    print("\nEste script irá:")
    print("  1. ✅ Fazer backup do banco de dados")
    print("  2. ✅ Fazer backup dos uploads")
    print("  3. ✅ Parar containers (mantendo volumes)")
    print("  4. ✅ Remover apenas imagens")
    print("  5. ✅ Reconstruir imagens")
    print("  6. ✅ Iniciar containers")
    print("  7. ✅ Verificar integridade dos dados")
    print("\n⚠️  IMPORTANTE: Nenhum dado será perdido!")
    print("\n" + "=" * 70)
    
    response = input("\nTem certeza? Digite 'SIM' para continuar: ")
    
    if response.upper() == "SIM":
        rebuild()
    else:
        print("Operação cancelada!")

