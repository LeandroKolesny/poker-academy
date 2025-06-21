#!/usr/bin/env python3
"""
Script para iniciar a Poker Academy completa
- Atualiza o banco de dados
- Inicia o backend Flask
- Inicia o frontend React
"""

import subprocess
import sys
import os
import time
import threading
from pathlib import Path

def run_command(command, cwd=None, shell=True):
    """Executa um comando e retorna o processo"""
    try:
        if shell and sys.platform == "win32":
            # No Windows, usar shell=True para comandos como npm
            process = subprocess.Popen(
                command, 
                shell=True, 
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
        else:
            process = subprocess.Popen(
                command.split() if isinstance(command, str) else command,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
        return process
    except Exception as e:
        print(f"❌ Erro ao executar comando: {e}")
        return None

def stream_output(process, name):
    """Stream da saída do processo em tempo real"""
    try:
        for line in iter(process.stdout.readline, ''):
            if line:
                print(f"[{name}] {line.rstrip()}")
        process.stdout.close()
        return_code = process.wait()
        if return_code != 0:
            print(f"❌ {name} terminou com código de erro: {return_code}")
    except Exception as e:
        print(f"❌ Erro no stream de {name}: {e}")

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    print("🔍 Verificando dependências...")
    
    # Verificar Python
    try:
        python_version = sys.version_info
        if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
            print("❌ Python 3.8+ é necessário")
            return False
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    except:
        print("❌ Python não encontrado")
        return False
    
    # Verificar Node.js
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print(f"✅ Node.js {result.stdout.strip()}")
        else:
            print("❌ Node.js não encontrado")
            return False
    except:
        print("❌ Node.js não encontrado")
        return False
    
    # Verificar npm
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print(f"✅ npm {result.stdout.strip()}")
        else:
            print("❌ npm não encontrado")
            return False
    except:
        print("❌ npm não encontrado")
        return False
    
    return True

def update_database():
    """Atualiza o banco de dados"""
    print("\n🗄️  Atualizando banco de dados...")
    try:
        result = subprocess.run([sys.executable, 'update_database_particao.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Banco de dados atualizado com sucesso!")
            print(result.stdout)
            return True
        else:
            print("❌ Erro ao atualizar banco de dados:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Erro ao executar script de banco: {e}")
        return False

def install_backend_dependencies():
    """Instala dependências do backend"""
    backend_path = Path("poker-academy-backend/poker_academy_api")
    requirements_file = backend_path / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ Arquivo requirements.txt não encontrado")
        return False
    
    print("\n📦 Instalando dependências do backend...")
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependências do backend instaladas!")
            return True
        else:
            print("❌ Erro ao instalar dependências do backend:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def install_frontend_dependencies():
    """Instala dependências do frontend"""
    frontend_path = Path("poker-academy")
    package_json = frontend_path / "package.json"
    
    if not package_json.exists():
        print("❌ Arquivo package.json não encontrado")
        return False
    
    print("\n📦 Instalando dependências do frontend...")
    try:
        result = subprocess.run(['npm', 'install'], 
                              cwd=str(frontend_path), 
                              capture_output=True, text=True, shell=True)
        
        if result.returncode == 0:
            print("✅ Dependências do frontend instaladas!")
            return True
        else:
            print("❌ Erro ao instalar dependências do frontend:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def start_application():
    """Inicia a aplicação completa"""
    print("\n🚀 Iniciando aplicação...")
    
    # Caminhos
    backend_path = Path("poker-academy-backend/poker_academy_api/src")
    frontend_path = Path("poker-academy")
    
    # Iniciar backend
    print("🔧 Iniciando backend Flask...")
    backend_process = run_command(
        f"{sys.executable} main.py",
        cwd=str(backend_path)
    )
    
    if not backend_process:
        print("❌ Falha ao iniciar backend")
        return False
    
    # Aguardar um pouco para o backend inicializar
    time.sleep(3)
    
    # Iniciar frontend
    print("⚛️  Iniciando frontend React...")
    frontend_process = run_command(
        "npm start",
        cwd=str(frontend_path)
    )
    
    if not frontend_process:
        print("❌ Falha ao iniciar frontend")
        backend_process.terminate()
        return False
    
    # Criar threads para stream de saída
    backend_thread = threading.Thread(
        target=stream_output, 
        args=(backend_process, "BACKEND"),
        daemon=True
    )
    frontend_thread = threading.Thread(
        target=stream_output, 
        args=(frontend_process, "FRONTEND"),
        daemon=True
    )
    
    backend_thread.start()
    frontend_thread.start()
    
    print("\n🎉 Aplicação iniciada com sucesso!")
    print("📍 Backend: http://localhost:5000")
    print("📍 Frontend: http://localhost:3000")
    print("\n⚠️  Pressione Ctrl+C para parar a aplicação")
    
    try:
        # Aguardar até que o usuário pare a aplicação
        while True:
            time.sleep(1)
            # Verificar se os processos ainda estão rodando
            if backend_process.poll() is not None:
                print("❌ Backend parou inesperadamente")
                break
            if frontend_process.poll() is not None:
                print("❌ Frontend parou inesperadamente")
                break
    except KeyboardInterrupt:
        print("\n🛑 Parando aplicação...")
        backend_process.terminate()
        frontend_process.terminate()
        
        # Aguardar processos terminarem
        backend_process.wait()
        frontend_process.wait()
        
        print("✅ Aplicação parada com sucesso!")
    
    return True

def main():
    """Função principal"""
    print("🎯 POKER ACADEMY - INICIALIZADOR")
    print("=" * 50)
    
    # Verificar dependências
    if not check_dependencies():
        print("❌ Dependências não atendidas. Instale Python 3.8+, Node.js e npm")
        sys.exit(1)
    
    # Atualizar banco de dados
    if not update_database():
        print("❌ Falha ao atualizar banco de dados")
        sys.exit(1)
    
    # Instalar dependências
    if not install_backend_dependencies():
        print("❌ Falha ao instalar dependências do backend")
        sys.exit(1)
    
    if not install_frontend_dependencies():
        print("❌ Falha ao instalar dependências do frontend")
        sys.exit(1)
    
    # Iniciar aplicação
    if not start_application():
        print("❌ Falha ao iniciar aplicação")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️  Operação cancelada pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        sys.exit(1)
