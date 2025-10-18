# Checklist de Verificação do Servidor

Use este checklist para verificar se o servidor está funcionando corretamente.

## ✅ Verificação Rápida (5 minutos)

- [ ] Conectar ao servidor: `ssh root@142.93.206.128`
- [ ] Verificar containers: `docker ps -a`
  - [ ] `backend` está **Up**
  - [ ] `0b2a94fd276e_poker_mysql` está **Up**
  - [ ] `node` está **Up**
- [ ] Verificar NGINX: `systemctl status nginx`
  - [ ] Status é **active (running)**
- [ ] Testar backend: `curl http://localhost:5000/api/health`
  - [ ] Resposta é JSON válido
- [ ] Acessar frontend: `https://cardroomgrinders.com.br`
  - [ ] Página carrega sem erros
  - [ ] Certificado SSL é válido

## 🔍 Verificação Detalhada (15 minutos)

### Portas
- [ ] Porta 80 (HTTP): `lsof -i :80`
  - [ ] NGINX está escutando
- [ ] Porta 443 (HTTPS): `lsof -i :443`
  - [ ] NGINX está escutando
- [ ] Porta 5000 (Backend): `lsof -i :5000`
  - [ ] Backend está escutando
- [ ] Porta 3306 (MySQL): `lsof -i :3306`
  - [ ] MySQL está escutando

### Banco de Dados
- [ ] Conectar ao MySQL: `mysql -h localhost -u poker_user -p poker_academy`
  - [ ] Senha: `Dojo@Sql159357`
  - [ ] Conexão bem-sucedida
- [ ] Verificar tabelas: `SHOW TABLES;`
  - [ ] Tabelas existem
- [ ] Verificar dados: `SELECT COUNT(*) FROM users;`
  - [ ] Dados estão presentes

### Frontend
- [ ] Verificar arquivos: `ls -la /var/www/html/`
  - [ ] `index.html` existe
  - [ ] Diretório `static/` existe
  - [ ] Arquivos têm permissões corretas
- [ ] Verificar tamanho: `du -sh /var/www/html/`
  - [ ] Tamanho é razoável (> 1MB)

### Backend
- [ ] Ver logs: `docker logs backend`
  - [ ] Sem erros críticos
  - [ ] Conectado ao banco de dados
- [ ] Testar endpoints:
  - [ ] `curl http://localhost:5000/api/health`
  - [ ] `curl http://localhost:5000/api/users` (com token)

### NGINX
- [ ] Testar configuração: `nginx -t`
  - [ ] Resultado: "successful"
- [ ] Ver logs: `tail -20 /var/log/nginx/error.log`
  - [ ] Sem erros críticos
- [ ] Verificar certificado: `openssl x509 -in /etc/letsencrypt/live/cardroomgrinders.com.br/fullchain.pem -noout -dates`
  - [ ] Certificado não expirou

### Sistema
- [ ] Espaço em disco: `df -h`
  - [ ] Menos de 80% utilizado
- [ ] Memória: `free -h`
  - [ ] Memória disponível > 1GB
- [ ] Uptime: `uptime`
  - [ ] Servidor está estável

## 🚨 Troubleshooting

### Se Backend não responde
```bash
# 1. Verificar se está rodando
docker ps | grep backend

# 2. Se não estiver, iniciar
docker start backend

# 3. Ver logs
docker logs backend

# 4. Se houver erro, reiniciar
docker restart backend
```

### Se NGINX não responde
```bash
# 1. Verificar status
systemctl status nginx

# 2. Se não estiver rodando, iniciar
systemctl start nginx

# 3. Testar configuração
nginx -t

# 4. Se houver erro, corrigir e reiniciar
systemctl restart nginx
```

### Se MySQL não responde
```bash
# 1. Verificar se está rodando
docker ps | grep mysql

# 2. Se não estiver, iniciar
docker start 0b2a94fd276e_poker_mysql

# 3. Ver logs
docker logs 0b2a94fd276e_poker_mysql

# 4. Se houver erro, reiniciar
docker restart 0b2a94fd276e_poker_mysql
```

### Se Frontend não carrega
```bash
# 1. Verificar se arquivos existem
ls -la /var/www/html/

# 2. Verificar permissões
chmod -R 755 /var/www/html/

# 3. Reiniciar NGINX
systemctl restart nginx

# 4. Limpar cache do navegador (Ctrl+Shift+Delete)
```

### Se Certificado SSL expirou
```bash
# 1. Renovar certificado
certbot renew

# 2. Se não funcionar, renovar com força
certbot renew --force-renewal

# 3. Reiniciar NGINX
systemctl restart nginx
```

## 📊 Monitoramento Contínuo

### Verificação Diária
- [ ] Acessar `https://cardroomgrinders.com.br`
- [ ] Fazer login com usuário de teste
- [ ] Verificar se funcionalidades básicas funcionam
- [ ] Verificar logs de erro: `tail -20 /var/log/nginx/error.log`

### Verificação Semanal
- [ ] Executar checklist detalhado completo
- [ ] Verificar espaço em disco
- [ ] Verificar certificado SSL (data de expiração)
- [ ] Fazer backup do banco de dados

### Verificação Mensal
- [ ] Atualizar sistema: `apt update && apt upgrade`
- [ ] Atualizar Docker: `docker pull poker-academy_backend:latest`
- [ ] Revisar logs de erro
- [ ] Testar recuperação de backup

## 🔐 Segurança

- [ ] SSH apenas com chave (não senha)
- [ ] Firewall configurado (UFW)
- [ ] Certificado SSL válido
- [ ] Senhas fortes em uso
- [ ] Backups regulares

## 📝 Notas

Adicione aqui qualquer informação importante ou problemas encontrados:

```
Data: _______________
Problema: ___________________________________________________________
Solução: ____________________________________________________________
```

## 🆘 Contato de Suporte

Se algo não funcionar:
1. Consulte este checklist
2. Verifique os logs
3. Tente reiniciar o serviço
4. Se persistir, entre em contato com suporte técnico

