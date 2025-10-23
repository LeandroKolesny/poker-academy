#!/usr/bin/env python3
"""
Script para extrair e verificar o conteúdo do main.js
"""
import paramiko
import subprocess
import os

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("🔌 Conectando ao servidor...")
client.connect('142.93.206.128', username='root', password='DojoShh159357')
print("✅ Conectado!")

# Copiar o arquivo main.js para a máquina local
print("\n📥 Copiando main.js do servidor...")
sftp = client.open_sftp()

# Primeiro, obter o nome do arquivo
stdin, stdout, stderr = client.exec_command("ls /root/Dojo_Deploy/poker-academy/poker-academy/build/static/js/main.*.js")
output = stdout.read().decode('utf-8').strip()
main_file = output.split('\n')[0] if output else None

if main_file:
    print(f"Arquivo encontrado: {main_file}")
    
    # Copiar para local
    local_path = "main_js_temp.js"
    sftp.get(main_file, local_path)
    print(f"✅ Arquivo copiado para {local_path}")
    
    # Procurar por strings importantes
    print("\n🔍 Procurando por strings importantes...")
    
    with open(local_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Procurar por 'monthly-database'
    if 'monthly-database' in content:
        print("✅ 'monthly-database' encontrado")
    else:
        print("❌ 'monthly-database' NÃO encontrado")
    
    # Procurar por '/student/catalog'
    if '/student/catalog' in content:
        print("✅ '/student/catalog' encontrado")
    else:
        print("❌ '/student/catalog' NÃO encontrado")
    
    # Procurar por 'to="catalog"'
    if 'to="catalog"' in content:
        print("⚠️  'to=\"catalog\"' encontrado (caminho relativo)")
    else:
        print("✅ Sem 'to=\"catalog\"' (caminhos relativos removidos)")
    
    # Limpar arquivo temporário
    os.remove(local_path)
    print("\n✅ Arquivo temporário removido")
else:
    print("❌ Arquivo main.js não encontrado")

sftp.close()
client.close()
print("\n✅ Verificação concluída!")

