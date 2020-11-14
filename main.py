import sys
import json
import argparse
import time
from datetime import datetime
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


class CRYPTO:
    def __init__(self, cryptocurrency, currency):
        self.cryptocurrency = cryptocurrency
        self.currency = currency
        # coinmarketcap id for top cryptocurrencies
        self.top_crypto_id = {
            'bitcoin': '1',
            'etherium': '1027',
            'tether': '825',
            'xrp': '52',
            'litecoin': '2',
        }
        self.crypto_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        self.parameters = {
            'id': self.top_crypto_id[cryptocurrency],
            'convert': currency
        }
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': 'ea1afa6b-d782-4ebe-8747-9b18ad5e5f51',
        }

    def fetch_price(self):
        session = Session()
        session.headers.update(self.headers)

        try:
            response = session.get(self.crypto_url, params=self.parameters)
            data = json.loads(response.text)
            price = "{:.2f}".format(
                data['data'][self.parameters['id']]['quote'][self.currency]['price'])
            print(data['data'][self.parameters['id']]
                  ['name'], self.currency, price)

            return float(price)

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(
                f"\nNot able to fetch price of '{self.cryptocurrency}' at this moment!\nPlease try later!")
            print(f"\n!! ERROR !!\n{e}\n")

    def format_crypto_history(self, crypto_history):
        rows = []
        for crypto_price in crypto_history:
            date = crypto_price['date'].strftime('%d.%m.%Y %H:%M')
            price = crypto_price['price']
            row = '{}: {} <b>{}</b>'.format(date, self.currency, price)
            rows.append(row)
        return '<br>'.join(rows)


class IFTTT:
    def __init__(self, cryptocurrency, currency):
        self.ifttt_url = 'https://maker.ifttt.com/trigger/{}/with/key/bNx9O6cKq_CpRFdguicR67vdBo2geCTGEYsRgbt3mWK'
        self.cryptocurrency = cryptocurrency
        self.currency = currency

    def trigger_event(self, event, message):
        session = Session()
        ifttt_event_url = self.ifttt_url.format(event)
        data = {'value1': self.cryptocurrency.upper(),
                'value2': self.currency, 'value3': message}

        try:
            session.post(ifttt_event_url, json=data)

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print("-" * 150)
            print(
                f"\nNot able to send notification at this moment!\nPlease try later!")
            print(f"\n!! ERROR !!\n{e}\n")


def parse_user_args():
    parser = argparse.ArgumentParser(
        description='CRYPTOCURRENCY PRICE NOTIFIER: Default Arguments: bitcoin, INR, 1200000, 60')

    parser.add_argument('--c', default='bitcoin',
                        type=str, help="Cryptocurrency Type: ['bitcoin', 'etherium', 'tether', 'xrp', 'litecoin']")
    parser.add_argument('--f', default='INR', type=str,
                        help="Fiat Currency ['INR', 'USD', 'CNY', 'EUR', 'JPY']")
    parser.add_argument('--p', default=1200000,
                        type=int, help='Threshold Price for emergency notification')
    parser.add_argument('--t', default=60,
                        type=int, help='Time Interval for Notification in seconds')

    user_input = parser.parse_args()

    cryptocurrency = user_input.c
    currency = user_input.f
    threshold_price = user_input.p
    time_interval = user_input.t

    top_crypto = ['bitcoin', 'etherium', 'tether', 'xrp', 'litecoin']
    if cryptocurrency.lower() not in top_crypto:
        print(f"\nSorry!\n'{cryptocurrency}' is not supported yet!")
        print("\nPlease enter one of these cryptocurrencies:", top_crypto)
        sys.exit()
    if currency.upper() not in ['INR', 'USD', 'CNY', 'EUR', 'JPY']:
        print(f"\nSorry!\n'{currency}' is not supported yet!")
        print(
            "\nPlease enter one of these cryptocurrencies: ['INR', 'USD', 'CNY', 'EUR', 'JPY']")
        sys.exit()
    if threshold_price < 1:
        print(f"\nPlease enter threshold_price greater than 1.")
        sys.exit()
    if time_interval < 1:
        print(f"\nPlease enter time_interval greater than 1.")
        sys.exit()

    return cryptocurrency.lower(), currency.upper(), threshold_price, time_interval


if __name__ == '__main__':
    cryptocurrency, currency, threshold_price, time_interval = parse_user_args()
    print("\nCRYPTO PRICE NOTIFIER v-0.1\n")

    bitcoin = CRYPTO(cryptocurrency, currency)
    ifttt_user = IFTTT(cryptocurrency, currency)

    crypto_history = []
    while True:
        price = bitcoin.fetch_price()
        date = datetime.now()
        crypto_history.append({'date': date, 'price': price})

        if price < threshold_price:
            ifttt_user.trigger_event('crypto_price_emergency', price)

        if len(crypto_history) == 5:
            ifttt_user.trigger_event('crypto_price_update',
                                     bitcoin.format_crypto_history(crypto_history))
            crypto_history = []

        time.sleep(time_interval)
