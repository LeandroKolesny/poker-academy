#!/usr/bin/env python3
"""
Script para testar upload de vídeo
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

def test():
    """Testa"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar vídeos salvos
        print("📁 Vídeos salvos no servidor:")
        output, _ = execute_command(client, "ls -lh /root/Dojo_Deploy/poker-academy/uploads/ | tail -10")
        
        # Verificar dados da aula 1 no banco
        print("\n📊 Dados da aula 1 no banco:")
        output, _ = execute_command(client, """
docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "
SELECT id, name, instructor_id, video_path, category FROM classes WHERE id=1;
"
""")
        
        # Verificar logs do backend
        print("\n📝 Últimos logs do backend:")
        output, _ = execute_command(client, "docker logs poker_backend --tail 50 | grep -E 'upload|video|class' | tail -20")
        
        # Verificar tamanho do volume de uploads
        print("\n📊 Tamanho do volume de uploads:")
        output, _ = execute_command(client, "du -sh /var/lib/docker/volumes/poker-academy_backend_uploads/_data/")
        
        # Listar arquivos no volume
        print("\n📁 Arquivos no volume de uploads:")
        output, _ = execute_command(client, "ls -lh /var/lib/docker/volumes/poker-academy_backend_uploads/_data/ | tail -10")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test()

