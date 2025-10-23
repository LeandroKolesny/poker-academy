#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configurar Chrome
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)

try:
    print('🌐 Abrindo https://cardroomgrinders.com.br...')
    driver.get('https://cardroomgrinders.com.br')
    time.sleep(3)
    
    print('📝 Fazendo login...')
    username_field = driver.find_element(By.NAME, 'username')
    password_field = driver.find_element(By.NAME, 'password')
    
    username_field.send_keys('leandrokoles')
    password_field.send_keys('leandrokoles123456')
    
    login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Entrar')]")
    login_button.click()
    
    print('⏳ Aguardando login...')
    time.sleep(5)
    
    print('🔍 Verificando URL após login...')
    current_url = driver.current_url
    print(f'URL atual: {current_url}')
    
    print('📌 Clicando em "Database Mensal"...')
    # Procurar pelo link de Database Mensal
    database_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Database Mensal')]"))
    )
    database_link.click()
    
    print('⏳ Aguardando navegação...')
    time.sleep(3)
    
    print('🔍 Verificando URL final...')
    final_url = driver.current_url
    print(f'URL final: {final_url}')
    
    # Verificar se há repetição de /catalog
    if '/catalog/catalog' in final_url:
        print('❌ ERRO: URL contém repetição de /catalog!')
    elif '/student/monthly-database' in final_url:
        print('✅ SUCESSO: URL está correta!')
    else:
        print('⚠️ URL inesperada')
    
    # Verificar console
    print('\n📋 Verificando console do navegador...')
    logs = driver.get_log('browser')
    for log in logs:
        if 'catalog' in log['message'].lower():
            print(f"  {log['level']}: {log['message'][:100]}")
    
finally:
    driver.quit()
    print('\n✅ Teste concluído!')

