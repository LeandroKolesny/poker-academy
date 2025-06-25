#!/bin/bash
# Script para configurar domínio grinders.com.br

echo "🌐 CONFIGURANDO DOMÍNIO grinders.com.br"
echo

# 1. Atualizar docker-compose.yml para usar o domínio
echo "📝 Atualizando docker-compose.yml..."
cd /root/Dojo_Deploy/poker-academy-deploy

# Backup do arquivo atual
cp docker-compose.yml docker-compose.yml.backup

# Atualizar configuração do NGINX
cat > nginx.conf << 'EOF'
server {
    listen 80;
    server_name grinders.com.br www.grinders.com.br;
    
    # Redirecionar HTTP para HTTPS (opcional)
    # return 301 https://$server_name$request_uri;
    
    location / {
        proxy_pass http://frontend:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
    
    location /api {
        proxy_pass http://backend:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
EOF

# 2. Atualizar frontend para usar o domínio
echo "📝 Atualizando configuração do frontend..."
cd /root/Dojo_Deploy/poker-academy/src/services

# Backup do arquivo atual
cp api.js api.js.backup

# Atualizar API_BASE_URL
sed -i 's|http://localhost:5000|https://grinders.com.br|g' api.js
sed -i 's|http://142.93.206.128:5000|https://grinders.com.br|g' api.js

# 3. Atualizar AuthContext
cd /root/Dojo_Deploy/poker-academy/src/context
cp AuthContext.js AuthContext.js.backup
sed -i 's|http://localhost:5000|https://grinders.com.br|g' AuthContext.js
sed -i 's|http://142.93.206.128:5000|https://grinders.com.br|g' AuthContext.js

# 4. Restart dos serviços
echo "🔄 Reiniciando serviços..."
cd /root/Dojo_Deploy/poker-academy-deploy
docker-compose down
docker-compose build --no-cache
docker-compose up -d

echo "✅ CONFIGURAÇÃO CONCLUÍDA!"
echo
echo "🌐 Seu site estará disponível em:"
echo "   - http://grinders.com.br"
echo "   - http://www.grinders.com.br"
echo
echo "⏰ Aguarde 5-10 minutos para propagação do DNS"
echo
echo "🔍 Para verificar se funcionou:"
echo "   nslookup grinders.com.br"
echo
echo "📋 Logs dos serviços:"
echo "   docker-compose logs -f"
