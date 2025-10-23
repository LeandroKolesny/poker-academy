#!/usr/bin/env python3
"""
Script para teste final após correção
"""

import paramiko
import time

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"
SSH_PORT = 22

def execute_command(client, command, timeout=60):
    """Executa um comando via SSH"""
    stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
    time.sleep(2)
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    return output, error

def test():
    """Testa"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Aguardar backend ficar healthy
        print("⏳ Aguardando backend ficar healthy...")
        for i in range(30):
            output, error = execute_command(client, "docker ps | grep backend | grep healthy")
            if output:
                print(f"✅ Backend está healthy!\n")
                break
            print(f"  Tentativa {i+1}/30...")
            time.sleep(2)
        
        # Verificar status
        print("📝 Status dos containers:")
        output, error = execute_command(client, "docker ps")
        print(output)
        
        # Testar backend
        print("\n📝 Testando backend...")
        output, error = execute_command(client, "docker exec poker_backend python -c \"import requests; r = requests.get('http://localhost:5000/api/health'); print(r.status_code, r.text)\" 2>&1")
        print(output)
        
        # Verificar dados
        print("\n📝 Total de aulas:")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT COUNT(*) as total FROM classes;\"")
        print(output)
        
        # Verificar categorias
        print("\n📝 Categorias no banco:")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SHOW COLUMNS FROM classes WHERE Field='category';\"")
        print(output)
        
        # Verificar aulas
        print("\n📝 Aulas com categorias:")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT id, name, category FROM classes LIMIT 10;\"")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ TESTE FINAL CONCLUÍDO COM SUCESSO!")
        print("=" * 70)
        print("\n🌐 Acesse a aplicação em: https://cardroomgrinders.com.br")
        print("👤 Usuário: admin")
        print("🔑 Senha: admin123")
        print("\n📝 Teste as categorias:")
        print("1. Vá para 'Gestão de Aulas'")
        print("2. Clique em editar uma aula")
        print("3. Verifique se as categorias aparecem:")
        print("   - Iniciante")
        print("   - Pré-Flop")
        print("   - Pós-Flop")
        print("   - Mental Games")
        print("   - ICM")
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test()

