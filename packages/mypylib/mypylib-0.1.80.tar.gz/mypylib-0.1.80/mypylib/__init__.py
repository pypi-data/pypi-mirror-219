import datetime
import json
import math
import os
import queue
import re
import ssl
import threading
import time
from typing import Union

import requests

ssl._create_default_https_context = ssl._create_unverified_context
from termcolor import cprint
from inspect import currentframe



__info__ = {
    '2022/01/04: 0.1.18 加入 __info__。',
    '2022/01/04: 0.1.18 Carey修改 MVP的部分。',
    '2022/01/05: 0.1.19 add check_place_cover 預防漲停鎖住',
    '2022/01/06: 0.1.20 add get_stock_future_data(). 用來抓取每天股票期貨資料',
    '2022/01/06: 0.1.20 add get_stock_future_snapshot(). 用來抓每天股票、股票期貨漲停、跌停價格',
    '2022/01/11: 0.1.21 Add virtual function, check_place_cover() in ti class',
    '2022/02/10: 0.1.22 Add build_dealer_downloader()',
    '2022/02/14: 0.1.23 把 libexcel.py 搬到這邊來，以後可以全部沿用。',
    '2022/06/13: 0.1.24 加入 tplaysound ',
    '2022/06/24: 0.1.28 加入 tLineNotify',
    '2022/06/26: 0.1.29 加入 my_addressable_IP()',
    '2022/06/29: 0.1.30 加入需要的module',
    '2022/07/02: 0.1.32 加入 DefaultOrderedDict',
    '2022/07/13: 0.1.33 加入 binance_copy_bot',
    '2022/07/14: 0.1.34 加入 price_ticks_offset_dec() 要用 Decimal 避免float error',
    '2022/07/15: 0.1.35 binance_copy_bot() 改用 API方式',
    '2022/07/16: 0.1.36 加入 read_warrant_bible()',
    '2022/07/17: 0.1.37 加入 tredis'
    '2022/08/01: 0.1.39 加入註解，把一些東西拆開來，以免每次mypylib都要載入一堆 module',
    '2022/08/05: 0.1.40 繼續拆開一些東西 tredis',
    '2022/08/12: 0.1.41 Remove password and 加入 finmind',
    '2022/08/12: 0.1.42 fix redis 跳出問題',
    '2022/08/18: 0.1.43 修改 redis_msg_sender(), 增加 channel參數',
    '2022/08/19: 0.1.44 修改Tredis，改成兩個thread，避免任何block',
    '2022/08/30: 0.1.48 修改 get_all_stock_code_name_dict() 加入account',
    '2022/09/05: 0.1.49 tplaysound 如果沒有找到檔案不播放，不然會crash',
    '2022/09/06: 0.1.50 加入 crypto 模組',
    '2022/10/23: 0.1.51 get_all_stock_code_name_dict() 加入 _api 參數',
    '2022/10/25: 0.1.52 price_ticks_offset_AB_dec() 還有其他改成Decimal',
    '2022/10/30: 0.1.53 price_ticks_offsets_dec()',
    '2022/11/24: 0.1.54 修正一個 redis 非常奇怪的問題',
    '2022/11/27: 0.1.55 加入 shioaji_kline, KLine OHLC',
    '2022/12/22: 0.1.56 加入 get_new_warrant_list() and add_new_issued_warrant_to_bible()',
    '2023/01/03: 0.1.57 加入 get_taifex_weight_list()',
    '2023/01/05: 0.1.59 加入 Quote() Market()',
    '2023/01/07: 0.1.60 加入 Pause/TradeType/BestBuy/BestSell',
    '2023/01/12: 0.1.61 Remove redis debug message. Too annoying',
    '2023/01/29: 0.1.63 del xls in read_warrant_bible()',
    '2023/01/29: 0.1.64 add block for playsound class',
    '2023/02/12: 0.1.65 修改 sjtools parse timestamp的方法，以免crash',
    '2023/02/13: 0.1.66 Move toggle_btn_off and toggle_btn_on here ',
    '2023/02/23: 0.1.67 get_new_warrant_list() 元富修改網站，封鎖 read_html()',
    '2023/03/15: 0.1.68 修正一些宣告',
    '2023/04/11: 0.1.69 換成shioaji 1.0 API',
    '2023/04/18: 0.1.70 Market() 增加 ask bid information',
    '2023/04/27: 0.1.71 tplaysound 減少buffer音量以免很吵',
    '2023/05/10: 0.1.72 改用shioaji API',
    '2023/05/17: 0.1.73 shioaji 1.0 改 Mmvp.py & ti.py',
    '2023/05/22: 0.1.74 mvp() 不繼承 base class。因為shioaji升級的關係。先可以跑再說',
    '2023/06/01: 0.1.75 Apply Carey change',
    '2023/06/15: 0.1.76 Add crawler',
    '2023/06/19: 0.1.77 Not using stupid Redis connection pool',
    '2023/07/05: 0.1.78 cynes api v1 support',
    '2023/07/06: 0.1.79 news crawler little modification',
    '2023/07/12: 0.1.80 修改crawler'

}

