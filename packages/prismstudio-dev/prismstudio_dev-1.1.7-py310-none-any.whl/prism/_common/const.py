import numpy as np
import pandas as pd
from enum import Enum


__all__ = [
    'BEGINNING_DATE',
    'ACTIVE_DATE',
    'PrismComponentType',
    'SMValues',
    'PreferenceType',
    'FrequencyType',
    'UniverseFrequencyType',
    'PeriodType',
    'AdjustmentType',
    'RankType',
    'DateType',
    'MarketDataComponentType',
    'FinancialDataComponentType',
    'EstimateDataComponentType',
    'PrecalculatedDataComponentType',
    'IndexDataComponentType',
    'OtherDataComponentType',
    'AggregationType',
    'FinancialPreliminaryType',
    'IndustryComponentType',
    'UniverseFreeDataComponentType',
    'FillnaMethodType',
    'BeyondType',
    'COMPONENT2CATEGORY',
    'FUNCTIONS',
    'FILEEXTENSION',
    'AggregateComponents',
    'PACKAGE_NAME',
    'SPECIALVALUEMAP',
    'DataCategoryType',
]

BEGINNING_DATE = pd.to_datetime('1700-01-01')
ACTIVE_DATE = pd.to_datetime('2199-12-31')


class PrismComponentType(str, Enum):
    FUNCTION_COMPONENT = 'functioncomponent'
    DATA_COMPONENT = 'datacomponent'
    TASK_COMPONENT = 'taskcomponent'


SMValues = None
PreferenceType = None


class AdjustmentType(Enum):
    ALL = 'all'
    SPLIT = 'split'
    DIVIDEND = 'dividend'
    TRUE = True
    FALSE = False


class FrequencyType(str, Enum):
    NANOSECONDS = 'N'
    MICROSECONDS = 'U'
    MICROSECONDS_ALIAS = 'us'
    MILISECONDS = 'L'
    MILISECONDS_ALIAS = 'ms'
    SECONDS = 'S'
    MINUTES = 'T'
    MINUTES_ALIAS = 'min'
    HOURS = 'H'
    BUSINESS_HOURS = 'BH'
    CALENDAR_DAY = 'D'
    BUSINESS_DAY = 'BD'
    WEEKS = 'W'
    MONTH_START = 'MS'
    BUSINESS_MONTH_START = 'BMS'
    SEMI_MONTH_START = 'SMS'
    SEMI_MONTH_END = 'SM'
    BUSINESS_MONTH_END = 'BM'
    MONTH_END = 'M'
    QUARTER_END = 'Q'
    QUARTER_START = 'QS'
    BUSINESS_QUARTER_END = 'BQ'
    BUSINESS_QUARTER_START = 'BQS'
    YEAR_START = 'AS'
    YEAR_END = 'A'


class UniverseFrequencyType(str, Enum):
    CALENDAR_DAY = 'D'
    WEEKS = 'W'
    MONTH_START = 'MS'
    SEMI_MONTH_START = 'SMS'
    SEMI_MONTH_END = 'SM'
    MONTH_END = 'M'
    QUARTER_END = 'Q'
    QUARTER_START = 'QS'
    YEAR_START = 'AS'
    YEAR_END = 'A'


class RankType(str, Enum):
    STANDARD = 'standard'
    MODIFIED = 'modified'
    DENSE = 'dense'
    ORDINAL = 'ordinal'
    FRACTIONAL = 'fractional'


class DateType(str, Enum):
    ENTEREDDATE = 'entereddate'
    ANNOUNCEDDATE = 'announceddate'


class PeriodType(str, Enum):
    ANNUAL = 'Annual'
    A = 'A'
    SEMI_ANNUAL = 'Semi-Annual'
    SA = 'SA'
    QUARTERLY = 'Quarterly'
    Q = 'Q'
    YTD = 'YTD'
    LTM = 'LTM'
    NON_PERIODIC = 'Non-Periodic'
    NTM = 'NTM'
    QSA = 'Q-SA'


class TaskComponentType(str, Enum):
    SCREEN = 'screen'
    FACTOR_BACKTEST = 'factor_backtest'
    STRATEGY_BACKTEST = 'strategy_backtest'
    EXPORT_DATA = 'export_data'


class DataCategoryType(str, Enum):
    FINANCIAL = "Financial"
    PRECALCAULATED = "Precalculated"
    EVENT = "Event"
    SM = "Securitymaster"
    MARKET = "Market"
    ESTIMATE = "Estimate"
    INDEX = "Index"
    INDUSTRY_ESTIMATE = "Industry Estimate"
    INDUSTRY_FINANCIAL = "Industry"


