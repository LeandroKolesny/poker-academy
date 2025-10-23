#!/usr/bin/env python3
"""
Script para testar se o frontend foi reconstruído
"""
import paramiko
import time

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("🔌 Conectando ao servidor...")
client.connect('142.93.206.128', username='root', password='DojoShh159357')
print("✅ Conectado!")

# Aguardar um pouco para o frontend iniciar
print("\n⏳ Aguardando 15 segundos para o frontend iniciar...")
time.sleep(15)

# Verificar se o frontend está respondendo
print("\n🧪 Testando se o frontend está respondendo...")
command = "curl -s -o /dev/null -w '%{http_code}' http://poker_frontend:80/"

stdin, stdout, stderr = client.exec_command(command)
output = stdout.read().decode('utf-8')

print(f"Status HTTP: {output}")

if output == "200":
    print("✅ Frontend está respondendo!")
else:
    print("❌ Frontend não está respondendo corretamente")

# Verificar se o arquivo build contém a rota de database
print("\n🔍 Verificando se o build contém 'monthly-database'...")
command = "docker exec poker_frontend grep -r 'monthly-database' /usr/share/nginx/html/ 2>/dev/null | head -3"

stdin, stdout, stderr = client.exec_command(command)
output = stdout.read().decode('utf-8')

if output:
    print("✅ Encontrado 'monthly-database' no build:")
    print(output)
else:
    print("❌ Não encontrado 'monthly-database' no build")

client.close()
print("\n✅ Teste concluído!")

