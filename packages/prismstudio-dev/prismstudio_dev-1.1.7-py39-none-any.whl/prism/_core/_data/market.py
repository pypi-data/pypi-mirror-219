from typing import Union

from ..._common.const import MarketDataComponentType as _MarketDataComponentType
from .._req_builder._list import _list_dataitem_market
from ..._prismcomponent.datacomponent import (
    _Open,
    _Close,
    _High,
    _Low,
    _Bid,
    _Ask,
    _VWAP,
    _MarketCap,
    _Volume,
    _Dividend,
    _DividendAdjustmentFactor,
    _Split,
    _SplitAdjustmentFactor,
    _ExchangeRate,
    _ShortInterest,
)
from ..._utils.validate_utils import _validate_args


__all__ = [
    'open',
    'close',
    'high',
    'low',
    'bid',
    'ask',
    'vwap',
    'market_cap',
    'volume',
    'dividend',
    'exchange_rate',
    'short_interest',
    'split',
    'split_adjustment_factor',
    'dividend_adjustment_factor',
    'dataitems',
    'short_interest_dataitems',
]


@_validate_args
def _build_price(
    datacomponentclass,
    adjustment: Union[str, bool] = None,
    currency: str = None,
    package : str = None,
):
    return datacomponentclass(
        package=package,
        adjustment=adjustment,
        currency=currency,
    )


def open(
    adjustment: Union[str, bool] = 'all',
    currency: str = 'trade',
    package : str = 'Prism Market',
):
    """
    | Daily open pricing history for equity securities.
    | Default frequency is business daily.

    Parameters
    ----------
        adjustment : str {'all', 'split', 'dividend'}, default 'all'
            | Adjustment for pricing data.

            - all : apply both split and dividend adjustment
            - split : apply only split adjustment
            - dividend : apply only dividend adjustment

        currency : str {'trade', 'report', ISO3 currency}, default 'trade'
            | Desired currency for the pricing data.

            - trade : trading currency for a given listing (i.e for Apple - USD, Tencent - HKD)
            - report : financial reporting currency for a given listing (i.e for Apple - USD, Tencent - CNY)
            - ISO3 currency : desired currency in ISO 4217 format (i.e USD, EUR, JPY, KRW, etc.)

        package : str {'Prism Market', 'Compustat', 'CIQ Market', 'MI Integrated Market'}, default 'Prism Market'
            | Desired data package in where the pricing data outputs from.

            .. admonition:: Warning
                :class: warning

                If an invalid package is entered without a license, an error will be generated as output.

    Returns
    -------
        prism._PrismComponent: Historical time-series of daily open prices for stocks

    Examples
    --------
        >>> open_prc = prism.market.open(adjustment='all', package='Prism Market')
        >>> open_df = prism.get_data([open_prc], 'KOSPI 200 Index', startdate='2015-01-01', enddate='2020-12-31', shownid=['ticker'])
        >>> open_df
                listingid        date           Open   ticker
        0        20108718  2015-01-02    7711.942343  A004430
        1        20108718  2015-01-05    7625.935551  A004430
        2        20108718  2015-01-06    7750.167583  A004430
        3        20108718  2015-01-07    7845.730686  A004430
        4        20108718  2015-01-08    8342.658817  A004430
        ...           ...         ...            ...      ...
        298991  686744025  2020-12-23  152679.990000  A352820
        298992  686744025  2020-12-24  151197.660000  A352820
        298993  686744025  2020-12-28  156632.870000  A352820
        298994  686744025  2020-12-29  154656.430000  A352820
        298995  686744025  2020-12-30  156632.870000  A352820
    """

    return _build_price(
        _Open,
        package=package,
        adjustment=adjustment,
        currency=currency,
    )


