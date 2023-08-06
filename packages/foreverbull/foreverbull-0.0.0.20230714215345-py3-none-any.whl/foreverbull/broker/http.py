import os

import requests

from .exceptions import RequestError

host = os.getenv("BROKER_URL", "127.0.0.1:8080")
s = requests.Session()


def api_call(func):
    def wrapper(*args, **kwargs):
        req: requests.Request = func(*args, **kwargs)
        req.url = f"http://{host}{req.url}"
        rsp = s.send(req.prepare())
        if not rsp.ok:
            if rsp.status_code == 404:
                return None

            code = rsp.status_code
            raise RequestError(
                f"""{req.method} call {req.url} gave bad return code: {code}
            Text: {rsp.text}"""
            )
        return rsp.json()

    return wrapper
