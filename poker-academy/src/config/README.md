# 🔧 Sistema de Configuração Centralizada

Este sistema permite gerenciar URLs e configurações de forma centralizada, facilitando o deploy entre diferentes ambientes.

## 📁 Estrutura dos Arquivos

```
src/config/
├── config.js          # Configuração principal (auto-detecta ambiente)
├── config.local.js     # Configuração específica para desenvolvimento local
├── config.server.js    # Configuração específica para servidor de produção
└── README.md          # Este arquivo
```

## 🎯 Como Usar

### 1. Importar a Configuração

```javascript
// Importar configuração principal
import config, { buildApiUrl, buildVideoUrl } from '../config/config';

// Usar URLs da configuração
const API_BASE_URL = config.API_BASE_URL;
const videoUrl = buildVideoUrl('video.mp4', token);
```

### 2. Usar Endpoints Pré-definidos

```javascript
// Em vez de hardcoded URLs
const response = await fetch('http://localhost:5000/api/classes');

// Use endpoints da configuração
const response = await fetch(buildApiUrl(config.API_ENDPOINTS.CLASSES));
```

### 3. Detecção Automática de Ambiente

O sistema detecta automaticamente o ambiente baseado no hostname:

- **localhost/127.0.0.1** → `development` (config.local.js)
- **142.93.206.128** → `production` (config.server.js)  
- **grinders.com.br** → `server` (configuração de domínio)

## 🔄 Mudança Manual de Ambiente

Para forçar um ambiente específico, defina a variável de ambiente:

```bash
# No .env ou variável de ambiente
REACT_APP_ENV=production
```

## 🛠️ Configurações Disponíveis

### URLs Base
- `API_BASE_URL` - URL base da API
- `FRONTEND_URL` - URL base do frontend
- `WEBSOCKET_URL` - URL base para WebSockets

### Configurações de Upload
- `UPLOAD.MAX_FILE_SIZE` - Tamanho máximo de arquivo
- `UPLOAD.ALLOWED_VIDEO_FORMATS` - Formatos permitidos
- `UPLOAD.CHUNK_SIZE` - Tamanho dos chunks

### Configurações de Autenticação
- `AUTH.TOKEN_REFRESH_INTERVAL` - Intervalo de refresh do token
- `AUTH.SESSION_TIMEOUT` - Timeout da sessão

### Endpoints da API
- `API_ENDPOINTS.LOGIN` - Endpoint de login
- `API_ENDPOINTS.CLASSES` - Endpoint de classes
- `API_ENDPOINTS.UPLOAD_COMPLETE` - Endpoint de upload
- E muitos outros...

## 🔍 Debug

Para ver a configuração atual:

```javascript
import { debugConfig } from '../config/config';

// Mostrar configuração no console
debugConfig();
```

## 📝 Exemplo Prático

### Antes (URLs hardcoded):
```javascript
const response = await fetch('http://localhost:5000/api/classes');
const videoUrl = `http://localhost:5000/api/videos/${path}?token=${token}`;
```

### Depois (configuração centralizada):
```javascript
import config, { buildApiUrl, buildVideoUrl } from '../config/config';

const response = await fetch(buildApiUrl(config.API_ENDPOINTS.CLASSES));
const videoUrl = buildVideoUrl(path, token);
```

## 🚀 Vantagens

1. **Centralização** - Todas as URLs em um lugar
2. **Detecção Automática** - Ambiente detectado automaticamente
3. **Fácil Deploy** - Sem necessidade de alterar código
4. **Manutenibilidade** - Mudanças em um só lugar
5. **Flexibilidade** - Configurações específicas por ambiente

## 🔧 Personalização

Para adicionar novas configurações, edite os arquivos:

- `config.js` - Configuração geral
- `config.local.js` - Específico para desenvolvimento
- `config.server.js` - Específico para produção
