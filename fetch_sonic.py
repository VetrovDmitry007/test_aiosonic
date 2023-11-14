import base64
import aiosonic
import asyncio
from typing import Optional, Tuple, Dict, Any

from aiosonic import Timeouts, Proxy

DEFAULT_CONNECT_TIMEOUT = 10
DEFAULT_REQUEST_TIMEOUT = 3600
DEFAULT_BUFFER_SIZE = 128 * 1024
DEFAULT_MAX_REDIRECTS = 5


async def fetch_sonic(
        url: str,
        method: str = "GET",
        headers: Dict = None,
        body: Dict = None, # Optional[bytes]
        connect_timeout=DEFAULT_CONNECT_TIMEOUT,
        request_timeout=DEFAULT_REQUEST_TIMEOUT,
        # resolver=resolve,
        # max_buffer_size=DEFAULT_BUFFER_SIZE,
        follow_redirects: bool = False,
        max_redirects=DEFAULT_MAX_REDIRECTS, # request() -> max_redirects = 30
        validate_cert: bool = False,  # config.http_client.validate_certs,
        allow_proxy: bool = False,
        proxies=None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        # content_encoding: Optional[str] = None,
        # eof_mark: Optional[bytes] = None,
) -> Tuple[int, Dict[str, Any], bytes]:

    # Include basic auth header
    if user and password:
        auth = base64.b64encode(f"{user}:{password}".encode()).decode()
        header_aut = {"Authorization":  b"Basic %s" % auth}
        if headers:
            headers.update(header_aut)
        else:
            headers = header_aut
    # Checking proxy usage
    if proxies and allow_proxy:
        proxy = Proxy(host=proxies)
    else:
        proxy = None
    # Sending a request
    async with aiosonic.HTTPClient(verify_ssl=validate_cert, proxy=proxy) as client:
        timeouts = Timeouts(sock_read=request_timeout, sock_connect=connect_timeout)
        if method == "GET":
            response = await client.get(url, headers=headers, timeouts=timeouts, follow=follow_redirects)
        elif method == "POST":
            response = await client.post(url, headers=headers, timeouts=timeouts, data=body, follow=follow_redirects)
        elif method == "PUT":
            response = await client.put(url, headers=headers, timeouts=timeouts,  data="" if body is None else body, follow=follow_redirects)
        elif method == "DELETE":
            response = await client.delete(url, headers=headers, timeouts=timeouts, follow=follow_redirects)
        status = response.status_code
        headers = dict(response.headers)
        body = response.body
        await response.connection.release()
    return (status, headers, body)


async def test_get():
    print('-'*30)
    print('Start GET request.')
    url = 'https://httpbin.org/get'
    method = 'GET'
    status, headers, body = await fetch_sonic(
        url,
        method=method,
        connect_timeout=5,
        request_timeout=3600,
        validate_cert=False,
    )
    print(f'{status=},\n{headers=},\n{body=}')

async def test_post():
    print('-'*30)
    print('Start POST request.')
    url = 'https://httpbin.org/post'
    method = 'POST'
    status, headers, body = await fetch_sonic(
        url,
        method=method,
        body= {'data_test': 'data_test'},
        connect_timeout=5,
        request_timeout=3600,
        validate_cert=False,
    )
    print(f'{status=},\n{headers=},\n{body=}')

async def test_put():
    print('-'*30)
    print('Start PUT request.')
    url = 'https://httpbin.org/put'
    method = 'PUT'
    status, headers, body = await fetch_sonic(
        url,
        method=method,
        body= {'data_test': 'data_test'},
        connect_timeout=5,
        request_timeout=3600,
        validate_cert=False,
    )
    print(f'{status=},\n{headers=},\n{body=}')

async def test_delete():
    print('-'*30)
    print('Start DELETE request.')
    url = 'https://httpbin.org/delete'
    method = 'DELETE'
    status, headers, body = await fetch_sonic(
        url,
        method=method,
        connect_timeout=5,
        request_timeout=3600,
        validate_cert=False,
    )
    print(f'{status=},\n{headers=},\n{body=}')



async def main():
    await test_get()
    # await test_post()
    # await test_put()
    # await test_delete()

if __name__ == '__main__':
    asyncio.run(main())
