#!/usr/bin/env python3
"""
Script para verificar se o arquivo foi copiado corretamente
"""
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("🔌 Conectando ao servidor...")
client.connect('142.93.206.128', username='root', password='DojoShh159357')
print("✅ Conectado!")

# Verificar o conteúdo do arquivo StudentPanel.js
print("\n📁 Verificando StudentPanel.js no servidor...")
stdin, stdout, stderr = client.exec_command("grep -n 'Navigate to' /root/Dojo_Deploy/poker-academy/poker-academy/src/components/student/StudentPanel.js")
output = stdout.read().decode('utf-8')
print(output)

# Verificar se contém '/student/catalog'
print("\n🔍 Procurando por '/student/catalog'...")
stdin, stdout, stderr = client.exec_command("grep '/student/catalog' /root/Dojo_Deploy/poker-academy/poker-academy/src/components/student/StudentPanel.js")
output = stdout.read().decode('utf-8')
print(output)

# Verificar se contém 'catalog' (relativo)
print("\n🔍 Procurando por 'catalog' (relativo)...")
stdin, stdout, stderr = client.exec_command("grep 'to=\"catalog\"' /root/Dojo_Deploy/poker-academy/poker-academy/src/components/student/StudentPanel.js")
output = stdout.read().decode('utf-8')
print(output)

client.close()
print("\n✅ Verificação concluída!")

