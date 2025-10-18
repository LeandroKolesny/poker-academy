#!/bin/bash

# Script de Recuperação Automática do Servidor Poker Academy
# Uso: ./recuperar_servidor.sh

SERVER_IP="142.93.206.128"
SERVER_USER="root"

echo "=========================================="
echo "Recuperação do Servidor Poker Academy"
echo "=========================================="
echo ""

# Conectar ao servidor e executar comandos
ssh -o StrictHostKeyChecking=no ${SERVER_USER}@${SERVER_IP} << 'EOF'

echo "1. Verificando status dos containers Docker..."
docker ps -a
echo ""

echo "2. Iniciando Backend (se estiver parado)..."
docker start backend 2>/dev/null || echo "Backend já está rodando"
echo ""

echo "3. Verificando status do NGINX..."
systemctl status nginx --no-pager
echo ""

echo "4. Iniciando NGINX (se estiver parado)..."
systemctl start nginx 2>/dev/null || echo "NGINX já está rodando"
echo ""

echo "5. Verificando portas em uso..."
echo "--- Porta 80 (NGINX) ---"
lsof -i :80 2>/dev/null || echo "Nenhum processo na porta 80"
echo ""

echo "--- Porta 5000 (Backend) ---"
lsof -i :5000 2>/dev/null || echo "Nenhum processo na porta 5000"
echo ""

echo "--- Porta 3306 (MySQL) ---"
lsof -i :3306 2>/dev/null || echo "Nenhum processo na porta 3306"
echo ""

echo "6. Testando conectividade do Backend..."
curl -s http://localhost:5000/api/health || echo "Backend não respondeu"
echo ""
echo ""

echo "7. Verificando arquivos do Frontend..."
ls -lh /var/www/html/ | head -15
echo ""

echo "=========================================="
echo "Recuperação Concluída!"
echo "=========================================="
echo ""
echo "Acesse: https://cardroomgrinders.com.br"
echo ""

EOF

echo "Script finalizado!"

