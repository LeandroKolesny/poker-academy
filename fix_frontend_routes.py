#!/usr/bin/env python3
import paramiko
import time

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('142.93.206.128', username='root', password='DojoShh159357')

# Copiar arquivos do frontend
sftp = client.open_sftp()
print('📤 Copiando StudentPanel.js...')
sftp.put('poker-academy/src/components/student/StudentPanel.js', '/root/Dojo_Deploy/poker-academy/poker-academy/src/components/student/StudentPanel.js')
print('✅ StudentPanel.js copiado!')

print('📤 Copiando AdminPanel.js...')
sftp.put('poker-academy/src/components/admin/AdminPanel.js', '/root/Dojo_Deploy/poker-academy/poker-academy/src/components/admin/AdminPanel.js')
print('✅ AdminPanel.js copiado!')

sftp.close()

# Rebuild frontend
print('\n🔨 Iniciando rebuild do frontend...')
stdin, stdout, stderr = client.exec_command('cd /root/Dojo_Deploy/poker-academy && docker-compose up -d --build frontend')
output = stdout.read().decode('utf-8')
print(output)

print('\n⏳ Aguardando 30 segundos...')
time.sleep(30)

# Verificar
print('\n📝 Verificando StudentPanel.js:')
stdin, stdout, stderr = client.exec_command('grep "Navigate to" /root/Dojo_Deploy/poker-academy/poker-academy/src/components/student/StudentPanel.js')
output = stdout.read().decode('utf-8')
print(output)

client.close()
print('\n✅ Concluído!')

