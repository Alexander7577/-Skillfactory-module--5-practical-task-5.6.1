import telebot
from telebot import types

import requests
import json

from config import TOKEN, currency
from extensions import ConversionException, Converter, Endings


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def welcome(message: telebot.types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("/start")
    item2 = types.KeyboardButton("Курс всех доступных валют")
    markup.add(item1, item2)

    bot.send_message(message.chat.id,
                     f"Приветствую, {message.chat.username}!\nЯ - Аркадий, бот созданный чтобы служить Вам."
                     f" Я могу конвертировать разные валюты.\n"
                     f"Формат ввода следующий:\n<Имя валюты> <в какую валюту перевести>\n<Количество переводимой валюты>",
                     reply_markup=markup)


@bot.message_handler(content_types=["text"])
def answer(message: telebot.types.Message):
    print(message.text)
    if message.text == "Курс всех доступных валют":
        bot.send_message(message.chat.id, "🫠идёт загрузка, подождите...")
        currencies = "Доступные валюты:\n"
        for keys, values in currency.items():
            r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={values}&tsyms=RUB")
            quantity = json.loads(r.content)["RUB"]
            currencies += f"{keys}: {quantity}₽ \n"

        bot.send_message(message.chat.id, currencies)

    else:
        data = message.text.split()
        try:
            if len(data) != 3:
                raise ConversionException("неправильный формат ввода!")

            quote, base, amount = data
            conversion = Converter.convert(quote, base, amount)

            ending = Endings(amount, conversion, quote.lower(), base.lower())

            text = f"цена за {amount} {ending.set_quote_ending()} равна {conversion} {ending.set_base_ending()}"
            bot.send_message(message.chat.id, text)
        except ConversionException as e:
            bot.reply_to(message, f"Ошибка пользователя.\n{e}")
        except Exception:
            bot.reply_to(message, f"не удаётся обработать запрос, попробуйте позже=(")


bot.polling(none_stop=True)
