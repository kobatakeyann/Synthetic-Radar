from urllib.request import Request, urlopen, _UrlopenRet
from urllib.error import HTTPError, URLError


def get_response(url:str) -> Request:
    try:
        req = Request(url)
    except URLError as err:
        raise URLError(err)
    else:
        return req

def read_response(response:Request) -> _UrlopenRet:
    try:
        with urlopen(response) as res:
            res_data = res.read()
    except HTTPError as err:
        raise HTTPError(err.url, err.code, err.reason, err.headers, err.fp)
    else:
        return res_data
