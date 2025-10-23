#!/usr/bin/env python3
import paramiko
import time
import requests
import json

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('🧪 TESTE COMPLETO: UPLOAD + DOWNLOAD\n')
print('='*60)

print('\n📝 1. Verificar arquivos no servidor\n')
stdin, stdout, stderr = client.exec_command('docker exec poker_backend ls -lh /app/uploads/databases/')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 2. Verificar registros no banco\n')
stdin, stdout, stderr = client.exec_command('docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "SELECT id, student_id, month, year, file_url FROM student_database ORDER BY id DESC LIMIT 3;"')
output = stdout.read().decode('utf-8', errors='ignore')
print(output)

print('\n📝 3. Testar rota de download com curl (arquivo existente)\n')
stdin, stdout, stderr = client.exec_command('curl -s -I https://cardroomgrinders.com.br/api/uploads/databases/db_26_jan_2025_59dd7852.zip 2>&1 | head -10')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 4. Verificar logs do backend para erros\n')
stdin, stdout, stderr = client.exec_command('docker logs poker_backend 2>&1 | grep -i "erro\|error\|404" | tail -5')
output = stdout.read().decode('utf-8')
if output.strip():
    print(output)
else:
    print("✅ Nenhum erro encontrado!")

print('\n' + '='*60)
print('\n🎯 PRÓXIMO PASSO: Teste manual no navegador')
print('   1. Abra https://cardroomgrinders.com.br')
print('   2. Faça login: leandrokoles / leandrokoles123456')
print('   3. Clique em "Database Mensal"')
print('   4. Faça upload de um novo arquivo .zip em um mês diferente')
print('   5. Clique no botão de download')
print('   6. Verifique se o arquivo foi baixado corretamente')

client.close()

