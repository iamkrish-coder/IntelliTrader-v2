from io import BytesIO

import pandas as pd
import requests


class NSEDataApi:
    def __init__(self, timeout=10):
        self.base_url = 'https://www.nseindia.com'
        self.session = requests.sessions.Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,"
                      "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "en-US,en;q=0.9"
        }
        self.timeout = timeout
        self.session.get(self.base_url, timeout=timeout)
        #self.cookies = []

    '''
    def __getCookies(self, renew=False):
        if len(self.cookies) > 0 and renew == False:
            return self.cookies

        r = requests.get(self.base_url, timeout=self.timeout, headers=self.headers)
        self.cookies = dict(r.cookies)
        return self.__getCookies()
    '''

    def get_historical_data(self, symbol, series, from_date, to_date):
        try:
            url = "/api/historical/cm/equity?symbol={0}&series=[%22{1}%22]&from={2}&to={3}&csv=true".format(
                symbol.replace('&', '%26'), series, from_date.strftime('%d-%m-%Y'), to_date.strftime('%d-%m-%Y'))
            r = self.session.get(self.base_url + url, timeout=self.timeout)
            df = pd.read_csv(BytesIO(r.content), sep=',', thousands=',')
            df = df.rename(
                columns={'Date ': 'date', 'series ': 'series', 'OPEN ': 'open', 'HIGH ': 'high', 'LOW ': 'low',
                         'PREV. CLOSE ': 'prev_close', 'ltp ': 'ltp', 'close ': 'close', '52W H ': 'hi_52_wk',
                         '52W L ': 'lo_52_wk', 'VOLUME ': 'volume', 'VALUE ': 'trdval', 'No of trades ': 'trades'})
            df.date = pd.to_datetime(df.date).dt.strftime('%Y-%m-%d')
            return df
        except:
            return None

    def fetch_index_from_nse(self, index_symbol):
        df = []
        res = self.session.get(self.base_url + '/api/equity-stockIndices?index=' + index_symbol, timeout=10)
        if res.status_code == 200:
            res_json = res.json()
            if 'data' in res_json:
                df = pd.json_normalize(res_json['data'])
            else:
                print('Data not returned from NSE')
                print(res_json)
        else:
            print('HTTP Request Failed: ')
            print(res)

        return df

    def save_index_to_csv(self, index_symbol, csv_file_name=None, delimiter=',', index=True, header=True):
        if csv_file_name is None:
            csv_file_name = index_symbol + '.csv'

        df = self.fetch_index_from_nse(index_symbol)
        if len(df) > 0:
            df.to_csv(csv_file_name, sep=delimiter, index=index, header=header)
            return True

        return False
