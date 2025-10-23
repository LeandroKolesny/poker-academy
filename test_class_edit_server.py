#!/usr/bin/env python3
"""
Script para testar edição de aula no servidor
"""

import paramiko
import time

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"
SSH_PORT = 22

def execute_command(client, command, timeout=120):
    """Executa um comando via SSH"""
    print(f"\n📝 Executando: {command}")
    stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
    time.sleep(1)
    
    output = stdout.read().decode('utf-8', errors='replace')
    error = stderr.read().decode('utf-8', errors='replace')
    
    if output:
        print(output[-2000:] if len(output) > 2000 else output)
    
    return output, error

def test_class_edit():
    """Testa edição de aula"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Criar script de teste
        test_script = """
import requests
import json
import urllib3
urllib3.disable_warnings()

BASE_URL = "https://cardroomgrinders.com.br"

# Login
login_data = {"username": "admin", "password": "admin123"}
r = requests.post(f"{BASE_URL}/api/login", json=login_data, verify=False)
token = r.json()['token']
print(f"✅ Login OK: {token[:20]}...")

# Buscar aulas
headers = {"Authorization": f"Bearer {token}"}
r = requests.get(f"{BASE_URL}/api/classes", headers=headers, verify=False)
classes = r.json()
print(f"✅ {len(classes)} aulas encontradas")

# Editar primeira aula
class_id = classes[0]['id']
update_data = {
    "name": classes[0]['name'],
    "instructor": "Eiji",
    "category": "preflop",
    "date": "2025-10-16",
    "priority": 5,
    "video_path": "test_video.mp4",
    "video_type": "local"
}

r = requests.put(f"{BASE_URL}/api/classes/{class_id}", json=update_data, headers=headers, verify=False)
print(f"Status: {r.status_code}")
if r.status_code == 200:
    print("✅ AULA EDITADA COM SUCESSO!")
    updated = r.json()
    print(f"  Instrutor: {updated.get('instructor_name')}")
    print(f"  Data: {updated.get('date')}")
else:
    print(f"❌ Erro: {r.text}")
"""
        
        # Salvar script no servidor
        print("📝 Criando script de teste no servidor...")
        execute_command(client, f"cat > /tmp/test_edit.py << 'EOF'\n{test_script}\nEOF")
        
        # Executar script
        print("\n🧪 Executando teste...")
        output, _ = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && python /tmp/test_edit.py")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_class_edit()

