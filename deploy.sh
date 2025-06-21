#!/bin/bash

# Script de Deploy para Poker Academy
# Uso: ./deploy.sh [production|development]
# Servidor: 10.116.0.2
# GitHub: LeandroKolesny/poker-academy

set -e  # Parar em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para log
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
    exit 1
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

# Verificar se Docker está instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        error "Docker não está instalado. Instale o Docker primeiro."
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose não está instalado. Instale o Docker Compose primeiro."
    fi
    
    log "Docker e Docker Compose encontrados ✓"
}

# Verificar arquivos necessários
check_files() {
    local required_files=(
        "docker-compose.yml"
        "poker-academy-backend/Dockerfile"
        "poker-academy/Dockerfile"
        ".env.production"
    )
    
    for file in "${required_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            error "Arquivo obrigatório não encontrado: $file"
        fi
    done
    
    log "Todos os arquivos necessários encontrados ✓"
}

# Configurar ambiente
setup_environment() {
    local env=${1:-production}
    
    if [[ "$env" == "production" ]]; then
        if [[ ! -f ".env.production" ]]; then
            error "Arquivo .env.production não encontrado"
        fi
        cp .env.production .env
        log "Ambiente de produção configurado ✓"
    else
        log "Ambiente de desenvolvimento configurado ✓"
    fi
}

# Parar containers existentes
stop_containers() {
    log "Parando containers existentes..."
    docker-compose down --remove-orphans || true
    
    # Remover containers órfãos
    docker container prune -f || true
    
    log "Containers parados ✓"
}

# Build das imagens
build_images() {
    log "Construindo imagens Docker..."
    
    # Build do backend
    info "Construindo imagem do backend..."
    docker-compose build backend
    
    # Build do frontend
    info "Construindo imagem do frontend..."
    docker-compose build frontend
    
    log "Imagens construídas com sucesso ✓"
}

# Iniciar serviços
start_services() {
    log "Iniciando serviços..."
    
    # Iniciar MySQL primeiro
    info "Iniciando MySQL..."
    docker-compose up -d mysql
    
    # Aguardar MySQL ficar pronto
    info "Aguardando MySQL ficar pronto..."
    sleep 30
    
    # Verificar se MySQL está pronto
    local retries=0
    local max_retries=30
    
    while ! docker-compose exec mysql mysqladmin ping -h localhost --silent; do
        retries=$((retries + 1))
        if [[ $retries -eq $max_retries ]]; then
            error "MySQL não ficou pronto após $max_retries tentativas"
        fi
        info "Aguardando MySQL... (tentativa $retries/$max_retries)"
        sleep 2
    done
    
    log "MySQL está pronto ✓"
    
    # Iniciar backend
    info "Iniciando backend..."
    docker-compose up -d backend
    
    # Aguardar backend ficar pronto
    sleep 15
    
    # Iniciar frontend
    info "Iniciando frontend..."
    docker-compose up -d frontend
    
    log "Todos os serviços iniciados ✓"
}

# Verificar saúde dos serviços
check_health() {
    log "Verificando saúde dos serviços..."
    
    # Verificar MySQL
    if docker-compose exec mysql mysqladmin ping -h localhost --silent; then
        log "MySQL está saudável ✓"
    else
        error "MySQL não está respondendo"
    fi
    
    # Verificar backend
    sleep 5
    if curl -f http://localhost:5000/api/health &> /dev/null; then
        log "Backend está saudável ✓"
    else
        warning "Backend pode não estar totalmente pronto ainda"
    fi
    
    # Verificar frontend
    if curl -f http://localhost:80 &> /dev/null; then
        log "Frontend está saudável ✓"
    else
        warning "Frontend pode não estar totalmente pronto ainda"
    fi
}

# Mostrar logs
show_logs() {
    log "Mostrando logs dos serviços..."
    docker-compose logs --tail=50
}

# Mostrar status
show_status() {
    log "Status dos containers:"
    docker-compose ps
    
    echo ""
    log "Uso de recursos:"
    docker stats --no-stream
}

# Função principal
main() {
    local env=${1:-production}
    
    log "🚀 Iniciando deploy do Poker Academy - Ambiente: $env"
    
    # Verificações
    check_docker
    check_files
    
    # Setup
    setup_environment "$env"
    
    # Deploy
    stop_containers
    build_images
    start_services
    
    # Verificações finais
    sleep 10
    check_health
    show_status
    
    echo ""
    log "🎉 Deploy concluído com sucesso!"
    log "🌐 Frontend: http://localhost"
    log "🔧 Backend: http://localhost:5000"
    log "🗄️  MySQL: localhost:3306"
    
    echo ""
    info "Para ver logs em tempo real: docker-compose logs -f"
    info "Para parar os serviços: docker-compose down"
    info "Para ver status: docker-compose ps"
}

# Verificar argumentos
if [[ $# -gt 1 ]]; then
    error "Uso: $0 [production|development]"
fi

# Executar função principal
main "$@"
