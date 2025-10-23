#!/usr/bin/env python3
"""
Script para verificar se models.py foi copiado corretamente
"""
import paramiko

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print("🔌 Conectando ao servidor...")
    ssh.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)
    print("✅ Conectado!")
    
    # Verificar arquivo no servidor
    print("\n📝 Verificando models.py no servidor:")
    stdin, stdout, stderr = ssh.exec_command("head -5 /root/Dojo_Deploy/poker-academy/poker_academy_api/src/models.py")
    print(stdout.read().decode())
    
    # Verificar arquivo dentro do container
    print("\n📝 Verificando models.py dentro do container:")
    stdin, stdout, stderr = ssh.exec_command("cd /root/Dojo_Deploy/poker-academy && docker exec poker_backend head -5 /app/src/models.py")
    print(stdout.read().decode())
    
    # Procurar por 'student = db.relationship' no arquivo do container
    print("\n🔍 Procurando por 'student = db.relationship' no container:")
    stdin, stdout, stderr = ssh.exec_command("cd /root/Dojo_Deploy/poker-academy && docker exec poker_backend grep -n 'student = db.relationship' /app/src/models.py")
    output = stdout.read().decode()
    if output:
        print(f"❌ ENCONTRADO (não deveria estar): {output}")
    else:
        print("✅ NÃO ENCONTRADO (correto!)")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
finally:
    ssh.close()

