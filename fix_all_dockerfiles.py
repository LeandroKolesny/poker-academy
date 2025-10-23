#!/usr/bin/env python3
"""
Script para corrigir todos os Dockerfiles
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

def fix():
    """Corrige"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Corrigir todos os Dockerfiles com o comando antigo
        dockerfiles_to_fix = [
            "/root/Dojo_Deploy/poker-academy/poker-academy-backend/Dockerfile",
            "/root/Dojo_Deploy/poker-academy/poker-academy-deploy/poker-academy-backend/Dockerfile",
        ]
        
        for dockerfile in dockerfiles_to_fix:
            print(f"📝 Corrigindo {dockerfile}...")
            execute_command(client, f"sed -i 's/mkdir -p uploads\\/videos logs/mkdir -p logs/g' {dockerfile}")
            
            # Verificar
            output, error = execute_command(client, f"grep -n 'mkdir' {dockerfile}")
            print(f"✅ Resultado: {output.strip()}\n")
        
        # Limpar Docker
        print("📝 Limpando Docker...")
        execute_command(client, "docker stop $(docker ps -q) 2>/dev/null || true")
        execute_command(client, "docker rm -f $(docker ps -a -q) 2>/dev/null || true")
        execute_command(client, "docker rmi -f $(docker images -q) 2>/dev/null || true")
        execute_command(client, "docker builder prune -af")
        print("✅ Docker limpo!\n")
        
        # Reconstruir
        print("📝 Reconstruindo...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose build --no-cache 2>&1 | tail -50", timeout=600)
        print(output)
        
        if "error" in output.lower() or "failed" in output.lower():
            print("\n❌ ERRO NO BUILD!")
        else:
            print("\n✅ Build OK!")
        
        # Iniciar
        print("\n📝 Iniciando containers...")
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d")
        print("✅ Comando enviado!\n")
        
        # Aguardar
        print("⏳ Aguardando 180 segundos...")
        time.sleep(180)
        
        # Verificar status
        print("\n📝 Status:")
        output, error = execute_command(client, "docker ps")
        print(output)
        
        # Verificar logs
        print("\n📝 Logs:")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose logs 2>&1 | tail -100")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ PROCESSO CONCLUÍDO!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix()

