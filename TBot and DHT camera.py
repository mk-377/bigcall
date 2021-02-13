# импортируем dofiga библиотек
import telebot
from telebot import types
import RPi.GPIO as GPIO
import dht11
import picamera
import time

bot = telebot.TeleBot("1688735327:AAEsc2qe6yPLoxIx8hBgCEu6U5dCnqUAFcE")
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
cam = picamera.PiCamera()

cam.start_preview('/home/pi/CAM-VIDEOS/video-try1.h264')

def checkTH():
    instance = dht11.DHT11(pin = 4)
    global result = instance.read()
    a = result.temperature
    while a == 0:
        instance = dht11.DHT11(pin = 4)
        result = instance.read()
        a = result.temperature

# создаем клавиатуру
def get_commands_keyboard():
    command_select = types.ReplyKeyboardMarkup(row_width=12, resize_keyboard=True, one_time_keyboard=True)
    command_select.row('room temp/hum', 'room light lvl')
    command_select.row('video', 'all info')
    command_select.row('robot back')
    command_select.row('/help')
    return command_select

# декоратор для команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, '''Система Робо-Офис запущена
Dostypno: only DHT
Razrabotka: Camera record and robotplaces command''', reply_markup=get_commands_keyboard())

@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, '''Help sheet
"room temp/hum" - show temperature and humidity in the room
"video" - send last video from robot`s videolibrary
"room light lvl" - show illumination level in the room
"robot back" - sends the robot to the base
"all info" - report of room`s indicators
"help" - show help sheet''')

# декоратор для текста
@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'room temp/hum':
        checkTH()
        bot.send_message(message.chat.id, f"""Cейчас в комнате:
TEMP: {result.temperature} °C
HUM: {result.humidity} %""")
        print(message.chat.id)
    elif message.text.lower() == 'video':
         last_video = open('/home/pi/CAM-VIDEOS/video-try1.h264')
         cam.stop_preview()
         bot.send_message(message.chat.id, last_video)
         
        
# для работы нон стоп
bot.polling(none_stop=True)