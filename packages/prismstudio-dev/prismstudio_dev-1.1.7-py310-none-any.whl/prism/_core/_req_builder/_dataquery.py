import requests
import warnings
import webbrowser
from typing import List, Union

import orjson
import pandas as pd

from prism._utils.exceptions import PrismNotFoundError, PrismResponseError, PrismTypeError, PrismValueError

from ..._common.config import *
from ..._common.const import *
from prism import _core
from ..._utils import (
    _validate_args,
    get,
    post,
    patch,
    delete,
    _authentication,
    _process_fileresponse,
    _process_response,
    _fetch_and_parse,
    _get_web_authentication_token,
    Loader,
    download,
    plot_tree,
    get_sm_attributevalue,
    are_periods_exclusive,
)
from .preference import get_quiet_mode
from ..._prismcomponent import prismcomponent as pcmpt
from ._universe import parse_universe_to_universeid


__all__ = [
    "list_dataquery",
    "load_dataquery",
    "save_dataquery",
    "rename_dataquery",
    "delete_dataquery",
    "extract_dataquery",
    "get_data",
    "view_data",
]


@_validate_args
def list_dataquery(search: str = None, tree=False):
    """
    Return the list of all saved data queries available.

    Parameters
    ----------
        search : str, default None
            | Search word for data query name, the search is case-insensitive.
            | If None, the entire list is returned.

        tree : bool, default False
            | If True, the folder structure of the data queries is visualized in a UNIX-style.

    Returns
    -------
        bool or pandas.DataFrame
            | If tree is True, print file system tree of data queries.
            | If tree is False, return usable dataqueries in pandas.DataFrame.
            | Columns:

            - *dataqueryid*
            - *dataqueryname*

    Examples
    --------
        >>> prism.list_dataquery()
        dataqueryid  dataqueryname
        0  	           1	          ROE
        1	           2	          PER
        2	           3	          STD
    """
    dataqueries_df = _fetch_and_parse(URL_DATAQUERIES, "pdq", search)
    if dataqueries_df.empty:
        raise PrismNotFoundError("No Dataqueries found.")
    if not tree:
        return dataqueries_df
    plot_tree(dataqueries_df["dataqueryname"].tolist(), "dataquery")


@_validate_args
def load_dataquery(dataquery: Union[str, int]):
    """
    Load specified data queries.

    Parameters
    ----------
        dataquery : str or int
            Data query name (str) or data query id (int) to load.

    Returns
    -------
        prism._PrismComponent
            Return data query component.

    Examples
    --------
        >>> prism.load_dataquery(7)
        ==== Close
        Query Structure
    """
    headers = _authentication()
    dataqueryid = parse_dataquery_to_dataqueryid(dataquery)
    res = requests.get(url=URL_DATAQUERIES + f"/{dataqueryid}", headers=headers)
    if not res.ok:
        raise PrismResponseError(res.json()["message"])
    query = res.json()["rescontent"]["data"]["dataquerybody"]
    return _dataquery_to_component(query)


def _dataquery_to_component(query: dict):
    component_name = query["component_name"]
    category_component_info = COMPONENT2CATEGORY.get(component_name)
    if category_component_info is None:
        component = pcmpt._PrismComponent(**query)
    else:
        category_name = category_component_info["category"]
        component_fn_name = category_component_info["component"]
        category = getattr(_core, category_name)
        component_fn = getattr(category, component_fn_name)
        component = component_fn(**query["component_args"])
    return component