def close(
    adjustment: Union[str, bool] = 'all',
    currency: str = 'trade',
    package : str = 'Prism Market',
):
    """
    | Daily close pricing history for equity securities.
    | Default frequency is business daily.

    Parameters
    ----------
        adjustment : str {'all', 'split', 'dividend'}, default 'all'
            | Adjustment for pricing data.

            - all : apply both split and dividend adjustment
            - split : apply only split adjustment
            - dividend : apply only dividend adjustment

        currency : str {'trade', 'report', ISO3 currency}, default 'trade'
            | Desired currency for the pricing data.

            - trade : trading currency for a given listing (i.e for Apple - USD, Tencent - HKD)
            - report : financial reporting currency for a given listing (i.e for Apple - USD, Tencent - CNY)
            - ISO3 currency : desired currency in ISO 4217 format (i.e USD, EUR, JPY, KRW, etc.)

        package : str {'Prism Market', 'Compustat', 'CIQ Market', 'MI Integrated Market'}, default 'Prism Market'
            | Desired data package in where the pricing data outputs from.

            .. admonition:: Warning
                :class: warning

                If an invalid package is entered without a license, an error will be generated as output.

    Returns
    -------
        prism._PrismComponent: Historical time-series of daily close prices for stocks

    Examples
    --------
        Obtain daily closing prices for a specific security:

        >>> close = prism.market.close(adjustment='all', package='Prism Market')
        >>> close_df = prism.get_data([close], 'KOSPI 200 Index', startdate='2015-01-01', enddate='2020-12-31', shownid=['ticker'])
        >>> close_df
                listingid        date          Close   ticker
        0        20108718  2015-01-02    7740.611273  A004430
        1        20108718  2015-01-05    7874.399616  A004430
        2        20108718  2015-01-06    7903.068547  A004430
        3        20108718  2015-01-07    8313.989886  A004430
        4        20108718  2015-01-08    8161.088923  A004430
        ...           ...         ...            ...      ...
        298992  686744025  2020-12-23  151197.660000  A352820
        298993  686744025  2020-12-24  156138.760000  A352820
        298994  686744025  2020-12-28  154656.430000  A352820
        298995  686744025  2020-12-29  156632.870000  A352820
        298996  686744025  2020-12-30  158115.200000  A352820
    """

    return _build_price(
        _Close,
        package=package,
        adjustment=adjustment,
        currency=currency,
    )


def high(
    adjustment: Union[str, bool] = 'all',
    currency: str = 'trade',
    package : str = 'Prism Market',
):
    """
    | Daily high pricing history for equity securities.
    | Default frequency is business daily.

    Parameters
    ----------
        adjustment : str {'all', 'split', 'dividend'}, default 'all'
            | Adjustment for pricing data.

            - all: apply both split and dividend adjustment
            - split: apply only split adjustment
            - dividend: apply only dividend adjustment

        currency : str {'trade', 'report', ISO3 currency}, default 'trade'
            | Desired currency for the pricing data.

            - trade : trading currency for a given listing (i.e for Apple - USD, Tencent - HKD)
            - report : financial reporting currency for a given listing (i.e for Apple - USD, Tencent - CNY)
            - ISO3 currency : desired currency in ISO 4217 format (i.e USD, EUR, JPY, KRW, etc.)

        package : str {'Prism Market', 'Compustat', 'CIQ Market', 'MI Integrated Market'}, default 'Prism Market'
            | Desired data package in where the pricing data outputs from.

            .. admonition:: Warning
                :class: warning

                If an invalid package is entered without a license, an error will be generated as output.

    Returns
    -------
        prism._PrismComponent: Historical time-series of daily high prices for stocks

    Examples
    --------
        >>> high = prism.market.high(adjustment='all', package='Prism Market')
        >>> high_df = prism.get_data([high], 'KOSPI 200 Index', startdate='2015-01-01', enddate='2020-12-31', shownid=['ticker'])
        >>> high_df
                listingid        date           High   ticker
        0        20108718  2015-01-02    7855.286996  A004430
        1        20108718  2015-01-05    7893.512237  A004430
        2        20108718  2015-01-06    7931.737478  A004430
        3        20108718  2015-01-07    8323.546196  A004430
        4        20108718  2015-01-08    8352.215127  A004430
        ...           ...         ...            ...      ...
        298991  686744025  2020-12-23  156138.760000  A352820
        298992  686744025  2020-12-24  156632.870000  A352820
        298993  686744025  2020-12-28  157126.980000  A352820
        298994  686744025  2020-12-29  158609.310000  A352820
        298995  686744025  2020-12-30  159103.420000  A352820
    """

    return _build_price(
        _High,
        package=package,
        adjustment=adjustment,
        currency=currency,
    )