__version__ = '0.1.80'

request_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

path_cronlog = 'cronlog'

toggle_btn_off = b'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'
toggle_btn_on = b'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'

from collections import OrderedDict
from collections.abc import Callable


class DefaultOrderedDict(OrderedDict):
    # Source: http://stackoverflow.com/a/6190500/562769
    def __init__(self, default_factory=None, *a, **kw):
        if (default_factory is not None and
                not isinstance(default_factory, Callable)):
            raise TypeError('first argument must be callable')
        OrderedDict.__init__(self, *a, **kw)
        self.default_factory = default_factory

    def __getitem__(self, key):
        try:
            return OrderedDict.__getitem__(self, key)
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        self[key] = value = self.default_factory()
        return value

    def __reduce__(self):
        if self.default_factory is None:
            args = tuple()
        else:
            args = self.default_factory,
        return type(self), args, None, None, self.items()

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        return type(self)(self.default_factory, self)

    def __deepcopy__(self, memo):
        import copy
        return type(self)(self.default_factory,
                          copy.deepcopy(self.items()))

    def __repr__(self):
        return 'OrderedDefaultDict(%s, %s)' % (self.default_factory,
                                               OrderedDict.__repr__(self))


import urllib.request


def my_addressable_IP():
    return urllib.request.urlopen('https://ident.me').read().decode('utf8')


def __LINE__():
    cf = currentframe()
    return cf.f_back.f_lineno


def get_all_stock_code_name_dict(_api=None):
    today = datetime.datetime.today()

    cache_file = f'all_stock_code-{today.strftime("%Y%m%d")}.json'

    if not os.path.isfile(cache_file):

        import shioaji as sj

        if _api is None:
            def login():
                api = sj.Shioaji()
                api.login(api_key='6Dkp67EVdMQBWE8Z6DZ5zPQAFTbvVPxEGzAEFiZ5ByhN',
                          secret_key='2NCQAhfP73PfKYaAi8xJVHZSp4Y91mSNViiFU7zQ19T2')
                return api

            api = login()
        else:
            api = _api

        all_code_name_dir = {}
        for x in api.Contracts.Stocks.OTC:
            if len(x.code) == 4:
                all_code_name_dir[x.code] = x.name

        for x in api.Contracts.Stocks.TSE:
            if len(x.code) == 4:
                all_code_name_dir[x.code] = x.name

        with open(cache_file, 'w') as fp:
            json.dump(all_code_name_dir, fp)
        api.logout()
    else:
        with open(cache_file, 'r') as fp:
            all_code_name_dir = json.load(fp)

    return all_code_name_dir


def get_day_trade_candidates(output_file_path='可當沖.json', days=0):
    import pandas as pd
    OTC_url_format = 'https://www.tpex.org.tw/web/stock/trading/' \
                     'intraday_trading/intraday_trading_list_print.php?' \
                     'l=zh-tw&d={}/{:02d}/{:02d}&stock_code=&s=0,asc,1'

    SEM_url_format = 'https://www.twse.com.tw/exchangeReport/' \
                     'TWTB4U?response=html&date={}{:02d}{:02d}&selectType=All'

    today = datetime.datetime.today() - datetime.timedelta(days=days)

    SEM_url = SEM_url_format.format(today.year, today.month, today.day)

    # print(SEM_url)

    ssl._create_default_https_context = ssl._create_unverified_context
    table = pd.read_html(SEM_url)
    df = table[0]
    df.columns = df.columns.droplevel()
    if '證券代號' not in df.columns:
        df = table[1]
        df.columns = df.columns.droplevel()
    df['證券代號'] = df['證券代號'].astype('str')
    mask = df['證券代號'].str.len() == 4
    df = df.loc[mask]
    df = df[['證券代號', '證券名稱', '暫停現股賣出後現款買進當沖註記']]
    df['暫停現股賣出後現款買進當沖註記'] = df['暫停現股賣出後現款買進當沖註記'].apply(lambda x: False if x == 'Y' else True)

    OCT_url = OTC_url_format.format(today.year - 1911, today.month, today.day)
    # print(OCT_url)

    ssl._create_default_https_context = ssl._create_unverified_context
    table = pd.read_html(OCT_url)

    df1 = table[0]
    df1.columns = df1.columns.droplevel()
    df1['證券代號'] = df1['證券代號'].astype('str')
    mask = df1['證券代號'].str.len() == 4
    df1 = df1.loc[mask]
    df1 = df1[['證券代號', '證券名稱', '暫停現股賣出後現款買進當沖註記']]
    df1['暫停現股賣出後現款買進當沖註記'] = df1['暫停現股賣出後現款買進當沖註記'].apply(lambda x: False if x == '＊' else True)

    all_df = pd.concat([df, df1])
    all_df.rename({'證券代號': 'symbol'}, axis=1, inplace=True)
    all_df.rename({'證券名稱': 'name'}, axis=1, inplace=True)
    all_df.rename({'暫停現股賣出後現款買進當沖註記': 'DayTrade'}, axis=1, inplace=True)
    all_df = all_df.set_index('name')
    ret = all_df.to_dict('index')
    all_df.to_csv(output_file_path)

    return ret


