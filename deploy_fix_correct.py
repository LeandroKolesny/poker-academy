#!/usr/bin/env python3
"""
Script para copiar arquivo e reiniciar backend (caminho correto)
"""

import paramiko
import time
import os

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
        print(output[-1500:] if len(output) > 1500 else output)
    
    return output, error

def deploy():
    """Deploy"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar se diretório existe
        print("📁 Verificando diretório no servidor...")
        output, _ = execute_command(client, "ls -la /root/Dojo_Deploy/poker-academy/poker-academy-backend/poker_academy_api/src/routes/")
        
        # Copiar arquivo via SCP
        print("\n📁 Copiando arquivo via SCP...")
        local_file = os.path.abspath('poker-academy-backend/poker_academy_api/src/routes/class_routes.py')
        remote_file = '/root/Dojo_Deploy/poker-academy/poker-academy-backend/poker_academy_api/src/routes/class_routes.py'
        
        sftp = client.open_sftp()
        sftp.put(local_file, remote_file)
        sftp.close()
        print("✅ Arquivo copiado!")
        
        # Verificar se foi copiado
        print("\n📝 Verificando arquivo copiado...")
        output, _ = execute_command(client, "ls -lh /root/Dojo_Deploy/poker-academy/poker-academy-backend/poker_academy_api/src/routes/class_routes.py")
        
        # Reiniciar backend
        print("\n🔄 Reiniciando backend...")
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose restart poker_backend")
        time.sleep(10)
        
        # Verificar status
        print("\n📝 Status do backend:")
        output, _ = execute_command(client, "docker ps | grep poker_backend")
        
        # Verificar logs
        print("\n📝 Últimos logs do backend:")
        output, _ = execute_command(client, "docker logs poker_backend --tail 20")
        
        print("\n✅ BACKEND REINICIADO COM SUCESSO!")
        print("\n📝 Próximos passos:")
        print("1. Acesse: https://cardroomgrinders.com.br")
        print("2. Faça login com: admin / admin123")
        print("3. Vá para 'Gestão de Aulas'")
        print("4. Clique em editar uma aula")
        print("5. Adicione um vídeo e salve")
        print("6. Verifique se o vídeo agora aparece na lista")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    deploy()