def low(
    adjustment: Union[str, bool] = 'all',
    currency: str = 'trade',
    package : str = 'Prism Market',
):
    """
    | Daily low pricing history for equity securities.
    | Default frequency is business daily.

    Parameters
    ----------
        adjustment : str, {'all', 'split', 'dividend'}, default 'all'
            | Adjustment for pricing data.

            - all : apply both split and dividend adjustment
            - split : apply only split adjustment
            - dividend : apply only dividend adjustment
        currency : str, {'trade', 'report', ISO3 currency}, default 'trade'
            | Desired currency for the pricing data.

            - trade : trading currency for a given listing (i.e for Apple - USD, Tencent - HKD)
            - report : financial reporting currency for a given listing (i.e for Apple - USD, Tencent - CNY)
            - ISO3 currency : desired currency in ISO 4217 format (i.e USD, EUR, JPY, KRW, etc.)
        package : str, {'Prism Market', 'Compustat', 'CIQ Market', 'MI Integrated Market'}, default 'Prism Market'
            | Desired data package in where the pricing data outputs from.

            .. admonition:: Warning
                :class: warning

                If an invalid package is entered without a license, an error will be generated as output.

    Returns
    -------
        prism._PrismComponent: Historical time-series of daily low prices for stocks

    Examples
    --------
        >>> low = prism.market.low(adjustment='all', package='Prism Market')
        >>> low_df = prism.get_data([low], 'KOSPI 200 Index', startdate='2015-01-01', enddate='2020-12-31', shownid=['ticker'])
        >>> low_df
                listingid       date            Low   ticker
        0        20108718 2015-01-02    7501.703518  A004430
        1        20108718 2015-01-05    7539.928759  A004430
        2        20108718 2015-01-06    7750.167583  A004430
        3        20108718 2015-01-07    7836.174375  A004430
        4        20108718 2015-01-08    8141.976302  A004430
        ...           ...        ...            ...      ...
        298991  686744025 2020-12-23  150703.550000  A352820
        298992  686744025 2020-12-24  149715.330000  A352820
        298993  686744025 2020-12-28  153174.100000  A352820
        298994  686744025 2020-12-29  153174.100000  A352820
        298995  686744025 2020-12-30  155644.650000  A352820
    """

    return _build_price(
        _Low,
        package=package,
        adjustment=adjustment,
        currency=currency,
    )


def ask(
    adjustment: Union[str, bool] = 'all',
    currency: str = 'trade',
    package : str = 'Prism Market',
):
    """
    | End of day ask pricing history for equity securities.
    | Default frequency is business daily.

    Parameters
    ----------
        adjustment : str, {'all', 'split', 'dividend'}, default 'all'
            | Adjustment for pricing data.

            - all : apply both split and dividend adjustment
            - split : apply only split adjustment
            - dividend : apply only dividend adjustment
        currency : str, {'trade', 'report', ISO3 currency}, default 'trade'
            | Desired currency for the pricing data.

            - trade : trading currency for a given listing (i.e for Apple - USD, Tencent - HKD)
            - report : financial reporting currency for a given listing (i.e for Apple - USD, Tencent - CNY)
            - ISO3 currency : desired currency in ISO 4217 format (i.e USD, EUR, JPY, KRW, etc.)
        package : str, {'Prism Market', 'CIQ Market', 'MI Integrated Market'}, default 'Prism Market'
            | Desired data package in where the pricing data outputs from.

            .. admonition:: Warning
                :class: warning

                If an invalid package is entered without a license, an error will be generated as output.

    Returns
    -------
        prism._PrismComponent: Historical time-series of daily end of day ask prices for stocks

    Examples
    --------
        >>> ask = prism.market.ask(adjustment='all', package='Prism Market')
        >>> ask_df = prism.get_data([ask], 'KOSPI 200 Index', startdate='2015-01-01', enddate='2020-12-31', shownid=['ticker'])
        >>> ask_df
                listingid        date            Ask   ticker
        0        20108718  2015-01-02    7740.611273  A004430
        1        20108718  2015-01-05    7874.399616  A004430
        2        20108718  2015-01-06    7903.068547  A004430
        3        20108718  2015-01-07    8313.989886  A004430
        4        20108718  2015-01-08    8199.314164  A004430
        ...           ...         ...            ...      ...
        298906  686744025  2020-12-23  151691.770000  A352820
        298907  686744025  2020-12-24  156138.760000  A352820
        298908  686744025  2020-12-28  155150.540000  A352820
        298909  686744025  2020-12-29  157126.980000  A352820
        298910  686744025  2020-12-30  158115.200000  A352820
    """

    return _build_price(
        _Ask,
        package=package,
        adjustment=adjustment,
        currency=currency,
    )


