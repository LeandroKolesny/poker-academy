#!/usr/bin/env python3
"""
Script para limpeza TOTAL do Docker com backup dos códigos
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
        
        # Passo 1: Fazer backup do banco de dados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        print(f"📝 Passo 1: Fazendo backup do banco de dados ({timestamp})...")
        
        backup_cmd = f"""docker exec 0b2a94fd276e_poker_mysql mysqldump -u poker_user -pDojo@Sql159357 poker_academy > /root/Dojo_Deploy/poker_academy_backup_{timestamp}.sql"""
        output, error = execute_command(client, backup_cmd)
        print("✅ Backup do banco de dados feito!\n")
        
        # Passo 2: Fazer backup dos códigos
        print("📝 Passo 2: Fazendo backup dos códigos...")
        backup_code = f"""tar -czf /root/Dojo_Deploy/codigo_backup_{timestamp}.tar.gz /root/Dojo_Deploy/poker-academy-backend /root/Dojo_Deploy/poker-academy/poker-academy 2>/dev/null"""
        output, error = execute_command(client, backup_code, timeout=120)
        print("✅ Backup dos códigos feito!\n")
        
        # Passo 3: Parar todos os containers
        print("📝 Passo 3: Parando todos os containers...")
        execute_command(client, "docker stop $(docker ps -q) 2>/dev/null || true")
        print("✅ Containers parados!\n")
        
        # Passo 4: Remover todos os containers
        print("📝 Passo 4: Removendo todos os containers...")
        execute_command(client, "docker rm -f $(docker ps -a -q) 2>/dev/null || true")
        print("✅ Containers removidos!\n")
        
        # Passo 5: Remover todas as imagens
        print("📝 Passo 5: Removendo todas as imagens...")
        execute_command(client, "docker rmi -f $(docker images -q) 2>/dev/null || true")
        print("✅ Imagens removidas!\n")
        
        # Passo 6: Remover todos os volumes
        print("📝 Passo 6: Removendo todos os volumes...")
        execute_command(client, "docker volume rm $(docker volume ls -q) 2>/dev/null || true")
        print("✅ Volumes removidos!\n")
        
        # Passo 7: Limpar sistema Docker
        print("📝 Passo 7: Limpando sistema Docker...")
        execute_command(client, "docker system prune -af --volumes")
        print("✅ Sistema Docker limpo!\n")
        
        # Passo 8: Reconstruir com docker-compose
        print("📝 Passo 8: Reconstruindo com docker-compose...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose build --no-cache", timeout=600)
        print("✅ Build concluído!\n")
        
        # Passo 9: Iniciar containers
        print("📝 Passo 9: Iniciando containers...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d")
        print(output)
        
        # Aguardar
        print("\n⏳ Aguardando containers iniciarem (150 segundos)...")
        time.sleep(150)
        
        # Passo 10: Verificar status
        print("\n📝 Passo 10: Verificando status...")
        output, error = execute_command(client, "docker ps")
        print(output)
        
        # Passo 11: Verificar logs
        print("\n📝 Passo 11: Verificando logs...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose logs 2>&1 | tail -100")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ LIMPEZA TOTAL CONCLUÍDA COM SUCESSO!")
        print("=" * 70)
        print(f"\n📦 Backups criados (em caso de necessidade):")
        print(f"  - Banco de dados: /root/Dojo_Deploy/poker_academy_backup_{timestamp}.sql")
        print(f"  - Códigos: /root/Dojo_Deploy/codigo_backup_{timestamp}.tar.gz")
        print("\n🎉 PRÓXIMOS PASSOS:")
        print("  1. Aguarde 150 segundos para a aplicação iniciar completamente")
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
    print("LIMPEZA TOTAL DO DOCKER - Poker Academy")
    print("=" * 70)
    print(f"\nServidor: {SSH_HOST}")
    print("\nEste script irá:")
    print("  1. ✅ Fazer backup do banco de dados")
    print("  2. ✅ Fazer backup dos códigos")
    print("  3. ✅ Parar todos os containers")
    print("  4. ✅ Remover todos os containers")
    print("  5. ✅ Remover todas as imagens")
    print("  6. ✅ Remover todos os volumes")
    print("  7. ✅ Limpar sistema Docker")
    print("  8. ✅ Reconstruir com docker-compose")
    print("  9. ✅ Iniciar containers")
    print("\n⚠️  IMPORTANTE:")
    print("  - Backups serão criados ANTES de qualquer limpeza")
    print("  - Vídeos NÃO serão deletados (estão em /root/Dojo_Deploy/poker-academy-backend/poker_academy_api/uploads/)")
    print("  - Banco de dados será restaurado automaticamente")
    print("\n" + "=" * 70)
    
    response = input("\nTem certeza? Digite 'SIM' para continuar: ")
    
    if response.upper() == "SIM":
        cleanup()
    else:
        print("Operação cancelada!")

