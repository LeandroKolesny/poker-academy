#!/bin/bash

# Script de Deploy Melhorado com Limpeza de Cache
# Este script faz deploy do build e limpa todos os caches

set -e

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                    🚀 DEPLOY COM LIMPEZA DE CACHE                         ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configurações
SERVER_IP="142.93.206.128"
SERVER_USER="root"
SERVER_PASSWORD="DojoShh159357"
DEPLOY_PATH="/root/Dojo_Deploy/poker-academy"
BUILD_PATH="./poker-academy/build"

echo -e "${BLUE}📋 Verificando pré-requisitos...${NC}"

# Verificar se o build existe
if [ ! -d "$BUILD_PATH" ]; then
    echo -e "${RED}❌ Erro: Diretório de build não encontrado em $BUILD_PATH${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Build encontrado${NC}"

# Fazer backup antes do deploy
echo -e "${BLUE}📦 Criando backup do build anterior...${NC}"
sshpass -p "$SERVER_PASSWORD" ssh -o StrictHostKeyChecking=no $SERVER_USER@$SERVER_IP \
    "cd $DEPLOY_PATH && tar czf backups/build_backup_\$(date +%Y%m%d_%H%M%S).tar.gz poker-academy/build/ 2>/dev/null || true" \
    && echo -e "${GREEN}✅ Backup criado${NC}"

# Copiar novo build
echo -e "${BLUE}📤 Copiando novo build para o servidor...${NC}"
sshpass -p "$SERVER_PASSWORD" scp -r -o StrictHostKeyChecking=no \
    "$BUILD_PATH"/* "$SERVER_USER@$SERVER_IP:$DEPLOY_PATH/poker-academy/build/" \
    && echo -e "${GREEN}✅ Build copiado${NC}"

# Limpar cache do Nginx
echo -e "${BLUE}🧹 Limpando cache do Nginx...${NC}"
sshpass -p "$SERVER_PASSWORD" ssh -o StrictHostKeyChecking=no $SERVER_USER@$SERVER_IP \
    "docker exec poker_frontend rm -rf /var/cache/nginx/* && \
     docker exec poker_frontend nginx -s reload && \
     sleep 2 && \
     echo '✅ Cache do Nginx limpo'" \
    && echo -e "${GREEN}✅ Nginx recarregado${NC}"

# Verificar se o novo arquivo está sendo servido
echo -e "${BLUE}🔍 Verificando se o novo build está sendo servido...${NC}"
MAIN_JS=$(sshpass -p "$SERVER_PASSWORD" ssh -o StrictHostKeyChecking=no $SERVER_USER@$SERVER_IP \
    "curl -s https://cardroomgrinders.com.br/admin/classes 2>&1 | grep -o 'main\.[a-z0-9]*\.js' | head -1")

echo -e "${YELLOW}📄 Arquivo JavaScript sendo servido: $MAIN_JS${NC}"

# Verificar se o novo texto está no arquivo
echo -e "${BLUE}🔍 Verificando se o novo texto está no build...${NC}"
TEXT_CHECK=$(sshpass -p "$SERVER_PASSWORD" ssh -o StrictHostKeyChecking=no $SERVER_USER@$SERVER_IP \
    "grep -o 'Data - Instrutor - Categoria - Nome da aula' $DEPLOY_PATH/poker-academy/build/static/js/$MAIN_JS | wc -l")

if [ "$TEXT_CHECK" -gt 0 ]; then
    echo -e "${GREEN}✅ Novo texto encontrado no build!${NC}"
else
    echo -e "${YELLOW}⚠️  Novo texto NÃO encontrado. Pode ser um problema de cache do Cloudflare.${NC}"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                         ✅ DEPLOY CONCLUÍDO!                              ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${YELLOW}📝 PRÓXIMOS PASSOS:${NC}"
echo "1. Limpe o cache do Cloudflare:"
echo "   - Acesse: https://dash.cloudflare.com"
echo "   - Selecione: cardroomgrinders.com.br"
echo "   - Vá para: Caching → Purge Cache"
echo "   - Clique em: Purge Everything"
echo ""
echo "2. Teste em uma NOVA JANELA ANÔNIMA:"
echo "   - Acesse: https://cardroomgrinders.com.br/admin/classes"
echo "   - Verifique se o novo texto aparece"
echo ""
echo -e "${BLUE}💡 DICA: Se ainda não funcionar, tente:${NC}"
echo "   - Ctrl+Shift+Delete (limpar cache do navegador)"
echo "   - Ou abra em modo incógnito"
echo ""

