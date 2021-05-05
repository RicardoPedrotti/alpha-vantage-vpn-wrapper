import requests
import pandas as pd
import random


class AlphaData:
    def __init__(self,
                 api_keys_csv='config/API_KEYS.csv'):
        self.API_KEYS_LIST = list(pd.read_csv(api_keys_csv)['API_KEYS'])

    def get_random_api_key(self):
        return self.API_KEYS_LIST[random.randrange(len(self.API_KEYS_LIST))]


    def alpha_to_pandas(self, symbol, endpoint, interval='15min', outputsize='full'):
        # ts = TimeSeries(key=get_random_api_key(), output_format='pandas')
        call_start = 'https://www.alphavantage.co/query?function='
        key = self.get_random_api_key()

        if endpoint == 'TIME_SERIES_INTRADAY':
            call = call_start + '{}&symbol={}&interval={}&outputsize={}&apikey={}'.format(endpoint, symbol, interval,
                                                                                          outputsize, key)
            print('Calling... ' + call)
            r = requests.get(call)
            r_json = r.json()
            metadata = r_json["Meta Data"]
            data = pd.DataFrame(r_json["Time Series ({})".format(interval)]).T
            # data = ts.get_intraday(symbol, interval, outputsize)

        elif endpoint == 'TIME_SERIES_DAILY':
            call = call_start + '{}&symbol={}&outputsize={}&apikey={}'.format(endpoint, symbol, outputsize, key)
            print('Calling... ' + call)
            r = requests.get(call)
            r_json = r.json()
            metadata = r_json["Meta Data"]
            data = pd.DataFrame(r_json["Time Series ({})".format(interval)]).T
            # data = ts.get_daily(symbol, outputsize)

        elif endpoint == 'TIME_SERIES_DAILY_ADJUSTED':
            call = call_start + '{}&symbol={}&outputsize={}&apikey={}'.format(endpoint, symbol, outputsize, key)
            print('Calling... ' + call)
            r = requests.get(call)
            r_json = r.json()
            metadata = r_json["Meta Data"]
            data = pd.DataFrame(r_json['Time Series (Daily)']).T
            # data = ts.get_daily_adjusted(symbol, outputsize)

        elif endpoint == 'TIME_SERIES_WEEKLY':
            call = call_start + '{}&symbol={}&outputsize={}&apikey={}'.format(endpoint, symbol, key)
            print('Calling... ' + call)
            r = requests.get(call)
            r_json = r.json()
            metadata = r_json["Meta Data"]
            data = pd.DataFrame(r_json["Time Series ({})".format(interval)]).T
            # data = ts.get_weekly(symbol)

        elif endpoint == 'TIME_SERIES_WEEKLY_ADJUSTED':
            call = call_start + '{}&symbol={}&apikey={}'.format(endpoint, symbol, key)
            print('Calling... ' + call)
            r = requests.get(call)
            r_json = r.json()
            metadata = r_json["Meta Data"]
            data = pd.DataFrame(r_json["Time Series ({})".format(interval)]).T
            # data = ts.get_weekly_adjusted(symbol)

        elif endpoint == 'TIME_SERIES_MONTHLY':
            call = call_start + '{}&symbol={}&apikey={}'.format(endpoint, symbol, key)
            print('Calling... ' + call)
            r = requests.get(call)
            r_json = r.json()
            metadata = r_json["Meta Data"]
            data = pd.DataFrame(r_json["Time Series ({})".format(interval)]).T
            # data = ts.get_monthly(symbol)

        elif endpoint == 'TIME_SERIES_MONTHLY_ADJUSTED':
            call = call_start + '{}&symbol={}&apikey={}'.format(endpoint, symbol, key)
            print('Calling... ' + call)
            r = requests.get(call)
            r_json = r.json()
            metadata = r_json["Meta Data"]
            data = pd.DataFrame(r_json["Time Series ({})".format(interval)]).T
            # data = ts.get_monthly_adjusted(symbol)

        elif endpoint == 'QUOTE_ENDPOINT':
            call = call_start + 'GLOBAL_QUOTE&symbol={}&apikey={}'.format(symbol, key)
            print('Calling... ' + call)
            r = requests.get(call)
            r_json = r.json()
            metadata = r_json["Meta Data"]
            data = pd.DataFrame(r_json["Time Series ({})".format(interval)]).T
            # data = ts.get_quote_endpoint(symbol)
        else:
            return print(
                '''The Endpoint {} does not exist! See 'Endpoint Cheat Sheet' for more information'''.format(endpoint))

        # data['1. open'] = data['1. open'].astype(float)
        # data['2. high'] = data['2. high'].astype(float)
        # data['3. low'] = data['3. low'].astype(float)
        # data['4. close'] = data['4. close'].astype(float)
        # data['5. volume'] = data['5. volume'].astype(int)
        return data
