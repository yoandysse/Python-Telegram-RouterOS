import paramiko
from functools import wraps
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ChatAction
import db
from models import GestionUsuarios

class MK:
    ip = ""
    port = ""
    username = ""
    password = ""
    status = ""

    def __init__(self, ip, port, username,password):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password


        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            client.connect(hostname=ip, port=port, username=username, password=password)
            with open("config","w", encoding="UTF-8") as data_conf:
                 data_conf.write("ip = {}\nport = {}\nusername = {}\npassword = {}\n".format(self.ip,self.port,self.username,self.password))
            self.status = "OK"

        except Exception as e:
            self.status = type(e).__name__

    def getData(self):
        data = []
        with open("config", "r", encoding="UTF-8") as data_conf:
            for value in data_conf.readlines():
                value = value.replace("\n","")
                value = value.split(" ")
                value = value[-1]
                data.append(value)
        return data

    def getUserInfo(self,user):

        data = self.getData()

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=data[0], port=int(data[1]), username=data[2], password=data[3])

        stdin, stdout, stderr = client.exec_command('return [tool user-manager user get {}]'.format(user))
        result = stdout.readline().split(";")

        return result


#### Global ###
def send_typing_action(func):
    """Sends typing action while processing func command."""
    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context,  *args, **kwargs)

    return command_func


## Acciones

@send_typing_action
def start(update, context):

    if update.message.chat.username == None:
        update.message.reply_text(
            'Hola, bienvenido!! \n\n He detectado que no tiene un nombre de usuario configurado. Antes de continuar configure su nombre de usuario y luego escriba /start')
    elif db.session.query(GestionUsuarios).filter_by(usernameTelegram=update.message.chat.username).first() == None:

        adduser = GestionUsuarios(idTelegram=update.message.chat.id, usernameTelegram=update.message.chat.username)
        db.session.add(adduser)
        db.session.commit()
        db.session.close()

        update.message.reply_text(
            'Hola, bienvenido!! \n\nUse:\n/consumo para saber el consumo de su cuenta\n/tutorial para aprender a configurar su cuenta')
    else:
        update.message.reply_text(
            'Hola, bienvenido!! \n\nUse:\n/consumo para saber el consumo de su cuenta\n/tutorial para aprender a configurar su cuenta')

@send_typing_action
def configMK(update, context):
    update.message.reply_text('Introduzca ip puerto usuario contraseña.\nEjemplo: 192.168.88.1 22 admin password')

    return configMK_text

@send_typing_action
def vincularusuario(update, context):
    update.message.reply_text('Introduzca usuario de telegram y cuenta.\nEjemplo: @elvirus95 cuenta31')

    return vincularusuario_text

@send_typing_action
def desvincularcuenta(update, context):
    update.message.reply_text('Introduzca nombre de la cuenta.\nEjemplo: cuenta31')

    return desvincularcuenta_text

@send_typing_action
def consumo(update, context):
    usuarioTelegram = update.message.chat.username
    cuenta = db.session.query(GestionUsuarios).filter_by(usernameTelegram=usuarioTelegram).first()

    data = []
    with open("config", "r", encoding="UTF-8") as data_conf:
        for value in data_conf.readlines():
            value = value.replace("\n", "")
            value = value.split(" ")
            value = value[-1]
            data.append(value)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=data[0], port=int(data[1]), username=data[2], password=data[3])

    stdin, stdout, stderr = client.exec_command('return [tool user-manager user get {}]'.format(cuenta.cuenta))
    result = stdout.readline().split(";")
    message = ""
    for i,m in enumerate(result):
        print(i,m)
        message += m+"\n"
    # message =
    update.message.reply_text(message)


@send_typing_action
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Lo siento, no reconozco este comando.")

## ENTRADAS DE DATOS
@send_typing_action
def configMK_text(update, context):
    text = update.message.text
    text = text.split(" ")

    ip = text[0]
    port = text[1]
    user = text[2]
    passwd = text[3]
    mikrotik = MK(ip,port,user,passwd)

    if mikrotik.status == "OK":
        message = "Se ha configurado correctamente la conexión con el equipo"
        update.message.reply_text(message)

    else:
        message = "Hemos tenido un error del tipo {} intente nuevamente ejecutar el comando.".format(mikrotik.status)
        update.message.reply_text(message)

    return ConversationHandler.END

@send_typing_action
def vincularusuario_text(update, context):
    text = update.message.text
    text = text.split(" ")

    usuario = text[0].replace("@","")
    cuenta = text[1]

    buscarCuenta = db.session.query(GestionUsuarios).filter_by(cuenta=cuenta).first()
    vincularusuario = db.session.query(GestionUsuarios).filter_by(usernameTelegram=usuario).first()

    if  buscarCuenta == None and vincularusuario != None:
        vincularusuario.cuenta = cuenta
        update.message.reply_text(
            "La cuenta {} fue vinculada con el usuario de Telegram {} correctamente".format(cuenta,usuario))
    elif vincularusuario == None:
        update.message.reply_text("La Cuenta de usuario de telegram @{} no se encuentra".format(usuario))
    elif buscarCuenta != None:
        update.message.reply_text(
            "La cuenta {} ya se encuentra vinculada con el usuario de Telegram @{} use /desvincular_cuenta primero".format(cuenta,
                buscarCuenta.usernameTelegram))

    db.session.commit()
    db.session.close()
    return ConversationHandler.END

@send_typing_action
def desvincularcuenta_text(update, context):
    cuenta = update.message.text

    buscarCuenta = db.session.query(GestionUsuarios).filter_by(cuenta=cuenta).first()

    if  buscarCuenta == None :
        update.message.reply_text(
            "La cuenta {} no se encuentra".format(cuenta))
    else:
        buscarCuenta.cuenta = None


        update.message.reply_text(
            "La cuenta {} se ha desvinculado correctamente del usuario de telegram @{}".format(cuenta, buscarCuenta.usernameTelegram))

    db.session.commit()
    db.session.close()
    return ConversationHandler.END


if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)

    token = "2032051580:AAEGkgb8yrvyRIiqQDvOP29d3lGGcE6CAFc"

    updater = Updater(token=token, use_context=True)
    dp = updater.dispatcher

    ### COMANDOS A RECONOCER
    ## /start
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('consumo', consumo))

    ## Acciones
    dp.add_handler(ConversationHandler(
        entry_points=[
            ## Administrativos
            CommandHandler('configMK', configMK),
            CommandHandler('vincular_usuario', vincularusuario),
            CommandHandler('desvincular_cuenta', desvincularcuenta),
            # CommandHandler('listar_cuentas', listarcuentas),

        ],

        states={
            configMK_text: [MessageHandler(Filters.text, configMK_text)],
            vincularusuario_text: [MessageHandler(Filters.text, vincularusuario_text)],
            desvincularcuenta_text: [MessageHandler(Filters.text, desvincularcuenta_text)]

        },

        fallbacks=[]

    ))


    ## para comandos desconocidos
    dp.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()
    updater.idle()

## comandos
# /configMK     (pedir, ip, puerto, usuario, contraseña) --- ok
# /vincular_usuario (pedir alias en telegram luego nombre de la cuenta a vincular)
# /consumo  (mostrar consumo del usuario)
# /tutorial (mostrar video tutoriales de como configurar el servicio)