@_validate_args
def rename_dataquery(old: Union[str, int], new: str):
    """
    Rename data query. Location of data query within the folder structure can be changed using the method.

    Parameters
    ----------
        old: str or int
            Name of existing data query (str) or data query id (int) to be renamed.
        new: str
            New name of the data query.

    Returns
    -------
        status: dict
            Status of rename_dataquery.

    Examples
    --------
        >>> prism.list_dataquery()
        dataqueryid  dataqueryname
        0  	         1	          ROE
        1	           2	          PER
        2	           3	          STD

        >>> prism.rename_dataquery(old="PER", name="Price to Earnings")
        {
        'status': 'Success',
        'message': 'Dataquery renamed',
        'result': [{'resulttype': 'dataqueryid', 'resultvalue': 2}]
        }

        >>> prism.list_dataquery()
        dataqueryid      dataqueryname
        0  	         1	              ROE
        1	           2  Price to Earnings
        2	           3	              STD
    """
    should_overwrite, err_msg = should_overwrite_dataquery(new, "renaming")
    if not should_overwrite:
        return err_msg
    dataqueryid = parse_dataquery_to_dataqueryid(old)
    ret = patch(URL_DATAQUERIES + f"/{dataqueryid}", {"newpath": new + ".pdq"}, None)
    print(ret["message"])
    return ret


@_validate_args
def save_dataquery(component, dataqueryname: str):
    """
    Save data query.

    Parameters
    ----------
        component : prism._PrismComponent
            New PrismComponent to be saved.

        dataqueryname : str
            Name of the new data query.

    Returns
    -------
        status: dict
            Status of save_dataquery.

    Examples
    --------
        >>> prism.list_dataquery()
        dataqueryid  dataqueryname
        0  	         1	          ROE
        1	           2	          PER
        2	           3	          STD

        >>> c = prism.market.close()
        >>> prism.save_dataquery(component=c, name="close")
        {
        'status': 'Success',
        'message': 'Dataquery saved',
        'result': [{'resulttype': 'dataqueryid', 'resultvalue': 4}]
        }

        >>> prism.list_dataquery()
        dataqueryid  dataqueryname
        0  	         1	          ROE
        1	           2	          PER
        2	           3	          STD
        3	           4	        close
    """
    should_overwrite, err_msg = should_overwrite_dataquery(dataqueryname, "saving")
    if not should_overwrite:
        return err_msg

    ret = post(URL_DATAQUERIES, {"path": dataqueryname + ".pdq"}, component._query)
    print(f'{ret["message"]}: {ret["result"][0]["resulttype"]} is {ret["result"][0]["resultvalue"]}')
    return ret


@_validate_args
def delete_dataquery(dataquery: Union[str, int]):
    """
    Delete data query.

    Parameters
    ----------
        dataquery: str or int
            Data query name (str) or data query id (int) to delete.

    Returns
    -------
        status: dict
            Status of delete_dataquery.

    Examples
    --------
        >>> prism.list_dataquery()
        dataqueryid  dataqueryname
        0  	         1	          ROE
        1	           2	          PER
        2	           3	          STD

        >>> prism.delete_dataquery(1)
        {
        'status': 'Success',
        'message': 'Dataquery deleted',
        'result': [{'resulttype': 'dataqueryid', 'resultvalue': 1}]
        }

        >>> prism.list_dataquery()
        dataqueryid  dataqueryname
        0	           2	          PER
        1	           3	          STD

        >>> prism.delete_dataquery("STD")
        {
        'status': 'Success',
        'message': 'Dataquery deleted',
        'result': [{'resulttype': 'dataqueryid', 'resultvalue': 3}]
        }

        >>> prism.list_dataquery()
        dataqueryid  dataqueryname
        0	           2	          PER
    """

    dataqueryid = parse_dataquery_to_dataqueryid(dataquery)
    ret = delete(URL_DATAQUERIES + f"/{dataqueryid}")
    print(f'{ret["message"]}')
    return ret


@_validate_args
def datacomponent_args_info(component_name: str):
    return get(URL_COMPONENT + f"/datacomponent/{component_name}/args")


