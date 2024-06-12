from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


def get_response(url:str) -> Request:
    try:
        response = Request(url)
        return response
    except URLError as err:
        raise URLError(err)

def read_response(response:Request):
    try:
        with urlopen(response) as res:
            res_data = res.read()
        return res_data
    except HTTPError as err:
        raise HTTPError(err.url, err.code, err.reason, err.headers, err.fp)
