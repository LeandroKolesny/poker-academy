#!/usr/bin/env python3
"""
Script simples para testar rotas
"""
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("🔌 Conectando ao servidor...")
client.connect('142.93.206.128', username='root', password='DojoShh159357')
print("✅ Conectado!")

# Testar rota de graphs (que sabemos que funciona)
print("\n🧪 Testando rota de graphs...")
command = "curl -s -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyNiwidXNlcl90eXBlIjoic3R1ZGVudCIsImV4cCI6MTc2MDc1MTc3NCwiaWF0IjoxNzYwNjY1Mzc0fQ.GsY7Mmt0fCerSoshG_ugOGm66XQnOJA6rSXSd0nj-40' http://poker_backend:5000/api/student/graphs?year=2025 | head -20"

stdin, stdout, stderr = client.exec_command(command)
output = stdout.read().decode('utf-8')

print(f"Graphs response:\n{output}")

# Testar rota de database
print("\n🧪 Testando rota de database...")
command = "curl -s -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyNiwidXNlcl90eXBlIjoic3R1ZGVudCIsImV4cCI6MTc2MDc1MTc3NCwiaWF0IjoxNzYwNjY1Mzc0fQ.GsY7Mmt0fCerSoshG_ugOGm66XQnOJA6rSXSd0nj-40' http://poker_backend:5000/api/student/database?year=2025 | head -20"

stdin, stdout, stderr = client.exec_command(command)
output = stdout.read().decode('utf-8')

print(f"Database response:\n{output}")

client.close()
print("\n✅ Teste concluído!")

