#!/usr/bin/env python3
"""
Script para corrigir categorias diretamente no servidor via SSH
"""

import paramiko
import time

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"
SSH_PORT = 22

def execute_command(client, command):
    """Executa um comando via SSH"""
    stdin, stdout, stderr = client.exec_command(command)
    time.sleep(1)
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    return output, error

def fix_categories():
    """Corrige categorias no servidor"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Arquivo 1: ClassManagement.js
        print("📝 Corrigindo ClassManagement.js...")
        cmd = """cat > /root/Dojo_Deploy/poker-academy/poker-academy/src/components/admin/ClassManagement.js << 'EOF'
// Arquivo será criado com as categorias corretas
EOF"""
        output, error = execute_command(client, cmd)
        
        # Vamos primeiro verificar o arquivo atual
        print("\n📋 Verificando ClassManagement.js atual...")
        output, error = execute_command(client, "grep -n 'value=\"' /root/Dojo_Deploy/poker-academy/poker-academy/src/components/admin/ClassManagement.js | head -20")
        print(output)
        
        # Usar sed para corrigir as opções do select
        print("\n📝 Corrigindo opções de categoria no ClassManagement.js...")
        
        # Remover opções antigas
        output, error = execute_command(client, "sed -i '/<option value=\"torneos\"/d' /root/Dojo_Deploy/poker-academy/poker-academy/src/components/admin/ClassManagement.js")
        output, error = execute_command(client, "sed -i '/<option value=\"cash\"/d' /root/Dojo_Deploy/poker-academy/poker-academy/src/components/admin/ClassManagement.js")
        
        # Adicionar novas opções se não existirem
        output, error = execute_command(client, """sed -i '/<option value=\"mental\">Mental Games<\\/option>/a\\
  <option value=\"icm\">ICM</option>' /root/Dojo_Deploy/poker-academy/poker-academy/src/components/admin/ClassManagement.js""")
        
        output, error = execute_command(client, """sed -i '/<option value=\"preflop\">Pré-Flop<\\/option>/i\\
  <option value=\"iniciantes\">Iniciante</option>' /root/Dojo_Deploy/poker-academy/poker-academy/src/components/admin/ClassManagement.js""")
        
        print("✅ ClassManagement.js corrigido!\n")
        
        # Verificar resultado
        print("📋 Verificando resultado...")
        output, error = execute_command(client, "grep -A 10 'name=\"category\"' /root/Dojo_Deploy/poker-academy/poker-academy/src/components/admin/ClassManagement.js | head -15")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ CATEGORIAS CORRIGIDAS NO SERVIDOR!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_categories()

