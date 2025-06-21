#!/usr/bin/env python3
"""
Script de deploy direto para o servidor via SSH
Servidor: 142.93.206.128
"""

import os
import sys
import subprocess
import time
import tarfile
import tempfile
from pathlib import Path

# Configurações do servidor
SERVER_IP = "142.93.206.128"
SERVER_USER = "root"
SERVER_PASS = "DojoShh159357"

def log(message, color="green"):
    colors = {
        "green": "\033[92m",
        "red": "\033[91m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "reset": "\033[0m"
    }
    print(f"{colors.get(color, '')}{message}{colors['reset']}")

def run_command(command, check=True):
    """Executa comando local"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=check)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        log(f"Erro ao executar: {command}", "red")
        log(f"Erro: {e.stderr}", "red")
        if check:
            sys.exit(1)
        return None

def ssh_command(command, check=True):
    """Executa comando no servidor via SSH"""
    ssh_cmd = f'sshpass -p "{SERVER_PASS}" ssh -o StrictHostKeyChecking=no {SERVER_USER}@{SERVER_IP} "{command}"'
    return run_command(ssh_cmd, check)

def scp_file(local_path, remote_path):
    """Copia arquivo para servidor via SCP"""
    scp_cmd = f'sshpass -p "{SERVER_PASS}" scp -o StrictHostKeyChecking=no "{local_path}" {SERVER_USER}@{SERVER_IP}:"{remote_path}"'
    return run_command(scp_cmd)

def check_dependencies():
    """Verifica dependências locais"""
    log("Verificando dependências...")
    
    # Verificar se sshpass está disponível (para Windows, usaremos plink)
    if os.name == 'nt':  # Windows
        log("Sistema Windows detectado")
        # Vamos usar uma abordagem diferente para Windows
        return True
    else:
        # Linux/Mac
        if not run_command("which sshpass", check=False):
            log("sshpass não encontrado. Instalando...", "yellow")
            run_command("sudo apt-get update && sudo apt-get install -y sshpass")
    
    log("Dependências OK ✓")
    return True

def test_connection():
    """Testa conexão SSH"""
    log("Testando conexão SSH...")
    
    if os.name == 'nt':  # Windows
        # Para Windows, vamos usar uma abordagem diferente
        log("Conexão SSH será testada durante o deploy")
        return True
    
    try:
        result = ssh_command("echo 'SSH OK'", check=False)
        if result and "SSH OK" in result:
            log("Conexão SSH OK ✓")
            return True
        else:
            log("Falha na conexão SSH", "red")
            return False
    except:
        log("Erro na conexão SSH", "red")
        return False

def create_archive():
    """Cria arquivo tar.gz com os arquivos da aplicação"""
    log("Criando arquivo da aplicação...")
    
    # Arquivos e diretórios para incluir
    include_files = [
        "docker-compose.yml",
        ".env.production",
        "deploy.sh",
        "Makefile",
        "mysql",
        "poker-academy-backend",
        "poker-academy"
    ]
    
    # Arquivos para excluir
    exclude_patterns = [
        "__pycache__",
        "*.pyc",
        "node_modules",
        ".git",
        "*.log",
        ".env"
    ]
    
    archive_path = "poker-academy-deploy.tar.gz"
    
    with tarfile.open(archive_path, "w:gz") as tar:
        for item in include_files:
            if os.path.exists(item):
                log(f"Adicionando: {item}")
                tar.add(item, arcname=item)
            else:
                log(f"Arquivo não encontrado: {item}", "yellow")
    
    log(f"Arquivo criado: {archive_path} ✓")
    return archive_path

def setup_server():
    """Configura o servidor"""
    log("Configurando servidor...")
    
    setup_script = """
#!/bin/bash
set -e

echo "🔧 Configurando servidor Ubuntu..."

# Atualizar sistema
apt update

# Instalar dependências básicas
apt install -y curl wget git unzip software-properties-common apt-transport-https ca-certificates gnupg lsb-release ufw fail2ban htop

# Verificar se Docker já está instalado
if ! command -v docker &> /dev/null; then
    echo "Instalando Docker..."
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    apt update
    apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
else
    echo "Docker já instalado ✓"
fi

# Verificar se Docker Compose já está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "Instalando Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose
else
    echo "Docker Compose já instalado ✓"
fi

# Configurar firewall básico
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 22
ufw allow 80
ufw allow 443
ufw --force enable

# Criar usuário poker se não existir
if ! id "poker" &>/dev/null; then
    useradd -m -s /bin/bash poker
    usermod -aG docker poker
    echo "Usuário poker criado ✓"
else
    echo "Usuário poker já existe ✓"
fi

# Criar diretório da aplicação
mkdir -p /home/poker/poker-academy
chown poker:poker /home/poker/poker-academy

# Habilitar e iniciar Docker
systemctl enable docker
systemctl start docker

echo "✅ Servidor configurado!"
"""
    
    # Salvar script temporário
    with open("temp_setup.sh", "w") as f:
        f.write(setup_script)
    
    # Enviar e executar script
    if os.name == 'nt':  # Windows
        log("Execute manualmente no servidor:", "yellow")
        log("1. Conecte via SSH: ssh root@142.93.206.128", "yellow")
        log("2. Execute o script de configuração", "yellow")
        print(setup_script)
        input("Pressione Enter após configurar o servidor...")
    else:
        scp_file("temp_setup.sh", "/tmp/setup.sh")
        ssh_command("chmod +x /tmp/setup.sh && /tmp/setup.sh")
    
    # Limpar arquivo temporário
    os.remove("temp_setup.sh")
    
    log("Servidor configurado ✓")

def deploy_application():
    """Faz deploy da aplicação"""
    log("Fazendo deploy da aplicação...")
    
    # Criar arquivo da aplicação
    archive_path = create_archive()
    
    if os.name == 'nt':  # Windows
        log("Para Windows, execute manualmente:", "yellow")
        log(f"1. Envie o arquivo {archive_path} para o servidor", "yellow")
        log("2. Extraia na pasta /home/poker/poker-academy", "yellow")
        log("3. Execute o deploy", "yellow")
        
        deploy_commands = """
# No servidor, execute:
cd /home/poker
tar -xzf poker-academy-deploy.tar.gz -C poker-academy
cd poker-academy
cp .env.production .env
chmod +x deploy.sh
./deploy.sh production
"""
        print(deploy_commands)
        return
    
    # Enviar arquivo
    scp_file(archive_path, "/home/poker/poker-academy-deploy.tar.gz")
    
    # Extrair e configurar
    ssh_command("cd /home/poker && tar -xzf poker-academy-deploy.tar.gz -C poker-academy")
    ssh_command("cd /home/poker/poker-academy && cp .env.production .env")
    ssh_command("cd /home/poker/poker-academy && chmod +x deploy.sh")
    
    # Executar deploy
    ssh_command("cd /home/poker/poker-academy && ./deploy.sh production")
    
    # Limpar arquivo local
    os.remove(archive_path)
    
    log("Deploy concluído ✓")

def verify_deployment():
    """Verifica se o deploy foi bem-sucedido"""
    log("Verificando deployment...")
    
    time.sleep(30)  # Aguardar serviços iniciarem
    
    # Verificar se serviços estão rodando
    try:
        import requests
        
        # Testar backend
        response = requests.get(f"http://{SERVER_IP}/api/health", timeout=10)
        if response.status_code == 200:
            log("Backend funcionando ✓")
        else:
            log("Backend com problemas", "yellow")
        
        # Testar frontend
        response = requests.get(f"http://{SERVER_IP}", timeout=10)
        if response.status_code == 200:
            log("Frontend funcionando ✓")
        else:
            log("Frontend com problemas", "yellow")
            
    except Exception as e:
        log(f"Erro na verificação: {e}", "yellow")
        log("Verifique manualmente os serviços", "yellow")

def main():
    """Função principal"""
    log("🚀 Iniciando deploy do Poker Academy")
    log(f"Servidor: {SERVER_IP}")
    
    try:
        # Verificar dependências
        check_dependencies()
        
        # Testar conexão
        test_connection()
        
        # Configurar servidor
        setup_server()
        
        # Deploy da aplicação
        deploy_application()
        
        # Verificar deployment
        verify_deployment()
        
        log("🎉 Deploy concluído com sucesso!")
        log(f"🌐 Acesse: http://{SERVER_IP}")
        log(f"🔧 API: http://{SERVER_IP}/api/health")
        
    except KeyboardInterrupt:
        log("Deploy cancelado pelo usuário", "yellow")
    except Exception as e:
        log(f"Erro durante deploy: {e}", "red")
        sys.exit(1)

if __name__ == "__main__":
    main()
