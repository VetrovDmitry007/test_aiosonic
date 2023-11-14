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
        headers=None,
        body: Dict = None, # Optional[bytes]
        connect_timeout=DEFAULT_CONNECT_TIMEOUT,
        request_timeout=DEFAULT_REQUEST_TIMEOUT,
        # resolver=resolve,
        max_buffer_size=DEFAULT_BUFFER_SIZE,
        follow_redirects: bool = False,
        max_redirects=DEFAULT_MAX_REDIRECTS,
        validate_cert: bool = False,  # config.http_client.validate_certs,
        allow_proxy: bool = False,
        proxies=None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        content_encoding: Optional[str] = None,
        eof_mark: Optional[bytes] = None,
) -> Tuple[int, Dict[str, Any], bytes]:

    if proxies and allow_proxy:
        proxy = Proxy(host=proxies, auth=f'{user}: {password}')
    else:
        proxy = None
    async with aiosonic.HTTPClient(verify_ssl=validate_cert, proxy=proxy) as client:
        timeouts = Timeouts(sock_read=request_timeout, sock_connect=connect_timeout)
        match method:
            case "GET":
                response = await client.get(url, headers=headers, timeouts=timeouts)
            case "POST":
                response = await client.post(url, headers=headers, timeouts=timeouts, data=body)
            case "PUT":
                response = await client.put(url, headers=headers, timeouts=timeouts,  data="" if body is None else body)
            case "DELETE":
                response = await client.delete(url, headers=headers, timeouts=timeouts)
        status = response.status_code
        headers = dict(response.headers)
        body = response.body
        # body = await response.content()
        await response.connection.release()
    return (status, headers, body)


async def test_get():
    url = 'https://httpbin.org/get'
    # url = 'https://www.google.com/'
    method = 'GET'
    status, headers, body = await fetch_sonic(
        url,
        method=method,
        body=None,
        connect_timeout=5,
        request_timeout=3600,
        validate_cert=False,
    )
    print(f'{status=},\n{headers=},\n{body=}')

async def main():
    await test_get()
    # await test_post()

if __name__ == '__main__':
    asyncio.run(main())
