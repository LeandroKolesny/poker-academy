# 🔧 Solução para Problemas de Cache do Docker

## 📋 Problema Identificado

O sistema estava tendo problemas com cache em múltiplas camadas:

1. **Nginx Cache**: Arquivos `.js` e `.css` eram cacheados por **1 ano** (`expires 1y`)
2. **Cloudflare Cache**: Cacheava a resposta HTML antiga que apontava para arquivos antigos
3. **Browser Cache**: Navegador cacheava os arquivos por 1 ano
4. **Falta de Versionamento**: Não havia forma de forçar atualização

## 🎯 Solução Implementada

### 1. Configuração Melhorada do Nginx (`nginx.conf`)

```nginx
# HTML - SEM CACHE (sempre buscar versão nova)
location ~* \.html?$ {
    add_header Cache-Control "no-cache, no-store, must-revalidate, max-age=0";
}

# JavaScript e CSS com hash - CACHE LONGO
location ~* \.(js|css)$ {
    # Se tem hash no nome (ex: main.e6eebbe9.js), cache por 1 ano
    if ($request_filename ~* \.[a-f0-9]{8}\.(js|css)$) {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    # Sem hash, sem cache
    else {
        add_header Cache-Control "no-cache, no-store, must-revalidate, max-age=0";
    }
}
```

**Benefícios:**
- ✅ HTML sempre atualizado (sem cache)
- ✅ Arquivos com hash podem ser cacheados (React gera hashes únicos)
- ✅ Quando há mudanças, React gera novo hash → novo arquivo → sem conflito de cache

### 2. Script de Deploy Automático (`deploy.sh`)

```bash
./deploy.sh
```

**O que faz:**
1. Cria backup do build anterior
2. Copia novo build para o servidor
3. Limpa cache do Nginx
4. Recarrega Nginx
5. Verifica se novo arquivo está sendo servido
6. Verifica se novo texto está no build

### 3. Backup Completo Realizado

Todos os dados foram salvos em `/root/backups/`:

- `database_backup_*.sql` - Banco de dados MySQL
- `mysql_volume_backup_*.tar.gz` - Volume do MySQL
- `poker_academy_config_*.tar.gz` - Configuração e código
- `uploads_volume_backup_*.tar.gz` - Arquivos de upload

**Cópias locais em:** `/mnt/persist/workspace/backups/`

## 🚀 Como Usar

### Deploy Automático (Recomendado)

```bash
cd /mnt/persist/workspace
chmod +x poker-academy/deploy.sh
./poker-academy/deploy.sh
```

### Deploy Manual

```bash
# 1. Fazer build
cd poker-academy
npm run build

# 2. Copiar para servidor
sshpass -p "DojoShh159357" scp -r build/* root@142.93.206.128:/root/Dojo_Deploy/poker-academy/poker-academy/build/

# 3. Limpar cache
sshpass -p "DojoShh159357" ssh -o StrictHostKeyChecking=no root@142.93.206.128 \
    "docker exec poker_frontend rm -rf /var/cache/nginx/* && \
     docker exec poker_frontend nginx -s reload"

# 4. Limpar cache do Cloudflare (manual)
# Acesse: https://dash.cloudflare.com
# Caching → Purge Cache → Purge Everything
```

## 🔍 Verificação

### Verificar se novo build está sendo servido

```bash
curl -s https://cardroomgrinders.com.br/admin/classes | grep -o 'main\.[a-z0-9]*\.js'
```

### Verificar se novo texto está no arquivo

```bash
curl -s https://cardroomgrinders.com.br/static/js/main.*.js | grep "Data - Instrutor - Categoria"
```

### Limpar cache do navegador

- **Chrome/Edge**: Ctrl+Shift+Delete
- **Firefox**: Ctrl+Shift+Delete
- **Safari**: Cmd+Option+E

### Testar em modo incógnito

- **Chrome**: Ctrl+Shift+N
- **Firefox**: Ctrl+Shift+P
- **Safari**: Cmd+Option+N

## 📊 Camadas de Cache

```
┌─────────────────────────────────────────────────────────────┐
│                    NAVEGADOR DO USUÁRIO                     │
│                   (Cache Local - 1 ano)                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    CLOUDFLARE CDN                           │
│              (Cache Global - Variável)                      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    NGINX (Docker)                           │
│  HTML: Sem cache | JS/CSS com hash: 1 ano | Outros: 30d   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    APLICAÇÃO REACT                          │
│              (Gera hashes únicos para cada build)           │
└─────────────────────────────────────────────────────────────┘
```

## ✅ Checklist de Verificação

- [ ] Backup realizado e salvo localmente
- [ ] nginx.conf atualizado com nova estratégia de cache
- [ ] deploy.sh criado e testado
- [ ] Build feito com `npm run build`
- [ ] Deploy executado com `./deploy.sh`
- [ ] Cache do Cloudflare limpo
- [ ] Testado em janela anônima
- [ ] Novo texto aparece na página

## 🆘 Troubleshooting

### Problema: Novo texto ainda não aparece

**Solução:**
1. Limpe cache do Cloudflare (https://dash.cloudflare.com)
2. Limpe cache do navegador (Ctrl+Shift+Delete)
3. Teste em modo incógnito
4. Aguarde 5-10 minutos para Cloudflare atualizar

### Problema: Arquivo não encontrado (404)

**Solução:**
1. Verifique se o build foi copiado: `ls -la /root/Dojo_Deploy/poker-academy/poker-academy/build/`
2. Verifique se o Nginx está rodando: `docker ps | grep poker_frontend`
3. Reinicie o Nginx: `docker restart poker_frontend`

### Problema: Perda de dados

**Recuperação:**
```bash
# Restaurar banco de dados
docker exec poker_mysql mysql -u root -p'poker_academy_2025' < /root/backups/database_backup_*.sql

# Restaurar volumes
docker run --rm -v mysql_data:/data -v /root/backups:/backup alpine tar xzf /backup/mysql_volume_backup_*.tar.gz -C /data
```

## 📚 Referências

- [Nginx Caching Best Practices](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cache)
- [HTTP Cache Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control)
- [Cloudflare Cache Purge](https://developers.cloudflare.com/cache/how-to/purge-cache/)
- [React Build Optimization](https://create-react-app.dev/docs/production-build/)

