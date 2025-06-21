# 📋 LISTA COMPLETA DE ARQUIVOS ALTERADOS

## 🔧 BACKEND (Flask) - Copiar para `/root/Dojo_Deploy/poker-academy-backend/poker_academy_api/`

### ✅ Arquivos que EXISTEM e foram ALTERADOS:
1. **src/routes/auth_routes.py** - Adicionada rota `/api/auth/change-password`
2. **src/models.py** - Correção de timezone na formatação de data
3. **src/routes/class_routes.py** - Correção de timezone e logs removidos
4. **src/main.py** - Correção de imports datetime

## ⚛️ FRONTEND (React) - Copiar para `/root/Dojo_Deploy/poker-academy/src/`

### ✅ Arquivos que EXISTEM e foram ALTERADOS:
1. **components/admin/ClassManagement.js** - Correção timezone + barra progresso
2. **components/student/Catalog.js** - Correção timezone na exibição
3. **components/student/Favorites.js** - Correção timezone na exibição  
4. **components/admin/StudentManagement.js** - Correção timezone na exibição

### ❌ Arquivos que PRECISAM SER CRIADOS:
1. **components/student/ChangePassword.js** - NOVO ARQUIVO (componente alteração senha)
2. **Modificação em components/student/StudentDashboard.js** - Adicionar link para alteração senha
3. **Modificação em services/authService.js** - Adicionar função changePassword

## 🗄️ BANCO DE DADOS
**✅ NENHUMA ALTERAÇÃO NECESSÁRIA** - Usamos estrutura existente da tabela `users`

## 📝 COMANDOS PARA DEPLOY NO SERVIDOR

### 1. Parar serviços
```bash
cd /root/Dojo_Deploy/poker-academy-deploy
docker-compose down
```

### 2. Fazer backup (recomendado)
```bash
cp -r /root/Dojo_Deploy/poker-academy /root/Dojo_Deploy/poker-academy-backup-$(date +%Y%m%d)
cp -r /root/Dojo_Deploy/poker-academy-backend /root/Dojo_Deploy/poker-academy-backend-backup-$(date +%Y%m%d)
```

### 3. Copiar arquivos alterados
- Use WinSCP, FileZilla ou comando `scp`
- Copie os arquivos listados acima para seus respectivos diretórios

### 4. Rebuild e restart
```bash
cd /root/Dojo_Deploy/poker-academy-deploy
docker-compose build --no-cache
docker-compose up -d
```

### 5. Verificar logs
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

## 🧪 TESTES PÓS-DEPLOY

1. **Login admin:** admin@pokeracademy.com / admin123
2. **Login student:** student@pokeracademy.com / 123456
3. **Teste alteração senha:** Ir em perfil → alterar senha
4. **Teste upload vídeo:** Verificar barra de progresso
5. **Teste datas:** Verificar se datas aparecem corretas (sem -1 dia)

## 🚨 ARQUIVOS CRÍTICOS QUE PRECISAM SER CRIADOS

### 1. ChangePassword.js
- Localização: `/root/Dojo_Deploy/poker-academy/src/components/student/ChangePassword.js`
- Função: Componente para alteração de senha do estudante

### 2. Modificações em StudentDashboard.js
- Adicionar link/botão para acessar alteração de senha

### 3. Modificações em authService.js  
- Adicionar função `changePassword` para comunicar com API

## 💡 DICA: USAR GIT (RECOMENDADO)

Se instalar Git:
```bash
git init
git add .
git commit -m "Funcionalidade alteração senha + correções timezone"
git remote add origin SEU_REPOSITORIO
git push origin main
```

No servidor:
```bash
git pull origin main
docker-compose build --no-cache
docker-compose up -d
```
