# 🚀 GUIA DE DEPLOY - ALTERAÇÕES DE SENHA E CORREÇÕES

## 📋 ARQUIVOS PARA COPIAR PARA O SERVIDOR

### 🔧 BACKEND (Flask) - Copiar para `/root/Dojo_Deploy/poker-academy-backend/poker_academy_api/`

1. **src/routes/auth_routes.py** - Rota de alteração de senha
2. **src/models.py** - Correções de timezone
3. **src/routes/class_routes.py** - Correções de timezone
4. **src/main.py** - Correções de imports

### ⚛️ FRONTEND (React) - Copiar para `/root/Dojo_Deploy/poker-academy/src/`

1. **components/student/ChangePassword.js** - NOVO ARQUIVO
2. **components/student/StudentDashboard.js** - Link para alteração de senha
3. **services/authService.js** - Função changePassword
4. **components/admin/ClassManagement.js** - Correções de timezone e barra de progresso
5. **components/student/Catalog.js** - Correções de timezone
6. **components/student/Favorites.js** - Correções de timezone
7. **components/admin/StudentManagement.js** - Correções de timezone

## 🗄️ BANCO DE DADOS
**✅ NENHUMA ALTERAÇÃO NECESSÁRIA** - Usamos estrutura existente

## 📝 COMANDOS PARA EXECUTAR NO SERVIDOR

### 1. Parar serviços
```bash
cd /root/Dojo_Deploy/poker-academy-deploy
docker-compose down
```

### 2. Copiar arquivos (via SCP ou FileZilla)
- Copie os arquivos listados acima para seus respectivos diretórios

### 3. Rebuild e restart
```bash
cd /root/Dojo_Deploy/poker-academy-deploy
docker-compose build --no-cache
docker-compose up -d
```

### 4. Verificar logs
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

## 🔍 VERIFICAÇÕES PÓS-DEPLOY

1. **Teste login:** admin@pokeracademy.com / admin123
2. **Teste alteração de senha:** student@pokeracademy.com / 123456
3. **Teste upload de vídeo:** Verificar barra de progresso
4. **Teste datas:** Verificar se aparecem corretas na tabela

## 📦 ALTERNATIVA: USAR RSYNC (se disponível)

```bash
# Do seu PC para o servidor
rsync -avz --exclude node_modules --exclude venv ./poker-academy/ root@SEU_IP:/root/Dojo_Deploy/poker-academy/
rsync -avz --exclude venv ./poker-academy-backend/ root@SEU_IP:/root/Dojo_Deploy/poker-academy-backend/
```

## 🆘 EM CASO DE PROBLEMAS

1. **Verificar logs:** `docker-compose logs backend`
2. **Verificar build:** `docker-compose build backend --no-cache`
3. **Verificar permissões:** `chmod -R 755 /root/Dojo_Deploy/`
4. **Restart completo:** `docker-compose down && docker-compose up -d`
