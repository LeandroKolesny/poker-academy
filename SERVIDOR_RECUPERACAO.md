# Guia de Recuperação do Servidor Poker Academy

## Informações do Servidor
- **IP**: 142.93.206.128
- **Usuário**: root
- **Senha**: DojoShh159357
- **Banco de Dados**: poker_academy
- **Usuário DB**: poker_user
- **Senha DB**: Dojo@Sql159357

## Passo a Passo para Recuperar o Servidor

### 1. Conectar ao Servidor via SSH

```bash
ssh root@142.93.206.128
```

Quando solicitado, digite a senha: `DojoShh159357`

### 2. Verificar Status dos Containers Docker

```bash
docker ps -a
```

**Esperado:**
- `node` - deve estar **Up** (rodando)
- `backend` - pode estar **Exited** (parado)
- `0b2a94fd276e_poker_mysql` - deve estar **Up** (rodando)
- `frontend` - pode estar **Exited** (parado)

### 3. Iniciar o Backend (se estiver parado)

```bash
docker start backend
```

### 4. Verificar se NGINX está rodando

```bash
systemctl status nginx
```

**Esperado:** Status deve ser `active (running)`

Se não estiver rodando, inicie com:
```bash
systemctl start nginx
```

### 5. Verificar Porta 80 (NGINX)

```bash
lsof -i :80
```

**Esperado:** Deve mostrar `nginx` usando a porta 80

### 6. Verificar Porta 5000 (Backend Flask)

```bash
lsof -i :5000
```

**Esperado:** Deve mostrar o container backend usando a porta 5000

### 7. Verificar Porta 3306 (MySQL)

```bash
lsof -i :3306
```

**Esperado:** Deve mostrar `mysqld` usando a porta 3306

### 8. Testar Conectividade

```bash
curl http://localhost:5000/api/health
```

**Esperado:** Resposta JSON com status do backend

### 9. Verificar Arquivos do Frontend

```bash
ls -la /var/www/html/
```

**Esperado:** Deve conter `index.html`, `static/`, e outros arquivos do React

### 10. Reiniciar NGINX (se necessário)

```bash
systemctl restart nginx
```

## Resumo dos Serviços

| Serviço | Porta | Status | Comando para Iniciar |
|---------|-------|--------|----------------------|
| NGINX | 80/443 | systemctl | `systemctl start nginx` |
| Backend (Flask) | 5000 | Docker | `docker start backend` |
| MySQL | 3306 | Docker | `docker start 0b2a94fd276e_poker_mysql` |
| Node (PasarGuard) | - | Docker | `docker start node` |

## Troubleshooting

### Problema: Porta 80 já está em uso
```bash
# Verificar qual processo está usando
lsof -i :80

# Se for NGINX, reiniciar
systemctl restart nginx
```

### Problema: Backend não conecta ao banco
```bash
# Verificar se MySQL está rodando
docker ps | grep mysql

# Se não estiver, iniciar
docker start 0b2a94fd276e_poker_mysql
```

### Problema: Frontend não carrega
```bash
# Verificar se NGINX está rodando
systemctl status nginx

# Verificar se arquivos existem
ls -la /var/www/html/

# Reiniciar NGINX
systemctl restart nginx
```

### Problema: Erro de conexão ao servidor
```bash
# Verificar conectividade
ping 142.93.206.128

# Verificar SSH
ssh -v root@142.93.206.128
```

## Verificação Rápida (Todos os Serviços)

Execute este comando para verificar tudo de uma vez:

```bash
echo "=== Docker Containers ===" && docker ps -a && \
echo -e "\n=== NGINX Status ===" && systemctl status nginx && \
echo -e "\n=== Portas em Uso ===" && lsof -i :80 && lsof -i :5000 && lsof -i :3306
```

## Notas Importantes

1. **NGINX** serve o frontend estático de `/var/www/html/`
2. **Backend Flask** roda em `localhost:5000` dentro do container
3. **MySQL** roda em `localhost:3306` dentro do container
4. **NGINX** faz proxy das requisições `/api/` para o backend
5. O frontend é servido via HTTPS com certificado Let's Encrypt
6. Domínios: `cardroomgrinders.com.br` e `www.cardroomgrinders.com.br`

## Sair do Servidor

```bash
exit
```

