#!/usr/bin/env python3
import paramiko
import time

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('142.93.206.128', username='root', password='DojoShh159357')

print('⏳ Aguardando 10 segundos para containers estabilizarem...')
time.sleep(10)

print('\n📝 Verificando logs do frontend:\n')
stdin, stdout, stderr = client.exec_command('docker logs poker_frontend 2>&1 | tail -30')
output = stdout.read().decode('utf-8')
print(output)

print('\n\n🔍 Procurando por /catalog/catalog nos logs:\n')
stdin, stdout, stderr = client.exec_command('docker logs poker_frontend 2>&1 | grep -i "catalog/catalog" | head -3')
output = stdout.read().decode('utf-8')
if output.strip():
    print('❌ ENCONTRADO /catalog/catalog:')
    print(output)
else:
    print('✅ NÃO ENCONTRADO /catalog/catalog - PROBLEMA RESOLVIDO!')

print('\n\n📝 Verificando logs do backend:\n')
stdin, stdout, stderr = client.exec_command('docker logs poker_backend 2>&1 | tail -20')
output = stdout.read().decode('utf-8')
print(output)

client.close()
print('\n✅ Teste concluído!')

