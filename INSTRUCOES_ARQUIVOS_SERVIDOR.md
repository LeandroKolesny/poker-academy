# 📥 Instruções - Arquivos do Servidor para Sua Máquina

**Data**: 16 de Outubro de 2025  
**Status**: ✅ Arquivos Copiados com Sucesso

---

## 📍 Localização dos Arquivos

### No Servidor (Não Alterado)
```
/var/www/html/
```

### No Workspace Augment
```
/mnt/persist/workspace/site_Dojo2_temp/
/mnt/persist/workspace/site_Dojo2_servidor.tar.gz (4.0 MB)
```

### Na Sua Máquina (Destino)
```
C:\Users\Usuario\Desktop\site_Dojo2\
```

---

## 📊 Arquivos Copiados

**Total**: 8.9 MB

### Estrutura
```
site_Dojo2_temp/
├── asset-manifest.json
├── favicon.ico
├── favicon.png
├── index.html
├── index.nginx-debian.html
├── logo-dojo-poker.png
├── manifest.json
├── reset-password.html
├── robots.txt
├── css/
├── js/
└── static/
    ├── css/
    ├── js/
    └── media/
```

---

## 📥 Como Baixar para Sua Máquina

### Opção 1: Baixar Arquivo Compactado (Recomendado)

**Arquivo**: `site_Dojo2_servidor.tar.gz` (4.0 MB)

**Passos**:
1. Abra o File Explorer do Augment
2. Navegue até `/mnt/persist/workspace/`
3. Procure por `site_Dojo2_servidor.tar.gz`
4. Clique em Download
5. Salve em `C:\Users\Usuario\Desktop\`

**Depois de baixar**:
1. Extraia o arquivo (use 7-Zip ou WinRAR)
2. Copie o conteúdo de `site_Dojo2_temp/` para `C:\Users\Usuario\Desktop\site_Dojo2\`

### Opção 2: Baixar Pasta Completa

**Pasta**: `site_Dojo2_temp/` (8.9 MB)

**Passos**:
1. Abra o File Explorer do Augment
2. Navegue até `/mnt/persist/workspace/site_Dojo2_temp/`
3. Selecione todos os arquivos (Ctrl+A)
4. Clique em Download
5. Salve em `C:\Users\Usuario\Desktop\site_Dojo2\`

### Opção 3: Usar SCP (Linha de Comando)

**Windows (PowerShell)**:
```powershell
# Criar pasta se não existir
mkdir "C:\Users\Usuario\Desktop\site_Dojo2" -Force

# Baixar arquivos
scp -r augment@<seu-ip>:/mnt/persist/workspace/site_Dojo2_temp/* "C:\Users\Usuario\Desktop\site_Dojo2\"
```

**Linux/Mac (Terminal)**:
```bash
mkdir -p ~/Desktop/site_Dojo2
scp -r augment@<seu-ip>:/mnt/persist/workspace/site_Dojo2_temp/* ~/Desktop/site_Dojo2/
```

---

## ✅ Verificação

Após baixar, verifique se tem todos os arquivos:

```
C:\Users\Usuario\Desktop\site_Dojo2\
├── asset-manifest.json ✅
├── favicon.ico ✅
├── favicon.png ✅
├── index.html ✅
├── logo-dojo-poker.png ✅
├── manifest.json ✅
├── reset-password.html ✅
├── robots.txt ✅
├── css/ ✅
├── js/ ✅
└── static/ ✅
```

**Total de arquivos**: ~50+  
**Tamanho total**: ~8.9 MB

---

## 🔄 Substituição de Arquivos

### Passo 1: Backup (Recomendado)
```powershell
# Fazer backup dos arquivos antigos
Copy-Item "C:\Users\Usuario\Desktop\site_Dojo2" "C:\Users\Usuario\Desktop\site_Dojo2_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')" -Recurse
```

### Passo 2: Limpar Pasta Antiga
```powershell
# Remover arquivos antigos (mantém a pasta)
Remove-Item "C:\Users\Usuario\Desktop\site_Dojo2\*" -Recurse -Force
```

### Passo 3: Copiar Novos Arquivos
```powershell
# Copiar arquivos do servidor
Copy-Item "C:\Users\Usuario\Desktop\site_Dojo2_temp\*" "C:\Users\Usuario\Desktop\site_Dojo2\" -Recurse -Force
```

### Passo 4: Verificar
```powershell
# Listar arquivos
Get-ChildItem "C:\Users\Usuario\Desktop\site_Dojo2\" -Recurse | Measure-Object
```

---

## 🛡️ Segurança - Servidor Não Alterado

✅ **Nenhum arquivo foi alterado no servidor**

Confirmação:
- Apenas leitura (SCP com `-r` flag)
- Sem permissões de escrita
- Sem exclusão de arquivos
- Sem modificação de permissões

---

## 📋 Conteúdo dos Arquivos

### Arquivos Principais
- **index.html** - Página principal do React
- **reset-password.html** - Página de reset de senha
- **manifest.json** - Configuração PWA
- **robots.txt** - Configuração para buscadores

### Diretórios
- **css/** - Estilos CSS
- **js/** - JavaScript compilado
- **static/** - Arquivos estáticos (CSS, JS, imagens)

### Imagens
- **favicon.ico** - Ícone do site
- **favicon.png** - Ícone em PNG
- **logo-dojo-poker.png** - Logo do Dojo Poker

---

## 🔍 Informações Técnicas

### Origem
```
Servidor: 142.93.206.128
Caminho: /var/www/html/
Data: 16 de Outubro de 2025
Tamanho: 8.9 MB
Arquivos: ~50+
```

### Formato
```
Compactado: site_Dojo2_servidor.tar.gz (4.0 MB)
Descompactado: site_Dojo2_temp/ (8.9 MB)
```

---

## 🆘 Troubleshooting

### Problema: Arquivo não baixa
**Solução**: Tente a Opção 2 (pasta completa) em vez do arquivo compactado

### Problema: Erro ao extrair
**Solução**: Use 7-Zip (gratuito) em vez de WinRAR

### Problema: Permissões negadas
**Solução**: Execute PowerShell como Administrador

### Problema: Arquivo incompleto
**Solução**: Verifique o tamanho (deve ser ~8.9 MB)

---

## ✅ Próximos Passos

1. **Baixe os arquivos** usando uma das opções acima
2. **Verifique** se todos os arquivos foram copiados
3. **Faça backup** dos arquivos antigos
4. **Substitua** os arquivos na pasta `site_Dojo2`
5. **Teste** o site localmente

---

## 📞 Informações Úteis

### Servidor
```
IP: 142.93.206.128
Usuário: root
Caminho: /var/www/html/
```

### Sua Máquina
```
Pasta: C:\Users\Usuario\Desktop\site_Dojo2\
```

### Arquivos Criados
```
site_Dojo2_temp/        (8.9 MB - pasta)
site_Dojo2_servidor.tar.gz (4.0 MB - compactado)
```

---

**Status**: ✅ Arquivos Prontos para Download  
**Data**: 16 de Outubro de 2025  
**Segurança**: ✅ Servidor Não Alterado

