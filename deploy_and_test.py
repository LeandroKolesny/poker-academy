#!/usr/bin/env python3
"""
Script para fazer deploy e testar o site
"""
import paramiko
import time
import os

def execute_command(client, command, timeout=120):
    """Executa um comando via SSH"""
    print(f"\n📝 Executando: {command}")
    stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
    output = stdout.read().decode('utf-8', errors='replace')
    error = stderr.read().decode('utf-8', errors='replace')
    return output, error

def deploy_and_test():
    """Faz deploy e testa"""
    
    # Conectar ao servidor
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    print("🔌 Conectando ao servidor...")
    client.connect('142.93.206.128', username='root', password='DojoShh159357')
    print("✅ Conectado!")
    
    # Copiar arquivo VideoPlayer.js
    print("\n📁 Copiando arquivo VideoPlayer.js...")
    sftp = client.open_sftp()
    
    local_file = os.path.abspath('poker-academy/src/components/shared/VideoPlayer.js')
    remote_file = '/root/Dojo_Deploy/poker-academy/poker-academy/src/components/shared/VideoPlayer.js'
    
    print(f"   Local: {local_file}")
    print(f"   Remote: {remote_file}")
    
    sftp.put(local_file, remote_file)
    
    # Copiar arquivo Catalog.js
    print("\n📁 Copiando arquivo Catalog.js...")
    local_file = os.path.abspath('poker-academy/src/components/student/Catalog.js')
    remote_file = '/root/Dojo_Deploy/poker-academy/poker-academy/src/components/student/Catalog.js'

    print(f"   Local: {local_file}")
    print(f"   Remote: {remote_file}")

    sftp.put(local_file, remote_file)

    # Copiar arquivo History.js
    print("\n📁 Copiando arquivo History.js...")
    local_file = os.path.abspath('poker-academy/src/components/student/History.js')
    remote_file = '/root/Dojo_Deploy/poker-academy/poker-academy/src/components/student/History.js'

    print(f"   Local: {local_file}")
    print(f"   Remote: {remote_file}")

    sftp.put(local_file, remote_file)

    # Copiar arquivo MonthlyDatabase.js
    print("\n📁 Copiando arquivo MonthlyDatabase.js...")
    local_file = os.path.abspath('poker-academy/src/components/student/MonthlyDatabase.js')
    remote_file = '/root/Dojo_Deploy/poker-academy/poker-academy/src/components/student/MonthlyDatabase.js'

    print(f"   Local: {local_file}")
    print(f"   Remote: {remote_file}")

    if os.path.exists(local_file):
        sftp.put(local_file, remote_file)
        print("✅ MonthlyDatabase.js copiado!")
    else:
        print(f"⚠️  Arquivo não encontrado: {local_file}")

    # Copiar arquivo AdminMonthlyDatabase.js
    print("\n📁 Copiando arquivo AdminMonthlyDatabase.js...")
    local_file = os.path.abspath('poker-academy/src/components/admin/AdminMonthlyDatabase.js')
    remote_file = '/root/Dojo_Deploy/poker-academy/poker-academy/src/components/admin/AdminMonthlyDatabase.js'

    print(f"   Local: {local_file}")
    print(f"   Remote: {remote_file}")

    if os.path.exists(local_file):
        sftp.put(local_file, remote_file)
        print("✅ AdminMonthlyDatabase.js copiado!")
    else:
        print(f"⚠️  Arquivo não encontrado: {local_file}")

    # Copiar arquivo Sidebar.js
    print("\n📁 Copiando arquivo Sidebar.js...")
    local_file = os.path.abspath('poker-academy/src/components/shared/Sidebar.js')
    remote_file = '/root/Dojo_Deploy/poker-academy/poker-academy/src/components/shared/Sidebar.js'

    print(f"   Local: {local_file}")
    print(f"   Remote: {remote_file}")

    if os.path.exists(local_file):
        sftp.put(local_file, remote_file)
        print("✅ Sidebar.js copiado!")
    else:
        print(f"⚠️  Arquivo não encontrado: {local_file}")

    # Copiar arquivo AdminPanel.js
    print("\n📁 Copiando arquivo AdminPanel.js...")
    local_file = os.path.abspath('poker-academy/src/components/admin/AdminPanel.js')
    remote_file = '/root/Dojo_Deploy/poker-academy/poker-academy/src/components/admin/AdminPanel.js'

    print(f"   Local: {local_file}")
    print(f"   Remote: {remote_file}")

    if os.path.exists(local_file):
        sftp.put(local_file, remote_file)
        print("✅ AdminPanel.js copiado!")
    else:
        print(f"⚠️  Arquivo não encontrado: {local_file}")

    # Copiar arquivo models.py para o diretório correto do Docker
    print("\n📁 Copiando arquivo models.py...")
    local_file = os.path.abspath(os.path.join('poker-academy-backend', 'poker_academy_api', 'src', 'models.py'))
    remote_file = '/root/Dojo_Deploy/poker-academy/poker-academy-backend/poker_academy_api/src/models.py'

    print(f"   Local: {local_file}")
    print(f"   Remote: {remote_file}")

    if os.path.exists(local_file):
        try:
            sftp.put(local_file, remote_file)
            print("✅ models.py copiado!")
        except Exception as e:
            print(f"⚠️  Erro ao copiar models.py: {e}")
    else:
        print(f"⚠️  Arquivo não encontrado: {local_file}")

    # Copiar arquivo graphs_routes.py para o diretório correto do Docker
    print("\n📁 Copiando arquivo graphs_routes.py...")
    local_file = os.path.abspath(os.path.join('poker-academy-backend', 'poker_academy_api', 'src', 'routes', 'graphs_routes.py'))
    remote_file = '/root/Dojo_Deploy/poker-academy/poker-academy-backend/poker_academy_api/src/routes/graphs_routes.py'

    print(f"   Local: {local_file}")
    print(f"   Remote: {remote_file}")

    if os.path.exists(local_file):
        try:
            sftp.put(local_file, remote_file)
            print("✅ graphs_routes.py copiado!")
        except Exception as e:
            print(f"⚠️  Erro ao copiar graphs_routes.py: {e}")
            print(f"   Tentando criar diretório remoto...")
            try:
                execute_command(client, f"mkdir -p {os.path.dirname(remote_file)}")
                sftp.put(local_file, remote_file)
                print("✅ graphs_routes.py copiado após criar diretório!")
            except Exception as e2:
                print(f"❌ Erro ao copiar mesmo após criar diretório: {e2}")
    else:
        print(f"⚠️  Arquivo não encontrado: {local_file}")

    # Copiar arquivo database_routes.py para o diretório correto do Docker
    print("\n📁 Copiando arquivo database_routes.py...")
    local_file = os.path.abspath(os.path.join('poker-academy-backend', 'poker_academy_api', 'src', 'routes', 'database_routes.py'))
    remote_file = '/root/Dojo_Deploy/poker-academy/poker-academy-backend/poker_academy_api/src/routes/database_routes.py'

    print(f"   Local: {local_file}")
    print(f"   Remote: {remote_file}")

    if os.path.exists(local_file):
        try:
            sftp.put(local_file, remote_file)
            print("✅ database_routes.py copiado!")
        except Exception as e:
            print(f"⚠️  Erro ao copiar database_routes.py: {e}")
    else:
        print(f"⚠️  Arquivo não encontrado: {local_file}")

    # Copiar docker-compose.yml
    print("\n📁 Copiando arquivo docker-compose.yml...")
    local_file = os.path.abspath('docker-compose.yml')
    remote_file = '/root/Dojo_Deploy/poker-academy/docker-compose.yml'

    print(f"   Local: {local_file}")
    print(f"   Remote: {remote_file}")

    if os.path.exists(local_file):
        try:
            sftp.put(local_file, remote_file)
            print("✅ docker-compose.yml copiado!")
        except Exception as e:
            print(f"⚠️  Erro ao copiar docker-compose.yml: {e}")
    else:
        print(f"⚠️  Arquivo não encontrado: {local_file}")

    sftp.close()
    print("✅ Arquivos copiados!")
    
    # Parar containers
    print("\n🛑 Parando containers...")
    output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose down")
    print(output)
    
    time.sleep(3)
    
    # Remover imagens do frontend
    print("\n🗑️  Removendo imagem do frontend...")
    output, error = execute_command(client, "docker rmi poker-academy_frontend:latest 2>/dev/null || true")
    print(output)
    
    # Rebuild e restart
    print("\n🔨 Rebuilding containers...")
    output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d --build", timeout=300)
    print(output)
    
    if error:
        print("\n⚠️  Stderr:")
        print(error)
    
    # Aguardar containers iniciarem
    print("\n⏳ Aguardando containers iniciarem...")
    time.sleep(10)
    
    # Verificar status
    print("\n📊 Status dos containers:")
    output, error = execute_command(client, "docker ps -a")
    print(output)
    
    # Verificar logs do frontend
    print("\n📝 Logs do frontend (últimas 20 linhas):")
    output, error = execute_command(client, "docker logs poker_frontend 2>&1 | tail -20")
    print(output)
    
    # Testar acesso
    print("\n🧪 Testando acesso ao site...")
    output, error = execute_command(client, "curl -s -o /dev/null -w 'Status: %{http_code}\\n' https://cardroomgrinders.com.br")
    print(output)
    
    client.close()
    print("\n✅ Deploy concluído!")

if __name__ == "__main__":
    deploy_and_test()