@_validate_args
def extract_dataquery(component: pcmpt._PrismComponent, return_code=False):
    """
    Generate code which reproduces the data query provided by the component. If return_code is False, the method returns None and prints the code.

    Parameters
    ----------
        component : PrismComponent
            PrismComponent whose data query is to be extracted. Data component or function component should be provided.

        return_code : bool, default False
            If True, the method returns the code. Else the code is printed as system output, returning None.

    Returns
    -------
        str or None
            | If return_code is True, return code in string.
            | If return_code is False, return None.

    Examples
    --------
        >>> ni = prism.financial.income_statement(100639, periodtype='LTM', package=None)
        >>> mcap = prism.market.market_cap(package=None)
        >>> ep = mcap/ni

        >>> prism.extract_dataquery(ep)
        x0 = prism.market.marketcap(currency=None, package="CIQ Market")
        x1 = prism.financial.income_statement(dataitemid=100639, periodtype="LTM", package="CIQ Premium Financials", preliminary=True, currency=None)
        x2 = x0 / x1
    """
    code = post(URL_DATAQUERIES + "/extract", {"dialect": "python"}, component._query)
    if return_code:
        return code
    else:
        print(code)


@_validate_args
def get_data(
    component: Union[pcmpt._AbstractPrismComponent, list],
    universe: Union[str, int] = None,
    startdate: str = None,
    enddate: str = None,
    shownid: list = None,
    display_pit: bool = True,
    name: Union[str, list] = None,
) -> pd.DataFrame:

    """
    Return data corresponding to the query of the component. Multiple components can be passed on, in which case tuple of dataframes are returned.

    Parameters
    ----------
        component : PrismComponent or list
            | PrismComponent which hold the logic to query data.

        universe : str or int, default None
            | Universe name (*str*) or universe id (*int*) used to query data.
            | Some components do not require universe information (eg. Exchange Rate), in which case to be left None.

        startdate : str, default None
            | Start date of the data. The data includes start date.
            | If None, the start date of the universe is used. The same applies when the input is earlier than the universe start date.

        enddate : str, default None
            | End date of the data. The data excludes end date.
            | If None, the end date of the universe is used. The same applies when the input is later than the universe end date.

        shownid : list, default None
            | List of Security Master attributes to display with the data.
            | See prism securitymaster list_attribute for full list of Security Master attributes.
            | If None, default attributes set in preferences is shown.
            | If empty list ([]), no attribute is shown.

        display_pit: bool, default True
            | If True, the data is shown as point-in-time format.
            | If False, the data is collapsed to display from the most recent view point.

        name : str or list, default None
            | Column names of the data to display.
            | If one component is passed to the function, accepts either string or list with one element.
            | If multiple components is passed to the function, accepts list of string.
            | If None:

            - If data component is passed, the column name is implicitly decided following the name of the data component.
            - If function component is passed, the default column name is 'value'.


    Returns
    -------
        pandas.DataFrame
            | Requested data component's DataFrame
            | Columns:

            - *listingid*
            - *date*
            - *value: can be provided by the user via 'name'*
            - *<attributes>: provided by the user via 'shownid'*
            - *period (Optional): for financial datacomponents*

    Examples
    --------
        >>> close = prism.market.close(adjustment='All', package='Prism Market')
        >>> close_df = prism.get_data(component=[close], universe='KOSPI 200 Index', startdate='2015-01-01', enddate='2020-12-31', shownid=['ticker'])
        >>> close_df
                listingid        date          Close   ticker
        0        20108718  2015-01-02    7740.611273  A004430
        1        20108718  2015-01-05    7874.399616  A004430
        2        20108718  2015-01-06    7903.068547  A004430
        3        20108718  2015-01-07    8313.989886  A004430
        4        20108718  2015-01-08    8161.088923  A004430
        ...           ...         ...            ...      ...
        298992  686744025  2020-12-23  151197.660000  A352820
    """

    query = []
    cmpts = set()
    if isinstance(name, list) & (name is not None):
        if any([not isinstance(n, str) for n in name]):
            raise PrismTypeError('Names shoud be string')

    def add_cmpts(o):
        cmpts = set()
        if o["component_type"] == "datacomponent":
            cmpts.add(o["component_name"])
        else:
            for c in o["children"]:
                cmpts = cmpts | add_cmpts(c)
        return cmpts

    if not isinstance(component, list):
        component = [component]
    for o in component:
        if isinstance(o, pcmpt._AbstractPrismComponent):
            query.append(o._query)
            cmpts = add_cmpts(o._query)
        else:
            raise PrismTypeError(f"Please provide Components into get data")

    if len(cmpts - set(UniverseFreeDataComponentType)) == 0:
        universeid = None
    else:
        universeid, _ = parse_universe_to_universeid(universe)

        universe_info = get(f"{URL_UNIVERSES}/{universeid}/info")
        universe_startdate = universe_info["Start Date"].values[0]
        universe_enddate = universe_info["End Date"].values[0]

        universe_period_violated = are_periods_exclusive(universe_startdate, universe_enddate, startdate, enddate)

        if universe_period_violated:
            raise PrismValueError(
                f'Query period should overlap with universe period ({str(universe_startdate).split("T")[0]} ~ {str(universe_enddate).split("T")[0]})'
            )

    default_shownid = True
    if (shownid is not None) and (len(shownid) == 0):
        shownid = None
        default_shownid = False
    if shownid is not None:
        shownid = [get_sm_attributevalue(a) for a in shownid]
    component_names = set([c._component_name for c in component])
    if (len(component_names - set(AggregateComponents)) == 0) & (shownid is not None):
        warnings.warn(f"Shownid will be ignored for: {list(component_names & set(AggregateComponents))}")

    params = {
        "universeid": universeid,
        "startdate": startdate,
        "enddate": enddate,
        "shownid": shownid,
        "default_shownid": default_shownid,
        "datanames": name,
        "metadata": False,
        "return_url": False,
        "display_pit": display_pit,
    }
    headers = _authentication()
    with Loader("\rFetching Data...") as l:
        try:
            res = requests.post(url=URL_DATAQUERIES + "/query", params=params, json=query, headers=headers)
        except:
            l.stop()
            raise PrismResponseError("Request ended with an error!")
        if res.status_code >= 400:
            l.stop()
            return _process_fileresponse(res, "data")
    links = _process_response(res)["urls"]
    res = requests.get(url=links, stream=True)
    ret = download(res)
    return _process_fileresponse(res, "tar", ret, file_type='tar')


