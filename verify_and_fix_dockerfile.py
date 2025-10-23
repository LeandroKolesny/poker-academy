#!/usr/bin/env python3
"""
Script para verificar e corrigir Dockerfile
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
    """Verifica e corrige"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar Dockerfile atual
        print("📝 Verificando Dockerfile atual...")
        output, error = execute_command(client, "cat /root/Dojo_Deploy/poker-academy-backend/Dockerfile | grep -A 5 'mkdir'")
        print(output)
        
        # Remover Dockerfile antigo
        print("\n📝 Removendo Dockerfile antigo...")
        execute_command(client, "rm -f /root/Dojo_Deploy/poker-academy-backend/Dockerfile")
        print("✅ Removido!\n")
        
        # Criar novo Dockerfile com sed (mais seguro)
        print("📝 Criando novo Dockerfile...")
        
        # Usar sed para criar o arquivo linha por linha
        commands = [
            "echo '# Dockerfile para Backend Flask' > /root/Dojo_Deploy/poker-academy-backend/Dockerfile",
            "echo 'FROM python:3.11-slim' >> /root/Dojo_Deploy/poker-academy-backend/Dockerfile",
            "echo '' >> /root/Dojo_Deploy/poker-academy-backend/Dockerfile",
            "echo 'ENV PYTHONDONTWRITEBYTECODE=1' >> /root/Dojo_Deploy/poker-academy-backend/Dockerfile",
            "echo 'ENV PYTHONUNBUFFERED=1' >> /root/Dojo_Deploy/poker-academy-backend/Dockerfile",
            "echo 'ENV FLASK_ENV=production' >> /root/Dojo_Deploy/poker-academy-backend/Dockerfile",
            "echo 'ENV FLASK_APP=src/main.py' >> /root/Dojo_Deploy/poker-academy-backend/Dockerfile",
            "echo '' >> /root/Dojo_Deploy/poker-academy-backend/Dockerfile",
            "echo 'RUN groupadd -r appuser && useradd -r -g appuser appuser' >> /root/Dojo_Deploy/poker-academy-backend/Dockerfile",
            "echo '' >> /root/Dojo_Deploy/poker-academy-backend/Dockerfile",
            "echo 'RUN apt-get update && apt-get install -y \\\\' >> /root/Dojo_Deploy/poker-academy-backend/Dockerfile",
            "echo '    gcc \\\\' >> /root/Dojo_Deploy/poker-academy-backend/Dockerfile",
            "echo '    default-libmysqlclient-dev \\\\' >> /root/Dojo_Deploy/poker-academy-backend/Dockerfile",
            "echo '    pkg-config \\\\' >> /root/Dojo_Deploy/poker-academy-backend/Dockerfile",
            "echo '    && rm -rf /var/lib/apt/lists/*' >> /root/Dojo_Deploy/poker-academy-backend/Dockerfile",
            "echo '' >> /root/Dojo_Deploy/poker-academy-backend/Dockerfile",
            "echo 'WORKDIR /app' >> /root/Dojo_Deploy/poker-academy-backend/Dockerfile",
            "echo '' >> /root/Dojo_Deploy/poker-academy-backend/Dockerfile",
            "echo 'COPY poker_academy_api/requirements.txt .' >> /root/Dojo_Deploy/poker-academy-backend/Dockerfile",
            "echo '' >> /root/Dojo_Deploy/poker-academy-backend/Dockerfile",
            "echo 'RUN pip install --no-cache-dir --upgrade pip && \\\\' >> /root/Dojo_Deploy/poker-academy-backend/Dockerfile",
            "echo '    pip install --no-cache-dir -r requirements.txt' >> /root/Dojo_Deploy/poker-academy-backend/Dockerfile",
            "echo '' >> /root/Dojo_Deploy/poker-academy-backend/Dockerfile",
            "echo 'RUN pip install gunicorn' >> /root/Dojo_Deploy/poker-academy-backend/Dockerfile",
            "echo '' >> /root/Dojo_Deploy/poker-academy-backend/Dockerfile",
            "echo 'COPY poker_academy_api/ .' >> /root/Dojo_Deploy/poker-academy-backend/Dockerfile",
            "echo '' >> /root/Dojo_Deploy/poker-academy-backend/Dockerfile",
            "echo 'RUN mkdir -p logs && chown -R appuser:appuser /app' >> /root/Dojo_Deploy/poker-academy-backend/Dockerfile",
            "echo '' >> /root/Dojo_Deploy/poker-academy-backend/Dockerfile",
            "echo 'USER appuser' >> /root/Dojo_Deploy/poker-academy-backend/Dockerfile",
            "echo '' >> /root/Dojo_Deploy/poker-academy-backend/Dockerfile",
            "echo 'EXPOSE 5000' >> /root/Dojo_Deploy/poker-academy-backend/Dockerfile",
            "echo '' >> /root/Dojo_Deploy/poker-academy-backend/Dockerfile",
            "echo 'CMD [\"gunicorn\", \"--bind\", \"0.0.0.0:5000\", \"--workers\", \"4\", \"--timeout\", \"120\", \"--access-logfile\", \"-\", \"--error-logfile\", \"-\", \"src.main:app\"]' >> /root/Dojo_Deploy/poker-academy-backend/Dockerfile",
        ]
        
        for cmd in commands:
            execute_command(client, cmd)
        
        print("✅ Novo Dockerfile criado!\n")
        
        # Verificar resultado
        print("📝 Verificando novo Dockerfile...")
        output, error = execute_command(client, "cat /root/Dojo_Deploy/poker-academy-backend/Dockerfile | tail -20")
        print(output)
        
        # Limpar imagens antigas
        print("\n📝 Limpando imagens antigas...")
        execute_command(client, "docker rmi -f $(docker images -q) 2>/dev/null || true")
        print("✅ Imagens limpas!\n")
        
        # Reconstruir
        print("📝 Reconstruindo...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose build --no-cache", timeout=600)
        print("✅ Build concluído!\n")
        
        # Iniciar
        print("📝 Iniciando containers...")
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d")
        print("✅ Comando enviado!\n")
        
        # Aguardar
        print("⏳ Aguardando 180 segundos...")
        time.sleep(180)
        
        # Verificar status
        print("\n📝 Status dos containers:")
        output, error = execute_command(client, "docker ps")
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

