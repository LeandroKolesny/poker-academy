# Script simples para copiar arquivos alterados
Write-Host "Preparando arquivos para deploy..." -ForegroundColor Green

# Criar pasta de deploy
$deployFolder = ".\deploy_package"
if (Test-Path $deployFolder) {
    Remove-Item $deployFolder -Recurse -Force
}
New-Item -ItemType Directory -Path $deployFolder | Out-Null
New-Item -ItemType Directory -Path "$deployFolder\backend\src\routes" -Force | Out-Null
New-Item -ItemType Directory -Path "$deployFolder\backend\src" -Force | Out-Null
New-Item -ItemType Directory -Path "$deployFolder\frontend\components\student" -Force | Out-Null
New-Item -ItemType Directory -Path "$deployFolder\frontend\components\admin" -Force | Out-Null
New-Item -ItemType Directory -Path "$deployFolder\frontend\services" -Force | Out-Null

# Copiar arquivos backend
Copy-Item "poker-academy-backend\poker_academy_api\src\routes\auth_routes.py" "$deployFolder\backend\src\routes\" -Force
Copy-Item "poker-academy-backend\poker_academy_api\src\models.py" "$deployFolder\backend\src\" -Force
Copy-Item "poker-academy-backend\poker_academy_api\src\routes\class_routes.py" "$deployFolder\backend\src\routes\" -Force
Copy-Item "poker-academy-backend\poker_academy_api\src\main.py" "$deployFolder\backend\src\" -Force

# Copiar arquivos frontend
Copy-Item "poker-academy\src\components\student\ChangePassword.js" "$deployFolder\frontend\components\student\" -Force
Copy-Item "poker-academy\src\components\student\StudentDashboard.js" "$deployFolder\frontend\components\student\" -Force
Copy-Item "poker-academy\src\services\authService.js" "$deployFolder\frontend\services\" -Force
Copy-Item "poker-academy\src\components\admin\ClassManagement.js" "$deployFolder\frontend\components\admin\" -Force
Copy-Item "poker-academy\src\components\student\Catalog.js" "$deployFolder\frontend\components\student\" -Force
Copy-Item "poker-academy\src\components\student\Favorites.js" "$deployFolder\frontend\components\student\" -Force
Copy-Item "poker-academy\src\components\admin\StudentManagement.js" "$deployFolder\frontend\components\admin\" -Force

Write-Host "Arquivos copiados para: $deployFolder" -ForegroundColor Green
Write-Host "Use WinSCP ou FileZilla para enviar ao servidor" -ForegroundColor Yellow