@_validate_args
def view_data(
    component: Union[pcmpt._AbstractPrismComponent, list],
    universe: Union[str, int] = None,
    startdate: str = None,
    enddate: str = None,
    shownid: list = None,
    name: Union[str, list] = None,
):
    """
    Open data viewer window on a new browser tab. The data corresponding to the query of the component gets displayed on the data viewer. Multiple components can be passed on, in which case a merged table is displayed.

    Parameters
    ----------
        component : PrismComponent or list
            PrismComponent which hold the logic to query data.

        universe : str or int, default None
            | Universe name (str) or universe id (int) used to query data.
            | Some components do not require universe information (eg. Exchange Rate), in which case to be left None.

        startdate : str, default None
            | Start date of the data. The data includes start date.
            | If None, the start date of the universe is used. The same applies when the input is earlier than the universe start date.

        enddate : str, default None
            | End date of the data. The data excludes end date.
            | If None, the end date of the universe is used. The same applies when the input is later than the universe end date.

        shownid : list, default None
            | List of Security Master attributes to display with the data.
            | See 'prism securitymaster list_attribute' for full list of Security Master attributes.
            | If None, default attributes set in preferences is shown.
            | If empty list ([]), no attribute is shown.

        name : str or list, default None
            | Column names of the data to display.
            | If one component is passed to the function, accepts either string or list with one element.
            | If multiple components is passed to the function, accepts list of string.
            | If None:

            - If data component is passed, the column name is implicitly decided following the name of the data component.
            - If function component is passed, the default column name is 'value'.

        include_na : bool, default False
            | If True, universe data is left-joined to show missing (NA) values.
            | If False, the NA values are dropped.

    Returns
    -------
        None

    Notes
    -----
        The user will be asked to login if not already logged in.

    Examples
    --------
        >>> close = prism.market.close()
        >>> close.view_data(
                universe='Korea Stock Price 200 Index',
                startdate='2010-01-01',
                enddate='2011-01-01',
                shownid=['SEDOL', 'Country', 'GICS Group', 'GVKEY', 'Companyname', 'Fitch Issuer ID', 'ISIN']
            )
    """
    query = []
    cmpts = set()
    if isinstance(name, list) & (name is not None):
        if any([not isinstance(n, str) for n in name]):
            raise PrismTypeError('Names shoud be string')

    def add_cmpts(o):
        cmpts = set()
        if o["component_type"] == "datacomponent":
            cmpts.add(o["component_name"])
        else:
            for c in o["children"]:
                cmpts = cmpts | add_cmpts(c)
        return cmpts

    if not isinstance(component, list):
        component = [component]
    for o in component:
        if isinstance(o, pcmpt._AbstractPrismComponent):
            query.append(o._query)
            cmpts = add_cmpts(o._query)
        else:
            raise PrismTypeError(f"Please provide Components into get data.")

    if len(cmpts - set(UniverseFreeDataComponentType)) == 0:
        universeid = None
    else:
        universeid, universename = parse_universe_to_universeid(universe)

    universe_info = get(f"{URL_UNIVERSES}/{universeid}/info")
    universe_startdate = universe_info["Start Date"].values[0]
    universe_enddate = universe_info["End Date"].values[0]

    universe_period_violated = are_periods_exclusive(universe_startdate, universe_enddate, startdate, enddate)

    if universe_period_violated:
        raise PrismValueError(
            f'Query period should overlap with universe period ({str(universe_startdate).split("T")[0]} ~ {str(universe_enddate).split("T")[0]})'
        )

    if shownid is not None:
        shownid = [get_sm_attributevalue(a) for a in shownid]
    params = {
        "universeid": universeid,
        "startdate": startdate,
        "enddate": enddate,
        "shownid": shownid,
        "view": True,
        "return_url": True,
        "datanames": name,
    }
    headers = _authentication()
    with Loader("\rFetching Data...") as l:
        try:
            res = requests.post(url=URL_DATAQUERIES + "/query", params=params, json=query, headers=headers)
        except:
            l.stop()
            raise PrismResponseError("Request ended with an error!")
        if res.status_code >= 400:
            l.stop()
            return _process_fileresponse(res, "data")
    links = _process_response(res)["urls"]
    if len(links) == 0:
        print("The dataframe is empty.")
        return
    else:
        links = links[0]
    view_data_link = ROOT_EXT_WEB_URL + "/view?"
    for k, v in links.items():
        view_data_link += f"{k}={v}&"
    view_data_link += f'universe={universename.replace("&", "%26")}&startdate={startdate}&enddate={enddate}&'
    web_auth_token = _get_web_authentication_token()
    view_data_link += f"token={web_auth_token}"
    webbrowser.open(view_data_link, new=2)


