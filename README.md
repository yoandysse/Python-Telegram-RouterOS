# Python-Telegram-RouterOS (beta 1)
Vinculación entre RouterOS Userman y Telegram

##Comandos
###Administrativos
* `/configMK` - Comando para configurar la conexión con el equipo RouterOS
* `/vincular_usuario` - Vincular un usuario de Telegram a una cuenta del Userman del RouterOS
* `/desvincular_cuenta` - Desvincular cuenta de usuario de Telegram con cuenta del Userman del RouterOS
* **`/listar_cuentas` - Mostrar cuentas de Telegram vinculadas con cuentas del Userman del RouterOS (no implementado aun)**

###Globales
* `/start` - Inicia el bot, comprueba que el usuario tenga configurado su username, sino le recomienta que lo agrege para poder usar el bot. Agrega el usuario a la BD en caso que sea nuevo.
* `/consumo` - Muestra el consumo de la cuenta de usuario
