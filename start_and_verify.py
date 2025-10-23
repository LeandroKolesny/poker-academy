#!/usr/bin/env python3
"""
Script para iniciar containers e verificar status
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

def start():
    """Inicia containers"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Iniciar em background
        print("📝 Iniciando containers em background...")
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && nohup docker-compose up -d > /tmp/docker_start.log 2>&1 &")
        print("✅ Comando enviado!\n")
        
        # Aguardar
        print("⏳ Aguardando containers iniciarem (180 segundos)...")
        time.sleep(180)
        
        # Verificar status
        print("\n📝 Verificando status dos containers...")
        output, error = execute_command(client, "docker ps")
        print(output)
        
        # Verificar logs
        print("\n📝 Verificando logs...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose logs 2>&1 | tail -100")
        print(output)
        
        # Verificar se backend está respondendo
        print("\n📝 Testando conexão com backend...")
        output, error = execute_command(client, "curl -s http://localhost:5000/health 2>&1 || echo 'Backend ainda não respondendo'")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ VERIFICAÇÃO CONCLUÍDA!")
        print("=" * 70)
        print("\n🎉 PRÓXIMOS PASSOS:")
        print("  1. Acesse https://cardroomgrinders.com.br")
        print("  2. Faça login com admin/admin123")
        print("  3. Vá para 'Gestão de Aulas'")
        print("  4. Tente editar uma aula existente")
        print("  5. Verifique se as categorias aparecem:")
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
    start()

