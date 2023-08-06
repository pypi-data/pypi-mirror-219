# encoding:utf-8

# 微信公众号：AlgoPlus
# 官网：http://algo.plus
# 项目地址：https://gitee.com/AlgoPlus/

import ctypes
from ..utils.base_field import BaseField


class LocalInputOrderField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # 交易所代码
        ('InstrumentID', ctypes.c_char * 31),  # 合约代码
        ('OrderRef', ctypes.c_char * 13),  # 报单引用
        ('Direction', ctypes.c_char * 1),  # 买卖方向
        ('OffsetFlag', ctypes.c_char * 5),  # 组合开平标志
        ('LimitPrice', ctypes.c_double),  # 报单价格
        ('VolumeTotalOriginal', ctypes.c_int),  # 数量
        ('VolumeTotal', ctypes.c_int),  # 剩余数量
        ('OrderStatus', ctypes.c_char * 1),  # 报单状态
        ('InputTime', ctypes.c_float),  # 委托时间
    ]


# ///信息分发
class DisseminationField(BaseField):
    _fields_ = [
        ('SequenceSeries', ctypes.c_short),  # ///序列系列号
        ('SequenceNo', ctypes.c_int),  # ///序列号
    ]


# ///用户登录请求
class ReqUserLoginField(BaseField):
    _fields_ = [
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('Password', ctypes.c_char * 41),  # ///密码
        ('UserProductInfo', ctypes.c_char * 11),  # ///用户端产品信息
        ('InterfaceProductInfo', ctypes.c_char * 11),  # ///接口端产品信息
        ('ProtocolInfo', ctypes.c_char * 11),  # ///协议信息
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('OneTimePassword', ctypes.c_char * 41),  # ///动态密码
        ('reserve1', ctypes.c_char * 16),  # ///保留的无效字段
        ('LoginRemark', ctypes.c_char * 36),  # ///登录备注
        ('ClientIPPort', ctypes.c_int),  # ///终端IP端口
        ('ClientIPAddress', ctypes.c_char * 33),  # ///终端IP地址
    ]


# ///用户登录应答
class RspUserLoginField(BaseField):
    _fields_ = [
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('LoginTime', ctypes.c_char * 9),  # ///登录成功时间
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('SystemName', ctypes.c_char * 41),  # ///交易系统名称
        ('FrontID', ctypes.c_int),  # ///前置编号
        ('SessionID', ctypes.c_int),  # ///会话编号
        ('MaxOrderRef', ctypes.c_char * 13),  # ///最大报单引用
        ('SHFETime', ctypes.c_char * 9),  # ///上期所时间
        ('DCETime', ctypes.c_char * 9),  # ///大商所时间
        ('CZCETime', ctypes.c_char * 9),  # ///郑商所时间
        ('FFEXTime', ctypes.c_char * 9),  # ///中金所时间
        ('INETime', ctypes.c_char * 9),  # ///能源中心时间
        ('SysVersion', ctypes.c_char * 41),  # ///后台版本信息
        ('GFEXTime', ctypes.c_char * 9),  # ///广期所时间
    ]


# ///用户登出请求
class UserLogoutField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
    ]


# ///强制交易员退出
class ForceUserLogoutField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
    ]


# ///客户端认证请求
class ReqAuthenticateField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('UserProductInfo', ctypes.c_char * 11),  # ///用户端产品信息
        ('AuthCode', ctypes.c_char * 17),  # ///认证码
        ('AppID', ctypes.c_char * 33),  # ///App代码
    ]


# ///客户端认证响应
class RspAuthenticateField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('UserProductInfo', ctypes.c_char * 11),  # ///用户端产品信息
        ('AppID', ctypes.c_char * 33),  # ///App代码
        ('AppType', ctypes.c_char * 1),  # ///App类型
    ]


# ///客户端认证信息
class AuthenticationInfoField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('UserProductInfo', ctypes.c_char * 11),  # ///用户端产品信息
        ('AuthInfo', ctypes.c_char * 129),  # ///认证信息
        ('IsResult', ctypes.c_int),  # ///是否为认证结果
        ('AppID', ctypes.c_char * 33),  # ///App代码
        ('AppType', ctypes.c_char * 1),  # ///App类型
        ('reserve1', ctypes.c_char * 16),  # ///保留的无效字段
        ('ClientIPAddress', ctypes.c_char * 33),  # ///终端IP地址
    ]


# ///用户登录应答2
class RspUserLogin2Field(BaseField):
    _fields_ = [
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('LoginTime', ctypes.c_char * 9),  # ///登录成功时间
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('SystemName', ctypes.c_char * 41),  # ///交易系统名称
        ('FrontID', ctypes.c_int),  # ///前置编号
        ('SessionID', ctypes.c_int),  # ///会话编号
        ('MaxOrderRef', ctypes.c_char * 13),  # ///最大报单引用
        ('SHFETime', ctypes.c_char * 9),  # ///上期所时间
        ('DCETime', ctypes.c_char * 9),  # ///大商所时间
        ('CZCETime', ctypes.c_char * 9),  # ///郑商所时间
        ('FFEXTime', ctypes.c_char * 9),  # ///中金所时间
        ('INETime', ctypes.c_char * 9),  # ///能源中心时间
        ('RandomString', ctypes.c_char * 17),  # ///随机串
    ]


# ///银期转帐报文头
class TransferHeaderField(BaseField):
    _fields_ = [
        ('Version', ctypes.c_char * 4),  # ///版本号，常量，1.0
        ('TradeCode', ctypes.c_char * 7),  # ///交易代码，必填
        ('TradeDate', ctypes.c_char * 9),  # ///交易日期，必填，格式：yyyymmdd
        ('TradeTime', ctypes.c_char * 9),  # ///交易时间，必填，格式：hhmmss
        ('TradeSerial', ctypes.c_char * 9),  # ///发起方流水号，N/A
        ('FutureID', ctypes.c_char * 11),  # ///期货公司代码，必填
        ('BankID', ctypes.c_char * 4),  # ///银行代码，根据查询银行得到，必填
        ('BankBrchID', ctypes.c_char * 5),  # ///银行分中心代码，根据查询银行得到，必填
        ('OperNo', ctypes.c_char * 17),  # ///操作员，N/A
        ('DeviceID', ctypes.c_char * 3),  # ///交易设备类型，N/A
        ('RecordNum', ctypes.c_char * 7),  # ///记录数，N/A
        ('SessionID', ctypes.c_int),  # ///会话编号，N/A
        ('RequestID', ctypes.c_int),  # ///请求编号，N/A
    ]


# ///银行资金转期货请求，TradeCode=202001
class TransferBankToFutureReqField(BaseField):
    _fields_ = [
        ('FutureAccount', ctypes.c_char * 13),  # ///期货资金账户
        ('FuturePwdFlag', ctypes.c_char * 1),  # ///密码标志
        ('FutureAccPwd', ctypes.c_char * 17),  # ///密码
        ('TradeAmt', ctypes.c_double),  # ///转账金额
        ('CustFee', ctypes.c_double),  # ///客户手续费
        ('CurrencyCode', ctypes.c_char * 4),  # ///币种：RMB-人民币 USD-美圆 HKD-港元
    ]


# ///银行资金转期货请求响应
class TransferBankToFutureRspField(BaseField):
    _fields_ = [
        ('RetCode', ctypes.c_char * 5),  # ///响应代码
        ('RetInfo', ctypes.c_char * 129),  # ///响应信息
        ('FutureAccount', ctypes.c_char * 13),  # ///资金账户
        ('TradeAmt', ctypes.c_double),  # ///转帐金额
        ('CustFee', ctypes.c_double),  # ///应收客户手续费
        ('CurrencyCode', ctypes.c_char * 4),  # ///币种
    ]


# ///期货资金转银行请求，TradeCode=202002
class TransferFutureToBankReqField(BaseField):
    _fields_ = [
        ('FutureAccount', ctypes.c_char * 13),  # ///期货资金账户
        ('FuturePwdFlag', ctypes.c_char * 1),  # ///密码标志
        ('FutureAccPwd', ctypes.c_char * 17),  # ///密码
        ('TradeAmt', ctypes.c_double),  # ///转账金额
        ('CustFee', ctypes.c_double),  # ///客户手续费
        ('CurrencyCode', ctypes.c_char * 4),  # ///币种：RMB-人民币 USD-美圆 HKD-港元
    ]


# ///期货资金转银行请求响应
class TransferFutureToBankRspField(BaseField):
    _fields_ = [
        ('RetCode', ctypes.c_char * 5),  # ///响应代码
        ('RetInfo', ctypes.c_char * 129),  # ///响应信息
        ('FutureAccount', ctypes.c_char * 13),  # ///资金账户
        ('TradeAmt', ctypes.c_double),  # ///转帐金额
        ('CustFee', ctypes.c_double),  # ///应收客户手续费
        ('CurrencyCode', ctypes.c_char * 4),  # ///币种
    ]


# ///查询银行资金请求，TradeCode=204002
class TransferQryBankReqField(BaseField):
    _fields_ = [
        ('FutureAccount', ctypes.c_char * 13),  # ///期货资金账户
        ('FuturePwdFlag', ctypes.c_char * 1),  # ///密码标志
        ('FutureAccPwd', ctypes.c_char * 17),  # ///密码
        ('CurrencyCode', ctypes.c_char * 4),  # ///币种：RMB-人民币 USD-美圆 HKD-港元
    ]


# ///查询银行资金请求响应
class TransferQryBankRspField(BaseField):
    _fields_ = [
        ('RetCode', ctypes.c_char * 5),  # ///响应代码
        ('RetInfo', ctypes.c_char * 129),  # ///响应信息
        ('FutureAccount', ctypes.c_char * 13),  # ///资金账户
        ('TradeAmt', ctypes.c_double),  # ///银行余额
        ('UseAmt', ctypes.c_double),  # ///银行可用余额
        ('FetchAmt', ctypes.c_double),  # ///银行可取余额
        ('CurrencyCode', ctypes.c_char * 4),  # ///币种
    ]


# ///查询银行交易明细请求，TradeCode=204999
class TransferQryDetailReqField(BaseField):
    _fields_ = [
        ('FutureAccount', ctypes.c_char * 13),  # ///期货资金账户
    ]


# ///查询银行交易明细请求响应
class TransferQryDetailRspField(BaseField):
    _fields_ = [
        ('TradeDate', ctypes.c_char * 9),  # ///交易日期
        ('TradeTime', ctypes.c_char * 9),  # ///交易时间
        ('TradeCode', ctypes.c_char * 7),  # ///交易代码
        ('FutureSerial', ctypes.c_int),  # ///期货流水号
        ('FutureID', ctypes.c_char * 11),  # ///期货公司代码
        ('FutureAccount', ctypes.c_char * 22),  # ///资金帐号
        ('BankSerial', ctypes.c_int),  # ///银行流水号
        ('BankID', ctypes.c_char * 4),  # ///银行代码
        ('BankBrchID', ctypes.c_char * 5),  # ///银行分中心代码
        ('BankAccount', ctypes.c_char * 41),  # ///银行账号
        ('CertCode', ctypes.c_char * 21),  # ///证件号码
        ('CurrencyCode', ctypes.c_char * 4),  # ///货币代码
        ('TxAmount', ctypes.c_double),  # ///发生金额
        ('Flag', ctypes.c_char * 1),  # ///有效标志
    ]


# ///响应信息
class RspInfoField(BaseField):
    _fields_ = [
        ('ErrorID', ctypes.c_int),  # ///错误代码
        ('ErrorMsg', ctypes.c_char * 81),  # ///错误信息
    ]


# ///交易所
class ExchangeField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ExchangeName', ctypes.c_char * 61),  # ///交易所名称
        ('ExchangeProperty', ctypes.c_char * 1),  # ///交易所属性
    ]


# ///产品
class ProductField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ProductName', ctypes.c_char * 21),  # ///产品名称
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ProductClass', ctypes.c_char * 1),  # ///产品类型
        ('VolumeMultiple', ctypes.c_int),  # ///合约数量乘数
        ('PriceTick', ctypes.c_double),  # ///最小变动价位
        ('MaxMarketOrderVolume', ctypes.c_int),  # ///市价单最大下单量
        ('MinMarketOrderVolume', ctypes.c_int),  # ///市价单最小下单量
        ('MaxLimitOrderVolume', ctypes.c_int),  # ///限价单最大下单量
        ('MinLimitOrderVolume', ctypes.c_int),  # ///限价单最小下单量
        ('PositionType', ctypes.c_char * 1),  # ///持仓类型
        ('PositionDateType', ctypes.c_char * 1),  # ///持仓日期类型
        ('CloseDealType', ctypes.c_char * 1),  # ///平仓处理类型
        ('TradeCurrencyID', ctypes.c_char * 4),  # ///交易币种类型
        ('MortgageFundUseRange', ctypes.c_char * 1),  # ///质押资金可用范围
        ('reserve2', ctypes.c_char * 31),  # ///保留的无效字段
        ('UnderlyingMultiple', ctypes.c_double),  # ///合约基础商品乘数
        ('ProductID', ctypes.c_char * 81),  # ///产品代码
        ('ExchangeProductID', ctypes.c_char * 81),  # ///交易所产品代码
        ('OpenLimitControlLevel', ctypes.c_char * 1),  # ///开仓量限制粒度
        ('OrderFreqControlLevel', ctypes.c_char * 1),  # ///报单频率控制粒度
    ]


# ///合约
class InstrumentField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InstrumentName', ctypes.c_char * 21),  # ///合约名称
        ('reserve2', ctypes.c_char * 31),  # ///保留的无效字段
        ('reserve3', ctypes.c_char * 31),  # ///保留的无效字段
        ('ProductClass', ctypes.c_char * 1),  # ///产品类型
        ('DeliveryYear', ctypes.c_int),  # ///交割年份
        ('DeliveryMonth', ctypes.c_int),  # ///交割月
        ('MaxMarketOrderVolume', ctypes.c_int),  # ///市价单最大下单量
        ('MinMarketOrderVolume', ctypes.c_int),  # ///市价单最小下单量
        ('MaxLimitOrderVolume', ctypes.c_int),  # ///限价单最大下单量
        ('MinLimitOrderVolume', ctypes.c_int),  # ///限价单最小下单量
        ('VolumeMultiple', ctypes.c_int),  # ///合约数量乘数
        ('PriceTick', ctypes.c_double),  # ///最小变动价位
        ('CreateDate', ctypes.c_char * 9),  # ///创建日
        ('OpenDate', ctypes.c_char * 9),  # ///上市日
        ('ExpireDate', ctypes.c_char * 9),  # ///到期日
        ('StartDelivDate', ctypes.c_char * 9),  # ///开始交割日
        ('EndDelivDate', ctypes.c_char * 9),  # ///结束交割日
        ('InstLifePhase', ctypes.c_char * 1),  # ///合约生命周期状态
        ('IsTrading', ctypes.c_int),  # ///当前是否交易
        ('PositionType', ctypes.c_char * 1),  # ///持仓类型
        ('PositionDateType', ctypes.c_char * 1),  # ///持仓日期类型
        ('LongMarginRatio', ctypes.c_double),  # ///多头保证金率
        ('ShortMarginRatio', ctypes.c_double),  # ///空头保证金率
        ('MaxMarginSideAlgorithm', ctypes.c_char * 1),  # ///是否使用大额单边保证金算法
        ('reserve4', ctypes.c_char * 31),  # ///保留的无效字段
        ('StrikePrice', ctypes.c_double),  # ///执行价
        ('OptionsType', ctypes.c_char * 1),  # ///期权类型
        ('UnderlyingMultiple', ctypes.c_double),  # ///合约基础商品乘数
        ('CombinationType', ctypes.c_char * 1),  # ///组合类型
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('ExchangeInstID', ctypes.c_char * 81),  # ///合约在交易所的代码
        ('ProductID', ctypes.c_char * 81),  # ///产品代码
        ('UnderlyingInstrID', ctypes.c_char * 81),  # ///基础商品代码
    ]


# ///经纪公司
class BrokerField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('BrokerAbbr', ctypes.c_char * 9),  # ///经纪公司简称
        ('BrokerName', ctypes.c_char * 81),  # ///经纪公司名称
        ('IsActive', ctypes.c_int),  # ///是否活跃
    ]


# ///交易所交易员
class TraderField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('Password', ctypes.c_char * 41),  # ///密码
        ('InstallCount', ctypes.c_int),  # ///安装数量
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('OrderCancelAlg', ctypes.c_char * 1),  # ///撤单时选择席位算法
    ]


# ///投资者
class InvestorField(BaseField):
    _fields_ = [
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorGroupID', ctypes.c_char * 13),  # ///投资者分组代码
        ('InvestorName', ctypes.c_char * 81),  # ///投资者名称
        ('IdentifiedCardType', ctypes.c_char * 1),  # ///证件类型
        ('IdentifiedCardNo', ctypes.c_char * 51),  # ///证件号码
        ('IsActive', ctypes.c_int),  # ///是否活跃
        ('Telephone', ctypes.c_char * 41),  # ///联系电话
        ('Address', ctypes.c_char * 101),  # ///通讯地址
        ('OpenDate', ctypes.c_char * 9),  # ///开户日期
        ('Mobile', ctypes.c_char * 41),  # ///手机
        ('CommModelID', ctypes.c_char * 13),  # ///手续费率模板代码
        ('MarginModelID', ctypes.c_char * 13),  # ///保证金率模板代码
        ('IsOrderFreq', ctypes.c_char * 1),  # ///是否频率控制
        ('IsOpenVolLimit', ctypes.c_char * 1),  # ///是否开仓限制
    ]


# ///交易编码
class TradingCodeField(BaseField):
    _fields_ = [
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('IsActive', ctypes.c_int),  # ///是否活跃
        ('ClientIDType', ctypes.c_char * 1),  # ///交易编码类型
        ('BranchID', ctypes.c_char * 9),  # ///营业部编号
        ('BizType', ctypes.c_char * 1),  # ///业务类型
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
    ]


# ///会员编码和经纪公司编码对照表
class PartBrokerField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('IsActive', ctypes.c_int),  # ///是否活跃
    ]


# ///管理用户
class SuperUserField(BaseField):
    _fields_ = [
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('UserName', ctypes.c_char * 81),  # ///用户名称
        ('Password', ctypes.c_char * 41),  # ///密码
        ('IsActive', ctypes.c_int),  # ///是否活跃
    ]


# ///管理用户功能权限
class SuperUserFunctionField(BaseField):
    _fields_ = [
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('FunctionCode', ctypes.c_char * 1),  # ///功能代码
    ]


# ///投资者组
class InvestorGroupField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorGroupID', ctypes.c_char * 13),  # ///投资者分组代码
        ('InvestorGroupName', ctypes.c_char * 41),  # ///投资者分组名称
    ]


# ///资金账户
class TradingAccountField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('PreMortgage', ctypes.c_double),  # ///上次质押金额
        ('PreCredit', ctypes.c_double),  # ///上次信用额度
        ('PreDeposit', ctypes.c_double),  # ///上次存款额
        ('PreBalance', ctypes.c_double),  # ///上次结算准备金
        ('PreMargin', ctypes.c_double),  # ///上次占用的保证金
        ('InterestBase', ctypes.c_double),  # ///利息基数
        ('Interest', ctypes.c_double),  # ///利息收入
        ('Deposit', ctypes.c_double),  # ///入金金额
        ('Withdraw', ctypes.c_double),  # ///出金金额
        ('FrozenMargin', ctypes.c_double),  # ///冻结的保证金
        ('FrozenCash', ctypes.c_double),  # ///冻结的资金
        ('FrozenCommission', ctypes.c_double),  # ///冻结的手续费
        ('CurrMargin', ctypes.c_double),  # ///当前保证金总额
        ('CashIn', ctypes.c_double),  # ///资金差额
        ('Commission', ctypes.c_double),  # ///手续费
        ('CloseProfit', ctypes.c_double),  # ///平仓盈亏
        ('PositionProfit', ctypes.c_double),  # ///持仓盈亏
        ('Balance', ctypes.c_double),  # ///期货结算准备金
        ('Available', ctypes.c_double),  # ///可用资金
        ('WithdrawQuota', ctypes.c_double),  # ///可取资金
        ('Reserve', ctypes.c_double),  # ///基本准备金
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('SettlementID', ctypes.c_int),  # ///结算编号
        ('Credit', ctypes.c_double),  # ///信用额度
        ('Mortgage', ctypes.c_double),  # ///质押金额
        ('ExchangeMargin', ctypes.c_double),  # ///交易所保证金
        ('DeliveryMargin', ctypes.c_double),  # ///投资者交割保证金
        ('ExchangeDeliveryMargin', ctypes.c_double),  # ///交易所交割保证金
        ('ReserveBalance', ctypes.c_double),  # ///保底期货结算准备金
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('PreFundMortgageIn', ctypes.c_double),  # ///上次货币质入金额
        ('PreFundMortgageOut', ctypes.c_double),  # ///上次货币质出金额
        ('FundMortgageIn', ctypes.c_double),  # ///货币质入金额
        ('FundMortgageOut', ctypes.c_double),  # ///货币质出金额
        ('FundMortgageAvailable', ctypes.c_double),  # ///货币质押余额
        ('MortgageableFund', ctypes.c_double),  # ///可质押货币金额
        ('SpecProductMargin', ctypes.c_double),  # ///特殊产品占用保证金
        ('SpecProductFrozenMargin', ctypes.c_double),  # ///特殊产品冻结保证金
        ('SpecProductCommission', ctypes.c_double),  # ///特殊产品手续费
        ('SpecProductFrozenCommission', ctypes.c_double),  # ///特殊产品冻结手续费
        ('SpecProductPositionProfit', ctypes.c_double),  # ///特殊产品持仓盈亏
        ('SpecProductCloseProfit', ctypes.c_double),  # ///特殊产品平仓盈亏
        ('SpecProductPositionProfitByAlg', ctypes.c_double),  # ///根据持仓盈亏算法计算的特殊产品持仓盈亏
        ('SpecProductExchangeMargin', ctypes.c_double),  # ///特殊产品交易所保证金
        ('BizType', ctypes.c_char * 1),  # ///业务类型
        ('FrozenSwap', ctypes.c_double),  # ///延时换汇冻结金额
        ('RemainSwap', ctypes.c_double),  # ///剩余换汇额度
    ]


# ///投资者持仓
class InvestorPositionField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('PosiDirection', ctypes.c_char * 1),  # ///持仓多空方向
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('PositionDate', ctypes.c_char * 1),  # ///持仓日期
        ('YdPosition', ctypes.c_int),  # ///上日持仓
        ('Position', ctypes.c_int),  # ///今日持仓
        ('LongFrozen', ctypes.c_int),  # ///多头冻结
        ('ShortFrozen', ctypes.c_int),  # ///空头冻结
        ('LongFrozenAmount', ctypes.c_double),  # ///开仓冻结金额
        ('ShortFrozenAmount', ctypes.c_double),  # ///开仓冻结金额
        ('OpenVolume', ctypes.c_int),  # ///开仓量
        ('CloseVolume', ctypes.c_int),  # ///平仓量
        ('OpenAmount', ctypes.c_double),  # ///开仓金额
        ('CloseAmount', ctypes.c_double),  # ///平仓金额
        ('PositionCost', ctypes.c_double),  # ///持仓成本
        ('PreMargin', ctypes.c_double),  # ///上次占用的保证金
        ('UseMargin', ctypes.c_double),  # ///占用的保证金
        ('FrozenMargin', ctypes.c_double),  # ///冻结的保证金
        ('FrozenCash', ctypes.c_double),  # ///冻结的资金
        ('FrozenCommission', ctypes.c_double),  # ///冻结的手续费
        ('CashIn', ctypes.c_double),  # ///资金差额
        ('Commission', ctypes.c_double),  # ///手续费
        ('CloseProfit', ctypes.c_double),  # ///平仓盈亏
        ('PositionProfit', ctypes.c_double),  # ///持仓盈亏
        ('PreSettlementPrice', ctypes.c_double),  # ///上次结算价
        ('SettlementPrice', ctypes.c_double),  # ///本次结算价
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('SettlementID', ctypes.c_int),  # ///结算编号
        ('OpenCost', ctypes.c_double),  # ///开仓成本
        ('ExchangeMargin', ctypes.c_double),  # ///交易所保证金
        ('CombPosition', ctypes.c_int),  # ///组合成交形成的持仓
        ('CombLongFrozen', ctypes.c_int),  # ///组合多头冻结
        ('CombShortFrozen', ctypes.c_int),  # ///组合空头冻结
        ('CloseProfitByDate', ctypes.c_double),  # ///逐日盯市平仓盈亏
        ('CloseProfitByTrade', ctypes.c_double),  # ///逐笔对冲平仓盈亏
        ('TodayPosition', ctypes.c_int),  # ///今日持仓
        ('MarginRateByMoney', ctypes.c_double),  # ///保证金率
        ('MarginRateByVolume', ctypes.c_double),  # ///保证金率(按手数)
        ('StrikeFrozen', ctypes.c_int),  # ///执行冻结
        ('StrikeFrozenAmount', ctypes.c_double),  # ///执行冻结金额
        ('AbandonFrozen', ctypes.c_int),  # ///放弃执行冻结
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('YdStrikeFrozen', ctypes.c_int),  # ///执行冻结的昨仓
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('PositionCostOffset', ctypes.c_double),  # ///持仓成本差值
        ('TasPosition', ctypes.c_int),  # ///tas持仓手数
        ('TasPositionCost', ctypes.c_double),  # ///tas持仓成本
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///合约保证金率
class InstrumentMarginRateField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('InvestorRange', ctypes.c_char * 1),  # ///投资者范围
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('LongMarginRatioByMoney', ctypes.c_double),  # ///多头保证金率
        ('LongMarginRatioByVolume', ctypes.c_double),  # ///多头保证金费
        ('ShortMarginRatioByMoney', ctypes.c_double),  # ///空头保证金率
        ('ShortMarginRatioByVolume', ctypes.c_double),  # ///空头保证金费
        ('IsRelative', ctypes.c_int),  # ///是否相对交易所收取
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///合约手续费率
class InstrumentCommissionRateField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('InvestorRange', ctypes.c_char * 1),  # ///投资者范围
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('OpenRatioByMoney', ctypes.c_double),  # ///开仓手续费率
        ('OpenRatioByVolume', ctypes.c_double),  # ///开仓手续费
        ('CloseRatioByMoney', ctypes.c_double),  # ///平仓手续费率
        ('CloseRatioByVolume', ctypes.c_double),  # ///平仓手续费
        ('CloseTodayRatioByMoney', ctypes.c_double),  # ///平今手续费率
        ('CloseTodayRatioByVolume', ctypes.c_double),  # ///平今手续费
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('BizType', ctypes.c_char * 1),  # ///业务类型
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///深度行情
class DepthMarketDataField(BaseField):
    _fields_ = [
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('reserve2', ctypes.c_char * 31),  # ///保留的无效字段
        ('LastPrice', ctypes.c_double),  # ///最新价
        ('PreSettlementPrice', ctypes.c_double),  # ///上次结算价
        ('PreClosePrice', ctypes.c_double),  # ///昨收盘
        ('PreOpenInterest', ctypes.c_double),  # ///昨持仓量
        ('OpenPrice', ctypes.c_double),  # ///今开盘
        ('HighestPrice', ctypes.c_double),  # ///最高价
        ('LowestPrice', ctypes.c_double),  # ///最低价
        ('Volume', ctypes.c_int),  # ///数量
        ('Turnover', ctypes.c_double),  # ///成交金额
        ('OpenInterest', ctypes.c_double),  # ///持仓量
        ('ClosePrice', ctypes.c_double),  # ///今收盘
        ('SettlementPrice', ctypes.c_double),  # ///本次结算价
        ('UpperLimitPrice', ctypes.c_double),  # ///涨停板价
        ('LowerLimitPrice', ctypes.c_double),  # ///跌停板价
        ('PreDelta', ctypes.c_double),  # ///昨虚实度
        ('CurrDelta', ctypes.c_double),  # ///今虚实度
        ('UpdateTime', ctypes.c_char * 9),  # ///最后修改时间
        ('UpdateMillisec', ctypes.c_int),  # ///最后修改毫秒
        ('BidPrice1', ctypes.c_double),  # ///申买价一
        ('BidVolume1', ctypes.c_int),  # ///申买量一
        ('AskPrice1', ctypes.c_double),  # ///申卖价一
        ('AskVolume1', ctypes.c_int),  # ///申卖量一
        ('BidPrice2', ctypes.c_double),  # ///申买价二
        ('BidVolume2', ctypes.c_int),  # ///申买量二
        ('AskPrice2', ctypes.c_double),  # ///申卖价二
        ('AskVolume2', ctypes.c_int),  # ///申卖量二
        ('BidPrice3', ctypes.c_double),  # ///申买价三
        ('BidVolume3', ctypes.c_int),  # ///申买量三
        ('AskPrice3', ctypes.c_double),  # ///申卖价三
        ('AskVolume3', ctypes.c_int),  # ///申卖量三
        ('BidPrice4', ctypes.c_double),  # ///申买价四
        ('BidVolume4', ctypes.c_int),  # ///申买量四
        ('AskPrice4', ctypes.c_double),  # ///申卖价四
        ('AskVolume4', ctypes.c_int),  # ///申卖量四
        ('BidPrice5', ctypes.c_double),  # ///申买价五
        ('BidVolume5', ctypes.c_int),  # ///申买量五
        ('AskPrice5', ctypes.c_double),  # ///申卖价五
        ('AskVolume5', ctypes.c_int),  # ///申卖量五
        ('AveragePrice', ctypes.c_double),  # ///当日均价
        ('ActionDay', ctypes.c_char * 9),  # ///业务日期
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('ExchangeInstID', ctypes.c_char * 81),  # ///合约在交易所的代码
        ('BandingUpperPrice', ctypes.c_double),  # ///上带价
        ('BandingLowerPrice', ctypes.c_double),  # ///下带价
    ]


# ///投资者合约交易权限
class InstrumentTradingRightField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('InvestorRange', ctypes.c_char * 1),  # ///投资者范围
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('TradingRight', ctypes.c_char * 1),  # ///交易权限
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///经纪公司用户
class BrokerUserField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('UserName', ctypes.c_char * 81),  # ///用户名称
        ('UserType', ctypes.c_char * 1),  # ///用户类型
        ('IsActive', ctypes.c_int),  # ///是否活跃
        ('IsUsingOTP', ctypes.c_int),  # ///是否使用令牌
        ('IsAuthForce', ctypes.c_int),  # ///是否强制终端认证
    ]


# ///经纪公司用户口令
class BrokerUserPasswordField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('Password', ctypes.c_char * 41),  # ///密码
        ('LastUpdateTime', ctypes.c_char * 17),  # ///上次修改时间
        ('LastLoginTime', ctypes.c_char * 17),  # ///上次登陆时间
        ('ExpireDate', ctypes.c_char * 9),  # ///密码过期时间
        ('WeakExpireDate', ctypes.c_char * 9),  # ///弱密码过期时间
    ]


# ///经纪公司用户功能权限
class BrokerUserFunctionField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('BrokerFunctionCode', ctypes.c_char * 1),  # ///经纪公司功能代码
    ]


# ///交易所交易员报盘机
class TraderOfferField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('Password', ctypes.c_char * 41),  # ///密码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('OrderLocalID', ctypes.c_char * 13),  # ///本地报单编号
        ('TraderConnectStatus', ctypes.c_char * 1),  # ///交易所交易员连接状态
        ('ConnectRequestDate', ctypes.c_char * 9),  # ///发出连接请求的日期
        ('ConnectRequestTime', ctypes.c_char * 9),  # ///发出连接请求的时间
        ('LastReportDate', ctypes.c_char * 9),  # ///上次报告日期
        ('LastReportTime', ctypes.c_char * 9),  # ///上次报告时间
        ('ConnectDate', ctypes.c_char * 9),  # ///完成连接日期
        ('ConnectTime', ctypes.c_char * 9),  # ///完成连接时间
        ('StartDate', ctypes.c_char * 9),  # ///启动日期
        ('StartTime', ctypes.c_char * 9),  # ///启动时间
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('MaxTradeID', ctypes.c_char * 21),  # ///本席位最大成交编号
        ('MaxOrderMessageReference', ctypes.c_char * 7),  # ///本席位最大报单备拷
        ('OrderCancelAlg', ctypes.c_char * 1),  # ///撤单时选择席位算法
    ]


# ///投资者结算结果
class SettlementInfoField(BaseField):
    _fields_ = [
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('SettlementID', ctypes.c_int),  # ///结算编号
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('SequenceNo', ctypes.c_int),  # ///序号
        ('Content', ctypes.c_char * 501),  # ///消息正文
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
    ]


# ///合约保证金率调整
class InstrumentMarginRateAdjustField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('InvestorRange', ctypes.c_char * 1),  # ///投资者范围
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('LongMarginRatioByMoney', ctypes.c_double),  # ///多头保证金率
        ('LongMarginRatioByVolume', ctypes.c_double),  # ///多头保证金费
        ('ShortMarginRatioByMoney', ctypes.c_double),  # ///空头保证金率
        ('ShortMarginRatioByVolume', ctypes.c_double),  # ///空头保证金费
        ('IsRelative', ctypes.c_int),  # ///是否相对交易所收取
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///交易所保证金率
class ExchangeMarginRateField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('LongMarginRatioByMoney', ctypes.c_double),  # ///多头保证金率
        ('LongMarginRatioByVolume', ctypes.c_double),  # ///多头保证金费
        ('ShortMarginRatioByMoney', ctypes.c_double),  # ///空头保证金率
        ('ShortMarginRatioByVolume', ctypes.c_double),  # ///空头保证金费
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///交易所保证金率调整
class ExchangeMarginRateAdjustField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('LongMarginRatioByMoney', ctypes.c_double),  # ///跟随交易所投资者多头保证金率
        ('LongMarginRatioByVolume', ctypes.c_double),  # ///跟随交易所投资者多头保证金费
        ('ShortMarginRatioByMoney', ctypes.c_double),  # ///跟随交易所投资者空头保证金率
        ('ShortMarginRatioByVolume', ctypes.c_double),  # ///跟随交易所投资者空头保证金费
        ('ExchLongMarginRatioByMoney', ctypes.c_double),  # ///交易所多头保证金率
        ('ExchLongMarginRatioByVolume', ctypes.c_double),  # ///交易所多头保证金费
        ('ExchShortMarginRatioByMoney', ctypes.c_double),  # ///交易所空头保证金率
        ('ExchShortMarginRatioByVolume', ctypes.c_double),  # ///交易所空头保证金费
        ('NoLongMarginRatioByMoney', ctypes.c_double),  # ///不跟随交易所投资者多头保证金率
        ('NoLongMarginRatioByVolume', ctypes.c_double),  # ///不跟随交易所投资者多头保证金费
        ('NoShortMarginRatioByMoney', ctypes.c_double),  # ///不跟随交易所投资者空头保证金率
        ('NoShortMarginRatioByVolume', ctypes.c_double),  # ///不跟随交易所投资者空头保证金费
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///汇率
class ExchangeRateField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('FromCurrencyID', ctypes.c_char * 4),  # ///源币种
        ('FromCurrencyUnit', ctypes.c_double),  # ///源币种单位数量
        ('ToCurrencyID', ctypes.c_char * 4),  # ///目标币种
        ('ExchangeRate', ctypes.c_double),  # ///汇率
    ]


