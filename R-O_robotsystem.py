# импортируем библиотеки
import telebot
from telebot import types
import RPi.GPIO as GPIO
from time import sleep
import dht11

# пины для подачи сигнала моторам
ln1 = 26
ln2 = 19
ln3 = 13
ln4 = 6

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ln1,GPIO.OUT)
    GPIO.setup(ln2,GPIO.OUT)
    GPIO.setup(ln3,GPIO.OUT)
    GPIO.setup(ln4,GPIO.OUT)
    
def stop():
    GPIO.output(ln1,GPIO.LOW)
    GPIO.output(ln2,GPIO.LOW)
    GPIO.output(ln3,GPIO.LOW)
    GPIO.output(ln4,GPIO.LOW)

def left():
    setup()
    GPIO.output(ln1,GPIO.LOW)
    GPIO.output(ln2,GPIO.HIGH)
    GPIO.output(ln3,GPIO.HIGH)
    GPIO.output(ln4,GPIO.LOW)
    sleep(0.33)
    stop()
    
def forward():
    setup()
    GPIO.output(ln1,GPIO.LOW)
    GPIO.output(ln2,GPIO.HIGH)
    GPIO.output(ln3,GPIO.LOW)
    GPIO.output(ln4,GPIO.HIGH)
    sleep(5)
    stop()
    
def back():
    setup()
    GPIO.output(ln1,GPIO.HIGH)
    GPIO.output(ln2,GPIO.LOW)
    GPIO.output(ln3,GPIO.HIGH)
    GPIO.output(ln4,GPIO.LOW)
    sleep(5)
    stop()

def right():
    setup()
    GPIO.output(ln1,GPIO.HIGH)
    GPIO.output(ln2,GPIO.LOW)
    GPIO.output(ln3,GPIO.LOW)
    GPIO.output(ln4,GPIO.HIGH)
    sleep(0.33)
    stop()


bot = telebot.TeleBot("1688735327:AAEsc2qe6yPLoxIx8hBgCEu6U5dCnqUAFcE")
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
setup()
GPIO.cleanup()

# основная клавиатура
def get_commands_keyboard():
    command_select = types.ReplyKeyboardMarkup(row_width=5, resize_keyboard=True, one_time_keyboard=True)
    command_select.row('Температура и влажность', 'Освещённость')
    command_select.row('Видео', 'Информация')
    command_select.row('Управление роботом')
    command_select.row('Помощь')
    return command_select

# клавиатура для ручного управления роботом
def get_commands_keyboard_moving():
    command_select = types.ReplyKeyboardMarkup(row_width=5, resize_keyboard=True, one_time_keyboard=True)
    command_select.row('Вперёд')
    command_select.row('Влево', 'Вправо')
    command_select.row('Назад')
    command_select.row('EXIT')
    return command_select

# ответ при отправке пользователем '/start'
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Система Робо-Офис запущена', reply_markup=get_commands_keyboard())

# ответ при отправке пользователем '/help'
@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, '''Лист помощи
"Температура и влажность" - показывает температутру и влажность в помещении
"Видео" - отправляет последнее видео из библиотеки
"Освещённость" - показывает уровень освещения в помещении
"На базу" - отправляет робота на базу
"Информация" - показывает все показатели в помещении
"Помощь" - выводит лист помощи''')

# декоратор для текста
@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'температура и влажность':
        setup()
        instance = dht11.DHT11(pin = 4)
        result = instance.read()
        a = result.temperature
        while a == 0:
            instance = dht11.DHT11(pin = 4)
            result = instance.read()
            a = result.temperature
        bot.send_message(message.chat.id, f"""Cейчас в комнате:
TEMP: {result.temperature} °C
HUM: {result.humidity} %""")
    elif message.text.lower() == 'помощь':
        bot.send_message(message.chat.id, '''Лист помощи
"Температура и влажность в помещении" - показывает температутру и влажность в помещении
"Видео" - отправляет последнее видео из библиотеки
"Освещённость" - показывает уровень освещения в помещении
"На базу" - отправляет робота на базу
"Вся информация" - показывает все показатели в помещении
"Помощь" - выводит лист помощи''')
    elif message.text.lower() == 'информация':
        setup()
        instance = dht11.DHT11(pin = 4)
        result = instance.read()
        a = result.temperature
        while a == 0:
            instance = dht11.DHT11(pin = 4)
            result = instance.read()
            a = result.temperature
        bot.send_message(message.chat.id, f'''В помещении:
Температура: {result.temperature} °C
Влажность: {result.humidity} %
Освещённость: none''')
    elif message.text.lower() == 'освещённость':
        bot.send_message(message.chat.id, 'а нема')
    elif message.text.lower() == 'управление роботом':
        bot.send_message(message.chat.id, 'Запущено ручное управление роботом', reply_markup=get_commands_keyboard_moving())
    elif message.text.lower() == 'вперёд':
        forward()
    elif message.text.lower() == 'назад':
        back()
    elif message.text.lower() == 'вправо':
        right()
    elif message.text.lower() == 'влево':
        left()
    elif message.text.lower() == 'exit':
        bot.send_message(message.chat.id, 'Bot in auto rezhime', reply_markup=get_commands_keyboard())
            
bot.polling(none_stop=True)
