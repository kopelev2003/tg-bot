import telebot
from telebot import types
from CurrencyParser import currency_checker
import pyowm
from pyowm import exceptions
import schedule
import threading

TOKEN = "1240393676:AAExBvQO0i36AQPrLDvnbEKY61cstyN6ZWY"
bot = telebot.TeleBot(TOKEN)
own = pyowm.OWM("8227d9262c5328258b70e2a914ce9cf7", language="RU")
NAMES = ["ДОЛЛАР: ", "ЕВРО: ", "РУБЛЬ: ", "ПОЛЬСКИЙ ЗЛОТЫЙ: ", "ШВЕЙЦАРСКИЙ ФРАНК: ", "АНГЛИЙСКИЙ ФУНТ СТЕРЛИНГОВ: ",
         "БЕЛОРУССКИЙ РУБЛЬ: "]

global time_func


@bot.message_handler(commands=["start"])
def start(message):
    send_message = f"<b>Добро пожаловать, {message.from_user.first_name}</b>\nВведите /help для ознакомления с функциями бота"
    bot.send_message(message.chat.id, send_message, parse_mode="html")


@bot.message_handler(commands=["help"])
def get_help(message):
    send_message = f"<b>/weather</b> - Для просмотра погоды в нужном вам городе\n<b>/currency</b> - Для просмотра актуального курса валют\n<b>/translation</b> - Калькулятор обмена валют\n<b>/time</b> - Для того чтобы указать функциям /weather и /currency время исполнения"
    bot.send_message(message.chat.id, send_message, parse_mode="html")


@bot.message_handler(commands=['currency'])
def currency(message):
    bot.send_message(message.chat.id, f"<b>КУРС ВАЛЮТ К ГРИВНЕ НА СЕГОДНЯ: </b>", parse_mode="html")
    x = int(0)
    currencies = currency_checker()
    for NAME in NAMES:
        bot.send_message(message.chat.id, NAME + currencies[x])
        x += 1


@bot.message_handler(commands=["translation"])
def translation_currency(message):
    send = bot.send_message(message.chat.id, "Выберите и введите число:"
                                             "\n1) Перевод из долларов в гривну"
                                             "\n2) Перевод из евро в гривну"
                                             "\n3) Перевод из российских рублей в гривну"
                                             "\n4) Перевод из польских злотых в гривну"
                                             "\n5) Перевод из швейцарских франков в гривну"
                                             "\n6) Перевод из английских фунтов стерлингов в гривну"
                                             "\n7) Перевод из белорусских рублей в гривну"
                                             "\n8) Перевод из гривны в доллары"
                                             "\n9) Перевод из гривны в евро"
                                             "\n10) Перевод из гривны в российские рубли"
                                             "\n11) Перевод из гривны в польские злоты"
                                             "\n12) Перевод из гривны в швейцарские франки"
                                             "\n13) Перевод из гривны в английских фунтов стерлингов"
                                             "\n14) Перевод из гривны в белорусские рубли")
    bot.register_next_step_handler(send, translation)


def translation(message):
    send = bot.reply_to(message, 'Введите количество: ')
    if message.text == "1":
        bot.register_next_step_handler(send, usd_to_uah)
    elif message.text == "2":
        bot.register_next_step_handler(send, eur_to_uah)
    elif message.text == "3":
        bot.register_next_step_handler(send, rub_to_uah)
    elif message.text == "4":
        bot.register_next_step_handler(send, pln_to_uah)
    elif message.text == "5":
        bot.register_next_step_handler(send, chf_to_uah)
    elif message.text == "6":
        bot.register_next_step_handler(send, gbp_to_uah)
    elif message.text == "7":
        bot.register_next_step_handler(send, byn_to_uah)
    elif message.text == "8":
        bot.register_next_step_handler(send, uah_to_usd)
    elif message.text == "9":
        bot.register_next_step_handler(send, uah_to_eur)
    elif message.text == "10":
        bot.register_next_step_handler(send, uah_to_rub)
    elif message.text == "11":
        bot.register_next_step_handler(send, uah_to_pln)
    elif message.text == "12":
        bot.register_next_step_handler(send, uah_to_chf)
    elif message.text == "13":
        bot.register_next_step_handler(send, uah_to_gbp)
    elif message.text == "14":
        bot.register_next_step_handler(send, uah_to_byn)
    else:
        bot.send_message(message.chat.id, f"<b>ВЫ ВВЕЛИ НЕ ЧИСЛО или ВЫШЛИ ЗА ПРЕДЕЛЫ</b>", parse_mode="html")
        bot.send_message(message.chat.id, "Введите число от 1-14 ")
        translation_currency(message)


