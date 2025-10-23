#!/usr/bin/env python3
"""
Script para corrigir o encoding via SSH executando Python no servidor
"""

import paramiko
import time

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"
SSH_PORT = 22

PYTHON_SCRIPT = """
import sys
sys.path.insert(0, '/root/Dojo_Deploy/poker-academy-backend')

from poker_academy_api.src.models import db, Particoes
from poker_academy_api.src.main import app

with app.app_context():
    # Buscar todas as partições
    particoes = Particoes.query.all()
    
    for p in particoes:
        print(f"Partição {p.id}: {p.nome}")
        print(f"  Descrição antes: {repr(p.descricao)}")
        
        # Corrigir encoding: decodificar como latin-1 e recodificar como utf-8
        if p.descricao:
            try:
                # Tentar corrigir se estiver com encoding errado
                fixed = p.descricao.encode('latin-1').decode('utf-8')
                p.descricao = fixed
                print(f"  Descrição depois: {repr(p.descricao)}")
            except:
                print(f"  Não foi possível corrigir")
    
    db.session.commit()
    print("\\n✅ Encoding corrigido!")
"""

def execute_command(client, command, timeout=120):
    """Executa um comando via SSH"""
    print(f"\n📝 Executando comando...")
    stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
    time.sleep(2)
    
    output = stdout.read().decode('utf-8', errors='replace')
    error = stderr.read().decode('utf-8', errors='replace')
    
    if output:
        print(output)
    
    if error:
        print(f"Stderr: {error}")
    
    return output, error

def fix_encoding():
    """Corrige o encoding"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Criar arquivo Python temporário
        print("📝 Criando script Python...")
        cmd = f"""cat > /tmp/fix_encoding.py << 'EOF'
{PYTHON_SCRIPT}
EOF
"""
        execute_command(client, cmd)
        
        # Executar script
        print("\n🔧 Executando script de correção...")
        cmd2 = "cd /root/Dojo_Deploy/poker-academy-backend && python /tmp/fix_encoding.py"
        execute_command(client, cmd2, timeout=30)
        
        print("\n✅ ENCODING CORRIGIDO COM SUCESSO!")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_encoding()

