#!/usr/bin/env python3
"""
Script para fazer backup do banco de dados MySQL do Docker
"""
import paramiko
import os
from datetime import datetime

# Configurações
SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_KEY = r"C:\Users\Usuario\.ssh\id_rsa"
SSH_PASSWORD = "DojoShh159357"

# Criar cliente SSH
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print("🔌 Conectando ao servidor...")
    ssh.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)
    print("✅ Conectado!")
    
    # Verificar se os containers estão rodando
    print("\n📊 Verificando status dos containers...")
    stdin, stdout, stderr = ssh.exec_command("cd /root/Dojo_Deploy/poker-academy && docker-compose ps")
    print(stdout.read().decode())
    
    # Fazer backup
    print("\n💾 Fazendo backup do banco de dados...")
    backup_filename = f"poker_academy_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
    backup_path = f"/root/{backup_filename}"
    
    # Comando para fazer dump (com --no-tablespaces para evitar erro de PROCESS privilege)
    dump_cmd = f"docker exec poker_mysql mysqldump -u poker_user -pDojo@Sql159357 --no-tablespaces poker_academy > {backup_path}"
    stdin, stdout, stderr = ssh.exec_command(dump_cmd)
    error = stderr.read().decode()
    if error:
        print(f"❌ Erro ao fazer dump: {error}")
    else:
        print(f"✅ Dump criado: {backup_path}")
    
    # Verificar tamanho do arquivo
    print("\n📁 Verificando arquivo de backup...")
    stdin, stdout, stderr = ssh.exec_command(f"ls -lh {backup_path}")
    print(stdout.read().decode())
    
    # Copiar para local
    print("\n📥 Copiando backup para máquina local...")
    sftp = ssh.open_sftp()
    local_backup = f"C:/Users/Usuario/Desktop/site_Dojo_Final/backups/{backup_filename}"
    
    # Criar diretório se não existir
    os.makedirs("backups", exist_ok=True)
    
    sftp.get(backup_path, local_backup)
    print(f"✅ Backup copiado para: {local_backup}")
    
    # Verificar tamanho local
    local_size = os.path.getsize(local_backup)
    print(f"📊 Tamanho do backup local: {local_size / (1024*1024):.2f} MB")
    
    sftp.close()
    
    print("\n✅ Backup concluído com sucesso!")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
finally:
    ssh.close()

