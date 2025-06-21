#!/usr/bin/env python3
"""
Script simples para iniciar a Poker Academy
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def start_backend():
    """Inicia o backend Flask"""
    backend_path = Path("poker-academy-backend/poker_academy_api/src")
    
    if not backend_path.exists():
        print("Erro: Diretorio do backend nao encontrado")
        return None
    
    print("Iniciando backend Flask...")
    try:
        # Usar python -m para garantir que o módulo seja encontrado
        process = subprocess.Popen([
            sys.executable, "main.py"
        ], cwd=str(backend_path))
        
        print("Backend iniciado com sucesso!")
        print("Backend rodando em: http://localhost:5000")
        return process
    except Exception as e:
        print(f"Erro ao iniciar backend: {e}")
        return None

def start_frontend():
    """Inicia o frontend React"""
    frontend_path = Path("poker-academy")
    
    if not frontend_path.exists():
        print("Erro: Diretorio do frontend nao encontrado")
        return None
    
    print("Iniciando frontend React...")
    try:
        process = subprocess.Popen([
            "npm", "start"
        ], cwd=str(frontend_path), shell=True)
        
        print("Frontend iniciado com sucesso!")
        print("Frontend rodando em: http://localhost:3000")
        return process
    except Exception as e:
        print(f"Erro ao iniciar frontend: {e}")
        return None

def main():
    """Função principal"""
    print("POKER ACADEMY - INICIALIZADOR SIMPLES")
    print("=" * 40)
    
    # Iniciar backend
    backend_process = start_backend()
    if not backend_process:
        print("Falha ao iniciar backend")
        sys.exit(1)
    
    # Aguardar um pouco
    time.sleep(3)
    
    # Iniciar frontend
    frontend_process = start_frontend()
    if not frontend_process:
        print("Falha ao iniciar frontend")
        backend_process.terminate()
        sys.exit(1)
    
    print("\nAplicacao iniciada com sucesso!")
    print("Backend: http://localhost:5000")
    print("Frontend: http://localhost:3000")
    print("\nPressione Ctrl+C para parar")
    
    try:
        # Aguardar até que o usuário pare
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nParando aplicacao...")
        backend_process.terminate()
        frontend_process.terminate()
        print("Aplicacao parada!")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)