# ///结算引用
class SettlementRefField(BaseField):
    _fields_ = [
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('SettlementID', ctypes.c_int),  # ///结算编号
    ]


# ///当前时间
class CurrentTimeField(BaseField):
    _fields_ = [
        ('CurrDate', ctypes.c_char * 9),  # ///当前交易日
        ('CurrTime', ctypes.c_char * 9),  # ///当前时间
        ('CurrMillisec', ctypes.c_int),  # ///当前时间（毫秒）
        ('ActionDay', ctypes.c_char * 9),  # ///自然日期
    ]


# ///通讯阶段
class CommPhaseField(BaseField):
    _fields_ = [
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('CommPhaseNo', ctypes.c_short),  # ///通讯时段编号
        ('SystemID', ctypes.c_char * 21),  # ///系统编号
    ]


# ///登录信息
class LoginInfoField(BaseField):
    _fields_ = [
        ('FrontID', ctypes.c_int),  # ///前置编号
        ('SessionID', ctypes.c_int),  # ///会话编号
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('LoginDate', ctypes.c_char * 9),  # ///登录日期
        ('LoginTime', ctypes.c_char * 9),  # ///登录时间
        ('reserve1', ctypes.c_char * 16),  # ///保留的无效字段
        ('UserProductInfo', ctypes.c_char * 11),  # ///用户端产品信息
        ('InterfaceProductInfo', ctypes.c_char * 11),  # ///接口端产品信息
        ('ProtocolInfo', ctypes.c_char * 11),  # ///协议信息
        ('SystemName', ctypes.c_char * 41),  # ///系统名称
        ('PasswordDeprecated', ctypes.c_char * 41),  # ///密码,已弃用
        ('MaxOrderRef', ctypes.c_char * 13),  # ///最大报单引用
        ('SHFETime', ctypes.c_char * 9),  # ///上期所时间
        ('DCETime', ctypes.c_char * 9),  # ///大商所时间
        ('CZCETime', ctypes.c_char * 9),  # ///郑商所时间
        ('FFEXTime', ctypes.c_char * 9),  # ///中金所时间
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('OneTimePassword', ctypes.c_char * 41),  # ///动态密码
        ('INETime', ctypes.c_char * 9),  # ///能源中心时间
        ('IsQryControl', ctypes.c_int),  # ///查询时是否需要流控
        ('LoginRemark', ctypes.c_char * 36),  # ///登录备注
        ('Password', ctypes.c_char * 41),  # ///密码
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///登录信息
class LogoutAllField(BaseField):
    _fields_ = [
        ('FrontID', ctypes.c_int),  # ///前置编号
        ('SessionID', ctypes.c_int),  # ///会话编号
        ('SystemName', ctypes.c_char * 41),  # ///系统名称
    ]


# ///前置状态
class FrontStatusField(BaseField):
    _fields_ = [
        ('FrontID', ctypes.c_int),  # ///前置编号
        ('LastReportDate', ctypes.c_char * 9),  # ///上次报告日期
        ('LastReportTime', ctypes.c_char * 9),  # ///上次报告时间
        ('IsActive', ctypes.c_int),  # ///是否活跃
    ]


# ///用户口令变更
class UserPasswordUpdateField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('OldPassword', ctypes.c_char * 41),  # ///原来的口令
        ('NewPassword', ctypes.c_char * 41),  # ///新的口令
    ]


# ///输入报单
class InputOrderField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('OrderRef', ctypes.c_char * 13),  # ///报单引用
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('OrderPriceType', ctypes.c_char * 1),  # ///报单价格条件
        ('Direction', ctypes.c_char * 1),  # ///买卖方向
        ('CombOffsetFlag', ctypes.c_char * 5),  # ///组合开平标志
        ('CombHedgeFlag', ctypes.c_char * 5),  # ///组合投机套保标志
        ('LimitPrice', ctypes.c_double),  # ///价格
        ('VolumeTotalOriginal', ctypes.c_int),  # ///数量
        ('TimeCondition', ctypes.c_char * 1),  # ///有效期类型
        ('GTDDate', ctypes.c_char * 9),  # ///GTD日期
        ('VolumeCondition', ctypes.c_char * 1),  # ///成交量类型
        ('MinVolume', ctypes.c_int),  # ///最小成交量
        ('ContingentCondition', ctypes.c_char * 1),  # ///触发条件
        ('StopPrice', ctypes.c_double),  # ///止损价
        ('ForceCloseReason', ctypes.c_char * 1),  # ///强平原因
        ('IsAutoSuspend', ctypes.c_int),  # ///自动挂起标志
        ('BusinessUnit', ctypes.c_char * 21),  # ///业务单元
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('UserForceClose', ctypes.c_int),  # ///用户强评标志
        ('IsSwapOrder', ctypes.c_int),  # ///互换单标志
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('AccountID', ctypes.c_char * 13),  # ///资金账号
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('ClientID', ctypes.c_char * 11),  # ///交易编码
        ('reserve2', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///报单
class OrderField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('OrderRef', ctypes.c_char * 13),  # ///报单引用
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('OrderPriceType', ctypes.c_char * 1),  # ///报单价格条件
        ('Direction', ctypes.c_char * 1),  # ///买卖方向
        ('CombOffsetFlag', ctypes.c_char * 5),  # ///组合开平标志
        ('CombHedgeFlag', ctypes.c_char * 5),  # ///组合投机套保标志
        ('LimitPrice', ctypes.c_double),  # ///价格
        ('VolumeTotalOriginal', ctypes.c_int),  # ///数量
        ('TimeCondition', ctypes.c_char * 1),  # ///有效期类型
        ('GTDDate', ctypes.c_char * 9),  # ///GTD日期
        ('VolumeCondition', ctypes.c_char * 1),  # ///成交量类型
        ('MinVolume', ctypes.c_int),  # ///最小成交量
        ('ContingentCondition', ctypes.c_char * 1),  # ///触发条件
        ('StopPrice', ctypes.c_double),  # ///止损价
        ('ForceCloseReason', ctypes.c_char * 1),  # ///强平原因
        ('IsAutoSuspend', ctypes.c_int),  # ///自动挂起标志
        ('BusinessUnit', ctypes.c_char * 21),  # ///业务单元
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('OrderLocalID', ctypes.c_char * 13),  # ///本地报单编号
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('reserve2', ctypes.c_char * 31),  # ///保留的无效字段
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('OrderSubmitStatus', ctypes.c_char * 1),  # ///报单提交状态
        ('NotifySequence', ctypes.c_int),  # ///报单提示序号
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('SettlementID', ctypes.c_int),  # ///结算编号
        ('OrderSysID', ctypes.c_char * 21),  # ///报单编号
        ('OrderSource', ctypes.c_char * 1),  # ///报单来源
        ('OrderStatus', ctypes.c_char * 1),  # ///报单状态
        ('OrderType', ctypes.c_char * 1),  # ///报单类型
        ('VolumeTraded', ctypes.c_int),  # ///今成交数量
        ('VolumeTotal', ctypes.c_int),  # ///剩余数量
        ('InsertDate', ctypes.c_char * 9),  # ///报单日期
        ('InsertTime', ctypes.c_char * 9),  # ///委托时间
        ('ActiveTime', ctypes.c_char * 9),  # ///激活时间
        ('SuspendTime', ctypes.c_char * 9),  # ///挂起时间
        ('UpdateTime', ctypes.c_char * 9),  # ///最后修改时间
        ('CancelTime', ctypes.c_char * 9),  # ///撤销时间
        ('ActiveTraderID', ctypes.c_char * 21),  # ///最后修改交易所交易员代码
        ('ClearingPartID', ctypes.c_char * 11),  # ///结算会员编号
        ('SequenceNo', ctypes.c_int),  # ///序号
        ('FrontID', ctypes.c_int),  # ///前置编号
        ('SessionID', ctypes.c_int),  # ///会话编号
        ('UserProductInfo', ctypes.c_char * 11),  # ///用户端产品信息
        ('StatusMsg', ctypes.c_char * 81),  # ///状态信息
        ('UserForceClose', ctypes.c_int),  # ///用户强评标志
        ('ActiveUserID', ctypes.c_char * 16),  # ///操作用户代码
        ('BrokerOrderSeq', ctypes.c_int),  # ///经纪公司报单编号
        ('RelativeOrderSysID', ctypes.c_char * 21),  # ///相关报单
        ('ZCETotalTradedVolume', ctypes.c_int),  # ///郑商所成交数量
        ('IsSwapOrder', ctypes.c_int),  # ///互换单标志
        ('BranchID', ctypes.c_char * 9),  # ///营业部编号
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('AccountID', ctypes.c_char * 13),  # ///资金账号
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('reserve3', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('ExchangeInstID', ctypes.c_char * 81),  # ///合约在交易所的代码
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///交易所报单
class ExchangeOrderField(BaseField):
    _fields_ = [
        ('OrderPriceType', ctypes.c_char * 1),  # ///报单价格条件
        ('Direction', ctypes.c_char * 1),  # ///买卖方向
        ('CombOffsetFlag', ctypes.c_char * 5),  # ///组合开平标志
        ('CombHedgeFlag', ctypes.c_char * 5),  # ///组合投机套保标志
        ('LimitPrice', ctypes.c_double),  # ///价格
        ('VolumeTotalOriginal', ctypes.c_int),  # ///数量
        ('TimeCondition', ctypes.c_char * 1),  # ///有效期类型
        ('GTDDate', ctypes.c_char * 9),  # ///GTD日期
        ('VolumeCondition', ctypes.c_char * 1),  # ///成交量类型
        ('MinVolume', ctypes.c_int),  # ///最小成交量
        ('ContingentCondition', ctypes.c_char * 1),  # ///触发条件
        ('StopPrice', ctypes.c_double),  # ///止损价
        ('ForceCloseReason', ctypes.c_char * 1),  # ///强平原因
        ('IsAutoSuspend', ctypes.c_int),  # ///自动挂起标志
        ('BusinessUnit', ctypes.c_char * 21),  # ///业务单元
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('OrderLocalID', ctypes.c_char * 13),  # ///本地报单编号
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('OrderSubmitStatus', ctypes.c_char * 1),  # ///报单提交状态
        ('NotifySequence', ctypes.c_int),  # ///报单提示序号
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('SettlementID', ctypes.c_int),  # ///结算编号
        ('OrderSysID', ctypes.c_char * 21),  # ///报单编号
        ('OrderSource', ctypes.c_char * 1),  # ///报单来源
        ('OrderStatus', ctypes.c_char * 1),  # ///报单状态
        ('OrderType', ctypes.c_char * 1),  # ///报单类型
        ('VolumeTraded', ctypes.c_int),  # ///今成交数量
        ('VolumeTotal', ctypes.c_int),  # ///剩余数量
        ('InsertDate', ctypes.c_char * 9),  # ///报单日期
        ('InsertTime', ctypes.c_char * 9),  # ///委托时间
        ('ActiveTime', ctypes.c_char * 9),  # ///激活时间
        ('SuspendTime', ctypes.c_char * 9),  # ///挂起时间
        ('UpdateTime', ctypes.c_char * 9),  # ///最后修改时间
        ('CancelTime', ctypes.c_char * 9),  # ///撤销时间
        ('ActiveTraderID', ctypes.c_char * 21),  # ///最后修改交易所交易员代码
        ('ClearingPartID', ctypes.c_char * 11),  # ///结算会员编号
        ('SequenceNo', ctypes.c_int),  # ///序号
        ('BranchID', ctypes.c_char * 9),  # ///营业部编号
        ('reserve2', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('ExchangeInstID', ctypes.c_char * 81),  # ///合约在交易所的代码
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///交易所报单插入失败
class ExchangeOrderInsertErrorField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('OrderLocalID', ctypes.c_char * 13),  # ///本地报单编号
        ('ErrorID', ctypes.c_int),  # ///错误代码
        ('ErrorMsg', ctypes.c_char * 81),  # ///错误信息
    ]


# ///输入报单操作
class InputOrderActionField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('OrderActionRef', ctypes.c_int),  # ///报单操作引用
        ('OrderRef', ctypes.c_char * 13),  # ///报单引用
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('FrontID', ctypes.c_int),  # ///前置编号
        ('SessionID', ctypes.c_int),  # ///会话编号
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('OrderSysID', ctypes.c_char * 21),  # ///报单编号
        ('ActionFlag', ctypes.c_char * 1),  # ///操作标志
        ('LimitPrice', ctypes.c_double),  # ///价格
        ('VolumeChange', ctypes.c_int),  # ///数量变化
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('reserve2', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///报单操作
class OrderActionField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('OrderActionRef', ctypes.c_int),  # ///报单操作引用
        ('OrderRef', ctypes.c_char * 13),  # ///报单引用
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('FrontID', ctypes.c_int),  # ///前置编号
        ('SessionID', ctypes.c_int),  # ///会话编号
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('OrderSysID', ctypes.c_char * 21),  # ///报单编号
        ('ActionFlag', ctypes.c_char * 1),  # ///操作标志
        ('LimitPrice', ctypes.c_double),  # ///价格
        ('VolumeChange', ctypes.c_int),  # ///数量变化
        ('ActionDate', ctypes.c_char * 9),  # ///操作日期
        ('ActionTime', ctypes.c_char * 9),  # ///操作时间
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('OrderLocalID', ctypes.c_char * 13),  # ///本地报单编号
        ('ActionLocalID', ctypes.c_char * 13),  # ///操作本地编号
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('BusinessUnit', ctypes.c_char * 21),  # ///业务单元
        ('OrderActionStatus', ctypes.c_char * 1),  # ///报单操作状态
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('StatusMsg', ctypes.c_char * 81),  # ///状态信息
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('BranchID', ctypes.c_char * 9),  # ///营业部编号
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('reserve2', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///交易所报单操作
class ExchangeOrderActionField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('OrderSysID', ctypes.c_char * 21),  # ///报单编号
        ('ActionFlag', ctypes.c_char * 1),  # ///操作标志
        ('LimitPrice', ctypes.c_double),  # ///价格
        ('VolumeChange', ctypes.c_int),  # ///数量变化
        ('ActionDate', ctypes.c_char * 9),  # ///操作日期
        ('ActionTime', ctypes.c_char * 9),  # ///操作时间
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('OrderLocalID', ctypes.c_char * 13),  # ///本地报单编号
        ('ActionLocalID', ctypes.c_char * 13),  # ///操作本地编号
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('BusinessUnit', ctypes.c_char * 21),  # ///业务单元
        ('OrderActionStatus', ctypes.c_char * 1),  # ///报单操作状态
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('BranchID', ctypes.c_char * 9),  # ///营业部编号
        ('reserve1', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///交易所报单操作失败
class ExchangeOrderActionErrorField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('OrderSysID', ctypes.c_char * 21),  # ///报单编号
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('OrderLocalID', ctypes.c_char * 13),  # ///本地报单编号
        ('ActionLocalID', ctypes.c_char * 13),  # ///操作本地编号
        ('ErrorID', ctypes.c_int),  # ///错误代码
        ('ErrorMsg', ctypes.c_char * 81),  # ///错误信息
    ]


# ///交易所成交
class ExchangeTradeField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('TradeID', ctypes.c_char * 21),  # ///成交编号
        ('Direction', ctypes.c_char * 1),  # ///买卖方向
        ('OrderSysID', ctypes.c_char * 21),  # ///报单编号
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('TradingRole', ctypes.c_char * 1),  # ///交易角色
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('OffsetFlag', ctypes.c_char * 1),  # ///开平标志
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('Price', ctypes.c_double),  # ///价格
        ('Volume', ctypes.c_int),  # ///数量
        ('TradeDate', ctypes.c_char * 9),  # ///成交时期
        ('TradeTime', ctypes.c_char * 9),  # ///成交时间
        ('TradeType', ctypes.c_char * 1),  # ///成交类型
        ('PriceSource', ctypes.c_char * 1),  # ///成交价来源
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
        ('OrderLocalID', ctypes.c_char * 13),  # ///本地报单编号
        ('ClearingPartID', ctypes.c_char * 11),  # ///结算会员编号
        ('BusinessUnit', ctypes.c_char * 21),  # ///业务单元
        ('SequenceNo', ctypes.c_int),  # ///序号
        ('TradeSource', ctypes.c_char * 1),  # ///成交来源
        ('ExchangeInstID', ctypes.c_char * 81),  # ///合约在交易所的代码
    ]


# ///成交
class TradeField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('OrderRef', ctypes.c_char * 13),  # ///报单引用
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('TradeID', ctypes.c_char * 21),  # ///成交编号
        ('Direction', ctypes.c_char * 1),  # ///买卖方向
        ('OrderSysID', ctypes.c_char * 21),  # ///报单编号
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('TradingRole', ctypes.c_char * 1),  # ///交易角色
        ('reserve2', ctypes.c_char * 31),  # ///保留的无效字段
        ('OffsetFlag', ctypes.c_char * 1),  # ///开平标志
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('Price', ctypes.c_double),  # ///价格
        ('Volume', ctypes.c_int),  # ///数量
        ('TradeDate', ctypes.c_char * 9),  # ///成交时期
        ('TradeTime', ctypes.c_char * 9),  # ///成交时间
        ('TradeType', ctypes.c_char * 1),  # ///成交类型
        ('PriceSource', ctypes.c_char * 1),  # ///成交价来源
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
        ('OrderLocalID', ctypes.c_char * 13),  # ///本地报单编号
        ('ClearingPartID', ctypes.c_char * 11),  # ///结算会员编号
        ('BusinessUnit', ctypes.c_char * 21),  # ///业务单元
        ('SequenceNo', ctypes.c_int),  # ///序号
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('SettlementID', ctypes.c_int),  # ///结算编号
        ('BrokerOrderSeq', ctypes.c_int),  # ///经纪公司报单编号
        ('TradeSource', ctypes.c_char * 1),  # ///成交来源
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('ExchangeInstID', ctypes.c_char * 81),  # ///合约在交易所的代码
    ]


# ///用户会话
class UserSessionField(BaseField):
    _fields_ = [
        ('FrontID', ctypes.c_int),  # ///前置编号
        ('SessionID', ctypes.c_int),  # ///会话编号
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('LoginDate', ctypes.c_char * 9),  # ///登录日期
        ('LoginTime', ctypes.c_char * 9),  # ///登录时间
        ('reserve1', ctypes.c_char * 16),  # ///保留的无效字段
        ('UserProductInfo', ctypes.c_char * 11),  # ///用户端产品信息
        ('InterfaceProductInfo', ctypes.c_char * 11),  # ///接口端产品信息
        ('ProtocolInfo', ctypes.c_char * 11),  # ///协议信息
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('LoginRemark', ctypes.c_char * 36),  # ///登录备注
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///查询最大报单数量
class QryMaxOrderVolumeField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('Direction', ctypes.c_char * 1),  # ///买卖方向
        ('OffsetFlag', ctypes.c_char * 1),  # ///开平标志
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('MaxVolume', ctypes.c_int),  # ///最大允许报单数量
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///投资者结算结果确认信息
class SettlementInfoConfirmField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('ConfirmDate', ctypes.c_char * 9),  # ///确认日期
        ('ConfirmTime', ctypes.c_char * 9),  # ///确认时间
        ('SettlementID', ctypes.c_int),  # ///结算编号
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
    ]


# ///出入金同步
class SyncDepositField(BaseField):
    _fields_ = [
        ('DepositSeqNo', ctypes.c_char * 15),  # ///出入金流水号
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('Deposit', ctypes.c_double),  # ///入金金额
        ('IsForce', ctypes.c_int),  # ///是否强制进行
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('IsFromSopt', ctypes.c_int),  # ///是否是个股期权内转
        ('TradingPassword', ctypes.c_char * 41),  # ///资金密码
    ]


# ///货币质押同步
class SyncFundMortgageField(BaseField):
    _fields_ = [
        ('MortgageSeqNo', ctypes.c_char * 15),  # ///货币质押流水号
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('FromCurrencyID', ctypes.c_char * 4),  # ///源币种
        ('MortgageAmount', ctypes.c_double),  # ///质押金额
        ('ToCurrencyID', ctypes.c_char * 4),  # ///目标币种
    ]


# ///经纪公司同步
class BrokerSyncField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
    ]


# ///正在同步中的投资者
class SyncingInvestorField(BaseField):
    _fields_ = [
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorGroupID', ctypes.c_char * 13),  # ///投资者分组代码
        ('InvestorName', ctypes.c_char * 81),  # ///投资者名称
        ('IdentifiedCardType', ctypes.c_char * 1),  # ///证件类型
        ('IdentifiedCardNo', ctypes.c_char * 51),  # ///证件号码
        ('IsActive', ctypes.c_int),  # ///是否活跃
        ('Telephone', ctypes.c_char * 41),  # ///联系电话
        ('Address', ctypes.c_char * 101),  # ///通讯地址
        ('OpenDate', ctypes.c_char * 9),  # ///开户日期
        ('Mobile', ctypes.c_char * 41),  # ///手机
        ('CommModelID', ctypes.c_char * 13),  # ///手续费率模板代码
        ('MarginModelID', ctypes.c_char * 13),  # ///保证金率模板代码
        ('IsOrderFreq', ctypes.c_char * 1),  # ///是否频率控制
        ('IsOpenVolLimit', ctypes.c_char * 1),  # ///是否开仓限制
    ]


# ///正在同步中的交易代码
class SyncingTradingCodeField(BaseField):
    _fields_ = [
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('IsActive', ctypes.c_int),  # ///是否活跃
        ('ClientIDType', ctypes.c_char * 1),  # ///交易编码类型
    ]


# ///正在同步中的投资者分组
class SyncingInvestorGroupField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorGroupID', ctypes.c_char * 13),  # ///投资者分组代码
        ('InvestorGroupName', ctypes.c_char * 41),  # ///投资者分组名称
    ]


# ///正在同步中的交易账号
class SyncingTradingAccountField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('PreMortgage', ctypes.c_double),  # ///上次质押金额
        ('PreCredit', ctypes.c_double),  # ///上次信用额度
        ('PreDeposit', ctypes.c_double),  # ///上次存款额
        ('PreBalance', ctypes.c_double),  # ///上次结算准备金
        ('PreMargin', ctypes.c_double),  # ///上次占用的保证金
        ('InterestBase', ctypes.c_double),  # ///利息基数
        ('Interest', ctypes.c_double),  # ///利息收入
        ('Deposit', ctypes.c_double),  # ///入金金额
        ('Withdraw', ctypes.c_double),  # ///出金金额
        ('FrozenMargin', ctypes.c_double),  # ///冻结的保证金
        ('FrozenCash', ctypes.c_double),  # ///冻结的资金
        ('FrozenCommission', ctypes.c_double),  # ///冻结的手续费
        ('CurrMargin', ctypes.c_double),  # ///当前保证金总额
        ('CashIn', ctypes.c_double),  # ///资金差额
        ('Commission', ctypes.c_double),  # ///手续费
        ('CloseProfit', ctypes.c_double),  # ///平仓盈亏
        ('PositionProfit', ctypes.c_double),  # ///持仓盈亏
        ('Balance', ctypes.c_double),  # ///期货结算准备金
        ('Available', ctypes.c_double),  # ///可用资金
        ('WithdrawQuota', ctypes.c_double),  # ///可取资金
        ('Reserve', ctypes.c_double),  # ///基本准备金
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('SettlementID', ctypes.c_int),  # ///结算编号
        ('Credit', ctypes.c_double),  # ///信用额度
        ('Mortgage', ctypes.c_double),  # ///质押金额
        ('ExchangeMargin', ctypes.c_double),  # ///交易所保证金
        ('DeliveryMargin', ctypes.c_double),  # ///投资者交割保证金
        ('ExchangeDeliveryMargin', ctypes.c_double),  # ///交易所交割保证金
        ('ReserveBalance', ctypes.c_double),  # ///保底期货结算准备金
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('PreFundMortgageIn', ctypes.c_double),  # ///上次货币质入金额
        ('PreFundMortgageOut', ctypes.c_double),  # ///上次货币质出金额
        ('FundMortgageIn', ctypes.c_double),  # ///货币质入金额
        ('FundMortgageOut', ctypes.c_double),  # ///货币质出金额
        ('FundMortgageAvailable', ctypes.c_double),  # ///货币质押余额
        ('MortgageableFund', ctypes.c_double),  # ///可质押货币金额
        ('SpecProductMargin', ctypes.c_double),  # ///特殊产品占用保证金
        ('SpecProductFrozenMargin', ctypes.c_double),  # ///特殊产品冻结保证金
        ('SpecProductCommission', ctypes.c_double),  # ///特殊产品手续费
        ('SpecProductFrozenCommission', ctypes.c_double),  # ///特殊产品冻结手续费
        ('SpecProductPositionProfit', ctypes.c_double),  # ///特殊产品持仓盈亏
        ('SpecProductCloseProfit', ctypes.c_double),  # ///特殊产品平仓盈亏
        ('SpecProductPositionProfitByAlg', ctypes.c_double),  # ///根据持仓盈亏算法计算的特殊产品持仓盈亏
        ('SpecProductExchangeMargin', ctypes.c_double),  # ///特殊产品交易所保证金
        ('FrozenSwap', ctypes.c_double),  # ///延时换汇冻结金额
        ('RemainSwap', ctypes.c_double),  # ///剩余换汇额度
    ]


# ///正在同步中的投资者持仓
class SyncingInvestorPositionField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('PosiDirection', ctypes.c_char * 1),  # ///持仓多空方向
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('PositionDate', ctypes.c_char * 1),  # ///持仓日期
        ('YdPosition', ctypes.c_int),  # ///上日持仓
        ('Position', ctypes.c_int),  # ///今日持仓
        ('LongFrozen', ctypes.c_int),  # ///多头冻结
        ('ShortFrozen', ctypes.c_int),  # ///空头冻结
        ('LongFrozenAmount', ctypes.c_double),  # ///开仓冻结金额
        ('ShortFrozenAmount', ctypes.c_double),  # ///开仓冻结金额
        ('OpenVolume', ctypes.c_int),  # ///开仓量
        ('CloseVolume', ctypes.c_int),  # ///平仓量
        ('OpenAmount', ctypes.c_double),  # ///开仓金额
        ('CloseAmount', ctypes.c_double),  # ///平仓金额
        ('PositionCost', ctypes.c_double),  # ///持仓成本
        ('PreMargin', ctypes.c_double),  # ///上次占用的保证金
        ('UseMargin', ctypes.c_double),  # ///占用的保证金
        ('FrozenMargin', ctypes.c_double),  # ///冻结的保证金
        ('FrozenCash', ctypes.c_double),  # ///冻结的资金
        ('FrozenCommission', ctypes.c_double),  # ///冻结的手续费
        ('CashIn', ctypes.c_double),  # ///资金差额
        ('Commission', ctypes.c_double),  # ///手续费
        ('CloseProfit', ctypes.c_double),  # ///平仓盈亏
        ('PositionProfit', ctypes.c_double),  # ///持仓盈亏
        ('PreSettlementPrice', ctypes.c_double),  # ///上次结算价
        ('SettlementPrice', ctypes.c_double),  # ///本次结算价
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('SettlementID', ctypes.c_int),  # ///结算编号
        ('OpenCost', ctypes.c_double),  # ///开仓成本
        ('ExchangeMargin', ctypes.c_double),  # ///交易所保证金
        ('CombPosition', ctypes.c_int),  # ///组合成交形成的持仓
        ('CombLongFrozen', ctypes.c_int),  # ///组合多头冻结
        ('CombShortFrozen', ctypes.c_int),  # ///组合空头冻结
        ('CloseProfitByDate', ctypes.c_double),  # ///逐日盯市平仓盈亏
        ('CloseProfitByTrade', ctypes.c_double),  # ///逐笔对冲平仓盈亏
        ('TodayPosition', ctypes.c_int),  # ///今日持仓
        ('MarginRateByMoney', ctypes.c_double),  # ///保证金率
        ('MarginRateByVolume', ctypes.c_double),  # ///保证金率(按手数)
        ('StrikeFrozen', ctypes.c_int),  # ///执行冻结
        ('StrikeFrozenAmount', ctypes.c_double),  # ///执行冻结金额
        ('AbandonFrozen', ctypes.c_int),  # ///放弃执行冻结
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('YdStrikeFrozen', ctypes.c_int),  # ///执行冻结的昨仓
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('PositionCostOffset', ctypes.c_double),  # ///持仓成本差值
        ('TasPosition', ctypes.c_int),  # ///tas持仓手数
        ('TasPositionCost', ctypes.c_double),  # ///tas持仓成本
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///正在同步中的合约保证金率
class SyncingInstrumentMarginRateField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('InvestorRange', ctypes.c_char * 1),  # ///投资者范围
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('LongMarginRatioByMoney', ctypes.c_double),  # ///多头保证金率
        ('LongMarginRatioByVolume', ctypes.c_double),  # ///多头保证金费
        ('ShortMarginRatioByMoney', ctypes.c_double),  # ///空头保证金率
        ('ShortMarginRatioByVolume', ctypes.c_double),  # ///空头保证金费
        ('IsRelative', ctypes.c_int),  # ///是否相对交易所收取
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///正在同步中的合约手续费率
class SyncingInstrumentCommissionRateField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('InvestorRange', ctypes.c_char * 1),  # ///投资者范围
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('OpenRatioByMoney', ctypes.c_double),  # ///开仓手续费率
        ('OpenRatioByVolume', ctypes.c_double),  # ///开仓手续费
        ('CloseRatioByMoney', ctypes.c_double),  # ///平仓手续费率
        ('CloseRatioByVolume', ctypes.c_double),  # ///平仓手续费
        ('CloseTodayRatioByMoney', ctypes.c_double),  # ///平今手续费率
        ('CloseTodayRatioByVolume', ctypes.c_double),  # ///平今手续费
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///正在同步中的合约交易权限
class SyncingInstrumentTradingRightField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('InvestorRange', ctypes.c_char * 1),  # ///投资者范围
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('TradingRight', ctypes.c_char * 1),  # ///交易权限
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///查询报单
class QryOrderField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('OrderSysID', ctypes.c_char * 21),  # ///报单编号
        ('InsertTimeStart', ctypes.c_char * 9),  # ///开始时间
        ('InsertTimeEnd', ctypes.c_char * 9),  # ///结束时间
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///查询成交
class QryTradeField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('TradeID', ctypes.c_char * 21),  # ///成交编号
        ('TradeTimeStart', ctypes.c_char * 9),  # ///开始时间
        ('TradeTimeEnd', ctypes.c_char * 9),  # ///结束时间
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///查询投资者持仓
class QryInvestorPositionField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///查询资金账户
class QryTradingAccountField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('BizType', ctypes.c_char * 1),  # ///业务类型
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
    ]


# ///查询投资者
class QryInvestorField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
    ]


# ///查询交易编码
class QryTradingCodeField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('ClientIDType', ctypes.c_char * 1),  # ///交易编码类型
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
    ]


# ///查询投资者组
class QryInvestorGroupField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
    ]


# ///查询合约保证金率
class QryInstrumentMarginRateField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///查询手续费率
class QryInstrumentCommissionRateField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///查询合约交易权限
class QryInstrumentTradingRightField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///查询经纪公司
class QryBrokerField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
    ]


# ///查询交易员
class QryTraderField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
    ]


# ///查询管理用户功能权限
class QrySuperUserFunctionField(BaseField):
    _fields_ = [
        ('UserID', ctypes.c_char * 16),  # ///用户代码
    ]


# ///查询用户会话
class QryUserSessionField(BaseField):
    _fields_ = [
        ('FrontID', ctypes.c_int),  # ///前置编号
        ('SessionID', ctypes.c_int),  # ///会话编号
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
    ]


# ///查询经纪公司会员代码
class QryPartBrokerField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
    ]


# ///查询前置状态
class QryFrontStatusField(BaseField):
    _fields_ = [
        ('FrontID', ctypes.c_int),  # ///前置编号
    ]


# ///查询交易所报单
class QryExchangeOrderField(BaseField):
    _fields_ = [
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
        ('ExchangeInstID', ctypes.c_char * 81),  # ///合约在交易所的代码
    ]


# ///查询报单操作
class QryOrderActionField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
    ]


# ///查询交易所报单操作
class QryExchangeOrderActionField(BaseField):
    _fields_ = [
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
    ]


# ///查询管理用户
class QrySuperUserField(BaseField):
    _fields_ = [
        ('UserID', ctypes.c_char * 16),  # ///用户代码
    ]


# ///查询交易所
class QryExchangeField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
    ]


# ///查询产品
class QryProductField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ProductClass', ctypes.c_char * 1),  # ///产品类型
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ProductID', ctypes.c_char * 81),  # ///产品代码
    ]


