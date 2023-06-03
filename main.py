import os
#from dotenv import load_dotenv
import telebot
import my_requests as rr
import my_messages as mm
import time
import threading
import datetime
from datetime import datetime

#load_dotenv('config.env')
#token = os.environ.get("TelegramBOT_TK")
#chat_id = os.environ.get("TelegramBOT_MyChatID")

token = ""
chat_id = ""

# instanciamos el bot de Telegram
bot = telebot.TeleBot(token)


# responde al comando /start
@bot.message_handler(commands=['start'])
def cmd_start(msg):
    """Da la bienvenida al usuario"""
    bot.send_message(msg.chat.id, mm.my_msgs["start"])


# responde al comando /crypto
@bot.message_handler(commands=['crypto'])
def get_cryptos(msg):
    """Muestra las crypto"""
    try:
        bot.send_chat_action(msg.chat.id, 'typing')
        c = rr.get_cryptos()
    except:
        bot.send_message(msg.chat.id, mm.my_msgs["error"])

    show = [crypto for crypto in c if round(crypto.quote.USD.price, 0) not in [1]]

    m = 'Top 5 cryptos de coinmarketcap\n\n'
    for d in show[0:5]:
        m += f'<b>{d.name} ({d.symbol})</b>\nUSD {round(d.quote.USD.price, 2)}\n\n'

    m += '🤑🤑🤑'

    bot.send_message(msg.chat.id, m, parse_mode='html')

# responde al comando /clima
@bot.message_handler(commands=['clima'])
def get_clima(msg):
    try:
        location_key = rr.get_location_key()
        m = rr.get_hourly_forecast(location_key)
    except Exception as ex:
        bot.send_message(msg.chat.id, mm.my_msgs["error"])
        print(ex)


    bot.send_message(msg.chat.id, m, parse_mode='html')


# envía las crypto todas las mañanas
def send_cryptos(msg_id):
    """Muestra las crypto"""
    try:
        bot.send_chat_action(msg_id, 'typing')
        c = rr.get_cryptos()
    except:
        bot.send_message(msg_id, mm.my_msgs["error"])

    show = [crypto for crypto in c if round(crypto.quote.USD.price, 0) not in [1]]

    m = 'Top 5 cryptos de coinmarketcap\n\n'
    for d in show[0:5]:
        m += f'<b>{d.name} ({d.symbol})</b>\nUSD {round(d.quote.USD.price, 2)}\n\n'

    m += '🤑🤑🤑'

    bot.send_message(msg_id, 'Buen día!')
    bot.send_message(msg_id, m, parse_mode='html')

# envía el clima
def send_clima(msg_id):
    """Muestra las crypto"""
    try:
        location_key = rr.get_location_key()
        m = rr.get_hourly_forecast(location_key)
    except:
        bot.send_message(msg_id, mm.my_msgs["error"])

    bot.send_message(msg_id, m, parse_mode='html')

'''
@bot.message_handler(content_types=["photo"])
def bot_mensajes_img(msg):
    fecha = datetime.now()
    file_info = bot.get_file(msg.photo[-1].file_id)
    file = bot.download_file(file_info.file_path)
    with open(f"D:\\ImagenesBOT\\{fecha.strftime('%Y%m%d%H%M%S')}.jpg", 'wb') as f:
        f.write(file)
    bot.reply_to(msg, "Imagen guardada")
'''

# responde a los mensajes de texto que no son comandos
@bot.message_handler(content_types=["text"])
def bot_mensajes_texto(msg):
    """Gestiona mensajes de texto recibidos"""
    if msg.text and msg.text.startswith("/"):
        bot.send_message(msg.chat.id, mm.my_msgs["not_found"])
    else:
        bot.send_message(msg.chat.id, mm.my_msgs["init"])

def my_pooling():
    # bucle infinito
    bot.infinity_polling()

# manda los precios de las crypto y clima todos los dias entre las 8 y las 8:30
def my_cron():
    while True:
        d = datetime.now()

        if d.hour == 8 and d.minute <= 30:
            send_cryptos(chat_id)
            send_clima(chat_id)

        time.sleep(30)


# MAIN ################################
if __name__ == '__main__':
    # comandos disponibles
    bot.set_my_commands([
        telebot.types.BotCommand("/start", "Muestra los comandos principales")
    ])

    hilo = threading.Thread(name="hilo_pooling", target=my_pooling)
    hilo.start()

    hilo_cron = threading.Thread(name="hilo_cron", target=my_cron)
    hilo_cron.start()

    print('Bot iniciado')

