import base64
import asyncio
from tqdm import tqdm
from typing import Optional, Tuple, Dict, Any
import httpx

DEFAULT_CONNECT_TIMEOUT = 10
DEFAULT_REQUEST_TIMEOUT = 3600
DEFAULT_BUFFER_SIZE = 128 * 1024
DEFAULT_MAX_REDIRECTS = 5


async def fetch_httpx(
        url: str,
        method: str = "GET",
        headers: Dict = None,
        body: Dict = None, # Optional[bytes]
        connect_timeout=DEFAULT_CONNECT_TIMEOUT,
        request_timeout=DEFAULT_REQUEST_TIMEOUT,
        # resolver=resolve,
        # max_buffer_size=DEFAULT_BUFFER_SIZE,
        follow_redirects: bool = False,
        max_redirects=DEFAULT_MAX_REDIRECTS,
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
        proxy = httpx.Proxy(url=proxies)
    else:
        proxy = None
    # Sending a request
    async with httpx.AsyncClient(proxies=proxy, verify=validate_cert, max_redirects=max_redirects) as client:
        timeouts = httpx.Timeout(read=request_timeout, connect=connect_timeout, pool=None, write=None)
        if method == "GET":
            response = await client.get(url, headers=headers)
        elif method == "POST":
            response = await client.post(url, headers=headers, timeout=timeouts, data=body, follow_redirects=follow_redirects)
        elif method == "PUT":
            response = await client.put(url, headers=headers, timeout=timeouts,  data="" if body is None else body, follow_redirects=follow_redirects)
        elif method == "DELETE":
            response = await client.delete(url, headers=headers, timeout=timeouts, follow_redirects=follow_redirects)
        status = response.status_code
        headers = dict(response.headers)
        body = await response.aread()
        # await response.connection.release()
    return (status, headers, body)


async def test_get():
    print('-'*30)
    print('Start GET request.')
    url = 'https://httpbin.org/get'
    method = 'GET'
    status, headers, body = await fetch_httpx(
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
    status, headers, body = await fetch_httpx(
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
    status, headers, body = await fetch_httpx(
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
    status, headers, body = await fetch_httpx(
        url,
        method=method,
        connect_timeout=5,
        request_timeout=10,
        validate_cert=False,
    )
    print(f'{status=},\n{headers=},\n{body=}')



async def main():
    await test_get()
    await test_post()
    await test_put()
    await test_delete()

if __name__ == '__main__':
    asyncio.run(main())