class FinancialDataComponentType(str, Enum):
    BALANCE_SHEET = 'Balance Sheet'
    CASH_FLOW = 'Cash Flow'
    DPS = 'DPS'
    EPS = 'EPS'
    FINANCIAL_DATE = 'Financial Date'
    INCOME_STATEMENT = 'Income Statement'
    SEGMENT = 'Segment'
    RATIO = 'Ratio'
    COMMITMENT = 'Commitment'
    PENSION = 'Pension'
    OPTION = 'Option'


class EstimateDataComponentType(str, Enum):
    CONSENSUS = 'Consensus'
    GROWTH = 'Growth'
    GUIDANCE = 'Guidance'
    REVISION = 'Revision'
    ACTUAL = 'Actual'
    SURPRISE = 'Surprise'


class MarketDataComponentType(str, Enum):
    CLOSE = 'Close'
    OPEN = 'Open'
    HIGH = 'High'
    LOW = 'Low'
    BID = 'Bid'
    ASK = 'Ask'
    VWAP = 'VWAP'
    MARKETCAP = 'Market Capitalization'
    VOLUME = 'Volume'
    DIVIDEND = 'Dividend'
    DIVIDEND_ADJ_FACTOR = 'Dividend Adjustment Factor'
    EXCHANGERATE = 'Exchange Rate'
    SHORT_INTEREST = 'Short Interest'
    SPLIT = 'Split'
    SPLIT_ADJ_FACTOR = 'Split Adjustment Factor'


class PrecalculatedDataComponentType(str, Enum):
    AFL = 'Alpha Factor Library'


class IndexDataComponentType(str, Enum):
    LEVEL = 'Index Level'
    SHARE = 'Index Share'
    WEIGHT = 'Index Weight'


class EventDataComponentType(str, Enum):
    NEWS = 'News'
    EARNINGSCALL = 'Earnings Call'


class IndustryComponentType(str, Enum):
    AIRLINES = 'Airlines'
    BANK = 'Bank'
    CAPITAL_MARKET = 'Capital Market'
    FINAICIAL_SERVICES = 'Financial Services'
    HEALTHCARE = 'Healthcare'
    HOMBUILDERS = 'Homebuilders'
    HOTEL_AND_GAMING = 'Hotel and Gaming'
    INSURANCE = 'Insurance'
    INTERNET_MEDIA = 'Internet Media'
    MANAGED_CARE = 'Managed Care'
    METALS_AND_MINING = 'Metals and Mining'
    OIL_AND_GAS = 'Oil and Gas'
    PHARMA = 'Pharmaceutical and Biotech'
    REAL_ESTATE = 'Real Estate'
    RESTAURANT = 'Restaurant'
    RETAIL = 'Retail'
    SEMICONDUCTORS = 'Semiconductors'
    TELECOM = 'Telecom/Cable/Wireless'
    UTILITY = 'Utility'


class UniverseFreeDataComponentType(str, Enum):
    EXCHANGERATE = 'Exchange Rate'
    VALUE = 'Index Share'
    WEIGHT = 'Index Weight'
    Level = 'Index Level'


class OtherDataComponentType(str, Enum):
    SM = 'SecurityMaster'
    PRISMVALUE = 'PrismValue'


class AggregationType(str, Enum):
    ONEDAY = '1 day'
    ONEWEEK = '1 week'
    ONEMONTH = '1 month'
    TWOMONTH = '2 month'
    THREEMONTH = '3 month'
    THREEMONTHLATEST = '3 month latest'


class FinancialPreliminaryType(str, Enum):
    KEEP = 'keep'
    IGNORE = 'ignore'
    DROP = 'drop'
    NULL = 'null'


class FillnaMethodType(str, Enum):
    BACKFILL = 'backfill'
    BFILL = 'bfill'
    PAD = 'pad'
    FFILL = 'ffill'


class BeyondType(str, Enum):
    LOOKBACK = 'lookback'
    ENDDATE = 'enddate'


COMPONENT2CATEGORY = {
    'Balance Sheet': {'category': 'financial', 'component': 'balance_sheet'},
    'Cash Flow': {'category': 'financial', 'component': 'cash_flow'},
    'Income Statement': {'category': 'financial', 'component': 'income_statement'},
    'Other Financial': {'category': 'financial', 'component': 'other_financial'},
    'Consensus': {'category': 'estimate', 'component': 'consensus'},
    'Guidance': {'category': 'estimate', 'component': 'guidance'},
    'Actual': {'category': 'estimate', 'component': 'actual'},
    'Surprise': {'category': 'estimate', 'component': 'surprise'},
    'Close': {'category': 'market', 'component': 'close'},
    'Open': {'category': 'market', 'component': 'open'},
    'High': {'category': 'market', 'component': 'high'},
    'Low': {'category': 'market', 'component': 'low'},
    'Bid': {'category': 'market', 'component': 'bid'},
    'Ask': {'category': 'market', 'component': 'ask'},
    'VWAP': {'category': 'market', 'component': 'vwap'},
    'Market Capitalization': {'category': 'market', 'component': 'market_cap'},
    'Volume': {'category': 'market', 'component': 'volume'},
    'Dividend': {'category': 'market', 'component': 'dividend'},
    'Exchange Rate': {'category': 'market', 'component': 'exchange_rate'},
    'Short Interest': {'category': 'market', 'component': 'short_interest'},
    'Split': {'category': 'market', 'component': 'split'},
    'Alpha Factor Library': {'category': 'precalculated', 'component': 'alpha_factor_library'},
    'Index Share': {'category': 'index', 'component': 'share'},
    'Index Weight': {'category': 'index', 'component': 'weight'},
    'Index Level': {'category': 'index', 'component': 'level'},
    'News': {'category': 'event', 'component': 'news'},
    'Earnings Call': {'category': 'event', 'component': 'earnings_call'},
}


