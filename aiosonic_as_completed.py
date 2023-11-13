"""

Отрабатывает но HTTPClient контекста зависает
"""
import aiosonic
import asyncio


async def main():
    urls = [
        'https://www.google.com/',
        'https://www.google.com/',
        'https://www.google.com/',
        'https://www.google.com/',
    ]
    async with aiosonic.HTTPClient() as client:
        # asyncio.gather is the key for concurrent requests.
        # responses = await asyncio.gather(*[client.get(url) for url in urls])
        ls_cur = [client.get(url) for url in urls]
        for cur in asyncio.as_completed(ls_cur):
            result = await cur
            print(result.status_code)

        # потоковых/частичных ответов не освобождает установленное соединение
        # из пула, пока ответ не будет прочитан, поэтому лучше прочитать
        # это.
        # for response in responses:
        #     if response.chunked:
        #         await response.text()
        #
        # assert all([res.status_code in [200, 301] for res in responses])

loop = asyncio.get_event_loop()
loop.run_until_complete(main())