def bid(
    adjustment: Union[str, bool] = 'all',
    currency: str = 'trade',
    package : str = 'Prism Market',
):
    """
    | End of day bid pricing history for equity securities.
    | Default frequency is business daily.

    Parameters
    ----------
        adjustment : str, {'all', 'split', 'dividend'}, default 'all'
            | Adjustment for pricing data.

            - all : apply both split and dividend adjustment
            - split : apply only split adjustment
            - dividend: apply only dividend adjustment
        currency : str, {'trade', 'report', ISO3 currency}, default 'trade'
            | Desired currency for the pricing data.

            - trade : trading currency for a given listing (i.e for Apple - USD, Tencent - HKD)
            - report : financial reporting currency for a given listing (i.e for Apple - USD, Tencent - CNY)
            - ISO3 currency : desired currency in ISO 4217 format (i.e USD, EUR, JPY, KRW, etc.)
        package : str, {'Prism Market', 'CIQ Market', 'MI Integrated Market'}, default 'Prism Market'
            | Desired data package in where the pricing data outputs from.

            .. admonition:: Warning
                :class: warning

                If an invalid package is entered without a license, an error will be generated as output.

    Returns
    -------
        prism._PrismComponent: Historical time-series of daily end of day ask prices for stocks

    Examples
    --------
        >>> bid = prism.market.bid(adjustment='all', package='Prism Market')
        >>> bid_df = prism.get_data([bid], 'KOSPI 200 Index', startdate='2015-01-01', enddate='2020-12-31', shownid=['ticker'])
        >>> bid_df
                listingid        date            Bid   ticker
        0        20108718  2015-01-02    7616.379240  A004430
        1        20108718  2015-01-05    7864.843306  A004430
        2        20108718  2015-01-06    7883.955926  A004430
        3        20108718  2015-01-07    8304.433576  A004430
        4        20108718  2015-01-08    8161.088923  A004430
        ...           ...         ...            ...      ...
        298976  686744025  2020-12-23  151197.660000  A352820
        298977  686744025  2020-12-24  155644.650000  A352820
        298978  686744025  2020-12-28  154656.430000  A352820
        298979  686744025  2020-12-29  156632.870000  A352820
        298980  686744025  2020-12-30  157621.090000  A352820
    """
    return _build_price(
        _Bid,
        package=package,
        adjustment=adjustment,
        currency=currency,
    )