def usd_to_uah(message):  # перевод из долларов в гривну
    uah = int(message.text) * float(currency_checker()[0])
    uah = round(uah, 2)
    return bot.send_message(message.chat.id, message.text + "$ = " + str(uah) + " ₴")


def eur_to_uah(message):  # перевод из евро в гривну
    uah = int(message.text) * float(currency_checker()[1])
    uah = round(uah, 2)
    return bot.send_message(message.chat.id, message.text + "€ = " + str(uah) + " ₴")


def rub_to_uah(message):  # перевод из российских рублей в гривну
    uah = int(message.text) * float(currency_checker()[2])
    uah = round(uah, 2)
    return bot.send_message(message.chat.id, message.text + "₽ = " + str(uah) + " ₴")


def pln_to_uah(message):  # перевод из польских злотых в гривну
    uah = int(message.text) * float(currency_checker()[3])
    uah = round(uah, 2)
    return bot.send_message(message.chat.id, message.text + "zł = " + str(uah) + " ₴")


def chf_to_uah(message):  # перевод из швейцарских франков в гривну
    uah = int(message.text) * float(currency_checker()[4])
    uah = round(uah, 2)
    return bot.send_message(message.chat.id, message.text + "₣ = " + str(uah) + " ₴")


def gbp_to_uah(message):  # перевод из английских фунтов стерлингов в гривну
    uah = int(message.text) * float(currency_checker()[5])
    uah = round(uah, 2)
    return bot.send_message(message.chat.id, message.text + "£ = " + str(uah) + " ₴")


def byn_to_uah(message):  # перевод из белорусских рублей в гривну
    uah = int(message.text) * float(currency_checker()[6])
    uah = round(uah, 2)
    return bot.send_message(message.chat.id, message.text + "Br = " + str(uah) + " ₴")


#
def uah_to_usd(message):  # перевод из гривны в доллары
    usd = currency_checker()[0]
    formula = 1 / float(usd)
    uah = int(message.text) * formula
    uah = round(uah, 2)
    return bot.send_message(message.chat.id, message.text + "₴ = " + str(uah) + " $")


def uah_to_eur(message):  # перевод из гривны в евро
    eur = currency_checker()[1]
    formula = 1 / float(eur)
    uah = int(message.text) * formula
    uah = round(uah, 2)
    return bot.send_message(message.chat.id, message.text + "₴ = " + str(uah) + " €")


def uah_to_rub(message):  # перевод из гривны в российские рубли
    rub = currency_checker()[2]
    formula = 1 / float(rub)
    uah = int(message.text) * formula
    uah = round(uah, 2)
    return bot.send_message(message.chat.id, message.text + "₴ = " + str(uah) + " ₽")


def uah_to_pln(message):  # перевод из гривны в польские злоты
    pln = currency_checker()[3]
    formula = 1 / float(pln)
    uah = int(message.text) * formula
    uah = round(uah, 2)
    return bot.send_message(message.chat.id, message.text + "₴ = " + str(uah) + " zł")


def uah_to_chf(message):  # перевод из гривны в швейцарские франки
    chf = currency_checker()[4]
    formula = 1 / float(chf)
    uah = int(message.text) * formula
    uah = round(uah, 2)
    return bot.send_message(message.chat.id, message.text + "₴ = " + str(uah) + " ₣")


