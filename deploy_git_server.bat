@echo off
echo 🚀 DEPLOY COM GIT PARA SERVIDOR
echo.

echo 📋 COMANDOS PARA EXECUTAR NO SERVIDOR:
echo.
echo 1. Conecte no servidor via SSH:
echo    ssh root@10.116.0.2
echo    Senha: DojoShh159357
echo.
echo 2. Navegue para pasta de deploy:
echo    cd /root/Dojo_Deploy
echo.
echo 3. Faça backup da versão atual:
echo    cp -r poker-academy poker-academy-backup-$(date +%%Y%%m%%d)
echo    cp -r poker-academy-backend poker-academy-backend-backup-$(date +%%Y%%m%%d)
echo.
echo 4. Clone o repositório Git (se ainda não existe):
echo    git clone https://github.com/LeandroKolesny/poker-academy.git poker-academy-git
echo.
echo 5. Ou atualize se já existe:
echo    cd poker-academy-git
echo    git pull origin main
echo.
echo 6. Copie arquivos atualizados:
echo    cp -r poker-academy-git/poker-academy/* poker-academy/
echo    cp -r poker-academy-git/poker-academy-backend/* poker-academy-backend/
echo.
echo 7. Rebuild e restart:
echo    cd /root/Dojo_Deploy/poker-academy-deploy
echo    docker-compose down
echo    docker-compose build --no-cache
echo    docker-compose up -d
echo.
echo 8. Verificar logs:
echo    docker-compose logs -f backend
echo.

echo 💡 DICA: Copie e cole cada comando um por vez no terminal SSH
echo.
pause
