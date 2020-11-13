import sys
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import argparse


class CRYPTO:
    def __init__(self, cryptocurrency, currency):
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
            # return "{:.2f}".format(data['data']['1']['quote']['INR']['price'])
            print(data['data'][self.parameters['id']]
                  ['name'], currency, end=" ")
            print("{:.2f}".format(
                data['data'][self.parameters['id']]['quote'][currency]['price']))
            # print(data)

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(f"\n!! ERROR !!\n\n{e}\n\n!! ERROR !!\n\nPlease Try Later")


class IFTTT:
    def __init__(self):
        self.ifttt_url = 'https://maker.ifttt.com/trigger/bitcoin_price_changed/with/key/bNx9O6cKq_CpRFdguicR67vdBo2geCTGEYsRgbt3mWK'

    def trigger_event(self, price):
        session = Session()
        session.post(self.ifttt_url, json={"value1": price})


def parse_user_input():
    parser = argparse.ArgumentParser(
        description='CRYPTOCURRENCY PRICE NOTIFIER: Default Arguments: bitcoin, INR, 1200000, 60')

    parser.add_argument('--c', default='bitcoin',
                        type=str, help="Cryptocurrency Type: ['bitcoin', 'etherium', 'tether', 'xrp', 'litecoin']")
    parser.add_argument('--f', default='INR', type=str,
                        help="Fiat Currency ['INR', 'USD']")
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

    if currency.upper() not in ['INR', 'USD']:
        print(f"\nSorry!\n'{currency}' is not supported yet!")
        print("\nPlease enter one of these cryptocurrencies: ['INR', 'USD']")
        sys.exit()

    return cryptocurrency.lower(), currency.upper(), threshold_price, time_interval


if __name__ == '__main__':
    cryptocurrency, currency, threshold_price, time_interval = parse_user_input()

    bitcoin = CRYPTO(cryptocurrency, currency)
    bitcoin.fetch_price()
    # current_price = bitcoin.fetch_price()

    # ifttt_user = IFTTT()
    # ifttt_user.trigger_event(current_price)
