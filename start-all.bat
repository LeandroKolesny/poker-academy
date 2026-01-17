@echo off
title CardroomGrinders - Iniciando Aplicacao
color 0A

echo ============================================
echo    CARDROOMGRINDERS - POKER ACADEMY
echo ============================================
echo.

:: Definir diretorio base
set BASE_DIR=%~dp0

:: Verificar se Python esta instalado
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERRO] Python nao encontrado! Instale o Python primeiro.
    pause
    exit /b 1
)

:: Verificar se Node.js esta instalado
where node >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERRO] Node.js nao encontrado! Instale o Node.js primeiro.
    pause
    exit /b 1
)

echo [OK] Python encontrado
echo [OK] Node.js encontrado
echo.

:: Verificar se node_modules existe no frontend
if not exist "%BASE_DIR%poker-academy\node_modules" (
    echo [INFO] Instalando dependencias do frontend...
    cd /d "%BASE_DIR%poker-academy"
    npm install
    echo [OK] Dependencias instaladas!
    echo.
)

:: Iniciar Backend (Flask) em nova janela
echo [1/2] Iniciando Backend (Flask) na porta 5000...
start "Backend - Flask API" cmd /k "cd /d %BASE_DIR%poker-academy-backend && python -m flask --app src.main run --host=0.0.0.0 --port=5000"

:: Aguardar backend iniciar
echo      Aguardando backend iniciar...
timeout /t 4 /nobreak >nul

:: Iniciar Frontend (React) em nova janela
echo [2/2] Iniciando Frontend (React) na porta 3000...
start "Frontend - React" cmd /k "cd /d %BASE_DIR%poker-academy && npm start"

echo.
echo ============================================
echo    APLICACAO INICIADA COM SUCESSO!
echo ============================================
echo.
echo  Backend:  http://localhost:5000
echo  Frontend: http://localhost:3000
echo.
echo  Login padrao:
echo    Usuario: admin
echo    Senha:   admin123
echo.
echo  Para parar, feche as janelas ou use stop-all.bat
echo ============================================
echo.

:: Aguardar frontend iniciar
timeout /t 8 /nobreak >nul

:: Abrir o navegador automaticamente
echo Abrindo navegador...
start http://localhost:3000

exit
