#!/usr/bin/env python3
"""
Script para testar se o frontend está respondendo
"""
import requests
import time

print("🧪 Testando frontend...")

for i in range(10):
    try:
        response = requests.get('https://cardroomgrinders.com.br/', verify=False, timeout=5)
        print(f"✅ Frontend respondendo! Status: {response.status_code}")
        
        # Verificar se contém a string 'monthly-database'
        if 'monthly-database' in response.text:
            print("✅ Arquivo contém 'monthly-database' - build foi bem-sucedido!")
        else:
            print("⚠️  Arquivo não contém 'monthly-database' - pode ser cache")
        
        break
    except Exception as e:
        print(f"⏳ Tentativa {i+1}/10 - Aguardando... ({str(e)[:50]})")
        time.sleep(5)
else:
    print("❌ Frontend não respondeu após 50 segundos")

print("\n✅ Teste concluído!")
print("\n📝 Próximos passos:")
print("1. Abra https://cardroomgrinders.com.br no navegador")
print("2. Faça login com: leandrokoles / leandrokoles123456")
print("3. Clique em 'Database Mensal' na sidebar")
print("4. A URL deve ser: https://cardroomgrinders.com.br/student/monthly-database")
print("5. Não deve haver repetição de '/catalog' na URL")

