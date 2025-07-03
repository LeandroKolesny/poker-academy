#!/usr/bin/env node

/**
 * Script para alternar entre ambientes de desenvolvimento e produção
 * 
 * Uso:
 * node switch-environment.js local    # Para desenvolvimento local
 * node switch-environment.js server   # Para servidor de produção
 * node switch-environment.js status   # Para ver ambiente atual
 */

const fs = require('fs');
const path = require('path');

const CONFIG_DIR = path.join(__dirname, 'poker-academy', 'src', 'config');
const MAIN_CONFIG = path.join(CONFIG_DIR, 'config.js');
const LOCAL_CONFIG = path.join(CONFIG_DIR, 'config.local.js');
const SERVER_CONFIG = path.join(CONFIG_DIR, 'config.server.js');

// Cores para output
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function getCurrentEnvironment() {
  try {
    const configContent = fs.readFileSync(MAIN_CONFIG, 'utf8');

    if (configContent.includes('http://localhost:5000')) {
      return 'local';
    } else if (configContent.includes('http://142.93.206.128:5000')) {
      return 'server';
    } else if (configContent.includes('https://cardroomgrinders.com.br')) {
      return 'domain';
    } else if (configContent.includes('https://grinders.com.br')) {
      return 'grinders';
    }

    return 'unknown';
  } catch (error) {
    log(`❌ Erro ao ler configuração: ${error.message}`, 'red');
    return 'error';
  }
}

function showStatus() {
  const current = getCurrentEnvironment();
  
  log('\n🔧 Status da Configuração:', 'cyan');
  log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', 'cyan');
  
  switch (current) {
    case 'local':
      log('📍 Ambiente Atual: DESENVOLVIMENTO LOCAL', 'green');
      log('🌐 API Base URL: http://localhost:5000', 'yellow');
      break;
    case 'server':
      log('📍 Ambiente Atual: SERVIDOR DE PRODUÇÃO', 'magenta');
      log('🌐 API Base URL: http://142.93.206.128:5000', 'yellow');
      break;
    case 'domain':
      log('📍 Ambiente Atual: DOMÍNIO CARDROOMGRINDERS', 'blue');
      log('🌐 API Base URL: https://cardroomgrinders.com.br', 'yellow');
      break;
    case 'grinders':
      log('📍 Ambiente Atual: DOMÍNIO GRINDERS', 'blue');
      log('🌐 API Base URL: https://cardroomgrinders.com.br', 'yellow');
      break;
    default:
      log('❌ Ambiente não identificado ou erro na configuração', 'red');
  }
  
  log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n', 'cyan');
}

function switchToLocal() {
  try {
    log('\n🔄 Alternando para ambiente LOCAL...', 'yellow');
    
    // Ler configuração local
    if (!fs.existsSync(LOCAL_CONFIG)) {
      log('❌ Arquivo config.local.js não encontrado!', 'red');
      return false;
    }
    
    // Fazer backup da configuração atual
    const backupPath = `${MAIN_CONFIG}.backup.${Date.now()}`;
    fs.copyFileSync(MAIN_CONFIG, backupPath);
    log(`📦 Backup criado: ${path.basename(backupPath)}`, 'blue');
    
    // Ler template da configuração principal
    let mainConfig = fs.readFileSync(MAIN_CONFIG, 'utf8');
    
    // Substituir URLs para desenvolvimento local
    mainConfig = mainConfig.replace(
      /API_BASE_URL: '[^']*'/g,
      "API_BASE_URL: 'http://localhost:5000'"
    );
    mainConfig = mainConfig.replace(
      /FRONTEND_URL: '[^']*'/g,
      "FRONTEND_URL: 'http://localhost:3000'"
    );
    mainConfig = mainConfig.replace(
      /WEBSOCKET_URL: '[^']*'/g,
      "WEBSOCKET_URL: 'ws://localhost:5000'"
    );
    
    // Salvar configuração atualizada
    fs.writeFileSync(MAIN_CONFIG, mainConfig);
    
    log('✅ Configuração alterada para DESENVOLVIMENTO LOCAL', 'green');
    log('🌐 API: http://localhost:5000', 'cyan');
    log('🖥️  Frontend: http://localhost:3000', 'cyan');
    
    return true;
  } catch (error) {
    log(`❌ Erro ao alternar para local: ${error.message}`, 'red');
    return false;
  }
}

function switchToServer() {
  try {
    log('\n🔄 Alternando para ambiente SERVIDOR...', 'yellow');

    // Ler configuração do servidor
    if (!fs.existsSync(SERVER_CONFIG)) {
      log('❌ Arquivo config.server.js não encontrado!', 'red');
      return false;
    }

    // Fazer backup da configuração atual
    const backupPath = `${MAIN_CONFIG}.backup.${Date.now()}`;
    fs.copyFileSync(MAIN_CONFIG, backupPath);
    log(`📦 Backup criado: ${path.basename(backupPath)}`, 'blue');

    // Ler template da configuração principal
    let mainConfig = fs.readFileSync(MAIN_CONFIG, 'utf8');

    // Substituir URLs para servidor de produção
    mainConfig = mainConfig.replace(
      /API_BASE_URL: '[^']*'/g,
      "API_BASE_URL: 'http://142.93.206.128:5000'"
    );
    mainConfig = mainConfig.replace(
      /FRONTEND_URL: '[^']*'/g,
      "FRONTEND_URL: 'http://142.93.206.128'"
    );
    mainConfig = mainConfig.replace(
      /WEBSOCKET_URL: '[^']*'/g,
      "WEBSOCKET_URL: 'ws://142.93.206.128:5000'"
    );

    // Salvar configuração atualizada
    fs.writeFileSync(MAIN_CONFIG, mainConfig);

    log('✅ Configuração alterada para SERVIDOR DE PRODUÇÃO', 'green');
    log('🌐 API: http://142.93.206.128:5000', 'cyan');
    log('🖥️  Frontend: http://142.93.206.128', 'cyan');

    return true;
  } catch (error) {
    log(`❌ Erro ao alternar para servidor: ${error.message}`, 'red');
    return false;
  }
}