def vwap(
    adjustment: Union[str, bool] = 'all',
    currency: str = 'trade',
    package : str = 'Prism Market',
):
    """
    | Daily VWAP pricing history for equity securities.
    | Default frequency is business daily.

    Parameters
    ----------
        adjustment : str, {'all', 'split', 'dividend'}, default 'all'
            | Adjustment for pricing data.

            - all : apply both split and dividend adjustment
            - split : apply only split adjustment
            - dividend : apply only dividend adjustment
        currency : str, {'trade', 'report', ISO3 currency}, default 'trade'
            | Desired currency for the pricing data.

            - trade : trading currency for a given listing (i.e for Apple - USD, Tencent - HKD)
            - report : financial reporting currency for a given listing (i.e for Apple - USD, Tencent - CNY)
            - ISO3 currency : desired currency in ISO 4217 format (i.e USD, EUR, JPY, KRW, etc.)
        package : str, {'CIQ Market'}, default 'CIQ Market'
            | Desired data package in where the pricing data outputs from.

            .. admonition:: Warning
                :class: warning

                If an invalid package is entered without a license, an error will be generated as output.

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> vwap = prism.market.ask(adjustment='all', package='CIQ Market')
        >>> vwap_df = prism.get_data([vwap], 'KOSPI 200 Index', startdate='2019-01-01', enddate='2020-12-31', shownid=['ticker'])
        >>> vwap_df
               listingid        date          VWAP   ticker
        0       20113302  2019-01-02  44884.613444  A078930
        1       20113302  2019-01-03  44146.922268  A078930
        2       20113302  2019-01-04  44883.697058  A078930
        3       20113302  2019-01-07  45929.294117  A078930
        4       20113302  2019-01-08  45773.508402  A078930
        ...          ...         ...           ...      ...
        97551  643903265  2020-12-23  14429.849563  A272210
        97552  643903265  2020-12-24  15179.657143  A272210
        97553  643903265  2020-12-28  16643.755102  A272210
        97554  643903265  2020-12-29  17252.000000  A272210
        97555  643903265  2020-12-30  17067.000000  A272210
    """
    return _build_price(
        _VWAP,
        package=package,
        adjustment=adjustment,
        currency=currency,
    )


@_validate_args
def market_cap(currency: str = 'trade', package : str = 'CIQ Market'):
    """
    | Market capitalization history for equity securities aggregated to the company level.
    | Default frequency is daily.

    Parameters
    ----------

        currency : str {'trade', 'report', ISO3 currency}, default 'trade'
            | Desired currency for the pricing data.

            - trade : trading currency for a given listing (i.e for Apple - USD, Tencent - HKD)
            - report : financial reporting currency for a given listing (i.e for Apple - USD, Tencent - CNY)
            - ISO3 currency : desired currency in ISO 4217 format (i.e USD, EUR, JPY, KRW, etc.)

        package : str {'CIQ Market'}, default 'CIQ Market'
            | Desired data package in where the pricing data outputs from.

            .. admonition:: Warning
                :class: warning

                If an invalid package is entered without a license, an error will be generated as output.


    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> mcap = prism.market.market_cap()
        >>> mcap_df = mcap.get_data(universe=1, startdate='2010-01-01', enddate='2015-12-31', shownid=['ticker'])
        >>> mcap_df
                listingid        date     marketcap   Ticker
        0        20108718  2010-06-11  2.592000e+11  A004430
        1        20108718  2010-06-12  2.592000e+11  A004430
        2        20108718  2010-06-13  2.592000e+11  A004430
        3        20108718  2010-06-14  2.592000e+11  A004430
        4        20108718  2010-06-15  2.640000e+11  A004430
        ...           ...         ...           ...      ...
        437100  278631846  2015-12-27  2.433650e+13  A028260
        437101  278631846  2015-12-28  2.317036e+13  A028260
        437102  278631846  2015-12-29  2.375490e+13  A028260
        437103  278631846  2015-12-30  2.341962e+13  A028260
        437104  278631846  2015-12-31  2.341962e+13  A028260
    """
    return _MarketCap(currency=currency, package=package)


@_validate_args
def volume(adjustment: str = 'all', package : str = 'Prism Market'):
    """
    | Daily volume for equity securities.
    | Default frequency is business daily.

    Parameters
    ----------
        adjustment : str, {'all', 'split', 'dividend'}, default 'all'
            | Adjustment for pricing data.

            - all : apply both split and dividend adjustment
            - split : apply only split adjustment
            - dividend : apply only dividend adjustment

        package : str, {'Prism Market', 'Compustat', 'CIQ Market', 'MI Integrated Market'}, default 'Prism Market'
            | Desired data package in where the pricing data outputs from.

            .. admonition:: Warning
                :class: warning

                If an invalid package is entered without a license, an error will be generated as output.

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> volume = prism.market.volume(package='MI Integrated Market')
        >>> volume_df = prism.get_data([volume], 'KOSPI 200 Index', startdate='2019-01-01', enddate='2020-12-31', shownid=['ticker'])
        >>> volume_df
                listingid        date    volume   ticker
        0        20113302  2019-01-02  271000.0  A078930
        1        20113302  2019-01-03  178985.0  A078930
        2        20113302  2019-01-04  166248.0  A078930
        3        20113302  2019-01-07  118530.0  A078930
        4        20113302  2019-01-08  112217.0  A078930
        ...           ...         ...       ...      ...
        100638  686744025  2020-12-23  149780.0  A352820
        100639  686744025  2020-12-24  132606.0  A352820
        100640  686744025  2020-12-28  115532.0  A352820
        100641  686744025  2020-12-29  110664.0  A352820
        100642  686744025  2020-12-30  117489.0  A352820
    """
    return _Volume(adjustment=adjustment, package=package)


