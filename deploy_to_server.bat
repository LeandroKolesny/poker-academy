@echo off
echo 🚀 DEPLOY PARA SERVIDOR COM GIT...
echo.

echo 📋 INSTRUÇÕES PARA DEPLOY:
echo.
echo 🔧 OPÇÃO 1: DEPLOY MANUAL (RECOMENDADO PARA PRIMEIRA VEZ)
echo 1. Use WinSCP ou FileZilla
echo 2. Conecte no servidor: root@SEU_IP (senha: DojoShh159357)
echo 3. Copie os arquivos da pasta deploy_final/
echo 4. Execute comandos Docker no servidor
echo.
echo 🔧 OPÇÃO 2: DEPLOY COM GIT (AVANÇADO)
echo 1. Criar repositório no GitHub/GitLab
echo 2. Fazer push do código
echo 3. Fazer pull no servidor
echo.

set /p choice="Escolha uma opção (1 ou 2): "

if "%choice%"=="1" (
    echo.
    echo 📁 Abrindo pasta deploy_final...
    explorer deploy_final
    echo.
    echo 📋 COMANDOS PARA O SERVIDOR:
    echo.
    echo cd /root/Dojo_Deploy/poker-academy-deploy
    echo docker-compose down
    echo docker-compose build --no-cache
    echo docker-compose up -d
    echo docker-compose logs -f backend
    echo.
    echo 🧪 TESTES PÓS-DEPLOY:
    echo - Login admin: admin@pokeracademy.com / admin123
    echo - Login student: student@pokeracademy.com / 123456
    echo - Teste alteração senha: Menu lateral → "Alterar Senha"
    echo - Teste upload vídeo: Verificar barra de progresso
    echo - Teste datas: Verificar se aparecem corretas
    echo.
) else if "%choice%"=="2" (
    echo.
    echo 🔧 CONFIGURANDO DEPLOY COM GIT...
    echo.
    echo 📋 PASSOS PARA DEPLOY COM GIT:
    echo 1. Crie um repositório no GitHub
    echo 2. Execute: git remote add origin URL_DO_REPOSITORIO
    echo 3. Execute: git push -u origin main
    echo 4. No servidor, clone o repositório
    echo 5. Configure deploy automático
    echo.
    echo 💡 DICA: Para primeira vez, use a Opção 1 (manual)
    echo.
) else (
    echo ❌ Opção inválida!
)

echo.
pause
