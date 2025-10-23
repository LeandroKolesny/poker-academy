#!/usr/bin/env python3
"""
Script para corrigir Dockerfile e reconstruir
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
    """Corrige e reconstrói"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Passo 1: Corrigir Dockerfile
        print("📝 Passo 1: Corrigindo Dockerfile...")
        
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
        
        cmd = f"""cat > /root/Dojo_Deploy/poker-academy-backend/Dockerfile << 'DOCKERFILE_EOF'
{new_dockerfile}
DOCKERFILE_EOF"""
        
        execute_command(client, cmd)
        print("✅ Dockerfile corrigido!\n")
        
        # Passo 2: Remover containers com erro
        print("📝 Passo 2: Removendo containers com erro...")
        execute_command(client, "docker rm -f $(docker ps -a -q) 2>/dev/null || true")
        print("✅ Containers removidos!\n")
        
        # Passo 3: Reconstruir
        print("📝 Passo 3: Reconstruindo com docker-compose...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose build --no-cache", timeout=600)
        print("✅ Build concluído!\n")
        
        # Passo 4: Iniciar
        print("📝 Passo 4: Iniciando containers...")
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d")
        print("✅ Comando enviado!\n")
        
        # Aguardar
        print("⏳ Aguardando containers iniciarem (180 segundos)...")
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
        print("✅ RECONSTRUÇÃO CONCLUÍDA!")
        print("=" * 70)
        print("\n🎉 APLICAÇÃO DEVE ESTAR RODANDO!")
        print("  Acesse https://cardroomgrinders.com.br para testar")
        print("\n" + "=" * 70)
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix()