def get_top_future_trade_volume_list():
    url = 'https://deeptrade.pfcf.com.tw/stockf/volume30/volume?format=json'
    r = requests.get(url)
    data = json.loads(r.text)

    pattern = '^[0-9]*'

    top_future_rank = []

    for x in data:
        code = re.match(pattern, x[0])[0]
        name = re.sub(pattern, '', x[0])
        top_future_rank.append([code, name, x[1]])

    return top_future_rank


def get_stock_future_snapshot(filename='stock_future_snapshot.txt'):
    import shioaji as sj

    def login():
        api = sj.Shioaji()
        api.login(api_key='6Dkp67EVdMQBWE8Z6DZ5zPQAFTbvVPxEGzAEFiZ5ByhN',
                  secret_key='2NCQAhfP73PfKYaAi8xJVHZSp4Y91mSNViiFU7zQ19T2')
        return api

    api = login()

    contracts = []

    for x in api.Contracts.Futures:
        target = x[x._name + 'R1']
        if target is not None:
            if target.name[0] == '小':
                continue
            if len(target.underlying_code) > 4:
                continue
            if target.underlying_code != "":
                print(target.underlying_code, target.symbol[0:3], target.name)
                contracts.append(target)
                c = api.Contracts.Stocks[target.underlying_code]
                if c is not None:
                    contracts.append(c)

    with open(f'{path_cronlog}/{filename}', 'w+') as fp:
        fp.write(f'# {datetime.datetime.now()}\n')
        # 隔天早上八點半以後資料會更新
        c: sj.shioaji.Contract
        for c in contracts:
            fp.write(f'{c.code} {c.reference} {c.limit_up} {c.limit_down}\n')

    api.logout()


def get_stock_future_data(filename='stock_future_data.txt'):
    import pandas as pd
    if not os.path.isdir(path_cronlog):
        os.mkdir(path_cronlog)

    html_tables = pd.read_html('https://www.taifex.com.tw/cht/5/stockMargining')

    df_dict: dict = html_tables[0].to_dict('index')

    with open(f'{path_cronlog}/{filename}', 'w+') as fp:
        fp.write(f'# {datetime.datetime.now()}\n')

        for rec in df_dict.values():
            line = f'{rec["股票期貨標的證券代號"]} {rec["股票期貨英文代碼"]} {rec["股票期貨  中文簡稱"]} {rec["原始保證金適用比例"]}'
            print(line)
            fp.write(f'{line}\n')


def get_punishment_list():
    import pandas as pd
    if not os.path.isdir(path_cronlog):
        os.mkdir(path_cronlog)

    if os.path.isfile(f'{path_cronlog}/punishment-{datetime.datetime.today().strftime("%Y-%m-%d")}.txt'):
        p_code = []
        p_name = []
        with open(f'{path_cronlog}/punishment-{datetime.datetime.today().strftime("%Y-%m-%d")}.txt') as f:
            line: str
            for line in f.readlines():
                line = line.rstrip()
                code, name = line.split(' ')
                p_code.append(code)
                p_name.append(name)
    else:
        URL_TWSE = 'https://www.twse.com.tw/announcement/punish?response=html'
        TPEX_TWSE = 'https://www.tpex.org.tw/web/bulletin/disposal_information/disposal_information_print.php'

        ssl._create_default_https_context = ssl._create_unverified_context

        # print('讀取上市處置股資料')
        p1_code = pd.read_html(URL_TWSE)[0].astype('str')['證券代號'].values
        p1_name = pd.read_html(URL_TWSE)[0].astype('str')['證券名稱'].values
        # print('讀取上櫃處置股資料')
        p2_code = pd.read_html(TPEX_TWSE)[0]['證券代號'][0:-1].values
        p2_name = pd.read_html(TPEX_TWSE)[0]['證券名稱'][0:-1].values
        p_code = list(p1_code) + list(p2_code)
        p_name = list(p1_name) + list(p2_name)
        print(f'處置股資料 {p_code}')

        with open(f'{path_cronlog}/punishment-{datetime.datetime.today().strftime("%Y-%m-%d")}.txt', 'w') as f:
            for code, name in zip(p_code, p_name):
                f.write(f'{code} {name}\n')

    for code, name in zip(p_code, p_name):
        pass
        # print(code, name)
    return p_code, p_name


