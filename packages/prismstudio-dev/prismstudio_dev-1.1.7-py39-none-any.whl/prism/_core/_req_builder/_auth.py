import requests
import hashlib
import uuid

import prism
from ..._common.config import *
from ..._utils import _validate_args, _create_token, get, _delete_token
from ..._common import const

__all__ = ['login']


@_validate_args
def login(username: str, password: str):
    """
    Log in to PrismStudio.

    Parameters
    ----------
        username : str
            A string representing the username of the user.
        password : str
            A string representing the password of the user.

    Returns
    -------
        str
            A string with a success message if the login is successful, or **None** if the login fails.
    """
    password = hashlib.sha512(password.encode())
    password = password.hexdigest()
    query = {'username': username, 'password': password}
    req_id = str(uuid.uuid4())[:8]
    headers = {'client-channel': 'python-extension', 'requestid': req_id}
    res = requests.post(url=URL_LOGIN, data=query, headers=headers)

    if res.ok:
        _create_token(res)
        smattributes = get(f'{URL_SM}/attributes')
        const.SMValues = {a['attributerepr']: a['attribute'] for a in smattributes}
        const.PreferenceType = get(f'{URL_PREFERENCES}/types')
        result = f'Login success! Welcome {username}'
    else:
        _delete_token()
        print(f'\033[91mLogin Failed\033[0m: Please check your username and password')
        return

    prism.username = username
    return result
