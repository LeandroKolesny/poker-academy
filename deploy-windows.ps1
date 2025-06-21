# Script de Deploy para Windows - Poker Academy
# Execute como Administrador no PowerShell

param(
    [string]$ServerIP = "10.116.0.2",
    [string]$ServerUser = "root"
)

Write-Host "🚀 Deploy do Poker Academy" -ForegroundColor Green
Write-Host "Servidor: $ServerIP" -ForegroundColor Yellow
Write-Host "Usuário: $ServerUser" -ForegroundColor Yellow

# Função para log
function Write-Log {
    param([string]$Message, [string]$Color = "Green")
    Write-Host "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $Message" -ForegroundColor $Color
}

# Verificar se SSH está disponível
function Test-SSH {
    try {
        $result = ssh -o ConnectTimeout=5 -o BatchMode=yes $ServerUser@$ServerIP "echo 'SSH OK'"
        if ($result -eq "SSH OK") {
            Write-Log "SSH conectado com sucesso ✓"
            return $true
        }
    }
    catch {
        Write-Log "Erro de SSH: $_" -Color Red
        return $false
    }
    return $false
}

# Configurar servidor
function Setup-Server {
    Write-Log "Configurando servidor..."
    
    $setupScript = @"
#!/bin/bash
set -e

echo "🔧 Configurando servidor Ubuntu..."

# Atualizar sistema
apt update && apt upgrade -y

# Instalar dependências
apt install -y curl wget git unzip software-properties-common apt-transport-https ca-certificates gnupg lsb-release ufw fail2ban htop

# Instalar Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=`$(dpkg --print-architecture)` signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu `$(lsb_release -cs)` stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Instalar Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-`$(uname -s)`-`$(uname -m)`" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose

# Configurar firewall
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 22
ufw allow 80
ufw allow 443
ufw --force enable

# Criar usuário poker
if ! id "poker" &>/dev/null; then
    useradd -m -s /bin/bash poker
    usermod -aG docker poker
fi

mkdir -p /home/poker/poker-academy
chown poker:poker /home/poker/poker-academy

systemctl enable docker
systemctl start docker

echo "✅ Servidor configurado!"
"@

    # Salvar script temporário
    $setupScript | Out-File -FilePath "temp-setup.sh" -Encoding UTF8
    
    # Enviar e executar
    scp temp-setup.sh ${ServerUser}@${ServerIP}:/tmp/setup.sh
    ssh ${ServerUser}@${ServerIP} "chmod +x /tmp/setup.sh && /tmp/setup.sh"
    
    # Limpar
    Remove-Item temp-setup.sh
    
    Write-Log "Servidor configurado ✓"
}

# Enviar arquivos
function Deploy-Files {
    Write-Log "Enviando arquivos para servidor..."
    
    # Criar arquivo tar (usando WSL se disponível, senão usar 7zip)
    if (Get-Command wsl -ErrorAction SilentlyContinue) {
        wsl tar -czf poker-academy.tar.gz --exclude='.git' --exclude='node_modules' --exclude='__pycache__' .
    } else {
        Write-Log "Criando arquivo ZIP..." -Color Yellow
        Compress-Archive -Path * -DestinationPath poker-academy.zip -Force
    }
    
    # Enviar arquivo
    if (Test-Path poker-academy.tar.gz) {
        scp poker-academy.tar.gz poker@${ServerIP}:/home/poker/
        ssh poker@${ServerIP} "cd /home/poker && tar -xzf poker-academy.tar.gz -C poker-academy && rm poker-academy.tar.gz"
        Remove-Item poker-academy.tar.gz
    } elseif (Test-Path poker-academy.zip) {
        scp poker-academy.zip poker@${ServerIP}:/home/poker/
        ssh poker@${ServerIP} "cd /home/poker && unzip -o poker-academy.zip -d poker-academy && rm poker-academy.zip"
        Remove-Item poker-academy.zip
    }
    
    Write-Log "Arquivos enviados ✓"
}

# Executar deploy
function Start-Deploy {
    Write-Log "Executando deploy..."
    
    ssh poker@${ServerIP} @"
cd /home/poker/poker-academy
cp .env.production .env
chmod +x deploy.sh
./deploy.sh production
"@
    
    Write-Log "Deploy executado ✓"
}

# Verificar deploy
function Test-Deploy {
    Write-Log "Verificando deploy..."
    
    Start-Sleep -Seconds 30
    
    try {
        $response = Invoke-WebRequest -Uri "http://${ServerIP}/api/health" -TimeoutSec 10
        if ($response.StatusCode -eq 200) {
            Write-Log "Backend funcionando ✓"
        }
    } catch {
        Write-Log "Backend ainda não está pronto" -Color Yellow
    }
    
    try {
        $response = Invoke-WebRequest -Uri "http://${ServerIP}" -TimeoutSec 10
        if ($response.StatusCode -eq 200) {
            Write-Log "Frontend funcionando ✓"
        }
    } catch {
        Write-Log "Frontend ainda não está pronto" -Color Yellow
    }
}

# Função principal
function Main {
    Write-Log "Iniciando deploy completo..."
    
    # Verificar conectividade
    if (-not (Test-Connection -ComputerName $ServerIP -Count 1 -Quiet)) {
        Write-Log "Servidor $ServerIP não está acessível" -Color Red
        return
    }
    
    # Verificar SSH
    if (-not (Test-SSH)) {
        Write-Log "Não foi possível conectar via SSH" -Color Red
        Write-Log "Certifique-se de que:" -Color Yellow
        Write-Log "1. O servidor está ligado e acessível" -Color Yellow
        Write-Log "2. SSH está habilitado no servidor" -Color Yellow
        Write-Log "3. Você tem as credenciais corretas" -Color Yellow
        return
    }
    
    # Executar deploy
    Setup-Server
    Deploy-Files
    Start-Deploy
    Test-Deploy
    
    Write-Log "🎉 Deploy concluído!" -Color Green
    Write-Log "🌐 Acesse: http://${ServerIP}" -Color Cyan
    Write-Log "🔧 API: http://${ServerIP}/api/health" -Color Cyan
}

# Executar se chamado diretamente
if ($MyInvocation.InvocationName -ne '.') {
    Main
}