# 來源網頁: https://www.twse.com.tw/zh/page/trading/exchange/TWT92U.html
# 抓取資料: https://www.twse.com.tw/exchangeReport/TWT92U?date=20211008
def get_TSE_short_selling_list(date=datetime.datetime.today()):
    if not os.path.isdir(path_cronlog):
        os.mkdir(path_cronlog)
    path_cache = f'{path_cronlog}/TSE-short-selling_list-{date.strftime("%Y-%m-%d")}.txt'
    if os.path.isfile(path_cache):
        with open(path_cache) as fp:
            ret_dict = json.load(fp)
    else:
        url = f'https://www.twse.com.tw/exchangeReport/TWT92U?date={date.strftime("%Y%m%d")}'
        r = requests.get(url, headers=request_headers)
        ret = json.loads(r.text)
        ret_dict = {'list': [], 'stop short selling list': []}
        for x in ret['data']:
            ret_dict['list'].append(x[0])
            if x[2] == '*':
                ret_dict['stop short selling list'].append(x[0])
        with open(path_cache, 'w') as fp:
            json.dump(ret_dict, fp)
    return ret_dict


# 來源網頁: https://www.tpex.org.tw/web/stock/margin_trading/margin_mark/margin_mark.php?l=zh-tw
# 抓取資料: https://www.tpex.org.tw/web/stock/margin_trading/margin_mark/margin_mark_result.php?&d=110/09/08
def get_OTC_short_selling_list(date=datetime.datetime.today()):
    if not os.path.isdir(path_cronlog):
        os.mkdir(path_cronlog)
    path_cache = f'{path_cronlog}/OTC-short-selling_list-{date.strftime("%Y-%m-%d")}.txt'
    if os.path.isfile(path_cache):
        with open(path_cache) as fp:
            ret_dict = json.load(fp)
    else:
        url = f'https://www.tpex.org.tw/web/stock/margin_trading/margin_mark/margin_mark_result.php?&d={date.year - 1911}/{date.month:02d}/{date.day:02d}'
        r = requests.get(url, headers=request_headers)
        ret = json.loads(r.text)
        ret_dict = {'list': [], 'stop short selling list': []}
        for x in ret['aaData']:
            ret_dict['list'].append(x[0])
            if x[2] == '*':
                ret_dict['stop short selling list'].append(x[0])
        with open(path_cache, 'w') as fp:
            json.dump(ret_dict, fp)
    return ret_dict


def get_short_selling_list(date=datetime.datetime.today()):
    TSE_list = get_TSE_short_selling_list(date)
    OTC_list = get_OTC_short_selling_list(date)

    return {'list': TSE_list['list'] + OTC_list['list'], 'stop short selling list': TSE_list['stop short selling list'] + OTC_list['stop short selling list']}


def parse_date_time(date_string, time_string) -> datetime.datetime:
    if '.' in time_string:
        if '/' in date_string:
            timestamp = datetime.datetime.strptime(f'{date_string} {time_string}', '%Y/%m/%d %H:%M:%S.%f')
        else:
            timestamp = datetime.datetime.strptime(f'{date_string} {time_string}', '%Y-%m-%d %H:%M:%S.%f')
    else:
        if '/' in date_string:
            timestamp = datetime.datetime.strptime(f'{date_string} {time_string}', '%Y/%m/%d %H:%M:%S')
        else:
            timestamp = datetime.datetime.strptime(f'{date_string} {time_string}', '%Y-%m-%d %H:%M:%S')
    return timestamp


class timeIt:
    def __init__(self, prompt=''):
        self.start_time = datetime.datetime.now()
        self.end_time = datetime.datetime.now()
        self.prompt = prompt

    def __enter__(self):
        self.start_time = datetime.datetime.now()
        print(f'Start to {self.prompt}. {self.start_time}')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = datetime.datetime.now()
        print(f'It took {(self.end_time - self.start_time).seconds} seconds to finish {self.prompt}.')


########################
# Decimal
########################
from decimal import Decimal


def get_current_price_tick_dec(price: Union[Decimal, float, int], down=False):
    if isinstance(price, int) or isinstance(price, float):
        price = Decimal(str(price))
    # print(f'get_current_price_tick: {price}')
    if down:
        if price <= Decimal('10'):
            return Decimal('0.01')
        if 10 < price <= Decimal('50'):
            return Decimal('0.05')
        if 50 < price <= Decimal('100'):
            return Decimal('0.1')
        if 100 < price <= Decimal('500'):
            return Decimal('0.5')
        if 500 < price <= Decimal('1000'):
            return Decimal('1')
        if price > Decimal('1000'):
            return Decimal('5')
    else:
        if price < Decimal('10'):
            return Decimal('0.01')
        if 10 <= price < Decimal('50'):
            return Decimal('0.05')
        if 50 <= price < Decimal('100'):
            return Decimal('0.1')
        if 100 <= price < Decimal('500'):
            return Decimal('0.5')
        if 500 <= price < Decimal('1000'):
            return Decimal('1')
        if price >= Decimal('1000'):
            return Decimal('5')


