import logging
import time
import json.decoder
import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
API_BASE = "https://cohost.org/api/v1"

cache = {}

headers = {
    'User-Agent': 'cohost.py'
}

timeout = 30


def fetch(method: str, endpoint, data: dict, cookies="", complex=False):
    """Send requests to cohost API, and return back data

    Args:
        method (_type_): _description_
        endpoint (_type_): _description_
        data (_type_): _description_
        cookies (str, optional): _description_. Defaults to "".
        complex (bool, optional): _description_. Defaults to False.

    Raises:
        Exception: _description_

    Returns:
        _type_: _description_
    """
    if not endpoint.startswith('/'):
        endpoint = "/" + endpoint
    url = API_BASE + endpoint
    logger.debug('{} to {}'.format(method, url))
    if method.lower() == "get":
        req = requests.get(url, cookies=cookies, params=data, headers=headers)
    elif method.lower() == "post":
        req = requests.post(url, cookies=cookies, data=data, headers=headers)
    elif method.lower() == 'postjson':
        req = requests.post(url, cookies=cookies, json=data, headers=headers)
    elif method.lower() == 'put':
        req = requests.put(url, cookies=cookies, json=data, headers=headers)
    else:
        logger.error('No such method handled: ' + method)
        logger.error('Defaulting to get')
        return fetch("GET", endpoint, data, cookies, complex)

    try:
        res = req.json()
    except json.decoder.JSONDecodeError:
        res = req.text

    if (req.status_code >= 400 and method != 'put'):
        raise Exception(res)
    if complex:
        return {
            'headers': req.headers,
            'body': res
        }
    return res


def fetchTrpc(methods: list, cookie: str,
              data: dict = None, methodType="get"):
    global cache
    """Fetch data from trpc API

    Args:
        methods (list): List of data points to retrieve
        cookie (str): Cookie of the user to retrieve from

    Returns:
        _type_: JSON encoded list from the trpc endpoint
    """
    if type(methods == str):
        m = methods
    else:
        m = ','.join(methods)
    if methodType == "get":
        cacheData = get_cache_data(cookie, m)
        if cacheData is not None:
            logger.debug('Cache hit!')
            return cacheData
    data = fetch(methodType, "/trpc/{}".format(m), data=data,
                 cookies=generate_login_cookies(cookie))
    if methodType == "get":
        set_cache_data(cookie, m, data)
    return data


# Caching utils !
def set_cache_data(cookie, key, data):
    if cache.get(cookie, None) is None:
        cache[cookie] = {}
    cache[cookie][key] = {
        'data': data,
        'time': time.time()
    }


def get_cache_data(cookie, key):
    entry = cache.get(cookie, {}).get(key, None)
    if entry is None:
        return None
    if time.time() - entry['time'] > timeout:
        return None
    return entry['data']


def generate_login_cookies(cookie):
    return {
        'connect.sid': cookie
    }
