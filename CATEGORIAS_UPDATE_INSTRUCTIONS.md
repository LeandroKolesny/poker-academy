# Atualização de Categorias de Aulas

## Resumo das Mudanças

As categorias de aulas foram atualizadas para:
- **Iniciante** (iniciantes)
- **Pré-Flop** (preflop)
- **Pós-Flop** (postflop)
- **Mental Games** (mental)
- **ICM** (icm)

As categorias antigas **Torneios** e **Cash Game** foram removidas.

## Arquivos Modificados

### Frontend (React)
1. **poker-academy/src/components/student/Catalog.js**
   - Atualizado array de categorias
   - Atualizado mapeamento de nomes de categorias

2. **poker-academy/src/components/admin/ClassManagement.js**
   - Atualizado getCategoryName()
   - Atualizado normalizeCategoryName()
   - Atualizado dropdown de seleção de categorias

3. **poker-academy/src/components/student/History.js**
   - Adicionada cor para categoria "iniciantes"
   - Atualizado getCategoryColor()

### Backend (Flask)
1. **poker-academy-backend/poker_academy_api/src/models.py**
   - ClassCategory enum já contém: iniciantes, preflop, postflop, mental, icm

2. **poker-academy-backend/poker_academy_api/src/routes/class_routes.py**
   - Atualizado normalize_category() para mapear nomes em português

### Banco de Dados
1. **update_database_categories.sql**
   - Script para atualizar o ENUM da tabela classes
   - Converte aulas antigas para novas categorias

## Passos para Implementar

### 1. No Servidor (SSH)

```bash
# Conectar ao servidor
ssh root@142.93.206.128

# Navegar para o diretório do projeto
cd /root/Dojo_Deploy/poker-academy

# Fazer pull das mudanças
git pull origin main

# Executar o script SQL no banco de dados
mysql -u poker_user -p poker_academy < update_database_categories.sql
# Senha: Dojo@Sql159357
```

### 2. Reconstruir e Reiniciar Containers

```bash
# Navegar para o diretório de deploy
cd /root/Dojo_Deploy

# Reconstruir os containers
docker-compose build

# Reiniciar os containers
docker-compose up -d

# Verificar status
docker-compose ps

# Ver logs do backend
docker logs poker-academy-backend
```

## Testes

### 1. Testar Frontend
- Acessar http://grinders.com.br (ou IP:porta)
- Verificar se as categorias aparecem no filtro do catálogo
- Verificar se as categorias aparecem no dropdown de cadastro de aulas

### 2. Testar Backend
- Criar uma nova aula com categoria "Iniciante"
- Verificar se a aula é salva com a categoria correta
- Testar auto-import com nomes como "15.10.25 - Instrutor - Iniciante.mp4"

### 3. Testar Banco de Dados
```bash
# Conectar ao banco
mysql -u poker_user -p poker_academy

# Verificar categorias
SELECT DISTINCT category FROM classes;

# Contar aulas por categoria
SELECT category, COUNT(*) FROM classes GROUP BY category;
```

## Normalização de Categorias

O sistema normaliza automaticamente nomes em português para valores do enum:
- "Iniciante" → "iniciantes"
- "Pré-Flop" → "preflop"
- "Pós-Flop" → "postflop"
- "Mental Games" → "mental"
- "ICM" → "icm"

Isso funciona tanto no upload de arquivos quanto no formulário de cadastro.

## Rollback (se necessário)

Se precisar reverter as mudanças:

```bash
# Reverter para o commit anterior
git reset --hard f503979

# Ou fazer revert
git revert HEAD~3
```

