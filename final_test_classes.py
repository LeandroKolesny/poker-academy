#!/usr/bin/env python3
"""
Script para testar se as aulas estão carregando corretamente
"""

import paramiko
import time
import json

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

def test_classes():
    """Testa se as aulas estão carregando corretamente"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Fazer login
        print("📝 Fazendo login...")
        output, _ = execute_command(client, """docker exec poker_backend curl -s -X POST http://localhost:5000/api/auth/login -H 'Content-Type: application/json' -d '{"username":"admin","password":"admin123"}'""")
        
        response = json.loads(output.split('\n')[0])
        token = response.get('token')
        print(f"✅ Token obtido")
        
        # Testar endpoint de aulas
        print("\n📝 Testando endpoint /api/classes...")
        output, _ = execute_command(client, f"""docker exec poker_backend curl -s -H 'Authorization: Bearer {token}' http://localhost:5000/api/classes""")

        # Verificar se os dados estão corretos
        # Encontrar o JSON na saída
        json_start = output.find('[')
        json_end = output.rfind(']') + 1
        json_str = output[json_start:json_end]
        classes_data = json.loads(json_str)
        
        print("\n✅ RESULTADO DO TESTE:\n")
        for cls in classes_data:
            print(f"  📚 {cls['name']}")
            print(f"     👨‍🏫 Instrutor: {cls.get('instructor_name', 'N/A')}")
            print(f"     📂 Categoria: {cls.get('category', 'N/A')}")
            print(f"     📅 Data: {cls.get('date', 'N/A')}")
            print()
        
        # Verificar se há problemas de encoding
        print("\n📊 VERIFICAÇÃO DE ENCODING:")
        has_encoding_issues = False
        for cls in classes_data:
            if 'Ã' in cls['name'] or 'Ã' in cls.get('description', ''):
                print(f"  ❌ Problema de encoding em: {cls['name']}")
                has_encoding_issues = True
        
        if not has_encoding_issues:
            print("  ✅ Nenhum problema de encoding detectado!")
        
        # Verificar se instrutores estão carregando
        print("\n📊 VERIFICAÇÃO DE INSTRUTORES:")
        all_have_instructors = all(cls.get('instructor_name') for cls in classes_data)
        if all_have_instructors:
            print("  ✅ Todos os instrutores estão carregando corretamente!")
        else:
            print("  ❌ Alguns instrutores não estão carregando")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_classes()