@_validate_args
def dividend(adjustment: bool = True, currency: str = 'trade', aggregate: bool = True, package : str = 'Prism Market'):
    """
    | Dividend history for equity securities.
    | Default frequency is aperiodic daily.

    Parameters
    ----------
        adjustment : bool, default True
            | Whether to apply split adjustment for dividend data.

        currency : str, {'trade', 'report', ISO3 currency}, default 'trade'
            | Desired currency for the pricing data.

            - trade : trading currency for a given listing (i.e for Apple - USD, Tencent - HKD)
            - report : financial reporting currency for a given listing (i.e for Apple - USD, Tencent - CNY)
            - ISO3 currency : desired currency in ISO 4217 format (i.e USD, EUR, JPY, KRW, etc.)
            - None : dividend payment currency

        aggregate: bool, default True
            | Desired aggregation for dividend. If True, dividends are aggregated based on listingid and exdate.

            - If `True`, paymentdate and dividendtype column will be dropped
            - If `True`, and currency is `None`, the currency will be automatically set to `trade`

        package : str, {'Prism Market', 'Compustat', 'CIQ Market'}, default 'Prism Market'
            | Desired data package in where the pricing data outputs from.

            .. admonition:: Warning
                :class: warning

                If an invalid package is entered without a license, an error will be generated as output.

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> dividend = prism.market.dividend(package='MI Integrated Market')
        >>> dividend _df = prism.get_data([dividend], 'KOSPI 200 Index', startdate='2019-01-01', enddate='2020-12-31', shownid=['ticker'])
        >>> dividend _df
              listingid        date  dividend  Ticker
        0       2586086  2010-02-11      0.14     AFL
        1       2586086  2010-05-17      0.14     AFL
        2       2586086  2010-08-16      0.14     AFL
        3       2586086  2010-11-15      0.15     AFL
        4       2586086  2011-02-11      0.15     AFL
                    ...         ...       ...     ...
        9544  344286611  2010-08-25      0.50     ITT
        9545  344286611  2010-11-09      0.50     ITT
        9546  344286611  2011-02-28      0.50     ITT
        9547  344286611  2011-05-18      0.50     ITT
        9548  344286611  2011-08-24      0.50     ITT
    """
    return _Dividend(adjustment=adjustment, currency=currency, aggregate = aggregate, package=package)


@_validate_args
def dividend_adjustment_factor(adjustment: bool = True, package : str = 'Prism Market'):
    """
    | Dividend adjustment factor history for equity securities.
    | Default frequency is daily.

    Parameters
    ----------
    adjustment : bool, default True
        | Split adjustment for dividend data.

    package : str, {'Prism Market', 'Compustat', 'CIQ Market'}, default 'Prism Market'
        | Desired data package in where the pricing data outputs from.

        .. admonition:: Warning
            :class: warning

            If an invalid package is entered without a license, an error will be generated as output.

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> divadj = prism.market.dividend_adjustment_factor()
        >>> divadj_df = divadj.get_data()
    """
    return _DividendAdjustmentFactor(adjustment=adjustment, package=package)


