#!/usr/bin/env python3
"""
Script para testar a API de gráficos e ver os logs do backend
"""
import paramiko
import time
import requests
import json
import io

def test_graphs_api():
    """Testa a API de gráficos e mostra os logs"""

    # Conectar ao servidor
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print("🔌 Conectando ao servidor...")
    client.connect('142.93.206.128', username='root', password='DojoShh159357')
    print("✅ Conectado!")

    # Token do usuário leandrokoles
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyNiwidXNlcl90eXBlIjoic3R1ZGVudCIsImV4cCI6MTc2MDczMDc2NywiaWF0IjoxNzYwNjQ0MzY3fQ.YOl6GpSLLppOcO0T4e-i4fQ3WqOtg6yOY7foOXirTAg"

    headers = {
        'Authorization': f'Bearer {token}',
    }

    # Criar uma imagem PNG simples (sem PIL)
    print("\n📸 Criando imagem de teste...")
    # PNG header + minimal valid PNG data
    png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18\r\xb5\x00\x00\x00\x00IEND\xaeB`\x82'
    img_bytes = io.BytesIO(png_data)
    
    # Fazer upload
    print("\n📤 Fazendo upload do gráfico...")
    files = {
        'file': ('test_graph.png', img_bytes, 'image/png')
    }
    data = {
        'month': 'jan',
        'year': '2025'
    }
    
    try:
        response = requests.post(
            'https://cardroomgrinders.com.br/api/student/graphs/upload',
            headers=headers,
            files=files,
            data=data,
            verify=False
        )
        print(f"📊 Upload Status Code: {response.status_code}")
        print(f"📊 Upload Response: {response.text}")
    except Exception as e:
        print(f"❌ Erro no upload: {e}")
    
    # Aguardar um pouco
    time.sleep(2)
    
    # Fazer requisição para buscar gráficos
    print("\n🔍 Fazendo requisição para /api/student/graphs...")
    
    try:
        response = requests.get(
            'https://cardroomgrinders.com.br/api/student/graphs?year=2025',
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
    
    stdin, stdout, stderr = client.exec_command("cd /root/Dojo_Deploy/poker-academy && docker-compose logs 2>&1 | tail -300")
    logs = stdout.read().decode('utf-8', errors='replace')
    
    print(logs)
    print("="*80)
    
    client.close()
    print("\n✅ Teste concluído!")

if __name__ == '__main__':
    test_graphs_api()

