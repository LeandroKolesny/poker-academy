# ✅ Comando Correto para Baixar Vídeos das Aulas

**Data**: 16 de Outubro de 2025  
**Status**: ✅ **CORRIGIDO**

---

## 🔧 O Problema

O erro ocorreu porque os vídeos estão **dentro do container Docker**, não no servidor diretamente.

```
❌ Erro: /app/uploads/videos/*: No such file or directory
```

---

## ✅ A Solução

Os vídeos foram copiados do container para `/tmp/videos_backup` no servidor. Agora você pode baixá-los com o comando correto:

---

## 🚀 Comando Correto

### **Abra PowerShell como Administrador e execute:**

```powershell
scp -r root@142.93.206.128:/tmp/videos_backup/* "C:\Users\Usuario\Desktop\Site_Dojo_final_15_10_2025\Aula_video\"
```

### **Quando solicitado, digite a senha:**
```
DojoShh159357
```

---

## 📋 Passo a Passo

**Passo 1**: Abra PowerShell como Administrador

**Passo 2**: Crie a pasta de destino (se não existir)
```powershell
mkdir "C:\Users\Usuario\Desktop\Site_Dojo_final_15_10_2025\Aula_video" -Force
```

**Passo 3**: Execute o comando SCP
```powershell
scp -r root@142.93.206.128:/tmp/videos_backup/* "C:\Users\Usuario\Desktop\Site_Dojo_final_15_10_2025\Aula_video\"
```

**Passo 4**: Digite a senha
```
DojoShh159357
```

**Passo 5**: Aguarde o download completar (pode levar alguns minutos)

---

## 📊 Informações dos Vídeos

```
Total de Arquivos: 26
Tamanho Total: ~5.8 GB
Localização Anterior: /app/uploads/videos/ (dentro do container)
Localização Atual: /tmp/videos_backup/ (no servidor)
```

---

## ✅ Verificação Após Download

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

## 💡 Dicas

### Se o Download for Interrompido
- Execute o comando novamente
- O SCP continuará de onde parou

### Se Receber Erro de Conexão
- Verifique se o servidor está online
- Verifique a senha
- Tente novamente

### Para Acelerar o Download
- Use uma conexão com internet rápida
- Feche outros programas que usam internet

---

## 🛡️ Segurança

✅ Apenas leitura (SCP)  
✅ Sem alterações no servidor  
✅ Sem exclusão de arquivos  
✅ Conexão segura (SSH)  

---

## ✨ Conclusão

Use o comando correto acima e os vídeos serão baixados com sucesso!

```powershell
scp -r root@142.93.206.128:/tmp/videos_backup/* "C:\Users\Usuario\Desktop\Site_Dojo_final_15_10_2025\Aula_video\"
```

---

**Status**: ✅ Corrigido  
**Data**: 16 de Outubro de 2025  
**Comando**: Pronto para usar

