<p align="center">
  <img src="crypto.jpg" alt="Bitcoin Price Notification">
</p>

# Python Project - Bitcoin Price Notification

A simple python app that fetch latest price of cryptocurrency periodically and send Telegram notifications based on threshold price.

## Table of contents

- [Technologies](#technologies)
- [Setup](#setup)
- [Usage](#usage)

## Technologies

Project is created with:

- Python: 3.8.5
- requests: 2.24.0 (Python external library for making get/post requests)
- pytz: 2020.4 (Python external library for timezone)
- flake8: 3.8.4 (Python external library for linting)
- CoinMarketCap API
- IFTTT
- Telegram

## Setup

To run this project:

1. Clone this repo.
2. Install Python
3. Install requests library:

   `$ pip install requests`

4. Install pytz library:

   `$ pip install pytz`

5. Create account on [CoinMarketCap](https://pro.coinmarketcap.com/signup) and get API Key.
6. Create account on Telegram and create a public channel and add @IFTTT to that channel as an admin.
7. Create account on [IFTTT](https://ifttt.com/) and create 2 applets as:
   `if this(webhook), then that(Telegram message)`

   - Applet-1:

     Event Name = `crypto_price_update`

     Target chat ==> Select the Telegram channel you have created and added @IFTTT in that channel.

     Message text = `Latest {{Value1}} prices in {{Value2}}:<br>{{Value3}}`

   - Applet-2:

     Event Name = `crypto_price_emergency`

     Target chat ==> Select the Telegram channel you have created and added @IFTTT in that channel.

     Message text = `Emergency!<br>{{Value1}} price is at {{Value2}} {{Value3}}.<br>Buy or sell now!`

8. In `main.py` file replace CoinMarketCap API key and IFTTT maker API key with your keys.

   - ```
     self.headers = {
             'Accepts': 'application/json',
             'X-CMC_PRO_API_KEY': 'your-CoinMarketCap-key',
         }
     ```

   - `https://maker.ifttt.com/trigger/{}/with/key/{your-IFTTT-key}`

9. Install flake8 library:

   - `$ pip install flake8`

   - goto root directory where `main.py` file is present.
   - Run this command and check for any errors:

   - `$ python -m flake8`

10. run `main.py`
    - `$ python main.py`
    - by default it will run with 4 default arguments:
      `-c bitcoin -f INR -p 1200000 -t 300`
    - these all are optional arguments, if you want to give arguments then it will take that otherwise it will defaults to the above arguments.
11. After every 300 sec (5 min), latest price will be fetched and compared with the threshold price and you will get emergency notification on your Telegram channel if the latest price is below the threshold price. Also, you will get 5 latest price updates after every 25 minutes.

## Usage

- `$ python main.py -h`

  ```
  usage: main.py [-h] [-c C] [-f F] [-p P] [-t T]

  CRYPTOCURRENCY PRICE NOTIFIER: Default Arguments: bitcoin, INR, 1200000, 300

  optional arguments:
    -h, --help  show this help message and exit
    -c C        Cryptocurrency Type: ['bitcoin', 'etherium', 'tether', 'xrp', 'litecoin']
    -f F        Fiat Currency ['INR', 'USD', 'CNY', 'EUR', 'JPY']
    -p P        Threshold Price for emergency notification
    -t T        Time Interval in seconds for sending Telegram notification
  ```

- `$ python main.py`

  It will run with default arguments as: bitcoin, INR, 1200000, 300

  It will fetch latest price for `Bitcoin` in `INR` after every `300 seconds` and send Telegram notification if latest price will be less than `INR 1200000`.

  After every `5*300 = 1500 seconds or 25 minutes`, you will get notified on Telegram with latest 5 prices for every past 5 minutes.

- `$ python main.py -c xrp -f USD -p 0.25 -t 60`

  It will fetch latest price for `XRP` in `USD` after every `60 seconds` and send Telegram notification if latest price will be less than `USD 0.25`.

  After every `5*60 = 300 seconds or 5 minutes`, you will get notified on Telegram with latest 5 prices for every past 1 minute.

- `$ python main.py -t 60`

  It will fetch latest price for `Bitcoin` in `INR` after every `60 seconds` and send Telegram notification if latest price will be less than `INR 1200000`.

  After every `5*60 = 300 seconds or 5 minutes`, you will get notified on Telegram with latest 5 prices for every past 1 minute.