@_validate_args
def parse_dataquery_to_dataqueryid(dataquery: Union[str, int]):
    dataqueries_df = _fetch_and_parse(URL_DATAQUERIES, "pdq")
    if dataqueries_df.empty:
        raise PrismNotFoundError("No dataqueries Found.")

    if isinstance(dataquery, int):
        dataqueries_df = dataqueries_df[dataqueries_df["dataqueryid"] == dataquery]
    elif isinstance(dataquery, str):
        dataqueries_df = dataqueries_df[dataqueries_df["dataqueryname"] == dataquery]
    else:
        raise PrismValueError("Please provide dataquery name or dataquery id for dataquery.")

    if dataqueries_df.empty:
        raise PrismNotFoundError(f"No dataquery matching: {dataquery}")

    dataqueryid = dataqueries_df["dataqueryid"].values[0]
    return dataqueryid


def should_overwrite_dataquery(dataqueryname, operation):
    if get_quiet_mode():
        return True, None
    dataqueries_df = _fetch_and_parse(URL_DATAQUERIES, "pdq")
    if dataqueries_df.empty:
        return True, None

    if dataqueryname in dataqueries_df["dataqueryname"].to_list():
        # overwrite = input(f"{dataqueryname} already exists. Do you want to overwrite? (Y/N) \n")
        overwrite = "y"
        if overwrite.lower() == "y":
            return True, None
        elif overwrite.lower() == "n":
            return False, f"Abort {operation} dataquery."
        else:
            return False, "Please provide a valid input."
    else:
        return True, None
