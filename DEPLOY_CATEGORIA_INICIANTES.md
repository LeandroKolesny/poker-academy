# 🚀 Deploy da Categoria "Iniciantes"

**Data**: 16 de Outubro de 2025  
**Status**: ✅ **PRONTO PARA DEPLOY**

---

## 📋 Resumo das Alterações

### Backend
- ✅ Adicionado `iniciantes` ao enum `ClassCategory` em `models.py`
- ✅ Alteração em 2 arquivos (deploy e local)

### Banco de Dados
- ✅ Adicionado "iniciantes" ao ENUM da coluna `category` na tabela `classes`
- ✅ Alteração executada com sucesso

---

## 🚀 Como Fazer o Deploy

### Opção 1: Deploy Completo (Recomendado)

**Passo 1**: Conectar ao servidor
```bash
ssh root@142.93.206.128
# Senha: DojoShh159357
```

**Passo 2**: Parar o backend
```bash
docker stop backend
```

**Passo 3**: Reconstruir a imagem do backend
```bash
cd /root/Dojo_Deploy/poker-academy
docker build -t poker-academy_backend .
```

**Passo 4**: Iniciar o backend
```bash
docker start backend
```

**Passo 5**: Verificar se está rodando
```bash
docker ps | grep backend
```

**Passo 6**: Verificar logs
```bash
docker logs backend
```

---

### Opção 2: Deploy Rápido (Se não quiser reconstruir)

Se o backend já tem o código atualizado, apenas reinicie:

```bash
docker restart backend
```

---

## ✅ Verificação Após Deploy

### 1. Verificar se o Backend está Rodando
```bash
docker ps | grep backend
```

**Esperado**: Container `backend` com status `Up`

### 2. Verificar Logs do Backend
```bash
docker logs backend | tail -20
```

**Esperado**: Sem erros, backend iniciado com sucesso

### 3. Testar a API
```bash
curl http://localhost:5000/api/health
```

**Esperado**: Resposta JSON com status do backend

### 4. Verificar Banco de Dados
```bash
docker exec 0b2a94fd276e_poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "SHOW COLUMNS FROM classes LIKE 'category';"
```

**Esperado**: Coluna `category` com enum incluindo "iniciantes"

---

## 🧪 Teste Manual

### 1. Criar uma Aula com Categoria "Iniciantes"

**Via API**:
```bash
curl -X POST http://localhost:5000/api/classes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "name": "Introdução ao Poker",
    "instructor": "João Silva",
    "category": "iniciantes",
    "description": "Aula para iniciantes"
  }'
```

### 2. Listar Aulas por Categoria
```bash
curl http://localhost:5000/api/classes?category=iniciantes
```

### 3. Verificar no Banco de Dados
```bash
docker exec 0b2a94fd276e_poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "SELECT * FROM classes WHERE category = 'iniciantes';"
```

---

## 🔄 Rollback (Se Necessário)

Se algo der errado, você pode reverter:

### 1. Remover a Categoria do Banco
```bash
docker exec 0b2a94fd276e_poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "ALTER TABLE classes MODIFY COLUMN category ENUM('preflop', 'postflop', 'mental', 'torneos', 'cash') NOT NULL;"
```

### 2. Reverter o Código
- Remova `iniciantes = "iniciantes"` do enum `ClassCategory` em `models.py`

### 3. Reconstruir e Reiniciar
```bash
docker stop backend
docker build -t poker-academy_backend .
docker start backend
```

---

## 📊 Checklist de Deploy

- [ ] Código atualizado em `models.py`
- [ ] Banco de dados alterado (ENUM atualizado)
- [ ] Backend parado
- [ ] Imagem reconstruída
- [ ] Backend iniciado
- [ ] Logs verificados (sem erros)
- [ ] API testada
- [ ] Banco de dados verificado
- [ ] Aula criada com categoria "iniciantes"
- [ ] Aula persiste no banco

---

## 🛡️ Segurança

✅ Alteração segura  
✅ Sem perda de dados  
✅ Compatível com dados existentes  
✅ Reversível se necessário  

---

## 📞 Informações Úteis

### Servidor
```
IP: 142.93.206.128
Usuário: root
Senha: DojoShh159357
```

### Banco de Dados
```
Servidor: localhost (dentro do container)
Banco: poker_academy
Usuário: poker_user
Senha: Dojo@Sql159357
```

### Backend
```
Container: backend
Porta: 5000
Imagem: poker-academy_backend
```

---

## ✨ Conclusão

O deploy da categoria "Iniciantes" é simples:

1. Parar o backend
2. Reconstruir a imagem
3. Iniciar o backend
4. Testar

**Tempo estimado**: 5-10 minutos

---

**Status**: ✅ Pronto para Deploy  
**Data**: 16 de Outubro de 2025  
**Categoria**: iniciantes

