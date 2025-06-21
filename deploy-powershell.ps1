# Deploy PowerShell para Poker Academy
# Execute como Administrador

param(
    [string]$ServerIP = "142.93.206.128",
    [string]$Username = "root",
    [string]$Password = "DojoShh159357"
)

Write-Host "🚀 Deploy Poker Academy" -ForegroundColor Green
Write-Host "Servidor: $ServerIP" -ForegroundColor Yellow

# Função para executar comando SSH
function Invoke-SSHCommand {
    param(
        [string]$Command,
        [string]$Server = $ServerIP,
        [string]$User = $Username,
        [string]$Pass = $Password
    )
    
    try {
        # Usar plink se disponível (PuTTY)
        if (Get-Command plink -ErrorAction SilentlyContinue) {
            $result = & plink -ssh -batch -pw $Pass "$User@$Server" $Command
            return $result
        }
        # Usar ssh nativo do Windows 10+
        elseif (Get-Command ssh -ErrorAction SilentlyContinue) {
            Write-Host "Usando SSH nativo do Windows..." -ForegroundColor Yellow
            Write-Host "Você precisará inserir a senha manualmente" -ForegroundColor Yellow
            $result = & ssh "$User@$Server" $Command
            return $result
        }
        else {
            Write-Host "SSH não encontrado. Instale OpenSSH ou PuTTY" -ForegroundColor Red
            return $null
        }
    }
    catch {
        Write-Host "Erro SSH: $_" -ForegroundColor Red
        return $null
    }
}

# Configurar servidor
function Setup-Server {
    Write-Host "🔧 Configurando servidor..." -ForegroundColor Blue
    
    $setupCommands = @(
        "apt update",
        "apt install -y curl wget git unzip docker.io docker-compose",
        "systemctl enable docker",
        "systemctl start docker",
        "useradd -m -s /bin/bash poker || true",
        "usermod -aG docker poker",
        "mkdir -p /home/poker/poker-academy",
        "chown poker:poker /home/poker/poker-academy",
        "ufw allow 80",
        "ufw allow 443"
    )
    
    foreach ($cmd in $setupCommands) {
        Write-Host "Executando: $cmd" -ForegroundColor Gray
        Invoke-SSHCommand -Command $cmd
    }
    
    Write-Host "✅ Servidor configurado" -ForegroundColor Green
}

# Criar pacote de deploy
function Create-DeployPackage {
    Write-Host "📦 Criando pacote de deploy..." -ForegroundColor Blue
    
    $packageDir = "poker-academy-deploy"
    
    if (Test-Path $packageDir) {
        Remove-Item -Recurse -Force $packageDir
    }
    
    New-Item -ItemType Directory -Path $packageDir
    
    # Copiar arquivos essenciais
    $files = @(
        "docker-compose.yml",
        ".env.production",
        "deploy.sh",
        "Makefile"
    )
    
    foreach ($file in $files) {
        if (Test-Path $file) {
            Copy-Item $file $packageDir
            Write-Host "Copiado: $file" -ForegroundColor Gray
        }
    }
    
    # Copiar diretórios
    $dirs = @("mysql", "poker-academy-backend", "poker-academy")
    
    foreach ($dir in $dirs) {
        if (Test-Path $dir) {
            Copy-Item -Recurse $dir $packageDir
            Write-Host "Copiado: $dir" -ForegroundColor Gray
        }
    }
    
    # Criar arquivo ZIP
    if (Test-Path "poker-academy-deploy.zip") {
        Remove-Item "poker-academy-deploy.zip"
    }
    
    Compress-Archive -Path $packageDir -DestinationPath "poker-academy-deploy.zip"
    
    Write-Host "✅ Pacote criado: poker-academy-deploy.zip" -ForegroundColor Green
    
    return "poker-academy-deploy.zip"
}