# ///查询合约
class QryInstrumentField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('reserve2', ctypes.c_char * 31),  # ///保留的无效字段
        ('reserve3', ctypes.c_char * 31),  # ///保留的无效字段
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('ExchangeInstID', ctypes.c_char * 81),  # ///合约在交易所的代码
        ('ProductID', ctypes.c_char * 81),  # ///产品代码
    ]


# ///查询行情
class QryDepthMarketDataField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///查询经纪公司用户
class QryBrokerUserField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
    ]


# ///查询经纪公司用户权限
class QryBrokerUserFunctionField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
    ]


# ///查询交易员报盘机
class QryTraderOfferField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
    ]


# ///查询出入金流水
class QrySyncDepositField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('DepositSeqNo', ctypes.c_char * 15),  # ///出入金流水号
    ]


# ///查询投资者结算结果
class QrySettlementInfoField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
    ]


# ///查询交易所保证金率
class QryExchangeMarginRateField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///查询交易所调整保证金率
class QryExchangeMarginRateAdjustField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///查询汇率
class QryExchangeRateField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('FromCurrencyID', ctypes.c_char * 4),  # ///源币种
        ('ToCurrencyID', ctypes.c_char * 4),  # ///目标币种
    ]


# ///查询货币质押流水
class QrySyncFundMortgageField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('MortgageSeqNo', ctypes.c_char * 15),  # ///货币质押流水号
    ]


# ///查询报单
class QryHisOrderField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('OrderSysID', ctypes.c_char * 21),  # ///报单编号
        ('InsertTimeStart', ctypes.c_char * 9),  # ///开始时间
        ('InsertTimeEnd', ctypes.c_char * 9),  # ///结束时间
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('SettlementID', ctypes.c_int),  # ///结算编号
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///当前期权合约最小保证金
class OptionInstrMiniMarginField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('InvestorRange', ctypes.c_char * 1),  # ///投资者范围
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('MinMargin', ctypes.c_double),  # ///单位（手）期权合约最小保证金
        ('ValueMethod', ctypes.c_char * 1),  # ///取值方式
        ('IsRelative', ctypes.c_int),  # ///是否跟随交易所收取
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///当前期权合约保证金调整系数
class OptionInstrMarginAdjustField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('InvestorRange', ctypes.c_char * 1),  # ///投资者范围
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('SShortMarginRatioByMoney', ctypes.c_double),  # ///投机空头保证金调整系数
        ('SShortMarginRatioByVolume', ctypes.c_double),  # ///投机空头保证金调整系数
        ('HShortMarginRatioByMoney', ctypes.c_double),  # ///保值空头保证金调整系数
        ('HShortMarginRatioByVolume', ctypes.c_double),  # ///保值空头保证金调整系数
        ('AShortMarginRatioByMoney', ctypes.c_double),  # ///套利空头保证金调整系数
        ('AShortMarginRatioByVolume', ctypes.c_double),  # ///套利空头保证金调整系数
        ('IsRelative', ctypes.c_int),  # ///是否跟随交易所收取
        ('MShortMarginRatioByMoney', ctypes.c_double),  # ///做市商空头保证金调整系数
        ('MShortMarginRatioByVolume', ctypes.c_double),  # ///做市商空头保证金调整系数
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///当前期权合约手续费的详细内容
class OptionInstrCommRateField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('InvestorRange', ctypes.c_char * 1),  # ///投资者范围
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('OpenRatioByMoney', ctypes.c_double),  # ///开仓手续费率
        ('OpenRatioByVolume', ctypes.c_double),  # ///开仓手续费
        ('CloseRatioByMoney', ctypes.c_double),  # ///平仓手续费率
        ('CloseRatioByVolume', ctypes.c_double),  # ///平仓手续费
        ('CloseTodayRatioByMoney', ctypes.c_double),  # ///平今手续费率
        ('CloseTodayRatioByVolume', ctypes.c_double),  # ///平今手续费
        ('StrikeRatioByMoney', ctypes.c_double),  # ///执行手续费率
        ('StrikeRatioByVolume', ctypes.c_double),  # ///执行手续费
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///期权交易成本
class OptionInstrTradeCostField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('FixedMargin', ctypes.c_double),  # ///期权合约保证金不变部分
        ('MiniMargin', ctypes.c_double),  # ///期权合约最小保证金
        ('Royalty', ctypes.c_double),  # ///期权合约权利金
        ('ExchFixedMargin', ctypes.c_double),  # ///交易所期权合约保证金不变部分
        ('ExchMiniMargin', ctypes.c_double),  # ///交易所期权合约最小保证金
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///期权交易成本查询
class QryOptionInstrTradeCostField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('InputPrice', ctypes.c_double),  # ///期权合约报价
        ('UnderlyingPrice', ctypes.c_double),  # ///标的价格,填0则用昨结算价
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///期权手续费率查询
class QryOptionInstrCommRateField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///股指现货指数
class IndexPriceField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ClosePrice', ctypes.c_double),  # ///指数现货收盘价
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///输入的执行宣告
class InputExecOrderField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ExecOrderRef', ctypes.c_char * 13),  # ///执行宣告引用
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('Volume', ctypes.c_int),  # ///数量
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('BusinessUnit', ctypes.c_char * 21),  # ///业务单元
        ('OffsetFlag', ctypes.c_char * 1),  # ///开平标志
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('ActionType', ctypes.c_char * 1),  # ///执行类型
        ('PosiDirection', ctypes.c_char * 1),  # ///保留头寸申请的持仓方向
        ('ReservePositionFlag', ctypes.c_char * 1),  # ///期权行权后是否保留期货头寸的标记,该字段已废弃
        ('CloseFlag', ctypes.c_char * 1),  # ///期权行权后生成的头寸是否自动平仓
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('AccountID', ctypes.c_char * 13),  # ///资金账号
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('ClientID', ctypes.c_char * 11),  # ///交易编码
        ('reserve2', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///输入执行宣告操作
class InputExecOrderActionField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('ExecOrderActionRef', ctypes.c_int),  # ///执行宣告操作引用
        ('ExecOrderRef', ctypes.c_char * 13),  # ///执行宣告引用
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('FrontID', ctypes.c_int),  # ///前置编号
        ('SessionID', ctypes.c_int),  # ///会话编号
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ExecOrderSysID', ctypes.c_char * 21),  # ///执行宣告操作编号
        ('ActionFlag', ctypes.c_char * 1),  # ///操作标志
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('reserve2', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///执行宣告
class ExecOrderField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ExecOrderRef', ctypes.c_char * 13),  # ///执行宣告引用
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('Volume', ctypes.c_int),  # ///数量
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('BusinessUnit', ctypes.c_char * 21),  # ///业务单元
        ('OffsetFlag', ctypes.c_char * 1),  # ///开平标志
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('ActionType', ctypes.c_char * 1),  # ///执行类型
        ('PosiDirection', ctypes.c_char * 1),  # ///保留头寸申请的持仓方向
        ('ReservePositionFlag', ctypes.c_char * 1),  # ///期权行权后是否保留期货头寸的标记,该字段已废弃
        ('CloseFlag', ctypes.c_char * 1),  # ///期权行权后生成的头寸是否自动平仓
        ('ExecOrderLocalID', ctypes.c_char * 13),  # ///本地执行宣告编号
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('reserve2', ctypes.c_char * 31),  # ///保留的无效字段
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('OrderSubmitStatus', ctypes.c_char * 1),  # ///执行宣告提交状态
        ('NotifySequence', ctypes.c_int),  # ///报单提示序号
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('SettlementID', ctypes.c_int),  # ///结算编号
        ('ExecOrderSysID', ctypes.c_char * 21),  # ///执行宣告编号
        ('InsertDate', ctypes.c_char * 9),  # ///报单日期
        ('InsertTime', ctypes.c_char * 9),  # ///插入时间
        ('CancelTime', ctypes.c_char * 9),  # ///撤销时间
        ('ExecResult', ctypes.c_char * 1),  # ///执行结果
        ('ClearingPartID', ctypes.c_char * 11),  # ///结算会员编号
        ('SequenceNo', ctypes.c_int),  # ///序号
        ('FrontID', ctypes.c_int),  # ///前置编号
        ('SessionID', ctypes.c_int),  # ///会话编号
        ('UserProductInfo', ctypes.c_char * 11),  # ///用户端产品信息
        ('StatusMsg', ctypes.c_char * 81),  # ///状态信息
        ('ActiveUserID', ctypes.c_char * 16),  # ///操作用户代码
        ('BrokerExecOrderSeq', ctypes.c_int),  # ///经纪公司报单编号
        ('BranchID', ctypes.c_char * 9),  # ///营业部编号
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('AccountID', ctypes.c_char * 13),  # ///资金账号
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('reserve3', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('ExchangeInstID', ctypes.c_char * 81),  # ///合约在交易所的代码
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///执行宣告操作
class ExecOrderActionField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('ExecOrderActionRef', ctypes.c_int),  # ///执行宣告操作引用
        ('ExecOrderRef', ctypes.c_char * 13),  # ///执行宣告引用
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('FrontID', ctypes.c_int),  # ///前置编号
        ('SessionID', ctypes.c_int),  # ///会话编号
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ExecOrderSysID', ctypes.c_char * 21),  # ///执行宣告操作编号
        ('ActionFlag', ctypes.c_char * 1),  # ///操作标志
        ('ActionDate', ctypes.c_char * 9),  # ///操作日期
        ('ActionTime', ctypes.c_char * 9),  # ///操作时间
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('ExecOrderLocalID', ctypes.c_char * 13),  # ///本地执行宣告编号
        ('ActionLocalID', ctypes.c_char * 13),  # ///操作本地编号
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('BusinessUnit', ctypes.c_char * 21),  # ///业务单元
        ('OrderActionStatus', ctypes.c_char * 1),  # ///报单操作状态
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('ActionType', ctypes.c_char * 1),  # ///执行类型
        ('StatusMsg', ctypes.c_char * 81),  # ///状态信息
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('BranchID', ctypes.c_char * 9),  # ///营业部编号
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('reserve2', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///执行宣告查询
class QryExecOrderField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ExecOrderSysID', ctypes.c_char * 21),  # ///执行宣告编号
        ('InsertTimeStart', ctypes.c_char * 9),  # ///开始时间
        ('InsertTimeEnd', ctypes.c_char * 9),  # ///结束时间
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///交易所执行宣告信息
class ExchangeExecOrderField(BaseField):
    _fields_ = [
        ('Volume', ctypes.c_int),  # ///数量
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('BusinessUnit', ctypes.c_char * 21),  # ///业务单元
        ('OffsetFlag', ctypes.c_char * 1),  # ///开平标志
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('ActionType', ctypes.c_char * 1),  # ///执行类型
        ('PosiDirection', ctypes.c_char * 1),  # ///保留头寸申请的持仓方向
        ('ReservePositionFlag', ctypes.c_char * 1),  # ///期权行权后是否保留期货头寸的标记,该字段已废弃
        ('CloseFlag', ctypes.c_char * 1),  # ///期权行权后生成的头寸是否自动平仓
        ('ExecOrderLocalID', ctypes.c_char * 13),  # ///本地执行宣告编号
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('OrderSubmitStatus', ctypes.c_char * 1),  # ///执行宣告提交状态
        ('NotifySequence', ctypes.c_int),  # ///报单提示序号
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('SettlementID', ctypes.c_int),  # ///结算编号
        ('ExecOrderSysID', ctypes.c_char * 21),  # ///执行宣告编号
        ('InsertDate', ctypes.c_char * 9),  # ///报单日期
        ('InsertTime', ctypes.c_char * 9),  # ///插入时间
        ('CancelTime', ctypes.c_char * 9),  # ///撤销时间
        ('ExecResult', ctypes.c_char * 1),  # ///执行结果
        ('ClearingPartID', ctypes.c_char * 11),  # ///结算会员编号
        ('SequenceNo', ctypes.c_int),  # ///序号
        ('BranchID', ctypes.c_char * 9),  # ///营业部编号
        ('reserve2', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('ExchangeInstID', ctypes.c_char * 81),  # ///合约在交易所的代码
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///交易所执行宣告查询
class QryExchangeExecOrderField(BaseField):
    _fields_ = [
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
        ('ExchangeInstID', ctypes.c_char * 81),  # ///合约在交易所的代码
    ]


# ///执行宣告操作查询
class QryExecOrderActionField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
    ]


# ///交易所执行宣告操作
class ExchangeExecOrderActionField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ExecOrderSysID', ctypes.c_char * 21),  # ///执行宣告操作编号
        ('ActionFlag', ctypes.c_char * 1),  # ///操作标志
        ('ActionDate', ctypes.c_char * 9),  # ///操作日期
        ('ActionTime', ctypes.c_char * 9),  # ///操作时间
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('ExecOrderLocalID', ctypes.c_char * 13),  # ///本地执行宣告编号
        ('ActionLocalID', ctypes.c_char * 13),  # ///操作本地编号
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('BusinessUnit', ctypes.c_char * 21),  # ///业务单元
        ('OrderActionStatus', ctypes.c_char * 1),  # ///报单操作状态
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('ActionType', ctypes.c_char * 1),  # ///执行类型
        ('BranchID', ctypes.c_char * 9),  # ///营业部编号
        ('reserve1', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('reserve2', ctypes.c_char * 31),  # ///保留的无效字段
        ('Volume', ctypes.c_int),  # ///数量
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
        ('ExchangeInstID', ctypes.c_char * 81),  # ///合约在交易所的代码
    ]


# ///交易所执行宣告操作查询
class QryExchangeExecOrderActionField(BaseField):
    _fields_ = [
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
    ]


# ///错误执行宣告
class ErrExecOrderField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ExecOrderRef', ctypes.c_char * 13),  # ///执行宣告引用
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('Volume', ctypes.c_int),  # ///数量
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('BusinessUnit', ctypes.c_char * 21),  # ///业务单元
        ('OffsetFlag', ctypes.c_char * 1),  # ///开平标志
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('ActionType', ctypes.c_char * 1),  # ///执行类型
        ('PosiDirection', ctypes.c_char * 1),  # ///保留头寸申请的持仓方向
        ('ReservePositionFlag', ctypes.c_char * 1),  # ///期权行权后是否保留期货头寸的标记,该字段已废弃
        ('CloseFlag', ctypes.c_char * 1),  # ///期权行权后生成的头寸是否自动平仓
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('AccountID', ctypes.c_char * 13),  # ///资金账号
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('ClientID', ctypes.c_char * 11),  # ///交易编码
        ('reserve2', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('ErrorID', ctypes.c_int),  # ///错误代码
        ('ErrorMsg', ctypes.c_char * 81),  # ///错误信息
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///查询错误执行宣告
class QryErrExecOrderField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
    ]


# ///错误执行宣告操作
class ErrExecOrderActionField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('ExecOrderActionRef', ctypes.c_int),  # ///执行宣告操作引用
        ('ExecOrderRef', ctypes.c_char * 13),  # ///执行宣告引用
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('FrontID', ctypes.c_int),  # ///前置编号
        ('SessionID', ctypes.c_int),  # ///会话编号
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ExecOrderSysID', ctypes.c_char * 21),  # ///执行宣告操作编号
        ('ActionFlag', ctypes.c_char * 1),  # ///操作标志
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('reserve2', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('ErrorID', ctypes.c_int),  # ///错误代码
        ('ErrorMsg', ctypes.c_char * 81),  # ///错误信息
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///查询错误执行宣告操作
class QryErrExecOrderActionField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
    ]


# ///投资者期权合约交易权限
class OptionInstrTradingRightField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('InvestorRange', ctypes.c_char * 1),  # ///投资者范围
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('Direction', ctypes.c_char * 1),  # ///买卖方向
        ('TradingRight', ctypes.c_char * 1),  # ///交易权限
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///查询期权合约交易权限
class QryOptionInstrTradingRightField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('Direction', ctypes.c_char * 1),  # ///买卖方向
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///输入的询价
class InputForQuoteField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ForQuoteRef', ctypes.c_char * 13),  # ///询价引用
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('reserve2', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///询价
class ForQuoteField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ForQuoteRef', ctypes.c_char * 13),  # ///询价引用
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('ForQuoteLocalID', ctypes.c_char * 13),  # ///本地询价编号
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('reserve2', ctypes.c_char * 31),  # ///保留的无效字段
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('InsertDate', ctypes.c_char * 9),  # ///报单日期
        ('InsertTime', ctypes.c_char * 9),  # ///插入时间
        ('ForQuoteStatus', ctypes.c_char * 1),  # ///询价状态
        ('FrontID', ctypes.c_int),  # ///前置编号
        ('SessionID', ctypes.c_int),  # ///会话编号
        ('StatusMsg', ctypes.c_char * 81),  # ///状态信息
        ('ActiveUserID', ctypes.c_char * 16),  # ///操作用户代码
        ('BrokerForQutoSeq', ctypes.c_int),  # ///经纪公司询价编号
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('reserve3', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('ExchangeInstID', ctypes.c_char * 81),  # ///合约在交易所的代码
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///询价查询
class QryForQuoteField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InsertTimeStart', ctypes.c_char * 9),  # ///开始时间
        ('InsertTimeEnd', ctypes.c_char * 9),  # ///结束时间
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///交易所询价信息
class ExchangeForQuoteField(BaseField):
    _fields_ = [
        ('ForQuoteLocalID', ctypes.c_char * 13),  # ///本地询价编号
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('InsertDate', ctypes.c_char * 9),  # ///报单日期
        ('InsertTime', ctypes.c_char * 9),  # ///插入时间
        ('ForQuoteStatus', ctypes.c_char * 1),  # ///询价状态
        ('reserve2', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('ExchangeInstID', ctypes.c_char * 81),  # ///合约在交易所的代码
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///交易所询价查询
class QryExchangeForQuoteField(BaseField):
    _fields_ = [
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
        ('ExchangeInstID', ctypes.c_char * 81),  # ///合约在交易所的代码
    ]


# ///输入的报价
class InputQuoteField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('QuoteRef', ctypes.c_char * 13),  # ///报价引用
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('AskPrice', ctypes.c_double),  # ///卖价格
        ('BidPrice', ctypes.c_double),  # ///买价格
        ('AskVolume', ctypes.c_int),  # ///卖数量
        ('BidVolume', ctypes.c_int),  # ///买数量
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('BusinessUnit', ctypes.c_char * 21),  # ///业务单元
        ('AskOffsetFlag', ctypes.c_char * 1),  # ///卖开平标志
        ('BidOffsetFlag', ctypes.c_char * 1),  # ///买开平标志
        ('AskHedgeFlag', ctypes.c_char * 1),  # ///卖投机套保标志
        ('BidHedgeFlag', ctypes.c_char * 1),  # ///买投机套保标志
        ('AskOrderRef', ctypes.c_char * 13),  # ///衍生卖报单引用
        ('BidOrderRef', ctypes.c_char * 13),  # ///衍生买报单引用
        ('ForQuoteSysID', ctypes.c_char * 21),  # ///应价编号
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('ClientID', ctypes.c_char * 11),  # ///交易编码
        ('reserve2', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
        ('ReplaceSysID', ctypes.c_char * 21),  # ///被顶单编号
    ]


# ///输入报价操作
class InputQuoteActionField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('QuoteActionRef', ctypes.c_int),  # ///报价操作引用
        ('QuoteRef', ctypes.c_char * 13),  # ///报价引用
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('FrontID', ctypes.c_int),  # ///前置编号
        ('SessionID', ctypes.c_int),  # ///会话编号
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('QuoteSysID', ctypes.c_char * 21),  # ///报价操作编号
        ('ActionFlag', ctypes.c_char * 1),  # ///操作标志
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('ClientID', ctypes.c_char * 11),  # ///交易编码
        ('reserve2', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///报价
class QuoteField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('QuoteRef', ctypes.c_char * 13),  # ///报价引用
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('AskPrice', ctypes.c_double),  # ///卖价格
        ('BidPrice', ctypes.c_double),  # ///买价格
        ('AskVolume', ctypes.c_int),  # ///卖数量
        ('BidVolume', ctypes.c_int),  # ///买数量
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('BusinessUnit', ctypes.c_char * 21),  # ///业务单元
        ('AskOffsetFlag', ctypes.c_char * 1),  # ///卖开平标志
        ('BidOffsetFlag', ctypes.c_char * 1),  # ///买开平标志
        ('AskHedgeFlag', ctypes.c_char * 1),  # ///卖投机套保标志
        ('BidHedgeFlag', ctypes.c_char * 1),  # ///买投机套保标志
        ('QuoteLocalID', ctypes.c_char * 13),  # ///本地报价编号
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('reserve2', ctypes.c_char * 31),  # ///保留的无效字段
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('NotifySequence', ctypes.c_int),  # ///报价提示序号
        ('OrderSubmitStatus', ctypes.c_char * 1),  # ///报价提交状态
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('SettlementID', ctypes.c_int),  # ///结算编号
        ('QuoteSysID', ctypes.c_char * 21),  # ///报价编号
        ('InsertDate', ctypes.c_char * 9),  # ///报单日期
        ('InsertTime', ctypes.c_char * 9),  # ///插入时间
        ('CancelTime', ctypes.c_char * 9),  # ///撤销时间
        ('QuoteStatus', ctypes.c_char * 1),  # ///报价状态
        ('ClearingPartID', ctypes.c_char * 11),  # ///结算会员编号
        ('SequenceNo', ctypes.c_int),  # ///序号
        ('AskOrderSysID', ctypes.c_char * 21),  # ///卖方报单编号
        ('BidOrderSysID', ctypes.c_char * 21),  # ///买方报单编号
        ('FrontID', ctypes.c_int),  # ///前置编号
        ('SessionID', ctypes.c_int),  # ///会话编号
        ('UserProductInfo', ctypes.c_char * 11),  # ///用户端产品信息
        ('StatusMsg', ctypes.c_char * 81),  # ///状态信息
        ('ActiveUserID', ctypes.c_char * 16),  # ///操作用户代码
        ('BrokerQuoteSeq', ctypes.c_int),  # ///经纪公司报价编号
        ('AskOrderRef', ctypes.c_char * 13),  # ///衍生卖报单引用
        ('BidOrderRef', ctypes.c_char * 13),  # ///衍生买报单引用
        ('ForQuoteSysID', ctypes.c_char * 21),  # ///应价编号
        ('BranchID', ctypes.c_char * 9),  # ///营业部编号
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('AccountID', ctypes.c_char * 13),  # ///资金账号
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('reserve3', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('ExchangeInstID', ctypes.c_char * 81),  # ///合约在交易所的代码
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
        ('ReplaceSysID', ctypes.c_char * 21),  # ///被顶单编号
    ]


# ///报价操作
class QuoteActionField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('QuoteActionRef', ctypes.c_int),  # ///报价操作引用
        ('QuoteRef', ctypes.c_char * 13),  # ///报价引用
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('FrontID', ctypes.c_int),  # ///前置编号
        ('SessionID', ctypes.c_int),  # ///会话编号
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('QuoteSysID', ctypes.c_char * 21),  # ///报价操作编号
        ('ActionFlag', ctypes.c_char * 1),  # ///操作标志
        ('ActionDate', ctypes.c_char * 9),  # ///操作日期
        ('ActionTime', ctypes.c_char * 9),  # ///操作时间
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('QuoteLocalID', ctypes.c_char * 13),  # ///本地报价编号
        ('ActionLocalID', ctypes.c_char * 13),  # ///操作本地编号
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('BusinessUnit', ctypes.c_char * 21),  # ///业务单元
        ('OrderActionStatus', ctypes.c_char * 1),  # ///报单操作状态
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('StatusMsg', ctypes.c_char * 81),  # ///状态信息
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('BranchID', ctypes.c_char * 9),  # ///营业部编号
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('reserve2', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///报价查询
class QryQuoteField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('QuoteSysID', ctypes.c_char * 21),  # ///报价编号
        ('InsertTimeStart', ctypes.c_char * 9),  # ///开始时间
        ('InsertTimeEnd', ctypes.c_char * 9),  # ///结束时间
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///交易所报价信息
class ExchangeQuoteField(BaseField):
    _fields_ = [
        ('AskPrice', ctypes.c_double),  # ///卖价格
        ('BidPrice', ctypes.c_double),  # ///买价格
        ('AskVolume', ctypes.c_int),  # ///卖数量
        ('BidVolume', ctypes.c_int),  # ///买数量
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('BusinessUnit', ctypes.c_char * 21),  # ///业务单元
        ('AskOffsetFlag', ctypes.c_char * 1),  # ///卖开平标志
        ('BidOffsetFlag', ctypes.c_char * 1),  # ///买开平标志
        ('AskHedgeFlag', ctypes.c_char * 1),  # ///卖投机套保标志
        ('BidHedgeFlag', ctypes.c_char * 1),  # ///买投机套保标志
        ('QuoteLocalID', ctypes.c_char * 13),  # ///本地报价编号
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('NotifySequence', ctypes.c_int),  # ///报价提示序号
        ('OrderSubmitStatus', ctypes.c_char * 1),  # ///报价提交状态
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('SettlementID', ctypes.c_int),  # ///结算编号
        ('QuoteSysID', ctypes.c_char * 21),  # ///报价编号
        ('InsertDate', ctypes.c_char * 9),  # ///报单日期
        ('InsertTime', ctypes.c_char * 9),  # ///插入时间
        ('CancelTime', ctypes.c_char * 9),  # ///撤销时间
        ('QuoteStatus', ctypes.c_char * 1),  # ///报价状态
        ('ClearingPartID', ctypes.c_char * 11),  # ///结算会员编号
        ('SequenceNo', ctypes.c_int),  # ///序号
        ('AskOrderSysID', ctypes.c_char * 21),  # ///卖方报单编号
        ('BidOrderSysID', ctypes.c_char * 21),  # ///买方报单编号
        ('ForQuoteSysID', ctypes.c_char * 21),  # ///应价编号
        ('BranchID', ctypes.c_char * 9),  # ///营业部编号
        ('reserve2', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('ExchangeInstID', ctypes.c_char * 81),  # ///合约在交易所的代码
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///交易所报价查询
class QryExchangeQuoteField(BaseField):
    _fields_ = [
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
        ('ExchangeInstID', ctypes.c_char * 81),  # ///合约在交易所的代码
    ]


# ///报价操作查询
class QryQuoteActionField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
    ]


# ///交易所报价操作
class ExchangeQuoteActionField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('QuoteSysID', ctypes.c_char * 21),  # ///报价操作编号
        ('ActionFlag', ctypes.c_char * 1),  # ///操作标志
        ('ActionDate', ctypes.c_char * 9),  # ///操作日期
        ('ActionTime', ctypes.c_char * 9),  # ///操作时间
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('QuoteLocalID', ctypes.c_char * 13),  # ///本地报价编号
        ('ActionLocalID', ctypes.c_char * 13),  # ///操作本地编号
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('BusinessUnit', ctypes.c_char * 21),  # ///业务单元
        ('OrderActionStatus', ctypes.c_char * 1),  # ///报单操作状态
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('reserve1', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///交易所报价操作查询
class QryExchangeQuoteActionField(BaseField):
    _fields_ = [
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
    ]


# ///期权合约delta值
class OptionInstrDeltaField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('InvestorRange', ctypes.c_char * 1),  # ///投资者范围
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('Delta', ctypes.c_double),  # ///Delta值
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///发给做市商的询价请求
class ForQuoteRspField(BaseField):
    _fields_ = [
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ForQuoteSysID', ctypes.c_char * 21),  # ///询价编号
        ('ForQuoteTime', ctypes.c_char * 9),  # ///询价时间
        ('ActionDay', ctypes.c_char * 9),  # ///业务日期
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///当前期权合约执行偏移值的详细内容
class StrikeOffsetField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('InvestorRange', ctypes.c_char * 1),  # ///投资者范围
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('Offset', ctypes.c_double),  # ///执行偏移值
        ('OffsetType', ctypes.c_char * 1),  # ///执行偏移类型
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///期权执行偏移值查询
class QryStrikeOffsetField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///输入批量报单操作
class InputBatchOrderActionField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('OrderActionRef', ctypes.c_int),  # ///报单操作引用
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('FrontID', ctypes.c_int),  # ///前置编号
        ('SessionID', ctypes.c_int),  # ///会话编号
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('reserve1', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///批量报单操作
class BatchOrderActionField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('OrderActionRef', ctypes.c_int),  # ///报单操作引用
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('FrontID', ctypes.c_int),  # ///前置编号
        ('SessionID', ctypes.c_int),  # ///会话编号
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ActionDate', ctypes.c_char * 9),  # ///操作日期
        ('ActionTime', ctypes.c_char * 9),  # ///操作时间
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('ActionLocalID', ctypes.c_char * 13),  # ///操作本地编号
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('BusinessUnit', ctypes.c_char * 21),  # ///业务单元
        ('OrderActionStatus', ctypes.c_char * 1),  # ///报单操作状态
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('StatusMsg', ctypes.c_char * 81),  # ///状态信息
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('reserve1', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///交易所批量报单操作
class ExchangeBatchOrderActionField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ActionDate', ctypes.c_char * 9),  # ///操作日期
        ('ActionTime', ctypes.c_char * 9),  # ///操作时间
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('ActionLocalID', ctypes.c_char * 13),  # ///操作本地编号
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('BusinessUnit', ctypes.c_char * 21),  # ///业务单元
        ('OrderActionStatus', ctypes.c_char * 1),  # ///报单操作状态
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('reserve1', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///查询批量报单操作
class QryBatchOrderActionField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
    ]


# ///组合合约安全系数
class CombInstrumentGuardField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('GuarantRatio', ctypes.c_double),  # ///
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///组合合约安全系数查询
class QryCombInstrumentGuardField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///输入的申请组合
class InputCombActionField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('CombActionRef', ctypes.c_char * 13),  # ///组合引用
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('Direction', ctypes.c_char * 1),  # ///买卖方向
        ('Volume', ctypes.c_int),  # ///数量
        ('CombDirection', ctypes.c_char * 1),  # ///组合指令方向
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('reserve2', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('FrontID', ctypes.c_int),  # ///前置编号
        ('SessionID', ctypes.c_int),  # ///会话编号
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///申请组合
class CombActionField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('CombActionRef', ctypes.c_char * 13),  # ///组合引用
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('Direction', ctypes.c_char * 1),  # ///买卖方向
        ('Volume', ctypes.c_int),  # ///数量
        ('CombDirection', ctypes.c_char * 1),  # ///组合指令方向
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('ActionLocalID', ctypes.c_char * 13),  # ///本地申请组合编号
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('reserve2', ctypes.c_char * 31),  # ///保留的无效字段
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('ActionStatus', ctypes.c_char * 1),  # ///组合状态
        ('NotifySequence', ctypes.c_int),  # ///报单提示序号
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('SettlementID', ctypes.c_int),  # ///结算编号
        ('SequenceNo', ctypes.c_int),  # ///序号
        ('FrontID', ctypes.c_int),  # ///前置编号
        ('SessionID', ctypes.c_int),  # ///会话编号
        ('UserProductInfo', ctypes.c_char * 11),  # ///用户端产品信息
        ('StatusMsg', ctypes.c_char * 81),  # ///状态信息
        ('reserve3', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('ComTradeID', ctypes.c_char * 21),  # ///组合编号
        ('BranchID', ctypes.c_char * 9),  # ///营业部编号
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('ExchangeInstID', ctypes.c_char * 81),  # ///合约在交易所的代码
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///申请组合查询
class QryCombActionField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///交易所申请组合信息
class ExchangeCombActionField(BaseField):
    _fields_ = [
        ('Direction', ctypes.c_char * 1),  # ///买卖方向
        ('Volume', ctypes.c_int),  # ///数量
        ('CombDirection', ctypes.c_char * 1),  # ///组合指令方向
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('ActionLocalID', ctypes.c_char * 13),  # ///本地申请组合编号
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('ActionStatus', ctypes.c_char * 1),  # ///组合状态
        ('NotifySequence', ctypes.c_int),  # ///报单提示序号
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('SettlementID', ctypes.c_int),  # ///结算编号
        ('SequenceNo', ctypes.c_int),  # ///序号
        ('reserve2', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('ComTradeID', ctypes.c_char * 21),  # ///组合编号
        ('BranchID', ctypes.c_char * 9),  # ///营业部编号
        ('ExchangeInstID', ctypes.c_char * 81),  # ///合约在交易所的代码
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///交易所申请组合查询
class QryExchangeCombActionField(BaseField):
    _fields_ = [
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
        ('ExchangeInstID', ctypes.c_char * 81),  # ///合约在交易所的代码
    ]


# ///产品报价汇率
class ProductExchRateField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('QuoteCurrencyID', ctypes.c_char * 4),  # ///报价币种类型
        ('ExchangeRate', ctypes.c_double),  # ///汇率
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ProductID', ctypes.c_char * 81),  # ///产品代码
    ]


# ///产品报价汇率查询
class QryProductExchRateField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ProductID', ctypes.c_char * 81),  # ///产品代码
    ]


# ///查询询价价差参数
class QryForQuoteParamField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///询价价差参数
class ForQuoteParamField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('LastPrice', ctypes.c_double),  # ///最新价
        ('PriceInterval', ctypes.c_double),  # ///价差
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///当前做市商期权合约手续费的详细内容
class MMOptionInstrCommRateField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('InvestorRange', ctypes.c_char * 1),  # ///投资者范围
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('OpenRatioByMoney', ctypes.c_double),  # ///开仓手续费率
        ('OpenRatioByVolume', ctypes.c_double),  # ///开仓手续费
        ('CloseRatioByMoney', ctypes.c_double),  # ///平仓手续费率
        ('CloseRatioByVolume', ctypes.c_double),  # ///平仓手续费
        ('CloseTodayRatioByMoney', ctypes.c_double),  # ///平今手续费率
        ('CloseTodayRatioByVolume', ctypes.c_double),  # ///平今手续费
        ('StrikeRatioByMoney', ctypes.c_double),  # ///执行手续费率
        ('StrikeRatioByVolume', ctypes.c_double),  # ///执行手续费
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///做市商期权手续费率查询
class QryMMOptionInstrCommRateField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///做市商合约手续费率
class MMInstrumentCommissionRateField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('InvestorRange', ctypes.c_char * 1),  # ///投资者范围
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('OpenRatioByMoney', ctypes.c_double),  # ///开仓手续费率
        ('OpenRatioByVolume', ctypes.c_double),  # ///开仓手续费
        ('CloseRatioByMoney', ctypes.c_double),  # ///平仓手续费率
        ('CloseRatioByVolume', ctypes.c_double),  # ///平仓手续费
        ('CloseTodayRatioByMoney', ctypes.c_double),  # ///平今手续费率
        ('CloseTodayRatioByVolume', ctypes.c_double),  # ///平今手续费
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///查询做市商合约手续费率
class QryMMInstrumentCommissionRateField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///当前报单手续费的详细内容
class InstrumentOrderCommRateField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('InvestorRange', ctypes.c_char * 1),  # ///投资者范围
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('OrderCommByVolume', ctypes.c_double),  # ///报单手续费
        ('OrderActionCommByVolume', ctypes.c_double),  # ///撤单手续费
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('OrderCommByTrade', ctypes.c_double),  # ///报单手续费
        ('OrderActionCommByTrade', ctypes.c_double),  # ///撤单手续费
    ]


# ///报单手续费率查询
class QryInstrumentOrderCommRateField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///交易参数
class TradeParamField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('TradeParamID', ctypes.c_char * 1),  # ///参数代码
        ('TradeParamValue', ctypes.c_char * 256),  # ///参数代码值
        ('Memo', ctypes.c_char * 161),  # ///备注
    ]


# ///合约保证金率调整
class InstrumentMarginRateULField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('InvestorRange', ctypes.c_char * 1),  # ///投资者范围
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('LongMarginRatioByMoney', ctypes.c_double),  # ///多头保证金率
        ('LongMarginRatioByVolume', ctypes.c_double),  # ///多头保证金费
        ('ShortMarginRatioByMoney', ctypes.c_double),  # ///空头保证金率
        ('ShortMarginRatioByVolume', ctypes.c_double),  # ///空头保证金费
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///期货持仓限制参数
class FutureLimitPosiParamField(BaseField):
    _fields_ = [
        ('InvestorRange', ctypes.c_char * 1),  # ///投资者范围
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('SpecOpenVolume', ctypes.c_int),  # ///当日投机开仓数量限制
        ('ArbiOpenVolume', ctypes.c_int),  # ///当日套利开仓数量限制
        ('OpenVolume', ctypes.c_int),  # ///当日投机+套利开仓数量限制
        ('ProductID', ctypes.c_char * 81),  # ///产品代码
    ]


# ///禁止登录IP
class LoginForbiddenIPField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 16),  # ///保留的无效字段
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///IP列表
class IPListField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 16),  # ///保留的无效字段
        ('IsWhite', ctypes.c_int),  # ///是否白名单
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///输入的期权自对冲
class InputOptionSelfCloseField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('OptionSelfCloseRef', ctypes.c_char * 13),  # ///期权自对冲引用
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('Volume', ctypes.c_int),  # ///数量
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('BusinessUnit', ctypes.c_char * 21),  # ///业务单元
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('OptSelfCloseFlag', ctypes.c_char * 1),  # ///期权行权的头寸是否自对冲
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('AccountID', ctypes.c_char * 13),  # ///资金账号
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('ClientID', ctypes.c_char * 11),  # ///交易编码
        ('reserve2', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///输入期权自对冲操作
class InputOptionSelfCloseActionField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('OptionSelfCloseActionRef', ctypes.c_int),  # ///期权自对冲操作引用
        ('OptionSelfCloseRef', ctypes.c_char * 13),  # ///期权自对冲引用
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('FrontID', ctypes.c_int),  # ///前置编号
        ('SessionID', ctypes.c_int),  # ///会话编号
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('OptionSelfCloseSysID', ctypes.c_char * 21),  # ///期权自对冲操作编号
        ('ActionFlag', ctypes.c_char * 1),  # ///操作标志
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('reserve2', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///期权自对冲
class OptionSelfCloseField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('OptionSelfCloseRef', ctypes.c_char * 13),  # ///期权自对冲引用
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('Volume', ctypes.c_int),  # ///数量
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('BusinessUnit', ctypes.c_char * 21),  # ///业务单元
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('OptSelfCloseFlag', ctypes.c_char * 1),  # ///期权行权的头寸是否自对冲
        ('OptionSelfCloseLocalID', ctypes.c_char * 13),  # ///本地期权自对冲编号
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('reserve2', ctypes.c_char * 31),  # ///保留的无效字段
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('OrderSubmitStatus', ctypes.c_char * 1),  # ///期权自对冲提交状态
        ('NotifySequence', ctypes.c_int),  # ///报单提示序号
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('SettlementID', ctypes.c_int),  # ///结算编号
        ('OptionSelfCloseSysID', ctypes.c_char * 21),  # ///期权自对冲编号
        ('InsertDate', ctypes.c_char * 9),  # ///报单日期
        ('InsertTime', ctypes.c_char * 9),  # ///插入时间
        ('CancelTime', ctypes.c_char * 9),  # ///撤销时间
        ('ExecResult', ctypes.c_char * 1),  # ///自对冲结果
        ('ClearingPartID', ctypes.c_char * 11),  # ///结算会员编号
        ('SequenceNo', ctypes.c_int),  # ///序号
        ('FrontID', ctypes.c_int),  # ///前置编号
        ('SessionID', ctypes.c_int),  # ///会话编号
        ('UserProductInfo', ctypes.c_char * 11),  # ///用户端产品信息
        ('StatusMsg', ctypes.c_char * 81),  # ///状态信息
        ('ActiveUserID', ctypes.c_char * 16),  # ///操作用户代码
        ('BrokerOptionSelfCloseSeq', ctypes.c_int),  # ///经纪公司报单编号
        ('BranchID', ctypes.c_char * 9),  # ///营业部编号
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('AccountID', ctypes.c_char * 13),  # ///资金账号
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('reserve3', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('ExchangeInstID', ctypes.c_char * 81),  # ///合约在交易所的代码
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///期权自对冲操作
class OptionSelfCloseActionField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('OptionSelfCloseActionRef', ctypes.c_int),  # ///期权自对冲操作引用
        ('OptionSelfCloseRef', ctypes.c_char * 13),  # ///期权自对冲引用
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('FrontID', ctypes.c_int),  # ///前置编号
        ('SessionID', ctypes.c_int),  # ///会话编号
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('OptionSelfCloseSysID', ctypes.c_char * 21),  # ///期权自对冲操作编号
        ('ActionFlag', ctypes.c_char * 1),  # ///操作标志
        ('ActionDate', ctypes.c_char * 9),  # ///操作日期
        ('ActionTime', ctypes.c_char * 9),  # ///操作时间
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('OptionSelfCloseLocalID', ctypes.c_char * 13),  # ///本地期权自对冲编号
        ('ActionLocalID', ctypes.c_char * 13),  # ///操作本地编号
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('BusinessUnit', ctypes.c_char * 21),  # ///业务单元
        ('OrderActionStatus', ctypes.c_char * 1),  # ///报单操作状态
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('StatusMsg', ctypes.c_char * 81),  # ///状态信息
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('BranchID', ctypes.c_char * 9),  # ///营业部编号
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('reserve2', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///期权自对冲查询
class QryOptionSelfCloseField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('OptionSelfCloseSysID', ctypes.c_char * 21),  # ///期权自对冲编号
        ('InsertTimeStart', ctypes.c_char * 9),  # ///开始时间
        ('InsertTimeEnd', ctypes.c_char * 9),  # ///结束时间
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///交易所期权自对冲信息
class ExchangeOptionSelfCloseField(BaseField):
    _fields_ = [
        ('Volume', ctypes.c_int),  # ///数量
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('BusinessUnit', ctypes.c_char * 21),  # ///业务单元
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('OptSelfCloseFlag', ctypes.c_char * 1),  # ///期权行权的头寸是否自对冲
        ('OptionSelfCloseLocalID', ctypes.c_char * 13),  # ///本地期权自对冲编号
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('OrderSubmitStatus', ctypes.c_char * 1),  # ///期权自对冲提交状态
        ('NotifySequence', ctypes.c_int),  # ///报单提示序号
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('SettlementID', ctypes.c_int),  # ///结算编号
        ('OptionSelfCloseSysID', ctypes.c_char * 21),  # ///期权自对冲编号
        ('InsertDate', ctypes.c_char * 9),  # ///报单日期
        ('InsertTime', ctypes.c_char * 9),  # ///插入时间
        ('CancelTime', ctypes.c_char * 9),  # ///撤销时间
        ('ExecResult', ctypes.c_char * 1),  # ///自对冲结果
        ('ClearingPartID', ctypes.c_char * 11),  # ///结算会员编号
        ('SequenceNo', ctypes.c_int),  # ///序号
        ('BranchID', ctypes.c_char * 9),  # ///营业部编号
        ('reserve2', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('ExchangeInstID', ctypes.c_char * 81),  # ///合约在交易所的代码
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///期权自对冲操作查询
class QryOptionSelfCloseActionField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
    ]


# ///交易所期权自对冲操作
class ExchangeOptionSelfCloseActionField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('OptionSelfCloseSysID', ctypes.c_char * 21),  # ///期权自对冲操作编号
        ('ActionFlag', ctypes.c_char * 1),  # ///操作标志
        ('ActionDate', ctypes.c_char * 9),  # ///操作日期
        ('ActionTime', ctypes.c_char * 9),  # ///操作时间
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('OptionSelfCloseLocalID', ctypes.c_char * 13),  # ///本地期权自对冲编号
        ('ActionLocalID', ctypes.c_char * 13),  # ///操作本地编号
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('BusinessUnit', ctypes.c_char * 21),  # ///业务单元
        ('OrderActionStatus', ctypes.c_char * 1),  # ///报单操作状态
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('BranchID', ctypes.c_char * 9),  # ///营业部编号
        ('reserve1', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('reserve2', ctypes.c_char * 31),  # ///保留的无效字段
        ('OptSelfCloseFlag', ctypes.c_char * 1),  # ///期权行权的头寸是否自对冲
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
        ('ExchangeInstID', ctypes.c_char * 81),  # ///合约在交易所的代码
    ]


# ///延时换汇同步
class SyncDelaySwapField(BaseField):
    _fields_ = [
        ('DelaySwapSeqNo', ctypes.c_char * 15),  # ///换汇流水号
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('FromCurrencyID', ctypes.c_char * 4),  # ///源币种
        ('FromAmount', ctypes.c_double),  # ///源金额
        ('FromFrozenSwap', ctypes.c_double),  # ///源换汇冻结金额(可用冻结)
        ('FromRemainSwap', ctypes.c_double),  # ///源剩余换汇额度(可提冻结)
        ('ToCurrencyID', ctypes.c_char * 4),  # ///目标币种
        ('ToAmount', ctypes.c_double),  # ///目标金额
        ('IsManualSwap', ctypes.c_int),  # ///是否手工换汇
        ('IsAllRemainSetZero', ctypes.c_int),  # ///是否将所有外币的剩余换汇额度设置为0
    ]


# ///查询延时换汇同步
class QrySyncDelaySwapField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('DelaySwapSeqNo', ctypes.c_char * 15),  # ///延时换汇流水号
    ]


# ///投资单元
class InvestUnitField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('InvestorUnitName', ctypes.c_char * 81),  # ///投资者单元名称
        ('InvestorGroupID', ctypes.c_char * 13),  # ///投资者分组代码
        ('CommModelID', ctypes.c_char * 13),  # ///手续费率模板代码
        ('MarginModelID', ctypes.c_char * 13),  # ///保证金率模板代码
        ('AccountID', ctypes.c_char * 13),  # ///资金账号
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
    ]


# ///查询投资单元
class QryInvestUnitField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
    ]


# ///二级代理商资金校验模式
class SecAgentCheckModeField(BaseField):
    _fields_ = [
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('CurrencyID', ctypes.c_char * 4),  # ///币种
        ('BrokerSecAgentID', ctypes.c_char * 13),  # ///境外中介机构资金帐号
        ('CheckSelfAccount', ctypes.c_int),  # ///是否需要校验自己的资金账户
    ]


# ///二级代理商信息
class SecAgentTradeInfoField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('BrokerSecAgentID', ctypes.c_char * 13),  # ///境外中介机构资金帐号
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('LongCustomerName', ctypes.c_char * 161),  # ///二级代理商姓名
    ]


# ///市场行情
class MarketDataField(BaseField):
    _fields_ = [
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('reserve2', ctypes.c_char * 31),  # ///保留的无效字段
        ('LastPrice', ctypes.c_double),  # ///最新价
        ('PreSettlementPrice', ctypes.c_double),  # ///上次结算价
        ('PreClosePrice', ctypes.c_double),  # ///昨收盘
        ('PreOpenInterest', ctypes.c_double),  # ///昨持仓量
        ('OpenPrice', ctypes.c_double),  # ///今开盘
        ('HighestPrice', ctypes.c_double),  # ///最高价
        ('LowestPrice', ctypes.c_double),  # ///最低价
        ('Volume', ctypes.c_int),  # ///数量
        ('Turnover', ctypes.c_double),  # ///成交金额
        ('OpenInterest', ctypes.c_double),  # ///持仓量
        ('ClosePrice', ctypes.c_double),  # ///今收盘
        ('SettlementPrice', ctypes.c_double),  # ///本次结算价
        ('UpperLimitPrice', ctypes.c_double),  # ///涨停板价
        ('LowerLimitPrice', ctypes.c_double),  # ///跌停板价
        ('PreDelta', ctypes.c_double),  # ///昨虚实度
        ('CurrDelta', ctypes.c_double),  # ///今虚实度
        ('UpdateTime', ctypes.c_char * 9),  # ///最后修改时间
        ('UpdateMillisec', ctypes.c_int),  # ///最后修改毫秒
        ('ActionDay', ctypes.c_char * 9),  # ///业务日期
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('ExchangeInstID', ctypes.c_char * 81),  # ///合约在交易所的代码
    ]


# ///行情基础属性
class MarketDataBaseField(BaseField):
    _fields_ = [
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('PreSettlementPrice', ctypes.c_double),  # ///上次结算价
        ('PreClosePrice', ctypes.c_double),  # ///昨收盘
        ('PreOpenInterest', ctypes.c_double),  # ///昨持仓量
        ('PreDelta', ctypes.c_double),  # ///昨虚实度
    ]


# ///行情静态属性
class MarketDataStaticField(BaseField):
    _fields_ = [
        ('OpenPrice', ctypes.c_double),  # ///今开盘
        ('HighestPrice', ctypes.c_double),  # ///最高价
        ('LowestPrice', ctypes.c_double),  # ///最低价
        ('ClosePrice', ctypes.c_double),  # ///今收盘
        ('UpperLimitPrice', ctypes.c_double),  # ///涨停板价
        ('LowerLimitPrice', ctypes.c_double),  # ///跌停板价
        ('SettlementPrice', ctypes.c_double),  # ///本次结算价
        ('CurrDelta', ctypes.c_double),  # ///今虚实度
    ]


# ///行情最新成交属性
class MarketDataLastMatchField(BaseField):
    _fields_ = [
        ('LastPrice', ctypes.c_double),  # ///最新价
        ('Volume', ctypes.c_int),  # ///数量
        ('Turnover', ctypes.c_double),  # ///成交金额
        ('OpenInterest', ctypes.c_double),  # ///持仓量
    ]


# ///行情最优价属性
class MarketDataBestPriceField(BaseField):
    _fields_ = [
        ('BidPrice1', ctypes.c_double),  # ///申买价一
        ('BidVolume1', ctypes.c_int),  # ///申买量一
        ('AskPrice1', ctypes.c_double),  # ///申卖价一
        ('AskVolume1', ctypes.c_int),  # ///申卖量一
    ]


# ///行情申买二、三属性
class MarketDataBid23Field(BaseField):
    _fields_ = [
        ('BidPrice2', ctypes.c_double),  # ///申买价二
        ('BidVolume2', ctypes.c_int),  # ///申买量二
        ('BidPrice3', ctypes.c_double),  # ///申买价三
        ('BidVolume3', ctypes.c_int),  # ///申买量三
    ]


# ///行情申卖二、三属性
class MarketDataAsk23Field(BaseField):
    _fields_ = [
        ('AskPrice2', ctypes.c_double),  # ///申卖价二
        ('AskVolume2', ctypes.c_int),  # ///申卖量二
        ('AskPrice3', ctypes.c_double),  # ///申卖价三
        ('AskVolume3', ctypes.c_int),  # ///申卖量三
    ]


# ///行情申买四、五属性
class MarketDataBid45Field(BaseField):
    _fields_ = [
        ('BidPrice4', ctypes.c_double),  # ///申买价四
        ('BidVolume4', ctypes.c_int),  # ///申买量四
        ('BidPrice5', ctypes.c_double),  # ///申买价五
        ('BidVolume5', ctypes.c_int),  # ///申买量五
    ]


# ///行情申卖四、五属性
class MarketDataAsk45Field(BaseField):
    _fields_ = [
        ('AskPrice4', ctypes.c_double),  # ///申卖价四
        ('AskVolume4', ctypes.c_int),  # ///申卖量四
        ('AskPrice5', ctypes.c_double),  # ///申卖价五
        ('AskVolume5', ctypes.c_int),  # ///申卖量五
    ]


# ///行情更新时间属性
class MarketDataUpdateTimeField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('UpdateTime', ctypes.c_char * 9),  # ///最后修改时间
        ('UpdateMillisec', ctypes.c_int),  # ///最后修改毫秒
        ('ActionDay', ctypes.c_char * 9),  # ///业务日期
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///行情上下带价
class MarketDataBandingPriceField(BaseField):
    _fields_ = [
        ('BandingUpperPrice', ctypes.c_double),  # ///上带价
        ('BandingLowerPrice', ctypes.c_double),  # ///下带价
    ]


# ///行情交易所代码属性
class MarketDataExchangeField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
    ]


# ///指定的合约
class SpecificInstrumentField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///合约状态
class InstrumentStatusField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('SettlementGroupID', ctypes.c_char * 9),  # ///结算组代码
        ('reserve2', ctypes.c_char * 31),  # ///保留的无效字段
        ('InstrumentStatus', ctypes.c_char * 1),  # ///合约交易状态
        ('TradingSegmentSN', ctypes.c_int),  # ///交易阶段编号
        ('EnterTime', ctypes.c_char * 9),  # ///进入本状态时间
        ('EnterReason', ctypes.c_char * 1),  # ///进入本状态原因
        ('ExchangeInstID', ctypes.c_char * 81),  # ///合约在交易所的代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///查询合约状态
class QryInstrumentStatusField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ExchangeInstID', ctypes.c_char * 81),  # ///合约在交易所的代码
    ]


# ///投资者账户
class InvestorAccountField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
    ]


# ///浮动盈亏算法
class PositionProfitAlgorithmField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('Algorithm', ctypes.c_char * 1),  # ///盈亏算法
        ('Memo', ctypes.c_char * 161),  # ///备注
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
    ]


# ///会员资金折扣
class DiscountField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorRange', ctypes.c_char * 1),  # ///投资者范围
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('Discount', ctypes.c_double),  # ///资金折扣比例
    ]


# ///查询转帐银行
class QryTransferBankField(BaseField):
    _fields_ = [
        ('BankID', ctypes.c_char * 4),  # ///银行代码
        ('BankBrchID', ctypes.c_char * 5),  # ///银行分中心代码
    ]


# ///转帐银行
class TransferBankField(BaseField):
    _fields_ = [
        ('BankID', ctypes.c_char * 4),  # ///银行代码
        ('BankBrchID', ctypes.c_char * 5),  # ///银行分中心代码
        ('BankName', ctypes.c_char * 101),  # ///银行名称
        ('IsActive', ctypes.c_int),  # ///是否活跃
    ]


# ///查询投资者持仓明细
class QryInvestorPositionDetailField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///投资者持仓明细
class InvestorPositionDetailField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('Direction', ctypes.c_char * 1),  # ///买卖
        ('OpenDate', ctypes.c_char * 9),  # ///开仓日期
        ('TradeID', ctypes.c_char * 21),  # ///成交编号
        ('Volume', ctypes.c_int),  # ///数量
        ('OpenPrice', ctypes.c_double),  # ///开仓价
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('SettlementID', ctypes.c_int),  # ///结算编号
        ('TradeType', ctypes.c_char * 1),  # ///成交类型
        ('reserve2', ctypes.c_char * 31),  # ///保留的无效字段
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('CloseProfitByDate', ctypes.c_double),  # ///逐日盯市平仓盈亏
        ('CloseProfitByTrade', ctypes.c_double),  # ///逐笔对冲平仓盈亏
        ('PositionProfitByDate', ctypes.c_double),  # ///逐日盯市持仓盈亏
        ('PositionProfitByTrade', ctypes.c_double),  # ///逐笔对冲持仓盈亏
        ('Margin', ctypes.c_double),  # ///投资者保证金
        ('ExchMargin', ctypes.c_double),  # ///交易所保证金
        ('MarginRateByMoney', ctypes.c_double),  # ///保证金率
        ('MarginRateByVolume', ctypes.c_double),  # ///保证金率(按手数)
        ('LastSettlementPrice', ctypes.c_double),  # ///昨结算价
        ('SettlementPrice', ctypes.c_double),  # ///结算价
        ('CloseVolume', ctypes.c_int),  # ///平仓量
        ('CloseAmount', ctypes.c_double),  # ///平仓金额
        ('TimeFirstVolume', ctypes.c_int),  # ///先开先平剩余数量
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('SpecPosiType', ctypes.c_char * 1),  # ///特殊持仓标志
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('CombInstrumentID', ctypes.c_char * 81),  # ///组合合约代码
    ]


# ///资金账户口令域
class TradingAccountPasswordField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('Password', ctypes.c_char * 41),  # ///密码
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
    ]


# ///交易所行情报盘机
class MDTraderOfferField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('Password', ctypes.c_char * 41),  # ///密码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('OrderLocalID', ctypes.c_char * 13),  # ///本地报单编号
        ('TraderConnectStatus', ctypes.c_char * 1),  # ///交易所交易员连接状态
        ('ConnectRequestDate', ctypes.c_char * 9),  # ///发出连接请求的日期
        ('ConnectRequestTime', ctypes.c_char * 9),  # ///发出连接请求的时间
        ('LastReportDate', ctypes.c_char * 9),  # ///上次报告日期
        ('LastReportTime', ctypes.c_char * 9),  # ///上次报告时间
        ('ConnectDate', ctypes.c_char * 9),  # ///完成连接日期
        ('ConnectTime', ctypes.c_char * 9),  # ///完成连接时间
        ('StartDate', ctypes.c_char * 9),  # ///启动日期
        ('StartTime', ctypes.c_char * 9),  # ///启动时间
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('MaxTradeID', ctypes.c_char * 21),  # ///本席位最大成交编号
        ('MaxOrderMessageReference', ctypes.c_char * 7),  # ///本席位最大报单备拷
        ('OrderCancelAlg', ctypes.c_char * 1),  # ///撤单时选择席位算法
    ]


# ///查询行情报盘机
class QryMDTraderOfferField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
    ]


# ///查询客户通知
class QryNoticeField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
    ]


# ///客户通知
class NoticeField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('Content', ctypes.c_char * 501),  # ///消息正文
        ('SequenceLabel', ctypes.c_char * 2),  # ///经纪公司通知内容序列号
    ]


# ///用户权限
class UserRightField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('UserRightType', ctypes.c_char * 1),  # ///客户权限类型
        ('IsForbidden', ctypes.c_int),  # ///是否禁止
    ]


# ///查询结算信息确认域
class QrySettlementInfoConfirmField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
    ]


# ///装载结算信息
class LoadSettlementInfoField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
    ]


# ///经纪公司可提资金算法表
class BrokerWithdrawAlgorithmField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('WithdrawAlgorithm', ctypes.c_char * 1),  # ///可提资金算法
        ('UsingRatio', ctypes.c_double),  # ///资金使用率
        ('IncludeCloseProfit', ctypes.c_char * 1),  # ///可提是否包含平仓盈利
        ('AllWithoutTrade', ctypes.c_char * 1),  # ///本日无仓且无成交客户是否受可提比例限制
        ('AvailIncludeCloseProfit', ctypes.c_char * 1),  # ///可用是否包含平仓盈利
        ('IsBrokerUserEvent', ctypes.c_int),  # ///是否启用用户事件
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('FundMortgageRatio', ctypes.c_double),  # ///货币质押比率
        ('BalanceAlgorithm', ctypes.c_char * 1),  # ///权益算法
    ]


