#!/usr/bin/env python3
"""
Script para testar a API de leaks e ver os logs do backend
"""
import paramiko
import time
import requests
import json

def test_leaks_api():
    """Testa a API de leaks e mostra os logs"""
    
    # Conectar ao servidor
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    print("🔌 Conectando ao servidor...")
    client.connect('142.93.206.128', username='root', password='DojoShh159357')
    print("✅ Conectado!")
    
    # Limpar logs anteriores
    print("\n🗑️  Limpando logs anteriores...")
    stdin, stdout, stderr = client.exec_command("cd /root/Dojo_Deploy/poker-academy && docker-compose logs --tail=0 poker_backend")
    stdout.read()
    
    time.sleep(1)
    
    # Fazer requisição para a API
    print("\n🔍 Fazendo requisição para /api/student/leaks...")
    
    # Token do usuário leandrokoles (você pode pegar do localStorage)
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyNiwidXNlcl90eXBlIjoic3R1ZGVudCIsImV4cCI6MTc2MDczMDc2NywiaWF0IjoxNzYwNjQ0MzY3fQ.YOl6GpSLLppOcO0T4e-i4fQ3WqOtg6yOY7foOXirTAg"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(
            'https://cardroomgrinders.com.br/api/student/leaks?year=2025',
            headers=headers,
            verify=False
        )
        print(f"📊 Status Code: {response.status_code}")
        print(f"📊 Response: {response.text}")
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
    
    # Aguardar um pouco para os logs serem escritos
    time.sleep(2)
    
    # Ler logs do backend
    print("\n📝 Lendo logs do backend...")
    print("="*80)

    # Primeiro, listar os containers
    stdin, stdout, stderr = client.exec_command("cd /root/Dojo_Deploy/poker-academy && docker-compose ps")
    containers = stdout.read().decode('utf-8', errors='replace')
    print("Containers:")
    print(containers)

    # Agora ler os logs
    stdin, stdout, stderr = client.exec_command("cd /root/Dojo_Deploy/poker-academy && docker-compose logs 2>&1 | tail -300")
    logs = stdout.read().decode('utf-8', errors='replace')
    
    print(logs)
    print("="*80)
    
    client.close()
    print("\n✅ Teste concluído!")

if __name__ == '__main__':
    test_leaks_api()

