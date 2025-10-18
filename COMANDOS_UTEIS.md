# Comandos Úteis para Gerenciar o Servidor

## Conexão SSH

```bash
# Conectar ao servidor
ssh root@142.93.206.128

# Com senha (se não tiver chave SSH)
sshpass -p "DojoShh159357" ssh root@142.93.206.128
```

## Docker - Containers

```bash
# Listar todos os containers
docker ps -a

# Listar apenas containers rodando
docker ps

# Iniciar um container
docker start backend
docker start 0b2a94fd276e_poker_mysql

# Parar um container
docker stop backend

# Reiniciar um container
docker restart backend

# Ver logs de um container
docker logs backend
docker logs -f backend  # Seguir logs em tempo real

# Executar comando dentro de um container
docker exec -it backend bash

# Ver informações de um container
docker inspect backend
```

## NGINX

```bash
# Verificar status
systemctl status nginx

# Iniciar NGINX
systemctl start nginx

# Parar NGINX
systemctl stop nginx

# Reiniciar NGINX
systemctl restart nginx

# Recarregar configuração (sem desconectar clientes)
systemctl reload nginx

# Testar configuração
nginx -t

# Ver logs de acesso
tail -f /var/log/nginx/access.log

# Ver logs de erro
tail -f /var/log/nginx/error.log

# Ver configuração ativa
cat /etc/nginx/sites-enabled/default
```

## MySQL

```bash
# Conectar ao MySQL
mysql -h localhost -u poker_user -p poker_academy
# Senha: Dojo@Sql159357

# Dentro do MySQL:
# Ver bancos de dados
SHOW DATABASES;

# Usar banco poker_academy
USE poker_academy;

# Ver tabelas
SHOW TABLES;

# Ver estrutura de uma tabela
DESCRIBE users;

# Contar registros
SELECT COUNT(*) FROM users;

# Sair
EXIT;
```

## Verificações de Porta

```bash
# Ver qual processo está usando uma porta
lsof -i :80      # NGINX
lsof -i :5000    # Backend
lsof -i :3306    # MySQL
lsof -i :22      # SSH

# Ver todas as portas em uso
netstat -tuln
ss -tuln
```

## Arquivos e Diretórios

```bash
# Listar arquivos do frontend
ls -la /var/www/html/

# Ver tamanho dos diretórios
du -sh /var/www/html/
du -sh /var/www/html/static/

# Verificar espaço em disco
df -h

# Verificar uso de memória
free -h

# Verificar uso de CPU
top
```

## Certificados SSL

```bash
# Ver informações do certificado
openssl x509 -in /etc/letsencrypt/live/cardroomgrinders.com.br/fullchain.pem -text -noout

# Ver data de expiração
openssl x509 -in /etc/letsencrypt/live/cardroomgrinders.com.br/fullchain.pem -noout -dates

# Renovar certificado Let's Encrypt
certbot renew

# Renovar com força
certbot renew --force-renewal
```

## Testes de Conectividade

```bash
# Testar backend
curl http://localhost:5000/api/health

# Testar com headers
curl -H "Authorization: Bearer TOKEN" http://localhost:5000/api/users

# Testar HTTPS
curl https://cardroomgrinders.com.br

# Testar com verbose
curl -v https://cardroomgrinders.com.br

# Testar DNS
nslookup cardroomgrinders.com.br
dig cardroomgrinders.com.br
```

## Monitoramento em Tempo Real

```bash
# Dashboard completo
watch -n 1 'docker ps && echo "---" && lsof -i :80,5000,3306'

# Monitorar logs do backend
docker logs -f backend

# Monitorar logs do NGINX
tail -f /var/log/nginx/access.log

# Monitorar recursos do sistema
htop
```

## Backup e Restauração

```bash
# Backup do banco de dados
mysqldump -h localhost -u poker_user -p poker_academy > backup.sql
# Senha: Dojo@Sql159357

# Restaurar banco de dados
mysql -h localhost -u poker_user -p poker_academy < backup.sql

# Backup do frontend
tar -czf frontend_backup.tar.gz /var/www/html/

# Restaurar frontend
tar -xzf frontend_backup.tar.gz -C /
```

## Limpeza e Manutenção

```bash
# Remover containers parados
docker container prune

# Remover imagens não utilizadas
docker image prune

# Remover volumes não utilizados
docker volume prune

# Limpar logs do NGINX
truncate -s 0 /var/log/nginx/access.log
truncate -s 0 /var/log/nginx/error.log

# Limpar cache do sistema
sync && echo 3 > /proc/sys/vm/drop_caches
```

## Troubleshooting Rápido

```bash
# Verificar se tudo está rodando
docker ps -a && systemctl status nginx && lsof -i :80,5000,3306

# Reiniciar tudo
docker restart backend && systemctl restart nginx

# Ver últimos erros
docker logs backend | tail -20
tail -20 /var/log/nginx/error.log

# Verificar conectividade
ping 8.8.8.8
curl https://google.com
```

## Atualizar Aplicação

```bash
# Parar backend
docker stop backend

# Atualizar imagem (se houver nova versão)
docker pull poker-academy_backend:latest

# Iniciar backend
docker start backend

# Verificar logs
docker logs -f backend
```

## Informações do Sistema

```bash
# Versão do Ubuntu
lsb_release -a

# Versão do Docker
docker --version

# Versão do Docker Compose
docker-compose --version

# Versão do NGINX
nginx -v

# Versão do MySQL
mysql --version

# Uptime do servidor
uptime

# Data e hora
date
```