# ///资金账户口令变更域
class TradingAccountPasswordUpdateV1Field(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('OldPassword', ctypes.c_char * 41),  # ///原来的口令
        ('NewPassword', ctypes.c_char * 41),  # ///新的口令
    ]


# ///资金账户口令变更域
class TradingAccountPasswordUpdateField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('OldPassword', ctypes.c_char * 41),  # ///原来的口令
        ('NewPassword', ctypes.c_char * 41),  # ///新的口令
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
    ]


# ///查询组合合约分腿
class QryCombinationLegField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('LegID', ctypes.c_int),  # ///单腿编号
        ('reserve2', ctypes.c_char * 31),  # ///保留的无效字段
        ('CombInstrumentID', ctypes.c_char * 81),  # ///组合合约代码
        ('LegInstrumentID', ctypes.c_char * 81),  # ///单腿合约代码
    ]


# ///查询组合合约分腿
class QrySyncStatusField(BaseField):
    _fields_ = [
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
    ]


# ///组合交易合约的单腿
class CombinationLegField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('LegID', ctypes.c_int),  # ///单腿编号
        ('reserve2', ctypes.c_char * 31),  # ///保留的无效字段
        ('Direction', ctypes.c_char * 1),  # ///买卖方向
        ('LegMultiple', ctypes.c_int),  # ///单腿乘数
        ('ImplyLevel', ctypes.c_int),  # ///派生层数
        ('CombInstrumentID', ctypes.c_char * 81),  # ///组合合约代码
        ('LegInstrumentID', ctypes.c_char * 81),  # ///单腿合约代码
    ]


# ///数据同步状态
class SyncStatusField(BaseField):
    _fields_ = [
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('DataSyncStatus', ctypes.c_char * 1),  # ///数据同步状态
    ]


# ///查询联系人
class QryLinkManField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
    ]


# ///联系人
class LinkManField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('PersonType', ctypes.c_char * 1),  # ///联系人类型
        ('IdentifiedCardType', ctypes.c_char * 1),  # ///证件类型
        ('IdentifiedCardNo', ctypes.c_char * 51),  # ///证件号码
        ('PersonName', ctypes.c_char * 81),  # ///名称
        ('Telephone', ctypes.c_char * 41),  # ///联系电话
        ('Address', ctypes.c_char * 101),  # ///通讯地址
        ('ZipCode', ctypes.c_char * 7),  # ///邮政编码
        ('Priority', ctypes.c_int),  # ///优先级
        ('UOAZipCode', ctypes.c_char * 11),  # ///开户邮政编码
        ('PersonFullName', ctypes.c_char * 101),  # ///全称
    ]


# ///查询经纪公司用户事件
class QryBrokerUserEventField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('UserEventType', ctypes.c_char * 1),  # ///用户事件类型
    ]


# ///查询经纪公司用户事件
class BrokerUserEventField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('UserEventType', ctypes.c_char * 1),  # ///用户事件类型
        ('EventSequenceNo', ctypes.c_int),  # ///用户事件序号
        ('EventDate', ctypes.c_char * 9),  # ///事件发生日期
        ('EventTime', ctypes.c_char * 9),  # ///事件发生时间
        ('UserEventInfo', ctypes.c_char * 1025),  # ///用户事件信息
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///查询签约银行请求
class QryContractBankField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('BankID', ctypes.c_char * 4),  # ///银行代码
        ('BankBrchID', ctypes.c_char * 5),  # ///银行分中心代码
    ]


# ///查询签约银行响应
class ContractBankField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('BankID', ctypes.c_char * 4),  # ///银行代码
        ('BankBrchID', ctypes.c_char * 5),  # ///银行分中心代码
        ('BankName', ctypes.c_char * 101),  # ///银行名称
    ]


# ///投资者组合持仓明细
class InvestorPositionCombineDetailField(BaseField):
    _fields_ = [
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('OpenDate', ctypes.c_char * 9),  # ///开仓日期
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('SettlementID', ctypes.c_int),  # ///结算编号
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('ComTradeID', ctypes.c_char * 21),  # ///组合编号
        ('TradeID', ctypes.c_char * 21),  # ///撮合编号
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('Direction', ctypes.c_char * 1),  # ///买卖
        ('TotalAmt', ctypes.c_int),  # ///持仓量
        ('Margin', ctypes.c_double),  # ///投资者保证金
        ('ExchMargin', ctypes.c_double),  # ///交易所保证金
        ('MarginRateByMoney', ctypes.c_double),  # ///保证金率
        ('MarginRateByVolume', ctypes.c_double),  # ///保证金率(按手数)
        ('LegID', ctypes.c_int),  # ///单腿编号
        ('LegMultiple', ctypes.c_int),  # ///单腿乘数
        ('reserve2', ctypes.c_char * 31),  # ///保留的无效字段
        ('TradeGroupID', ctypes.c_int),  # ///成交组号
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('CombInstrumentID', ctypes.c_char * 81),  # ///组合持仓合约编码
    ]


# ///预埋单
class ParkedOrderField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('OrderRef', ctypes.c_char * 13),  # ///报单引用
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('OrderPriceType', ctypes.c_char * 1),  # ///报单价格条件
        ('Direction', ctypes.c_char * 1),  # ///买卖方向
        ('CombOffsetFlag', ctypes.c_char * 5),  # ///组合开平标志
        ('CombHedgeFlag', ctypes.c_char * 5),  # ///组合投机套保标志
        ('LimitPrice', ctypes.c_double),  # ///价格
        ('VolumeTotalOriginal', ctypes.c_int),  # ///数量
        ('TimeCondition', ctypes.c_char * 1),  # ///有效期类型
        ('GTDDate', ctypes.c_char * 9),  # ///GTD日期
        ('VolumeCondition', ctypes.c_char * 1),  # ///成交量类型
        ('MinVolume', ctypes.c_int),  # ///最小成交量
        ('ContingentCondition', ctypes.c_char * 1),  # ///触发条件
        ('StopPrice', ctypes.c_double),  # ///止损价
        ('ForceCloseReason', ctypes.c_char * 1),  # ///强平原因
        ('IsAutoSuspend', ctypes.c_int),  # ///自动挂起标志
        ('BusinessUnit', ctypes.c_char * 21),  # ///业务单元
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('UserForceClose', ctypes.c_int),  # ///用户强评标志
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ParkedOrderID', ctypes.c_char * 13),  # ///预埋报单编号
        ('UserType', ctypes.c_char * 1),  # ///用户类型
        ('Status', ctypes.c_char * 1),  # ///预埋单状态
        ('ErrorID', ctypes.c_int),  # ///错误代码
        ('ErrorMsg', ctypes.c_char * 81),  # ///错误信息
        ('IsSwapOrder', ctypes.c_int),  # ///互换单标志
        ('AccountID', ctypes.c_char * 13),  # ///资金账号
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('ClientID', ctypes.c_char * 11),  # ///交易编码
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('reserve2', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///输入预埋单操作
class ParkedOrderActionField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('OrderActionRef', ctypes.c_int),  # ///报单操作引用
        ('OrderRef', ctypes.c_char * 13),  # ///报单引用
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('FrontID', ctypes.c_int),  # ///前置编号
        ('SessionID', ctypes.c_int),  # ///会话编号
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('OrderSysID', ctypes.c_char * 21),  # ///报单编号
        ('ActionFlag', ctypes.c_char * 1),  # ///操作标志
        ('LimitPrice', ctypes.c_double),  # ///价格
        ('VolumeChange', ctypes.c_int),  # ///数量变化
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ParkedOrderActionID', ctypes.c_char * 13),  # ///预埋撤单单编号
        ('UserType', ctypes.c_char * 1),  # ///用户类型
        ('Status', ctypes.c_char * 1),  # ///预埋撤单状态
        ('ErrorID', ctypes.c_int),  # ///错误代码
        ('ErrorMsg', ctypes.c_char * 81),  # ///错误信息
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('reserve2', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///查询预埋单
class QryParkedOrderField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///查询预埋撤单
class QryParkedOrderActionField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///删除预埋单
class RemoveParkedOrderField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('ParkedOrderID', ctypes.c_char * 13),  # ///预埋报单编号
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
    ]


# ///删除预埋撤单
class RemoveParkedOrderActionField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('ParkedOrderActionID', ctypes.c_char * 13),  # ///预埋撤单编号
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
    ]


# ///经纪公司可提资金算法表
class InvestorWithdrawAlgorithmField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorRange', ctypes.c_char * 1),  # ///投资者范围
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('UsingRatio', ctypes.c_double),  # ///可提资金比例
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('FundMortgageRatio', ctypes.c_double),  # ///货币质押比率
    ]


# ///查询组合持仓明细
class QryInvestorPositionCombineDetailField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('CombInstrumentID', ctypes.c_char * 81),  # ///组合持仓合约编码
    ]


# ///成交均价
class MarketDataAveragePriceField(BaseField):
    _fields_ = [
        ('AveragePrice', ctypes.c_double),  # ///当日均价
    ]


# ///校验投资者密码
class VerifyInvestorPasswordField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('Password', ctypes.c_char * 41),  # ///密码
    ]


# ///用户IP
class UserIPField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('reserve1', ctypes.c_char * 16),  # ///保留的无效字段
        ('reserve2', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
        ('IPMask', ctypes.c_char * 33),  # ///IP地址掩码
    ]


# ///用户事件通知信息
class TradingNoticeInfoField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('SendTime', ctypes.c_char * 9),  # ///发送时间
        ('FieldContent', ctypes.c_char * 501),  # ///消息正文
        ('SequenceSeries', ctypes.c_short),  # ///序列系列号
        ('SequenceNo', ctypes.c_int),  # ///序列号
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
    ]