@_validate_args
def split(package : str ='Prism Market'):
    """
    | Return the split history for equity securities.
    | Default frequency is aperiodic daily.

    Parameters
    ----------
    package : str, {'Prism Market', 'Compustat', 'CIQ Market'}, default 'Prism Market'
        | Desired data package in where the pricing data outputs from.

        .. admonition:: Warning
            :class: warning

            If an invalid package is entered without a license, an error will be generated as output.

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> split = prism.market.split()
        >>> split_df = split.get_data(universe=1, startdate='2010-01-01', enddate='2015-12-31', shownid=['ticker'])
        >>> split_df
            listingid        date     split   Ticker
        0    20126254  2015-07-29  1.350000  A014830
        1    20158335  2013-04-30  0.100000  A008000
        2    20158445  2015-01-01  0.620935  A004150
        3    20158447  2010-12-29  1.030000  A001060
        4    20158758  2012-10-19  0.142857  A001440
        ..        ...         ...       ...      ...
        60  104646533  2014-09-01  0.478239  A060980
        61  107478344  2012-12-27  1.050000  A128940
        62  107478344  2014-02-10  1.050000  A128940
        63  107478344  2014-12-29  1.050000  A128940
        64  107478344  2015-12-29  1.020000  A128940
    """
    return _Split(package=package)


@_validate_args
def split_adjustment_factor(package : str = 'Prism Market'):
    """
    | Split adjustment factor history for equity securities.
    | Default frequency is daily.

    Parameters
    ----------
    package : str, {'Prism Market', 'Compustat', 'CIQ Market'}, default 'Prism Market'
        | Desired data package in where the pricing data outputs from.

        .. admonition:: Warning
            :class: warning

            If an invalid package is entered without a license, an error will be generated as output.

    Returns
    -------
        prism._PrismComponent
    """
    return _SplitAdjustmentFactor(package=package)


@_validate_args
def exchange_rate(currency: list, to_convert: bool = False, package : str = 'CIQ Market'):
    """
    | Daily exchange rate history.
    | Default frequency is daily.

    Parameters
    ----------
        currency : list of ISO3 currency
            | Desired exchange rates.
        to_convert : bool, default False
            | True
            | False : business daily
        package : str, {'Compustat', 'CIQ Market'}, default 'CIQ Market'
            | Desired data package in where the pricing data outputs from.

            .. admonition:: Warning
                :class: warning

                If an invalid package is entered without a license, an error will be generated as output.

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> exrt = prism.market.exchange_rate(currency=['USD', 'KRW'])
        >>> exrt_df = exrt.get_data(startdate='2010-01-01', enddate='2015-12-31')
        >>> exrt_df
            currency        date       exrt
        0         KRW  2010-01-01  1881.5000
        1         KRW  2010-01-02  1881.5000
        2         KRW  2010-01-03  1881.5000
        3         KRW  2010-01-04  1854.5000
        4         KRW  2010-01-05  1826.1000
        ...       ...         ...        ...
        3873      USD  2015-12-27     1.4933
        3874      USD  2015-12-28     1.4903
        3875      USD  2015-12-29     1.4795
        3876      USD  2015-12-30     1.4833
        3877      USD  2015-12-31     1.4740
    """
    return _ExchangeRate(currency=currency, to_convert=to_convert, pacakge=package)


@_validate_args
def short_interest(dataitemid: int, package : str = 'IHS Markit Short Interest'):
    """
    | Short interest dataitems for equity securities and global data coverage.
    | Default frequency is business daily.

    Parameters
    ----------
    dataitemid : int
        | Unique identifier for the different dataitem. This identifies the type of the value (Revenue, Expense, etc.)

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> prism.market.short_interest_dataitems(search='short')
           dataitemid                               dataitemname  ...  datamodule                packagename
        0     1100035                Broker Short Interest Value  ...        None  IHS Markit Short Interest
        1     1100055        Short Interest Ratio (Day to Cover)  ...        None  IHS Markit Short Interest
        2     1100056                      Short Interest Tenure  ...        None  IHS Markit Short Interest
        3     1100057                       Short Interest Value  ...        None  IHS Markit Short Interest
        4     1100058          Short Interest as % Of Free Float  ...        None  IHS Markit Short Interest
        5     1100059  Short Interest as % Of Shares Outstanding  ...        None  IHS Markit Short Interest
        6     1100060                                Short Score  ...        None  IHS Markit Short Interest
        7     1100063           Supply Side Short Interest Value  ...        None  IHS Markit Short Interest

        >>> short = prism.market.short_interest(dataitemid=1100057)
        >>> short_df = short.get_data(universe=1, startdate='2010-01-01', enddate='2015-12-31', shownid=['ticker'])
        >>> short_df
                listingid        date  shortinterestvalue   Ticker
        0        20108718  2010-06-11        1.288440e+08  A004430
        1        20108718  2010-06-14        1.288440e+08  A004430
        2        20108718  2010-06-15        1.298000e+08  A004430
        3        20108718  2010-06-16        1.309800e+08  A004430
        4        20108718  2010-06-17        6.660000e+07  A004430
        ...           ...         ...                 ...      ...
        305527  278631846  2015-12-25        7.331920e+10  A028260
        305528  278631846  2015-12-28        7.045744e+10  A028260
        305529  278631846  2015-12-29        7.223796e+10  A028260
        305530  278631846  2015-12-30        6.464626e+10  A028260
        305531  278631846  2015-12-31        6.800626e+10  A028260
    """
    return _ShortInterest(dataitemid=dataitemid, package=package)


