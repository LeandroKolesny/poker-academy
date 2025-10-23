#!/usr/bin/env python3
"""
Script para restaurar arquivos no servidor via SCP
"""

import paramiko
import time
import os

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"
SSH_PORT = 22

def copy_file_via_ssh(local_path, remote_path):
    """Copia arquivo via SSH"""
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        
        sftp = client.open_sftp()
        sftp.put(local_path, remote_path)
        sftp.close()
        client.close()
        
        return True
    except Exception as e:
        print(f"❌ Erro ao copiar {local_path}: {str(e)}")
        return False

def execute_command(client, command):
    """Executa um comando via SSH"""
    stdin, stdout, stderr = client.exec_command(command)
    time.sleep(1)
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    return output, error

def restore():
    """Restaura arquivos"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Arquivos a copiar
        files_to_copy = [
            ("poker-academy/src/components/admin/ClassManagement.js", 
             "/root/Dojo_Deploy/poker-academy/poker-academy/src/components/admin/ClassManagement.js"),
            ("poker-academy/src/components/student/Catalog.js",
             "/root/Dojo_Deploy/poker-academy/poker-academy/src/components/student/Catalog.js"),
            ("poker-academy/src/components/student/History.js",
             "/root/Dojo_Deploy/poker-academy/poker-academy/src/components/student/History.js"),
        ]
        
        print("📝 Copiando arquivos para o servidor...\n")
        
        for local_file, remote_file in files_to_copy:
            print(f"📋 Copiando {local_file}...")
            
            # Verificar se arquivo local existe
            if not os.path.exists(local_file):
                print(f"❌ Arquivo local não encontrado: {local_file}\n")
                continue
            
            # Copiar arquivo
            if copy_file_via_ssh(local_file, remote_file):
                print(f"✅ {remote_file} copiado com sucesso!\n")
            else:
                print(f"❌ Erro ao copiar {remote_file}\n")
        
        # Verificar resultado
        print("\n" + "=" * 70)
        print("📋 VERIFICANDO ARQUIVOS NO SERVIDOR")
        print("=" * 70)
        
        # Verificar ClassManagement.js
        print("\n📋 ClassManagement.js:")
        output, error = execute_command(client, "grep -n 'option value=' /root/Dojo_Deploy/poker-academy/poker-academy/src/components/admin/ClassManagement.js | grep -E '(iniciantes|preflop|postflop|mental|icm)'")
        print(output if output else "Nenhuma opção encontrada")
        
        # Verificar Catalog.js
        print("\n📋 Catalog.js:")
        output, error = execute_command(client, "grep -n 'const categories' /root/Dojo_Deploy/poker-academy/poker-academy/src/components/student/Catalog.js")
        print(output if output else "Nenhuma definição encontrada")
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ RESTAURAÇÃO CONCLUÍDA!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=" * 70)
    print("Restauração de Arquivos no Servidor")
    print("=" * 70)
    print(f"\nServidor: {SSH_HOST}")
    print("\nEste script irá:")
    print("  1. Copiar ClassManagement.js")
    print("  2. Copiar Catalog.js")
    print("  3. Copiar History.js")
    print("  4. Verificar resultado")
    print("\n" + "=" * 70)
    
    input("\nPressione ENTER para continuar...")
    
    restore()

