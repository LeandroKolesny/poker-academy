# 💾 Backup do Banco de Dados - Poker Academy

## ✅ Status Atual

**Backup criado com sucesso em:** `backups/` directory

### Arquivos de Backup:
- `poker_academy_backup_20251016_192842.sql` - 20 KB ✅
- `poker_academy_backup_20251016_192908.sql` - 20 KB ✅

## 🚀 Como Usar

### 1. Fazer Backup Manual

```bash
python backup_database.py
```

Isso irá:
- Conectar ao servidor via SSH
- Fazer dump do banco de dados MySQL
- Copiar o arquivo para `backups/` local
- Exibir o tamanho do backup

### 2. Fazer Backups Automáticos (A cada 6 horas)

```bash
python backup_schedule.py
```

Isso irá:
- Fazer um backup imediatamente
- Agendar backups automáticos a cada 6 horas
- Continuar rodando até você pressionar Ctrl+C

### 3. Restaurar um Backup

```bash
# Copiar o arquivo de backup para o servidor
scp -i "C:\Users\Usuario\.ssh\id_rsa" backups/poker_academy_backup_20251016_192908.sql root@142.93.206.128:/root/

# Conectar ao servidor
ssh -i "C:\Users\Usuario\.ssh\id_rsa" root@142.93.206.128

# Restaurar o banco de dados
docker exec -i poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy < /root/poker_academy_backup_20251016_192908.sql
```

## 📋 Configurações

### Credenciais (em backup_database.py):
- **Host:** 142.93.206.128
- **SSH User:** root
- **SSH Password:** DojoShh159357
- **MySQL User:** poker_user
- **MySQL Password:** Dojo@Sql159357
- **Database:** poker_academy

### Localização dos Backups:
- **Local:** `C:/Users/Usuario/Desktop/site_Dojo_Final/backups/`
- **Servidor:** `/root/poker_academy_backup_*.sql`

## ⚠️ Importante

1. **Nunca compartilhe as credenciais** - Estão no script por conveniência, mas em produção devem estar em variáveis de ambiente
2. **Faça backups regularmente** - Use `backup_schedule.py` para automatizar
3. **Teste restaurações** - Sempre teste se o backup pode ser restaurado
4. **Armazene em local seguro** - Copie os backups para um local seguro (Google Drive, OneDrive, etc.)

## 🔧 Dependências

```bash
pip install paramiko schedule
```

## 📊 Tamanho Esperado

- Banco de dados vazio: ~20 KB
- Com dados: Depende da quantidade de dados

## 🆘 Troubleshooting

### Erro: "No such container: poker_mysql"
- Os containers não estão rodando
- Solução: `ssh root@142.93.206.128 "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d"`

### Erro: "Access denied"
- Credenciais incorretas
- Solução: Verificar as credenciais em `backup_database.py`

### Arquivo de backup vazio
- Containers não estavam prontos
- Solução: Esperar alguns segundos e tentar novamente

## 📝 Próximos Passos

1. ✅ Backup criado
2. ⏳ Configurar backups automáticos
3. ⏳ Armazenar backups em local seguro
4. ⏳ Testar restauração