@_validate_args
def dataitems(search : str = None, package : str = None):
    """
    Usable dataitems for the market data categories.

    Parameters
    ----------
        search : str, default None
            | Search word for Data Items name, the search is case-insensitive.
        package : str, default None
            | Search word for package name, the search is case-insensitive.

    Returns
    -------
        pandas.DataFrame
            Data items that belong to market data categories.

        Columns:
            - *dataitemid : int*
            - *dataitemname : str*
            - *dataitemdescription : str*
            - *datamodule : str*
            - *datacomponent : str*
            - *packagename : str*

    Examples
    --------
        >>> prism.market.dataitems(search='short')
            dataitemid                               dataitemname  ...   datacomponent                packagename
        0     1100035                Broker Short Interest Value  ...  Short Interest  IHS Markit Short Interest
        1     1100055        Short Interest Ratio (Day to Cover)  ...  Short Interest  IHS Markit Short Interest
        2     1100056                      Short Interest Tenure  ...  Short Interest  IHS Markit Short Interest
        3     1100057                       Short Interest Value  ...  Short Interest  IHS Markit Short Interest
        4     1100058          Short Interest as % Of Free Float  ...  Short Interest  IHS Markit Short Interest
        5     1100059  Short Interest as % Of Shares Outstanding  ...  Short Interest  IHS Markit Short Interest
        6     1100060                                Short Score  ...  Short Interest  IHS Markit Short Interest
        7     1100063           Supply Side Short Interest Value  ...  Short Interest  IHS Markit Short Interest
    """

    return _list_dataitem_market(None, search, package)


@_validate_args
def short_interest_dataitems(search : str = None, package : str = None):
    """
    Usable data items for the short_interest data component.

    Parameters
    ----------
        search : str, default None
            | Search word for data items name, the search is case-insensitive.
        package : str, default None
            | Search word for package name, the search is case-insensitive.

    Returns
    -------
        pandas.DataFrame
            Data items that belong to short_interest data component.

        Columns:
            - *dataitemid : int*
            - *dataitemname : str*
            - *dataitemdescription : str*
            - *datamodule : str*
            - *datacomponent : str*
            - *packagename : str*

    Examples
    --------
        >>> prism.market.short_interest_dataitems(search='short')
           dataitemid                               dataitemname  ...  datamodule                packagename
        0     1100035                Broker Short Interest Value  ...        None  IHS Markit Short Interest
        1     1100055        Short Interest Ratio (Day to Cover)  ...        None  IHS Markit Short Interest
        2     1100056                      Short Interest Tenure  ...        None  IHS Markit Short Interest
        3     1100057                       Short Interest Value  ...        None  IHS Markit Short Interest
        4     1100058          Short Interest as % Of Free Float  ...        None  IHS Markit Short Interest
        5     1100059  Short Interest as % Of Shares Outstanding  ...        None  IHS Markit Short Interest
        6     1100060                                Short Score  ...        None  IHS Markit Short Interest
        7     1100063           Supply Side Short Interest Value  ...        None  IHS Markit Short Interest
    """

    return _list_dataitem_market(_MarketDataComponentType.SHORT_INTEREST, search, package)
