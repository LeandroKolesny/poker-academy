# 📥 Como Baixar Vídeos das Aulas do Servidor

**Data**: 16 de Outubro de 2025  
**Status**: ✅ **INSTRUÇÕES PRONTAS**

---

## 📊 Informações dos Vídeos

### Localização no Servidor
```
Servidor: 142.93.206.128
Caminho: /app/uploads/videos/
Container: backend
```

### Dados dos Vídeos
```
Total de Arquivos: 26
Tamanho Total: ~5.8 GB
Formato: MP4, MKV
```

### Destino na Sua Máquina
```
C:\Users\Usuario\Desktop\Site_Dojo_final_15_10_2025\Aula_video\
```

---

## 🚀 Como Baixar (2 Opções)

### **Opção 1: Usar SCP (Recomendado - Mais Rápido)**

**Passo 1**: Abra PowerShell como Administrador

**Passo 2**: Crie a pasta de destino
```powershell
mkdir "C:\Users\Usuario\Desktop\Site_Dojo_final_15_10_2025\Aula_video" -Force
```

**Passo 3**: Execute o comando SCP
```powershell
scp -r root@142.93.206.128:/app/uploads/videos/* "C:\Users\Usuario\Desktop\Site_Dojo_final_15_10_2025\Aula_video\"
```

**Passo 4**: Quando solicitado, digite a senha
```
DojoShh159357
```

**Passo 5**: Aguarde o download completar (pode levar alguns minutos)

---

### **Opção 2: Usar Docker (Se SCP não funcionar)**

**Passo 1**: Conecte ao servidor
```bash
ssh root@142.93.206.128
# Senha: DojoShh159357
```

**Passo 2**: Copie os vídeos do container para /tmp
```bash
docker cp backend:/app/uploads/videos /tmp/videos
```

**Passo 3**: Saia do servidor
```bash
exit
```

**Passo 4**: Baixe os vídeos via SCP
```powershell
scp -r root@142.93.206.128:/tmp/videos/* "C:\Users\Usuario\Desktop\Site_Dojo_final_15_10_2025\Aula_video\"
```

---

## 📋 Lista de Vídeos

Os vídeos incluem aulas sobre:
- Pseudo Fruto - Short
- Gustavo Biguethi - BvM
- Carlos.Rox - Cold Call
- Ruan Bispo - Check-Raise
- Quadskilla - ISO BW
- Luandods - Floats Flop
- Diego Tgrinder - CBet Turn
- Danton - Linhas não contínuas
- Morfeu90 - Check-Raise Turn
- Koles - 3Bet
- E muitos outros...

**Total**: 26 vídeos

---

## ✅ Verificação Após Download

Após o download completar, verifique:

```powershell
# Listar arquivos
Get-ChildItem "C:\Users\Usuario\Desktop\Site_Dojo_final_15_10_2025\Aula_video\" -Recurse

# Contar arquivos
(Get-ChildItem "C:\Users\Usuario\Desktop\Site_Dojo_final_15_10_2025\Aula_video\" -Recurse | Measure-Object).Count

# Ver tamanho total
(Get-ChildItem "C:\Users\Usuario\Desktop\Site_Dojo_final_15_10_2025\Aula_video\" -Recurse | Measure-Object -Property Length -Sum).Sum / 1GB
```

**Esperado**:
- Arquivos: 26
- Tamanho: ~5.8 GB

---

## 🔄 Script PowerShell (Automático)

**Arquivo**: `baixar_videos_aulas.ps1`

**Passos**:
1. Baixe o script `baixar_videos_aulas.ps1`
2. Coloque em `C:\Users\Usuario\Desktop\`
3. Abra PowerShell como Administrador
4. Execute: `.\baixar_videos_aulas.ps1`
5. Siga as instruções na tela

---

## 💡 Dicas Importantes

### Se o Download for Interrompido
- Execute o comando SCP novamente
- O SCP continuará de onde parou
- Não precisa baixar tudo novamente

### Se Receber Erro de Conexão
- Verifique se o servidor está online
- Verifique a senha
- Tente novamente

### Se Receber Erro de Permissão
- Abra PowerShell como Administrador
- Verifique se a pasta de destino existe
- Crie a pasta manualmente se necessário

### Para Acelerar o Download
- Use uma conexão com internet rápida
- Feche outros programas que usam internet
- Não interrompa o download

---

## 🛡️ Segurança

✅ Apenas leitura (SCP)  
✅ Sem alterações no servidor  
✅ Sem exclusão de arquivos  
✅ Conexão segura (SSH)  

---

## 📞 Informações Úteis

### Servidor
```
IP: 142.93.206.128
Usuário: root
Senha: DojoShh159357
Caminho: /app/uploads/videos/
```

### Sua Máquina
```
Pasta Destino: C:\Users\Usuario\Desktop\Site_Dojo_final_15_10_2025\Aula_video\
```

---

## ✨ Conclusão

Você tem 2 opções para baixar os vídeos:

1. **SCP** (Recomendado) - Mais rápido e direto
2. **Docker** - Se SCP não funcionar

Escolha uma e siga os passos acima!

---

**Status**: ✅ Instruções Prontas  
**Data**: 16 de Outubro de 2025  
**Total de Vídeos**: 26  
**Tamanho**: ~5.8 GB

