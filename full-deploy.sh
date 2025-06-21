#!/bin/bash

# Script de Deploy Completo - Poker Academy
# Executa todo o processo de deploy automaticamente
# Servidor: 10.116.0.2
# GitHub: LeandroKolesny

set -e

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SERVER_IP="10.116.0.2"
GITHUB_USER="LeandroKolesny"
REPO_NAME="poker-academy"

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

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

# Função para verificar se comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Verificar dependências locais
check_local_dependencies() {
    log "Verificando dependências locais..."
    
    if ! command_exists git; then
        error "Git não está instalado"
    fi
    
    if ! command_exists ssh; then
        error "SSH não está instalado"
    fi
    
    log "Dependências locais OK ✓"
}

# Configurar Git (se necessário)
setup_git() {
    log "Configurando Git..."
    
    # Verificar se já está configurado
    if ! git config user.name >/dev/null 2>&1; then
        git config user.name "leandro"
        git config user.email "lekolesny@hotmail.com"
        log "Git configurado ✓"
    else
        log "Git já configurado ✓"
    fi
}

# Criar repositório local
setup_local_repo() {
    log "Configurando repositório local..."
    
    # Inicializar git se necessário
    if [[ ! -d ".git" ]]; then
        git init
        log "Repositório Git inicializado ✓"
    fi
    
    # Adicionar arquivos
    git add .
    
    # Commit se há mudanças
    if ! git diff --cached --quiet; then
        git commit -m "Deploy setup - Poker Academy with Docker configuration"
        log "Commit criado ✓"
    else
        log "Nenhuma mudança para commit ✓"
    fi
    
    # Configurar branch main
    git branch -M main
    
    log "Repositório local configurado ✓"
}

# Verificar conectividade com servidor
check_server_connection() {
    log "Verificando conectividade com servidor $SERVER_IP..."
    
    if ping -c 1 "$SERVER_IP" >/dev/null 2>&1; then
        log "Servidor $SERVER_IP está acessível ✓"
    else
        error "Não foi possível conectar ao servidor $SERVER_IP"
    fi
}

# Configurar servidor via SSH
setup_server() {
    log "Configurando servidor $SERVER_IP..."
    
    # Criar script temporário para enviar ao servidor
    cat > /tmp/server_setup_remote.sh << 'EOF'
#!/bin/bash
set -e

log() {
    echo -e "\033[0;32m[$(date +'%Y-%m-%d %H:%M:%S')] $1\033[0m"
}

error() {
    echo -e "\033[0;31m[ERROR] $1\033[0m"
    exit 1
}

log "Iniciando configuração do servidor..."

# Atualizar sistema
log "Atualizando sistema..."
apt update && apt upgrade -y

# Instalar dependências
log "Instalando dependências..."
apt install -y curl wget git unzip software-properties-common apt-transport-https ca-certificates gnupg lsb-release ufw fail2ban htop

# Instalar Docker
log "Instalando Docker..."
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Instalar Docker Compose standalone
log "Instalando Docker Compose..."
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose

# Configurar firewall
log "Configurando firewall..."
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 22
ufw allow 80
ufw allow 443
ufw --force enable

# Criar usuário para aplicação
log "Criando usuário poker..."
if ! id "poker" &>/dev/null; then
    useradd -m -s /bin/bash poker
    usermod -aG docker poker
fi

# Criar diretório da aplicação
mkdir -p /home/poker/poker-academy
chown poker:poker /home/poker/poker-academy

# Habilitar Docker
systemctl enable docker
systemctl start docker

log "Servidor configurado com sucesso!"
EOF

    # Enviar e executar script no servidor
    info "Enviando script de configuração para o servidor..."
    scp /tmp/server_setup_remote.sh root@$SERVER_IP:/tmp/
    
    info "Executando configuração no servidor..."
    ssh root@$SERVER_IP "chmod +x /tmp/server_setup_remote.sh && /tmp/server_setup_remote.sh"
    
    # Limpar arquivo temporário
    rm /tmp/server_setup_remote.sh
    
    log "Servidor configurado com sucesso ✓"
}

# Enviar arquivos para servidor
deploy_to_server() {
    log "Enviando arquivos para o servidor..."
    
    # Criar arquivo tar com todos os arquivos necessários
    tar -czf /tmp/poker-academy.tar.gz \
        --exclude='.git' \
        --exclude='node_modules' \
        --exclude='__pycache__' \
        --exclude='*.pyc' \
        --exclude='.env' \
        .
    
    # Enviar arquivo
    scp /tmp/poker-academy.tar.gz poker@$SERVER_IP:/home/poker/
    
    # Extrair no servidor
    ssh poker@$SERVER_IP "
        cd /home/poker && 
        tar -xzf poker-academy.tar.gz -C poker-academy --strip-components=0 || 
        (rm -rf poker-academy && mkdir poker-academy && tar -xzf poker-academy.tar.gz -C poker-academy) &&
        rm poker-academy.tar.gz
    "
    
    # Limpar arquivo local
    rm /tmp/poker-academy.tar.gz
    
    log "Arquivos enviados com sucesso ✓"
}

# Executar deploy no servidor
run_deploy() {
    log "Executando deploy no servidor..."
    
    ssh poker@$SERVER_IP "
        cd /home/poker/poker-academy &&
        cp .env.production .env &&
        chmod +x deploy.sh &&
        ./deploy.sh production
    "
    
    log "Deploy executado com sucesso ✓"
}

# Verificar deploy
verify_deploy() {
    log "Verificando deploy..."
    
    # Aguardar serviços iniciarem
    sleep 30
    
    # Verificar se serviços estão rodando
    if curl -f http://$SERVER_IP/api/health >/dev/null 2>&1; then
        log "Backend está funcionando ✓"
    else
        warning "Backend pode não estar totalmente pronto ainda"
    fi
    
    if curl -f http://$SERVER_IP >/dev/null 2>&1; then
        log "Frontend está funcionando ✓"
    else
        warning "Frontend pode não estar totalmente pronto ainda"
    fi
}

# Função principal
main() {
    log "🚀 Iniciando deploy completo do Poker Academy"
    log "Servidor: $SERVER_IP"
    log "GitHub: $GITHUB_USER/$REPO_NAME"
    
    echo ""
    warning "Este script irá:"
    warning "1. Configurar Git local"
    warning "2. Configurar servidor $SERVER_IP"
    warning "3. Instalar Docker no servidor"
    warning "4. Enviar arquivos da aplicação"
    warning "5. Executar deploy com Docker"
    echo ""
    
    read -p "Deseja continuar? (s/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        log "Deploy cancelado pelo usuário"
        exit 0
    fi
    
    # Executar passos
    check_local_dependencies
    setup_git
    setup_local_repo
    check_server_connection
    setup_server
    deploy_to_server
    run_deploy
    verify_deploy
    
    echo ""
    log "🎉 Deploy concluído com sucesso!"
    log "🌐 Acesse sua aplicação em: http://$SERVER_IP"
    log "🔧 Backend API: http://$SERVER_IP/api/health"
    
    echo ""
    info "Para monitorar os serviços:"
    info "ssh poker@$SERVER_IP"
    info "cd /home/poker/poker-academy"
    info "docker-compose logs -f"
}

# Verificar se é executado diretamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
