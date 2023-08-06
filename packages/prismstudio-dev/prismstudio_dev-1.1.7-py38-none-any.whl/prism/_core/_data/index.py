from typing import Union

from prism._utils.exceptions import PrismTypeError
from .._req_builder._list import _list_dataitem_index
from ..._prismcomponent.datacomponent import _IndexLevel, _IndexShare, _IndexWeight
from ..._common.const import INDEXLEVELTYPE2ID, IndexDataComponentType
from ..._utils import _validate_args

__all__ = [
    "share",
    "weight",
    "level",
    "share_dataitems",
    "weight_dataitems",
    "level_dataitems",
    "universe_dataitems",
    "portfolio_dataitems",
    "dataitems"]


@_validate_args
def share(dataitemid: int):
    """
    | Index constituent share data.
    | Default frequency is business daily.

    Parameters
    ----------
        dataitemid : int
            | Unique identifier for the different data item. This identifies the type of the balance sheet value (Revenue, Expense, etc.)

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> di = prism.index.share_dataitems("Russell 3000 Index")
        >>> di[["dataitemid", "dataitemname"]]
           dataitemid        dataitemname
        0     4000099  Russell 3000 Index

        >>> rus = prism.index.share(4000099)
        >>> rus_df = rus.get_data(startdate='2010-01-01', enddate='2020-12-31', shownid=["Company Name"])
        >>> rus_df
                 listingid        date	     value	         Company Name
        0          2598345  2012-06-25  15863000.0  CARRIAGE SERVICES INC
        1          2598345  2012-06-26  15863000.0  CARRIAGE SERVICES INC
        2          2598345  2012-06-27  15863000.0  CARRIAGE SERVICES INC
        3          2598345  2012-06-28  15863000.0  CARRIAGE SERVICES INC
        4          2598345  2012-06-29  15863000.0  CARRIAGE SERVICES INC
        ...            ...         ...         ...                    ...
        2810518  403068703  2014-06-30  16860000.0   TRI POINTE HOMES INC
        2810519  403068703  2014-07-01  16860000.0   TRI POINTE HOMES INC
        2810520  403068703  2014-07-02  16860000.0   TRI POINTE HOMES INC
        2810521  403068703  2014-07-03  16860000.0   TRI POINTE HOMES INC
        2810522  403068703  2014-07-07  16860000.0   TRI POINTE HOMES INC
    """
    return _IndexShare(dataitemid=dataitemid)


@_validate_args
def weight(dataitemid: int):
    """
    | Index constituent weight data.
    | Default frequency is business daily.

    Parameters
    ----------
        dataitemid : int
            | Unique identifier for the different data item. This identifies the type of the balance sheet value (Revenue, Expense, etc.)

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> di = prism.index.weight_dataitems("Russell 3000 Index")
        >>> di[["dataitemid", "dataitemname"]]
           dataitemid        dataitemname
        0     4000099  Russell 3000 Index

        >>> rus = prism.index.weight(4000099)
        >>> rus_df = rus.get_data(startdate='2010-01-01', enddate='2020-12-31', shownid=["Company Name"])
        >>> rus_df
                 listingid        date     value           Company Name
        0          2598345  2012-06-25  0.000009  CARRIAGE SERVICES INC
        1          2598345  2012-06-26  0.000009  CARRIAGE SERVICES INC
        2          2598345  2012-06-27  0.000009  CARRIAGE SERVICES INC
        3          2598345  2012-06-28  0.000009  CARRIAGE SERVICES INC
        4          2598345  2012-06-29  0.000009  CARRIAGE SERVICES INC
        ...            ...         ...       ...                    ...
        5989430  692043613  2020-12-23  0.000013         MEDIAALPHA INC
        5989431  692043613  2020-12-24  0.000013         MEDIAALPHA INC
        5989432  692043613  2020-12-28  0.000012         MEDIAALPHA INC
        5989433  692043613  2020-12-29  0.000011	     MEDIAALPHA INC
        5989434  692043613  2020-12-30  0.000011	     MEDIAALPHA INC
    """
    return _IndexWeight(dataitemid=dataitemid)


