# 🎬 Guia Completo - Auto Import com Categorias

## 📋 O que foi alterado?

### Antes (Formato Antigo)
```
Data - Instrutor - Nome da aula.mp4
Exemplo: 21.01.25 - Eiji - Mystery bounty.mp4
```

### Depois (Novo Formato)
```
Data - Instrutor - Categoria - Nome da aula.mp4
Exemplo: 21.01.25 - Eiji - PreFlop - Mystery bounty.mp4
```

## 🎯 Categorias Disponíveis

| Nome do Arquivo | Normalizado | Exibição |
|---|---|---|
| PreFlop | preflop | Pré-Flop |
| PosFlop | postflop | Pós-Flop |
| Mental | mental | Mental Games |
| ICM | icm | ICM |
| iniciante | iniciantes | Iniciante |

## 📝 Exemplos de Nomes Válidos

✅ **Corretos:**
- `21.01.25 - Eiji - PreFlop - Mystery bounty.mp4`
- `22.01.25 - João - Mental - Estratégias de torneio.avi`
- `23.01.25 - Maria - PosFlop - Cash game avançado.mov`
- `24.01.25 - Pedro - ICM - Bubble play.mkv`
- `25.01.25 - Ana - iniciante - Conceitos básicos.webm`

❌ **Incorretos (faltam 4 partes):**
- `21.01.25 - Eiji - Mystery bounty.mp4` (faltam categoria)
- `Eiji - PreFlop - Mystery bounty.mp4` (faltam data)

## 🧪 Teste Passo a Passo

### 1. Criar Arquivos de Teste

Execute este comando no seu terminal:

```bash
mkdir -p ~/Downloads/videos_teste

# Arquivo 1
dd if=/dev/zero bs=1M count=1 of="$HOME/Downloads/videos_teste/21.01.25 - Eiji - PreFlop - Mystery bounty.mp4" 2>/dev/null

# Arquivo 2
dd if=/dev/zero bs=1M count=1 of="$HOME/Downloads/videos_teste/22.01.25 - João - Mental - Estratégias de torneio.avi" 2>/dev/null

# Arquivo 3
dd if=/dev/zero bs=1M count=1 of="$HOME/Downloads/videos_teste/23.01.25 - Maria - PosFlop - Cash game avançado.mov" 2>/dev/null
```

### 2. Acessar o Sistema

- URL: https://cardroomgrinders.com.br/admin/classes
- Login: admin
- Senha: admin123

### 3. Usar Auto Import

1. Clique no botão "Auto Import"
2. Selecione os 3 arquivos criados
3. Verifique a tabela de preview

### 4. Verificar Preview

Você deve ver algo como:

```
Mystery bounty
📅 21/01/2025 | 👨‍🏫 Eiji | 📂 Pré-Flop | 📁 1.00 MB

Estratégias de torneio
📅 22/01/2025 | 👨‍🏫 João | 📂 Mental Games | 📁 1.00 MB

Cash game avançado
📅 23/01/2025 | 👨‍🏫 Maria | 📂 Pós-Flop | 📁 1.00 MB
```

### 5. Fazer Upload

1. Clique em "🚀 Fazer Upload (3 vídeos)"
2. Aguarde o upload completar
3. Verifique se as aulas foram criadas

## 🔍 Verificar no Console (F12)

Abra o Developer Tools (F12) e vá para a aba "Console".

Você deve ver logs como:

```
✅ Arquivo parseado: Data=21.01.25, Instrutor=Eiji, Categoria=PreFlop, Nome=Mystery bounty
✅ Arquivo parseado: Data=22.01.25, Instrutor=João, Categoria=Mental, Nome=Estratégias de torneio
✅ Arquivo parseado: Data=23.01.25, Instrutor=Maria, Categoria=PosFlop, Nome=Cash game avançado
```

## 📊 Verificar no Banco de Dados

Após o upload, as aulas devem aparecer na lista com:
- ✅ Data: 21/01/2025, 22/01/2025, 23/01/2025
- ✅ Instrutor: Eiji, João, Maria
- ✅ **Categoria: Pré-Flop, Mental Games, Pós-Flop** (NOVO!)
- ✅ Nome: Mystery bounty, Estratégias de torneio, Cash game avançado

## 🔧 Arquivos Modificados

- `poker-academy/src/components/admin/ClassManagement.js`
  - Função `extractCategoryFromFileName()` - Agora espera 4 partes
  - Função `handleImportFilesChange()` - Parseia categoria
  - Função `uploadVideosWithProgress()` - Usa categoria parseada
  - Tabela de preview - Exibe categoria

## ✨ Resultado Final

O sistema agora:
1. ✅ Parseia corretamente o novo formato com 4 partes
2. ✅ Extrai a categoria do nome do arquivo
3. ✅ Normaliza a categoria para valores padrão
4. ✅ Exibe a categoria na tabela de preview
5. ✅ Envia a categoria para o backend
6. ✅ Cria as aulas com as categorias corretas

## 🚀 Deploy

- ✅ Build realizado
- ✅ Frontend reiniciado
- ✅ Sistema pronto para teste

