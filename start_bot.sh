#!/bin/bash

# Instalar PM2 si no está instalado
if ! command -v pm2 &> /dev/null
then
    echo "PM2 no está instalado. Instalando..."
    npm install -g pm2
fi

# Configurar variables de entorno
export TELEGRAM_BOT_TOKEN='TU_TELEGRAM_BOT_TOKEN'
export API_ID='TU_API_ID'
export API_HASH='TU_API_HASH'
export KEYS_URL='URL_DE_TUS_KEYS'

# Iniciar el bot con PM2
pm2 start bot/thanubis_bot.py --name thanubis_bot --interpreter python3

# Guardar la configuración de PM2 para reinicios automáticos
pm2 save
