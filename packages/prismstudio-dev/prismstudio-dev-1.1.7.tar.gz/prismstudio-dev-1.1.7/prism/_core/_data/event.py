from ..._common.const import EventDataComponentType as _EventDataComponentType
from .._req_builder._list import _list_dataitem_event
from ..._prismcomponent.datacomponent import _News
from ..._utils.validate_utils import _validate_args

__all__ = ['news', 'dataitems', 'news_dataitems']


@_validate_args
def _build_event(
    datacomponentclass,
    dataitemid: int,
    datetype: str = 'entereddate',
    package: str = None,
):
    return datacomponentclass(
        dataitemid=dataitemid,
        datetype=datetype,
        package=package,
    )


def news(
    dataitemid: int,
    datetype: str = 'entereddate',
    package: str = None,
):
    """
    | News data for a specific event type.
    | Default frequency is aperiodic.

    Parameters
    ----------
        dataitemid : int
            | Unique identifier for the different data item. This identifies the type of the value (Revenue, Expense, etc.)

        datetype : str, {'entereddate', 'announceddate'}, default 'entereddate'
            | Datetype determines which date is fetched.

            - entereddate: when news data is inserted to the database
            - announceddate: when news data is announced
            
    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> di = prism.event.dataitems()
        >>> di[["dataitemid", "dataitemname"]]
           dataitemid                                  dataitemname
        0      400001                               Address Changes
        1      400002                          Analyst/Investor Day
        2      400003  Announcement of Interim Management Statement
        3      400004             Announcement of Operating Results
        4      400005                     Announcements of Earnings
        ...       ...                                           ...
        156    400157                         Stock Dividends (<5%)
        157    400158    Stock Splits & Significant Stock Dividends
        158    400159                           Strategic Alliances
        159    400160                 Structured Products Offerings
        160    400161                                Ticker Changes

        >>> news = prism.event.news(dataitemid=400005)
        >>> news_df = news.get_data(universe="S&P 500", startdate="2010-01-01", enddate="2015-12-31", shownid=["Company Name"])
        >>> news_df
               listingid                 date                                           headline                                            content                 Company Name
        0        2588294  2010-04-28 22:51:00  The Allstate Corporation Reports Earnings Resu...  The Allstate Corporation reported earnings res...                ALLSTATE CORP
        1        2588294  2010-02-11 00:55:00  Allstate Corp. Reports Earnings Results for th...  Allstate Corp. reported earnings results for t...                ALLSTATE CORP
        2        2588294  2010-04-28 22:40:00  The Allstate Corporation Reports Earnings Resu...  The Allstate Corporation reported earnings res...                ALLSTATE CORP
        3        2588294  2010-10-27 23:36:00  The Allstate Corporation Reports Unaudited Con...  The Allstate Corporation reported unaudited co...                ALLSTATE CORP
        4        2588294  2011-08-02 00:09:00  Allstate Corp. Reports Earnings Results for th...  Allstate Corp. reported earnings results for t...                ALLSTATE CORP
        ...          ...                  ...                                                ...                                                ...                          ...
        13056  302980253  2015-10-20 00:03:00  NiSource Gas Transmission & Storage Company Re...  NiSource Gas Transmission & Storage Company re...  COLUMBIA PIPELINE GROUP INC
        13057  302980253  2015-10-20 00:03:00  NiSource Gas Transmission & Storage Company An...  NiSource Gas Transmission & Storage Company an...  COLUMBIA PIPELINE GROUP INC
        13058  302980253  2015-10-20 00:03:00  NiSource Gas Transmission & Storage Company Re...  NiSource Gas Transmission & Storage Company re...  COLUMBIA PIPELINE GROUP INC
        13059  302980253  2015-11-03 07:42:00  Columbia Pipeline Group, Inc. Announces Unaudi...  Columbia Pipeline Group, Inc. announced unaudi...  COLUMBIA PIPELINE GROUP INC
        13060  316754620  2015-12-02 21:26:00  Computer Sciences GS Business Reports Unaudite...  Computer Sciences GS Business reported unaudit...                     CSRA INC
    """
    return _build_event(
        _News,
        dataitemid=dataitemid,
        datetype=datetype,
        package=package,
    )


def dataitems(search: str = None, package: str = None):
    """
    Usable data items for the event data category.

    Parameters
    ----------
        search : str, default None
            | Search word for dataitems name, the search is case-insensitive.

        package : str, default None
            | Search word for package name, the search is case-insensitive.

    Returns
    -------
        pandas.DataFrame
            Data items that belong to cash flow statement data component.

        Columns:
            - *datamodule*
            - *datacomponent*
            - *dataitemid*
            - *datadescription*


    Examples
    --------
        >>> di = prism.event.dataitems()
        >>> di[["dataitemid", "dataitemname"]]
           dataitemid                                  dataitemname
        0      400001                               Address Changes
        1      400002                          Analyst/Investor Day
        2      400003  Announcement of Interim Management Statement
        3      400004             Announcement of Operating Results
        4      400005                     Announcements of Earnings
        ...       ...                                           ...
        156    400157                         Stock Dividends (<5%)
        157    400158    Stock Splits & Significant Stock Dividends
        158    400159                           Strategic Alliances
        159    400160                 Structured Products Offerings
        160    400161                                Ticker Changes
    """
    return _list_dataitem_event(None, search, package)


@_validate_args
def news_dataitems(search: str = None, package: str = None):
    """
    Usable data items for the news data component.

    Parameters
    ----------
        search : str, default None
            | Search word for dataitems name, the search is case-insensitive.

        package : str, default None
            | Search word for package name, the search is case-insensitive.

    Returns
    -------
        pandas.DataFrame
            Data items that belong to cash flow statement data component.

        Columns:
            - *datamodule*
            - *datacomponent*
            - *dataitemid*
            - *datadescription*


    Examples
    --------
        >>> di = prism.event.news_dataitems()
        >>> di[["dataitemid", "dataitemname"]]
           dataitemid                                  dataitemname
        0      400001                               Address Changes
        1      400002                          Analyst/Investor Day
        2      400003  Announcement of Interim Management Statement
        3      400004             Announcement of Operating Results
        4      400005                     Announcements of Earnings
        ...       ...                                           ...
        156    400157                         Stock Dividends (<5%)
        157    400158    Stock Splits & Significant Stock Dividends
        158    400159                           Strategic Alliances
        159    400160                 Structured Products Offerings
        160    400161                                Ticker Changes
    """

    return _list_dataitem_event(_EventDataComponentType.NEWS, search, package)
