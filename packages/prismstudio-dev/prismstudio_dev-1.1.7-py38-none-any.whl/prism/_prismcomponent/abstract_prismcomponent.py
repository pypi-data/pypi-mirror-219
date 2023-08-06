import copy
import json
import pandas as pd
import traceback
from abc import ABC
from uuid import UUID
from typing import Union


from .._core._req_builder import _dataquery
from .._utils import _validate_args, _req_call
from .._utils.exceptions import PrismNotFoundError, PrismTypeError
from .._common.const import PrismComponentType


class _AbstractPrismComponent(ABC):
    """
    Args:
        query(dict): incl. component_type, component_name, component_args, children
    """

    def __init__(
        self,
        *,
        component_type: str,
        component_name: str,
        component_args: dict = {},
        children: list,
        component_category: str = None,
        nodeid: UUID = None,
        query_name: str = None,
    ):
        # if not hasattr(self, '_func_name'): self._func_name = func_name
        if component_type == PrismComponentType.FUNCTION_COMPONENT:
            if not hasattr(self, "_component_name"):
                self._component_name = component_name
            if not hasattr(self, "_component_category"):
                self._component_category = component_category
        self._query = {
            "component_type": component_type,
            "component_category": component_category,
            "component_name": component_name,
            "component_args": component_args,
            "children": children,
            "nodeid": nodeid,
        }
        try:
            json.dumps(self._query)
        except:
            raise PrismTypeError("Invalid types in query! Please use basic python types for constructing query!")


    def __repr__(self):
        self.query(verbose=False)
        return "Query Structure"

    def _dict_to_tree(self, query: dict, verbose: bool, depth: int = 0):
        if not verbose:
            try:
                print("\t" * depth, "====", query["component_name"])
                for c in query["children"]:
                    self._dict_to_tree(c, False, depth + 1)
            except:
                pass
        else:
            try:
                print(
                    "\t" * depth,
                    "====",
                    query["component_category"] + "/" + query["component_name"] if query["component_category"] is not None else query["component_name"],
                )
                if len(query["component_args"]) > 0:
                    print(
                        "\t" * (depth + 1),
                        "parameters: {",
                    )
                    for k, v in query["component_args"].items():
                        if "_dataquery" in k:
                            print("\t" * (depth + 2), k.split("_dataquery")[0], ":")
                            if isinstance(v, list):
                                for d in v:
                                    print(self._dict_to_tree(d, True, depth + 2))
                            else:
                                print(self._dict_to_tree(v, True, depth + 2))
                        else:
                            print("\t" * (depth + 2), k, ":", v)
                    print("\t" * (depth + 2), "}")
                else:
                    print("\t" * (depth + 1), "parameters: {}")
                for idx, c in enumerate(query["children"]):
                    if (self._component_name == "map") & (idx != 0):
                        break
                    self._dict_to_tree(c, True, depth + 1)
            except:
                pass

    def copy(self):
        """
        Return a deep copy of PrismComponent.

        Returns
        -------
            PrismComponent
                A deep copy of PrismComponent object

        Examples
        --------
            >>> o = prism.market.open()
            >>> intraday_r = c/o
            >>> intraday_r.query()
            ==== __truediv__
                parameters: {}
                ==== MarketDataComponentType.CLOSE
                    parameters: {
                        package : None
                        adjustment : True
                        currency : None
                        }
                ==== MarketDataComponentType.OPEN
                    parameters: {
                        package : None
                        adjustment : True
                        currency : None

            >>> intraday_r_copy = intraday_r.copy()
            >>> intraday_r_copy.query()
            ==== __truediv__
                parameters: {}
                ==== MarketDataComponentType.CLOSE
                    parameters: {
                        package : None
                        adjustment : True
                        currency : None
                        }
                ==== MarketDataComponentType.OPEN
                    parameters: {
                        package : None
                        adjustment : True
                        currency : None

        """
        return copy.deepcopy(self)

    def query(self, verbose: bool = True):
        """
        Print query held by the component represented in a tree format.

        Parameters
        ----------
            verbose : bool, default True
                | Option to run execution in 'verbose' mode.
                | If True, the parameter details are also printed.

        Returns
        -------
            None
                Print query held by the component represented in a tree format.

        Examples
        --------
            >>> c = prism.market.close()
            >>> o = prism.market.open()
            >>> intraday_r = c/o
            >>> print(intraday_r )
            === __truediv__
            ==== MarketDataComponentType.CLOSE
            ==== MarketDataComponentType.OPEN
            Query Structure

            >>> intraday_r.query()
            ==== __truediv__
                parameters: {}
                ==== MarketDataComponentType.CLOSE
                    parameters: {
                        package : None
                        adjustment : True
                        currency : None
                        }
                ==== MarketDataComponentType.OPEN
                    parameters: {
                        package : None
                        adjustment : True
                        currency : None
                        }
        """
        self._dict_to_tree(self._query, verbose)

    @_validate_args
    @_req_call(_dataquery)
    def get_data(
        self,
        universe: Union[str, int],
        startdate: str = None,
        enddate: str = None,
        shownid: list = None,
        display_pit: bool = True,
        name: list = None,
    ) -> pd.DataFrame:
        """
        This is an alias to :func:`prism.get_data`.
        """
        ...

    @_validate_args
    @_req_call(_dataquery)
    def view_data(
        self,
        universe,
        startdate: str = None,
        enddate: str = None,
        shownid: list = None,
        name: list = None,
    ) -> pd.DataFrame: ...

    @_validate_args
    def save(self, name: str):
        """
        If the component is a data component, this is an alias to :func:`prism.save_dataquery`
        and if the component is a task component, this is an alias to :func:`prism.save_taskquery`
        """
        return _dataquery.save_dataquery(self, name)

    @_validate_args
    def extract(self, return_code=False):
        """
        If the component is a data component, this is an alias to :func:`prism.extract_dataquery`
        and if the component is a task component, this is an alias to :func:`prism.extract_taskquery`
        """
        return _dataquery.extract_dataquery(self, return_code)
