@echo off
echo 🚀 ENVIANDO CÓDIGO PARA GITHUB
echo.

echo 📋 Configurando repositório remoto...
"C:\Program Files\Git\bin\git.exe" remote add origin https://github.com/LeandroKolesny/poker-academy.git

echo 📤 Enviando código para GitHub...
"C:\Program Files\Git\bin\git.exe" push -u origin main

if %errorlevel% equ 0 (
    echo ✅ CÓDIGO ENVIADO COM SUCESSO PARA GITHUB!
    echo.
    echo 🎯 PRÓXIMO PASSO: Execute deploy_git_server.bat
    echo    Ou conecte no servidor e execute os comandos manualmente
) else (
    echo ❌ ERRO AO ENVIAR PARA GITHUB
    echo.
    echo 💡 POSSÍVEIS SOLUÇÕES:
    echo 1. Verifique se o repositório existe: https://github.com/LeandroKolesny/poker-academy
    echo 2. Verifique suas credenciais do GitHub
    echo 3. Tente fazer login no GitHub Desktop primeiro
)

echo.
pause
