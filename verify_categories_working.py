#!/usr/bin/env python3
"""
Script para verificar se as categorias estão funcionando
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

def verify():
    """Verifica"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar se o backend está respondendo
        print("📝 Testando backend...")
        output, error = execute_command(client, "docker exec poker_backend python -c \"import requests; r = requests.get('http://localhost:5000/api/health'); print(r.status_code, r.text)\" 2>&1 || echo 'Erro'")
        print(output)
        
        # Verificar categorias no banco
        print("\n📝 Verificando categorias no banco de dados...")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT COLUMN_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='classes' AND COLUMN_NAME='category';\"")
        print(output)
        
        # Verificar aulas
        print("\n📝 Verificando aulas...")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 poker_academy -e \"SELECT COUNT(*) as total, GROUP_CONCAT(DISTINCT category) as categorias FROM classes;\"")
        print(output)
        
        # Verificar arquivo ClassManagement.js
        print("\n📝 Verificando arquivo ClassManagement.js no servidor...")
        output, error = execute_command(client, "grep -A5 'getCategoryName' /root/Dojo_Deploy/poker-academy/poker-academy/src/components/admin/ClassManagement.js | head -20")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ VERIFICAÇÃO CONCLUÍDA!")
        print("=" * 70)
        print("\n📝 Próximos passos:")
        print("1. Acesse https://cardroomgrinders.com.br")
        print("2. Faça login com admin/admin123")
        print("3. Vá para 'Gestão de Aulas'")
        print("4. Clique em editar uma aula existente")
        print("5. Verifique se as categorias aparecem no dropdown:")
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
    verify()

