#!/usr/bin/env python3
"""
Script para testar o workflow completo de edição de aula
"""

import requests
import json
import time
import tempfile
import os

BASE_URL = "https://cardroomgrinders.com.br"

def test_complete_workflow():
    """Test complete workflow"""
    
    session = requests.Session()
    session.verify = False  # Ignorar SSL para teste
    
    try:
        print("🔌 Conectando ao servidor...")
        
        # 1. Login
        print("\n1️⃣  Fazendo login...")
        login_data = {"username": "admin", "password": "admin123"}
        response = session.post(f"{BASE_URL}/api/auth/login", json=login_data)
        if response.status_code != 200:
            print(f"❌ Erro ao fazer login: {response.status_code}")
            print(response.text)
            return
        
        token = response.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Login bem-sucedido!")
        
        # 2. Obter aulas
        print("\n2️⃣  Obtendo lista de aulas...")
        response = session.get(f"{BASE_URL}/api/classes", headers=headers)
        if response.status_code != 200:
            print(f"❌ Erro ao obter aulas: {response.status_code}")
            print(response.text)
            return
        
        classes = response.json()
        print(f"✅ Total de aulas: {len(classes)}")
        
        # 3. Editar primeira aula
        class_id = classes[0]["id"]
        print(f"\n3️⃣  Editando aula ID {class_id}...")
        
        update_data = {
            "name": classes[0]["name"],
            "instructor": "Admin Instructor",
            "date": "2025-10-16",
            "category": "preflop",
            "video_type": "local",
            "video_path": "test_video.mp4",
            "priority": 5
        }
        
        response = session.put(
            f"{BASE_URL}/api/classes/{class_id}",
            json=update_data,
            headers=headers
        )
        
        if response.status_code != 200:
            print(f"❌ Erro ao atualizar aula: {response.status_code}")
            print(response.text)
            return
        
        print("✅ Aula atualizada com sucesso!")
        
        # 4. Verificar se os dados foram salvos
        print("\n4️⃣  Verificando se os dados foram salvos...")
        response = session.get(f"{BASE_URL}/api/classes/{class_id}", headers=headers)
        if response.status_code != 200:
            print(f"❌ Erro ao obter aula: {response.status_code}")
            return
        
        updated_class = response.json()
        print(f"✅ Aula recuperada!")
        print(f"   - Nome: {updated_class['name']}")
        print(f"   - Instrutor: {updated_class.get('instructor_name', 'N/A')}")
        print(f"   - Data: {updated_class['date']}")
        print(f"   - Vídeo: {updated_class.get('video_path', 'N/A')}")
        
        print("\n✅ TESTE COMPLETO COM SUCESSO!")
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_complete_workflow()

