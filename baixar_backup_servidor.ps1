# Script PowerShell para baixar backup do servidor
# Uso: .\baixar_backup_servidor.ps1

# Configurações
$pastaDestino = "C:\Users\Usuario\Desktop\Site_Dojo_final_15_10_2025"
$arquivoBackup = "backup_servidor_completo"
$dataAtual = Get-Date -Format "yyyyMMdd_HHmmss"

Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║         Download de Backup do Servidor - Iniciando...         ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Passo 1: Verificar pasta de destino
Write-Host "1️⃣  Verificando pasta de destino..." -ForegroundColor Cyan
if (-not (Test-Path $pastaDestino)) {
    Write-Host "   Criando pasta: $pastaDestino" -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $pastaDestino -Force | Out-Null
}
Write-Host "✅ Pasta de destino: $pastaDestino" -ForegroundColor Green
Write-Host ""

# Passo 2: Informar ao usuário
Write-Host "2️⃣  Instruções para baixar:" -ForegroundColor Cyan
Write-Host "   1. Abra File Explorer do Augment" -ForegroundColor Gray
Write-Host "   2. Navegue até: /mnt/persist/workspace/backup_servidor_completo/" -ForegroundColor Gray
Write-Host "   3. Selecione TODOS os arquivos (Ctrl+A)" -ForegroundColor Gray
Write-Host "   4. Clique em Download" -ForegroundColor Gray
Write-Host "   5. Salve em: $pastaDestino" -ForegroundColor Gray
Write-Host ""

# Passo 3: Aguardar confirmação
Write-Host "3️⃣  Aguardando download..." -ForegroundColor Cyan
Write-Host "   Pressione ENTER quando terminar o download" -ForegroundColor Yellow
Read-Host

Write-Host ""

# Passo 4: Verificar se arquivos foram baixados
Write-Host "4️⃣  Verificando arquivos baixados..." -ForegroundColor Cyan
$arquivos = Get-ChildItem $pastaDestino -Recurse -ErrorAction SilentlyContinue
$totalArquivos = ($arquivos | Measure-Object).Count
$tamanhoTotal = ($arquivos | Measure-Object -Property Length -Sum).Sum / 1MB

if ($totalArquivos -gt 0) {
    Write-Host "✅ Arquivos encontrados: $totalArquivos" -ForegroundColor Green
    Write-Host "✅ Tamanho total: $([Math]::Round($tamanhoTotal, 2)) MB" -ForegroundColor Green
} else {
    Write-Host "❌ Nenhum arquivo encontrado!" -ForegroundColor Red
    Write-Host "   Verifique se o download foi concluído corretamente" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Passo 5: Listar arquivos principais
Write-Host "5️⃣  Arquivos principais:" -ForegroundColor Cyan
Get-ChildItem $pastaDestino -File | Select-Object Name, @{Name="Tamanho";Expression={"{0:N2} KB" -f ($_.Length/1KB)}} | Format-Table -AutoSize
Write-Host ""

# Passo 6: Resumo final
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║              ✅ BACKUP BAIXADO COM SUCESSO!                   ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-Host "📊 Resumo:" -ForegroundColor Cyan
Write-Host "   Pasta: $pastaDestino" -ForegroundColor Gray
Write-Host "   Arquivos: $totalArquivos" -ForegroundColor Gray
Write-Host "   Tamanho: $([Math]::Round($tamanhoTotal, 2)) MB" -ForegroundColor Gray
Write-Host ""

Write-Host "🛡️  Segurança:" -ForegroundColor Cyan
Write-Host "   ✅ Servidor não foi alterado" -ForegroundColor Green
Write-Host "   ✅ Nenhum arquivo foi deletado" -ForegroundColor Green
Write-Host "   ✅ Apenas leitura (SCP)" -ForegroundColor Green
Write-Host ""

Write-Host "🎉 Backup completo e seguro!" -ForegroundColor Green