# price1 should be .LE. to price2
def get_ticks_between_dec(_price1: Union[Decimal, float, int], _price2: Union[Decimal, float, int]):
    if isinstance(_price1, int) or isinstance(_price1, float):
        _price1 = Decimal(str(_price1))

    if isinstance(_price2, int) or isinstance(_price2, float):
        _price2 = Decimal(str(_price2))

    if _price2 < _price1:
        price1 = _price2
        price2 = _price1
    else:
        price1 = _price1
        price2 = _price2
    # print(price1, price2)
    ticks = 0
    while True:
        price1 += get_current_price_tick_dec(price1)
        # print(f'{ticks}: {price1} {price2}')
        if price1 > price2:
            break
        ticks += 1
    return ticks


def price_ticks_offsets_dec(price: Union[Decimal, float, int], ticks, bool_down=False):
    if isinstance(price, int) or isinstance(price, float):
        price = Decimal(str(price))
    list_prices = [price]
    for i in range(ticks):
        if bool_down:
            price -= get_current_price_tick_dec(price, down=bool_down)
        else:
            price += get_current_price_tick_dec(price, down=bool_down)
        list_prices.append(price)
    return list_prices




def price_ticks_offset_AB_dec(price: Union[Decimal, float, int], ticks):
    if isinstance(price, int) or isinstance(price, float):
        price = Decimal(str(price))
    list_ask = []
    list_bid = []
    price_ask = price
    price_bid = price
    for i in range(ticks):
        price_ask += get_current_price_tick_dec(price_ask, down=False)
        price_bid -= get_current_price_tick_dec(price_bid, down=True)
        list_ask.append(price_ask)
        list_bid.append(price_bid)
    return list_ask, list_bid



def price_ticks_offset_dec(price: Union[Decimal, float, int], ticks):
    if isinstance(price, int) or isinstance(price, float):
        price = Decimal(str(price))
    step = -1 if ticks < 0 else 1
    for i in range(0, ticks, step):
        price += step * get_current_price_tick_dec(price, down=True if step < 0 else False)
    return price


# TODO: 這個還有問題，並不是Decimal ，目前沒時間修 2022/10/23
def get_limit_up_and_down_price_dec(price):
    limit_up = price * 1.1
    tick = get_current_price_tick(limit_up)
    # By Carey
    # df['漲停價'] = round(df['漲停價'] - ((df['漲停價']+0.001) % df['tick_up']),2)
    limit_up = round(limit_up - (limit_up + 0.001) % tick, 2)

    limit_down = price * 0.9
    tick = get_current_price_tick(limit_down)
    limit_down = math.ceil(limit_down / tick)
    limit_down = limit_down * tick

    return round(limit_up, 3), round(limit_down, 3)


def price_stop_profit_and_lose_dec(price_enter, percentage_stop_profit, percentage_stop_lose, bool_call_or_put, tax=0.0015, fee=0.001425):
    if bool_call_or_put:
        price_stop_profit = price_ticks_offset(price_enter * (1 + percentage_stop_profit + fee * 2 + tax), 0)
        price_stop_lose = price_ticks_offset(price_enter * (1 + percentage_stop_lose + fee * 2 + tax), 0)
    else:
        price_stop_profit = price_ticks_offset(price_enter * (1 - percentage_stop_profit - fee * 2 - tax), 0)
        price_stop_lose = price_ticks_offset(price_enter * (1 - percentage_stop_lose - fee * 2 - tax), 0)

    return price_stop_profit, price_stop_lose


########################
# Obselete
########################

def get_current_price_tick(price, down=False):
    # print(f'get_current_price_tick: {price}')
    if down:
        if price <= 10:
            return 0.01
        if 10 < price <= 50:
            return 0.05
        if 50 < price <= 100:
            return 0.1
        if 100 < price <= 500:
            return 0.5
        if 500 < price <= 1000:
            return 1
        if price > 1000:
            return 5
    else:
        if price < 10:
            return 0.01
        if 10 <= price < 50:
            return 0.05
        if 50 <= price < 100:
            return 0.1
        if 100 <= price < 500:
            return 0.5
        if 500 <= price < 1000:
            return 1
        if price >= 1000:
            return 5


