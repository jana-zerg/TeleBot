import telebot
from config import exchanges, TOKEN
from extensions import ConvertionExeption, СurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = "Привет! Я помогу тебе конвертировать валюты. Введи через пробел <валюту, которую переводим>  \
<валюту, в которую переводим> <количество переводимой валюты>. Увидеть список доступных валют: набери /values"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Я еще маленький и знаю мало валют:"
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def converter(message: telebot.types.Message):
    try:
        values = message.text.split()

        if len(values) != 3:
            raise ConvertionExeption("Слишком много параметров")

        quote, base, amount = values
        total_base = СurrencyConverter.convert(quote, base, amount)
    except ConvertionExeption as e:
        bot.reply_to(message, f"Ошибка пользователя. \n{e}")
    except Exception as e:
        bot.reply_to(message, f"Что-то пошло не так\n {e}")
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