function switchToDomain() {
  try {
    log('\n🔄 Alternando para ambiente DOMÍNIO...', 'yellow');

    // Fazer backup da configuração atual
    const backupPath = `${MAIN_CONFIG}.backup.${Date.now()}`;
    fs.copyFileSync(MAIN_CONFIG, backupPath);
    log(`📦 Backup criado: ${path.basename(backupPath)}`, 'blue');

    // Ler template da configuração principal
    let mainConfig = fs.readFileSync(MAIN_CONFIG, 'utf8');

    // Substituir URLs para domínio personalizado
    mainConfig = mainConfig.replace(
      /API_BASE_URL: '[^']*'/g,
      "API_BASE_URL: 'https://cardroomgrinders.com.br'"
    );
    mainConfig = mainConfig.replace(
      /FRONTEND_URL: '[^']*'/g,
      "FRONTEND_URL: 'https://cardroomgrinders.com.br'"
    );
    mainConfig = mainConfig.replace(
      /WEBSOCKET_URL: '[^']*'/g,
      "WEBSOCKET_URL: 'wss://cardroomgrinders.com.br'"
    );

    // Salvar configuração atualizada
    fs.writeFileSync(MAIN_CONFIG, mainConfig);

    log('✅ Configuração alterada para DOMÍNIO CARDROOMGRINDERS', 'green');
    log('🌐 API: https://cardroomgrinders.com.br', 'cyan');
    log('🖥️  Frontend: https://cardroomgrinders.com.br', 'cyan');
    log('🔒 SSL/HTTPS ativado', 'cyan');

    return true;
  } catch (error) {
    log(`❌ Erro ao alternar para domínio: ${error.message}`, 'red');
    return false;
  }
}

function switchToDomain() {
  try {
    log('\n🔄 Alternando para DOMÍNIO PERSONALIZADO...', 'yellow');

    // Fazer backup da configuração atual
    const backupPath = `${MAIN_CONFIG}.backup.${Date.now()}`;
    fs.copyFileSync(MAIN_CONFIG, backupPath);
    log(`📦 Backup criado: ${path.basename(backupPath)}`, 'blue');

    // Ler template da configuração principal
    let mainConfig = fs.readFileSync(MAIN_CONFIG, 'utf8');

    // Substituir URLs para domínio personalizado
    mainConfig = mainConfig.replace(
      /API_BASE_URL: '[^']*'/g,
      "API_BASE_URL: 'https://cardroomgrinders.com.br'"
    );
    mainConfig = mainConfig.replace(
      /FRONTEND_URL: '[^']*'/g,
      "FRONTEND_URL: 'https://cardroomgrinders.com.br'"
    );
    mainConfig = mainConfig.replace(
      /WEBSOCKET_URL: '[^']*'/g,
      "WEBSOCKET_URL: 'wss://cardroomgrinders.com.br'"
    );

    // Salvar configuração atualizada
    fs.writeFileSync(MAIN_CONFIG, mainConfig);

    log('✅ Configuração alterada para DOMÍNIO PERSONALIZADO', 'green');
    log('🌐 API: https://cardroomgrinders.com.br', 'cyan');
    log('🖥️  Frontend: https://cardroomgrinders.com.br', 'cyan');

    return true;
  } catch (error) {
    log(`❌ Erro ao alternar para domínio: ${error.message}`, 'red');
    return false;
  }
}

function showHelp() {
  log('\n🔧 Script de Alternância de Ambiente - Poker Academy', 'cyan');
  log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', 'cyan');
  log('\n📋 Comandos disponíveis:', 'bright');
  log('  node switch-environment.js local    # Alternar para desenvolvimento local', 'yellow');
  log('  node switch-environment.js server   # Alternar para servidor de produção', 'yellow');
  log('  node switch-environment.js domain   # Alternar para domínio personalizado', 'yellow');
  log('  node switch-environment.js status   # Ver ambiente atual', 'yellow');
  log('  node switch-environment.js help     # Mostrar esta ajuda', 'yellow');
  log('\n💡 Exemplos:', 'bright');
  log('  # Para trabalhar localmente:', 'green');
  log('  node switch-environment.js local', 'green');
  log('  npm start', 'green');
  log('\n  # Para fazer deploy:', 'magenta');
  log('  node switch-environment.js server', 'magenta');
  log('  npm run build', 'magenta');
  log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n', 'cyan');
}

// Processar argumentos da linha de comando
const command = process.argv[2];

switch (command) {
  case 'local':
    if (switchToLocal()) {
      showStatus();
    }
    break;
    
  case 'server':
    if (switchToServer()) {
      showStatus();
    }
    break;

  case 'domain':
    if (switchToDomain()) {
      showStatus();
    }
    break;

  case 'status':
    showStatus();
    break;
    
  case 'help':
  case '--help':
  case '-h':
    showHelp();
    break;
    
  default:
    log('❌ Comando não reconhecido!', 'red');
    showHelp();
    process.exit(1);
}
