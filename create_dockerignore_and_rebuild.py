#!/usr/bin/env python3
"""
Script para criar .dockerignore e reconstruir
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
    """Cria .dockerignore e reconstrói"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Passo 1: Criar .dockerignore
        print("📝 Passo 1: Criando .dockerignore...")
        dockerignore_content = """__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv
.env
.git
.gitignore
.dockerignore
Dockerfile
docker-compose.yml
.DS_Store
*.log
uploads/
"""
        
        # Usar SFTP para criar arquivo
        sftp = client.open_sftp()
        with sftp.file("/root/Dojo_Deploy/poker-academy-backend/.dockerignore", "w") as f:
            f.write(dockerignore_content)
        sftp.close()
        print("✅ .dockerignore criado!\n")
        
        # Passo 2: Limpar Docker
        print("📝 Passo 2: Limpando Docker...")
        execute_command(client, "docker stop $(docker ps -q) 2>/dev/null || true")
        execute_command(client, "docker rm -f $(docker ps -a -q) 2>/dev/null || true")
        execute_command(client, "docker rmi -f $(docker images -q) 2>/dev/null || true")
        execute_command(client, "docker builder prune -af")
        print("✅ Docker limpo!\n")
        
        # Passo 3: Reconstruir
        print("📝 Passo 3: Reconstruindo...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose build --no-cache 2>&1 | tail -50", timeout=600)
        print(output)
        
        if "error" in output.lower() or "failed" in output.lower():
            print("\n❌ ERRO NO BUILD!")
        else:
            print("\n✅ Build OK!")
        
        # Passo 4: Iniciar
        print("\n📝 Passo 4: Iniciando containers...")
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d")
        print("✅ Comando enviado!\n")
        
        # Aguardar
        print("⏳ Aguardando 180 segundos...")
        time.sleep(180)
        
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
        print("✅ PROCESSO CONCLUÍDO!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    rebuild()

