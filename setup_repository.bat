@echo off
echo 🚀 CONFIGURANDO REPOSITÓRIO GIT...
echo.

REM Verificar se já é um repositório Git
if exist ".git" (
    echo ✅ Repositório Git já existe
) else (
    echo 📁 Inicializando repositório Git...
    git init
    echo ✅ Repositório Git criado!
)

echo.
echo 📝 Criando .gitignore...
(
echo # Dependências Node.js
echo node_modules/
echo npm-debug.log*
echo yarn-debug.log*
echo yarn-error.log*
echo.
echo # Ambiente virtual Python
echo venv/
echo __pycache__/
echo *.pyc
echo *.pyo
echo.
echo # Arquivos de configuração sensíveis
echo .env
echo *.log
echo.
echo # Arquivos temporários
echo *.tmp
echo *.temp
echo .DS_Store
echo Thumbs.db
echo.
echo # Uploads e arquivos grandes
echo uploads/
echo *.mp4
echo *.avi
echo *.mov
echo.
echo # Arquivos de deploy temporários
echo deploy_*/
echo backup_*/
) > .gitignore

echo ✅ .gitignore criado!

echo.
echo 📦 Adicionando arquivos ao Git...
git add .
git status

echo.
echo 💾 Fazendo primeiro commit...
git commit -m "Projeto inicial: Poker Academy com alteração de senha e correções de timezone"

echo.
echo ✅ REPOSITÓRIO CONFIGURADO COM SUCESSO!
echo.
echo 🎯 PRÓXIMOS PASSOS:
echo 1. Execute: deploy_to_server.bat
echo 2. Ou siga as instruções manuais no arquivo DEPLOY_INSTRUCTIONS.txt
echo.
pause
