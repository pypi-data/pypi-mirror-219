# encoding:utf-8

# 微信公众号：AlgoPlus
# 官网：http://algo.plus
# 项目地址：https://gitee.com/AlgoPlus/

import os, copy, csv
from AlgoPlus.CTP.MdApiBase import MdApiBase
from AlgoPlus.CTP.FutureAccount import FutureAccount
from AlgoPlus.CTP.ApiStruct import DepthMarketDataField
from AlgoPlus.ta.time_bar import tick_to_bar
from AlgoPlus.utils.base_field import to_str, to_bytes


class TickEngine(MdApiBase):
    def __init__(self, broker_id, md_server, subscribe_list, md_queue_list=None, investor_id=b'', password=b'', flow_path='', using_udp=False, multicast=False):
        pass


class BarEngine(MdApiBase):
    def __init__(self, broker_id, md_server, subscribe_list, md_queue_list=None, investor_id=b'', password=b'', flow_path='', using_udp=False, multicast=False):
        pass

    def init_extra(self):
        # Bar字段
        bar_cache = {
            "InstrumentID": b"",
            "UpdateTime": b"99:99:99",
            "LastPrice": 0.0,
            "HighPrice": 0.0,
            "LowPrice": 0.0,
            "OpenPrice": 0.0,
            "BarVolume": 0,
            "BarTurnover": 0.0,
            "BarSettlement": 0.0,
            "BVolume": 0,
            "SVolume": 0,
            "FVolume": 0,
            "DayVolume": 0,
            "DayTurnover": 0.0,
            "DaySettlement": 0.0,
            "OpenInterest": 0.0,
            "TradingDay": b"99999999",
        }

        self.bar_dict = {}  # Bar字典容器
        # 遍历订阅列表
        for instrument_id in self.subscribe_list:
            # 将str转为byte
            if not isinstance(instrument_id, bytes):
                instrument_id = to_bytes(instrument_id.encode('utf-8'))

            # 初始化Bar字段
            bar_cache["InstrumentID"] = instrument_id
            self.bar_dict[instrument_id] = bar_cache.copy()

    # ///深度行情通知
    def OnRtnDepthMarketData(self, pDepthMarketData):
        bar_data = self.bar_dict[pDepthMarketData['InstrumentID']]
        last_update_time = bar_data["UpdateTime"]
        is_new_1minute = (pDepthMarketData['UpdateTime'][:-2] != last_update_time[:-2]) and pDepthMarketData['UpdateTime'] != b'21:00:00'  # 1分钟K线条件
        # is_new_5minute = is_new_1minute and int(pDepthMarketData['UpdateTime'][-4]) % 5 == 0  # 5分钟K线条件
        # is_new_10minute = is_new_1minute and pDepthMarketData['UpdateTime'][-4] == b"0"  # 10分钟K线条件
        # is_new_10minute = is_new_1minute and int(pDepthMarketData['UpdateTime'][-5:-3]) % 15 == 0  # 15分钟K线条件
        # is_new_30minute = is_new_1minute and int(pDepthMarketData['UpdateTime'][-5:-3]) % 30 == 0  # 30分钟K线条件
        # is_new_hour = is_new_1minute and int(pDepthMarketData['UpdateTime'][-5:-3]) % 60 == 0  # 60分钟K线条件

        # # 新K线开始
        if is_new_1minute and last_update_time != b"99:99:99":
            for md_queue in self.md_queue_list:
                md_queue.put(copy.deepcopy(bar_data))

        # 将Tick池化为Bar
        tick_to_bar(bar_data, pDepthMarketData, is_new_1minute)


class MdRecorder(MdApiBase):
    def __init__(self, broker_id, md_server, subscribe_list, md_queue_list=None, investor_id=b'', password=b'', flow_path='', using_udp=False, multicast=False):
        pass

    def init_csv_files(self):
        self.csv_file_dict = {}
        self.csv_writer = {}
        # 深度行情结构体字段名列表
        header = list(DepthMarketDataField().to_dict())
        for instrument_id in self.subscribe_list:
            instrument_id = to_str(instrument_id)
            # file object
            file_dir = os.path.join(self.flow_path, f'{instrument_id}-{self.GetTradingDay()}.csv')
            self.csv_file_dict[instrument_id] = open(file_dir, 'a', newline='')
            # writer object
            self.csv_writer[instrument_id] = csv.DictWriter(self.csv_file_dict[instrument_id], header)
            # 写入表头
            self.csv_writer[instrument_id].writeheader()
            self.csv_file_dict[instrument_id].flush()

    def OnRspUserLogin(self, pRspUserLogin, pRspInfo, nRequestID, bIsLast):
        self.write_log('OnRspUserLogin', pRspInfo, f'RequestID:{nRequestID}', f'IsLast:{bIsLast}', pRspUserLogin)

        if bIsLast and (not pRspInfo or pRspInfo['ErrorID'] == 0):
            self.init_csv_files()

            error_id = 0
            if self.subscribe_list:
                error_id = self.SubscribeMarketData(self.subscribe_list)
                if error_id != 0:
                    self.write_log('SubscribeMarketData', {'ErrorID': error_id, 'ErrorMsg': 'Error:Fail to SubscribeMarketData.'}, self.subscribe_list)

            if error_id == 0:
                self.status = 0
                self.write_log('Md Ready!', f'CTP Md API Version:{MdApiBase.GetApiVersion(self)}', f'TradingDay:{self.GetTradingDay()}',
                               f'broker_id:{self.broker_id}', f'server:{self.md_server}', f'subscribe_list:{self.subscribe_list}')

    # ///深度行情通知
    def OnRtnDepthMarketData(self, pDepthMarketData):
        for key in pDepthMarketData.keys():
            pDepthMarketData[key] = to_str(pDepthMarketData[key])
        # 写入行情
        self.csv_writer[pDepthMarketData['InstrumentID']].writerow(pDepthMarketData)
        self.csv_file_dict[pDepthMarketData['InstrumentID']].flush()


def run_api(api_cls, account, md_queue_list=None):
    if isinstance(account, FutureAccount):
        tick_engine = api_cls(
            account.broker_id,
            account.server_dict['MDServer'],
            account.subscribe_list,
            md_queue_list,
            account.investor_id,
            account.password,
            account.md_flow_path
        )
        tick_engine.Join()


def run_tick_engine(account, md_queue_list):
    run_api(TickEngine, account, md_queue_list)


def run_bar_engine(account, md_queue_list):
    run_api(BarEngine, account, md_queue_list)


def run_mdrecorder(account):
    run_api(MdRecorder, account, None)
