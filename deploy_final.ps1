# Script final para preparar deploy
Write-Host "🚀 PREPARANDO DEPLOY FINAL..." -ForegroundColor Green

# Criar pasta de deploy
$deployFolder = ".\deploy_final"
if (Test-Path $deployFolder) {
    Remove-Item $deployFolder -Recurse -Force
}
New-Item -ItemType Directory -Path $deployFolder | Out-Null

# Criar estrutura backend
New-Item -ItemType Directory -Path "$deployFolder\backend\src\routes" -Force | Out-Null
New-Item -ItemType Directory -Path "$deployFolder\backend\src" -Force | Out-Null

# Criar estrutura frontend
New-Item -ItemType Directory -Path "$deployFolder\frontend\components\student" -Force | Out-Null
New-Item -ItemType Directory -Path "$deployFolder\frontend\components\admin" -Force | Out-Null
New-Item -ItemType Directory -Path "$deployFolder\frontend\services" -Force | Out-Null

Write-Host "📁 Copiando arquivos BACKEND..." -ForegroundColor Yellow

# Backend - arquivos que existem
Copy-Item "poker-academy-backend\poker_academy_api\src\routes\auth_routes.py" "$deployFolder\backend\src\routes\" -Force
Write-Host "  ✅ auth_routes.py" -ForegroundColor Green

Copy-Item "poker-academy-backend\poker_academy_api\src\models.py" "$deployFolder\backend\src\" -Force
Write-Host "  ✅ models.py" -ForegroundColor Green

Copy-Item "poker-academy-backend\poker_academy_api\src\routes\class_routes.py" "$deployFolder\backend\src\routes\" -Force
Write-Host "  ✅ class_routes.py" -ForegroundColor Green

Copy-Item "poker-academy-backend\poker_academy_api\src\main.py" "$deployFolder\backend\src\" -Force
Write-Host "  ✅ main.py" -ForegroundColor Green

Write-Host "📁 Copiando arquivos FRONTEND..." -ForegroundColor Yellow

# Frontend - arquivos que existem
Copy-Item "poker-academy\src\components\student\ChangePassword.js" "$deployFolder\frontend\components\student\" -Force
Write-Host "  ✅ ChangePassword.js (NOVO)" -ForegroundColor Green

Copy-Item "poker-academy\src\components\student\StudentPanel.js" "$deployFolder\frontend\components\student\" -Force
Write-Host "  ✅ StudentPanel.js (corrigido import)" -ForegroundColor Green

Copy-Item "poker-academy\src\services\api.js" "$deployFolder\frontend\services\" -Force
Write-Host "  ✅ api.js (adicionada função changePassword)" -ForegroundColor Green

Copy-Item "poker-academy\src\components\admin\ClassManagement.js" "$deployFolder\frontend\components\admin\" -Force
Write-Host "  ✅ ClassManagement.js (timezone + barra progresso)" -ForegroundColor Green

Copy-Item "poker-academy\src\components\student\Catalog.js" "$deployFolder\frontend\components\student\" -Force
Write-Host "  ✅ Catalog.js (timezone corrigido)" -ForegroundColor Green

Copy-Item "poker-academy\src\components\student\Favorites.js" "$deployFolder\frontend\components\student\" -Force
Write-Host "  ✅ Favorites.js (timezone corrigido)" -ForegroundColor Green

Copy-Item "poker-academy\src\components\admin\StudentManagement.js" "$deployFolder\frontend\components\admin\" -Force
Write-Host "  ✅ StudentManagement.js (timezone corrigido)" -ForegroundColor Green

# Criar arquivo de instruções detalhadas
$instructions = @"
🚀 INSTRUÇÕES COMPLETAS DE DEPLOY

📋 RESUMO DAS ALTERAÇÕES:
✅ Funcionalidade de alteração de senha para estudantes
✅ Correção de timezone nas datas (problema do -1 dia)
✅ Barra de progresso no upload de vídeos
✅ Limpeza de logs de debug

🗄️ BANCO DE DADOS:
❌ NENHUMA ALTERAÇÃO NECESSÁRIA - Usa estrutura existente

📂 ARQUIVOS PARA COPIAR:

BACKEND (copiar para /root/Dojo_Deploy/poker-academy-backend/poker_academy_api/):
- backend/src/routes/auth_routes.py → src/routes/auth_routes.py
- backend/src/models.py → src/models.py  
- backend/src/routes/class_routes.py → src/routes/class_routes.py
- backend/src/main.py → src/main.py

FRONTEND (copiar para /root/Dojo_Deploy/poker-academy/src/):
- frontend/components/student/ChangePassword.js → components/student/ChangePassword.js
- frontend/components/student/StudentPanel.js → components/student/StudentPanel.js
- frontend/services/api.js → services/api.js
- frontend/components/admin/ClassManagement.js → components/admin/ClassManagement.js
- frontend/components/student/Catalog.js → components/student/Catalog.js
- frontend/components/student/Favorites.js → components/student/Favorites.js
- frontend/components/admin/StudentManagement.js → components/admin/StudentManagement.js

🔧 COMANDOS NO SERVIDOR:

1. Fazer backup:
   cp -r /root/Dojo_Deploy/poker-academy /root/backup-$(date +%Y%m%d)
   cp -r /root/Dojo_Deploy/poker-academy-backend /root/backup-backend-$(date +%Y%m%d)

2. Parar serviços:
   cd /root/Dojo_Deploy/poker-academy-deploy
   docker-compose down

3. Copiar arquivos (use WinSCP/FileZilla)

4. Rebuild e restart:
   docker-compose build --no-cache
   docker-compose up -d

5. Verificar logs:
   docker-compose logs -f backend
   docker-compose logs -f frontend

🧪 TESTES PÓS-DEPLOY:
1. Login admin: admin@pokeracademy.com / admin123
2. Login student: student@pokeracademy.com / 123456  
3. Teste alteração senha: Menu lateral → "Alterar Senha"
4. Teste upload vídeo: Verificar barra de progresso
5. Teste datas: Verificar se aparecem corretas (sem -1 dia)

🆘 TROUBLESHOOTING:
- Se erro 500: docker-compose logs backend
- Se erro build: docker-compose build --no-cache backend
- Se erro frontend: docker-compose logs frontend
- Restart completo: docker-compose down && docker-compose up -d
"@

$instructions | Out-File -FilePath "$deployFolder\DEPLOY_INSTRUCTIONS.txt" -Encoding UTF8

Write-Host ""
Write-Host "✅ DEPLOY PREPARADO EM: $deployFolder" -ForegroundColor Green
Write-Host "📋 Leia DEPLOY_INSTRUCTIONS.txt para instruções completas" -ForegroundColor Cyan
Write-Host ""
Write-Host "🎯 PRÓXIMOS PASSOS:" -ForegroundColor Yellow
Write-Host "1. Use WinSCP ou FileZilla para conectar no servidor" -ForegroundColor White
Write-Host "2. Copie os arquivos conforme instruções" -ForegroundColor White  
Write-Host "3. Execute comandos Docker no servidor" -ForegroundColor White
Write-Host "4. Teste todas as funcionalidades" -ForegroundColor White
