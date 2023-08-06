import asyncio
from dataclasses import dataclass, field

import aiohttp
import requests
from requests import Response




@dataclass
class Login:
    username: str
    password: str


@dataclass
class API:
    _url_prefix: str
    _auth_tokens: dict = field(default_factory=dict)

    def _put_extra_headers(self, kwargs):
        extra_headers = kwargs.get("headers")
        if self._auth_tokens or "login" in kwargs:
            if extra_headers is None:
                extra_headers = {}
                kwargs["headers"] = extra_headers
            for k, v in self._auth_tokens.items():
                extra_headers[f"Authorization-{k}"] = f"Bearer {v}"
            if "login" in kwargs:
                login = kwargs.pop("login")
                # auth = HTTPBasicAuth(login.username, login.password) if login else None
                auth = aiohttp.BasicAuth(login.username, login.password) if login else None
                extra_headers["Authorization"] = auth.encode()
    def http_get(self, path, **kwargs):
        return self.http_request("get", path, **kwargs)

    def http_put(self, path, **kwargs):
        return self.http_request("put", path, **kwargs)


    def http_patch(self, path, **kwargs):
        return self.http_request("patch", path, **kwargs)

    def http_post(self, path, **kwargs):
        return self.http_request("post", path, **kwargs)

    def http_delete(self, path, **kwargs):
        return self.http_request("delete", path, **kwargs)

    def http_request(self, method, path, **kwargs):
        url = self._url_prefix + path
        self._put_extra_headers(kwargs)
        return http_request(method, url, **kwargs)

    def async_requests(self, reqs):
        for r in reqs:
            r["url"] = self._url_prefix + r.pop("path")
            self._put_extra_headers(r)
        async_requests(reqs)




# https://www.twilio.com/blog/asynchronous-http-requests-in-python-with-aiohttp
def async_requests(reqs):
    from mstuff.mstuff import obj





    async def main():
        async with aiohttp.ClientSession() as session:
            async def send_request(**req_kwargs):
                async with session.request(**req_kwargs) as resp:
                    await resp.read()
                    # noinspection PyTypeChecker
                    _default_resp_checker(obj(dict(status_code=resp.status, url=resp.url)))

            tasks = []
            for req in reqs:
                tasks.append(asyncio.ensure_future(send_request(**req)))

            await asyncio.gather(*tasks)



    asyncio.run(main())




def _default_resp_checker(resp: Response):
    status = resp.status_code
    url = resp.url
    if status >= 300:
        raise Exception(f"{status=} {url=}")
    return True


@dataclass
class StatusMustBe:
    status: int

    def __call__(self, resp: Response):
        status = resp.status_code
        url = resp.url
        if status != self.status:
            raise Exception(f"Expected status {self.status} but got {status=} {url=}")


def http_get(path, **kwargs):
    return http_request("get", path=path, **kwargs)


def http_put(path, **kwargs):
    return http_request("put", path=path, **kwargs)


def http_patch(path, **kwargs):
    return http_request("patch", path=path ** kwargs)


def http_post(path, **kwargs):
    return http_request("post", path=path, **kwargs)


def http_delete(path, **kwargs):
    return http_request("delete", path=path, **kwargs)


def http_request(
        method: str,
        path: str,
        json=None,
        data=None,
        params=None,
        headers=None,
        status_checker=_default_resp_checker,
        **kwargs
):
    resp = requests.request(method, path, json=json, data=data, params=params, headers=headers, **kwargs)
    if status_checker is not None:
        status_checker(resp)
    return resp