# ///用户事件通知
class TradingNoticeField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorRange', ctypes.c_char * 1),  # ///投资者范围
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('SequenceSeries', ctypes.c_short),  # ///序列系列号
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('SendTime', ctypes.c_char * 9),  # ///发送时间
        ('SequenceNo', ctypes.c_int),  # ///序列号
        ('FieldContent', ctypes.c_char * 501),  # ///消息正文
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
    ]


# ///查询交易事件通知
class QryTradingNoticeField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
    ]


# ///查询错误报单
class QryErrOrderField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
    ]


# ///错误报单
class ErrOrderField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('OrderRef', ctypes.c_char * 13),  # ///报单引用
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('OrderPriceType', ctypes.c_char * 1),  # ///报单价格条件
        ('Direction', ctypes.c_char * 1),  # ///买卖方向
        ('CombOffsetFlag', ctypes.c_char * 5),  # ///组合开平标志
        ('CombHedgeFlag', ctypes.c_char * 5),  # ///组合投机套保标志
        ('LimitPrice', ctypes.c_double),  # ///价格
        ('VolumeTotalOriginal', ctypes.c_int),  # ///数量
        ('TimeCondition', ctypes.c_char * 1),  # ///有效期类型
        ('GTDDate', ctypes.c_char * 9),  # ///GTD日期
        ('VolumeCondition', ctypes.c_char * 1),  # ///成交量类型
        ('MinVolume', ctypes.c_int),  # ///最小成交量
        ('ContingentCondition', ctypes.c_char * 1),  # ///触发条件
        ('StopPrice', ctypes.c_double),  # ///止损价
        ('ForceCloseReason', ctypes.c_char * 1),  # ///强平原因
        ('IsAutoSuspend', ctypes.c_int),  # ///自动挂起标志
        ('BusinessUnit', ctypes.c_char * 21),  # ///业务单元
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('UserForceClose', ctypes.c_int),  # ///用户强评标志
        ('ErrorID', ctypes.c_int),  # ///错误代码
        ('ErrorMsg', ctypes.c_char * 81),  # ///错误信息
        ('IsSwapOrder', ctypes.c_int),  # ///互换单标志
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('AccountID', ctypes.c_char * 13),  # ///资金账号
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('ClientID', ctypes.c_char * 11),  # ///交易编码
        ('reserve2', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///查询错误报单操作
class ErrorConditionalOrderField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('OrderRef', ctypes.c_char * 13),  # ///报单引用
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('OrderPriceType', ctypes.c_char * 1),  # ///报单价格条件
        ('Direction', ctypes.c_char * 1),  # ///买卖方向
        ('CombOffsetFlag', ctypes.c_char * 5),  # ///组合开平标志
        ('CombHedgeFlag', ctypes.c_char * 5),  # ///组合投机套保标志
        ('LimitPrice', ctypes.c_double),  # ///价格
        ('VolumeTotalOriginal', ctypes.c_int),  # ///数量
        ('TimeCondition', ctypes.c_char * 1),  # ///有效期类型
        ('GTDDate', ctypes.c_char * 9),  # ///GTD日期
        ('VolumeCondition', ctypes.c_char * 1),  # ///成交量类型
        ('MinVolume', ctypes.c_int),  # ///最小成交量
        ('ContingentCondition', ctypes.c_char * 1),  # ///触发条件
        ('StopPrice', ctypes.c_double),  # ///止损价
        ('ForceCloseReason', ctypes.c_char * 1),  # ///强平原因
        ('IsAutoSuspend', ctypes.c_int),  # ///自动挂起标志
        ('BusinessUnit', ctypes.c_char * 21),  # ///业务单元
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('OrderLocalID', ctypes.c_char * 13),  # ///本地报单编号
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('reserve2', ctypes.c_char * 31),  # ///保留的无效字段
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('OrderSubmitStatus', ctypes.c_char * 1),  # ///报单提交状态
        ('NotifySequence', ctypes.c_int),  # ///报单提示序号
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('SettlementID', ctypes.c_int),  # ///结算编号
        ('OrderSysID', ctypes.c_char * 21),  # ///报单编号
        ('OrderSource', ctypes.c_char * 1),  # ///报单来源
        ('OrderStatus', ctypes.c_char * 1),  # ///报单状态
        ('OrderType', ctypes.c_char * 1),  # ///报单类型
        ('VolumeTraded', ctypes.c_int),  # ///今成交数量
        ('VolumeTotal', ctypes.c_int),  # ///剩余数量
        ('InsertDate', ctypes.c_char * 9),  # ///报单日期
        ('InsertTime', ctypes.c_char * 9),  # ///委托时间
        ('ActiveTime', ctypes.c_char * 9),  # ///激活时间
        ('SuspendTime', ctypes.c_char * 9),  # ///挂起时间
        ('UpdateTime', ctypes.c_char * 9),  # ///最后修改时间
        ('CancelTime', ctypes.c_char * 9),  # ///撤销时间
        ('ActiveTraderID', ctypes.c_char * 21),  # ///最后修改交易所交易员代码
        ('ClearingPartID', ctypes.c_char * 11),  # ///结算会员编号
        ('SequenceNo', ctypes.c_int),  # ///序号
        ('FrontID', ctypes.c_int),  # ///前置编号
        ('SessionID', ctypes.c_int),  # ///会话编号
        ('UserProductInfo', ctypes.c_char * 11),  # ///用户端产品信息
        ('StatusMsg', ctypes.c_char * 81),  # ///状态信息
        ('UserForceClose', ctypes.c_int),  # ///用户强评标志
        ('ActiveUserID', ctypes.c_char * 16),  # ///操作用户代码
        ('BrokerOrderSeq', ctypes.c_int),  # ///经纪公司报单编号
        ('RelativeOrderSysID', ctypes.c_char * 21),  # ///相关报单
        ('ZCETotalTradedVolume', ctypes.c_int),  # ///郑商所成交数量
        ('ErrorID', ctypes.c_int),  # ///错误代码
        ('ErrorMsg', ctypes.c_char * 81),  # ///错误信息
        ('IsSwapOrder', ctypes.c_int),  # ///互换单标志
        ('BranchID', ctypes.c_char * 9),  # ///营业部编号
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('AccountID', ctypes.c_char * 13),  # ///资金账号
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('reserve3', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('ExchangeInstID', ctypes.c_char * 81),  # ///合约在交易所的代码
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///查询错误报单操作
class QryErrOrderActionField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
    ]


# ///错误报单操作
class ErrOrderActionField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('OrderActionRef', ctypes.c_int),  # ///报单操作引用
        ('OrderRef', ctypes.c_char * 13),  # ///报单引用
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('FrontID', ctypes.c_int),  # ///前置编号
        ('SessionID', ctypes.c_int),  # ///会话编号
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('OrderSysID', ctypes.c_char * 21),  # ///报单编号
        ('ActionFlag', ctypes.c_char * 1),  # ///操作标志
        ('LimitPrice', ctypes.c_double),  # ///价格
        ('VolumeChange', ctypes.c_int),  # ///数量变化
        ('ActionDate', ctypes.c_char * 9),  # ///操作日期
        ('ActionTime', ctypes.c_char * 9),  # ///操作时间
        ('TraderID', ctypes.c_char * 21),  # ///交易所交易员代码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('OrderLocalID', ctypes.c_char * 13),  # ///本地报单编号
        ('ActionLocalID', ctypes.c_char * 13),  # ///操作本地编号
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('ClientID', ctypes.c_char * 11),  # ///客户代码
        ('BusinessUnit', ctypes.c_char * 21),  # ///业务单元
        ('OrderActionStatus', ctypes.c_char * 1),  # ///报单操作状态
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('StatusMsg', ctypes.c_char * 81),  # ///状态信息
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('BranchID', ctypes.c_char * 9),  # ///营业部编号
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('reserve2', ctypes.c_char * 16),  # ///保留的无效字段
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('ErrorID', ctypes.c_int),  # ///错误代码
        ('ErrorMsg', ctypes.c_char * 81),  # ///错误信息
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///查询交易所状态
class QryExchangeSequenceField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
    ]


# ///交易所状态
class ExchangeSequenceField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('SequenceNo', ctypes.c_int),  # ///序号
        ('MarketStatus', ctypes.c_char * 1),  # ///合约交易状态
    ]


# ///根据价格查询最大报单数量
class QryMaxOrderVolumeWithPriceField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('Direction', ctypes.c_char * 1),  # ///买卖方向
        ('OffsetFlag', ctypes.c_char * 1),  # ///开平标志
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('MaxVolume', ctypes.c_int),  # ///最大允许报单数量
        ('Price', ctypes.c_double),  # ///报单价格
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///查询经纪公司交易参数
class QryBrokerTradingParamsField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
    ]


# ///经纪公司交易参数
class BrokerTradingParamsField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('MarginPriceType', ctypes.c_char * 1),  # ///保证金价格类型
        ('Algorithm', ctypes.c_char * 1),  # ///盈亏算法
        ('AvailIncludeCloseProfit', ctypes.c_char * 1),  # ///可用是否包含平仓盈利
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('OptionRoyaltyPriceType', ctypes.c_char * 1),  # ///期权权利金价格类型
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
    ]


# ///查询经纪公司交易算法
class QryBrokerTradingAlgosField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///经纪公司交易算法
class BrokerTradingAlgosField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('HandlePositionAlgoID', ctypes.c_char * 1),  # ///持仓处理算法编号
        ('FindMarginRateAlgoID', ctypes.c_char * 1),  # ///寻找保证金率算法编号
        ('HandleTradingAccountAlgoID', ctypes.c_char * 1),  # ///资金处理算法编号
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///查询经纪公司资金
class QueryBrokerDepositField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
    ]


# ///经纪公司资金
class BrokerDepositField(BaseField):
    _fields_ = [
        ('TradingDay', ctypes.c_char * 9),  # ///交易日期
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('ParticipantID', ctypes.c_char * 11),  # ///会员代码
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('PreBalance', ctypes.c_double),  # ///上次结算准备金
        ('CurrMargin', ctypes.c_double),  # ///当前保证金总额
        ('CloseProfit', ctypes.c_double),  # ///平仓盈亏
        ('Balance', ctypes.c_double),  # ///期货结算准备金
        ('Deposit', ctypes.c_double),  # ///入金金额
        ('Withdraw', ctypes.c_double),  # ///出金金额
        ('Available', ctypes.c_double),  # ///可提资金
        ('Reserve', ctypes.c_double),  # ///基本准备金
        ('FrozenMargin', ctypes.c_double),  # ///冻结的保证金
    ]


# ///查询保证金监管系统经纪公司密钥
class QryCFMMCBrokerKeyField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
    ]


# ///保证金监管系统经纪公司密钥
class CFMMCBrokerKeyField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('ParticipantID', ctypes.c_char * 11),  # ///经纪公司统一编码
        ('CreateDate', ctypes.c_char * 9),  # ///密钥生成日期
        ('CreateTime', ctypes.c_char * 9),  # ///密钥生成时间
        ('KeyID', ctypes.c_int),  # ///密钥编号
        ('CurrentKey', ctypes.c_char * 21),  # ///动态密钥
        ('KeyKind', ctypes.c_char * 1),  # ///动态密钥类型
    ]


# ///保证金监管系统经纪公司资金账户密钥
class CFMMCTradingAccountKeyField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('ParticipantID', ctypes.c_char * 11),  # ///经纪公司统一编码
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('KeyID', ctypes.c_int),  # ///密钥编号
        ('CurrentKey', ctypes.c_char * 21),  # ///动态密钥
    ]


# ///请求查询保证金监管系统经纪公司资金账户密钥
class QryCFMMCTradingAccountKeyField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
    ]


# ///用户动态令牌参数
class BrokerUserOTPParamField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('OTPVendorsID', ctypes.c_char * 2),  # ///动态令牌提供商
        ('SerialNumber', ctypes.c_char * 17),  # ///动态令牌序列号
        ('AuthKey', ctypes.c_char * 41),  # ///令牌密钥
        ('LastDrift', ctypes.c_int),  # ///漂移值
        ('LastSuccess', ctypes.c_int),  # ///成功值
        ('OTPType', ctypes.c_char * 1),  # ///动态令牌类型
    ]


# ///手工同步用户动态令牌
class ManualSyncBrokerUserOTPField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('OTPType', ctypes.c_char * 1),  # ///动态令牌类型
        ('FirstOTP', ctypes.c_char * 41),  # ///第一个动态密码
        ('SecondOTP', ctypes.c_char * 41),  # ///第二个动态密码
    ]


# ///投资者手续费率模板
class CommRateModelField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('CommModelID', ctypes.c_char * 13),  # ///手续费率模板代码
        ('CommModelName', ctypes.c_char * 161),  # ///模板名称
    ]


# ///请求查询投资者手续费率模板
class QryCommRateModelField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('CommModelID', ctypes.c_char * 13),  # ///手续费率模板代码
    ]


# ///投资者保证金率模板
class MarginModelField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('MarginModelID', ctypes.c_char * 13),  # ///保证金率模板代码
        ('MarginModelName', ctypes.c_char * 161),  # ///模板名称
    ]


# ///请求查询投资者保证金率模板
class QryMarginModelField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('MarginModelID', ctypes.c_char * 13),  # ///保证金率模板代码
    ]


# ///仓单折抵信息
class EWarrantOffsetField(BaseField):
    _fields_ = [
        ('TradingDay', ctypes.c_char * 9),  # ///交易日期
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('Direction', ctypes.c_char * 1),  # ///买卖方向
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('Volume', ctypes.c_int),  # ///数量
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///查询仓单折抵信息
class QryEWarrantOffsetField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///查询投资者品种/跨品种保证金
class QryInvestorProductGroupMarginField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('ProductGroupID', ctypes.c_char * 81),  # ///品种/跨品种标示
    ]


# ///投资者品种/跨品种保证金
class InvestorProductGroupMarginField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('SettlementID', ctypes.c_int),  # ///结算编号
        ('FrozenMargin', ctypes.c_double),  # ///冻结的保证金
        ('LongFrozenMargin', ctypes.c_double),  # ///多头冻结的保证金
        ('ShortFrozenMargin', ctypes.c_double),  # ///空头冻结的保证金
        ('UseMargin', ctypes.c_double),  # ///占用的保证金
        ('LongUseMargin', ctypes.c_double),  # ///多头保证金
        ('ShortUseMargin', ctypes.c_double),  # ///空头保证金
        ('ExchMargin', ctypes.c_double),  # ///交易所保证金
        ('LongExchMargin', ctypes.c_double),  # ///交易所多头保证金
        ('ShortExchMargin', ctypes.c_double),  # ///交易所空头保证金
        ('CloseProfit', ctypes.c_double),  # ///平仓盈亏
        ('FrozenCommission', ctypes.c_double),  # ///冻结的手续费
        ('Commission', ctypes.c_double),  # ///手续费
        ('FrozenCash', ctypes.c_double),  # ///冻结的资金
        ('CashIn', ctypes.c_double),  # ///资金差额
        ('PositionProfit', ctypes.c_double),  # ///持仓盈亏
        ('OffsetAmount', ctypes.c_double),  # ///折抵总金额
        ('LongOffsetAmount', ctypes.c_double),  # ///多头折抵总金额
        ('ShortOffsetAmount', ctypes.c_double),  # ///空头折抵总金额
        ('ExchOffsetAmount', ctypes.c_double),  # ///交易所折抵总金额
        ('LongExchOffsetAmount', ctypes.c_double),  # ///交易所多头折抵总金额
        ('ShortExchOffsetAmount', ctypes.c_double),  # ///交易所空头折抵总金额
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('ProductGroupID', ctypes.c_char * 81),  # ///品种/跨品种标示
    ]


# ///查询监控中心用户令牌
class QueryCFMMCTradingAccountTokenField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
    ]


# ///监控中心用户令牌
class CFMMCTradingAccountTokenField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('ParticipantID', ctypes.c_char * 11),  # ///经纪公司统一编码
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('KeyID', ctypes.c_int),  # ///密钥编号
        ('Token', ctypes.c_char * 21),  # ///动态令牌
    ]


# ///查询产品组
class QryProductGroupField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ProductID', ctypes.c_char * 81),  # ///产品代码
    ]


# ///投资者品种/跨品种保证金产品组
class ProductGroupField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('reserve2', ctypes.c_char * 31),  # ///保留的无效字段
        ('ProductID', ctypes.c_char * 81),  # ///产品代码
        ('ProductGroupID', ctypes.c_char * 81),  # ///产品组代码
    ]


# ///交易所公告
class BulletinField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('BulletinID', ctypes.c_int),  # ///公告编号
        ('SequenceNo', ctypes.c_int),  # ///序列号
        ('NewsType', ctypes.c_char * 3),  # ///公告类型
        ('NewsUrgency', ctypes.c_char * 1),  # ///紧急程度
        ('SendTime', ctypes.c_char * 9),  # ///发送时间
        ('Abstract', ctypes.c_char * 81),  # ///消息摘要
        ('ComeFrom', ctypes.c_char * 21),  # ///消息来源
        ('Content', ctypes.c_char * 501),  # ///消息正文
        ('URLLink', ctypes.c_char * 201),  # ///WEB地址
        ('MarketID', ctypes.c_char * 31),  # ///市场代码
    ]


# ///查询交易所公告
class QryBulletinField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('BulletinID', ctypes.c_int),  # ///公告编号
        ('SequenceNo', ctypes.c_int),  # ///序列号
        ('NewsType', ctypes.c_char * 3),  # ///公告类型
        ('NewsUrgency', ctypes.c_char * 1),  # ///紧急程度
    ]


