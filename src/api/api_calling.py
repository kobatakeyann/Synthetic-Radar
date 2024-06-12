from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from util.tempfile_name import generate_random_string
from util.path_complement import generate_path


def get_response(url:str) -> Request:
    try:
        req = Request(url)
        return req
    except URLError as err:
        raise URLError(err)

def read_response(req:Request):
    try:
        with urlopen(req) as res:
            res_data = res.read()
    except HTTPError as err:
        raise HTTPError(err.url, err.code, err.reason, err.headers, err.fp)
    else:
        return res_data

def write_down_res(res_data) -> str:
    random_string = generate_random_string(100)
    tmpfile = generate_path(f"/tmp/tmp{random_string}.tar")
    with open(tmpfile, mode='wb') as f:
        f.write(res_data)
    output_path = tmpfile
    return output_path