@_validate_args
def level(dataitemid: int, leveltype: Union[str, int]=None, package: str = None):
    """
    | Index level data.
    | Default frequency is business daily.

    Parameters
    ----------
        dataitemid : int
            | Unique identifier for the different data item. This identifies the type of the balance sheet value (Revenue, Expense, etc.)

        leveltype : str, default None, {'Price Return', 'Total Return Gross'}
            | Default value None gives all leveltype.

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> di = prism.index.level_dataitems("Russell 3000 Index")
        >>> di[["dataitemid", "dataitemname"]]
           dataitemid        dataitemname
        0     4000099  Russell 3000 Index

        >>> rus = prism.index.level(4000099)
        >>> rus_df = rus.get_data(startdate='2010-01-01', enddate='2020-12-31')
        >>> rus_df
                     date           leveltype       value
        0      2010-01-04  Total Return Gross  2925.36135
        1      2010-01-05  Total Return Gross  2933.81744
        2      2010-01-06  Total Return Gross  2937.46528
        3      2010-01-07  Total Return Gross  2949.90064
        4      2010-01-08  Total Return Gross  2959.37327
        ...           ...                 ...         ...
        11067  2020-12-23    Total Return Net  3243.92347
        11068  2020-12-24    Total Return Net  3252.86186
        11069  2020-12-28    Total Return Net  3270.69819
        11070  2020-12-29    Total Return Net  3257.80733
        11071  2020-12-30    Total Return Net  3266.55282
    """
    leveltypeid = None
    if leveltype is not None:
        if isinstance(leveltype, str):
            leveltypeid = INDEXLEVELTYPE2ID.get(leveltype)
            if leveltypeid is None:
                raise PrismTypeError(f"Level Type should be one of: {list(INDEXLEVELTYPE2ID.keys())}")
        elif isinstance(leveltype, int):
            leveltypeid = leveltype
            if leveltype not in INDEXLEVELTYPE2ID.values():
                raise PrismTypeError(f"Level Type ID should be one of: {list(INDEXLEVELTYPE2ID.values())}")
    return _IndexLevel(dataitemid=dataitemid, leveltypeid=leveltypeid, package=package)


@_validate_args
def share_dataitems(search: str = None, package: str = None):
    """
    Usable data items for the share data component.

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

        Columns :
            - *datamodule*
            - *datacomponent*
            - *dataitemid*
            - *datadescription*


    Examples
    --------
        >>> di = prism.index.share_dataitems("Russell 3000 Index")
        >>> di[["dataitemid", "dataitemname"]]
           dataitemid        dataitemname
        0     4000099  Russell 3000 Index
    """
    ret = _list_dataitem_index(
        datacomponent=IndexDataComponentType.SHARE,
        search=search,
        package=package,
    )
    ret = ret.drop(["dataitemdescription"], axis=1, errors="ignore")
    return ret


@_validate_args
def weight_dataitems(search: str = None, package: str = None):
    """
    Usable data items for the weight data component.

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

        Columns :
            - *datamodule*
            - *datacomponent*
            - *dataitemid*
            - *datadescription*

    Examples
    --------
        >>> di = prism.index.weight_dataitems("Russell 3000 Index")
        >>> di[["dataitemid", "dataitemname"]]
           dataitemid        dataitemname
        0     4000099  Russell 3000 Index
    """
    ret = _list_dataitem_index(
        datacomponent=IndexDataComponentType.WEIGHT,
        search=search,
        package=package,
    )
    ret = ret.drop(["dataitemdescription"], axis=1, errors="ignore")
    return ret


@_validate_args
def level_dataitems(search: str = None, package: str = None):
    """
    Usable data items for the level data component.

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

        Columns :
            - *datamodule*
            - *datacomponent*
            - *dataitemid*
            - *datadescription*

    Examples
    --------
        >>> di = prism.index.level_dataitems("Russell 3000 Index")
        >>> di[["dataitemid", "dataitemname"]]
           dataitemid        dataitemname
        0     4000099  Russell 3000 Index
    """
    ret = _list_dataitem_index(datacomponent=IndexDataComponentType.LEVEL, search=search, package=package)
    ret = ret.drop(["dataitemdescription"], axis=1, errors="ignore")
    return ret


@_validate_args
def universe_dataitems(search: str = None, package: str = None):
    """
    Usable data items for the index data category, which can be used to create universe in prism.save_index_as_universe()

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
    >>> di = prism.index.universe_dataitems("Korea Stock Price 200 Index")
    >>> di[["dataitemid", "dataitemname"]]
       dataitemid                 dataitemname
    0     6000034  Korea Stock Price 200 Index
    1     6000034  Korea Stock Price 200 Index
    """
    ret = _list_dataitem_index(datacomponent="Universe", search=search, package=package)
    ret = ret.drop(["dataitemdescription"], axis=1, errors="ignore")
    return ret


@_validate_args
def portfolio_dataitems(search: str = None, package: str = None):
    """
    Usable data items for the index data category, which can be used to create portfolio in prism.save_index_as_portfolio().

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
        >>> di = prism.index.portfolio_dataitems("Russell 3000 Index")
        >>> di[["dataitemid", "dataitemname"]]
           dataitemid        dataitemname
        0     4000099  Russell 3000 Index
    """
    ret = _list_dataitem_index(datacomponent="Portfolio", search=search, package=package)
    ret = ret.drop(["dataitemdescription"], axis=1, errors="ignore")
    return ret


@_validate_args
def dataitems(search: str = None, package: str = None):
    """
    Usable data items for the index data category.

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
    >>> di = prism.index.dataitems("Korea Stock Price 200 Index")
    >>> di[["dataitemid", "dataitemname"]]
       dataitemid                 dataitemname
    0     6000034  Korea Stock Price 200 Index
    1     6000034  Korea Stock Price 200 Index
    """
    ret = _list_dataitem_index(datacomponent=None, search=search, package=package)
    ret = ret.drop(["dataitemdescription"], axis=1, errors="ignore")
    return ret
