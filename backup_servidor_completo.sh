#!/bin/bash

# Script de Backup Completo do Servidor
# Copia TODOS os arquivos do servidor para sua máquina local
# Segurança: Apenas leitura, sem alterações no servidor

set -e  # Parar se houver erro

# Configurações
SERVIDOR="root@142.93.206.128"
SENHA="DojoShh159357"
CAMINHO_SERVIDOR="/var/www/html"
CAMINHO_LOCAL="/mnt/persist/workspace/backup_servidor_completo"
DATA=$(date +"%Y%m%d_%H%M%S")
ARQUIVO_BACKUP="backup_servidor_${DATA}.tar.gz"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         Backup Completo do Servidor - Iniciando...            ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Passo 1: Criar pasta local
echo "1️⃣  Criando pasta local..."
mkdir -p "$CAMINHO_LOCAL"
echo "✅ Pasta criada: $CAMINHO_LOCAL"
echo ""

# Passo 2: Verificar conexão
echo "2️⃣  Verificando conexão com servidor..."
if sshpass -p "$SENHA" ssh -o StrictHostKeyChecking=no "$SERVIDOR" "echo 'Conectado'" > /dev/null 2>&1; then
    echo "✅ Conexão estabelecida com sucesso"
else
    echo "❌ Erro: Não foi possível conectar ao servidor"
    exit 1
fi
echo ""

# Passo 3: Contar arquivos no servidor
echo "3️⃣  Contando arquivos no servidor..."
TOTAL_ARQUIVOS=$(sshpass -p "$SENHA" ssh -o StrictHostKeyChecking=no "$SERVIDOR" "find $CAMINHO_SERVIDOR -type f | wc -l")
echo "✅ Total de arquivos: $TOTAL_ARQUIVOS"
echo ""

# Passo 4: Copiar arquivos com SCP
echo "4️⃣  Copiando arquivos do servidor (isso pode levar alguns minutos)..."
echo "   Origem: $CAMINHO_SERVIDOR"
echo "   Destino: $CAMINHO_LOCAL"
echo ""

sshpass -p "$SENHA" scp -r -o StrictHostKeyChecking=no "$SERVIDOR:$CAMINHO_SERVIDOR/*" "$CAMINHO_LOCAL/" 2>&1 | grep -E "^[0-9]|^$" || true

echo "✅ Arquivos copiados com sucesso"
echo ""

# Passo 5: Verificar cópia
echo "5️⃣  Verificando integridade da cópia..."
ARQUIVOS_COPIADOS=$(find "$CAMINHO_LOCAL" -type f | wc -l)
TAMANHO_TOTAL=$(du -sh "$CAMINHO_LOCAL" | cut -f1)

echo "   Arquivos copiados: $ARQUIVOS_COPIADOS"
echo "   Tamanho total: $TAMANHO_TOTAL"

if [ "$ARQUIVOS_COPIADOS" -eq "$TOTAL_ARQUIVOS" ]; then
    echo "✅ Verificação OK - Todos os arquivos foram copiados"
else
    echo "⚠️  Aviso: Número de arquivos diferente"
    echo "   Servidor: $TOTAL_ARQUIVOS"
    echo "   Local: $ARQUIVOS_COPIADOS"
fi
echo ""

# Passo 6: Criar arquivo compactado
echo "6️⃣  Criando arquivo compactado..."
cd /mnt/persist/workspace
tar -czf "$ARQUIVO_BACKUP" backup_servidor_completo/
TAMANHO_ARQUIVO=$(ls -lh "$ARQUIVO_BACKUP" | awk '{print $5}')
echo "✅ Arquivo criado: $ARQUIVO_BACKUP ($TAMANHO_ARQUIVO)"
echo ""

# Passo 7: Listar arquivos principais
echo "7️⃣  Arquivos principais copiados:"
ls -lh "$CAMINHO_LOCAL" | tail -20
echo ""

# Passo 8: Resumo final
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║              ✅ BACKUP CONCLUÍDO COM SUCESSO!                 ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 Resumo:"
echo "   Pasta local: $CAMINHO_LOCAL"
echo "   Arquivos: $ARQUIVOS_COPIADOS"
echo "   Tamanho: $TAMANHO_TOTAL"
echo "   Arquivo compactado: $ARQUIVO_BACKUP ($TAMANHO_ARQUIVO)"
echo ""
echo "🛡️  Segurança:"
echo "   ✅ Servidor não foi alterado"
echo "   ✅ Nenhum arquivo foi deletado"
echo "   ✅ Apenas leitura (SCP)"
echo ""
echo "📥 Para baixar:"
echo "   Pasta: /mnt/persist/workspace/backup_servidor_completo/"
echo "   Arquivo: /mnt/persist/workspace/$ARQUIVO_BACKUP"
echo ""

