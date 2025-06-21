@echo off
echo 🚀 Configurando Git e enviando para GitHub...

REM Configurar Git (se necessário)
git config user.name "leandro"
git config user.email "lekolesny@hotmail.com"

REM Inicializar repositório
git init

REM Adicionar todos os arquivos
git add .

REM Fazer commit
git commit -m "Initial commit - Poker Academy with Docker setup"

REM Configurar branch main
git branch -M main

REM Adicionar remote (substitua pela URL do seu repositório)
git remote add origin https://github.com/LeandroKolesny/poker-academy.git

REM Push para GitHub
git push -u origin main

echo ✅ Código enviado para GitHub!
echo 🌐 Repositório: https://github.com/LeandroKolesny/poker-academy
pause