# ///MulticastInstrument
class MulticastInstrumentField(BaseField):
    _fields_ = [
        ('TopicID', ctypes.c_int),  # ///主题号
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('InstrumentNo', ctypes.c_int),  # ///合约编号
        ('CodePrice', ctypes.c_double),  # ///基准价
        ('VolumeMultiple', ctypes.c_int),  # ///合约数量乘数
        ('PriceTick', ctypes.c_double),  # ///最小变动价位
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///QryMulticastInstrument
class QryMulticastInstrumentField(BaseField):
    _fields_ = [
        ('TopicID', ctypes.c_int),  # ///主题号
        ('reserve1', ctypes.c_char * 31),  # ///保留的无效字段
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///App客户端权限分配
class AppIDAuthAssignField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('AppID', ctypes.c_char * 33),  # ///App代码
        ('DRIdentityID', ctypes.c_int),  # ///交易中心代码
    ]


# ///转帐开户请求
class ReqOpenAccountField(BaseField):
    _fields_ = [
        ('TradeCode', ctypes.c_char * 7),  # ///业务功能码
        ('BankID', ctypes.c_char * 4),  # ///银行代码
        ('BankBranchID', ctypes.c_char * 5),  # ///银行分支机构代码
        ('BrokerID', ctypes.c_char * 11),  # ///期商代码
        ('BrokerBranchID', ctypes.c_char * 31),  # ///期商分支机构代码
        ('TradeDate', ctypes.c_char * 9),  # ///交易日期
        ('TradeTime', ctypes.c_char * 9),  # ///交易时间
        ('BankSerial', ctypes.c_char * 13),  # ///银行流水号
        ('TradingDay', ctypes.c_char * 9),  # ///交易系统日期
        ('PlateSerial', ctypes.c_int),  # ///银期平台消息流水号
        ('LastFragment', ctypes.c_char * 1),  # ///最后分片标志
        ('SessionID', ctypes.c_int),  # ///会话号
        ('CustomerName', ctypes.c_char * 51),  # ///客户姓名
        ('IdCardType', ctypes.c_char * 1),  # ///证件类型
        ('IdentifiedCardNo', ctypes.c_char * 51),  # ///证件号码
        ('Gender', ctypes.c_char * 1),  # ///性别
        ('CountryCode', ctypes.c_char * 21),  # ///国家代码
        ('CustType', ctypes.c_char * 1),  # ///客户类型
        ('Address', ctypes.c_char * 101),  # ///地址
        ('ZipCode', ctypes.c_char * 7),  # ///邮编
        ('Telephone', ctypes.c_char * 41),  # ///电话号码
        ('MobilePhone', ctypes.c_char * 21),  # ///手机
        ('Fax', ctypes.c_char * 41),  # ///传真
        ('EMail', ctypes.c_char * 41),  # ///电子邮件
        ('MoneyAccountStatus', ctypes.c_char * 1),  # ///资金账户状态
        ('BankAccount', ctypes.c_char * 41),  # ///银行帐号
        ('BankPassWord', ctypes.c_char * 41),  # ///银行密码
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('Password', ctypes.c_char * 41),  # ///期货密码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('VerifyCertNoFlag', ctypes.c_char * 1),  # ///验证客户证件号码标志
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('CashExchangeCode', ctypes.c_char * 1),  # ///汇钞标志
        ('Digest', ctypes.c_char * 36),  # ///摘要
        ('BankAccType', ctypes.c_char * 1),  # ///银行帐号类型
        ('DeviceID', ctypes.c_char * 3),  # ///渠道标志
        ('BankSecuAccType', ctypes.c_char * 1),  # ///期货单位帐号类型
        ('BrokerIDByBank', ctypes.c_char * 33),  # ///期货公司银行编码
        ('BankSecuAcc', ctypes.c_char * 41),  # ///期货单位帐号
        ('BankPwdFlag', ctypes.c_char * 1),  # ///银行密码标志
        ('SecuPwdFlag', ctypes.c_char * 1),  # ///期货资金密码核对标志
        ('OperNo', ctypes.c_char * 17),  # ///交易柜员
        ('TID', ctypes.c_int),  # ///交易ID
        ('UserID', ctypes.c_char * 16),  # ///用户标识
        ('LongCustomerName', ctypes.c_char * 161),  # ///长客户姓名
    ]


# ///转帐销户请求
class ReqCancelAccountField(BaseField):
    _fields_ = [
        ('TradeCode', ctypes.c_char * 7),  # ///业务功能码
        ('BankID', ctypes.c_char * 4),  # ///银行代码
        ('BankBranchID', ctypes.c_char * 5),  # ///银行分支机构代码
        ('BrokerID', ctypes.c_char * 11),  # ///期商代码
        ('BrokerBranchID', ctypes.c_char * 31),  # ///期商分支机构代码
        ('TradeDate', ctypes.c_char * 9),  # ///交易日期
        ('TradeTime', ctypes.c_char * 9),  # ///交易时间
        ('BankSerial', ctypes.c_char * 13),  # ///银行流水号
        ('TradingDay', ctypes.c_char * 9),  # ///交易系统日期
        ('PlateSerial', ctypes.c_int),  # ///银期平台消息流水号
        ('LastFragment', ctypes.c_char * 1),  # ///最后分片标志
        ('SessionID', ctypes.c_int),  # ///会话号
        ('CustomerName', ctypes.c_char * 51),  # ///客户姓名
        ('IdCardType', ctypes.c_char * 1),  # ///证件类型
        ('IdentifiedCardNo', ctypes.c_char * 51),  # ///证件号码
        ('Gender', ctypes.c_char * 1),  # ///性别
        ('CountryCode', ctypes.c_char * 21),  # ///国家代码
        ('CustType', ctypes.c_char * 1),  # ///客户类型
        ('Address', ctypes.c_char * 101),  # ///地址
        ('ZipCode', ctypes.c_char * 7),  # ///邮编
        ('Telephone', ctypes.c_char * 41),  # ///电话号码
        ('MobilePhone', ctypes.c_char * 21),  # ///手机
        ('Fax', ctypes.c_char * 41),  # ///传真
        ('EMail', ctypes.c_char * 41),  # ///电子邮件
        ('MoneyAccountStatus', ctypes.c_char * 1),  # ///资金账户状态
        ('BankAccount', ctypes.c_char * 41),  # ///银行帐号
        ('BankPassWord', ctypes.c_char * 41),  # ///银行密码
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('Password', ctypes.c_char * 41),  # ///期货密码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('VerifyCertNoFlag', ctypes.c_char * 1),  # ///验证客户证件号码标志
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('CashExchangeCode', ctypes.c_char * 1),  # ///汇钞标志
        ('Digest', ctypes.c_char * 36),  # ///摘要
        ('BankAccType', ctypes.c_char * 1),  # ///银行帐号类型
        ('DeviceID', ctypes.c_char * 3),  # ///渠道标志
        ('BankSecuAccType', ctypes.c_char * 1),  # ///期货单位帐号类型
        ('BrokerIDByBank', ctypes.c_char * 33),  # ///期货公司银行编码
        ('BankSecuAcc', ctypes.c_char * 41),  # ///期货单位帐号
        ('BankPwdFlag', ctypes.c_char * 1),  # ///银行密码标志
        ('SecuPwdFlag', ctypes.c_char * 1),  # ///期货资金密码核对标志
        ('OperNo', ctypes.c_char * 17),  # ///交易柜员
        ('TID', ctypes.c_int),  # ///交易ID
        ('UserID', ctypes.c_char * 16),  # ///用户标识
        ('LongCustomerName', ctypes.c_char * 161),  # ///长客户姓名
    ]


# ///变更银行账户请求
class ReqChangeAccountField(BaseField):
    _fields_ = [
        ('TradeCode', ctypes.c_char * 7),  # ///业务功能码
        ('BankID', ctypes.c_char * 4),  # ///银行代码
        ('BankBranchID', ctypes.c_char * 5),  # ///银行分支机构代码
        ('BrokerID', ctypes.c_char * 11),  # ///期商代码
        ('BrokerBranchID', ctypes.c_char * 31),  # ///期商分支机构代码
        ('TradeDate', ctypes.c_char * 9),  # ///交易日期
        ('TradeTime', ctypes.c_char * 9),  # ///交易时间
        ('BankSerial', ctypes.c_char * 13),  # ///银行流水号
        ('TradingDay', ctypes.c_char * 9),  # ///交易系统日期
        ('PlateSerial', ctypes.c_int),  # ///银期平台消息流水号
        ('LastFragment', ctypes.c_char * 1),  # ///最后分片标志
        ('SessionID', ctypes.c_int),  # ///会话号
        ('CustomerName', ctypes.c_char * 51),  # ///客户姓名
        ('IdCardType', ctypes.c_char * 1),  # ///证件类型
        ('IdentifiedCardNo', ctypes.c_char * 51),  # ///证件号码
        ('Gender', ctypes.c_char * 1),  # ///性别
        ('CountryCode', ctypes.c_char * 21),  # ///国家代码
        ('CustType', ctypes.c_char * 1),  # ///客户类型
        ('Address', ctypes.c_char * 101),  # ///地址
        ('ZipCode', ctypes.c_char * 7),  # ///邮编
        ('Telephone', ctypes.c_char * 41),  # ///电话号码
        ('MobilePhone', ctypes.c_char * 21),  # ///手机
        ('Fax', ctypes.c_char * 41),  # ///传真
        ('EMail', ctypes.c_char * 41),  # ///电子邮件
        ('MoneyAccountStatus', ctypes.c_char * 1),  # ///资金账户状态
        ('BankAccount', ctypes.c_char * 41),  # ///银行帐号
        ('BankPassWord', ctypes.c_char * 41),  # ///银行密码
        ('NewBankAccount', ctypes.c_char * 41),  # ///新银行帐号
        ('NewBankPassWord', ctypes.c_char * 41),  # ///新银行密码
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('Password', ctypes.c_char * 41),  # ///期货密码
        ('BankAccType', ctypes.c_char * 1),  # ///银行帐号类型
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('VerifyCertNoFlag', ctypes.c_char * 1),  # ///验证客户证件号码标志
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('BrokerIDByBank', ctypes.c_char * 33),  # ///期货公司银行编码
        ('BankPwdFlag', ctypes.c_char * 1),  # ///银行密码标志
        ('SecuPwdFlag', ctypes.c_char * 1),  # ///期货资金密码核对标志
        ('TID', ctypes.c_int),  # ///交易ID
        ('Digest', ctypes.c_char * 36),  # ///摘要
        ('LongCustomerName', ctypes.c_char * 161),  # ///长客户姓名
    ]


# ///转账请求
class ReqTransferField(BaseField):
    _fields_ = [
        ('TradeCode', ctypes.c_char * 7),  # ///业务功能码
        ('BankID', ctypes.c_char * 4),  # ///银行代码
        ('BankBranchID', ctypes.c_char * 5),  # ///银行分支机构代码
        ('BrokerID', ctypes.c_char * 11),  # ///期商代码
        ('BrokerBranchID', ctypes.c_char * 31),  # ///期商分支机构代码
        ('TradeDate', ctypes.c_char * 9),  # ///交易日期
        ('TradeTime', ctypes.c_char * 9),  # ///交易时间
        ('BankSerial', ctypes.c_char * 13),  # ///银行流水号
        ('TradingDay', ctypes.c_char * 9),  # ///交易系统日期
        ('PlateSerial', ctypes.c_int),  # ///银期平台消息流水号
        ('LastFragment', ctypes.c_char * 1),  # ///最后分片标志
        ('SessionID', ctypes.c_int),  # ///会话号
        ('CustomerName', ctypes.c_char * 51),  # ///客户姓名
        ('IdCardType', ctypes.c_char * 1),  # ///证件类型
        ('IdentifiedCardNo', ctypes.c_char * 51),  # ///证件号码
        ('CustType', ctypes.c_char * 1),  # ///客户类型
        ('BankAccount', ctypes.c_char * 41),  # ///银行帐号
        ('BankPassWord', ctypes.c_char * 41),  # ///银行密码
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('Password', ctypes.c_char * 41),  # ///期货密码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('FutureSerial', ctypes.c_int),  # ///期货公司流水号
        ('UserID', ctypes.c_char * 16),  # ///用户标识
        ('VerifyCertNoFlag', ctypes.c_char * 1),  # ///验证客户证件号码标志
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('TradeAmount', ctypes.c_double),  # ///转帐金额
        ('FutureFetchAmount', ctypes.c_double),  # ///期货可取金额
        ('FeePayFlag', ctypes.c_char * 1),  # ///费用支付标志
        ('CustFee', ctypes.c_double),  # ///应收客户费用
        ('BrokerFee', ctypes.c_double),  # ///应收期货公司费用
        ('Message', ctypes.c_char * 129),  # ///发送方给接收方的消息
        ('Digest', ctypes.c_char * 36),  # ///摘要
        ('BankAccType', ctypes.c_char * 1),  # ///银行帐号类型
        ('DeviceID', ctypes.c_char * 3),  # ///渠道标志
        ('BankSecuAccType', ctypes.c_char * 1),  # ///期货单位帐号类型
        ('BrokerIDByBank', ctypes.c_char * 33),  # ///期货公司银行编码
        ('BankSecuAcc', ctypes.c_char * 41),  # ///期货单位帐号
        ('BankPwdFlag', ctypes.c_char * 1),  # ///银行密码标志
        ('SecuPwdFlag', ctypes.c_char * 1),  # ///期货资金密码核对标志
        ('OperNo', ctypes.c_char * 17),  # ///交易柜员
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('TID', ctypes.c_int),  # ///交易ID
        ('TransferStatus', ctypes.c_char * 1),  # ///转账交易状态
        ('LongCustomerName', ctypes.c_char * 161),  # ///长客户姓名
    ]


# ///银行发起银行资金转期货响应
class RspTransferField(BaseField):
    _fields_ = [
        ('TradeCode', ctypes.c_char * 7),  # ///业务功能码
        ('BankID', ctypes.c_char * 4),  # ///银行代码
        ('BankBranchID', ctypes.c_char * 5),  # ///银行分支机构代码
        ('BrokerID', ctypes.c_char * 11),  # ///期商代码
        ('BrokerBranchID', ctypes.c_char * 31),  # ///期商分支机构代码
        ('TradeDate', ctypes.c_char * 9),  # ///交易日期
        ('TradeTime', ctypes.c_char * 9),  # ///交易时间
        ('BankSerial', ctypes.c_char * 13),  # ///银行流水号
        ('TradingDay', ctypes.c_char * 9),  # ///交易系统日期
        ('PlateSerial', ctypes.c_int),  # ///银期平台消息流水号
        ('LastFragment', ctypes.c_char * 1),  # ///最后分片标志
        ('SessionID', ctypes.c_int),  # ///会话号
        ('CustomerName', ctypes.c_char * 51),  # ///客户姓名
        ('IdCardType', ctypes.c_char * 1),  # ///证件类型
        ('IdentifiedCardNo', ctypes.c_char * 51),  # ///证件号码
        ('CustType', ctypes.c_char * 1),  # ///客户类型
        ('BankAccount', ctypes.c_char * 41),  # ///银行帐号
        ('BankPassWord', ctypes.c_char * 41),  # ///银行密码
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('Password', ctypes.c_char * 41),  # ///期货密码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('FutureSerial', ctypes.c_int),  # ///期货公司流水号
        ('UserID', ctypes.c_char * 16),  # ///用户标识
        ('VerifyCertNoFlag', ctypes.c_char * 1),  # ///验证客户证件号码标志
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('TradeAmount', ctypes.c_double),  # ///转帐金额
        ('FutureFetchAmount', ctypes.c_double),  # ///期货可取金额
        ('FeePayFlag', ctypes.c_char * 1),  # ///费用支付标志
        ('CustFee', ctypes.c_double),  # ///应收客户费用
        ('BrokerFee', ctypes.c_double),  # ///应收期货公司费用
        ('Message', ctypes.c_char * 129),  # ///发送方给接收方的消息
        ('Digest', ctypes.c_char * 36),  # ///摘要
        ('BankAccType', ctypes.c_char * 1),  # ///银行帐号类型
        ('DeviceID', ctypes.c_char * 3),  # ///渠道标志
        ('BankSecuAccType', ctypes.c_char * 1),  # ///期货单位帐号类型
        ('BrokerIDByBank', ctypes.c_char * 33),  # ///期货公司银行编码
        ('BankSecuAcc', ctypes.c_char * 41),  # ///期货单位帐号
        ('BankPwdFlag', ctypes.c_char * 1),  # ///银行密码标志
        ('SecuPwdFlag', ctypes.c_char * 1),  # ///期货资金密码核对标志
        ('OperNo', ctypes.c_char * 17),  # ///交易柜员
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('TID', ctypes.c_int),  # ///交易ID
        ('TransferStatus', ctypes.c_char * 1),  # ///转账交易状态
        ('ErrorID', ctypes.c_int),  # ///错误代码
        ('ErrorMsg', ctypes.c_char * 81),  # ///错误信息
        ('LongCustomerName', ctypes.c_char * 161),  # ///长客户姓名
    ]


# ///冲正请求
class ReqRepealField(BaseField):
    _fields_ = [
        ('RepealTimeInterval', ctypes.c_int),  # ///冲正时间间隔
        ('RepealedTimes', ctypes.c_int),  # ///已经冲正次数
        ('BankRepealFlag', ctypes.c_char * 1),  # ///银行冲正标志
        ('BrokerRepealFlag', ctypes.c_char * 1),  # ///期商冲正标志
        ('PlateRepealSerial', ctypes.c_int),  # ///被冲正平台流水号
        ('BankRepealSerial', ctypes.c_char * 13),  # ///被冲正银行流水号
        ('FutureRepealSerial', ctypes.c_int),  # ///被冲正期货流水号
        ('TradeCode', ctypes.c_char * 7),  # ///业务功能码
        ('BankID', ctypes.c_char * 4),  # ///银行代码
        ('BankBranchID', ctypes.c_char * 5),  # ///银行分支机构代码
        ('BrokerID', ctypes.c_char * 11),  # ///期商代码
        ('BrokerBranchID', ctypes.c_char * 31),  # ///期商分支机构代码
        ('TradeDate', ctypes.c_char * 9),  # ///交易日期
        ('TradeTime', ctypes.c_char * 9),  # ///交易时间
        ('BankSerial', ctypes.c_char * 13),  # ///银行流水号
        ('TradingDay', ctypes.c_char * 9),  # ///交易系统日期
        ('PlateSerial', ctypes.c_int),  # ///银期平台消息流水号
        ('LastFragment', ctypes.c_char * 1),  # ///最后分片标志
        ('SessionID', ctypes.c_int),  # ///会话号
        ('CustomerName', ctypes.c_char * 51),  # ///客户姓名
        ('IdCardType', ctypes.c_char * 1),  # ///证件类型
        ('IdentifiedCardNo', ctypes.c_char * 51),  # ///证件号码
        ('CustType', ctypes.c_char * 1),  # ///客户类型
        ('BankAccount', ctypes.c_char * 41),  # ///银行帐号
        ('BankPassWord', ctypes.c_char * 41),  # ///银行密码
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('Password', ctypes.c_char * 41),  # ///期货密码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('FutureSerial', ctypes.c_int),  # ///期货公司流水号
        ('UserID', ctypes.c_char * 16),  # ///用户标识
        ('VerifyCertNoFlag', ctypes.c_char * 1),  # ///验证客户证件号码标志
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('TradeAmount', ctypes.c_double),  # ///转帐金额
        ('FutureFetchAmount', ctypes.c_double),  # ///期货可取金额
        ('FeePayFlag', ctypes.c_char * 1),  # ///费用支付标志
        ('CustFee', ctypes.c_double),  # ///应收客户费用
        ('BrokerFee', ctypes.c_double),  # ///应收期货公司费用
        ('Message', ctypes.c_char * 129),  # ///发送方给接收方的消息
        ('Digest', ctypes.c_char * 36),  # ///摘要
        ('BankAccType', ctypes.c_char * 1),  # ///银行帐号类型
        ('DeviceID', ctypes.c_char * 3),  # ///渠道标志
        ('BankSecuAccType', ctypes.c_char * 1),  # ///期货单位帐号类型
        ('BrokerIDByBank', ctypes.c_char * 33),  # ///期货公司银行编码
        ('BankSecuAcc', ctypes.c_char * 41),  # ///期货单位帐号
        ('BankPwdFlag', ctypes.c_char * 1),  # ///银行密码标志
        ('SecuPwdFlag', ctypes.c_char * 1),  # ///期货资金密码核对标志
        ('OperNo', ctypes.c_char * 17),  # ///交易柜员
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('TID', ctypes.c_int),  # ///交易ID
        ('TransferStatus', ctypes.c_char * 1),  # ///转账交易状态
        ('LongCustomerName', ctypes.c_char * 161),  # ///长客户姓名
    ]


# ///冲正响应
class RspRepealField(BaseField):
    _fields_ = [
        ('RepealTimeInterval', ctypes.c_int),  # ///冲正时间间隔
        ('RepealedTimes', ctypes.c_int),  # ///已经冲正次数
        ('BankRepealFlag', ctypes.c_char * 1),  # ///银行冲正标志
        ('BrokerRepealFlag', ctypes.c_char * 1),  # ///期商冲正标志
        ('PlateRepealSerial', ctypes.c_int),  # ///被冲正平台流水号
        ('BankRepealSerial', ctypes.c_char * 13),  # ///被冲正银行流水号
        ('FutureRepealSerial', ctypes.c_int),  # ///被冲正期货流水号
        ('TradeCode', ctypes.c_char * 7),  # ///业务功能码
        ('BankID', ctypes.c_char * 4),  # ///银行代码
        ('BankBranchID', ctypes.c_char * 5),  # ///银行分支机构代码
        ('BrokerID', ctypes.c_char * 11),  # ///期商代码
        ('BrokerBranchID', ctypes.c_char * 31),  # ///期商分支机构代码
        ('TradeDate', ctypes.c_char * 9),  # ///交易日期
        ('TradeTime', ctypes.c_char * 9),  # ///交易时间
        ('BankSerial', ctypes.c_char * 13),  # ///银行流水号
        ('TradingDay', ctypes.c_char * 9),  # ///交易系统日期
        ('PlateSerial', ctypes.c_int),  # ///银期平台消息流水号
        ('LastFragment', ctypes.c_char * 1),  # ///最后分片标志
        ('SessionID', ctypes.c_int),  # ///会话号
        ('CustomerName', ctypes.c_char * 51),  # ///客户姓名
        ('IdCardType', ctypes.c_char * 1),  # ///证件类型
        ('IdentifiedCardNo', ctypes.c_char * 51),  # ///证件号码
        ('CustType', ctypes.c_char * 1),  # ///客户类型
        ('BankAccount', ctypes.c_char * 41),  # ///银行帐号
        ('BankPassWord', ctypes.c_char * 41),  # ///银行密码
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('Password', ctypes.c_char * 41),  # ///期货密码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('FutureSerial', ctypes.c_int),  # ///期货公司流水号
        ('UserID', ctypes.c_char * 16),  # ///用户标识
        ('VerifyCertNoFlag', ctypes.c_char * 1),  # ///验证客户证件号码标志
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('TradeAmount', ctypes.c_double),  # ///转帐金额
        ('FutureFetchAmount', ctypes.c_double),  # ///期货可取金额
        ('FeePayFlag', ctypes.c_char * 1),  # ///费用支付标志
        ('CustFee', ctypes.c_double),  # ///应收客户费用
        ('BrokerFee', ctypes.c_double),  # ///应收期货公司费用
        ('Message', ctypes.c_char * 129),  # ///发送方给接收方的消息
        ('Digest', ctypes.c_char * 36),  # ///摘要
        ('BankAccType', ctypes.c_char * 1),  # ///银行帐号类型
        ('DeviceID', ctypes.c_char * 3),  # ///渠道标志
        ('BankSecuAccType', ctypes.c_char * 1),  # ///期货单位帐号类型
        ('BrokerIDByBank', ctypes.c_char * 33),  # ///期货公司银行编码
        ('BankSecuAcc', ctypes.c_char * 41),  # ///期货单位帐号
        ('BankPwdFlag', ctypes.c_char * 1),  # ///银行密码标志
        ('SecuPwdFlag', ctypes.c_char * 1),  # ///期货资金密码核对标志
        ('OperNo', ctypes.c_char * 17),  # ///交易柜员
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('TID', ctypes.c_int),  # ///交易ID
        ('TransferStatus', ctypes.c_char * 1),  # ///转账交易状态
        ('ErrorID', ctypes.c_int),  # ///错误代码
        ('ErrorMsg', ctypes.c_char * 81),  # ///错误信息
        ('LongCustomerName', ctypes.c_char * 161),  # ///长客户姓名
    ]


# ///查询账户信息请求
class ReqQueryAccountField(BaseField):
    _fields_ = [
        ('TradeCode', ctypes.c_char * 7),  # ///业务功能码
        ('BankID', ctypes.c_char * 4),  # ///银行代码
        ('BankBranchID', ctypes.c_char * 5),  # ///银行分支机构代码
        ('BrokerID', ctypes.c_char * 11),  # ///期商代码
        ('BrokerBranchID', ctypes.c_char * 31),  # ///期商分支机构代码
        ('TradeDate', ctypes.c_char * 9),  # ///交易日期
        ('TradeTime', ctypes.c_char * 9),  # ///交易时间
        ('BankSerial', ctypes.c_char * 13),  # ///银行流水号
        ('TradingDay', ctypes.c_char * 9),  # ///交易系统日期
        ('PlateSerial', ctypes.c_int),  # ///银期平台消息流水号
        ('LastFragment', ctypes.c_char * 1),  # ///最后分片标志
        ('SessionID', ctypes.c_int),  # ///会话号
        ('CustomerName', ctypes.c_char * 51),  # ///客户姓名
        ('IdCardType', ctypes.c_char * 1),  # ///证件类型
        ('IdentifiedCardNo', ctypes.c_char * 51),  # ///证件号码
        ('CustType', ctypes.c_char * 1),  # ///客户类型
        ('BankAccount', ctypes.c_char * 41),  # ///银行帐号
        ('BankPassWord', ctypes.c_char * 41),  # ///银行密码
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('Password', ctypes.c_char * 41),  # ///期货密码
        ('FutureSerial', ctypes.c_int),  # ///期货公司流水号
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('UserID', ctypes.c_char * 16),  # ///用户标识
        ('VerifyCertNoFlag', ctypes.c_char * 1),  # ///验证客户证件号码标志
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('Digest', ctypes.c_char * 36),  # ///摘要
        ('BankAccType', ctypes.c_char * 1),  # ///银行帐号类型
        ('DeviceID', ctypes.c_char * 3),  # ///渠道标志
        ('BankSecuAccType', ctypes.c_char * 1),  # ///期货单位帐号类型
        ('BrokerIDByBank', ctypes.c_char * 33),  # ///期货公司银行编码
        ('BankSecuAcc', ctypes.c_char * 41),  # ///期货单位帐号
        ('BankPwdFlag', ctypes.c_char * 1),  # ///银行密码标志
        ('SecuPwdFlag', ctypes.c_char * 1),  # ///期货资金密码核对标志
        ('OperNo', ctypes.c_char * 17),  # ///交易柜员
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('TID', ctypes.c_int),  # ///交易ID
        ('LongCustomerName', ctypes.c_char * 161),  # ///长客户姓名
    ]


# ///查询账户信息响应
class RspQueryAccountField(BaseField):
    _fields_ = [
        ('TradeCode', ctypes.c_char * 7),  # ///业务功能码
        ('BankID', ctypes.c_char * 4),  # ///银行代码
        ('BankBranchID', ctypes.c_char * 5),  # ///银行分支机构代码
        ('BrokerID', ctypes.c_char * 11),  # ///期商代码
        ('BrokerBranchID', ctypes.c_char * 31),  # ///期商分支机构代码
        ('TradeDate', ctypes.c_char * 9),  # ///交易日期
        ('TradeTime', ctypes.c_char * 9),  # ///交易时间
        ('BankSerial', ctypes.c_char * 13),  # ///银行流水号
        ('TradingDay', ctypes.c_char * 9),  # ///交易系统日期
        ('PlateSerial', ctypes.c_int),  # ///银期平台消息流水号
        ('LastFragment', ctypes.c_char * 1),  # ///最后分片标志
        ('SessionID', ctypes.c_int),  # ///会话号
        ('CustomerName', ctypes.c_char * 51),  # ///客户姓名
        ('IdCardType', ctypes.c_char * 1),  # ///证件类型
        ('IdentifiedCardNo', ctypes.c_char * 51),  # ///证件号码
        ('CustType', ctypes.c_char * 1),  # ///客户类型
        ('BankAccount', ctypes.c_char * 41),  # ///银行帐号
        ('BankPassWord', ctypes.c_char * 41),  # ///银行密码
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('Password', ctypes.c_char * 41),  # ///期货密码
        ('FutureSerial', ctypes.c_int),  # ///期货公司流水号
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('UserID', ctypes.c_char * 16),  # ///用户标识
        ('VerifyCertNoFlag', ctypes.c_char * 1),  # ///验证客户证件号码标志
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('Digest', ctypes.c_char * 36),  # ///摘要
        ('BankAccType', ctypes.c_char * 1),  # ///银行帐号类型
        ('DeviceID', ctypes.c_char * 3),  # ///渠道标志
        ('BankSecuAccType', ctypes.c_char * 1),  # ///期货单位帐号类型
        ('BrokerIDByBank', ctypes.c_char * 33),  # ///期货公司银行编码
        ('BankSecuAcc', ctypes.c_char * 41),  # ///期货单位帐号
        ('BankPwdFlag', ctypes.c_char * 1),  # ///银行密码标志
        ('SecuPwdFlag', ctypes.c_char * 1),  # ///期货资金密码核对标志
        ('OperNo', ctypes.c_char * 17),  # ///交易柜员
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('TID', ctypes.c_int),  # ///交易ID
        ('BankUseAmount', ctypes.c_double),  # ///银行可用金额
        ('BankFetchAmount', ctypes.c_double),  # ///银行可取金额
        ('LongCustomerName', ctypes.c_char * 161),  # ///长客户姓名
    ]


# ///期商签到签退
class FutureSignIOField(BaseField):
    _fields_ = [
        ('TradeCode', ctypes.c_char * 7),  # ///业务功能码
        ('BankID', ctypes.c_char * 4),  # ///银行代码
        ('BankBranchID', ctypes.c_char * 5),  # ///银行分支机构代码
        ('BrokerID', ctypes.c_char * 11),  # ///期商代码
        ('BrokerBranchID', ctypes.c_char * 31),  # ///期商分支机构代码
        ('TradeDate', ctypes.c_char * 9),  # ///交易日期
        ('TradeTime', ctypes.c_char * 9),  # ///交易时间
        ('BankSerial', ctypes.c_char * 13),  # ///银行流水号
        ('TradingDay', ctypes.c_char * 9),  # ///交易系统日期
        ('PlateSerial', ctypes.c_int),  # ///银期平台消息流水号
        ('LastFragment', ctypes.c_char * 1),  # ///最后分片标志
        ('SessionID', ctypes.c_int),  # ///会话号
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('UserID', ctypes.c_char * 16),  # ///用户标识
        ('Digest', ctypes.c_char * 36),  # ///摘要
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('DeviceID', ctypes.c_char * 3),  # ///渠道标志
        ('BrokerIDByBank', ctypes.c_char * 33),  # ///期货公司银行编码
        ('OperNo', ctypes.c_char * 17),  # ///交易柜员
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('TID', ctypes.c_int),  # ///交易ID
    ]


# ///期商签到响应
class RspFutureSignInField(BaseField):
    _fields_ = [
        ('TradeCode', ctypes.c_char * 7),  # ///业务功能码
        ('BankID', ctypes.c_char * 4),  # ///银行代码
        ('BankBranchID', ctypes.c_char * 5),  # ///银行分支机构代码
        ('BrokerID', ctypes.c_char * 11),  # ///期商代码
        ('BrokerBranchID', ctypes.c_char * 31),  # ///期商分支机构代码
        ('TradeDate', ctypes.c_char * 9),  # ///交易日期
        ('TradeTime', ctypes.c_char * 9),  # ///交易时间
        ('BankSerial', ctypes.c_char * 13),  # ///银行流水号
        ('TradingDay', ctypes.c_char * 9),  # ///交易系统日期
        ('PlateSerial', ctypes.c_int),  # ///银期平台消息流水号
        ('LastFragment', ctypes.c_char * 1),  # ///最后分片标志
        ('SessionID', ctypes.c_int),  # ///会话号
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('UserID', ctypes.c_char * 16),  # ///用户标识
        ('Digest', ctypes.c_char * 36),  # ///摘要
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('DeviceID', ctypes.c_char * 3),  # ///渠道标志
        ('BrokerIDByBank', ctypes.c_char * 33),  # ///期货公司银行编码
        ('OperNo', ctypes.c_char * 17),  # ///交易柜员
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('TID', ctypes.c_int),  # ///交易ID
        ('ErrorID', ctypes.c_int),  # ///错误代码
        ('ErrorMsg', ctypes.c_char * 81),  # ///错误信息
        ('PinKey', ctypes.c_char * 129),  # ///PIN密钥
        ('MacKey', ctypes.c_char * 129),  # ///MAC密钥
    ]


# ///期商签退请求
class ReqFutureSignOutField(BaseField):
    _fields_ = [
        ('TradeCode', ctypes.c_char * 7),  # ///业务功能码
        ('BankID', ctypes.c_char * 4),  # ///银行代码
        ('BankBranchID', ctypes.c_char * 5),  # ///银行分支机构代码
        ('BrokerID', ctypes.c_char * 11),  # ///期商代码
        ('BrokerBranchID', ctypes.c_char * 31),  # ///期商分支机构代码
        ('TradeDate', ctypes.c_char * 9),  # ///交易日期
        ('TradeTime', ctypes.c_char * 9),  # ///交易时间
        ('BankSerial', ctypes.c_char * 13),  # ///银行流水号
        ('TradingDay', ctypes.c_char * 9),  # ///交易系统日期
        ('PlateSerial', ctypes.c_int),  # ///银期平台消息流水号
        ('LastFragment', ctypes.c_char * 1),  # ///最后分片标志
        ('SessionID', ctypes.c_int),  # ///会话号
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('UserID', ctypes.c_char * 16),  # ///用户标识
        ('Digest', ctypes.c_char * 36),  # ///摘要
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('DeviceID', ctypes.c_char * 3),  # ///渠道标志
        ('BrokerIDByBank', ctypes.c_char * 33),  # ///期货公司银行编码
        ('OperNo', ctypes.c_char * 17),  # ///交易柜员
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('TID', ctypes.c_int),  # ///交易ID
    ]


# ///期商签退响应
class RspFutureSignOutField(BaseField):
    _fields_ = [
        ('TradeCode', ctypes.c_char * 7),  # ///业务功能码
        ('BankID', ctypes.c_char * 4),  # ///银行代码
        ('BankBranchID', ctypes.c_char * 5),  # ///银行分支机构代码
        ('BrokerID', ctypes.c_char * 11),  # ///期商代码
        ('BrokerBranchID', ctypes.c_char * 31),  # ///期商分支机构代码
        ('TradeDate', ctypes.c_char * 9),  # ///交易日期
        ('TradeTime', ctypes.c_char * 9),  # ///交易时间
        ('BankSerial', ctypes.c_char * 13),  # ///银行流水号
        ('TradingDay', ctypes.c_char * 9),  # ///交易系统日期
        ('PlateSerial', ctypes.c_int),  # ///银期平台消息流水号
        ('LastFragment', ctypes.c_char * 1),  # ///最后分片标志
        ('SessionID', ctypes.c_int),  # ///会话号
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('UserID', ctypes.c_char * 16),  # ///用户标识
        ('Digest', ctypes.c_char * 36),  # ///摘要
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('DeviceID', ctypes.c_char * 3),  # ///渠道标志
        ('BrokerIDByBank', ctypes.c_char * 33),  # ///期货公司银行编码
        ('OperNo', ctypes.c_char * 17),  # ///交易柜员
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('TID', ctypes.c_int),  # ///交易ID
        ('ErrorID', ctypes.c_int),  # ///错误代码
        ('ErrorMsg', ctypes.c_char * 81),  # ///错误信息
    ]


# ///查询指定流水号的交易结果请求
class ReqQueryTradeResultBySerialField(BaseField):
    _fields_ = [
        ('TradeCode', ctypes.c_char * 7),  # ///业务功能码
        ('BankID', ctypes.c_char * 4),  # ///银行代码
        ('BankBranchID', ctypes.c_char * 5),  # ///银行分支机构代码
        ('BrokerID', ctypes.c_char * 11),  # ///期商代码
        ('BrokerBranchID', ctypes.c_char * 31),  # ///期商分支机构代码
        ('TradeDate', ctypes.c_char * 9),  # ///交易日期
        ('TradeTime', ctypes.c_char * 9),  # ///交易时间
        ('BankSerial', ctypes.c_char * 13),  # ///银行流水号
        ('TradingDay', ctypes.c_char * 9),  # ///交易系统日期
        ('PlateSerial', ctypes.c_int),  # ///银期平台消息流水号
        ('LastFragment', ctypes.c_char * 1),  # ///最后分片标志
        ('SessionID', ctypes.c_int),  # ///会话号
        ('Reference', ctypes.c_int),  # ///流水号
        ('RefrenceIssureType', ctypes.c_char * 1),  # ///本流水号发布者的机构类型
        ('RefrenceIssure', ctypes.c_char * 36),  # ///本流水号发布者机构编码
        ('CustomerName', ctypes.c_char * 51),  # ///客户姓名
        ('IdCardType', ctypes.c_char * 1),  # ///证件类型
        ('IdentifiedCardNo', ctypes.c_char * 51),  # ///证件号码
        ('CustType', ctypes.c_char * 1),  # ///客户类型
        ('BankAccount', ctypes.c_char * 41),  # ///银行帐号
        ('BankPassWord', ctypes.c_char * 41),  # ///银行密码
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('Password', ctypes.c_char * 41),  # ///期货密码
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('TradeAmount', ctypes.c_double),  # ///转帐金额
        ('Digest', ctypes.c_char * 36),  # ///摘要
        ('LongCustomerName', ctypes.c_char * 161),  # ///长客户姓名
    ]


# ///查询指定流水号的交易结果响应
class RspQueryTradeResultBySerialField(BaseField):
    _fields_ = [
        ('TradeCode', ctypes.c_char * 7),  # ///业务功能码
        ('BankID', ctypes.c_char * 4),  # ///银行代码
        ('BankBranchID', ctypes.c_char * 5),  # ///银行分支机构代码
        ('BrokerID', ctypes.c_char * 11),  # ///期商代码
        ('BrokerBranchID', ctypes.c_char * 31),  # ///期商分支机构代码
        ('TradeDate', ctypes.c_char * 9),  # ///交易日期
        ('TradeTime', ctypes.c_char * 9),  # ///交易时间
        ('BankSerial', ctypes.c_char * 13),  # ///银行流水号
        ('TradingDay', ctypes.c_char * 9),  # ///交易系统日期
        ('PlateSerial', ctypes.c_int),  # ///银期平台消息流水号
        ('LastFragment', ctypes.c_char * 1),  # ///最后分片标志
        ('SessionID', ctypes.c_int),  # ///会话号
        ('ErrorID', ctypes.c_int),  # ///错误代码
        ('ErrorMsg', ctypes.c_char * 81),  # ///错误信息
        ('Reference', ctypes.c_int),  # ///流水号
        ('RefrenceIssureType', ctypes.c_char * 1),  # ///本流水号发布者的机构类型
        ('RefrenceIssure', ctypes.c_char * 36),  # ///本流水号发布者机构编码
        ('OriginReturnCode', ctypes.c_char * 7),  # ///原始返回代码
        ('OriginDescrInfoForReturnCode', ctypes.c_char * 129),  # ///原始返回码描述
        ('BankAccount', ctypes.c_char * 41),  # ///银行帐号
        ('BankPassWord', ctypes.c_char * 41),  # ///银行密码
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('Password', ctypes.c_char * 41),  # ///期货密码
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('TradeAmount', ctypes.c_double),  # ///转帐金额
        ('Digest', ctypes.c_char * 36),  # ///摘要
    ]


# ///日终文件就绪请求
class ReqDayEndFileReadyField(BaseField):
    _fields_ = [
        ('TradeCode', ctypes.c_char * 7),  # ///业务功能码
        ('BankID', ctypes.c_char * 4),  # ///银行代码
        ('BankBranchID', ctypes.c_char * 5),  # ///银行分支机构代码
        ('BrokerID', ctypes.c_char * 11),  # ///期商代码
        ('BrokerBranchID', ctypes.c_char * 31),  # ///期商分支机构代码
        ('TradeDate', ctypes.c_char * 9),  # ///交易日期
        ('TradeTime', ctypes.c_char * 9),  # ///交易时间
        ('BankSerial', ctypes.c_char * 13),  # ///银行流水号
        ('TradingDay', ctypes.c_char * 9),  # ///交易系统日期
        ('PlateSerial', ctypes.c_int),  # ///银期平台消息流水号
        ('LastFragment', ctypes.c_char * 1),  # ///最后分片标志
        ('SessionID', ctypes.c_int),  # ///会话号
        ('FileBusinessCode', ctypes.c_char * 1),  # ///文件业务功能
        ('Digest', ctypes.c_char * 36),  # ///摘要
    ]


# ///返回结果
class ReturnResultField(BaseField):
    _fields_ = [
        ('ReturnCode', ctypes.c_char * 7),  # ///返回代码
        ('DescrInfoForReturnCode', ctypes.c_char * 129),  # ///返回码描述
    ]


# ///验证期货资金密码
class VerifyFuturePasswordField(BaseField):
    _fields_ = [
        ('TradeCode', ctypes.c_char * 7),  # ///业务功能码
        ('BankID', ctypes.c_char * 4),  # ///银行代码
        ('BankBranchID', ctypes.c_char * 5),  # ///银行分支机构代码
        ('BrokerID', ctypes.c_char * 11),  # ///期商代码
        ('BrokerBranchID', ctypes.c_char * 31),  # ///期商分支机构代码
        ('TradeDate', ctypes.c_char * 9),  # ///交易日期
        ('TradeTime', ctypes.c_char * 9),  # ///交易时间
        ('BankSerial', ctypes.c_char * 13),  # ///银行流水号
        ('TradingDay', ctypes.c_char * 9),  # ///交易系统日期
        ('PlateSerial', ctypes.c_int),  # ///银期平台消息流水号
        ('LastFragment', ctypes.c_char * 1),  # ///最后分片标志
        ('SessionID', ctypes.c_int),  # ///会话号
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('Password', ctypes.c_char * 41),  # ///期货密码
        ('BankAccount', ctypes.c_char * 41),  # ///银行帐号
        ('BankPassWord', ctypes.c_char * 41),  # ///银行密码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('TID', ctypes.c_int),  # ///交易ID
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
    ]


# ///验证客户信息
class VerifyCustInfoField(BaseField):
    _fields_ = [
        ('CustomerName', ctypes.c_char * 51),  # ///客户姓名
        ('IdCardType', ctypes.c_char * 1),  # ///证件类型
        ('IdentifiedCardNo', ctypes.c_char * 51),  # ///证件号码
        ('CustType', ctypes.c_char * 1),  # ///客户类型
        ('LongCustomerName', ctypes.c_char * 161),  # ///长客户姓名
    ]


# ///验证期货资金密码和客户信息
class VerifyFuturePasswordAndCustInfoField(BaseField):
    _fields_ = [
        ('CustomerName', ctypes.c_char * 51),  # ///客户姓名
        ('IdCardType', ctypes.c_char * 1),  # ///证件类型
        ('IdentifiedCardNo', ctypes.c_char * 51),  # ///证件号码
        ('CustType', ctypes.c_char * 1),  # ///客户类型
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('Password', ctypes.c_char * 41),  # ///期货密码
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('LongCustomerName', ctypes.c_char * 161),  # ///长客户姓名
    ]


# ///验证期货资金密码和客户信息
class DepositResultInformField(BaseField):
    _fields_ = [
        ('DepositSeqNo', ctypes.c_char * 15),  # ///出入金流水号，该流水号为银期报盘返回的流水号
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('Deposit', ctypes.c_double),  # ///入金金额
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('ReturnCode', ctypes.c_char * 7),  # ///返回代码
        ('DescrInfoForReturnCode', ctypes.c_char * 129),  # ///返回码描述
    ]


# ///交易核心向银期报盘发出密钥同步请求
class ReqSyncKeyField(BaseField):
    _fields_ = [
        ('TradeCode', ctypes.c_char * 7),  # ///业务功能码
        ('BankID', ctypes.c_char * 4),  # ///银行代码
        ('BankBranchID', ctypes.c_char * 5),  # ///银行分支机构代码
        ('BrokerID', ctypes.c_char * 11),  # ///期商代码
        ('BrokerBranchID', ctypes.c_char * 31),  # ///期商分支机构代码
        ('TradeDate', ctypes.c_char * 9),  # ///交易日期
        ('TradeTime', ctypes.c_char * 9),  # ///交易时间
        ('BankSerial', ctypes.c_char * 13),  # ///银行流水号
        ('TradingDay', ctypes.c_char * 9),  # ///交易系统日期
        ('PlateSerial', ctypes.c_int),  # ///银期平台消息流水号
        ('LastFragment', ctypes.c_char * 1),  # ///最后分片标志
        ('SessionID', ctypes.c_int),  # ///会话号
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('UserID', ctypes.c_char * 16),  # ///用户标识
        ('Message', ctypes.c_char * 129),  # ///交易核心给银期报盘的消息
        ('DeviceID', ctypes.c_char * 3),  # ///渠道标志
        ('BrokerIDByBank', ctypes.c_char * 33),  # ///期货公司银行编码
        ('OperNo', ctypes.c_char * 17),  # ///交易柜员
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('TID', ctypes.c_int),  # ///交易ID
    ]


# ///交易核心向银期报盘发出密钥同步响应
class RspSyncKeyField(BaseField):
    _fields_ = [
        ('TradeCode', ctypes.c_char * 7),  # ///业务功能码
        ('BankID', ctypes.c_char * 4),  # ///银行代码
        ('BankBranchID', ctypes.c_char * 5),  # ///银行分支机构代码
        ('BrokerID', ctypes.c_char * 11),  # ///期商代码
        ('BrokerBranchID', ctypes.c_char * 31),  # ///期商分支机构代码
        ('TradeDate', ctypes.c_char * 9),  # ///交易日期
        ('TradeTime', ctypes.c_char * 9),  # ///交易时间
        ('BankSerial', ctypes.c_char * 13),  # ///银行流水号
        ('TradingDay', ctypes.c_char * 9),  # ///交易系统日期
        ('PlateSerial', ctypes.c_int),  # ///银期平台消息流水号
        ('LastFragment', ctypes.c_char * 1),  # ///最后分片标志
        ('SessionID', ctypes.c_int),  # ///会话号
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('UserID', ctypes.c_char * 16),  # ///用户标识
        ('Message', ctypes.c_char * 129),  # ///交易核心给银期报盘的消息
        ('DeviceID', ctypes.c_char * 3),  # ///渠道标志
        ('BrokerIDByBank', ctypes.c_char * 33),  # ///期货公司银行编码
        ('OperNo', ctypes.c_char * 17),  # ///交易柜员
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('TID', ctypes.c_int),  # ///交易ID
        ('ErrorID', ctypes.c_int),  # ///错误代码
        ('ErrorMsg', ctypes.c_char * 81),  # ///错误信息
    ]


# ///查询账户信息通知
class NotifyQueryAccountField(BaseField):
    _fields_ = [
        ('TradeCode', ctypes.c_char * 7),  # ///业务功能码
        ('BankID', ctypes.c_char * 4),  # ///银行代码
        ('BankBranchID', ctypes.c_char * 5),  # ///银行分支机构代码
        ('BrokerID', ctypes.c_char * 11),  # ///期商代码
        ('BrokerBranchID', ctypes.c_char * 31),  # ///期商分支机构代码
        ('TradeDate', ctypes.c_char * 9),  # ///交易日期
        ('TradeTime', ctypes.c_char * 9),  # ///交易时间
        ('BankSerial', ctypes.c_char * 13),  # ///银行流水号
        ('TradingDay', ctypes.c_char * 9),  # ///交易系统日期
        ('PlateSerial', ctypes.c_int),  # ///银期平台消息流水号
        ('LastFragment', ctypes.c_char * 1),  # ///最后分片标志
        ('SessionID', ctypes.c_int),  # ///会话号
        ('CustomerName', ctypes.c_char * 51),  # ///客户姓名
        ('IdCardType', ctypes.c_char * 1),  # ///证件类型
        ('IdentifiedCardNo', ctypes.c_char * 51),  # ///证件号码
        ('CustType', ctypes.c_char * 1),  # ///客户类型
        ('BankAccount', ctypes.c_char * 41),  # ///银行帐号
        ('BankPassWord', ctypes.c_char * 41),  # ///银行密码
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('Password', ctypes.c_char * 41),  # ///期货密码
        ('FutureSerial', ctypes.c_int),  # ///期货公司流水号
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('UserID', ctypes.c_char * 16),  # ///用户标识
        ('VerifyCertNoFlag', ctypes.c_char * 1),  # ///验证客户证件号码标志
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('Digest', ctypes.c_char * 36),  # ///摘要
        ('BankAccType', ctypes.c_char * 1),  # ///银行帐号类型
        ('DeviceID', ctypes.c_char * 3),  # ///渠道标志
        ('BankSecuAccType', ctypes.c_char * 1),  # ///期货单位帐号类型
        ('BrokerIDByBank', ctypes.c_char * 33),  # ///期货公司银行编码
        ('BankSecuAcc', ctypes.c_char * 41),  # ///期货单位帐号
        ('BankPwdFlag', ctypes.c_char * 1),  # ///银行密码标志
        ('SecuPwdFlag', ctypes.c_char * 1),  # ///期货资金密码核对标志
        ('OperNo', ctypes.c_char * 17),  # ///交易柜员
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('TID', ctypes.c_int),  # ///交易ID
        ('BankUseAmount', ctypes.c_double),  # ///银行可用金额
        ('BankFetchAmount', ctypes.c_double),  # ///银行可取金额
        ('ErrorID', ctypes.c_int),  # ///错误代码
        ('ErrorMsg', ctypes.c_char * 81),  # ///错误信息
        ('LongCustomerName', ctypes.c_char * 161),  # ///长客户姓名
    ]


# ///银期转账交易流水表
class TransferSerialField(BaseField):
    _fields_ = [
        ('PlateSerial', ctypes.c_int),  # ///平台流水号
        ('TradeDate', ctypes.c_char * 9),  # ///交易发起方日期
        ('TradingDay', ctypes.c_char * 9),  # ///交易日期
        ('TradeTime', ctypes.c_char * 9),  # ///交易时间
        ('TradeCode', ctypes.c_char * 7),  # ///交易代码
        ('SessionID', ctypes.c_int),  # ///会话编号
        ('BankID', ctypes.c_char * 4),  # ///银行编码
        ('BankBranchID', ctypes.c_char * 5),  # ///银行分支机构编码
        ('BankAccType', ctypes.c_char * 1),  # ///银行帐号类型
        ('BankAccount', ctypes.c_char * 41),  # ///银行帐号
        ('BankSerial', ctypes.c_char * 13),  # ///银行流水号
        ('BrokerID', ctypes.c_char * 11),  # ///期货公司编码
        ('BrokerBranchID', ctypes.c_char * 31),  # ///期商分支机构代码
        ('FutureAccType', ctypes.c_char * 1),  # ///期货公司帐号类型
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('FutureSerial', ctypes.c_int),  # ///期货公司流水号
        ('IdCardType', ctypes.c_char * 1),  # ///证件类型
        ('IdentifiedCardNo', ctypes.c_char * 51),  # ///证件号码
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('TradeAmount', ctypes.c_double),  # ///交易金额
        ('CustFee', ctypes.c_double),  # ///应收客户费用
        ('BrokerFee', ctypes.c_double),  # ///应收期货公司费用
        ('AvailabilityFlag', ctypes.c_char * 1),  # ///有效标志
        ('OperatorCode', ctypes.c_char * 17),  # ///操作员
        ('BankNewAccount', ctypes.c_char * 41),  # ///新银行帐号
        ('ErrorID', ctypes.c_int),  # ///错误代码
        ('ErrorMsg', ctypes.c_char * 81),  # ///错误信息
    ]


# ///请求查询转帐流水
class QryTransferSerialField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('BankID', ctypes.c_char * 4),  # ///银行编码
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
    ]