# price1 should be .LE. to price2
def get_ticks_between(_price1, _price2):
    if _price2 < _price1:
        price1 = _price2
        price2 = _price1
    else:
        price1 = _price1
        price2 = _price2

    ticks = 0
    while True:
        price1 += get_current_price_tick(price1)
        if price1 > price2:
            break
        ticks += 1
    return ticks


def price_ticks_offset(price, ticks):
    current_tick = get_current_price_tick(price)
    price = round(price - (price + 0.001) % current_tick, 2)
    # print(f'normalized price: {price}')
    if ticks == 0:
        return price
    step = 1 if ticks > 0 else -1
    for i in range(0, ticks, step):
        current_tick = get_current_price_tick(price, down=True if step == -1 else False)
        # print(i, price, current_tick)
        price += current_tick * step
    return round(price, 3)


def get_limit_up_and_down_price(price):
    limit_up = price * 1.1
    tick = get_current_price_tick(limit_up)
    # By Carey
    # df['漲停價'] = round(df['漲停價'] - ((df['漲停價']+0.001) % df['tick_up']),2)
    limit_up = round(limit_up - (limit_up + 0.001) % tick, 2)

    limit_down = price * 0.9
    tick = get_current_price_tick(limit_down)
    limit_down = math.ceil(limit_down / tick)
    limit_down = limit_down * tick

    return round(limit_up, 3), round(limit_down, 3)


def price_stop_profit_and_lose(price_enter, percentage_stop_profit, percentage_stop_lose, bool_call_or_put, tax=0.0015, fee=0.001425):
    if bool_call_or_put:
        price_stop_profit = price_ticks_offset(price_enter * (1 + percentage_stop_profit + fee * 2 + tax), 0)
        price_stop_lose = price_ticks_offset(price_enter * (1 + percentage_stop_lose + fee * 2 + tax), 0)
    else:
        price_stop_profit = price_ticks_offset(price_enter * (1 - percentage_stop_profit - fee * 2 - tax), 0)
        price_stop_lose = price_ticks_offset(price_enter * (1 - percentage_stop_lose - fee * 2 - tax), 0)

    return price_stop_profit, price_stop_lose


#
# Usage:
#   for day in date_range(datetime.datetime(year=2021, month=1, day=1), datetime.datetime(year=2021, month=10, day=1)):
#       print(day)
#
def date_range(start_date, end_date, bool_reverse=False):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


def mypylib_unit_test():
    cprint('抓取上市融券資料', 'yellow')
    print(get_TSE_short_selling_list())

    cprint('抓取上櫃融券資料', 'yellow')
    print(get_OTC_short_selling_list())

    cprint('抓取融券資料', 'yellow')
    print(get_short_selling_list())

    cprint('抓取處置股資料', 'yellow')
    print(get_punishment_list())

    cprint('抓取成交量前幾名的股票期貨名單', 'yellow')
    print(get_top_future_trade_volume_list())

    cprint('抓取可當沖資料', 'yellow')
    print(get_day_trade_candidates())


def short_selling_to_csv():
    import pandas as pd
    for day in date_range(datetime.datetime(year=2019, month=1, day=1), datetime.datetime.today()):
        print(day)
        TSE_path_cache = f'{path_cronlog}/TSE-short-selling_list-{day.strftime("%Y-%m-%d")}.txt'
        OTC_path_cache = f'{path_cronlog}/OTC-short-selling_list-{day.strftime("%Y-%m-%d")}.txt'

        if os.path.isfile(TSE_path_cache) and os.path.isfile(OTC_path_cache):
            with open(TSE_path_cache) as fp:
                TSE_list = json.load(fp)
            with open(OTC_path_cache) as fp:
                OTC_list = json.load(fp)

            all = {'list': TSE_list['list'] + OTC_list['list'], 'stop short selling list': TSE_list['stop short selling list'] + OTC_list['stop short selling list']}

            if len(all['list']) < 100:
                continue

            data = {}

            for symbol in all['list']:
                data[symbol] = [1, 0]

            for symbol in all['stop short selling list']:
                data[symbol][1] = 1

            # df = pd.DataFrame.from_dict(data, orient='index', columns=['list', 'stop short selling list'])
            # print(df)
            # df.to_csv(f'csv/list-{day.strftime("%Y-%m-%d")}.csv')

            with open(f'json/list-{day.strftime("%Y-%m-%d")}.json', 'w') as fp:
                json.dump(data, fp)


def get_future_ex(date: datetime.datetime, next_month=False):
    end_of_contract_day = 21 - (date.replace(day=1).weekday() + 2) % 7;
    letter = chr(ord('A') - (0 if next_month else 1) + date.month + (1 if end_of_contract_day < date.day else 0))

    return f'{"A" if letter == "M" else letter}{(date.year + (1 if letter == "M" else 0)) % 10}'


def is_end_of_contract_day(date: datetime.datetime):
    end_of_contract_day = 21 - (date.replace(day=1).weekday() + 4) % 7
    # print(f'end of contrract day: {end_of_contract_day}')
    return True if date.day == end_of_contract_day else False


