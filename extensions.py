import requests
import json
from config import exchanges

class ConvertionExeption(Exception):
    pass

class СurrencyConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):

        if quote == base:
            raise ConvertionExeption(f"Невозможно конвертировать одинаковые валюты {base}")

        try:
            quote_ticker = exchanges[quote]
        except KeyError:
            raise ConvertionExeption(f"Не могу обоработать валюту {quote}")

        try:
            base_ticker = exchanges[base]
        except KeyError:
            raise ConvertionExeption(f"Не могу обоработать валюту {base}")

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionExeption(f"Не могу обработать количество {amount}")

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}")
        total_base = json.loads(r.content)[exchanges[base]] * float(amount)

        return total_base
