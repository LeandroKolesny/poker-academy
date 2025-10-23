#!/usr/bin/env python3
import paramiko
import time

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('142.93.206.128', username='root', password='DojoShh159357')

print('📊 Verificando logs do servidor...\n')

# Verificar logs do NGINX
print('📝 Últimas requisições do NGINX:')
stdin, stdout, stderr = client.exec_command('tail -20 /var/log/nginx/access.log 2>/dev/null || echo "Log não encontrado"')
output = stdout.read().decode('utf-8')
print(output)

# Verificar se há repetição de /catalog
print('\n🔍 Procurando por /catalog/catalog nos logs:')
stdin, stdout, stderr = client.exec_command('grep -i "catalog/catalog" /var/log/nginx/access.log 2>/dev/null | tail -5 || echo "Nenhuma ocorrência encontrada"')
output = stdout.read().decode('utf-8')
print(output)

# Verificar logs do Docker
print('\n📝 Logs do container frontend:')
stdin, stdout, stderr = client.exec_command('docker logs poker_frontend 2>&1 | tail -20')
output = stdout.read().decode('utf-8')
print(output)

# Verificar se o arquivo main.js foi atualizado
print('\n📝 Verificando hash do main.js:')
stdin, stdout, stderr = client.exec_command('ls -la /usr/share/nginx/html/static/js/ | grep main')
output = stdout.read().decode('utf-8')
print(output)

client.close()
print('\n✅ Verificação concluída!')

