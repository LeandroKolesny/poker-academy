#!/usr/bin/env python3
"""
Script para corrigir Dockerfile via SFTP
"""

import paramiko
import time
import io

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
    """Corrige via SFTP"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Criar novo Dockerfile
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
        
        # Usar SFTP para copiar arquivo
        print("📝 Conectando via SFTP...")
        sftp = client.open_sftp()
        
        # Remover arquivo antigo
        try:
            sftp.remove("/root/Dojo_Deploy/poker-academy-backend/Dockerfile")
            print("✅ Arquivo antigo removido!\n")
        except:
            pass
        
        # Escrever novo arquivo
        print("📝 Escrevendo novo Dockerfile...")
        with sftp.file("/root/Dojo_Deploy/poker-academy-backend/Dockerfile", "w") as f:
            f.write(dockerfile_content)
        print("✅ Novo Dockerfile escrito!\n")
        
        sftp.close()
        
        # Verificar arquivo
        print("📝 Verificando arquivo...")
        output, error = execute_command(client, "cat /root/Dojo_Deploy/poker-academy-backend/Dockerfile | tail -20")
        print(output)
        
        # Limpar cache do Docker
        print("\n📝 Limpando cache do Docker...")
        execute_command(client, "docker builder prune -af")
        print("✅ Cache limpo!\n")
        
        # Remover imagens
        print("📝 Removendo imagens...")
        execute_command(client, "docker rmi -f $(docker images -q) 2>/dev/null || true")
        print("✅ Imagens removidas!\n")
        
        # Reconstruir
        print("📝 Reconstruindo...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose build --no-cache 2>&1 | tail -100", timeout=600)
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