# ///期商签到通知
class NotifyFutureSignInField(BaseField):
    _fields_ = [
        ('TradeCode', ctypes.c_char * 7),  # ///业务功能码
        ('BankID', ctypes.c_char * 4),  # ///银行代码
        ('BankBranchID', ctypes.c_char * 5),  # ///银行分支机构代码
        ('BrokerID', ctypes.c_char * 11),  # ///期商代码
        ('BrokerBranchID', ctypes.c_char * 31),  # ///期商分支机构代码
        ('TradeDate', ctypes.c_char * 9),  # ///交易日期
        ('TradeTime', ctypes.c_char * 9),  # ///交易时间
        ('BankSerial', ctypes.c_char * 13),  # ///银行流水号
        ('TradingDay', ctypes.c_char * 9),  # ///交易系统日期
        ('PlateSerial', ctypes.c_int),  # ///银期平台消息流水号
        ('LastFragment', ctypes.c_char * 1),  # ///最后分片标志
        ('SessionID', ctypes.c_int),  # ///会话号
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('UserID', ctypes.c_char * 16),  # ///用户标识
        ('Digest', ctypes.c_char * 36),  # ///摘要
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('DeviceID', ctypes.c_char * 3),  # ///渠道标志
        ('BrokerIDByBank', ctypes.c_char * 33),  # ///期货公司银行编码
        ('OperNo', ctypes.c_char * 17),  # ///交易柜员
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('TID', ctypes.c_int),  # ///交易ID
        ('ErrorID', ctypes.c_int),  # ///错误代码
        ('ErrorMsg', ctypes.c_char * 81),  # ///错误信息
        ('PinKey', ctypes.c_char * 129),  # ///PIN密钥
        ('MacKey', ctypes.c_char * 129),  # ///MAC密钥
    ]


# ///期商签退通知
class NotifyFutureSignOutField(BaseField):
    _fields_ = [
        ('TradeCode', ctypes.c_char * 7),  # ///业务功能码
        ('BankID', ctypes.c_char * 4),  # ///银行代码
        ('BankBranchID', ctypes.c_char * 5),  # ///银行分支机构代码
        ('BrokerID', ctypes.c_char * 11),  # ///期商代码
        ('BrokerBranchID', ctypes.c_char * 31),  # ///期商分支机构代码
        ('TradeDate', ctypes.c_char * 9),  # ///交易日期
        ('TradeTime', ctypes.c_char * 9),  # ///交易时间
        ('BankSerial', ctypes.c_char * 13),  # ///银行流水号
        ('TradingDay', ctypes.c_char * 9),  # ///交易系统日期
        ('PlateSerial', ctypes.c_int),  # ///银期平台消息流水号
        ('LastFragment', ctypes.c_char * 1),  # ///最后分片标志
        ('SessionID', ctypes.c_int),  # ///会话号
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('UserID', ctypes.c_char * 16),  # ///用户标识
        ('Digest', ctypes.c_char * 36),  # ///摘要
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('DeviceID', ctypes.c_char * 3),  # ///渠道标志
        ('BrokerIDByBank', ctypes.c_char * 33),  # ///期货公司银行编码
        ('OperNo', ctypes.c_char * 17),  # ///交易柜员
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('TID', ctypes.c_int),  # ///交易ID
        ('ErrorID', ctypes.c_int),  # ///错误代码
        ('ErrorMsg', ctypes.c_char * 81),  # ///错误信息
    ]


# ///交易核心向银期报盘发出密钥同步处理结果的通知
class NotifySyncKeyField(BaseField):
    _fields_ = [
        ('TradeCode', ctypes.c_char * 7),  # ///业务功能码
        ('BankID', ctypes.c_char * 4),  # ///银行代码
        ('BankBranchID', ctypes.c_char * 5),  # ///银行分支机构代码
        ('BrokerID', ctypes.c_char * 11),  # ///期商代码
        ('BrokerBranchID', ctypes.c_char * 31),  # ///期商分支机构代码
        ('TradeDate', ctypes.c_char * 9),  # ///交易日期
        ('TradeTime', ctypes.c_char * 9),  # ///交易时间
        ('BankSerial', ctypes.c_char * 13),  # ///银行流水号
        ('TradingDay', ctypes.c_char * 9),  # ///交易系统日期
        ('PlateSerial', ctypes.c_int),  # ///银期平台消息流水号
        ('LastFragment', ctypes.c_char * 1),  # ///最后分片标志
        ('SessionID', ctypes.c_int),  # ///会话号
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('UserID', ctypes.c_char * 16),  # ///用户标识
        ('Message', ctypes.c_char * 129),  # ///交易核心给银期报盘的消息
        ('DeviceID', ctypes.c_char * 3),  # ///渠道标志
        ('BrokerIDByBank', ctypes.c_char * 33),  # ///期货公司银行编码
        ('OperNo', ctypes.c_char * 17),  # ///交易柜员
        ('RequestID', ctypes.c_int),  # ///请求编号
        ('TID', ctypes.c_int),  # ///交易ID
        ('ErrorID', ctypes.c_int),  # ///错误代码
        ('ErrorMsg', ctypes.c_char * 81),  # ///错误信息
    ]


# ///请求查询银期签约关系
class QryAccountregisterField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('BankID', ctypes.c_char * 4),  # ///银行编码
        ('BankBranchID', ctypes.c_char * 5),  # ///银行分支机构编码
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
    ]


# ///客户开销户信息表
class AccountregisterField(BaseField):
    _fields_ = [
        ('TradeDay', ctypes.c_char * 9),  # ///交易日期
        ('BankID', ctypes.c_char * 4),  # ///银行编码
        ('BankBranchID', ctypes.c_char * 5),  # ///银行分支机构编码
        ('BankAccount', ctypes.c_char * 41),  # ///银行帐号
        ('BrokerID', ctypes.c_char * 11),  # ///期货公司编码
        ('BrokerBranchID', ctypes.c_char * 31),  # ///期货公司分支机构编码
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('IdCardType', ctypes.c_char * 1),  # ///证件类型
        ('IdentifiedCardNo', ctypes.c_char * 51),  # ///证件号码
        ('CustomerName', ctypes.c_char * 51),  # ///客户姓名
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('OpenOrDestroy', ctypes.c_char * 1),  # ///开销户类别
        ('RegDate', ctypes.c_char * 9),  # ///签约日期
        ('OutDate', ctypes.c_char * 9),  # ///解约日期
        ('TID', ctypes.c_int),  # ///交易ID
        ('CustType', ctypes.c_char * 1),  # ///客户类型
        ('BankAccType', ctypes.c_char * 1),  # ///银行帐号类型
        ('LongCustomerName', ctypes.c_char * 161),  # ///长客户姓名
    ]


# ///银期开户信息
class OpenAccountField(BaseField):
    _fields_ = [
        ('TradeCode', ctypes.c_char * 7),  # ///业务功能码
        ('BankID', ctypes.c_char * 4),  # ///银行代码
        ('BankBranchID', ctypes.c_char * 5),  # ///银行分支机构代码
        ('BrokerID', ctypes.c_char * 11),  # ///期商代码
        ('BrokerBranchID', ctypes.c_char * 31),  # ///期商分支机构代码
        ('TradeDate', ctypes.c_char * 9),  # ///交易日期
        ('TradeTime', ctypes.c_char * 9),  # ///交易时间
        ('BankSerial', ctypes.c_char * 13),  # ///银行流水号
        ('TradingDay', ctypes.c_char * 9),  # ///交易系统日期
        ('PlateSerial', ctypes.c_int),  # ///银期平台消息流水号
        ('LastFragment', ctypes.c_char * 1),  # ///最后分片标志
        ('SessionID', ctypes.c_int),  # ///会话号
        ('CustomerName', ctypes.c_char * 51),  # ///客户姓名
        ('IdCardType', ctypes.c_char * 1),  # ///证件类型
        ('IdentifiedCardNo', ctypes.c_char * 51),  # ///证件号码
        ('Gender', ctypes.c_char * 1),  # ///性别
        ('CountryCode', ctypes.c_char * 21),  # ///国家代码
        ('CustType', ctypes.c_char * 1),  # ///客户类型
        ('Address', ctypes.c_char * 101),  # ///地址
        ('ZipCode', ctypes.c_char * 7),  # ///邮编
        ('Telephone', ctypes.c_char * 41),  # ///电话号码
        ('MobilePhone', ctypes.c_char * 21),  # ///手机
        ('Fax', ctypes.c_char * 41),  # ///传真
        ('EMail', ctypes.c_char * 41),  # ///电子邮件
        ('MoneyAccountStatus', ctypes.c_char * 1),  # ///资金账户状态
        ('BankAccount', ctypes.c_char * 41),  # ///银行帐号
        ('BankPassWord', ctypes.c_char * 41),  # ///银行密码
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('Password', ctypes.c_char * 41),  # ///期货密码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('VerifyCertNoFlag', ctypes.c_char * 1),  # ///验证客户证件号码标志
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('CashExchangeCode', ctypes.c_char * 1),  # ///汇钞标志
        ('Digest', ctypes.c_char * 36),  # ///摘要
        ('BankAccType', ctypes.c_char * 1),  # ///银行帐号类型
        ('DeviceID', ctypes.c_char * 3),  # ///渠道标志
        ('BankSecuAccType', ctypes.c_char * 1),  # ///期货单位帐号类型
        ('BrokerIDByBank', ctypes.c_char * 33),  # ///期货公司银行编码
        ('BankSecuAcc', ctypes.c_char * 41),  # ///期货单位帐号
        ('BankPwdFlag', ctypes.c_char * 1),  # ///银行密码标志
        ('SecuPwdFlag', ctypes.c_char * 1),  # ///期货资金密码核对标志
        ('OperNo', ctypes.c_char * 17),  # ///交易柜员
        ('TID', ctypes.c_int),  # ///交易ID
        ('UserID', ctypes.c_char * 16),  # ///用户标识
        ('ErrorID', ctypes.c_int),  # ///错误代码
        ('ErrorMsg', ctypes.c_char * 81),  # ///错误信息
        ('LongCustomerName', ctypes.c_char * 161),  # ///长客户姓名
    ]


# ///银期销户信息
class CancelAccountField(BaseField):
    _fields_ = [
        ('TradeCode', ctypes.c_char * 7),  # ///业务功能码
        ('BankID', ctypes.c_char * 4),  # ///银行代码
        ('BankBranchID', ctypes.c_char * 5),  # ///银行分支机构代码
        ('BrokerID', ctypes.c_char * 11),  # ///期商代码
        ('BrokerBranchID', ctypes.c_char * 31),  # ///期商分支机构代码
        ('TradeDate', ctypes.c_char * 9),  # ///交易日期
        ('TradeTime', ctypes.c_char * 9),  # ///交易时间
        ('BankSerial', ctypes.c_char * 13),  # ///银行流水号
        ('TradingDay', ctypes.c_char * 9),  # ///交易系统日期
        ('PlateSerial', ctypes.c_int),  # ///银期平台消息流水号
        ('LastFragment', ctypes.c_char * 1),  # ///最后分片标志
        ('SessionID', ctypes.c_int),  # ///会话号
        ('CustomerName', ctypes.c_char * 51),  # ///客户姓名
        ('IdCardType', ctypes.c_char * 1),  # ///证件类型
        ('IdentifiedCardNo', ctypes.c_char * 51),  # ///证件号码
        ('Gender', ctypes.c_char * 1),  # ///性别
        ('CountryCode', ctypes.c_char * 21),  # ///国家代码
        ('CustType', ctypes.c_char * 1),  # ///客户类型
        ('Address', ctypes.c_char * 101),  # ///地址
        ('ZipCode', ctypes.c_char * 7),  # ///邮编
        ('Telephone', ctypes.c_char * 41),  # ///电话号码
        ('MobilePhone', ctypes.c_char * 21),  # ///手机
        ('Fax', ctypes.c_char * 41),  # ///传真
        ('EMail', ctypes.c_char * 41),  # ///电子邮件
        ('MoneyAccountStatus', ctypes.c_char * 1),  # ///资金账户状态
        ('BankAccount', ctypes.c_char * 41),  # ///银行帐号
        ('BankPassWord', ctypes.c_char * 41),  # ///银行密码
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('Password', ctypes.c_char * 41),  # ///期货密码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('VerifyCertNoFlag', ctypes.c_char * 1),  # ///验证客户证件号码标志
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('CashExchangeCode', ctypes.c_char * 1),  # ///汇钞标志
        ('Digest', ctypes.c_char * 36),  # ///摘要
        ('BankAccType', ctypes.c_char * 1),  # ///银行帐号类型
        ('DeviceID', ctypes.c_char * 3),  # ///渠道标志
        ('BankSecuAccType', ctypes.c_char * 1),  # ///期货单位帐号类型
        ('BrokerIDByBank', ctypes.c_char * 33),  # ///期货公司银行编码
        ('BankSecuAcc', ctypes.c_char * 41),  # ///期货单位帐号
        ('BankPwdFlag', ctypes.c_char * 1),  # ///银行密码标志
        ('SecuPwdFlag', ctypes.c_char * 1),  # ///期货资金密码核对标志
        ('OperNo', ctypes.c_char * 17),  # ///交易柜员
        ('TID', ctypes.c_int),  # ///交易ID
        ('UserID', ctypes.c_char * 16),  # ///用户标识
        ('ErrorID', ctypes.c_int),  # ///错误代码
        ('ErrorMsg', ctypes.c_char * 81),  # ///错误信息
        ('LongCustomerName', ctypes.c_char * 161),  # ///长客户姓名
    ]


# ///银期变更银行账号信息
class ChangeAccountField(BaseField):
    _fields_ = [
        ('TradeCode', ctypes.c_char * 7),  # ///业务功能码
        ('BankID', ctypes.c_char * 4),  # ///银行代码
        ('BankBranchID', ctypes.c_char * 5),  # ///银行分支机构代码
        ('BrokerID', ctypes.c_char * 11),  # ///期商代码
        ('BrokerBranchID', ctypes.c_char * 31),  # ///期商分支机构代码
        ('TradeDate', ctypes.c_char * 9),  # ///交易日期
        ('TradeTime', ctypes.c_char * 9),  # ///交易时间
        ('BankSerial', ctypes.c_char * 13),  # ///银行流水号
        ('TradingDay', ctypes.c_char * 9),  # ///交易系统日期
        ('PlateSerial', ctypes.c_int),  # ///银期平台消息流水号
        ('LastFragment', ctypes.c_char * 1),  # ///最后分片标志
        ('SessionID', ctypes.c_int),  # ///会话号
        ('CustomerName', ctypes.c_char * 51),  # ///客户姓名
        ('IdCardType', ctypes.c_char * 1),  # ///证件类型
        ('IdentifiedCardNo', ctypes.c_char * 51),  # ///证件号码
        ('Gender', ctypes.c_char * 1),  # ///性别
        ('CountryCode', ctypes.c_char * 21),  # ///国家代码
        ('CustType', ctypes.c_char * 1),  # ///客户类型
        ('Address', ctypes.c_char * 101),  # ///地址
        ('ZipCode', ctypes.c_char * 7),  # ///邮编
        ('Telephone', ctypes.c_char * 41),  # ///电话号码
        ('MobilePhone', ctypes.c_char * 21),  # ///手机
        ('Fax', ctypes.c_char * 41),  # ///传真
        ('EMail', ctypes.c_char * 41),  # ///电子邮件
        ('MoneyAccountStatus', ctypes.c_char * 1),  # ///资金账户状态
        ('BankAccount', ctypes.c_char * 41),  # ///银行帐号
        ('BankPassWord', ctypes.c_char * 41),  # ///银行密码
        ('NewBankAccount', ctypes.c_char * 41),  # ///新银行帐号
        ('NewBankPassWord', ctypes.c_char * 41),  # ///新银行密码
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('Password', ctypes.c_char * 41),  # ///期货密码
        ('BankAccType', ctypes.c_char * 1),  # ///银行帐号类型
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('VerifyCertNoFlag', ctypes.c_char * 1),  # ///验证客户证件号码标志
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('BrokerIDByBank', ctypes.c_char * 33),  # ///期货公司银行编码
        ('BankPwdFlag', ctypes.c_char * 1),  # ///银行密码标志
        ('SecuPwdFlag', ctypes.c_char * 1),  # ///期货资金密码核对标志
        ('TID', ctypes.c_int),  # ///交易ID
        ('Digest', ctypes.c_char * 36),  # ///摘要
        ('ErrorID', ctypes.c_int),  # ///错误代码
        ('ErrorMsg', ctypes.c_char * 81),  # ///错误信息
        ('LongCustomerName', ctypes.c_char * 161),  # ///长客户姓名
    ]


# ///二级代理操作员银期权限
class SecAgentACIDMapField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('AccountID', ctypes.c_char * 13),  # ///资金账户
        ('CurrencyID', ctypes.c_char * 4),  # ///币种
        ('BrokerSecAgentID', ctypes.c_char * 13),  # ///境外中介机构资金帐号
    ]


# ///二级代理操作员银期权限查询
class QrySecAgentACIDMapField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('AccountID', ctypes.c_char * 13),  # ///资金账户
        ('CurrencyID', ctypes.c_char * 4),  # ///币种
    ]


# ///灾备中心交易权限
class UserRightsAssignField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///应用单元代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('DRIdentityID', ctypes.c_int),  # ///交易中心代码
    ]


# ///经济公司是否有在本标示的交易权限
class BrokerUserRightAssignField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///应用单元代码
        ('DRIdentityID', ctypes.c_int),  # ///交易中心代码
        ('Tradeable', ctypes.c_int),  # ///能否交易
    ]


# ///灾备交易转换报文
class DRTransferField(BaseField):
    _fields_ = [
        ('OrigDRIdentityID', ctypes.c_int),  # ///原交易中心代码
        ('DestDRIdentityID', ctypes.c_int),  # ///目标交易中心代码
        ('OrigBrokerID', ctypes.c_char * 11),  # ///原应用单元代码
        ('DestBrokerID', ctypes.c_char * 11),  # ///目标易用单元代码
    ]


# ///Fens用户信息
class FensUserInfoField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('LoginMode', ctypes.c_char * 1),  # ///登录模式
    ]


# ///当前银期所属交易中心
class CurrTransferIdentityField(BaseField):
    _fields_ = [
        ('IdentityID', ctypes.c_int),  # ///交易中心代码
    ]


# ///禁止登录用户
class LoginForbiddenUserField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('reserve1', ctypes.c_char * 16),  # ///保留的无效字段
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///查询禁止登录用户
class QryLoginForbiddenUserField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
    ]


# ///资金账户基本准备金
class TradingAccountReserveField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('Reserve', ctypes.c_double),  # ///基本准备金
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
    ]


# ///查询禁止登录IP
class QryLoginForbiddenIPField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 16),  # ///保留的无效字段
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///查询IP列表
class QryIPListField(BaseField):
    _fields_ = [
        ('reserve1', ctypes.c_char * 16),  # ///保留的无效字段
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///查询用户下单权限分配表
class QryUserRightsAssignField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///应用单元代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
    ]


# ///银期预约开户确认请求
class ReserveOpenAccountConfirmField(BaseField):
    _fields_ = [
        ('TradeCode', ctypes.c_char * 7),  # ///业务功能码
        ('BankID', ctypes.c_char * 4),  # ///银行代码
        ('BankBranchID', ctypes.c_char * 5),  # ///银行分支机构代码
        ('BrokerID', ctypes.c_char * 11),  # ///期商代码
        ('BrokerBranchID', ctypes.c_char * 31),  # ///期商分支机构代码
        ('TradeDate', ctypes.c_char * 9),  # ///交易日期
        ('TradeTime', ctypes.c_char * 9),  # ///交易时间
        ('BankSerial', ctypes.c_char * 13),  # ///银行流水号
        ('TradingDay', ctypes.c_char * 9),  # ///交易系统日期
        ('PlateSerial', ctypes.c_int),  # ///银期平台消息流水号
        ('LastFragment', ctypes.c_char * 1),  # ///最后分片标志
        ('SessionID', ctypes.c_int),  # ///会话号
        ('CustomerName', ctypes.c_char * 161),  # ///客户姓名
        ('IdCardType', ctypes.c_char * 1),  # ///证件类型
        ('IdentifiedCardNo', ctypes.c_char * 51),  # ///证件号码
        ('Gender', ctypes.c_char * 1),  # ///性别
        ('CountryCode', ctypes.c_char * 21),  # ///国家代码
        ('CustType', ctypes.c_char * 1),  # ///客户类型
        ('Address', ctypes.c_char * 101),  # ///地址
        ('ZipCode', ctypes.c_char * 7),  # ///邮编
        ('Telephone', ctypes.c_char * 41),  # ///电话号码
        ('MobilePhone', ctypes.c_char * 21),  # ///手机
        ('Fax', ctypes.c_char * 41),  # ///传真
        ('EMail', ctypes.c_char * 41),  # ///电子邮件
        ('MoneyAccountStatus', ctypes.c_char * 1),  # ///资金账户状态
        ('BankAccount', ctypes.c_char * 41),  # ///银行帐号
        ('BankPassWord', ctypes.c_char * 41),  # ///银行密码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('VerifyCertNoFlag', ctypes.c_char * 1),  # ///验证客户证件号码标志
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('Digest', ctypes.c_char * 36),  # ///摘要
        ('BankAccType', ctypes.c_char * 1),  # ///银行帐号类型
        ('BrokerIDByBank', ctypes.c_char * 33),  # ///期货公司银行编码
        ('TID', ctypes.c_int),  # ///交易ID
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('Password', ctypes.c_char * 41),  # ///期货密码
        ('BankReserveOpenSeq', ctypes.c_char * 13),  # ///预约开户银行流水号
        ('BookDate', ctypes.c_char * 9),  # ///预约开户日期
        ('BookPsw', ctypes.c_char * 41),  # ///预约开户验证密码
        ('ErrorID', ctypes.c_int),  # ///错误代码
        ('ErrorMsg', ctypes.c_char * 81),  # ///错误信息
    ]


# ///银期预约开户
class ReserveOpenAccountField(BaseField):
    _fields_ = [
        ('TradeCode', ctypes.c_char * 7),  # ///业务功能码
        ('BankID', ctypes.c_char * 4),  # ///银行代码
        ('BankBranchID', ctypes.c_char * 5),  # ///银行分支机构代码
        ('BrokerID', ctypes.c_char * 11),  # ///期商代码
        ('BrokerBranchID', ctypes.c_char * 31),  # ///期商分支机构代码
        ('TradeDate', ctypes.c_char * 9),  # ///交易日期
        ('TradeTime', ctypes.c_char * 9),  # ///交易时间
        ('BankSerial', ctypes.c_char * 13),  # ///银行流水号
        ('TradingDay', ctypes.c_char * 9),  # ///交易系统日期
        ('PlateSerial', ctypes.c_int),  # ///银期平台消息流水号
        ('LastFragment', ctypes.c_char * 1),  # ///最后分片标志
        ('SessionID', ctypes.c_int),  # ///会话号
        ('CustomerName', ctypes.c_char * 161),  # ///客户姓名
        ('IdCardType', ctypes.c_char * 1),  # ///证件类型
        ('IdentifiedCardNo', ctypes.c_char * 51),  # ///证件号码
        ('Gender', ctypes.c_char * 1),  # ///性别
        ('CountryCode', ctypes.c_char * 21),  # ///国家代码
        ('CustType', ctypes.c_char * 1),  # ///客户类型
        ('Address', ctypes.c_char * 101),  # ///地址
        ('ZipCode', ctypes.c_char * 7),  # ///邮编
        ('Telephone', ctypes.c_char * 41),  # ///电话号码
        ('MobilePhone', ctypes.c_char * 21),  # ///手机
        ('Fax', ctypes.c_char * 41),  # ///传真
        ('EMail', ctypes.c_char * 41),  # ///电子邮件
        ('MoneyAccountStatus', ctypes.c_char * 1),  # ///资金账户状态
        ('BankAccount', ctypes.c_char * 41),  # ///银行帐号
        ('BankPassWord', ctypes.c_char * 41),  # ///银行密码
        ('InstallID', ctypes.c_int),  # ///安装编号
        ('VerifyCertNoFlag', ctypes.c_char * 1),  # ///验证客户证件号码标志
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('Digest', ctypes.c_char * 36),  # ///摘要
        ('BankAccType', ctypes.c_char * 1),  # ///银行帐号类型
        ('BrokerIDByBank', ctypes.c_char * 33),  # ///期货公司银行编码
        ('TID', ctypes.c_int),  # ///交易ID
        ('ReserveOpenAccStas', ctypes.c_char * 1),  # ///预约开户状态
        ('ErrorID', ctypes.c_int),  # ///错误代码
        ('ErrorMsg', ctypes.c_char * 81),  # ///错误信息
    ]


# ///银行账户属性
class AccountPropertyField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('BankID', ctypes.c_char * 4),  # ///银行统一标识类型
        ('BankAccount', ctypes.c_char * 41),  # ///银行账户
        ('OpenName', ctypes.c_char * 101),  # ///银行账户的开户人名称
        ('OpenBank', ctypes.c_char * 101),  # ///银行账户的开户行
        ('IsActive', ctypes.c_int),  # ///是否活跃
        ('AccountSourceType', ctypes.c_char * 1),  # ///账户来源
        ('OpenDate', ctypes.c_char * 9),  # ///开户日期
        ('CancelDate', ctypes.c_char * 9),  # ///注销日期
        ('OperatorID', ctypes.c_char * 65),  # ///录入员代码
        ('OperateDate', ctypes.c_char * 9),  # ///录入日期
        ('OperateTime', ctypes.c_char * 9),  # ///录入时间
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
    ]


# ///查询当前交易中心
class QryCurrDRIdentityField(BaseField):
    _fields_ = [
        ('DRIdentityID', ctypes.c_int),  # ///交易中心代码
    ]


# ///当前交易中心
class CurrDRIdentityField(BaseField):
    _fields_ = [
        ('DRIdentityID', ctypes.c_int),  # ///交易中心代码
    ]


# ///查询二级代理商资金校验模式
class QrySecAgentCheckModeField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
    ]


# ///查询二级代理商信息
class QrySecAgentTradeInfoField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('BrokerSecAgentID', ctypes.c_char * 13),  # ///境外中介机构资金帐号
    ]


# ///用户发出获取安全安全登陆方法请求
class ReqUserAuthMethodField(BaseField):
    _fields_ = [
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
    ]


# ///用户发出获取安全安全登陆方法回复
class RspUserAuthMethodField(BaseField):
    _fields_ = [
        ('UsableAuthMethod', ctypes.c_int),  # ///当前可以用的认证模式
    ]


# ///用户发出获取安全安全登陆方法请求
class ReqGenUserCaptchaField(BaseField):
    _fields_ = [
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
    ]


# ///生成的图片验证码信息
class RspGenUserCaptchaField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('CaptchaInfoLen', ctypes.c_int),  # ///图片信息长度
        ('CaptchaInfo', ctypes.c_char * 2561),  # ///图片信息
    ]


# ///用户发出获取安全安全登陆方法请求
class ReqGenUserTextField(BaseField):
    _fields_ = [
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
    ]


# ///短信验证码生成的回复
class RspGenUserTextField(BaseField):
    _fields_ = [
        ('UserTextSeq', ctypes.c_int),  # ///短信验证码序号
    ]


# ///用户发出带图形验证码的登录请求请求
class ReqUserLoginWithCaptchaField(BaseField):
    _fields_ = [
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('Password', ctypes.c_char * 41),  # ///密码
        ('UserProductInfo', ctypes.c_char * 11),  # ///用户端产品信息
        ('InterfaceProductInfo', ctypes.c_char * 11),  # ///接口端产品信息
        ('ProtocolInfo', ctypes.c_char * 11),  # ///协议信息
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('reserve1', ctypes.c_char * 16),  # ///保留的无效字段
        ('LoginRemark', ctypes.c_char * 36),  # ///登录备注
        ('Captcha', ctypes.c_char * 41),  # ///图形验证码的文字内容
        ('ClientIPPort', ctypes.c_int),  # ///终端IP端口
        ('ClientIPAddress', ctypes.c_char * 33),  # ///终端IP地址
    ]


# ///用户发出带短信验证码的登录请求请求
class ReqUserLoginWithTextField(BaseField):
    _fields_ = [
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('Password', ctypes.c_char * 41),  # ///密码
        ('UserProductInfo', ctypes.c_char * 11),  # ///用户端产品信息
        ('InterfaceProductInfo', ctypes.c_char * 11),  # ///接口端产品信息
        ('ProtocolInfo', ctypes.c_char * 11),  # ///协议信息
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('reserve1', ctypes.c_char * 16),  # ///保留的无效字段
        ('LoginRemark', ctypes.c_char * 36),  # ///登录备注
        ('Text', ctypes.c_char * 41),  # ///短信验证码文字内容
        ('ClientIPPort', ctypes.c_int),  # ///终端IP端口
        ('ClientIPAddress', ctypes.c_char * 33),  # ///终端IP地址
    ]


# ///用户发出带动态验证码的登录请求请求
class ReqUserLoginWithOTPField(BaseField):
    _fields_ = [
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('Password', ctypes.c_char * 41),  # ///密码
        ('UserProductInfo', ctypes.c_char * 11),  # ///用户端产品信息
        ('InterfaceProductInfo', ctypes.c_char * 11),  # ///接口端产品信息
        ('ProtocolInfo', ctypes.c_char * 11),  # ///协议信息
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('reserve1', ctypes.c_char * 16),  # ///保留的无效字段
        ('LoginRemark', ctypes.c_char * 36),  # ///登录备注
        ('OTPPassword', ctypes.c_char * 41),  # ///OTP密码
        ('ClientIPPort', ctypes.c_int),  # ///终端IP端口
        ('ClientIPAddress', ctypes.c_char * 33),  # ///终端IP地址
    ]


# ///api握手请求
class ReqApiHandshakeField(BaseField):
    _fields_ = [
        ('CryptoKeyVersion', ctypes.c_char * 31),  # ///api与front通信密钥版本号
    ]


# ///front发给api的握手回复
class RspApiHandshakeField(BaseField):
    _fields_ = [
        ('FrontHandshakeDataLen', ctypes.c_int),  # ///握手回复数据长度
        ('FrontHandshakeData', ctypes.c_char * 301),  # ///握手回复数据
        ('IsApiAuthEnabled', ctypes.c_int),  # ///API认证是否开启
    ]


# ///api给front的验证key的请求
class ReqVerifyApiKeyField(BaseField):
    _fields_ = [
        ('ApiHandshakeDataLen', ctypes.c_int),  # ///握手回复数据长度
        ('ApiHandshakeData', ctypes.c_char * 301),  # ///握手回复数据
    ]


# ///操作员组织架构关系
class DepartmentUserField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('InvestorRange', ctypes.c_char * 1),  # ///投资者范围
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
    ]


# ///查询频率，每秒查询比数
class QueryFreqField(BaseField):
    _fields_ = [
        ('QueryFreq', ctypes.c_int),  # ///查询频率
    ]


# ///禁止认证IP
class AuthForbiddenIPField(BaseField):
    _fields_ = [
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///查询禁止认证IP
class QryAuthForbiddenIPField(BaseField):
    _fields_ = [
        ('IPAddress', ctypes.c_char * 33),  # ///IP地址
    ]


# ///换汇可提冻结
class SyncDelaySwapFrozenField(BaseField):
    _fields_ = [
        ('DelaySwapSeqNo', ctypes.c_char * 15),  # ///换汇流水号
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('FromCurrencyID', ctypes.c_char * 4),  # ///源币种
        ('FromRemainSwap', ctypes.c_double),  # ///源剩余换汇额度(可提冻结)
        ('IsManualSwap', ctypes.c_int),  # ///是否手工换汇
    ]


# ///用户系统信息
class UserSystemInfoField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('ClientSystemInfoLen', ctypes.c_int),  # ///用户端系统内部信息长度
        ('ClientSystemInfo', ctypes.c_char * 273),  # ///用户端系统内部信息
        ('reserve1', ctypes.c_char * 16),  # ///保留的无效字段
        ('ClientIPPort', ctypes.c_int),  # ///终端IP端口
        ('ClientLoginTime', ctypes.c_char * 9),  # ///登录成功时间
        ('ClientAppID', ctypes.c_char * 33),  # ///App代码
        ('ClientPublicIP', ctypes.c_char * 33),  # ///用户公网IP
        ('ClientLoginRemark', ctypes.c_char * 151),  # ///客户登录备注2
    ]