def load_all_shioaji_ticks(source_dir='../../shioaji_ticks'):
    all_files = []

    for d in os.listdir(source_dir):
        if not os.path.isdir(f'{source_dir}/{d}'):
            continue
        if d == 'cache':
            continue
        for f in os.listdir(f'{source_dir}/{d}'):
            if not f.startswith('20'):
                continue
            full_path = f'{source_dir}/{d}/{f}'
            all_files.append([full_path, d, f.split('.')[0]])
    return all_files


def build_dealer_downloader(date=datetime.datetime(year=2020, month=1, day=1), target_directory='自營商歷史資料'):
    if not os.path.isdir(target_directory):
        os.mkdir(target_directory)

    day_delta = datetime.timedelta(days=1)
    while date < datetime.datetime.now():
        print(date)

        # time.sleep(30)

        date = date + day_delta

        #
        # 上櫃
        #
        otc_dealer_buy_csv_path = f'{target_directory}/{date.year}{date.month:02d}{date.day:02d}_OTC_buy.csv'
        otc_dealer_sell_csv_path = f'{target_directory}/{date.year}{date.month:02d}{date.day:02d}_OTC_sell.csv'
        if os.path.isfile(otc_dealer_buy_csv_path) is False:
            url = f"https://www.tpex.org.tw/web/stock/3insti/dealer_trading/dealtr_hedge_result.php?l=zh-tw&t=D&type=buy&d={date.year - 1911}/{date.month:02d}/{date.day:02d}"
            print(url)

            r = requests.get(url, headers=request_headers)
            jdata = json.loads(r.content)

            if len(jdata['aaData']) == 0:
                continue

            with open(otc_dealer_buy_csv_path, 'w') as f:
                f.write('\ufeff')
                f.write(',,,(自行買賣),(自行買賣),(自行買賣),(避險),(避險),(避險),買賣超\n')
                f.write(',,,買進,賣出,買賣超,買進,賣出,買賣超,(仟股)\n')
                f.write(',,,,,(仟股),,,(仟股),,\n')
                # print(jdata)

                for x in jdata['aaData']:
                    # print(x)
                    string = '\t'.join(x)
                    string = string.replace(',', '')
                    string = string.replace('\t', ',')
                    f.write(string + '\n')

        if os.path.isfile(otc_dealer_sell_csv_path) is False:
            url = f"https://www.tpex.org.tw/web/stock/3insti/dealer_trading/dealtr_hedge_result.php?l=zh-tw&t=D&type=sell&d={date.year - 1911}/{date.month:02d}/{date.day:02d}"
            print(url)

            r = requests.get(url, headers=request_headers)
            jdata = json.loads(r.content)
            with open(otc_dealer_sell_csv_path, 'w') as f:
                f.write('\ufeff')
                f.write(',,,(自行買賣),(自行買賣),(自行買賣),(避險),(避險),(避險),買賣超\n')
                f.write(',,,買進,賣出,買賣超,買進,賣出,買賣超,(仟股)\n')
                f.write(',,,,,(仟股),,,(仟股),,\n')

                for x in jdata['aaData']:
                    # print(x)
                    string = '\t'.join(x)
                    string = string.replace(',', '')
                    string = string.replace('\t', ',')
                    f.write(string + '\n')

        #
        # 上市
        #
        dealer_csv_path = f'{target_directory}/{date.year}{date.month:02d}{date.day:02d}.csv'
        if os.path.isfile(dealer_csv_path) is False:
            url = f'https://www.twse.com.tw/fund/TWT43U?response=csv&date={date.year}{date.month:02d}{date.day:02d}'
            print(url)

            r = requests.get(url, headers=request_headers)
            with open(dealer_csv_path + '_', 'wb') as f:
                f.write(r.content)

            with open(dealer_csv_path, 'w') as f:
                f.write('\ufeff')

            time.sleep(10)

            os.system(f'/usr/bin/iconv -f BIG5-2003 -t UTF-8 {dealer_csv_path}_ >> {dealer_csv_path}')
            os.unlink(dealer_csv_path + '_')


def get_trade_days(date_start: Union[str, datetime.datetime] = '2018-01-01',
                   date_end: Union[str, datetime.datetime] = '2022-07-31') -> list:
    date_start = date_start if isinstance(date_start, str) else date_start.strftime('%Y-%m-%d')
    date_end = date_end if isinstance(date_end, str) else date_end.strftime('%Y-%m-%d')

    file_cache = f'trade_days_{date_start}_{date_end}.txt'

    if os.path.isfile(file_cache):
        with open(file_cache) as fp:
            return json.load(fp)

    from FinMind.data import DataLoader
    # print(date_start, date_end)

    dl = DataLoader()
    stock_data = dl.taiwan_stock_daily(stock_id='2330', start_date=date_start, end_date=date_end)
    days = stock_data['date']
    # print(days)
    list_days = []
    for x in days:
        list_days.append(x)

    with open(file_cache, 'w+') as fp:
        json.dump(list_days, fp)

    return list_days


