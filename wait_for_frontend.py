#!/usr/bin/env python3
"""
Script para aguardar o frontend estar pronto
"""
import paramiko
import time

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("🔌 Conectando ao servidor...")
client.connect('142.93.206.128', username='root', password='DojoShh159357')
print("✅ Conectado!")

# Aguardar o frontend estar pronto
print("\n⏳ Aguardando o frontend estar pronto...")
for i in range(60):
    command = "curl -s -o /dev/null -w '%{http_code}' http://poker_frontend:80/"
    stdin, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode('utf-8').strip()
    
    if output == "200":
        print(f"✅ Frontend está pronto! (tentativa {i+1})")
        break
    else:
        print(f"⏳ Aguardando... (tentativa {i+1}, status: {output})")
        time.sleep(1)
else:
    print("❌ Frontend não ficou pronto após 60 segundos")

client.close()
print("\n✅ Verificação concluída!")

