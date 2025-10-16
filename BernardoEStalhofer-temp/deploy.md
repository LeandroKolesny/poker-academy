# 🚀 Guia de Deploy - Sistema Bernardo & Stahlhöfer

## 📋 Pré-requisitos

1. ✅ Conta no GitHub (leroots919)
2. ✅ Repositório: https://github.com/leroots919/BernardoEStalhofer
3. ✅ Conta no Railway (railway.app)
4. ✅ Conta no Vercel (vercel.com)

## 🔄 Passos para Deploy

### 1. Preparar Repositório GitHub

```bash
# Navegar para o diretório do projeto
cd C:\Users\Usuario\Desktop\BernardoEStalhofer

# Verificar se é repositório git
git status

# Se não for, inicializar
git init

# Adicionar remote (VERIFICAR URL)
git remote add origin https://github.com/leroots919/BernardoEStalhofer.git

# Verificar remote
git remote -v

# Adicionar arquivos
git add .

# Commit
git commit -m "Sistema completo: Frontend React + Backend FastAPI"

# Push
git push -u origin main
```

### 2. Deploy Backend no Railway

1. **Acessar:** https://railway.app
2. **Login** com GitHub
3. **New Project** → **Deploy from GitHub repo**
4. **Selecionar:** leroots919/BernardoEStalhofer
5. **Configurar variáveis:**
   ```
   DATABASE_URL=mysql://user:pass@host:port/BS
   JWT_SECRET_KEY=seu-jwt-secret-aqui
   PORT=8000
   ```
6. **Deploy automático**

### 3. Deploy Frontend no Vercel

1. **Acessar:** https://vercel.com
2. **Login** com GitHub
3. **New Project** → **Import Git Repository**
4. **Selecionar:** leroots919/BernardoEStalhofer
5. **Root Directory:** `advBS`
6. **Build Command:** `npm run build`
7. **Output Directory:** `build`
8. **Deploy**

### 4. Configurar Domínio (Opcional)

#### Freenom (Gratuito)
1. **Acessar:** https://freenom.com
2. **Registrar:** bernardostahlhofer.tk
3. **DNS:** Apontar para Railway/Vercel

## 🌐 URLs Finais

- **Frontend:** https://bernardostahlhofer.vercel.app
- **Backend:** https://bernardoestahlhofer-production.up.railway.app
- **Admin:** https://bernardostahlhofer.vercel.app/admin/login

## 🔑 Credenciais de Teste

- **Admin:** admin / admin123
- **Cliente:** Criar via painel admin

## ⚠️ Importante

1. **Backup** do banco antes do deploy
2. **Testar** todas as funcionalidades
3. **Configurar CORS** no backend
4. **Verificar** variáveis de ambiente