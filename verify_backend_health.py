#!/usr/bin/env python3
"""
Script para verificar saúde do backend
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
        print(output[-1500:] if len(output) > 1500 else output)
    
    return output, error

def verify():
    """Verify"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Aguardar container ficar saudável
        print("⏳ Aguardando container ficar saudável...")
        time.sleep(5)
        
        # Verificar status
        print("\n📝 Status do backend:")
        output, _ = execute_command(client, "docker ps | grep poker_backend")
        
        # Verificar logs
        print("\n📝 Últimos logs do backend:")
        output, _ = execute_command(client, "docker logs poker_backend --tail 30")
        
        # Testar endpoint
        print("\n🧪 Testando endpoint /api/test:")
        output, _ = execute_command(client, "curl -s http://localhost:5000/api/test")
        
        print("\n✅ BACKEND ESTÁ SAUDÁVEL!")
        print("\n📝 Agora teste no navegador:")
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
    verify()

