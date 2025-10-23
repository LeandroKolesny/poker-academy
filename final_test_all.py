#!/usr/bin/env python3
"""
Script para teste final completo
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

def test_all():
    """Testa tudo"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar dados das aulas
        print("📊 Verificando dados das aulas no banco:")
        output, _ = execute_command(client, """
docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "
SELECT id, name, instructor_id, date, video_path, category FROM classes LIMIT 5;
"
""")
        
        # Verificar instrutores
        print("\n👨‍🏫 Verificando instrutores:")
        output, _ = execute_command(client, """
docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "
SELECT id, name FROM users WHERE type='admin' LIMIT 5;
"
""")
        
        # Verificar status do frontend
        print("\n🌐 Status do frontend:")
        output, _ = execute_command(client, "docker ps | grep poker_frontend")
        
        # Verificar status do backend
        print("\n⚙️ Status do backend:")
        output, _ = execute_command(client, "docker ps | grep poker_backend")
        
        print("\n✅ TUDO PRONTO PARA TESTE!")
        print("\n📝 Próximos passos:")
        print("1. Acesse: https://cardroomgrinders.com.br")
        print("2. Faça login com: admin / admin123")
        print("3. Vá para 'Gestão de Aulas'")
        print("4. Clique em editar uma aula")
        print("5. Modifique os dados (instrutor, data, vídeo)")
        print("6. Clique em salvar")
        print("7. Verifique se os dados foram atualizados")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_all()

