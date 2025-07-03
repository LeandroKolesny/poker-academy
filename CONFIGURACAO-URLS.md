# 🔧 Sistema de Configuração de URLs Centralizada

## 🎯 Problema Resolvido

Antes, as URLs estavam espalhadas por vários arquivos:
- `src/services/api.js` - `http://localhost:5000`
- `src/context/AuthContext.js` - `http://localhost:5000`
- `src/components/shared/VideoPlayer.js` - `http://localhost:5000`
- `src/components/admin/StudentManagement.js` - `http://localhost:5000`
- `src/components/admin/ClassManagement.js` - `http://localhost:5000`

**Agora tudo está centralizado em um só lugar!** ✅

## 📁 Arquivos Criados

```
poker-academy/src/config/
├── config.js          # ⭐ Configuração principal (auto-detecta ambiente)
├── config.local.js     # 🏠 Configuração para desenvolvimento local
├── config.server.js    # 🌐 Configuração para servidor de produção
└── README.md          # 📖 Documentação detalhada

switch-environment.js   # 🔄 Script para alternar ambientes
CONFIGURACAO-URLS.md   # 📋 Este arquivo de instruções
```

## 🚀 Como Usar

### 1. Para Desenvolvimento Local

```bash
# Método 1: Usar script npm
npm run dev

# Método 2: Alternar manualmente
npm run env:local
npm start

# Método 3: Usar script direto
node switch-environment.js local
```

### 2. Para Deploy no Servidor

```bash
# Método 1: Build para servidor
npm run build:server

# Método 2: Alternar manualmente
npm run env:server
npm run build

# Método 3: Usar script direto
node switch-environment.js server
npm run build
```

### 3. Verificar Ambiente Atual

```bash
# Ver qual ambiente está ativo
npm run env:status

# Ou usar script direto
node switch-environment.js status
```

## 🔍 Detecção Automática

O sistema detecta automaticamente o ambiente baseado no hostname:

| Hostname | Ambiente | Configuração |
|----------|----------|--------------|
| `localhost` | Development | `http://localhost:5000` |
| `127.0.0.1` | Development | `http://localhost:5000` |
| `142.93.206.128` | Production | `http://142.93.206.128:5000` |
| `grinders.com.br` | Server | `https://grinders.com.br` |

## 📋 Comandos Disponíveis

```bash
# Scripts npm (recomendado)
npm run env:local      # Alternar para desenvolvimento
npm run env:server     # Alternar para servidor
npm run env:status     # Ver ambiente atual
npm run dev           # Desenvolvimento (local + start)
npm run build:server  # Build para servidor

# Scripts diretos
node switch-environment.js local    # Alternar para local
node switch-environment.js server   # Alternar para servidor
node switch-environment.js status   # Ver status
node switch-environment.js help     # Ajuda
```

## 🔧 Configurações Incluídas

### URLs Base
- `API_BASE_URL` - URL da API backend
- `FRONTEND_URL` - URL do frontend
- `WEBSOCKET_URL` - URL para WebSockets

### Upload
- `MAX_FILE_SIZE` - Tamanho máximo (1GB produção, 500MB dev)
- `ALLOWED_VIDEO_FORMATS` - Formatos permitidos
- `CHUNK_SIZE` - Tamanho dos chunks

### Autenticação
- `TOKEN_REFRESH_INTERVAL` - Intervalo de refresh
- `SESSION_TIMEOUT` - Timeout da sessão

### UI
- `ITEMS_PER_PAGE` - Itens por página
- `SEARCH_DEBOUNCE` - Delay da busca
- `NOTIFICATION_TIMEOUT` - Tempo das notificações

## 🎯 Vantagens

1. **✅ Centralização** - Todas as URLs em um lugar
2. **✅ Detecção Automática** - Ambiente detectado pelo hostname
3. **✅ Fácil Deploy** - Sem necessidade de editar código
4. **✅ Scripts Automatizados** - Comandos npm prontos
5. **✅ Backup Automático** - Backups criados automaticamente
6. **✅ Manutenibilidade** - Mudanças em um só lugar

## 🔄 Workflow de Deploy

### Desenvolvimento Local
```bash
# 1. Configurar para local
npm run env:local

# 2. Iniciar desenvolvimento
npm start

# ✅ Pronto! API: http://localhost:5000
```

### Deploy para Servidor
```bash
# 1. Configurar para servidor
npm run env:server

# 2. Fazer build
npm run build

# 3. Copiar pasta build/ para servidor
# ✅ Pronto! API: http://142.93.206.128:5000
```

## 🛠️ Personalização

Para adicionar novas URLs ou configurações:

1. **Edite `poker-academy/src/config/config.js`**
2. **Adicione novos endpoints em `API_ENDPOINTS`**
3. **Use `buildApiUrl()` nos componentes**

Exemplo:
```javascript
// Adicionar novo endpoint
API_ENDPOINTS: {
  NEW_FEATURE: '/api/new-feature',
}

// Usar no componente
import config, { buildApiUrl } from '../config/config';
const response = await fetch(buildApiUrl(config.API_ENDPOINTS.NEW_FEATURE));
```

## 🔍 Debug

Para ver a configuração atual no console:

```javascript
import { debugConfig } from '../config/config';
debugConfig(); // Mostra configuração completa
```

## 📝 Arquivos Modificados

Todos esses arquivos foram atualizados para usar a configuração centralizada:

- ✅ `src/services/api.js`
- ✅ `src/context/AuthContext.js`
- ✅ `src/components/shared/VideoPlayer.js`
- ✅ `src/components/admin/StudentManagement.js`
- ✅ `src/components/admin/ClassManagement.js`
- ✅ `package.json` (novos scripts)

## 🎉 Resultado

**Antes:** 5+ arquivos com URLs hardcoded
**Depois:** 1 arquivo de configuração centralizada

**Antes:** Editar manualmente cada arquivo para deploy
**Depois:** 1 comando para alternar ambiente

**Antes:** Risco de esquecer URLs
**Depois:** Detecção automática + scripts automatizados

---

🚀 **Agora você pode fazer deploy facilmente sem se preocupar com URLs!**
