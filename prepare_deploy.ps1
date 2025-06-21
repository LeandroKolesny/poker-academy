# 🚀 Script para preparar arquivos para deploy
# Execute: .\prepare_deploy.ps1

Write-Host "🚀 PREPARANDO ARQUIVOS PARA DEPLOY..." -ForegroundColor Green

# Criar pasta de deploy
$deployFolder = ".\deploy_package"
if (Test-Path $deployFolder) {
    Remove-Item $deployFolder -Recurse -Force
}
New-Item -ItemType Directory -Path $deployFolder | Out-Null

# Criar estrutura de pastas
New-Item -ItemType Directory -Path "$deployFolder\backend" -Force | Out-Null
New-Item -ItemType Directory -Path "$deployFolder\frontend" -Force | Out-Null

Write-Host "📁 Copiando arquivos do BACKEND..." -ForegroundColor Yellow

# Backend files
$backendFiles = @(
    "poker-academy-backend\poker_academy_api\src\routes\auth_routes.py",
    "poker-academy-backend\poker_academy_api\src\models.py",
    "poker-academy-backend\poker_academy_api\src\routes\class_routes.py",
    "poker-academy-backend\poker_academy_api\src\main.py"
)

foreach ($file in $backendFiles) {
    if (Test-Path $file) {
        $relativePath = $file -replace "poker-academy-backend\\poker_academy_api\\", ""
        $destPath = "$deployFolder\backend\$relativePath"
        $destDir = Split-Path $destPath -Parent
        
        if (!(Test-Path $destDir)) {
            New-Item -ItemType Directory -Path $destDir -Force | Out-Null
        }
        
        Copy-Item $file $destPath -Force
        Write-Host "  ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "  ❌ ARQUIVO NÃO ENCONTRADO: $file" -ForegroundColor Red
    }
}

Write-Host "📁 Copiando arquivos do FRONTEND..." -ForegroundColor Yellow

# Frontend files
$frontendFiles = @(
    "poker-academy\src\components\student\ChangePassword.js",
    "poker-academy\src\components\student\StudentDashboard.js",
    "poker-academy\src\services\authService.js",
    "poker-academy\src\components\admin\ClassManagement.js",
    "poker-academy\src\components\student\Catalog.js",
    "poker-academy\src\components\student\Favorites.js",
    "poker-academy\src\components\admin\StudentManagement.js"
)

foreach ($file in $frontendFiles) {
    if (Test-Path $file) {
        $relativePath = $file -replace "poker-academy\\src\\", ""
        $destPath = "$deployFolder\frontend\$relativePath"
        $destDir = Split-Path $destPath -Parent
        
        if (!(Test-Path $destDir)) {
            New-Item -ItemType Directory -Path $destDir -Force | Out-Null
        }
        
        Copy-Item $file $destPath -Force
        Write-Host "  ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "  ❌ ARQUIVO NÃO ENCONTRADO: $file" -ForegroundColor Red
    }
}

# Criar arquivo de instruções
$instructions = @"
🚀 INSTRUÇÕES DE DEPLOY

1. Copie os arquivos desta pasta para o servidor:
   - backend/* → /root/Dojo_Deploy/poker-academy-backend/poker_academy_api/
   - frontend/* → /root/Dojo_Deploy/poker-academy/src/

2. No servidor, execute:
   cd /root/Dojo_Deploy/poker-academy-deploy
   docker-compose down
   docker-compose build --no-cache
   docker-compose up -d

3. Verifique os logs:
   docker-compose logs -f backend
   docker-compose logs -f frontend

4. Teste as funcionalidades:
   - Login admin: admin@pokeracademy.com / admin123
   - Alteração de senha: student@pokeracademy.com / 123456
   - Upload de vídeo com barra de progresso
   - Datas corretas na tabela
"@

$instructions | Out-File -FilePath "$deployFolder\INSTRUCOES_DEPLOY.txt" -Encoding UTF8

Write-Host ""
Write-Host "✅ ARQUIVOS PREPARADOS EM: $deployFolder" -ForegroundColor Green
Write-Host "📋 Leia o arquivo INSTRUCOES_DEPLOY.txt para próximos passos" -ForegroundColor Cyan
Write-Host ""
Write-Host "🔧 PRÓXIMOS PASSOS:" -ForegroundColor Yellow
Write-Host "1. Use WinSCP, FileZilla ou outro cliente SFTP" -ForegroundColor White
Write-Host "2. Conecte no servidor: root@SEU_IP" -ForegroundColor White
Write-Host "3. Copie os arquivos para os diretórios corretos" -ForegroundColor White
Write-Host "4. Execute os comandos Docker no servidor" -ForegroundColor White