def uah_to_gbp(message):  # перевод из гривны в английских фунтов стерлингов
    gbp = currency_checker()[5]
    formula = 1 / float(gbp)
    uah = int(message.text) * formula
    uah = round(uah, 2)
    return bot.send_message(message.chat.id, message.text + "₴ = " + str(uah) + " £")


def uah_to_byn(message):  # перевод из гривны в белорусские рубли
    byn = currency_checker()[6]
    formula = 1 / float(byn)
    uah = int(message.text) * formula
    uah = round(uah, 2)
    return bot.send_message(message.chat.id, message.text + "₴ = " + str(uah) + " Br")


@bot.message_handler(commands=['weather'])
def weather(message):
    send = bot.send_message(message.chat.id, "Введите название города:")
    bot.register_next_step_handler(send, get_weather)


def get_weather(message):
    try:
        try:
            observation = own.weather_at_place(message.text)
            w = observation.get_weather()
            temp = w.get_temperature('celsius')["temp"]
            status = w.get_detailed_status()
            # sunrise = w.get_sunrise_time("iso")
            # sunset = w.get_sunset_time("iso")
            wind = w.get_wind()['speed']
            humidity = w.get_humidity()
            bot.send_message(message.chat.id,
                             "ПРОГНОЗ ПОГОДЫ В ГОРОДЕ: " + message.text +
                             "\nТЕМПЕРАТУРА: " + str(int(temp)) + "°C" +
                             "\nСТАТУС: " + status +
                             # "\nВОСХОД СОЛНЦА: " + sunrise +
                             # "\nЗАХОД СОЛНЦА: " + str(sunset) +
                             "\nСКОРОСТЬ ВЕТРА: " + str(wind) + "м/с" +
                             "\nВЛАЖНОСТЬ ВОЗДУХА: " + str(humidity) + "%"
                             )
        except pyowm.exceptions.api_response_error.NotFoundError:
            bot.send_message(message.chat.id, "Данного названия города не существует")
            weather(message)
    except pyowm.exceptions.api_call_error.APICallTimeoutError:
        bot.send_message(message.chat.id, "Проблема с соединением")
        weather(message)


@bot.message_handler(commands=["time"])
def get_time(message):
    send = bot.reply_to(message, "Выберите функцию (Введите либо weather, либо currency)  ")
    bot.register_next_step_handler(send, choice)

    def go():
        while True:
            schedule.run_pending()
    t = threading.Thread(target=go, name="тест")
    t.start()


def choice(message):
    if message.text == "weather":
        send = bot.reply_to(message, " Укажите время: ")
        bot.register_next_step_handler(send, time_for_weather)
    elif message.text == "currency":
        send = bot.reply_to(message, " Укажите время: ")
        bot.register_next_step_handler(send, time_for_currency)
    else:
        bot.send_message(message.chat.id, "Попробуйте заново! ")
        get_time(message)

def check():
    print("I'm working!!!")

def time_for_weather(message):
    try:
        global time_func
        time_func = message.text
        schedule.every().day.at(str(time_func)).do(check)
        send = bot.reply_to(message, "Введите название города: ")
        bot.register_next_step_handler(send, turn_func)
    except schedule.ScheduleValueError:
        bot.send_message(message.chat.id, "Введите время в формате HH:MM")
        choice(message)

def turn_func(message):
    try:
        observation = own.weather_at_place(message.text)
        w = observation.get_weather()
        schedule.every().day.at(str(time_func)).do(get_weather, message)
    except pyowm.exceptions.api_response_error.NotFoundError:
        bot.send_message(message.chat.id, "Данного названия города не существует")
        choice(message)


def time_for_currency(message):
    try:
        schedule.every().day.at(str(message.text)).do(currency, message)
    except schedule.ScheduleValueError:
        bot.send_message(message.chat.id, "Введите время в формате HH:MM")
        choice(message)



@bot.message_handler(content_types=["text"])
def something_text(message):
    bot.send_message(message.chat.id, f"Выберите один из предложенных вариантов:\n<b>/weather</b>\n<b>/currency</b>\n<b>/translation</b>\n<b>/time</b>", parse_mode="html")





bot.polling(none_stop=True)
