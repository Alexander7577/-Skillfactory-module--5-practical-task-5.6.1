import requests
import json

from config import currency


class ConversionException(Exception):
    pass


class Converter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        try:
            quote_ticker = currency[quote.lower()]

        except KeyError:
            raise ConversionException("Не удалось обработать валюту")

        try:
            base_ticker = currency[base.lower()]

        except KeyError:
            raise ConversionException("Не удалось обработать переводимую валюту")

        try:
            amount = float(amount)

        except ValueError:
            raise ConversionException("Не удалось обработать количество переводимой валюты")

        call = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}")
        conversion = float(json.loads(call.content)[currency[base.lower()]]) * amount
        return conversion


class Endings:
    def __init__(self, amount, conversion, quote, base):
        self.amount = amount
        self.conversion = conversion
        self.quote = quote
        self.base = base

    @staticmethod
    def get_rub_ending(value):
        if value == 1:
            return "ль"
        elif 1 < value <= 4 or value < 1:
            return "ля"
        else:
            return "лей"

    @staticmethod
    def get_usd_ending(value):
        if value == 1:
            return "р"
        elif 1 < value <= 4 or value < 1:
            return "ра"
        else:
            return "ров"

    @staticmethod
    def get_gbp_ending(value):
        if value == 1:
            return "т"
        elif 1 < value <= 4 or value < 1:
            return "та"
        else:
            return "тов"

    @staticmethod
    def get_try_ending(value):
        if value == 1:
            return "ра"
        elif 1 < value <= 4 or value < 1:
            return "ры"
        else:
            return "р"

    @staticmethod
    def get_uah_ending(value):
        if value == 1:
            return "на"
        elif 1 < value <= 4 or value < 1:
            return "ны"
        else:
            return "ен"

    @staticmethod
    def get_pln_ending(value):
        if value == 1:
            return "ый"
        else:
            return "ых"

    @staticmethod
    def get_cny_ending(value):
        if value == 1:
            return "ь"
        elif 1 < value <= 4 or value < 1:
            return "я"
        else:
            return "ей"

    @staticmethod
    def get_jpy_ending(value):
        if value == 1:
            return "на"
        elif 1 < value <= 4 or value < 1:
            return "ны"
        else:
            return "н"

    @staticmethod
    def get_btc_ending(value):
        if value == 1:
            return "н"
        elif 1 < value <= 4 or value < 1:
            return "на"
        else:
            return "нов"

    @staticmethod
    def get_eth_ending(value):
        if value == 1:
            return "м"
        elif 1 < value <= 4 or value < 1:
            return "ма"
        else:
            return "мов"

    def set_quote_ending(self):
        if self.quote == "рубль":
            quote = f"руб{self.get_rub_ending(int(self.amount))}"
            return quote

        if self.quote == "доллар":
            quote = f"долла{self.get_usd_ending(int(self.amount))}"
            return quote

        if self.quote == "евро":
            return self.quote

        if self.quote == "фунт":
            quote = f"фун{self.get_gbp_ending(int(self.amount))}"
            return quote

        if self.quote == "лира":
            quote = f"ли{self.get_try_ending(int(self.amount))}"
            return quote

        if self.quote == "гривна":
            quote = f"грив{self.get_uah_ending(int(self.amount))}"
            return quote

        if self.quote == "тенге":
            return self.quote

        if self.quote == "злотый":
            quote = f"злот{self.get_pln_ending(int(self.amount))}"
            return quote

        if self.quote == "юань":
            quote = f"юан{self.get_cny_ending(int(self.amount))}"
            return quote

        if self.quote == "йена":
            quote = f"йе{self.get_jpy_ending(int(self.amount))}"
            return quote

        if self.quote == "биткоин":
            quote = f"биткои{self.get_btc_ending(int(self.amount))}"
            return quote

        if self.quote == "эфириум":
            quote = f"эфириу{self.get_eth_ending(int(self.amount))}"
            return quote

    def set_base_ending(self):
        if self.base == "рубль":
            base = f"руб{self.get_rub_ending(int(self.conversion))}"
            return base

        if self.base == "доллар":
            base = f"долла{self.get_usd_ending(int(self.conversion))}"
            return base

        if self.base == "евро":
            return self.base

        if self.base == "фунт":
            base = f"фун{self.get_gbp_ending(int(self.conversion))}"
            return base

        if self.base == "лира":
            base = f"ли{self.get_try_ending(int(self.conversion))}"
            return base

        if self.base == "гривна":
            base = f"грив{self.get_uah_ending(int(self.conversion))}"
            return base

        if self.base == "тенге":
            return self.base

        if self.base == "злотый":
            base = f"злот{self.get_pln_ending(int(self.conversion))}"
            return base

        if self.base == "юань":
            base = f"юан{self.get_cny_ending(int(self.conversion))}"
            return base

        if self.base == "йена":
            base = f"йе{self.get_jpy_ending(int(self.conversion))}"
            return base

        if self.base == "биткоин":
            base = f"биткои{self.get_btc_ending(int(self.conversion))}"
            return base

        if self.base == "эфириум":
            base = f"эфириу{self.get_eth_ending(int(self.conversion))}"
            return base