# [
#   {'symbol': 2330, 'weight': Decimal('0.26513')},
#   {'symbol': 2464.0, 'weight': Decimal('0.000169')},
#   {'symbol': 2317, 'weight': Decimal('0.031573')},
#
def get_taifex_weight_list(filename=None):
    import pandas as pd
    from decimal import Decimal
    df = pd.read_html('https://www.taifex.com.tw/cht/9/futuresQADetail')
    list_weight = []
    try:
        for x in df[0].to_dict('index').values():
            list_weight.append({'symbol': str(x['證券名稱']).split(".")[0], 'weight': Decimal(x['市值佔 大盤比重'][:-1])/100})
            list_weight.append({'symbol': str(x['證券名稱.2']).split(".")[0], 'weight': Decimal(x['市值佔 大盤比重.1'][:-1])/100})
    except Exception as e:
        pass

    if filename is not None:
        with open(filename, 'w+') as fp:
            for x in list_weight:
                fp.write(f'{x["symbol"]} {str(x["weight"])}\n')

    return list_weight







if __name__ == '__main__':
    from time import sleep

    if True:
        print(get_taifex_weight_list("taifex_weight.txt"))

    if True:
        print(price_ticks_offsets_dec(99, 6))
        print(price_ticks_offsets_dec(99, 6, True))

    if False:
        print(100.5, 1, price_ticks_offset_dec(100.5, 1))
        print(100.5, -1, price_ticks_offset_dec(100.5, -1))
        print(100, 1, price_ticks_offset_dec(100, 1))
        print(100, -1, price_ticks_offset_dec(100, -1))
        print(99.9, 1, price_ticks_offset_dec(99.9, 1))
        print(99.9, -1, price_ticks_offset_dec(99.9, -1))

        print(50.1, 1, price_ticks_offset_dec(50.1, 1))
        print(50.1, -1, price_ticks_offset_dec(50.1, -1))
        print(50, 1, price_ticks_offset_dec(50, 1))
        print(50, -1, price_ticks_offset_dec(50, -1))
        print(49.5, 1, price_ticks_offset_dec(49.5, 1))
        print(49.5, -1, price_ticks_offset_dec(49.5, -1))

        print(100, 6, price_ticks_offset_AB_dec(100, 6))
        print(99.8, 6, price_ticks_offset_AB_dec(99.8, 6))
        print(101.5, 6, price_ticks_offset_AB_dec(101.5, 6))
        print(50.2, 6, price_ticks_offset_AB_dec(50.2, 6))
        print(50, 6, price_ticks_offset_AB_dec(50, 6))
        print(49.9, 6, price_ticks_offset_AB_dec(49.9, 6))

    if True:
        print(get_all_stock_code_name_dict())

    if False:
        ret = get_trade_days()
        print(ret)

        exit(0)

    if False:
        build_dealer_downloader()

    if False:
        all = load_all_shioaji_ticks()
        print(f'There are {len(all)} files')

        get_stock_future_snapshot()
        get_stock_future_data()

        print(get_future_ex(datetime.datetime(year=2021, month=12, day=1)))
        print(get_future_ex(datetime.datetime(year=2021, month=12, day=15)))
        print(get_future_ex(datetime.datetime(year=2021, month=12, day=30)))
        print(is_end_of_contract_day(datetime.datetime(year=2021, month=12, day=1)))
        print(is_end_of_contract_day(datetime.datetime(year=2021, month=12, day=14)))
        print(is_end_of_contract_day(datetime.datetime(year=2021, month=12, day=15)))
        print(is_end_of_contract_day(datetime.datetime(year=2021, month=12, day=16)))
        print(get_future_ex(datetime.datetime(year=2021, month=12, day=15), next_month=is_end_of_contract_day(datetime.datetime(year=2021, month=12, day=15))))

        print(get_ticks_between(100, 100))

        mypylib_unit_test()

    if False:
        for day in date_range(datetime.datetime(year=2019, month=1, day=1), datetime.datetime.today()):
            print(day)
            TSE_path_cache = f'{path_cronlog}/TSE-short-selling_list-{day.strftime("%Y-%m-%d")}.txt'
            OTC_path_cache = f'{path_cronlog}/OTC-short-selling_list-{day.strftime("%Y-%m-%d")}.txt'
            if not os.path.isfile(TSE_path_cache) and not os.path.isfile(OTC_path_cache):
                get_short_selling_list(day)
                sleep(5)

        short_selling_to_csv()

        print(__LINE__())
