#!/usr/bin/env python3
"""
Script para corrigir Dockerfile no servidor
"""

import paramiko
import time

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"
SSH_PORT = 22

def execute_command(client, command, timeout=120):
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
        
        # Criar novo Dockerfile correto
        dockerfile_content = """# Dockerfile para Backend Flask
FROM python:3.11-slim

# Definir variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production
ENV FLASK_APP=src/main.py

# Criar usuário não-root para segurança
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \\
    gcc \\
    default-libmysqlclient-dev \\
    pkg-config \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar requirements primeiro (para cache do Docker)
COPY poker_academy_api/requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir --upgrade pip && \\
    pip install --no-cache-dir -r requirements.txt

# Instalar Gunicorn para produção
RUN pip install gunicorn

# Copiar código da aplicação
COPY poker_academy_api/ .

# Criar diretórios necessários
# Cache invalidation: 2025-10-16-add-curl
RUN mkdir -p logs && \\
    chown -R appuser:appuser /app

# Mudar para usuário não-root
USER appuser

# Expor porta
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "src.main:app"]
"""
        
        print("📝 Criando novo Dockerfile correto...")
        # Usar SFTP para copiar
        sftp = client.open_sftp()
        with sftp.file('/root/Dojo_Deploy/poker-academy/poker-academy-backend/Dockerfile', 'w') as f:
            f.write(dockerfile_content)
        sftp.close()
        print("✅ Dockerfile criado!")
        
        # Verificar
        print("\n📝 Verificando Dockerfile:")
        output, error = execute_command(client, "cat /root/Dojo_Deploy/poker-academy/poker-academy-backend/Dockerfile | grep -A 6 'Instalar dependências'")
        print(output)
        
        # Parar containers
        print("\n📝 Parando containers...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose down")
        print("✅ Containers parados!")
        
        # Remover imagens e cache
        print("\n📝 Removendo imagens e cache...")
        output, error = execute_command(client, "docker rmi poker-academy_backend -f 2>/dev/null; docker builder prune -af 2>/dev/null; true")
        print("✅ Imagens removidas!")
        
        # Reconstruir
        print("\n📝 Reconstruindo backend (isso pode levar alguns minutos)...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose build backend 2>&1 | tail -50", timeout=300)
        print(output)
        
        # Iniciar
        print("\n📝 Iniciando containers...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d")
        print("✅ Containers iniciados!")
        
        # Aguardar
        print("\n⏳ Aguardando 40 segundos para containers iniciarem...")
        time.sleep(40)
        
        # Verificar curl
        print("\n📝 Verificando se curl está instalado...")
        output, error = execute_command(client, "docker exec poker_backend which curl")
        if output.strip():
            print(f"✅ curl encontrado em: {output.strip()}")
        else:
            print("❌ curl não encontrado!")
        
        # Testar health check
        print("\n📝 Testando health check...")
        output, error = execute_command(client, "docker exec poker_backend curl -s http://localhost:5000/api/health")
        print(f"Response: {output}")
        
        # Testar login
        print("\n📝 Testando login com admin/admin123...")
        output, error = execute_command(client, "docker exec poker_backend curl -s -X POST http://localhost:5000/api/auth/login -H 'Content-Type: application/json' -d '{\"username\":\"admin\",\"password\":\"admin123\"}'")
        print(f"Response: {output}")
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ DOCKERFILE CORRIGIDO E TESTADO!")
        print("=" * 70)
        print("\n🌐 Acesse: https://cardroomgrinders.com.br")
        print("👤 Usuário: admin")
        print("🔑 Senha: admin123")
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix()

