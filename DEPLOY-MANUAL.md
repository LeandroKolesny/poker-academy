# 🚀 GUIA COMPLETO DE DEPLOY - POKER ACADEMY

## 📋 INFORMAÇÕES DO PROJETO
- **Servidor:** 10.116.0.2
- **GitHub:** LeandroKolesny/poker-academy
- **Stack:** Flask + React + MySQL + Docker + NGINX

---

## 🎯 PASSO 1: CRIAR REPOSITÓRIO NO GITHUB

1. **Acesse:** https://github.com/new
2. **Nome:** `poker-academy`
3. **Descrição:** `Poker Academy - Sistema de gestão com Flask + React + Docker`
4. **Público** ✅
5. **NÃO marque** "Add a README file"
6. **Clique em "Create repository"**

---

## 🎯 PASSO 2: SUBIR CÓDIGO PARA GITHUB

### Opção A: Usando Git Bash/Terminal
```bash
# Configurar Git
git config user.name "leandro"
git config user.email "lekolesny@hotmail.com"

# Inicializar repositório
git init
git add .
git commit -m "Initial commit - Poker Academy with Docker setup"
git branch -M main

# Adicionar remote e push
git remote add origin https://github.com/LeandroKolesny/poker-academy.git
git push -u origin main
```

### Opção B: Usando o arquivo git-setup.bat
1. **Execute:** `git-setup.bat`
2. **Siga as instruções**

---

## 🎯 PASSO 3: CONECTAR AO SERVIDOR

### Verificar IP do Servidor
O IP `10.116.0.2` parece ser interno. Verifique:
- Se é o IP público correto
- Se você está na mesma rede
- Se precisa de VPN para acessar

### Conectar via SSH
```bash
ssh root@10.116.0.2
```

**Se não conseguir conectar:**
- Verifique se o SSH está habilitado
- Confirme o IP correto
- Verifique se há firewall bloqueando

---

## 🎯 PASSO 4: CONFIGURAR SERVIDOR (Execute no servidor)

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependências
sudo apt install -y curl wget git unzip software-properties-common apt-transport-https ca-certificates gnupg lsb-release ufw fail2ban htop

# Instalar Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose

# Configurar firewall
sudo ufw --force reset
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw --force enable

# Criar usuário para aplicação
sudo useradd -m -s /bin/bash poker
sudo usermod -aG docker poker
sudo mkdir -p /home/poker/poker-academy
sudo chown poker:poker /home/poker/poker-academy

# Habilitar Docker
sudo systemctl enable docker
sudo systemctl start docker
```

---

## 🎯 PASSO 5: CLONAR REPOSITÓRIO NO SERVIDOR

```bash
# Mudar para usuário poker
sudo su - poker

# Clonar repositório
cd /home/poker
git clone https://github.com/LeandroKolesny/poker-academy.git
cd poker-academy

# Verificar arquivos
ls -la
```

---

## 🎯 PASSO 6: CONFIGURAR AMBIENTE

```bash
# Copiar arquivo de produção
cp .env.production .env

# Editar se necessário (opcional)
nano .env
```

---

## 🎯 PASSO 7: EXECUTAR DEPLOY

```bash
# Dar permissão ao script
chmod +x deploy.sh

# Executar deploy
./deploy.sh production
```

**O script irá:**
1. ✅ Verificar Docker
2. ✅ Construir imagens
3. ✅ Iniciar MySQL
4. ✅ Iniciar Backend
5. ✅ Iniciar Frontend
6. ✅ Verificar saúde dos serviços

---

## 🎯 PASSO 8: VERIFICAR DEPLOY

```bash
# Ver status dos containers
docker-compose ps

# Ver logs
docker-compose logs -f

# Testar serviços
curl http://localhost/api/health
curl http://localhost
```

---

## 🌐 ACESSAR APLICAÇÃO

- **Frontend:** http://10.116.0.2
- **Backend API:** http://10.116.0.2/api/health
- **Login Admin:** admin@pokeracademy.com / 123456

---

## 🔧 COMANDOS ÚTEIS

```bash
# Ver logs em tempo real
docker-compose logs -f

# Reiniciar serviços
docker-compose restart

# Parar serviços
docker-compose down

# Ver uso de recursos
docker stats

# Backup do banco
docker-compose exec mysql mysqldump -u root -p poker_academy > backup.sql

# Atualizar aplicação
git pull
docker-compose build
docker-compose up -d
```

---

## 🚨 TROUBLESHOOTING

### Se algo der errado:

1. **Ver logs detalhados:**
```bash
docker-compose logs backend
docker-compose logs frontend
docker-compose logs mysql
```

2. **Reiniciar serviço específico:**
```bash
docker-compose restart backend
```

3. **Reset completo:**
```bash
docker-compose down
docker system prune -f
docker-compose up -d
```

4. **Verificar portas:**
```bash
netstat -tlnp | grep :80
netstat -tlnp | grep :5000
netstat -tlnp | grep :3306
```

---

## 📞 SUPORTE

Se encontrar problemas:
1. Verifique os logs: `docker-compose logs -f`
2. Confirme se todas as portas estão abertas
3. Verifique se o MySQL está rodando
4. Teste a conectividade de rede

---

## 🎉 SUCESSO!

Se tudo funcionou:
- ✅ Aplicação rodando em Docker
- ✅ Frontend acessível
- ✅ Backend funcionando
- ✅ Banco de dados conectado
- ✅ NGINX configurado
- ✅ Firewall protegendo

**Sua aplicação está no ar! 🚀**
