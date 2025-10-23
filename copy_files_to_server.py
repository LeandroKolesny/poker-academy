#!/usr/bin/env python3
"""
Script para copiar arquivos atualizados para o servidor
"""

import paramiko
import os

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"
SSH_PORT = 22

def copy_files():
    """Copia arquivos para o servidor"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Abrir SFTP
        sftp = client.open_sftp()
        
        # Copiar models.py
        print("📝 Copiando models.py...")
        local_models = r"C:\Users\Usuario\Desktop\site_Dojo_Final\poker-academy-backend\poker_academy_api\src\models.py"
        remote_models = "/root/Dojo_Deploy/poker-academy/poker-academy-backend/poker_academy_api/src/models.py"
        sftp.put(local_models, remote_models)
        print("✅ models.py copiado!")
        
        # Copiar class_routes.py
        print("📝 Copiando class_routes.py...")
        local_routes = r"C:\Users\Usuario\Desktop\site_Dojo_Final\poker-academy-backend\poker_academy_api\src\routes\class_routes.py"
        remote_routes = "/root/Dojo_Deploy/poker-academy/poker-academy-backend/poker_academy_api/src/routes/class_routes.py"
        sftp.put(local_routes, remote_routes)
        print("✅ class_routes.py copiado!")
        
        sftp.close()
        client.close()
        
        print("\n✅ Arquivos copiados com sucesso!")
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    copy_files()

