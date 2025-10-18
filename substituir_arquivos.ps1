# Script PowerShell para substituir arquivos do servidor
# Uso: .\substituir_arquivos.ps1

# Configurações
$pastaOrigem = "C:\Users\Usuario\Desktop\site_Dojo2_temp"
$pastaDestino = "C:\Users\Usuario\Desktop\site_Dojo2"
$dataBackup = Get-Date -Format "yyyyMMdd_HHmmss"
$pastaBackup = "C:\Users\Usuario\Desktop\site_Dojo2_backup_$dataBackup"

Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║         Substituição de Arquivos do Servidor                  ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Verificar se pasta de origem existe
if (-not (Test-Path $pastaOrigem)) {
    Write-Host "❌ Erro: Pasta de origem não encontrada!" -ForegroundColor Red
    Write-Host "   Caminho: $pastaOrigem" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Pasta de origem encontrada: $pastaOrigem" -ForegroundColor Green
Write-Host ""

# Verificar se pasta de destino existe
if (-not (Test-Path $pastaDestino)) {
    Write-Host "⚠️  Pasta de destino não existe. Criando..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $pastaDestino -Force | Out-Null
    Write-Host "✅ Pasta criada: $pastaDestino" -ForegroundColor Green
} else {
    Write-Host "✅ Pasta de destino encontrada: $pastaDestino" -ForegroundColor Green
}

Write-Host ""

# Fazer backup
Write-Host "1️⃣  Fazendo backup dos arquivos antigos..." -ForegroundColor Cyan
Write-Host "   Destino: $pastaBackup" -ForegroundColor Gray

if ((Get-ChildItem $pastaDestino -ErrorAction SilentlyContinue | Measure-Object).Count -gt 0) {
    Copy-Item $pastaDestino $pastaBackup -Recurse -Force
    Write-Host "✅ Backup realizado com sucesso!" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Pasta de destino vazia, nenhum backup necessário" -ForegroundColor Yellow
}

Write-Host ""

# Limpar pasta de destino
Write-Host "2️⃣  Limpando pasta de destino..." -ForegroundColor Cyan
Get-ChildItem $pastaDestino -Recurse -Force | Remove-Item -Force -ErrorAction SilentlyContinue
Write-Host "✅ Pasta limpa!" -ForegroundColor Green

Write-Host ""

# Copiar novos arquivos
Write-Host "3️⃣  Copiando novos arquivos..." -ForegroundColor Cyan
Copy-Item "$pastaOrigem\*" $pastaDestino -Recurse -Force
Write-Host "✅ Arquivos copiados com sucesso!" -ForegroundColor Green

Write-Host ""

# Verificar
Write-Host "4️⃣  Verificando arquivos..." -ForegroundColor Cyan
$arquivos = Get-ChildItem $pastaDestino -Recurse | Measure-Object
$tamanho = (Get-ChildItem $pastaDestino -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB

Write-Host "   Total de arquivos: $($arquivos.Count)" -ForegroundColor Gray
Write-Host "   Tamanho total: $([Math]::Round($tamanho, 2)) MB" -ForegroundColor Gray
Write-Host "✅ Verificação concluída!" -ForegroundColor Green

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║              ✅ SUBSTITUIÇÃO CONCLUÍDA COM SUCESSO!           ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Green

Write-Host ""
Write-Host "📋 Resumo:" -ForegroundColor Cyan
Write-Host "   Pasta de origem:  $pastaOrigem" -ForegroundColor Gray
Write-Host "   Pasta de destino: $pastaDestino" -ForegroundColor Gray
Write-Host "   Backup realizado: $pastaBackup" -ForegroundColor Gray
Write-Host "   Arquivos: $($arquivos.Count)" -ForegroundColor Gray
Write-Host "   Tamanho: $([Math]::Round($tamanho, 2)) MB" -ForegroundColor Gray

Write-Host ""
Write-Host "🎉 Pronto! Os arquivos foram substituídos com sucesso!" -ForegroundColor Green

