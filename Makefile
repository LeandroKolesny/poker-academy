# Makefile para Poker Academy
# Comandos úteis para desenvolvimento e produção

.PHONY: help build up down logs status clean restart deploy

# Variáveis
COMPOSE_FILE = docker-compose.yml
ENV_FILE = .env

# Comando padrão
help:
	@echo "🎯 Comandos disponíveis para Poker Academy:"
	@echo ""
	@echo "📦 Build e Deploy:"
	@echo "  make build     - Construir todas as imagens"
	@echo "  make up        - Iniciar todos os serviços"
	@echo "  make down      - Parar todos os serviços"
	@echo "  make restart   - Reiniciar todos os serviços"
	@echo "  make deploy    - Deploy completo (build + up)"
	@echo ""
	@echo "📊 Monitoramento:"
	@echo "  make logs      - Ver logs de todos os serviços"
	@echo "  make status    - Ver status dos containers"
	@echo "  make stats     - Ver estatísticas de recursos"
	@echo ""
	@echo "🧹 Limpeza:"
	@echo "  make clean     - Limpar containers e imagens não utilizadas"
	@echo "  make reset     - Reset completo (down + clean + up)"
	@echo ""
	@echo "🔧 Desenvolvimento:"
	@echo "  make dev       - Iniciar em modo desenvolvimento"
	@echo "  make prod      - Iniciar em modo produção"
	@echo "  make shell-backend  - Acessar shell do backend"
	@echo "  make shell-mysql    - Acessar MySQL"

# Build das imagens
build:
	@echo "🔨 Construindo imagens..."
	docker-compose build

# Iniciar serviços
up:
	@echo "🚀 Iniciando serviços..."
	docker-compose up -d

# Parar serviços
down:
	@echo "🛑 Parando serviços..."
	docker-compose down

# Ver logs
logs:
	@echo "📋 Logs dos serviços:"
	docker-compose logs -f

# Status dos containers
status:
	@echo "📊 Status dos containers:"
	docker-compose ps

# Estatísticas de recursos
stats:
	@echo "📈 Estatísticas de recursos:"
	docker stats --no-stream

# Reiniciar serviços
restart: down up

# Deploy completo
deploy:
	@echo "🚀 Iniciando deploy completo..."
	chmod +x deploy.sh
	./deploy.sh production

# Modo desenvolvimento
dev:
	@echo "🔧 Iniciando em modo desenvolvimento..."
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Modo produção
prod:
	@echo "🏭 Iniciando em modo produção..."
	cp .env.production .env
	docker-compose up -d

# Limpeza
clean:
	@echo "🧹 Limpando containers e imagens não utilizadas..."
	docker system prune -f
	docker volume prune -f

# Reset completo
reset: down clean
	@echo "🔄 Reset completo..."
	docker-compose up -d

# Acessar shell do backend
shell-backend:
	@echo "🐚 Acessando shell do backend..."
	docker-compose exec backend /bin/bash

# Acessar MySQL
shell-mysql:
	@echo "🗄️ Acessando MySQL..."
	docker-compose exec mysql mysql -u root -p poker_academy

# Backup do banco
backup:
	@echo "💾 Criando backup do banco..."
	mkdir -p backups
	docker-compose exec mysql mysqldump -u root -p poker_academy > backups/backup_$(shell date +%Y%m%d_%H%M%S).sql

# Restaurar backup
restore:
	@echo "📥 Para restaurar um backup, use:"
	@echo "docker-compose exec -T mysql mysql -u root -p poker_academy < backups/seu_backup.sql"

# Ver configuração
config:
	@echo "⚙️ Configuração do Docker Compose:"
	docker-compose config

# Atualizar imagens
update:
	@echo "🔄 Atualizando imagens..."
	docker-compose pull
	docker-compose build --no-cache

# Verificar saúde
health:
	@echo "🏥 Verificando saúde dos serviços..."
	@echo "Backend:" && curl -f http://localhost:5000/api/health || echo "❌ Backend não está respondendo"
	@echo "Frontend:" && curl -f http://localhost:80 || echo "❌ Frontend não está respondendo"
	@echo "MySQL:" && docker-compose exec mysql mysqladmin ping -h localhost --silent && echo "✅ MySQL OK" || echo "❌ MySQL não está respondendo"
