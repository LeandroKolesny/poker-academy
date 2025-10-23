#!/usr/bin/env python3
"""
Script para testar upload de vídeo no servidor
"""

import requests
import json
import time

BASE_URL = "https://cardroomgrinders.com.br"
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

def test_video_upload():
    """Test video upload"""
    
    try:
        print("🔌 Conectando ao servidor...")
        
        # 1. Login
        print("\n1️⃣  Fazendo login...")
        login_data = {
            "username": ADMIN_USER,
            "password": ADMIN_PASS
        }
        
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=login_data,
            verify=False
        )
        
        if response.status_code != 200:
            print(f"❌ Erro no login: {response.status_code}")
            print(response.text)
            return
        
        token = response.json().get("token")
        print(f"✅ Login bem-sucedido! Token: {token[:20]}...")
        
        # 2. Obter lista de aulas
        print("\n2️⃣  Obtendo lista de aulas...")
        headers = {"Authorization": f"Bearer {token}"}
        
        response = requests.get(
            f"{BASE_URL}/api/classes",
            headers=headers,
            verify=False
        )
        
        if response.status_code != 200:
            print(f"❌ Erro ao obter aulas: {response.status_code}")
            return
        
        classes = response.json()
        print(f"✅ Total de aulas: {len(classes)}")
        
        if not classes:
            print("❌ Nenhuma aula encontrada!")
            return
        
        class_id = classes[0]["id"]
        print(f"✅ Usando aula ID: {class_id}")
        
        # 3. Criar arquivo de teste
        print("\n3️⃣  Criando arquivo de teste...")
        import tempfile
        import os
        temp_dir = tempfile.gettempdir()
        test_file = os.path.join(temp_dir, "test_video.mp4")
        with open(test_file, "wb") as f:
            f.write(b"fake video content" * 1000)  # ~18KB
        print(f"✅ Arquivo criado: {test_file}")
        
        # 4. Upload do vídeo
        print("\n4️⃣  Fazendo upload do vídeo...")
        with open(test_file, "rb") as f:
            files = {"video": f}
            response = requests.post(
                f"{BASE_URL}/api/classes/upload-video",
                files=files,
                headers={"Authorization": f"Bearer {token}"},
                verify=False
            )
        
        if response.status_code != 200:
            print(f"❌ Erro no upload: {response.status_code}")
            print(response.text)
            return
        
        upload_result = response.json()
        print(f"✅ Upload bem-sucedido!")
        print(f"📁 Resposta completa: {upload_result}")
        video_path = upload_result.get("video_path") or upload_result.get("filename")
        print(f"📁 Video path: {video_path}")
        
        # 5. Atualizar aula com vídeo
        print("\n5️⃣  Atualizando aula com vídeo...")
        update_data = {
            "name": "Teste de Upload",
            "instructor": "Test Instructor",
            "date": "2025-10-16",
            "category": "preflop",
            "video_type": "local",
            "video_path": video_path,
            "priority": 5
        }
        
        response = requests.put(
            f"{BASE_URL}/api/classes/{class_id}",
            json=update_data,
            headers=headers,
            verify=False
        )
        
        if response.status_code != 200:
            print(f"❌ Erro ao atualizar aula: {response.status_code}")
            print(response.text)
            return
        
        print(f"✅ Aula atualizada com sucesso!")
        
        # 6. Verificar se vídeo foi salvo
        print("\n6️⃣  Verificando se vídeo foi salvo...")
        response = requests.get(
            f"{BASE_URL}/api/classes/{class_id}",
            headers=headers,
            verify=False
        )
        
        if response.status_code != 200:
            print(f"❌ Erro ao obter aula: {response.status_code}")
            return
        
        class_data = response.json()
        saved_video_path = class_data.get("video_path")
        
        if saved_video_path == video_path:
            print(f"✅ Vídeo foi salvo corretamente!")
            print(f"📁 Video path salvo: {saved_video_path}")
        else:
            print(f"❌ Vídeo NÃO foi salvo!")
            print(f"📁 Esperado: {video_path}")
            print(f"📁 Obtido: {saved_video_path}")
        
        print("\n✅ TESTE COMPLETO!")
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Desabilitar SSL warning
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    test_video_upload()

