#!/bin/bash

# Script para renovar certificado SSL
# Uso: ./renovar_ssl.sh

echo "=========================================="
echo "Renovação de Certificado SSL"
echo "=========================================="
echo ""

echo "1. Parando NGINX..."
systemctl stop nginx
sleep 3

echo "2. Renovando certificado SSL..."
certbot renew --force-renewal --non-interactive --agree-tos

echo ""
echo "3. Iniciando NGINX..."
systemctl start nginx
sleep 3

echo ""
echo "4. Verificando certificado..."
openssl x509 -in /etc/letsencrypt/live/cardroomgrinders.com.br/fullchain.pem -noout -dates

echo ""
echo "5. Testando HTTPS..."
curl -I https://cardroomgrinders.com.br

echo ""
echo "=========================================="
echo "Renovação Concluída!"
echo "=========================================="

