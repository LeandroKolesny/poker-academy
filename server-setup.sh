#!/bin/bash

# Script de configuração inicial do servidor Ubuntu/Debian
# Para ser executado no servidor VPS da DigitalOcean

set -e

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
    exit 1
}

info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

# Atualizar sistema
update_system() {
    log "Atualizando sistema..."
    apt update && apt upgrade -y
    log "Sistema atualizado ✓"
}

# Instalar dependências básicas
install_dependencies() {
    log "Instalando dependências básicas..."
    apt install -y \
        curl \
        wget \
        git \
        unzip \
        software-properties-common \
        apt-transport-https \
        ca-certificates \
        gnupg \
        lsb-release \
        ufw \
        fail2ban \
        htop \
        nano \
        vim
    log "Dependências básicas instaladas ✓"
}

# Instalar Docker
install_docker() {
    log "Instalando Docker..."
    
    # Remover versões antigas
    apt remove -y docker docker-engine docker.io containerd runc || true
    
    # Adicionar repositório oficial do Docker
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Instalar Docker
    apt update
    apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    
    # Adicionar usuário ao grupo docker
    usermod -aG docker $USER
    
    # Habilitar Docker para iniciar automaticamente
    systemctl enable docker
    systemctl start docker
    
    log "Docker instalado ✓"
}

# Instalar Docker Compose (versão standalone)
install_docker_compose() {
    log "Instalando Docker Compose..."
    
    # Baixar Docker Compose
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    
    # Dar permissão de execução
    chmod +x /usr/local/bin/docker-compose
    
    # Criar link simbólico
    ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose
    
    log "Docker Compose instalado ✓"
}

# Configurar firewall
setup_firewall() {
    log "Configurando firewall..."
    
    # Resetar UFW
    ufw --force reset
    
    # Configurações padrão
    ufw default deny incoming
    ufw default allow outgoing
    
    # Permitir SSH
    ufw allow ssh
    ufw allow 22
    
    # Permitir HTTP e HTTPS
    ufw allow 80
    ufw allow 443
    
    # Permitir MySQL (apenas local)
    ufw allow from 172.16.0.0/12 to any port 3306
    
    # Habilitar UFW
    ufw --force enable
    
    log "Firewall configurado ✓"
}

# Configurar Fail2Ban
setup_fail2ban() {
    log "Configurando Fail2Ban..."
    
    # Criar configuração personalizada
    cat > /etc/fail2ban/jail.local << EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
EOF
    
    # Reiniciar Fail2Ban
    systemctl enable fail2ban
    systemctl restart fail2ban
    
    log "Fail2Ban configurado ✓"
}

# Criar usuário para aplicação
create_app_user() {
    log "Criando usuário para aplicação..."
    
    # Criar usuário se não existir
    if ! id "poker" &>/dev/null; then
        useradd -m -s /bin/bash poker
        usermod -aG docker poker
        log "Usuário 'poker' criado ✓"
    else
        log "Usuário 'poker' já existe ✓"
    fi
    
    # Criar diretório da aplicação
    mkdir -p /home/poker/poker-academy
    chown poker:poker /home/poker/poker-academy
    
    log "Diretório da aplicação criado ✓"
}

# Configurar swap (se necessário)
setup_swap() {
    log "Verificando swap..."
    
    if [[ $(swapon --show | wc -l) -eq 0 ]]; then
        log "Criando arquivo de swap..."
        
        # Criar arquivo de swap de 2GB
        fallocate -l 2G /swapfile
        chmod 600 /swapfile
        mkswap /swapfile
        swapon /swapfile
        
        # Adicionar ao fstab
        echo '/swapfile none swap sw 0 0' | tee -a /etc/fstab
        
        log "Swap configurado ✓"
    else
        log "Swap já configurado ✓"
    fi
}

# Otimizar sistema
optimize_system() {
    log "Otimizando sistema..."
    
    # Configurar limites do sistema
    cat >> /etc/security/limits.conf << EOF
* soft nofile 65536
* hard nofile 65536
* soft nproc 32768
* hard nproc 32768
EOF
    
    # Configurar sysctl
    cat >> /etc/sysctl.conf << EOF
# Otimizações para aplicação web
net.core.somaxconn = 65536
net.ipv4.tcp_max_syn_backlog = 65536
net.ipv4.ip_local_port_range = 1024 65535
vm.swappiness = 10
EOF
    
    sysctl -p
    
    log "Sistema otimizado ✓"
}

# Instalar ferramentas de monitoramento
install_monitoring() {
    log "Instalando ferramentas de monitoramento..."
    
    # Instalar htop, iotop, etc.
    apt install -y htop iotop nethogs ncdu tree
    
    log "Ferramentas de monitoramento instaladas ✓"
}

# Função principal
main() {
    log "🚀 Iniciando configuração do servidor..."
    
    # Verificar se é root
    if [[ $EUID -ne 0 ]]; then
        error "Este script deve ser executado como root (use sudo)"
    fi
    
    # Executar configurações
    update_system
    install_dependencies
    install_docker
    install_docker_compose
    setup_firewall
    setup_fail2ban
    create_app_user
    setup_swap
    optimize_system
    install_monitoring
    
    log "🎉 Configuração do servidor concluída!"
    
    echo ""
    info "Próximos passos:"
    info "1. Faça logout e login novamente para aplicar as permissões do Docker"
    info "2. Clone o repositório da aplicação em /home/poker/poker-academy"
    info "3. Configure o arquivo .env.production"
    info "4. Execute o script de deploy: ./deploy.sh production"
    
    echo ""
    info "Comandos úteis:"
    info "- Ver status do firewall: ufw status"
    info "- Ver logs do Fail2Ban: fail2ban-client status"
    info "- Ver containers Docker: docker ps"
    info "- Ver uso de recursos: htop"
}

# Executar
main "$@"
