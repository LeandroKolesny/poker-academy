#!/bin/bash

# Script para fazer upload do novo logo para o servidor

echo "🔧 Fazendo upload do novo logo..."

# Verificar se o arquivo existe
if [ ! -f "poker-academy/public/logo-dojo-poker.png" ]; then
    echo "❌ Arquivo logo-dojo-poker.png não encontrado!"
    echo "📁 Certifique-se de que o arquivo está em: poker-academy/public/logo-dojo-poker.png"
    exit 1
fi

# Mostrar informações do arquivo
echo "📊 Informações do arquivo local:"
ls -la poker-academy/public/logo-dojo-poker.png

# Fazer upload para o servidor
echo "📤 Enviando arquivo para o servidor..."
sshpass -p 'DojoShh159357' scp -o StrictHostKeyChecking=no poker-academy/public/logo-dojo-poker.png root@142.93.206.128:/root/poker-academy/poker-academy/public/logo-dojo-poker.png

if [ $? -eq 0 ]; then
    echo "✅ Upload concluído!"
    
    # Verificar no servidor
    echo "🔍 Verificando arquivo no servidor..."
    sshpass -p 'DojoShh159357' ssh -o StrictHostKeyChecking=no root@142.93.206.128 "ls -la /root/poker-academy/poker-academy/public/logo-dojo-poker.png"
    
    # Reconstruir frontend
    echo "🔄 Reconstruindo frontend..."
    sshpass -p 'DojoShh159357' ssh -o StrictHostKeyChecking=no root@142.93.206.128 "cd /root/poker-academy && docker-compose stop frontend && docker-compose rm -f frontend && docker-compose build --no-cache frontend && docker-compose up -d frontend"
    
    echo "🎉 Logo atualizado com sucesso!"
    echo "🌐 Acesse http://142.93.206.128 e use Ctrl+F5 para ver o novo logo"
else
    echo "❌ Erro no upload!"
fi
