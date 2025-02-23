# Thanubis-Userbot
Bot para administrar Telegram 

# Thanubis Bot

Thanubis es un poderoso userbot para Telegram diseñado para realizar tareas de eliminación de grupos, canales y cuentas. Además, incluye un sistema de validación de números telefónicos, monitoreo de spam y detección de amenazas. El bot está optimizado para ser "invisible", minimizando su detección y asegurando la seguridad de la comunidad.

## Características

- **Validación de Números Telefónicos**: Utiliza múltiples APIs para validar números de teléfono.
- **Eliminación de Grupos, Canales y Cuentas**: Permite eliminar grupos, canales y cuentas de Telegram.
- **Búsqueda de Grupos y Canales**: Busca y localiza links de grupos y canales por nombre y país.
- **Geolocalización de Usuarios**: Obtiene la geolocalización de usuarios mediante su @username.
- **Baneo Global**: Banea globalmente a un usuario en todos los chats donde el bot está presente.
- **Silencio Global**: Silencia globalmente a un usuario en todos los chats donde el bot está presente.
- **Monitoreo Autónomo de Spam**: Detecta y elimina mensajes que contengan spam o contenido ilegal.
- **Seguridad Robusta**: Utiliza variables de entorno para almacenar tokens y claves de API de forma segura.
- **Autenticación de Usuarios**: Solo permite que usuarios autorizados ejecuten comandos de eliminación y búsqueda.
- **Manejo de Excepciones**: Captura y registra todas las posibles excepciones para evitar caídas inesperadas.
- **Anti-Detector**: Mantiene al bot invisible para minimizar su detección.

## Requisitos

- Python 3.6+
- Node.js y npm (para instalar PM2)
- Una cuenta de Telegram y un bot token
- Librerías: `python-telegram-bot`, `requests`, `telethon`, `cryptography`, `aiosqlite`, `bcrypt`

## Instalación

1. Clona este repositorio:
    ```bash
    git clone https://github.com/tu_usuario/thanubis_bot.git
    cd thanubis_bot
    ```

2. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

3. Configura las variables de entorno y ejecuta el bot con PM2:
    ```bash
    bash start_bot.sh
    ```

### Comandos Disponibles

- `/start`: Inicia la interacción con el bot.
- `/search <nombre_del_grupo> <pais>`: Busca un grupo por nombre y país.
- `/addgroup <nombre_del_grupo> <pais> <link>`: Agrega un grupo con su nombre, país y link.
- `/geolocate <username>`: Obtiene la geolocalización de un usuario por su username.
- `/ban <user_id>`: Banea globalmente al usuario especificado.
- `/silence <user_id>`: Silencia globalmente al usuario especificado.
- `/deletegroup <group_id>`: Elimina el grupo especificado.
- `/deletechannel <channel_id>`: Elimina el canal especificado.
- `/deleteaccount <account_id>`: Elimina la cuenta especificada.
- `.ban <user_id> [reason]`: Banea a un usuario en el chat actual.
- `.unban <user_id>`: Desbanea a un usuario en el chat actual.
- `.mute <user_id> [duration] [reason]`: Silencia a un usuario en el chat actual.
- `.unmute <user_id>`: Des-silencia a un usuario en el chat actual.
- `.kick <user_id> [reason]`: Expulsa a un usuario del chat actual.
- `.warn <user_id> [reason]`: Advierte a un usuario en el chat actual.
- `.unwarn <user_id>`: Elimina advertencias de un usuario en el chat actual.
- `.warnings <user_id>`: Muestra el número de advertencias de un usuario en el chat actual.
- `.deletegroup`: Elimina el grupo actual.
- `.deleteuser <user_id>`: Elimina a un usuario del chat actual.
- `.gban <user_id>`: Banea globalmente a un usuario.
- `.ungban <user_id>`: Desbanea globalmente a un usuario.
- `.gmute <user_id>`: Silencia globalmente a un usuario.
- `.ungmute <user_id>`: Des-silencia globalmente a un usuario.

## Seguridad

- **Variables de Entorno**: Asegúrate de almacenar los tokens en variables de entorno.
- **Usuarios Autorizados**: Solo los usuarios cuyo ID esté en la lista de autorizados pueden ejecutar comandos de eliminación y búsqueda.
- **Anti-Detector**: Mantiene al bot invisible para minimizar su detección.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cualquier cambio que te gustaría hacer.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.

---

Funciones para una nueva era digital.
