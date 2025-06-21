@echo off
echo 📦 Criando pacote de deploy do Poker Academy...

REM Criar diretório temporário
if exist poker-academy-deploy rmdir /s /q poker-academy-deploy
mkdir poker-academy-deploy

REM Copiar arquivos essenciais
echo Copiando arquivos...
copy docker-compose.yml poker-academy-deploy\
copy .env.production poker-academy-deploy\
copy deploy.sh poker-academy-deploy\
copy Makefile poker-academy-deploy\
copy DEPLOY-INSTRUCTIONS.md poker-academy-deploy\

REM Copiar diretórios
xcopy /E /I mysql poker-academy-deploy\mysql
xcopy /E /I poker-academy-backend poker-academy-deploy\poker-academy-backend
xcopy /E /I poker-academy poker-academy-deploy\poker-academy

REM Excluir arquivos desnecessários
if exist poker-academy-deploy\poker-academy\node_modules rmdir /s /q poker-academy-deploy\poker-academy\node_modules
if exist poker-academy-deploy\poker-academy-backend\__pycache__ rmdir /s /q poker-academy-deploy\poker-academy-backend\__pycache__

echo ✅ Pacote criado na pasta: poker-academy-deploy
echo.
echo 📋 Próximos passos:
echo 1. Use WinSCP ou similar para enviar a pasta poker-academy-deploy para o servidor
echo 2. Conecte via SSH: ssh root@142.93.206.128
echo 3. Siga as instruções em DEPLOY-INSTRUCTIONS.md
echo.
echo 🌐 Servidor: 142.93.206.128
echo 👤 Usuário: root
echo 🔑 Senha: DojoShh159357
echo.
pause
