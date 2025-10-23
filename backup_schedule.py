#!/usr/bin/env python3
"""
Script para fazer backups automáticos do banco de dados
Executa a cada 6 horas
"""
import schedule
import time
import subprocess
import os
from datetime import datetime

def fazer_backup():
    """Executa o script de backup"""
    print(f"\n{'='*80}")
    print(f"⏰ Iniciando backup automático em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}")
    
    try:
        result = subprocess.run(['python', 'backup_database.py'], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        print(f"✅ Backup concluído!")
    except Exception as e:
        print(f"❌ Erro ao fazer backup: {e}")
    
    print(f"{'='*80}\n")

def agendar_backups():
    """Agenda backups automáticos"""
    # Fazer backup a cada 6 horas
    schedule.every(6).hours.do(fazer_backup)
    
    # Fazer backup também ao iniciar
    fazer_backup()
    
    print("📅 Backups agendados para cada 6 horas")
    print("💡 Pressione Ctrl+C para parar\n")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    try:
        agendar_backups()
    except KeyboardInterrupt:
        print("\n\n⏹️  Backup automático parado")

