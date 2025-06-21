# 🚀 INSTRUÇÕES DE DEPLOY - POKER ACADEMY

## 📋 INFORMAÇÕES DO SERVIDOR
- **IP:** 142.93.206.128
- **Usuário:** root
- **Senha:** DojoShh159357

---

## 🎯 PASSO 1: CONECTAR AO SERVIDOR

```bash
ssh root@142.93.206.128
# Senha: DojoShh159357
```

---

## 🎯 PASSO 2: CONFIGURAR SERVIDOR (Execute no servidor)

```bash
# Atualizar sistema
apt update && apt upgrade -y

# Instalar dependências
apt install -y curl wget git unzip software-properties-common apt-transport-https ca-certificates gnupg lsb-release ufw fail2ban htop

# Instalar Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Instalar Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose

# Verificar instalação
docker --version
docker-compose --version

# Configurar firewall
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 22
ufw allow 80
ufw allow 443
ufw --force enable

# Criar usuário para aplicação
useradd -m -s /bin/bash poker
usermod -aG docker poker
mkdir -p /home/poker/poker-academy
chown poker:poker /home/poker/poker-academy

# Habilitar Docker
systemctl enable docker
systemctl start docker
```

---

## 🎯 PASSO 3: ENVIAR ARQUIVOS PARA SERVIDOR

### Opção A: Usando SCP (Recomendado)
No seu computador Windows, use WinSCP ou similar para enviar os arquivos:

1. **Conecte via WinSCP:**
   - Host: 142.93.206.128
   - Usuário: root
   - Senha: DojoShh159357

2. **Envie toda a pasta do projeto para:** `/home/poker/poker-academy/`

### Opção B: Usando Git (se tiver repositório)
```bash
# No servidor
su - poker
cd /home/poker
git clone https://github.com/LeandroKolesny/poker-academy.git
```

### Opção C: Criar arquivo ZIP e enviar
1. Comprima toda a pasta do projeto
2. Envie via WinSCP para `/home/poker/poker-academy.zip`
3. No servidor:
```bash
cd /home/poker
unzip poker-academy.zip
chown -R poker:poker poker-academy/
```

---

## 🎯 PASSO 4: EXECUTAR DEPLOY (No servidor)

```bash
# Mudar para usuário poker
su - poker

# Ir para diretório da aplicação
cd /home/poker/poker-academy

# Verificar arquivos
ls -la

# Configurar ambiente
cp .env.production .env

# Dar permissão ao script
chmod +x deploy.sh

# Executar deploy
./deploy.sh production
```

---

## 🎯 PASSO 5: VERIFICAR DEPLOY

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

Após o deploy bem-sucedido:
- **Frontend:** http://142.93.206.128
- **Backend API:** http://142.93.206.128/api/health
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

# Entrar no container do backend
docker-compose exec backend bash

# Entrar no MySQL
docker-compose exec mysql mysql -u root -p poker_academy
```

---

## 🚨 TROUBLESHOOTING

### Se der erro de permissão:
```bash
sudo chown -R poker:poker /home/poker/poker-academy
sudo chmod +x /home/poker/poker-academy/deploy.sh
```

### Se MySQL não iniciar:
```bash
docker-compose logs mysql
docker-compose restart mysql
```

### Se backend não conectar ao MySQL:
```bash
docker-compose logs backend
# Aguarde o MySQL estar totalmente pronto antes de iniciar o backend
```

### Se frontend não carregar:
```bash
docker-compose logs frontend
# Verifique se o build do React foi bem-sucedido
```

### Reset completo se necessário:
```bash
docker-compose down
docker system prune -f
docker-compose up -d
```

---

## 📞 PRÓXIMOS PASSOS

1. **Execute os comandos acima na ordem**
2. **Se encontrar erro, me envie os logs**
3. **Teste a aplicação no navegador**
4. **Configure domínio (opcional)**

---

## 🎉 SUCESSO!

Se tudo funcionou, você terá:
- ✅ Aplicação rodando em Docker
- ✅ Frontend React acessível
- ✅ Backend Flask funcionando
- ✅ MySQL configurado
- ✅ NGINX como proxy reverso
- ✅ Firewall configurado

**Sua aplicação estará no ar em http://142.93.206.128** 🚀