INDEXLEVELTYPE2ID = {
    'Total Return Gross': 1,
    'Price Return': 2,
    'Currency Hedged Return': 3,
    'Total Return Net': 4,
    'Currency Hedged Total Return Gross': 16,
    'Currency Hedged Total Return Net': 17,
    'Volatility': 31,
}


FREQUENCY_TYPE = {
    'N': 1,
    'U': 2,
    'us': 2,
    'L': 3,
    'ms': 3,
    'S': 4,
    'T': 5,
    'min': 5,
    'H': 6,
    'BH': 7,
    'D': 8,
    'B': 9,
    'W': 10,
    'MS': 11,
    'BMS': 11,
    'SMS': 11,
    'SM': 11,
    'BM': 11,
    'M': 11,
    'Q': 12,
    'QS': 12,
    'BQ': 12,
    'BQS': 12,
    'AS': 13,
    'A': 13,
}


RANK_MAP = {
    'standard': 'min',
    'modified': 'max',
    'dense': 'dense',
    'ordinal': 'first',
    'fractional': 'average',
}


PERIOD2FREQUENCY = {
    'Annual': 'A',
    'A': 'A',
    'Semi-Annual': '6M',
    'SA': '6M',
    'Quarterly': 'Q',
    'Q': 'Q',
    'YTD': 'Q',
    'LTM': 'Q',
}


FILEEXTENSION = {'pdq': 'dataquery', 'ptq': 'taskquery', 'pws': 'workspace', 'puv': 'universe', 'ppt': 'portfolio', 'ped': 'datafile'}


FUNCTIONS = {
    '__add__': {'op': '+', 'type': 'binary'},
    '__radd__': {'op': '+', 'type': 'binary'},
    '__sub__': {'op': '-', 'type': 'binary'},
    '__rsub__': {'op': '-', 'type': 'binary'},
    '__mul__': {'op': '*', 'type': 'binary'},
    '__rmul__': {'op': '*', 'type': 'binary'},
    '__truediv__': {'op': '/', 'type': 'binary'},
    '__rtruediv__': {'op': '/', 'type': 'binary'},
    '__mod__': {'op': '%', 'type': 'binary'},
    '__rmod__': {'op': '%', 'type': 'binary'},
    '__pow__': {'op': '**', 'type': 'binary'},
    '__rpow__': {'op': '**', 'type': 'binary'},
    '__eq__': {'op': '==', 'type': 'logical'},
    '__ne__': {'op': '!=', 'type': 'logical'},
    '__gt__': {'op': '>', 'type': 'logical'},
    '__ge__': {'op': '>=', 'type': 'logical'},
    '__lt__': {'op': '<', 'type': 'logical'},
    '__le__': {'op': '<=', 'type': 'logical'},
    '__and__': {'op': '&', 'type': 'logical'},
    '__rand__': {'op': '&', 'type': 'logical'},
    '__or__': {'op': '|', 'type': 'logical'},
    '__ror__': {'op': '|', 'type': 'logical'},
    '__xor__': {'op': '^', 'type': 'logical'},
    '__rxor__': {'op': '^', 'type': 'logical'},
}


AggregateComponents = [
    'cross_sectional_std',
    'cross_sectional_sum',
    'cross_sectional_mean',
    'cross_sectional_median',
    'cross_sectional_max',
    'cross_sectional_min',
    'cross_sectional_count',
    'cross_sectional_sem',
    'cross_sectional_mad',
    'group_std',
    'group_sum',
    'group_mean',
    'group_median',
    'group_max',
    'group_min',
    'group_count',
    'group_sem',
    'group_mad',
]

# PACKAGE_NAME = 'p3s9'
PACKAGE_NAME = 'prism'

SPECIALVALUEMAP = {
    np.nan: "\x01NaN",
    np.inf: "\x01inf",
    np.NINF: "\x01ninf",
}