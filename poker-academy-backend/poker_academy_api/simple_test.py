#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste simples usando PowerShell
"""

import subprocess
import json

def test_with_powershell():
    """Testar usando PowerShell"""
    print("🧪 TESTANDO SISTEMA COM POWERSHELL")
    print("=" * 60)
    
    # 1. Testar login
    print("1️⃣ TESTANDO LOGIN...")
    login_cmd = '''
    $body = @{
        email = "student@pokeracademy.com"
        password = "student"
    } | ConvertTo-Json
    
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:5000/api/auth/login" -Method POST -Body $body -ContentType "application/json"
        $data = $response.Content | ConvertFrom-Json
        Write-Host "✅ Login bem-sucedido!"
        Write-Host "Token: $($data.token.Substring(0,50))..."
        $data.token
    } catch {
        Write-Host "❌ Erro no login: $($_.Exception.Message)"
    }
    '''
    
    try:
        result = subprocess.run(['powershell', '-Command', login_cmd], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            token = lines[-1] if lines else None
            
            if token and token.startswith('eyJ'):
                print(f"✅ Login bem-sucedido!")
                print(f"   Token: {token[:50]}...")
                
                # 2. Testar verificação
                print("\n2️⃣ TESTANDO VERIFICAÇÃO...")
                verify_cmd = f'''
                try {{
                    $response = Invoke-WebRequest -Uri "http://localhost:5000/api/auth/verify" -Headers @{{"Authorization"="Bearer {token}"}} -Method GET
                    $data = $response.Content | ConvertFrom-Json
                    Write-Host "✅ Token válido!"
                    Write-Host "Usuário: $($data.user.name)"
                }} catch {{
                    Write-Host "❌ Erro na verificação: $($_.Exception.Message)"
                }}
                '''
                
                verify_result = subprocess.run(['powershell', '-Command', verify_cmd], 
                                             capture_output=True, text=True, timeout=30)
                print(verify_result.stdout)
                
                # 3. Testar alteração de senha
                print("\n3️⃣ TESTANDO ALTERAÇÃO DE SENHA...")
                change_cmd = f'''
                $body = @{{
                    current_password = "student"
                    new_password = "student123"
                }} | ConvertTo-Json
                
                try {{
                    $response = Invoke-WebRequest -Uri "http://localhost:5000/api/auth/change-password" -Method PUT -Body $body -ContentType "application/json" -Headers @{{"Authorization"="Bearer {token}"}}
                    Write-Host "✅ Alteração de senha bem-sucedida!"
                }} catch {{
                    Write-Host "❌ Erro na alteração: $($_.Exception.Message)"
                }}
                '''
                
                change_result = subprocess.run(['powershell', '-Command', change_cmd], 
                                             capture_output=True, text=True, timeout=30)
                print(change_result.stdout)
                
                # 4. Reverter senha
                print("\n4️⃣ REVERTENDO SENHA...")
                revert_cmd = f'''
                $body = @{{
                    current_password = "student123"
                    new_password = "student"
                }} | ConvertTo-Json
                
                try {{
                    $response = Invoke-WebRequest -Uri "http://localhost:5000/api/auth/change-password" -Method PUT -Body $body -ContentType "application/json" -Headers @{{"Authorization"="Bearer {token}"}}
                    Write-Host "✅ Senha revertida!"
                }} catch {{
                    Write-Host "❌ Erro ao reverter: $($_.Exception.Message)"
                }}
                '''
                
                revert_result = subprocess.run(['powershell', '-Command', revert_cmd], 
                                             capture_output=True, text=True, timeout=30)
                print(revert_result.stdout)
                
            else:
                print("❌ Token não encontrado na resposta")
        else:
            print(f"❌ Erro no login: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
    
    print("\n🎯 TESTE CONCLUÍDO!")
    print("=" * 60)
    print("📋 AGORA TESTE NO FRONTEND:")
    print("1. Abra http://localhost:3000")
    print("2. Faça login com: student@pokeracademy.com / student")
    print("3. Tente alterar a senha")
    print("4. Deve funcionar automaticamente!")

if __name__ == "__main__":
    test_with_powershell()
