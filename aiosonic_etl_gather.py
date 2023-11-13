"""
Пример из -- https://aiosonic.readthedocs.io/en/latest/examples.html#concurrent-requests

Работает
"""
import aiosonic
import asyncio

async def main():
    url = 'https://www.google.com/'

    async with aiosonic.HTTPClient() as client:
        responses = await asyncio.gather(*[client.get(url) for _ in range(20)])

        # потоковых/частичных ответов не освобождает установленное соединение
        # из пула, пока ответ не будет прочитан, поэтому лучше прочитать
        # это.
        for response in responses:
            if response.chunked:
                s = await response.text()
                print(s)

        assert all([res.status_code in [200, 301] for res in responses])

loop = asyncio.get_event_loop()
loop.run_until_complete(main())