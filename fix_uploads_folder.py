#!/usr/bin/env python3
"""
Script para corrigir pasta de uploads
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
    
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    
    if output:
        print(output)
    
    return output, error

def fix_uploads():
    """Corrige pasta de uploads"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar o que existe
        print("📝 Verificando /app/uploads:")
        output, _ = execute_command(client, "docker exec poker_backend ls -la /app/uploads/ 2>/dev/null || echo 'Não existe'")
        print(output)
        
        # Remover arquivo/diretório problemático
        print("\n🗑️  Removendo /app/uploads/videos...")
        execute_command(client, "docker exec poker_backend rm -rf /app/uploads/videos")
        
        # Criar diretório correto
        print("\n📁 Criando diretório /app/uploads/videos...")
        execute_command(client, "docker exec poker_backend mkdir -p /app/uploads/videos")
        
        # Verificar resultado
        print("\n📝 Verificando resultado:")
        output, _ = execute_command(client, "docker exec poker_backend ls -la /app/uploads/")
        print(output)
        
        # Reiniciar backend
        print("\n🔄 Reiniciando backend...")
        execute_command(client, "docker restart poker_backend")
        time.sleep(10)
        
        # Verificar status
        print("\n📝 Status do backend:")
        output, _ = execute_command(client, "docker ps | grep poker_backend")
        print(output)
        
        # Testar login
        print("\n📝 Testando login...")
        output, _ = execute_command(client, """docker exec poker_backend curl -s -X POST http://localhost:5000/api/auth/login -H 'Content-Type: application/json' -d '{"username":"admin","password":"admin123"}'""")
        print(output)
        
        if '"token"' in output:
            print("\n✅ LOGIN BEM-SUCEDIDO!")
        else:
            print("\n❌ LOGIN AINDA FALHOU")
            print("\n📝 Últimos logs:")
            output, _ = execute_command(client, "docker logs poker_backend 2>&1 | tail -30")
            print(output)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_uploads()

