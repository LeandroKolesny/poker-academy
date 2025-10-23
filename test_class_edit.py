#!/usr/bin/env python3
"""
Script para testar edição de aula
"""

import requests
import json
import time

BASE_URL = "https://cardroomgrinders.com.br"
LOGIN_URL = f"{BASE_URL}/api/login"
CLASSES_URL = f"{BASE_URL}/api/classes"

def test_class_edit():
    """Testa edição de aula"""
    
    try:
        print("🔌 Testando edição de aula...\n")
        
        # 1. Login
        print("1️⃣ Fazendo login...")
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        
        response = requests.post(LOGIN_URL, json=login_data, verify=False)
        print(f"Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ Erro no login: {response.text}")
            return
        
        login_response = response.json()
        token = login_response.get('token')
        print(f"✅ Login bem-sucedido! Token: {token[:20]}...\n")
        
        # 2. Buscar aulas
        print("2️⃣ Buscando aulas...")
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(CLASSES_URL, headers=headers, verify=False)
        print(f"Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ Erro ao buscar aulas: {response.text}")
            return
        
        classes = response.json()
        print(f"✅ {len(classes)} aulas encontradas\n")
        
        # 3. Editar primeira aula
        print("3️⃣ Editando primeira aula...")
        class_id = classes[0]['id']
        class_name = classes[0]['name']
        
        update_data = {
            "name": class_name,
            "instructor": "Eiji",
            "category": "preflop",
            "date": "2025-10-16",
            "priority": 5,
            "video_path": "test_video.mp4",
            "video_type": "local"
        }
        
        print(f"Atualizando aula ID {class_id}...")
        print(f"Dados: {json.dumps(update_data, indent=2)}")
        
        response = requests.put(
            f"{CLASSES_URL}/{class_id}",
            json=update_data,
            headers=headers,
            verify=False
        )
        
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.text}\n")
        
        if response.status_code == 200:
            print("✅ AULA EDITADA COM SUCESSO!")
            updated_class = response.json()
            print(f"Instrutor: {updated_class.get('instructor_name')}")
            print(f"Data: {updated_class.get('date')}")
            print(f"Vídeo: {updated_class.get('video_path')}")
        else:
            print(f"❌ Erro ao editar aula: {response.text}")
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Desabilitar aviso de SSL
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    test_class_edit()