# Enviar arquivos
function Send-Files {
    param([string]$PackagePath)
    
    Write-Host "📤 Enviando arquivos..." -ForegroundColor Blue
    
    # Usar pscp se disponível (PuTTY)
    if (Get-Command pscp -ErrorAction SilentlyContinue) {
        & pscp -pw $Password $PackagePath "$Username@${ServerIP}:/home/poker/"
    }
    # Usar scp nativo
    elseif (Get-Command scp -ErrorAction SilentlyContinue) {
        Write-Host "Você precisará inserir a senha manualmente" -ForegroundColor Yellow
        & scp $PackagePath "$Username@${ServerIP}:/home/poker/"
    }
    else {
        Write-Host "SCP não encontrado. Use WinSCP manualmente:" -ForegroundColor Red
        Write-Host "1. Abra WinSCP" -ForegroundColor Yellow
        Write-Host "2. Conecte em $ServerIP com usuário $Username" -ForegroundColor Yellow
        Write-Host "3. Envie o arquivo $PackagePath para /home/poker/" -ForegroundColor Yellow
        Read-Host "Pressione Enter após enviar o arquivo"
    }
    
    Write-Host "✅ Arquivos enviados" -ForegroundColor Green
}

# Executar deploy
function Start-Deploy {
    Write-Host "🚀 Executando deploy..." -ForegroundColor Blue
    
    $deployCommands = @(
        "cd /home/poker",
        "unzip -o poker-academy-deploy.zip",
        "chown -R poker:poker poker-academy-deploy",
        "su - poker -c 'cd /home/poker/poker-academy-deploy && cp .env.production .env'",
        "su - poker -c 'cd /home/poker/poker-academy-deploy && chmod +x deploy.sh'",
        "su - poker -c 'cd /home/poker/poker-academy-deploy && ./deploy.sh production'"
    )
    
    foreach ($cmd in $deployCommands) {
        Write-Host "Executando: $cmd" -ForegroundColor Gray
        Invoke-SSHCommand -Command $cmd
        Start-Sleep -Seconds 2
    }
    
    Write-Host "✅ Deploy executado" -ForegroundColor Green
}

# Verificar deploy
function Test-Deploy {
    Write-Host "🔍 Verificando deploy..." -ForegroundColor Blue
    
    Start-Sleep -Seconds 30
    
    try {
        $response = Invoke-WebRequest -Uri "http://$ServerIP" -TimeoutSec 10
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ Frontend funcionando" -ForegroundColor Green
        }
    }
    catch {
        Write-Host "⚠️ Frontend ainda não está pronto" -ForegroundColor Yellow
    }
    
    try {
        $response = Invoke-WebRequest -Uri "http://$ServerIP/api/health" -TimeoutSec 10
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ Backend funcionando" -ForegroundColor Green
        }
    }
    catch {
        Write-Host "⚠️ Backend ainda não está pronto" -ForegroundColor Yellow
    }
}

# Função principal
function Main {
    Write-Host "🎯 Iniciando deploy completo..." -ForegroundColor Cyan
    
    # Testar conectividade
    if (-not (Test-Connection -ComputerName $ServerIP -Count 1 -Quiet)) {
        Write-Host "❌ Servidor não acessível" -ForegroundColor Red
        return
    }
    
    Write-Host "✅ Servidor acessível" -ForegroundColor Green
    
    # Executar deploy
    Setup-Server
    $package = Create-DeployPackage
    Send-Files -PackagePath $package
    Start-Deploy
    Test-Deploy
    
    Write-Host ""
    Write-Host "🎉 Deploy concluído!" -ForegroundColor Green
    Write-Host "🌐 Acesse: http://$ServerIP" -ForegroundColor Cyan
    Write-Host "🔧 API: http://$ServerIP/api/health" -ForegroundColor Cyan
    
    # Limpar arquivos temporários
    if (Test-Path "poker-academy-deploy") {
        Remove-Item -Recurse -Force "poker-academy-deploy"
    }
    if (Test-Path "poker-academy-deploy.zip") {
        Remove-Item "poker-academy-deploy.zip"
    }
}

# Executar se chamado diretamente
if ($MyInvocation.InvocationName -ne '.') {
    Main
}