# ///终端用户绑定信息
class AuthUserIDField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('AppID', ctypes.c_char * 33),  # ///App代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('AuthType', ctypes.c_char * 1),  # ///校验类型
    ]


# ///用户IP绑定信息
class AuthIPField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('AppID', ctypes.c_char * 33),  # ///App代码
        ('IPAddress', ctypes.c_char * 33),  # ///用户代码
    ]


# ///查询分类合约
class QryClassifiedInstrumentField(BaseField):
    _fields_ = [
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ExchangeInstID', ctypes.c_char * 81),  # ///合约在交易所的代码
        ('ProductID', ctypes.c_char * 81),  # ///产品代码
        ('TradingType', ctypes.c_char * 1),  # ///合约交易状态
        ('ClassType', ctypes.c_char * 1),  # ///合约分类类型
    ]


# ///查询组合优惠比例
class QryCombPromotionParamField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///组合优惠比例
class CombPromotionParamField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('CombHedgeFlag', ctypes.c_char * 5),  # ///投机套保标志
        ('Xparameter', ctypes.c_double),  # ///期权组合保证金比例
    ]


# ///国密用户登录请求
class ReqUserLoginSCField(BaseField):
    _fields_ = [
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('UserID', ctypes.c_char * 16),  # ///用户代码
        ('Password', ctypes.c_char * 41),  # ///密码
        ('UserProductInfo', ctypes.c_char * 11),  # ///用户端产品信息
        ('InterfaceProductInfo', ctypes.c_char * 11),  # ///接口端产品信息
        ('ProtocolInfo', ctypes.c_char * 11),  # ///协议信息
        ('MacAddress', ctypes.c_char * 21),  # ///Mac地址
        ('OneTimePassword', ctypes.c_char * 41),  # ///动态密码
        ('ClientIPAddress', ctypes.c_char * 33),  # ///终端IP地址
        ('LoginRemark', ctypes.c_char * 36),  # ///登录备注
        ('ClientIPPort', ctypes.c_int),  # ///终端IP端口
        ('AuthCode', ctypes.c_char * 17),  # ///认证码
        ('AppID', ctypes.c_char * 33),  # ///App代码
    ]


# ///投资者风险结算持仓查询
class QryRiskSettleInvstPositionField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
    ]


# ///风险结算产品查询
class QryRiskSettleProductStatusField(BaseField):
    _fields_ = [
        ('ProductID', ctypes.c_char * 81),  # ///产品代码
    ]


# ///投资者风险结算持仓
class RiskSettleInvstPositionField(BaseField):
    _fields_ = [
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('PosiDirection', ctypes.c_char * 1),  # ///持仓多空方向
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('PositionDate', ctypes.c_char * 1),  # ///持仓日期
        ('YdPosition', ctypes.c_int),  # ///上日持仓
        ('Position', ctypes.c_int),  # ///今日持仓
        ('LongFrozen', ctypes.c_int),  # ///多头冻结
        ('ShortFrozen', ctypes.c_int),  # ///空头冻结
        ('LongFrozenAmount', ctypes.c_double),  # ///开仓冻结金额
        ('ShortFrozenAmount', ctypes.c_double),  # ///开仓冻结金额
        ('OpenVolume', ctypes.c_int),  # ///开仓量
        ('CloseVolume', ctypes.c_int),  # ///平仓量
        ('OpenAmount', ctypes.c_double),  # ///开仓金额
        ('CloseAmount', ctypes.c_double),  # ///平仓金额
        ('PositionCost', ctypes.c_double),  # ///持仓成本
        ('PreMargin', ctypes.c_double),  # ///上次占用的保证金
        ('UseMargin', ctypes.c_double),  # ///占用的保证金
        ('FrozenMargin', ctypes.c_double),  # ///冻结的保证金
        ('FrozenCash', ctypes.c_double),  # ///冻结的资金
        ('FrozenCommission', ctypes.c_double),  # ///冻结的手续费
        ('CashIn', ctypes.c_double),  # ///资金差额
        ('Commission', ctypes.c_double),  # ///手续费
        ('CloseProfit', ctypes.c_double),  # ///平仓盈亏
        ('PositionProfit', ctypes.c_double),  # ///持仓盈亏
        ('PreSettlementPrice', ctypes.c_double),  # ///上次结算价
        ('SettlementPrice', ctypes.c_double),  # ///本次结算价
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('SettlementID', ctypes.c_int),  # ///结算编号
        ('OpenCost', ctypes.c_double),  # ///开仓成本
        ('ExchangeMargin', ctypes.c_double),  # ///交易所保证金
        ('CombPosition', ctypes.c_int),  # ///组合成交形成的持仓
        ('CombLongFrozen', ctypes.c_int),  # ///组合多头冻结
        ('CombShortFrozen', ctypes.c_int),  # ///组合空头冻结
        ('CloseProfitByDate', ctypes.c_double),  # ///逐日盯市平仓盈亏
        ('CloseProfitByTrade', ctypes.c_double),  # ///逐笔对冲平仓盈亏
        ('TodayPosition', ctypes.c_int),  # ///今日持仓
        ('MarginRateByMoney', ctypes.c_double),  # ///保证金率
        ('MarginRateByVolume', ctypes.c_double),  # ///保证金率(按手数)
        ('StrikeFrozen', ctypes.c_int),  # ///执行冻结
        ('StrikeFrozenAmount', ctypes.c_double),  # ///执行冻结金额
        ('AbandonFrozen', ctypes.c_int),  # ///放弃执行冻结
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('YdStrikeFrozen', ctypes.c_int),  # ///执行冻结的昨仓
        ('InvestUnitID', ctypes.c_char * 17),  # ///投资单元代码
        ('PositionCostOffset', ctypes.c_double),  # ///持仓成本差值
        ('TasPosition', ctypes.c_int),  # ///tas持仓手数
        ('TasPositionCost', ctypes.c_double),  # ///tas持仓成本
    ]


# ///风险品种
class RiskSettleProductStatusField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ProductID', ctypes.c_char * 81),  # ///产品编号
        ('ProductStatus', ctypes.c_char * 1),  # ///产品结算状态
    ]


# ///风险结算追平信息
class SyncDeltaInfoField(BaseField):
    _fields_ = [
        ('SyncDeltaSequenceNo', ctypes.c_int),  # ///追平序号
        ('SyncDeltaStatus', ctypes.c_char * 1),  # ///追平状态
        ('SyncDescription', ctypes.c_char * 257),  # ///追平描述
        ('IsOnlyTrdDelta', ctypes.c_int),  # ///是否只有资金追平
    ]


# ///风险结算追平产品信息
class SyncDeltaProductStatusField(BaseField):
    _fields_ = [
        ('SyncDeltaSequenceNo', ctypes.c_int),  # ///追平序号
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ProductID', ctypes.c_char * 81),  # ///产品代码
        ('ProductStatus', ctypes.c_char * 1),  # ///是否允许交易
    ]


# ///风险结算追平持仓明细
class SyncDeltaInvstPosDtlField(BaseField):
    _fields_ = [
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('Direction', ctypes.c_char * 1),  # ///买卖
        ('OpenDate', ctypes.c_char * 9),  # ///开仓日期
        ('TradeID', ctypes.c_char * 21),  # ///成交编号
        ('Volume', ctypes.c_int),  # ///数量
        ('OpenPrice', ctypes.c_double),  # ///开仓价
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('SettlementID', ctypes.c_int),  # ///结算编号
        ('TradeType', ctypes.c_char * 1),  # ///成交类型
        ('CombInstrumentID', ctypes.c_char * 81),  # ///组合合约代码
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('CloseProfitByDate', ctypes.c_double),  # ///逐日盯市平仓盈亏
        ('CloseProfitByTrade', ctypes.c_double),  # ///逐笔对冲平仓盈亏
        ('PositionProfitByDate', ctypes.c_double),  # ///逐日盯市持仓盈亏
        ('PositionProfitByTrade', ctypes.c_double),  # ///逐笔对冲持仓盈亏
        ('Margin', ctypes.c_double),  # ///投资者保证金
        ('ExchMargin', ctypes.c_double),  # ///交易所保证金
        ('MarginRateByMoney', ctypes.c_double),  # ///保证金率
        ('MarginRateByVolume', ctypes.c_double),  # ///保证金率(按手数)
        ('LastSettlementPrice', ctypes.c_double),  # ///昨结算价
        ('SettlementPrice', ctypes.c_double),  # ///结算价
        ('CloseVolume', ctypes.c_int),  # ///平仓量
        ('CloseAmount', ctypes.c_double),  # ///平仓金额
        ('TimeFirstVolume', ctypes.c_int),  # ///先开先平剩余数量
        ('SpecPosiType', ctypes.c_char * 1),  # ///特殊持仓标志
        ('ActionDirection', ctypes.c_char * 1),  # ///操作标志
        ('SyncDeltaSequenceNo', ctypes.c_int),  # ///追平序号
    ]


# ///风险结算追平组合持仓明细
class SyncDeltaInvstPosCombDtlField(BaseField):
    _fields_ = [
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('OpenDate', ctypes.c_char * 9),  # ///开仓日期
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('SettlementID', ctypes.c_int),  # ///结算编号
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('ComTradeID', ctypes.c_char * 21),  # ///组合编号
        ('TradeID', ctypes.c_char * 21),  # ///撮合编号
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('Direction', ctypes.c_char * 1),  # ///买卖
        ('TotalAmt', ctypes.c_int),  # ///持仓量
        ('Margin', ctypes.c_double),  # ///投资者保证金
        ('ExchMargin', ctypes.c_double),  # ///交易所保证金
        ('MarginRateByMoney', ctypes.c_double),  # ///保证金率
        ('MarginRateByVolume', ctypes.c_double),  # ///保证金率(按手数)
        ('LegID', ctypes.c_int),  # ///单腿编号
        ('LegMultiple', ctypes.c_int),  # ///单腿乘数
        ('TradeGroupID', ctypes.c_int),  # ///成交组号
        ('ActionDirection', ctypes.c_char * 1),  # ///操作标志
        ('SyncDeltaSequenceNo', ctypes.c_int),  # ///追平序号
    ]


# ///风险结算追平资金
class SyncDeltaTradingAccountField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('AccountID', ctypes.c_char * 13),  # ///投资者帐号
        ('PreMortgage', ctypes.c_double),  # ///上次质押金额
        ('PreCredit', ctypes.c_double),  # ///上次信用额度
        ('PreDeposit', ctypes.c_double),  # ///上次存款额
        ('PreBalance', ctypes.c_double),  # ///上次结算准备金
        ('PreMargin', ctypes.c_double),  # ///上次占用的保证金
        ('InterestBase', ctypes.c_double),  # ///利息基数
        ('Interest', ctypes.c_double),  # ///利息收入
        ('Deposit', ctypes.c_double),  # ///入金金额
        ('Withdraw', ctypes.c_double),  # ///出金金额
        ('FrozenMargin', ctypes.c_double),  # ///冻结的保证金
        ('FrozenCash', ctypes.c_double),  # ///冻结的资金
        ('FrozenCommission', ctypes.c_double),  # ///冻结的手续费
        ('CurrMargin', ctypes.c_double),  # ///当前保证金总额
        ('CashIn', ctypes.c_double),  # ///资金差额
        ('Commission', ctypes.c_double),  # ///手续费
        ('CloseProfit', ctypes.c_double),  # ///平仓盈亏
        ('PositionProfit', ctypes.c_double),  # ///持仓盈亏
        ('Balance', ctypes.c_double),  # ///期货结算准备金
        ('Available', ctypes.c_double),  # ///可用资金
        ('WithdrawQuota', ctypes.c_double),  # ///可取资金
        ('Reserve', ctypes.c_double),  # ///基本准备金
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('SettlementID', ctypes.c_int),  # ///结算编号
        ('Credit', ctypes.c_double),  # ///信用额度
        ('Mortgage', ctypes.c_double),  # ///质押金额
        ('ExchangeMargin', ctypes.c_double),  # ///交易所保证金
        ('DeliveryMargin', ctypes.c_double),  # ///投资者交割保证金
        ('ExchangeDeliveryMargin', ctypes.c_double),  # ///交易所交割保证金
        ('ReserveBalance', ctypes.c_double),  # ///保底期货结算准备金
        ('CurrencyID', ctypes.c_char * 4),  # ///币种代码
        ('PreFundMortgageIn', ctypes.c_double),  # ///上次货币质入金额
        ('PreFundMortgageOut', ctypes.c_double),  # ///上次货币质出金额
        ('FundMortgageIn', ctypes.c_double),  # ///货币质入金额
        ('FundMortgageOut', ctypes.c_double),  # ///货币质出金额
        ('FundMortgageAvailable', ctypes.c_double),  # ///货币质押余额
        ('MortgageableFund', ctypes.c_double),  # ///可质押货币金额
        ('SpecProductMargin', ctypes.c_double),  # ///特殊产品占用保证金
        ('SpecProductFrozenMargin', ctypes.c_double),  # ///特殊产品冻结保证金
        ('SpecProductCommission', ctypes.c_double),  # ///特殊产品手续费
        ('SpecProductFrozenCommission', ctypes.c_double),  # ///特殊产品冻结手续费
        ('SpecProductPositionProfit', ctypes.c_double),  # ///特殊产品持仓盈亏
        ('SpecProductCloseProfit', ctypes.c_double),  # ///特殊产品平仓盈亏
        ('SpecProductPositionProfitByAlg', ctypes.c_double),  # ///根据持仓盈亏算法计算的特殊产品持仓盈亏
        ('SpecProductExchangeMargin', ctypes.c_double),  # ///特殊产品交易所保证金
        ('FrozenSwap', ctypes.c_double),  # ///延时换汇冻结金额
        ('RemainSwap', ctypes.c_double),  # ///剩余换汇额度
        ('SyncDeltaSequenceNo', ctypes.c_int),  # ///追平序号
    ]


# ///投资者风险结算总保证金
class SyncDeltaInitInvstMarginField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('LastRiskTotalInvstMargin', ctypes.c_double),  # ///追平前总风险保证金
        ('LastRiskTotalExchMargin', ctypes.c_double),  # ///追平前交易所总风险保证金
        ('ThisSyncInvstMargin', ctypes.c_double),  # ///本次追平品种总保证金
        ('ThisSyncExchMargin', ctypes.c_double),  # ///本次追平品种交易所总保证金
        ('RemainRiskInvstMargin', ctypes.c_double),  # ///本次未追平品种总保证金
        ('RemainRiskExchMargin', ctypes.c_double),  # ///本次未追平品种交易所总保证金
        ('LastRiskSpecTotalInvstMargin', ctypes.c_double),  # ///追平前总特殊产品风险保证金
        ('LastRiskSpecTotalExchMargin', ctypes.c_double),  # ///追平前总特殊产品交易所风险保证金
        ('ThisSyncSpecInvstMargin', ctypes.c_double),  # ///本次追平品种特殊产品总保证金
        ('ThisSyncSpecExchMargin', ctypes.c_double),  # ///本次追平品种特殊产品交易所总保证金
        ('RemainRiskSpecInvstMargin', ctypes.c_double),  # ///本次未追平品种特殊产品总保证金
        ('RemainRiskSpecExchMargin', ctypes.c_double),  # ///本次未追平品种特殊产品交易所总保证金
        ('SyncDeltaSequenceNo', ctypes.c_int),  # ///追平序号
    ]


# ///风险结算追平组合优先级
class SyncDeltaDceCombInstrumentField(BaseField):
    _fields_ = [
        ('CombInstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ExchangeInstID', ctypes.c_char * 81),  # ///合约在交易所的代码
        ('TradeGroupID', ctypes.c_int),  # ///成交组号
        ('CombHedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('CombinationType', ctypes.c_char * 1),  # ///组合类型
        ('Direction', ctypes.c_char * 1),  # ///买卖
        ('ProductID', ctypes.c_char * 81),  # ///产品代码
        ('Xparameter', ctypes.c_double),  # ///期权组合保证金比例
        ('ActionDirection', ctypes.c_char * 1),  # ///操作标志
        ('SyncDeltaSequenceNo', ctypes.c_int),  # ///追平序号
    ]


# ///风险结算追平投资者期货保证金率
class SyncDeltaInvstMarginRateField(BaseField):
    _fields_ = [
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('InvestorRange', ctypes.c_char * 1),  # ///投资者范围
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('LongMarginRatioByMoney', ctypes.c_double),  # ///多头保证金率
        ('LongMarginRatioByVolume', ctypes.c_double),  # ///多头保证金费
        ('ShortMarginRatioByMoney', ctypes.c_double),  # ///空头保证金率
        ('ShortMarginRatioByVolume', ctypes.c_double),  # ///空头保证金费
        ('IsRelative', ctypes.c_int),  # ///是否相对交易所收取
        ('ActionDirection', ctypes.c_char * 1),  # ///操作标志
        ('SyncDeltaSequenceNo', ctypes.c_int),  # ///追平序号
    ]


# ///风险结算追平交易所期货保证金率
class SyncDeltaExchMarginRateField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('LongMarginRatioByMoney', ctypes.c_double),  # ///多头保证金率
        ('LongMarginRatioByVolume', ctypes.c_double),  # ///多头保证金费
        ('ShortMarginRatioByMoney', ctypes.c_double),  # ///空头保证金率
        ('ShortMarginRatioByVolume', ctypes.c_double),  # ///空头保证金费
        ('ActionDirection', ctypes.c_char * 1),  # ///操作标志
        ('SyncDeltaSequenceNo', ctypes.c_int),  # ///追平序号
    ]


# ///风险结算追平中金现货期权交易所保证金率
class SyncDeltaOptExchMarginField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('SShortMarginRatioByMoney', ctypes.c_double),  # ///投机空头保证金调整系数
        ('SShortMarginRatioByVolume', ctypes.c_double),  # ///投机空头保证金调整系数
        ('HShortMarginRatioByMoney', ctypes.c_double),  # ///保值空头保证金调整系数
        ('HShortMarginRatioByVolume', ctypes.c_double),  # ///保值空头保证金调整系数
        ('AShortMarginRatioByMoney', ctypes.c_double),  # ///套利空头保证金调整系数
        ('AShortMarginRatioByVolume', ctypes.c_double),  # ///套利空头保证金调整系数
        ('MShortMarginRatioByMoney', ctypes.c_double),  # ///做市商空头保证金调整系数
        ('MShortMarginRatioByVolume', ctypes.c_double),  # ///做市商空头保证金调整系数
        ('ActionDirection', ctypes.c_char * 1),  # ///操作标志
        ('SyncDeltaSequenceNo', ctypes.c_int),  # ///追平序号
    ]


# ///风险结算追平中金现货期权投资者保证金率
class SyncDeltaOptInvstMarginField(BaseField):
    _fields_ = [
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('InvestorRange', ctypes.c_char * 1),  # ///投资者范围
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('SShortMarginRatioByMoney', ctypes.c_double),  # ///投机空头保证金调整系数
        ('SShortMarginRatioByVolume', ctypes.c_double),  # ///投机空头保证金调整系数
        ('HShortMarginRatioByMoney', ctypes.c_double),  # ///保值空头保证金调整系数
        ('HShortMarginRatioByVolume', ctypes.c_double),  # ///保值空头保证金调整系数
        ('AShortMarginRatioByMoney', ctypes.c_double),  # ///套利空头保证金调整系数
        ('AShortMarginRatioByVolume', ctypes.c_double),  # ///套利空头保证金调整系数
        ('IsRelative', ctypes.c_int),  # ///是否跟随交易所收取
        ('MShortMarginRatioByMoney', ctypes.c_double),  # ///做市商空头保证金调整系数
        ('MShortMarginRatioByVolume', ctypes.c_double),  # ///做市商空头保证金调整系数
        ('ActionDirection', ctypes.c_char * 1),  # ///操作标志
        ('SyncDeltaSequenceNo', ctypes.c_int),  # ///追平序号
    ]


# ///风险结算追平期权标的调整保证金率
class SyncDeltaInvstMarginRateULField(BaseField):
    _fields_ = [
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('InvestorRange', ctypes.c_char * 1),  # ///投资者范围
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('LongMarginRatioByMoney', ctypes.c_double),  # ///多头保证金率
        ('LongMarginRatioByVolume', ctypes.c_double),  # ///多头保证金费
        ('ShortMarginRatioByMoney', ctypes.c_double),  # ///空头保证金率
        ('ShortMarginRatioByVolume', ctypes.c_double),  # ///空头保证金费
        ('ActionDirection', ctypes.c_char * 1),  # ///操作标志
        ('SyncDeltaSequenceNo', ctypes.c_int),  # ///追平序号
    ]


# ///风险结算追平期权手续费率
class SyncDeltaOptInvstCommRateField(BaseField):
    _fields_ = [
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('InvestorRange', ctypes.c_char * 1),  # ///投资者范围
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('OpenRatioByMoney', ctypes.c_double),  # ///开仓手续费率
        ('OpenRatioByVolume', ctypes.c_double),  # ///开仓手续费
        ('CloseRatioByMoney', ctypes.c_double),  # ///平仓手续费率
        ('CloseRatioByVolume', ctypes.c_double),  # ///平仓手续费
        ('CloseTodayRatioByMoney', ctypes.c_double),  # ///平今手续费率
        ('CloseTodayRatioByVolume', ctypes.c_double),  # ///平今手续费
        ('StrikeRatioByMoney', ctypes.c_double),  # ///执行手续费率
        ('StrikeRatioByVolume', ctypes.c_double),  # ///执行手续费
        ('ActionDirection', ctypes.c_char * 1),  # ///操作标志
        ('SyncDeltaSequenceNo', ctypes.c_int),  # ///追平序号
    ]


# ///风险结算追平期货手续费率
class SyncDeltaInvstCommRateField(BaseField):
    _fields_ = [
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('InvestorRange', ctypes.c_char * 1),  # ///投资者范围
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('OpenRatioByMoney', ctypes.c_double),  # ///开仓手续费率
        ('OpenRatioByVolume', ctypes.c_double),  # ///开仓手续费
        ('CloseRatioByMoney', ctypes.c_double),  # ///平仓手续费率
        ('CloseRatioByVolume', ctypes.c_double),  # ///平仓手续费
        ('CloseTodayRatioByMoney', ctypes.c_double),  # ///平今手续费率
        ('CloseTodayRatioByVolume', ctypes.c_double),  # ///平今手续费
        ('ActionDirection', ctypes.c_char * 1),  # ///操作标志
        ('SyncDeltaSequenceNo', ctypes.c_int),  # ///追平序号
    ]


# ///风险结算追平交叉汇率
class SyncDeltaProductExchRateField(BaseField):
    _fields_ = [
        ('ProductID', ctypes.c_char * 81),  # ///产品代码
        ('QuoteCurrencyID', ctypes.c_char * 4),  # ///报价币种类型
        ('ExchangeRate', ctypes.c_double),  # ///汇率
        ('ActionDirection', ctypes.c_char * 1),  # ///操作标志
        ('SyncDeltaSequenceNo', ctypes.c_int),  # ///追平序号
    ]


# ///风险结算追平行情
class SyncDeltaDepthMarketDataField(BaseField):
    _fields_ = [
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ExchangeInstID', ctypes.c_char * 81),  # ///合约在交易所的代码
        ('LastPrice', ctypes.c_double),  # ///最新价
        ('PreSettlementPrice', ctypes.c_double),  # ///上次结算价
        ('PreClosePrice', ctypes.c_double),  # ///昨收盘
        ('PreOpenInterest', ctypes.c_double),  # ///昨持仓量
        ('OpenPrice', ctypes.c_double),  # ///今开盘
        ('HighestPrice', ctypes.c_double),  # ///最高价
        ('LowestPrice', ctypes.c_double),  # ///最低价
        ('Volume', ctypes.c_int),  # ///数量
        ('Turnover', ctypes.c_double),  # ///成交金额
        ('OpenInterest', ctypes.c_double),  # ///持仓量
        ('ClosePrice', ctypes.c_double),  # ///今收盘
        ('SettlementPrice', ctypes.c_double),  # ///本次结算价
        ('UpperLimitPrice', ctypes.c_double),  # ///涨停板价
        ('LowerLimitPrice', ctypes.c_double),  # ///跌停板价
        ('PreDelta', ctypes.c_double),  # ///昨虚实度
        ('CurrDelta', ctypes.c_double),  # ///今虚实度
        ('UpdateTime', ctypes.c_char * 9),  # ///最后修改时间
        ('UpdateMillisec', ctypes.c_int),  # ///最后修改毫秒
        ('BidPrice1', ctypes.c_double),  # ///申买价一
        ('BidVolume1', ctypes.c_int),  # ///申买量一
        ('AskPrice1', ctypes.c_double),  # ///申卖价一
        ('AskVolume1', ctypes.c_int),  # ///申卖量一
        ('BidPrice2', ctypes.c_double),  # ///申买价二
        ('BidVolume2', ctypes.c_int),  # ///申买量二
        ('AskPrice2', ctypes.c_double),  # ///申卖价二
        ('AskVolume2', ctypes.c_int),  # ///申卖量二
        ('BidPrice3', ctypes.c_double),  # ///申买价三
        ('BidVolume3', ctypes.c_int),  # ///申买量三
        ('AskPrice3', ctypes.c_double),  # ///申卖价三
        ('AskVolume3', ctypes.c_int),  # ///申卖量三
        ('BidPrice4', ctypes.c_double),  # ///申买价四
        ('BidVolume4', ctypes.c_int),  # ///申买量四
        ('AskPrice4', ctypes.c_double),  # ///申卖价四
        ('AskVolume4', ctypes.c_int),  # ///申卖量四
        ('BidPrice5', ctypes.c_double),  # ///申买价五
        ('BidVolume5', ctypes.c_int),  # ///申买量五
        ('AskPrice5', ctypes.c_double),  # ///申卖价五
        ('AskVolume5', ctypes.c_int),  # ///申卖量五
        ('AveragePrice', ctypes.c_double),  # ///当日均价
        ('ActionDay', ctypes.c_char * 9),  # ///业务日期
        ('BandingUpperPrice', ctypes.c_double),  # ///上带价
        ('BandingLowerPrice', ctypes.c_double),  # ///下带价
        ('ActionDirection', ctypes.c_char * 1),  # ///操作标志
        ('SyncDeltaSequenceNo', ctypes.c_int),  # ///追平序号
    ]


# ///风险结算追平现货指数
class SyncDeltaIndexPriceField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('ClosePrice', ctypes.c_double),  # ///指数现货收盘价
        ('ActionDirection', ctypes.c_char * 1),  # ///操作标志
        ('SyncDeltaSequenceNo', ctypes.c_int),  # ///追平序号
    ]


# ///风险结算追平仓单折抵
class SyncDeltaEWarrantOffsetField(BaseField):
    _fields_ = [
        ('TradingDay', ctypes.c_char * 9),  # ///交易日期
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('Direction', ctypes.c_char * 1),  # ///买卖方向
        ('HedgeFlag', ctypes.c_char * 1),  # ///投机套保标志
        ('Volume', ctypes.c_int),  # ///数量
        ('ActionDirection', ctypes.c_char * 1),  # ///操作标志
        ('SyncDeltaSequenceNo', ctypes.c_int),  # ///追平序号
    ]


# ///SPBM期货合约保证金参数
class SPBMFutureParameterField(BaseField):
    _fields_ = [
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('ProdFamilyCode', ctypes.c_char * 81),  # ///品种代码
        ('Cvf', ctypes.c_int),  # ///期货合约因子
        ('TimeRange', ctypes.c_char * 1),  # ///阶段标识
        ('MarginRate', ctypes.c_double),  # ///品种保证金标准
        ('LockRateX', ctypes.c_double),  # ///期货合约内部对锁仓费率折扣比例
        ('AddOnRate', ctypes.c_double),  # ///提高保证金标准
        ('PreSettlementPrice', ctypes.c_double),  # ///昨结算价
    ]


# ///SPBM期权合约保证金参数
class SPBMOptionParameterField(BaseField):
    _fields_ = [
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('ProdFamilyCode', ctypes.c_char * 81),  # ///品种代码
        ('Cvf', ctypes.c_int),  # ///期权合约因子
        ('DownPrice', ctypes.c_double),  # ///期权冲抵价格
        ('Delta', ctypes.c_double),  # ///Delta值
        ('SlimiDelta', ctypes.c_double),  # ///卖方期权风险转换最低值
        ('PreSettlementPrice', ctypes.c_double),  # ///昨结算价
    ]


# ///SPBM品种内对锁仓折扣参数
class SPBMIntraParameterField(BaseField):
    _fields_ = [
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ProdFamilyCode', ctypes.c_char * 81),  # ///品种代码
        ('IntraRateY', ctypes.c_double),  # ///品种内合约间对锁仓费率折扣比例
    ]


# ///SPBM跨品种抵扣参数
class SPBMInterParameterField(BaseField):
    _fields_ = [
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('SpreadId', ctypes.c_int),  # ///优先级
        ('InterRateZ', ctypes.c_double),  # ///品种间对锁仓费率折扣比例
        ('Leg1ProdFamilyCode', ctypes.c_char * 81),  # ///第一腿构成品种
        ('Leg2ProdFamilyCode', ctypes.c_char * 81),  # ///第二腿构成品种
    ]


# ///同步SPBM参数结束
class SyncSPBMParameterEndField(BaseField):
    _fields_ = [
        ('TradingDay', ctypes.c_char * 9),  # ///交易日
    ]


# ///SPBM期货合约保证金参数查询
class QrySPBMFutureParameterField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('ProdFamilyCode', ctypes.c_char * 81),  # ///品种代码
    ]


# ///SPBM期权合约保证金参数查询
class QrySPBMOptionParameterField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('InstrumentID', ctypes.c_char * 81),  # ///合约代码
        ('ProdFamilyCode', ctypes.c_char * 81),  # ///品种代码
    ]


# ///SPBM品种内对锁仓折扣参数查询
class QrySPBMIntraParameterField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('ProdFamilyCode', ctypes.c_char * 81),  # ///品种代码
    ]


# ///SPBM跨品种抵扣参数查询
class QrySPBMInterParameterField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('Leg1ProdFamilyCode', ctypes.c_char * 81),  # ///第一腿构成品种
        ('Leg2ProdFamilyCode', ctypes.c_char * 81),  # ///第二腿构成品种
    ]


# ///组合保证金套餐
class SPBMPortfDefinitionField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('PortfolioDefID', ctypes.c_int),  # ///组合保证金套餐代码
        ('ProdFamilyCode', ctypes.c_char * 81),  # ///品种代码
        ('IsSPBM', ctypes.c_int),  # ///是否启用SPBM
    ]


# ///投资者套餐选择
class SPBMInvestorPortfDefField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('PortfolioDefID', ctypes.c_int),  # ///组合保证金套餐代码
    ]


# ///投资者新型组合保证金系数
class InvestorPortfMarginRatioField(BaseField):
    _fields_ = [
        ('InvestorRange', ctypes.c_char * 1),  # ///投资者范围
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('MarginRatio', ctypes.c_double),  # ///会员对投资者收取的保证金和交易所对投资者收取的保证金的比例
    ]


# ///组合保证金套餐查询
class QrySPBMPortfDefinitionField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('PortfolioDefID', ctypes.c_int),  # ///组合保证金套餐代码
        ('ProdFamilyCode', ctypes.c_char * 81),  # ///品种代码
    ]


# ///投资者套餐选择查询
class QrySPBMInvestorPortfDefField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
    ]


# ///投资者新型组合保证金系数查询
class QryInvestorPortfMarginRatioField(BaseField):
    _fields_ = [
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
    ]


# ///投资者产品SPBM明细
class InvestorProdSPBMDetailField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('ProdFamilyCode', ctypes.c_char * 81),  # ///品种代码
        ('IntraInstrMargin', ctypes.c_double),  # ///合约内对锁保证金
        ('BCollectingMargin', ctypes.c_double),  # ///买归集保证金
        ('SCollectingMargin', ctypes.c_double),  # ///卖归集保证金
        ('IntraProdMargin', ctypes.c_double),  # ///品种内合约间对锁保证金
        ('NetMargin', ctypes.c_double),  # ///净保证金
        ('InterProdMargin', ctypes.c_double),  # ///产品间对锁保证金
        ('SingleMargin', ctypes.c_double),  # ///裸保证金
        ('AddOnMargin', ctypes.c_double),  # ///附加保证金
        ('DeliveryMargin', ctypes.c_double),  # ///交割月保证金
        ('CallOptionMinRisk', ctypes.c_double),  # ///看涨期权最低风险
        ('PutOptionMinRisk', ctypes.c_double),  # ///看跌期权最低风险
        ('OptionMinRisk', ctypes.c_double),  # ///卖方期权最低风险
        ('OptionValueOffset', ctypes.c_double),  # ///买方期权冲抵价值
        ('OptionRoyalty', ctypes.c_double),  # ///卖方期权权利金
        ('RealOptionValueOffset', ctypes.c_double),  # ///价值冲抵
        ('Margin', ctypes.c_double),  # ///保证金
        ('ExchMargin', ctypes.c_double),  # ///交易所保证金
    ]


# ///投资者产品SPBM明细查询
class QryInvestorProdSPBMDetailField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('ProdFamilyCode', ctypes.c_char * 81),  # ///品种代码
    ]


# ///组保交易参数设置
class PortfTradeParamSettingField(BaseField):
    _fields_ = [
        ('ExchangeID', ctypes.c_char * 9),  # ///交易所代码
        ('BrokerID', ctypes.c_char * 11),  # ///经纪公司代码
        ('InvestorID', ctypes.c_char * 13),  # ///投资者代码
        ('Portfolio', ctypes.c_char * 1),  # ///新型组保算法
        ('IsActionVerify', ctypes.c_int),  # ///撤单是否验资
        ('IsCloseVerify', ctypes.c_int),  # ///平仓是否验资
    ]
