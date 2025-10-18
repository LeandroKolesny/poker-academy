# Script PowerShell para baixar vídeos das aulas do servidor
# Uso: .\baixar_videos_aulas.ps1

# Configurações
$pastaDestino = "C:\Users\Usuario\Desktop\Site_Dojo_final_15_10_2025\Aula_video"
$servidorIP = "142.93.206.128"
$servidorUser = "root"
$servidorSenha = "DojoShh159357"

Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║         Download de Vídeos das Aulas - Iniciando...           ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Passo 1: Criar pasta de destino
Write-Host "1️⃣  Criando pasta de destino..." -ForegroundColor Cyan
if (-not (Test-Path $pastaDestino)) {
    New-Item -ItemType Directory -Path $pastaDestino -Force | Out-Null
    Write-Host "✅ Pasta criada: $pastaDestino" -ForegroundColor Green
} else {
    Write-Host "✅ Pasta já existe: $pastaDestino" -ForegroundColor Green
}
Write-Host ""

# Passo 2: Informar sobre os arquivos
Write-Host "2️⃣  Informações dos vídeos:" -ForegroundColor Cyan
Write-Host "   Total de arquivos: 26" -ForegroundColor Gray
Write-Host "   Tamanho total: ~5.8 GB" -ForegroundColor Gray
Write-Host "   Localização no servidor: /app/uploads/videos/" -ForegroundColor Gray
Write-Host ""

# Passo 3: Instruções para usar SCP
Write-Host "3️⃣  Instruções para baixar:" -ForegroundColor Cyan
Write-Host ""
Write-Host "   Opção 1: Usar SCP (Recomendado)" -ForegroundColor Yellow
Write-Host "   ────────────────────────────────" -ForegroundColor Yellow
Write-Host "   Execute este comando no PowerShell:" -ForegroundColor Gray
Write-Host ""
Write-Host "   scp -r ${servidorUser}@${servidorIP}:/app/uploads/videos/* `"$pastaDestino\`"" -ForegroundColor White
Write-Host ""
Write-Host "   Quando solicitado, digite a senha: $servidorSenha" -ForegroundColor Gray
Write-Host ""
Write-Host "   Opção 2: Usar Docker (Se preferir)" -ForegroundColor Yellow
Write-Host "   ──────────────────────────────────" -ForegroundColor Yellow
Write-Host "   1. Conecte ao servidor: ssh ${servidorUser}@${servidorIP}" -ForegroundColor Gray
Write-Host "   2. Execute: docker cp backend:/app/uploads/videos /tmp/videos" -ForegroundColor Gray
Write-Host "   3. Depois copie via SCP: scp -r ${servidorUser}@${servidorIP}:/tmp/videos/* `"$pastaDestino\`"" -ForegroundColor Gray
Write-Host ""

# Passo 4: Aguardar confirmação
Write-Host "4️⃣  Próximos passos:" -ForegroundColor Cyan
Write-Host "   1. Copie o comando SCP acima" -ForegroundColor Gray
Write-Host "   2. Cole no PowerShell" -ForegroundColor Gray
Write-Host "   3. Pressione Enter" -ForegroundColor Gray
Write-Host "   4. Digite a senha quando solicitado" -ForegroundColor Gray
Write-Host ""

Write-Host "5️⃣  Aguardando..." -ForegroundColor Cyan
Write-Host "   Pressione ENTER para continuar" -ForegroundColor Yellow
Read-Host

Write-Host ""

# Passo 5: Verificar se arquivos foram baixados
Write-Host "6️⃣  Verificando arquivos baixados..." -ForegroundColor Cyan
$arquivos = Get-ChildItem $pastaDestino -Recurse -ErrorAction SilentlyContinue
$totalArquivos = ($arquivos | Measure-Object).Count
$tamanhoTotal = ($arquivos | Measure-Object -Property Length -Sum).Sum / 1GB

if ($totalArquivos -gt 0) {
    Write-Host "✅ Arquivos encontrados: $totalArquivos" -ForegroundColor Green
    Write-Host "✅ Tamanho total: $([Math]::Round($tamanhoTotal, 2)) GB" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Nenhum arquivo encontrado ainda" -ForegroundColor Yellow
    Write-Host "   Verifique se o download foi iniciado" -ForegroundColor Yellow
}

Write-Host ""

# Passo 6: Listar arquivos
if ($totalArquivos -gt 0) {
    Write-Host "7️⃣  Arquivos baixados:" -ForegroundColor Cyan
    Get-ChildItem $pastaDestino -File | Select-Object Name, @{Name="Tamanho";Expression={"{0:N2} MB" -f ($_.Length/1MB)}} | Format-Table -AutoSize
}

Write-Host ""

# Passo 7: Resumo final
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║              ✅ INSTRUÇÕES FORNECIDAS COM SUCESSO!            ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-Host "📊 Resumo:" -ForegroundColor Cyan
Write-Host "   Pasta de destino: $pastaDestino" -ForegroundColor Gray
Write-Host "   Total de vídeos: 26" -ForegroundColor Gray
Write-Host "   Tamanho total: ~5.8 GB" -ForegroundColor Gray
Write-Host ""

Write-Host "🎯 Próximos passos:" -ForegroundColor Cyan
Write-Host "   1. Copie o comando SCP fornecido acima" -ForegroundColor Gray
Write-Host "   2. Cole no PowerShell" -ForegroundColor Gray
Write-Host "   3. Aguarde o download completar (pode levar alguns minutos)" -ForegroundColor Gray
Write-Host "   4. Verifique os arquivos na pasta" -ForegroundColor Gray
Write-Host ""

Write-Host "💡 Dica:" -ForegroundColor Yellow
Write-Host "   Se o download for interrompido, execute o comando novamente" -ForegroundColor Gray
Write-Host "   O SCP continuará de onde parou" -ForegroundColor Gray
Write-Host ""

