@echo off
echo 🔧 CONFIGURANDO GIT PARA DEPLOY...
echo.

REM Verificar se Git está instalado
echo 📋 Verificando instalação do Git...
git --version
if %errorlevel% neq 0 (
    echo ❌ Git não encontrado no PATH
    echo 🔍 Tentando localizar Git...
    if exist "C:\Program Files\Git\bin\git.exe" (
        echo ✅ Git encontrado em: C:\Program Files\Git\bin\git.exe
        set PATH=%PATH%;C:\Program Files\Git\bin
    ) else if exist "C:\Program Files (x86)\Git\bin\git.exe" (
        echo ✅ Git encontrado em: C:\Program Files (x86)\Git\bin\git.exe
        set PATH=%PATH%;C:\Program Files (x86)\Git\bin
    ) else (
        echo ❌ Git não encontrado. Instale o Git primeiro!
        pause
        exit /b 1
    )
)

echo.
echo ✅ Git está funcionando!
git --version

echo.
echo 🔧 Configurando Git com suas informações...
git config --global user.name "Dojo Poker"
git config --global user.email "admin@pokeracademy.com"
git config --global init.defaultBranch main

echo.
echo ✅ Git configurado com sucesso!
echo 📋 Configurações atuais:
git config --global user.name
git config --global user.email

echo.
echo 🚀 Próximo passo: Execute setup_repository.bat
pause
