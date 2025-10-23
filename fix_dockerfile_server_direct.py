#!/usr/bin/env python3
"""
Script para corrigir Dockerfile no servidor diretamente
"""

import paramiko
import time

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"
SSH_PORT = 22

def execute_command(client, command):
    """Executa um comando via SSH"""
    stdin, stdout, stderr = client.exec_command(command)
    time.sleep(1)
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
        
        # Verificar Dockerfile atual
        print("📋 Dockerfile atual:")
        output, error = execute_command(client, "cat /root/Dojo_Deploy/poker-academy-backend/Dockerfile | tail -20")
        print(output)
        
        # Fazer backup
        print("\n📝 Fazendo backup...")
        execute_command(client, "cp /root/Dojo_Deploy/poker-academy-backend/Dockerfile /root/Dojo_Deploy/poker-academy-backend/Dockerfile.bak2")
        print("✅ Backup feito!\n")
        
        # Criar novo Dockerfile sem o mkdir problemático
        print("📝 Criando novo Dockerfile...")
        new_dockerfile = """# Dockerfile para Backend Flask
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

# Criar apenas diretório logs (uploads já existe no código)
RUN mkdir -p logs && \\
    chown -R appuser:appuser /app

# Mudar para usuário não-root
USER appuser

# Expor porta
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "src.main:app"]
"""
        
        # Escrever novo Dockerfile
        cmd = f"""cat > /root/Dojo_Deploy/poker-academy-backend/Dockerfile << 'DOCKERFILE_EOF'
{new_dockerfile}
DOCKERFILE_EOF"""
        
        output, error = execute_command(client, cmd)
        print("✅ Novo Dockerfile criado!\n")
        
        # Verificar resultado
        print("📋 Novo Dockerfile:")
        output, error = execute_command(client, "cat /root/Dojo_Deploy/poker-academy-backend/Dockerfile | tail -20")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ DOCKERFILE CORRIGIDO!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix()

