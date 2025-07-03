# 🌐 Configuração do Servidor para cardroomgrinders.com.br

## ✅ **Configuração Local Concluída**

A aplicação já está configurada para o domínio **cardroomgrinders.com.br**:

```bash
# Para fazer build para o domínio
npm run build:domain

# Para alternar configuração
npm run env:domain
```

## 🔧 **Configuração no Servidor DigitalOcean**

### 1. **Configurar NGINX para o Domínio**

Conecte no servidor e edite a configuração do NGINX:

```bash
ssh root@142.93.206.128
```

Crie/edite o arquivo de configuração do site:

```bash
nano /etc/nginx/sites-available/cardroomgrinders.com.br
```

Adicione esta configuração:

```nginx
server {
    listen 80;
    server_name cardroomgrinders.com.br www.cardroomgrinders.com.br;
    
    # Redirecionar HTTP para HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name cardroomgrinders.com.br www.cardroomgrinders.com.br;
    
    # Certificados SSL (será configurado com Certbot)
    ssl_certificate /etc/letsencrypt/live/cardroomgrinders.com.br/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/cardroomgrinders.com.br/privkey.pem;
    
    # Configurações SSL
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    # Root do frontend React
    root /var/www/cardroomgrinders;
    index index.html;
    
    # Servir arquivos estáticos do React
    location / {
        try_files $uri $uri/ /index.html;
        add_header Cache-Control "no-cache, no-store, must-revalidate";
        add_header Pragma "no-cache";
        add_header Expires "0";
    }
    
    # Proxy para API Flask
    location /api/ {
        proxy_pass http://localhost:5000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # CORS Headers
        add_header Access-Control-Allow-Origin "https://cardroomgrinders.com.br" always;
        add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
        add_header Access-Control-Allow-Headers "Origin, X-Requested-With, Content-Type, Accept, Authorization" always;
        
        # Handle preflight requests
        if ($request_method = 'OPTIONS') {
            add_header Access-Control-Allow-Origin "https://cardroomgrinders.com.br";
            add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS";
            add_header Access-Control-Allow-Headers "Origin, X-Requested-With, Content-Type, Accept, Authorization";
            add_header Content-Length 0;
            add_header Content-Type text/plain;
            return 204;
        }
    }
    
    # Servir vídeos com autenticação
    location /videos/ {
        proxy_pass http://localhost:5000/api/videos/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Logs
    access_log /var/log/nginx/cardroomgrinders_access.log;
    error_log /var/log/nginx/cardroomgrinders_error.log;
}
```

### 2. **Ativar o Site**

```bash
# Criar link simbólico
ln -s /etc/nginx/sites-available/cardroomgrinders.com.br /etc/nginx/sites-enabled/

# Testar configuração
nginx -t

# Se OK, recarregar NGINX
systemctl reload nginx
```

### 3. **Instalar Certificado SSL com Certbot**

```bash
# Instalar Certbot (se não estiver instalado)
apt update
apt install certbot python3-certbot-nginx

# Obter certificado SSL
certbot --nginx -d cardroomgrinders.com.br -d www.cardroomgrinders.com.br

# Testar renovação automática
certbot renew --dry-run
```

### 4. **Configurar Backend Flask para HTTPS**

Edite o arquivo de configuração do Flask:

```bash
nano /root/poker-academy/poker-academy-backend/poker_academy_api/.env
```

Adicione/atualize estas variáveis:

```env
# URLs para domínio
FRONTEND_URL=https://cardroomgrinders.com.br
API_BASE_URL=https://cardroomgrinders.com.br/api

# CORS
CORS_ORIGINS=https://cardroomgrinders.com.br,https://www.cardroomgrinders.com.br

# SSL
FORCE_HTTPS=true
SECURE_COOKIES=true
```

### 5. **Atualizar CORS no Flask**

Edite o arquivo principal do Flask:

```bash
nano /root/poker-academy/poker-academy-backend/poker_academy_api/src/main.py
```

Atualize a configuração CORS:

```python
from flask_cors import CORS

# Configurar CORS para domínio
CORS(app, origins=[
    'https://cardroomgrinders.com.br',
    'https://www.cardroomgrinders.com.br',
    'http://localhost:3000'  # Para desenvolvimento
])
```

### 6. **Criar Diretório do Frontend**

```bash
# Criar diretório para o frontend
mkdir -p /var/www/cardroomgrinders

# Definir permissões
chown -R www-data:www-data /var/www/cardroomgrinders
chmod -R 755 /var/www/cardroomgrinders
```

### 7. **Deploy do Frontend**

No seu PC local, faça o build para o domínio:

```bash
# Alternar para configuração de domínio
npm run env:domain

# Fazer build
npm run build
```

Depois copie os arquivos para o servidor:

```bash
# Copiar build para servidor (execute no seu PC)
scp -r build/* root@142.93.206.128:/var/www/cardroomgrinders/
```

### 8. **Reiniciar Serviços**

No servidor:

```bash
# Reiniciar Flask (se usando PM2)
pm2 restart poker-academy-api

# Ou se usando systemd
systemctl restart poker-academy

# Reiniciar NGINX
systemctl restart nginx

# Verificar status
pm2 status
systemctl status nginx
```

### 9. **Configurar DNS (se necessário)**

No painel do seu provedor de domínio, configure:

```
Tipo: A
Nome: @
Valor: 142.93.206.128

Tipo: A  
Nome: www
Valor: 142.93.206.128
```

### 10. **Testar a Configuração**

```bash
# Testar se o domínio responde
curl -I https://cardroomgrinders.com.br

# Testar API
curl -I https://cardroomgrinders.com.br/api/auth/verify-token

# Ver logs do NGINX
tail -f /var/log/nginx/cardroomgrinders_access.log
tail -f /var/log/nginx/cardroomgrinders_error.log
```

## 🔍 **Comandos de Debug**

```bash
# Ver status dos serviços
systemctl status nginx
pm2 status

# Ver logs
journalctl -u nginx -f
pm2 logs poker-academy-api

# Testar configuração NGINX
nginx -t

# Verificar certificado SSL
certbot certificates
```

## 🎯 **Resumo dos Comandos**

### **No seu PC (para deploy):**
```bash
npm run build:domain
scp -r build/* root@142.93.206.128:/var/www/cardroomgrinders/
```

### **No servidor (configuração inicial):**
```bash
# 1. Configurar NGINX
nano /etc/nginx/sites-available/cardroomgrinders.com.br
ln -s /etc/nginx/sites-available/cardroomgrinders.com.br /etc/nginx/sites-enabled/

# 2. SSL
certbot --nginx -d cardroomgrinders.com.br -d www.cardroomgrinders.com.br

# 3. Reiniciar serviços
systemctl restart nginx
pm2 restart poker-academy-api
```

**🎉 Após seguir estes passos, sua aplicação estará rodando em https://cardroomgrinders.com.br!**
