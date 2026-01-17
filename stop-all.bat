@echo off
title CardroomGrinders - Parando Aplicacao
color 0C

echo ============================================
echo    PARANDO CARDROOMGRINDERS
echo ============================================
echo.

:: Matar processos do Flask (Python)
echo [1/2] Parando Backend (Flask)...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Backend*" >nul 2>nul

:: Matar processos do Node (React)
echo [2/2] Parando Frontend (React)...
taskkill /F /FI "WINDOWTITLE eq Frontend*" >nul 2>nul

:: Matar processos na porta 5000 e 3000
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>nul
)
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>nul
)

echo.
echo ============================================
echo    APLICACAO PARADA!
echo ============================================
echo.

timeout /t 3
exit
