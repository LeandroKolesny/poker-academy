# Arquitetura do Servidor Poker Academy

## Visão Geral

O servidor Poker Academy é composto por vários componentes que trabalham juntos:

```
┌─────────────────────────────────────────────────────────────┐
│                    Internet / Usuários                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                    HTTPS (443)
                         │
        ┌────────────────▼────────────────┐
        │      NGINX (Reverse Proxy)      │
        │  - Porta 80/443                 │
        │  - Serve Frontend (React)       │
        │  - Proxy para Backend (/api/)   │
        │  - SSL/TLS com Let's Encrypt    │
        └────────────────┬────────────────┘
                         │
        ┌────────────────┴────────────────┐
        │                                 │
    HTTP (5000)                    Arquivos Estáticos
        │                          (/var/www/html/)
        │                                 │
┌───────▼──────────┐          ┌──────────▼──────────┐
│  Backend Flask   │          │  Frontend React     │
│  - Gunicorn      │          │  - index.html       │
│  - Python        │          │  - static/          │
│  - SQLAlchemy    │          │  - CSS/JS           │
└───────┬──────────┘          └─────────────────────┘
        │
    TCP (3306)
        │
┌───────▼──────────┐
│   MySQL 8.0      │
│  - poker_academy │
│  - poker_user    │
└──────────────────┘
```

## Componentes Detalhados

### 1. NGINX (Reverse Proxy)
- **Localização**: `/etc/nginx/sites-enabled/default`
- **Porta**: 80 (HTTP) e 443 (HTTPS)
- **Função**: 
  - Servir arquivos estáticos do frontend
  - Fazer proxy das requisições `/api/` para o backend
  - Gerenciar SSL/TLS
  - Otimizar cache e compressão
- **Iniciar**: `systemctl start nginx`
- **Status**: `systemctl status nginx`

### 2. Backend Flask
- **Localização**: Container Docker `backend`
- **Porta**: 5000 (localhost)
- **Tecnologia**: 
  - Flask 2.2.2
  - Gunicorn (WSGI server)
  - SQLAlchemy 1.4.39
  - PyMySQL 1.0.2
- **Iniciar**: `docker start backend`
- **Logs**: `docker logs backend`

### 3. Frontend React
- **Localização**: `/var/www/html/`
- **Tecnologia**: 
  - React 19.1.0
  - React Router DOM 7.5.3
  - Tailwind CSS
  - FontAwesome Icons
- **Servido por**: NGINX
- **Build**: Pré-compilado em `/var/www/html/static/`

### 4. MySQL Database
- **Localização**: Container Docker `0b2a94fd276e_poker_mysql`
- **Porta**: 3306 (localhost)
- **Banco**: `poker_academy`
- **Usuário**: `poker_user`
- **Versão**: MySQL 8.0
- **Iniciar**: `docker start 0b2a94fd276e_poker_mysql`

### 5. Node.js (PasarGuard)
- **Localização**: Container Docker `node`
- **Função**: Serviço adicional (não crítico para Poker Academy)
- **Status**: Geralmente rodando

## Fluxo de Requisições

### Requisição do Frontend (HTML/CSS/JS)
```
1. Usuário acessa: https://cardroomgrinders.com.br
2. NGINX recebe na porta 443 (HTTPS)
3. NGINX serve arquivos de /var/www/html/
4. Browser carrega React app
```

### Requisição de API
```
1. React faz fetch para: https://cardroomgrinders.com.br/api/...
2. NGINX recebe na porta 443
3. NGINX faz proxy para: http://localhost:5000/api/...
4. Backend Flask processa
5. Backend consulta MySQL
6. Resposta retorna ao frontend
```

## Portas Utilizadas

| Porta | Protocolo | Serviço | Acesso |
|-------|-----------|---------|--------|
| 80 | HTTP | NGINX | Externo (redireciona para 443) |
| 443 | HTTPS | NGINX | Externo |
| 5000 | HTTP | Backend Flask | Apenas localhost (via NGINX) |
| 3306 | TCP | MySQL | Apenas localhost |
| 22 | SSH | SSH Server | Externo (gerenciamento) |

## Diretórios Importantes

| Caminho | Descrição |
|---------|-----------|
| `/var/www/html/` | Frontend React (arquivos estáticos) |
| `/etc/nginx/` | Configuração NGINX |
| `/etc/letsencrypt/` | Certificados SSL/TLS |
| `/var/log/nginx/` | Logs NGINX |
| `/root/` | Diretório home do root |

## Domínios

- **Principal**: `cardroomgrinders.com.br`
- **WWW**: `www.cardroomgrinders.com.br`
- **Certificado SSL**: Let's Encrypt (válido até 2025)

## Variáveis de Ambiente (Backend)

O backend usa variáveis de ambiente para configuração:
- `DATABASE_URL`: Conexão MySQL
- `FLASK_ENV`: Ambiente (production/development)
- `SECRET_KEY`: Chave secreta Flask

## Backup e Recuperação

### Dados Críticos
- **Banco de Dados**: MySQL (container)
- **Frontend**: `/var/www/html/`
- **Certificados SSL**: `/etc/letsencrypt/`

### Recuperação Rápida
Se o servidor desligar:
1. Iniciar MySQL: `docker start 0b2a94fd276e_poker_mysql`
2. Iniciar Backend: `docker start backend`
3. Iniciar NGINX: `systemctl start nginx`

## Monitoramento

### Verificar Saúde do Sistema
```bash
# Todos os serviços
docker ps -a
systemctl status nginx
lsof -i :80,5000,3306
```

### Logs
```bash
# NGINX
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# Backend
docker logs -f backend

# MySQL
docker logs -f 0b2a94fd276e_poker_mysql
```

